from abc import ABC, abstractmethod

import psycopg2

from config import DB_NAME, USER, PASSWORD, HOST, PORT
from dataclass import User, UserResult, UserGet, ArticleResult, Article, ArticleUpdate, Like, LikeGet, LikeGetById, \
    Comment, CommentCreate, CommentById, CommentByName
from tokens import TokenGen


class AbstractModels(ABC):
    def __init__(self):
        self.param = {'database': DB_NAME,
                     'user': USER,
                     'password': PASSWORD,
                     'host': HOST,
                     'port': PORT}
        self.conn = psycopg2.connect(**self.param)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    @abstractmethod
    def get(self):
        '''
        get all resources
        :return: list of resources
        '''
        pass

    @abstractmethod
    def get_by_id(self, id: str):
        '''
        get resource by id
        :param id: id of resource
        :return: list of resource
        '''
        pass

    @abstractmethod
    def get_by_name(self, name: str):
        '''
        get resource by name
        :param name: name of resource
        :return: list of resource
        '''
        pass

    @abstractmethod
    def create(self, data):
        '''
        resource creation
        :param data: resource parameter dic
        :return: resource id or response code
        '''
        pass

    @abstractmethod
    def update(self, data):
        '''
        resource updating
        :param data: resource parameter dic
        :return: response code
        '''
        pass

    @abstractmethod
    def delete(self):
        '''
        deleting all resources
        :return: response code
        '''
        pass

    @abstractmethod
    def delete_by_id(self, id: str):
        '''
        deleting a resource by id
        :param id: id of the resource to be deleted
        :return: response code
        '''
        pass

    @abstractmethod
    def delete_by_name(self, name: str):
        '''
        deleting a resource by name
        :param name: name of the resource to be deleted
        :return: response code
        '''
        pass

    def __del__(self):
        self.cur.close()
        self.conn.close()


class AuthModel():
    def __init__(self):
        self.param = {'database': DB_NAME,
                     'user': USER,
                     'password': PASSWORD,
                     'host': HOST,
                     'port': PORT }
        self.conn = psycopg2.connect(**self.param)
        self.cur = self.conn.cursor()

    def authorization(self, token: str) -> tuple :
        sql = f"SELECT user_id FROM tokens WHERE token = '{token}'"
        try:
            self.cur.execute(sql)
            user_id = self.cur.fetchone()
            if user_id:
                return user_id
            else:
                raise SystemError("Authorization DB : NO DATA")
        except psycopg2.OperationalError as err:
            raise SystemError(f"Authorization DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Authorization DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Authorization DB: Error, {err}")

    def __del__(self):
        self.cur.close()
        self.conn.close()


class UserModels(AbstractModels):
    def get(self) -> list:
        sql = 'SELECT name, first_name, last_name, age\
               FROM users\
               where is_deleted = false;'
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
            result = [UserGet(name=val[0], first_name=val[1], last_name=val[2], age=val[3]) for val in values]
            return result
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get all users DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get all users DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get all users DB: Error, {err}")

    def get_by_id(self, user_id: str) -> UserGet:
        sql = f'SELECT  name, first_name, last_name, age\
                FROM users\
                WHERE id = {user_id}\
                AND is_deleted = false;'
        try:
            self.cur.execute(sql)
            val = self.cur.fetchone()
            if val:
                result = UserGet(name=val[0], first_name=val[1], last_name=val[2], age=val[3])
                return result
            else:
                raise SystemError("Get user by id DB: NO DATA")
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get user by id DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get user by id DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get user by id DB: Error, {err}")

    def get_by_name(self, name: str) -> UserGet:
        sql = f'SELECT name, first_name, last_name, age\
                FROM users\
                WHERE name = {name} \
                AND is_deleted = false;'
        try:
            self.cur.execute(sql)
            val = self.cur.fetchone()
            if val:
                result = UserGet(name=val[0], first_name=val[1], last_name=val[2], age=val[3])
                return result
            else:
                raise SystemError("Get user by name 'DB': NO DATA")
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get user by name DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get user by name DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get user by name DB: Error, {err}")

    def create(self, new_user: User) -> UserResult:
        tg = TokenGen()
        try:
            sql = f"SELECT max(id) FROM users;"
            self.cur.execute(sql)
            user_id = self.cur.fetchone()
            user_id = user_id[0] + 1
            token = tg.generate(user_id)
            sql = f"BEGIN; \
                  INSERT INTO users(id, name, password, first_name, last_name, age)\
                           VALUES('{user_id}', '{new_user.name}', '{new_user.password}', '{new_user.first_name}',\
                           '{new_user.last_name}', '{new_user.age}');\
                  INSERT INTO tokens (user_id, token) VALUES ({user_id}, '{token}');\
                  COMMIT;"
            self.cur.execute(sql)
            result = UserResult(user_id=user_id, token=token)
            return result
        except psycopg2.DatabaseError as err:
            raise SystemError(f"Create new user DB: Error, {err}")

    def update(self, user_update: User) -> bool:
        dict_user_update = {"name": user_update.name, "password": user_update.password,
                            "first_name": user_update.first_name, "last_name": user_update.last_name,
                            "age": user_update.age}
        keys = ('name', 'password', 'first_name', 'last_name', 'age')
        sql = f"SELECT name, password  FROM users\
                WHERE first_name = '{user_update.first_name}'\
                AND last_name = '{user_update.last_name}' \
                AND  age = '{user_update.age}';"
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
            values = values[0]
            dict_from_db = dict(zip(keys, values))
            dict_for_db = {**dict_from_db, **dict_user_update}
            sql = f"UPDATE users SET name = '{dict_for_db.get('name')}',\
                    password = '{dict_for_db.get('password')}'\
                    WHERE first_name = '{user_update.first_name}'\
                    AND last_name = '{user_update.last_name}' \
                    AND  age = '{user_update.age}' \
                    AND is_deleted = false;"
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Update user DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Update user DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Update user DB: Error, {err}")

    def delete(self) -> bool:
        sql = "UPDATE users SET is_deleted = true;"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete all users DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete all users DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete all users DB: Error, {err}")

    def delete_by_id(self, user_id: str) -> bool:
        sql = f"UPDATE users\
                SET is_deleted = true\
                WHERE id = {user_id};"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete user by id DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete user by id DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete user by id DB: Error, {err}")

    def delete_by_name(self, name: str) -> bool:
        sql = f"UPDATE users\
              SET is_deleted = true\
              WHERE name = {name};"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete user by name DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete user by name DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete user by name DB: Error, {err}")


class ArticleModels(AbstractModels):
    def get(self) -> list:
        sql = 'SELECT name, article_text, pub_date, users_id\
               FROM articles\
               where is_deleted = false;'
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
            result = [Article(name=val[0], text=val[1], date=val[2], user_id=val[3]) for val in values]
            return result
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get all articles DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get all articles DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get all articles DB: Error, {err}")

    def get_by_id(self, article_id: int) -> Article:
        sql = f'SELECT name, article_text, pub_date, users_id\
                FROM articles\
                WHERE id = {article_id}\
                AND is_deleted = false;'
        try:
            self.cur.execute(sql)
            val = self.cur.fetchone()
            if val:
                result = Article(name=val[0], text=val[1], date=val[2], user_id=val[3])
                return result
            else:
                raise SystemError("Get article by id 'DB': NO DATA")
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get article by id DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get article by id DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get article by id DB: Error, {err}")

    def get_by_name(self, name: str) -> Article:
        sql = f'SELECT name, article_text, pub_date, users_id\
                FROM articles\
                WHERE name = {name} \
                AND is_deleted = false;'
        try:
            self.cur.execute(sql)
            val = self.cur.fetchone()
            if val:
                result = Article(name=val[0], text=val[1], date=val[2], user_id=val[3])
                return result
            else:
                raise SystemError("Get article by name 'DB': NO DATA")
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get article by name DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get article by name DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get article by name DB: Error, {err}")

    def create(self, new_article: Article) -> ArticleResult:
        sql = f"INSERT INTO articles(name, article_text, pub_date, users_id)\
                VALUES('{new_article.name}', '{new_article.text}', '{new_article.date}','{new_article.author_id}')\
                RETURNING id;"
        try:
            self.cur.execute(sql)
            value = self.cur.fetchone()
            result = ArticleResult(article_id=value[0])
            return result
        except psycopg2.OperationalError as err:
            raise SystemError(f"Create new article  DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Create new article DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Create new article DB: Error, {err}")

    def update(self, article_update: ArticleUpdate) -> bool:
        keys = ('article_id', 'name', 'text', 'date')
        sql = f"SELECT name, article_text, pub_date FROM articles\
                WHERE id = '{article_update['id']}';"
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
            values = values[0]
            dict_from_db = dict(zip(keys, values))
            dict_for_db = {**dict_from_db, **article_update}
            sql = f"UPDATE articles SET name = '{dict_for_db.get('name')}',\
                    article_text = '{dict_for_db.get('text')}',\
                    pub_date = '{dict_for_db.get('date')}'\
                    WHERE id = '{article_update['id']}' \
                    AND is_deleted = false;"
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Update article DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Update article DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Update article DB: Error, {err}")

    def delete(self) -> bool:
        sql = "UPDATE articles SET is_deleted = true;"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete all articles DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete all articles DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete all articles DB: Error, {err}")

    def delete_by_id(self, article_id: str) -> bool:
        sql = f"UPDATE articles\
                SET is_deleted = true\
                WHERE id = {article_id};"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete article by id DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete article by id DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete article by id DB: Error, {err}")

    def delete_by_name(self, name: str) -> bool:
        sql = f"UPDATE articles\
              SET is_deleted = true\
              WHERE name = '{name}';"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete article by name DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete article by name DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete article by name DB: Error, {err}")


class LikeModels(AbstractModels):
    def get(self) -> list:
        sql = "select name, count(article_like.users_id)\
              from articles\
              inner join article_like\
              on articles.id = article_like.articles_id\
              where article_like.is_deleted = false\
              and articles.is_deleted = false\
              group by name\
              order by count desc;"
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
            result = [LikeGet(article_name=val[0], likes=val[1]) for val in values]
            return result
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get all likes DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get all likes DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get all likes DB: Error, {err}")

    def get_by_id(self, article_id: int) -> list:
        sql = f'select articles.name, users.name\
                from articles\
                inner join article_like\
                on article_like.articles_id = articles.id\
                inner join users\
                on article_like.users_id = users.id\
                where articles.id = {article_id}\
                and articles.is_deleted = false\
                and article_like.is_deleted = false;'
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
            if values:
                result = [LikeGetById(article_name=val[0], user_name=val[1]) for val in values]
                return result
            else:
                raise SystemError("Get like by id 'DB': NO DATA")
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get like by id DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get like by id DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get like by id DB: Error, {err}")

    def get_by_name(self, name: str) -> list:
        sql = f"select articles.name, users.name\
                from articles\
                inner join article_like\
                on article_like.articles_id = articles.id\
                inner join users\
                on article_like.users_id = users.id\
                where articles.name = {name}\
                and article_like.is_deleted = false\
                and articles.is_deleted = false;"
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
            if values:
                result = [LikeGetById(article_name=val[0], user_name=val[1]) for val in values]
                return result
            else:
                raise SystemError("Get like by name 'DB': NO DATA")
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get like by name DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get like by name DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get like by name DB: Error, {err}")

    def create(self, new_like: Like) -> bool:
        sql = f"insert into article_like(articles_id, users_id)\
                values('{new_like.article_id}','{new_like.user_id}');"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Create new like DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Create new like DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Create new like DB: Error, {err}")

    def update(self, data: dict):
        pass

    def delete(self) -> bool:
        sql = "UPDATE article_like SET is_deleted = true;"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete all likes DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete all likes DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete all likes DB: Error, {err}")

    def delete_by_id(self, delete_like: Like) -> bool:
        sql = f"update article_like set is_deleted = true where articles_id = {delete_like.article_id}\
                and users_id = {delete_like.user_id};"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete like by id DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete like by id DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete like by id DB: Error, {err}")

    def delete_by_name(self, delete_like: LikeGetById) -> bool:
        sql = f"update article_like set is_deleted = true where articles_id in\
                (select id from articles where name = '{delete_like.article_name}')\
                and users_id in\
                (select id from users where name ='{delete_like.user_name}');"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete like by name DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete like by name DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete like by name DB: Error, {err}")


class CommentModels(AbstractModels):
    def get(self) -> list:
        sql = "select articles.name, users.name, comments.comment_text\
               from articles\
               inner join comments\
               on comments.articles_id = articles.id\
               inner join users\
               on comments.users_id = users.id\
               and articles.is_deleted = false\
               and comments.is_deleted = false;"
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
            result = [Comment(article_name=val[0], user_name=val[1], comment=val[2]) for val in values]
            return result
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get all comments DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get all comments DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get all comments DB: Error, {err}")

    def get_by_id(self, article_id: str) -> list:
        sql = f'select articles.name, users.name, comments.comment_text\
                from articles\
                inner join comments\
                on comments.articles_id = articles.id\
                inner join users\
                on comments.users_id = users.id\
                where articles.id = {article_id}\
                and articles.is_deleted = false\
                and comments.is_deleted = false;'
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
            if values:
                result = [Comment(article_name=val[0], user_name=val[1], comment=val[2]) for val in values]
                return result
            else:
                raise SystemError("Get comment by id DB: NO DATA")
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get comment by id DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get comment by id DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get comment by id DB: Error, {err}")

    def get_by_name(self, name: str) -> list:
        sql = f"select articles.name, users.name, comments.comment_text\
                from articles\
                inner join comments\
                on comments.articles_id = articles.id\
                inner join users\
                on comments.users_id = users.id\
                where articles.name ={name}\
                and articles.is_deleted = false\
                and comments.is_deleted = false;"
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
            if values:
                result = [Comment(article_name=val[0], user_name=val[1], comment=val[2]) for val in values]
                return result
            else:
                raise SystemError("Get comment by name DB: NO DATA")
        except psycopg2.OperationalError as err:
            raise SystemError(f"Get comment by name DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Get comment by name DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Get comment by name DB: Error, {err}")

    def create(self, new_comment: CommentCreate) -> bool:
        sql = f"insert into comments(articles_id, users_id, comment_text)\
                values('{new_comment.article_id}', '{new_comment.user_id}', '{new_comment.comment}');"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Create new comment DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Create new comment DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Create new comment DB: Error, {err}")

    def update(self, comment_update: CommentCreate) -> bool:
        sql = f"update comments set comment_text = '{comment_update.comment}'\
                where articles_id = '{comment_update.article_id}'\
                and users_id = '{comment_update.user_id}' \
                and is_deleted = false;"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Update comment DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Update comment DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Update comment DB: Error, {err}")

    def delete(self) -> bool:
        sql = "UPDATE comments SET is_deleted = true;"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete all comments DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete all comments DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete all comments DB: Error, {err}")

    def delete_by_id(self, comment_delete: CommentById) -> bool:
        sql = f"update comments set is_deleted = true where articles_id = {comment_delete.article_id}\
                and users_id = {comment_delete.user_id};"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete comment by id DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete comment by id DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete comment by id DB: Error, {err}")

    def delete_by_name(self, comment_delete: CommentByName) -> bool:
        sql = f"update comments set is_deleted = true where articles_id in\
                (select id from articles where name = {comment_delete.article_name})\
                and users_id in\
                (select id from users where name ={comment_delete.user_name});"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.OperationalError as err:
            raise SystemError(f"Delete comment by name DB: Operational Error, {err}")
        except psycopg2.InternalError as err:
            raise SystemError(f"Delete comment by name DB: Internal Error, {err}")
        except psycopg2.Error as err:
            raise SystemError(f"Delete comment by name DB: Error, {err}")


def main():
    pass


if __name__ == '__main__':
    main()






