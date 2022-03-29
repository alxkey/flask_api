from abc import ABC, abstractmethod

import psycopg2
from flask import make_response

from config import DB_NAME, USER, PASSWORD, HOST, PORT
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
    def create(self, data: dict):
        '''
        resource creation
        :param data: resource parameter dic
        :return: resource id or response code
        '''
        pass

    @abstractmethod
    def update(self, data: dict):
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

    def authorization(self, token: str) -> tuple or None :
        sql = f"SELECT user_id FROM tokens WHERE token = '{token}'"
        try:
            self.cur.execute(sql)
            id = self.cur.fetchone()
            return id
        except psycopg2.Error:
            return None

    def __del__(self):
        self.cur.close()
        self.conn.close()


class UserModels(AbstractModels):
    def get(self) -> list or None:
        keys = ('nick_name', 'first_name', 'last_name','age')
        sql = 'SELECT name, first_name, last_name, age\
               FROM users\
               where is_deleted = false;'
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
        except psycopg2.Error:
            return None
        else:
            response = []
            for value in values:
                result = dict(zip(keys, value))
                response.append(result)
            #logger
            return response

    def get_by_id(self, user_id: str) -> dict or None:
        keys = ('nick_name', 'first_name', 'last_name','age')
        sql = f'SELECT  name, first_name, last_name, age\
                FROM users\
                WHERE id = {user_id}\
                AND is_deleted = false;'
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
        except psycopg2.Error:
            return None
        else:
            values = values[0]
            response = dict(zip(keys, values))
            return response

    def get_by_name(self, name: str) -> dict or None:
        keys = ('nick_name', 'first_name', 'last_name','age')
        sql = f'SELECT  name, first_name, last_name, age\
                FROM users\
                WHERE name = {name} \
                AND is_deleted = false;'
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
        except psycopg2.Error:
            return None
        else:
            values = values[0]
            response = dict(zip(keys, values))
            return response

    def create(self, data: dict) -> dict or None:
        tg = TokenGen()

        try:
            sql = f"SELECT max(id) FROM users;"
            self.cur.execute(sql)
            user_id = self.cur.fetchone()
            token = tg.generate(user_id)
            sql = f"BEGIN; \
                  INSERT INTO users(name, password, first_name, last_name, age)\
                           VALUES('{data['nick_name']}', '{data['password']}', '{data['first_name']}',\
                           '{data['last_name']}', '{data['age']}');\
                  INSERT INTO tokens (user_id, token) VALUES ({user_id}, '{token}');\
                  COMMIT;"
            self.cur.execute(sql)
            result = {'user_id': user_id, 'token': token}
            return result
        except(Exception, psycopg2.DatabaseError) as error:
            result = None
            return result

    def update(self, data: dict) -> bool or None:
        keys = ('name', 'text', 'date')
        sql = f"SELECT name, article_text, pub_date FROM articles\
                WHERE id = '{data['id']}';"
        try:
            self.cur.execute(sql)
            values = self.cur.fetchall()
            values = values[0]
            dict_from_db = dict(zip(keys, values))
            dict_for_db = {**dict_from_db, **data}
            sql = f"UPDATE articles SET name = '{dict_for_db.get('name')}',\
                    article_text = '{dict_for_db.get('text')}',\
                    pub_date = '{dict_for_db.get('date')}'\
                    WHERE id = '{data['id']}' \
                    AND is_deleted = false;"
            self.cur.execute(sql)
            return True
        except psycopg2.Error:
            return None

    def delete(self) -> bool or None:
        sql = "UPDATE users SET is_deleted = true;"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.Error:
            return None

    def delete_by_id(self, user_id: str) -> bool or None:
        sql = f"UPDATE users\
                SET is_deleted = true\
                WHERE id = {user_id};"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.Error:
            return None

    def delete_by_name(self, name: str) -> bool or None:
        sql = f"UPDATE users\
              SET is_deleted = true\
              WHERE name = {name};"
        try:
            self.cur.execute(sql)
            return True
        except psycopg2.Error:
            return None


class ArticleModels(AbstractModels):
    def get(self):
        keys = ('title', 'date', 'author_id')
        sql = 'SELECT name, pub_date, users_id\
               FROM articles\
               where is_deleted = false;'
        self.cur.execute(sql)
        values = self.cur.fetchall()
        response = []
        for value in values:
            result = dict(zip(keys, value))
            response.append(result)
        return response

    def get_by_id(self, article_id: str) -> dict:
        keys = ('title', 'text', 'date', 'author_id')
        sql = f'SELECT name, article_text, pub_date, users_id\
                FROM articles\
                WHERE id = {article_id}\
                AND is_deleted = false;'
        self.cur.execute(sql)
        values = self.cur.fetchall()
        values = values[0]
        response = dict(zip(keys, values))
        return response

    def get_by_name(self, name: str) -> dict:
        keys = ('title', 'text', 'date', 'author_id')
        sql = f'SELECT name, article_text, pub_date, users_id\
                FROM articles\
                WHERE name = {name} \
                AND is_deleted = false;'
        self.cur.execute(sql)
        values = self.cur.fetchall()
        values = values[0]
        response = dict(zip(keys, values))
        return response

    def create(self, new_article: dict) -> dict:
        sql = f"INSERT INTO articles(name, article_text, pub_date, users_id)\
                VALUES('{new_article['name']}', '{new_article['text']}', '{new_article['date']}',\
                '{new_article['author_id']}')\
                RETURNING id;"
        self.cur.execute(sql)
#        self.conn.commit()
        values = self.cur.fetchone()
        response = {'article_id': values[0]}
        return response

    def update(self, data: dict) -> str:
        keys = ('name', 'text', 'date')
        sql = f"SELECT name, article_text, pub_date FROM articles\
                WHERE id = '{data['id']}';"
        self.cur.execute(sql)
        values = self.cur.fetchall()
        values=values[0]
        dict_from_db = dict(zip(keys, values))
        dict_for_db = {**dict_from_db, **data}
        sql = f"UPDATE articles SET name = '{dict_for_db.get('name')}',\
                article_text = '{dict_for_db.get('text')}',\
                pub_date = '{dict_for_db.get('date')}'\
                WHERE id = '{data['id']}' \
                AND is_deleted = false;"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete(self) -> str:
        sql = "UPDATE articles SET is_deleted = true;"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_id(self, article_id: str) -> str:
        sql = f"UPDATE articles\
                SET is_deleted = true\
                WHERE id = {article_id};"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_name(self, name: str) -> str:
        sql = f"UPDATE articles\
              SET is_deleted = true\
              WHERE name = {name};"
        self.cur.execute(sql)
#        self.conn.commit()
        response = make_response("Ok 200", 200)      #########################################
        return response


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
        self.cur.execute(sql)
        response = self.cur.fetchall()
        return response

    def get_by_id(self, article_id: str) -> dict:
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
        response = self.cur.fetchall()
        return response

    def get_by_name(self, name: str) -> dict:
        sql = f"select articles.name, users.name\
                from articles\
                inner join article_like\
                on article_like.articles_id = articles.id\
                inner join users\
                on article_like.users_id = users.id\
                where articles.name = '{name}'\
                and article_like.is_deleted = false\
                and articles.is_deleted = false;"
        self.cur.execute(sql)
        response = self.cur.fetchall()
        return response

    def create(self, data: dict) -> dict:
        sql = f"insert into article_like(articles_id, users_id)\
                values('{data['article_id']}','{data['author_id']}');"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete(self) -> str:
        sql = "UPDATE article_like SET is_deleted = true;"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_id(self, article_id: str, author_id: str) -> str:
        sql = f"update article_like set is_deleted = true where articles_id = {article_id}\
                and users_id = {author_id};"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_name(self, title: str, name: str) -> str:
        sql = f"update article_like set is_deleted = true where articles_id in\
                (select id from articles where name = '{title}')\
                and users_id in\
                (select id from users where name ='{name}');"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200'
        return response


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
        self.cur.execute(sql)
        response = self.cur.fetchall()
        return response

    def get_by_id(self, article_id: str) -> dict:
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
        response = self.cur.fetchall()
        return response

    def get_by_name(self, name: str) -> dict:
        sql = f"select articles.name, users.name, comments.comment_text\
                from articles\
                inner join comments\
                on comments.articles_id = articles.id\
                inner join users\
                on comments.users_id = users.id\
                where articles.id =15\
                and articles.is_deleted = false\
                and comments.is_deleted = false;"
        self.cur.execute(sql)
        response = self.cur.fetchall()
        return response

    def create(self, data: dict) -> dict:
        sql = f"insert into comments(aricles_id, users_id, comment_text)\
                values('{data['article_id']}', '{data['user_id']}', '{data['comment']}');"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def update(self, data: dict) -> dict:
        sql = f"update comments set comment_text = '{data['comment']}'\
                where articles_id = '{data['article_id']}'\
                and users_id = '{data['author_id']}' \
                and is_deleted = false;"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete(self) -> str:
        sql = "UPDATE comments SET is_deleted = true;"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_id(self, article_id: str, author_id: str) -> str:
        sql = f"update comments set is_deleted = true where articles_id = {article_id}\
                and users_id = {author_id};"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_name(self, title: str, name: str) -> str:
        sql = f"update comments set is_deleted = true where articles_id in\
                (select id from articles where name = '{title}')\
                and users_id in\
                (select id from users where name ='{name}');"
        self.cur.execute(sql)
#        self.conn.commit()
        response = '"Ok 200", 200'
        return response


def main():
    pass


if __name__ == '__main__':
    main()






