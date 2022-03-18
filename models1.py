import psycopg2
from flask import make_response
from werkzeug.exceptions import InternalServerError

import config


class ArticleModels:
    param = {'database': config.database,
             'user': config.user,
             'password': config.password,
             'host': config.host,
             'port': config.port
             }

    @classmethod
    def get_all_articles(cls) -> list:
        keys = ('title', 'date', 'author_id')
        try:
            with psycopg2.connect(**cls.param) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT name, pub_date, users_id FROM articles ;')
                    values = cur.fetchall()
            response = []
            for v in values:
                result = dict(zip(keys, v))
                response.append(result)
            return response
        except psycopg2.OperationalError:
            print("Ошибка подключения к базе  500")
            raise InternalServerError("Ошибка подключения к базе- 500")

    @classmethod
    def get_article(cls, id: str) -> dict:
        keys = ('title', 'text', 'date', 'author_id')
        try:
            with psycopg2.connect(**cls.param) as conn:
                with conn.cursor() as cur:
                    cur.execute(f'SELECT name, article_text, pub_date, users_id FROM articles WHERE id = {id};')
                    values = cur.fetchall()
            response = dict(zip(keys, values))
            return response
        except psycopg2.OperationalError:
            print("Ошибка подключения к базе  500")
            raise InternalServerError("Ошибка подключения к базе- 500")

    @classmethod
    def post_article(cls, new_article: dict) -> dict:
        try:
            with psycopg2.connect(**cls.param) as conn:
                with conn.cursor() as cur:
                    sql = "INSERT INTO articles(name, article_text, pub_date, users_id)" \
                          f"VALUES('{new_article['name']}', '{new_article['text']}', '{new_article['date']}', " \
                          f"'{new_article['author_id']}') RETURNING id;"
                    cur.execute(sql)
                    values = cur.fetchone()
            response = {'article_id': values[0]}
            return response
        except psycopg2.OperationalError:
            print("Ошибка подключения к базе  500")
            raise InternalServerError("Ошибка подключения к базе- 500")

    @classmethod
    def post_like(cls, article_id: str, user_id: str) -> str:
        try:
            with psycopg2.connect(**cls.param) as conn:
                with conn.cursor() as cur:
                    sql = "INSERT INTO article_like(articles_id, users_id)" \
                          f"VALUES('{article_id}', '{user_id}');"
                    cur.execute(sql)
            response = make_response("Ok 200", 200)
            return response
        except psycopg2.OperationalError:
            print("Ошибка подключения к базе  500")
            raise InternalServerError("Ошибка подключения к базе- 500")

    @classmethod
    def post_comment(cls, new_comment: dict) -> str:
        try:
            with psycopg2.connect(**cls.param) as conn:
                with conn.cursor() as cur:
                    sql = "INSERT INTO comments(articles_id, users_id, comment_text)" \
                          f"VALUES('{new_comment['article_id']}', '{new_comment['user_id']}', '{new_comment['comment']}');"
                    cur.execute(sql)
            response = make_response("Ok 200", 200)  ### фласковский респонс!
            return response
        except psycopg2.OperationalError:
            print("Ошибка подключения к базе  500")
            raise InternalServerError("Ошибка подключения к базе- 500")

    @classmethod
    def delete_article(cls, article_id: str)-> str:
        try:
            with psycopg2.connect(**cls.param) as conn:
                with conn.cursor() as cur:
                    sql = f"UPDATE articles SET is_deleted = true WHERE id = {article_id}"
                    cur.execute(sql)
            response = make_response("Ok 200", 200)  ### фласковский респонс!
            return response
        except psycopg2.OperationalError:
            print("Ошибка подключения к базе  500")
            raise InternalServerError("Ошибка подключения к базе- 500")

    @classmethod
    def delete_article_name(cls, name: str) -> str:
        try:
            with psycopg2.connect(**cls.param) as conn:
                with conn.cursor() as cur:
                    sql = f"UPDATE articles SET is_deleted = true WHERE name = {name}"
                    cur.execute(sql)
            response = make_response("Ok 200", 200)  ### фласковский респонс!
            return response
        except psycopg2.OperationalError:
            print("Ошибка подключения к базе  500")
            raise InternalServerError("Ошибка подключения к базе- 500")




