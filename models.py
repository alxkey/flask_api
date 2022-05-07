from abc import ABC, abstractmethod

import psycopg2

from config import DB_NAME, USER, PASSWORD, HOST, PORT
from dataclass import User, UserUpdate, UserResult, UserGet, ArticleResult, Article, ArticleUpdate, Like, LikeGet, \
    LikeGetById, Comment, CommentCreate, CommentById, CommentByName
from decorators import try_catch
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

    @try_catch
    def authorization(self, token: str) -> tuple:
        '''
        User  authorization by token
        :param token: user token
        :return: user_id corresponding to the token
        '''
        sql = f"SELECT user_id FROM tokens WHERE token = '{token}'"
        self.cur.execute(sql)
        user_id = self.cur.fetchone()
        if user_id:
            return user_id
        else:
            raise SystemError("Authorization DB : NO DATA")

    def __del__(self):
        self.cur.close()
        self.conn.close()


class UserModels(AbstractModels):
    @try_catch
    def get(self) -> list:
        '''
        Getting data from all users.
        :return: data from all users
        '''
        sql = 'SELECT name, first_name, last_name, age\
               FROM users\
               where is_deleted = false;'
        self.cur.execute(sql)
        values = self.cur.fetchall()
        result = [UserGet(name=val[0],
                          first_name=val[1],
                          last_name=val[2],
                          age=val[3]) for val in values]
        return result

    @try_catch
    def get_by_id(self, user_id: str) -> UserGet:
        '''
        Getting user data by id
        :param user_id: - unique user identifier
        :return: instance of user dataclass
        '''
        sql = f'SELECT  name, first_name, last_name, age\
                FROM users\
                WHERE id = {user_id}\
                AND is_deleted = false;'
        self.cur.execute(sql)
        val = self.cur.fetchone()
        if val:
            result = UserGet(name=val[0],
                             first_name=val[1],
                             last_name=val[2],
                             age=val[3])
            return result
        else:
            raise SystemError("Get user by id DB: NO DATA")

    @try_catch
    def get_by_name(self, name: str) -> UserGet:
        '''
        Getting user data by id
        :param name: - unique user nic name
        :return: instance of user dataclass
        '''
        sql = f'SELECT name, first_name, last_name, age\
                FROM users\
                WHERE name = {name} \
                AND is_deleted = false;'
        self.cur.execute(sql)
        val = self.cur.fetchone()
        if val:
            result = UserGet(name=val[0],
                             first_name=val[1],
                             last_name=val[2],
                             age=val[3])
            return result
        else:
            raise SystemError("Get user by name 'DB': NO DATA")

    def create(self, new_user: User) -> UserResult:
        '''
        Creating new user
        :param new_user: instance of user dataclass
        :return: instance of user result dataclass (user_id, token)
        '''
        tg = TokenGen()
        try:
            sql = f"SELECT max(id) FROM users;"
            self.cur.execute(sql)
            user_id = self.cur.fetchone()
            user_id = user_id[0] + 1
            token = tg.generate(user_id)
            sql = f"BEGIN; \
                  INSERT INTO users(id, name, password, first_name, last_name, age)\
                           VALUES('{user_id}', \
                                  '{new_user.name}', \
                                  '{new_user.password}', \
                                  '{new_user.first_name}',\
                                  '{new_user.last_name}',\
                                  '{new_user.age}');\
                  INSERT INTO tokens (user_id, token) VALUES ({user_id}, '{token}');\
                  COMMIT;"
            self.cur.execute(sql)
            result = UserResult(user_id=user_id, token=token)
            return result
        except psycopg2.DatabaseError as err:
            raise SystemError(f"Create new user DB: Error, {err}")

    @try_catch
    def update(self, user_update: UserUpdate) -> bool:
        '''
        User updating
        :param user_update: instance of user update  dataclass
        :return: - successful updating response
        '''
        sql = f"UPDATE users SET name = '{user_update.name}',\
                          password = '{user_update.password}',\
                          first_name = '{user_update.first_name}',\
                          last_name = '{user_update.last_name}',\
                          age = '{user_update.age}'\
                WHERE id = '{user_update.user_id}';"
        self.cur.execute(sql)
        return True

    @try_catch
    def delete(self) -> bool:
        '''
        Removing data from all users.
        :return: - successful delete response
        '''
        sql = "UPDATE users SET is_deleted = true;"
        self.cur.execute(sql)
        return True

    @try_catch
    def delete_by_id(self, user_id: str) -> bool:
        '''
        User removing by id
        :param user_id: - unique user identifier
        :return: - successful delete response
        '''
        sql = f"UPDATE users\
                SET is_deleted = true\
                WHERE id = {user_id};"
        self.cur.execute(sql)
        return True

    @try_catch
    def delete_by_name(self, name: str) -> bool:
        '''
        User removing by name
        :param name: - unique user nic name
        :return: - successful delete response
        '''
        sql = f"UPDATE users\
              SET is_deleted = true\
              WHERE name = {name};"
        self.cur.execute(sql)
        return True


class ArticleModels(AbstractModels):
    @try_catch
    def get(self) -> list:
        '''
        Getting data from all articles.
        :return:  data from all articles
        '''
        sql = 'SELECT name, article_text, pub_date, users_id\
               FROM articles\
               where is_deleted = false;'
        self.cur.execute(sql)
        values = self.cur.fetchall()
        result = [Article(name=val[0],
                          text=val[1],
                          date=val[2],
                          user_id=val[3]) for val in values]
        return result

    @try_catch
    def get_by_id(self, article_id: str) -> Article:
        '''
        Getting article by id
        :param article_id: unique article identifier
        :return: instance of article dataclass
        '''
        sql = f'SELECT name, article_text, pub_date, users_id\
                FROM articles\
                WHERE id = {article_id}\
                AND is_deleted = false;'
        self.cur.execute(sql)
        val = self.cur.fetchone()
        if val:
            result = Article(name=val[0],
                             text=val[1],
                             date=val[2],
                             user_id=val[3])
            return result
        else:
            raise SystemError("Get article by id 'DB': NO DATA")

    @try_catch
    def get_by_name(self, name: str) -> Article:
        '''
        Getting article by title
        :param name: article title
        :return: instance of article dataclass
        '''
        sql = f'SELECT name, article_text, pub_date, users_id\
                FROM articles\
                WHERE name = {name} \
                AND is_deleted = false;'
        self.cur.execute(sql)
        val = self.cur.fetchone()
        if val:
            result = Article(name=val[0],
                             text=val[1],
                             date=val[2],
                             user_id=val[3])
            return result
        else:
            raise SystemError("Get article by name 'DB': NO DATA")

    @try_catch
    def create(self, new_article: Article) -> ArticleResult:
        '''
        Creating new article
        :param new_article: instance of article dataclass
        :return: unique article identifier as dataclass
        '''
        sql = f"INSERT INTO articles(name, article_text, pub_date, users_id)\
                VALUES('{new_article.name}', '{new_article.text}', '{new_article.date}','{new_article.author_id}')\
                RETURNING id;"
        self.cur.execute(sql)
        value = self.cur.fetchone()
        result = ArticleResult(article_id=value[0])
        return result

    @try_catch
    def update(self, article_update: ArticleUpdate) -> bool:
        '''
        Updating article
        :param article_update: instance of article dataclass
        :return: - successful update response
        '''
        sql = f"UPDATE articles SET name = '{article_update.name}',\
                article_text = '{article_update.text}',\
                pub_date = '{article_update.date}',\
                users_id = '{article_update.user_id}'\
                WHERE id = '{article_update.article_id}'\
                AND is_deleted = false;"
        self.cur.execute(sql)
        return True

    @try_catch
    def delete(self) -> bool:
        '''
        Removing data from all articles.
        :return: - successful delete response
        '''
        sql = "UPDATE articles SET is_deleted = true;"
        self.cur.execute(sql)
        return True

    @try_catch
    def delete_by_id(self, article_id: str) -> bool:
        '''
        Article removing by id
        :param article_id: unique article identifier
        :return: - successful delete response
        '''
        sql = f"UPDATE articles\
                SET is_deleted = true\
                WHERE id = {article_id};"
        self.cur.execute(sql)
        return True

    @try_catch
    def delete_by_name(self, name: str) -> bool:
        '''
        Article removing by title
        :param name: article title
        :return: - successful delete response
        '''
        sql = f"UPDATE articles\
              SET is_deleted = true\
              WHERE name = '{name}';"
        self.cur.execute(sql)
        return True


class LikeModels(AbstractModels):
    @try_catch
    def get(self) -> list:
        '''
        Getting data from all likes.
        :return: data from all likes
        '''
        sql = "select name, count(article_like.users_id)\
              from articles\
              inner join article_like\
              on articles.id = article_like.articles_id\
              where article_like.is_deleted = false\
              and articles.is_deleted = false\
              group by name\
              order by count desc;"
        self.cur.execute(sql)
        values = self.cur.fetchall()
        result = [LikeGet(article_name=val[0],
                          likes=val[1]) for val in values]
        return result

    @try_catch
    def get_by_id(self, article_id: str) -> list:
        '''
        Getting likes by article id
        :param article_id: unique article identifier
        :return: data of likes
        '''
        sql = f'select articles.name, users.name\
                from articles\
                inner join article_like\
                on article_like.articles_id = articles.id\
                inner join users\
                on article_like.users_id = users.id\
                where articles.id = {article_id}\
                and articles.is_deleted = false\
                and article_like.is_deleted = false;'
        self.cur.execute(sql)
        values = self.cur.fetchall()
        if values:
            result = [LikeGetById(article_name=val[0],
                                  user_name=val[1]) for val in values]
            return result
        else:
            raise SystemError("Get like by id 'DB': NO DATA")

    @try_catch
    def get_by_name(self, name: str) -> list:
        '''
        Getting likes by article title
        :param name: article title
        :return: data of likes
        '''
        sql = f"select articles.name, users.name\
                from articles\
                inner join article_like\
                on article_like.articles_id = articles.id\
                inner join users\
                on article_like.users_id = users.id\
                where articles.name = {name}\
                and article_like.is_deleted = false\
                and articles.is_deleted = false;"
        self.cur.execute(sql)
        values = self.cur.fetchall()
        if values:
            result = [LikeGetById(article_name=val[0],
                                  user_name=val[1]) for val in values]
            return result
        else:
            raise SystemError("Get like by name 'DB': NO DATA")

    @try_catch
    def create(self, new_like: Like) -> bool:
        '''
        Creating new like
        :param new_like: instance of like dataclass
        :return: successful create response
        '''
        sql = f"insert into article_like(articles_id, users_id)\
                values('{new_like.article_id}','{new_like.user_id}');"
        self.cur.execute(sql)
        return True

    def update(self, data: dict):
        pass

    @try_catch
    def delete(self) -> bool:
        '''
        Removing data from all likes.
        :return: - successful delete response
        '''
        sql = "UPDATE article_like SET is_deleted = true;"
        self.cur.execute(sql)
        return True

    @try_catch
    def delete_by_id(self, delete_like: Like) -> bool:
        '''
        Like removing by article id  and user id
        :param delete_like: instance of like dataclass
        :return: - successful delete response
        '''
        sql = f"update article_like set is_deleted = true where articles_id = {delete_like.article_id}\
                and users_id = {delete_like.user_id};"
        self.cur.execute(sql)
        return True

    @try_catch
    def delete_by_name(self, delete_like: LikeGetById) -> bool:
        '''
        Like removing by article title and user nic name
        :param delete_like: instance of like dataclass
        :return: - successful delete response
        '''
        sql = f"update article_like set is_deleted = true where articles_id in\
                (select id from articles where name = '{delete_like.article_name}')\
                and users_id in\
                (select id from users where name ='{delete_like.user_name}');"
        self.cur.execute(sql)
        return True


class CommentModels(AbstractModels):
    @try_catch
    def get(self) -> list:
        '''
        Getting data from all comments.
        :return: data from all comments
        '''
        sql = "select articles.name, users.name, comments.comment_text\
               from articles\
               inner join comments\
               on comments.articles_id = articles.id\
               inner join users\
               on comments.users_id = users.id\
               and articles.is_deleted = false\
               and comments.is_deleted = false;"
        self.cur.execute(sql)
        values = self.cur.fetchall()
        result = [Comment(article_name=val[0],
                          user_name=val[1],
                          comment=val[2]) for val in values]
        return result

    @try_catch
    def get_by_id(self, article_id: str) -> list:
        '''
        Getting comments by article id
        :param article_id: unique article identifier
        :return: data of comments
        '''
        sql = f'select articles.name, users.name, comments.comment_text\
                from articles\
                inner join comments\
                on comments.articles_id = articles.id\
                inner join users\
                on comments.users_id = users.id\
                where articles.id = {article_id}\
                and articles.is_deleted = false\
                and comments.is_deleted = false;'
        self.cur.execute(sql)
        values = self.cur.fetchall()
        if values:
            result = [Comment(article_name=val[0],
                              user_name=val[1],
                              comment=val[2]) for val in values]
            return result
        else:
            raise SystemError("Get comment by id DB: NO DATA")

    @try_catch
    def get_by_name(self, name: str) -> list:
        '''
        Getting comments by article title
        :param name: article title
        :return: data of comments
        '''
        sql = f"select articles.name, users.name, comments.comment_text\
                from articles\
                inner join comments\
                on comments.articles_id = articles.id\
                inner join users\
                on comments.users_id = users.id\
                where articles.name ={name}\
                and articles.is_deleted = false\
                and comments.is_deleted = false;"
        self.cur.execute(sql)
        values = self.cur.fetchall()
        if values:
            result = [Comment(article_name=val[0],
                              user_name=val[1],
                              comment=val[2]) for val in values]
            return result
        else:
            raise SystemError("Get comment by name DB: NO DATA")

    @try_catch
    def create(self, new_comment: CommentCreate) -> bool:
        '''
        Crearting new comment
        :param new_comment: instance of comment dataclass
        :return: - successful creating response
        '''
        sql = f"insert into comments(articles_id, users_id, comment_text)\
                values('{new_comment.article_id}', '{new_comment.user_id}', '{new_comment.comment}');"
        self.cur.execute(sql)
        return True

    @try_catch
    def update(self, comment_update: CommentCreate) -> bool:
        '''
        Comment updating
        :param comment_update: instance of comment dataclass
        :return: - successful updating response
        '''
        sql = f"update comments set comment_text = '{comment_update.comment}'\
                where articles_id = '{comment_update.article_id}'\
                and users_id = '{comment_update.user_id}' \
                and is_deleted = false;"
        self.cur.execute(sql)
        return True

    @try_catch
    def delete(self) -> bool:
        '''
        Removing data from all comments.
        :return: - successful delete response
        '''
        sql = "UPDATE comments SET is_deleted = true;"
        self.cur.execute(sql)
        return True

    @try_catch
    def delete_by_id(self, comment_delete: CommentById) -> bool:
        '''
        Removing comment by article id and user id
        :param comment_delete: instance of comment dataclass
        :return: - successful delete response
        '''
        sql = f"update comments set is_deleted = true where articles_id = {comment_delete.article_id}\
                and users_id = {comment_delete.user_id};"
        self.cur.execute(sql)
        return True

    @try_catch
    def delete_by_name(self, comment_delete: CommentByName) -> bool:
        '''
        Removing comment by article title and user nic name
        :param comment_delete: instance of comment dataclass
        :return: - successful delete response
        '''
        sql = f"update comments set is_deleted = true where articles_id in\
                (select id from articles where name = {comment_delete.article_name})\
                and users_id in\
                (select id from users where name ={comment_delete.user_name});"
        self.cur.execute(sql)
        return True


def main():
    pass


if __name__ == '__main__':
    main()






