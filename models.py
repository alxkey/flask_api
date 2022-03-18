import psycopg2
from flask import make_response
from abc import ABC, abstractmethod

from config import DB_NAME, USER, PASSWORD, HOST, PORT


class AbstractModels(ABC):
    def __init__(self):
        self.param = {'database': DB_NAME,
                     'user': USER,
                     'password': PASSWORD,
                     'host': HOST,
                     'port': PORT }
        self.conn = psycopg2.connect(**self.param)
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
    def post(self, data: dict):
        '''
        resource creation
        :param data: resource parameter dic
        :return: resource id or response code
        '''
        pass

    @abstractmethod
    def put(self, data: dict):
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


class ArticleModels(AbstractModels):
    def get(self) -> list:
        keys = ('title', 'date', 'author_id')
        sql = 'SELECT name, pub_date, users_id\
               FROM articles\
               where is_deleted = false;'
        self.cur.execute(sql)
        values = self.cur.fetchall()
        print(values)
        response = []
        for value in values:
            result = dict(zip(keys, value))
            response.append(result)
        return response

    def get_by_id(self, id: str) -> dict:
        keys = ('title', 'text', 'date', 'author_id')
        sql = f'SELECT name, article_text, pub_date, users_id\
                FROM articles\
                WHERE id = {id}\
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

    def post(self, new_article: dict) -> dict:
        sql = f"INSERT INTO articles(name, article_text, pub_date, users_id)\
                VALUES('{new_article['name']}', '{new_article['text']}', '{new_article['date']}',\
                '{new_article['author_id']}')\
                RETURNING id;"
        self.cur.execute(sql)
        self.conn.commit()
        values = self.cur.fetchone()
        response = {'article_id': values[0]}
        return response

    def put(self, data: dict) -> str:
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
        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete(self) -> str:
        sql = "UPDATE articles SET is_deleted = true;"
        self.cur.execute(sql)
        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_id(self, article_id: str) -> str:
        sql = f"UPDATE articles\
                SET is_deleted = true\
                WHERE id = {article_id};"
        self.cur.execute(sql)
        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_name(self, name: str) -> str:
        sql = f"UPDATE articles\
              SET is_deleted = true\
              WHERE name = {name};"
        self.cur.execute(sql)
        self.conn.commit()
        response = make_response("Ok 200", 200)
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

    def get_by_id(self, id: str) -> dict:
        sql = f'select articles.name, users.name\
                from articles\
                inner join article_like\
                on article_like.articles_id = articles.id\
                inner join users\
                on article_like.users_id = users.id\
                where articles.id = {id}\
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

    def post(self, data: dict) -> dict:
        sql = f"insert into article_like(articles_id, users_id)\
                values('{data['article_id']}','{data['author_id']}');"
        self.cur.execute(sql)
        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete(self) -> str:
        sql = "UPDATE article_like SET is_deleted = true;"
        self.cur.execute(sql)
        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_id(self, article_id: str, author_id: str) -> str:
        sql = f"update article_like set is_deleted = true where articles_id = {article_id}\
                and users_id = {author_id};"
        self.cur.execute(sql)
        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_name(self, title: str, name: str) -> str:
        sql = f"update article_like set is_deleted = true where articles_id in\
                (select id from articles where name = '{title}')\
                and users_id in\
                (select id from users where name ='{name}');"
        self.cur.execute(sql)
        self.conn.commit()
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

    def get_by_id(self, id: str) -> dict:
        sql = f'select articles.name, users.name, comments.comment_text\
                from articles\
                inner join comments\
                on comments.articles_id = articles.id\
                inner join users\
                on comments.users_id = users.id\
                where articles.id = {id}\
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

    def post(self, data: dict) -> dict:
        sql = f"insert into comments(aricles_id, users_id, comment_text)\
                values('{data['article_id']}', '{data['user_id']}', '{data['comment']}');"
        self.cur.execute(sql)
        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def put(self, data: dict) -> dict:
        sql = f"update comments set comment_text = '{data['comment']}'\
                where articles_id = '{data['article_id']}'\
                and users_id = '{data['author_id']}' \
                and is_deleted = false;"
        self.cur.execute(sql)
        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete(self) -> str:
        sql = "UPDATE comments SET is_deleted = true;"
        self.cur.execute(sql)
        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_id(self, article_id: str, author_id: str) -> str:
        sql = f"update comments set is_deleted = true where articles_id = {article_id}\
                and users_id = {author_id};"
        self.cur.execute(sql)
        self.conn.commit()
        response = '"Ok 200", 200 '
        return response

    def delete_by_name(self, title: str, name: str) -> str:
        sql = f"update comments set is_deleted = true where articles_id in\
                (select id from articles where name = '{title}')\
                and users_id in\
                (select id from users where name ='{name}');"
        self.cur.execute(sql)
        self.conn.commit()
        response = '"Ok 200", 200'
        return response


def main():
    db = ArticleModels()
    lst = db.get_all_articles()
    print(lst)
    string = db.post_like(2, 12)
    print(string)

if __name__ == '__main__':
    main()






