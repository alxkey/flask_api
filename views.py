from flask import make_response
from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from controller import ArticleController, LikeController, CommentController, UserController, AuthController
from logger import logger
from tokens import token_extraction
from validation import SchemaAddArticle, SchemaUpdateArticle, SchemaAddLike, SchemaAddComment, SchemaAddUser, \
    SchemaUpdateUser


class UserView(MethodView):
    def __init__(self):
        self.controller = UserController()
        self.auth = AuthController()

    def get(self, user_id: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if user_id is None and name is None:
                result = self.__get()
                response = make_response(result)
                return response
            elif name is None:
                result = self.__get_by_id(user_id)
                response = make_response(result)
                return response
            else:
                result = self.__get_by_name(name)
                response = make_response(result)
                return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def __get(self) -> dict:
        result = self.controller.get()
        return result

    def __get_by_id(self, user_id) -> dict or str:
        if user_id.isdigit():
            result = self.controller.get_by_id(user_id)
            response = make_response(result)
            return response
        else:
            response = make_response("Неправильный article_id", 400)
            return response

    def __get_by_name(self, name):
        result = self.controller.get_by_name(name)
        response = make_response(result)
        return response

    def post(self) -> dict or str:
        data = request.get_json()
        try:
            SchemaAddUser().load(data)
        except ValidationError as err:
            result = (err, 400)
            response = make_response(result)
        else:
            result = self.controller.post(data)
            response = make_response(result)
        return response

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            data = request.get_json()
            try:
                SchemaUpdateUser().load(data)
            except ValidationError as err:
                result = (err, 400)
                response = make_response(result)
            else:
                result = self.controller.put(data)
                response = make_response(result)
            return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def delete(self, user_id: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if user_id is None and name is None:
                result = self.__delete()
                response = make_response(result)
                return response
            elif name is None:
                result = self.__delete_by_id(user_id)
                response = make_response(result)
                return response
            else:
                result = self.__delete_by_name(name)
                response = make_response(result)
                return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def __delete(self):
        result = self.controller.delete()
        response = make_response(result)
        return response

    def __delete_by_name(self, name):
        result = self.controller.delete_by_name(name)
        response = make_response(result)
        return response

    def __delete_by_id(self, user_id) -> dict or str:
        if user_id.isdigit():
            result = self.controller.delete_by_id(user_id)
            response = make_response(result)
            return response
        else:
            response = make_response("Неправильный article_id", 400)
            return response


class ArticleView(MethodView):
    def __init__(self):
        self.controller = ArticleController()
        self.auth = AuthController()

    def get(self, article_id: str, name: str):
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                result = self.__get()
                response = make_response(result)
                return response
            elif name is None:
                result = self.__get_by_id(article_id)
                response = make_response(result)
                return response
            else:
                result = self.__get_by_name(name)
                response = make_response(result)
                return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def __get(self) -> dict:
        result = self.controller.get()
        return result

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            result = self.controller.get_by_id(article_id)
            return result
        else:
            result = ("Неправильный article_id", 400)
            return result

    def __get_by_name(self, name):
        result = self.controller.get_by_name(name)
        return result

    def post(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            data = request.get_json()
            try:
                SchemaAddArticle().load(data)
            except ValidationError as err:
                result = (err, 400)
                response = make_response(result)
            else:
                result = self.controller.post(data)
                response = make_response(result)
            return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            data = request.get_json()
            try:
                SchemaUpdateArticle().load(data)
            except ValidationError as err:
                result = (err, 400)
                response = make_response(result)
            else:
                result = self.controller.put(data)
                response = make_response(result)
            return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def delete(self, article_id: str, name: str):
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                result = self.__delete()
                response = make_response(result)
            elif name is None:
                result = self.__delete_by_id(article_id)
                response = make_response(result)
            else:
                result = self.__delete_by_name(name)
                response = make_response(result)
            return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def __delete(self):
        result = self.controller.delete()
        return result

    def __delete_by_name(self, name) -> dict:
        result = self.controller.delete_by_name(name)
        return result

    def __delete_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            result = self.controller.delete_by_id(article_id)
            return result
        else:
            result = ("Неправильный article_id", 400)
            return result


class LikeView(MethodView):
    def __init__(self):
        self.controller = LikeController()
        self.auth = AuthController()

    def get(self, article_id: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                result = self.__get()
                response = make_response(result)
            elif name is None:
                result = self.__get_by_id(article_id)
                response = make_response(result)
            else:
                result = self.__get_by_name(name)
                response = make_response(result)
            return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def __get(self) -> dict:
        result = self.controller.get()
        return result

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            result = self.controller.get_by_id(article_id)
            return result
        else:
            result = ("Неправильный article_id", 400)
            return result

    def __get_by_name(self, name) -> dict or str:
        result = self.controller.get_by_name(name)
        return result

    def post(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            data = request.get_json()
            try:
                SchemaAddLike().load(data)
            except ValidationError as err:
                result =(err, 400)
                response = make_response(result)
            else:
                result = self.controller.post(data)
                response = make_response(result)
            return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def delete(self, article_id: str, author_id: str, title: str,  name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and title is None:
                result = self.__delete()
                response = make_response(result)
            elif name is None and title is None:
                result = self.__delete_by_id(article_id, author_id)
                response = make_response(result)
            else:
                result = self.__delete_by_name(title, name)
                response = make_response(result)
            return response
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result

    def __delete(self) -> dict:
        result = self.controller.delete()
        return result

    def __delete_by_id(self, article_id, author_id) -> dict or str:
        if article_id.isdigit() and author_id.isdigit():
            result = self.controller.delete_by_id(article_id, author_id)
            return result
        else:
            result = ("Неправильный article_id", 400)
            return result

    def __delete_by_name(self, title, name) -> dict:
        result = self.controller.delete_by_name(title, name)
        return result


class CommentView(MethodView):
    def __init__(self):
        self.controller = CommentController()
        self.auth = AuthController()

    def get(self, article_id: str, name: str) -> dict and str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                result = self.__get()
                response = make_response(result)
            elif name is None:
                result = self.__get_by_id(article_id)
                response = make_response(result)
            else:
                result = self.__get_by_name(name)
                response = make_response(result)
            return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def __get(self) -> dict:
        result = self.controller.get()
        return result

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            result = self.controller.get_by_id(article_id)
            return result
        else:
            result = ("Неправильный article_id", 400)
            return result

    def __get_by_name(self, name) -> dict or str:

        result = self.controller.get_by_name(name)
        return result

    def post(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            data = request.get_json()
            try:
                SchemaAddComment().load(data)
            except ValidationError as err:
                result = (err, 400)
                response = make_response(result)
            else:
                result = self.controller.post(data)
                response = make_response(result)
            return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            data = request.get_json()
            try:
                SchemaAddComment().load(data)
            except ValidationError as err:
                result = (err, 400)
                response = make_response(result)
            else:
                result = self.controller.put(data)
                response = make_response(result)
            return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def delete(self, article_id: str, author_id: str, title: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and title is None:
                result = self.__delete()
                response = make_response(result)
            elif name is None and title is None:
                result = self.__delete_by_id(article_id, author_id)
                response = make_response(result)
            else:
                result = self.__delete_by_name(title, name)
                response = make_response(result)
            return response
        else:
            result = ("Ошибка авторизации", 401)
            response = make_response(result)
            return response

    def __delete(self) -> dict:
        result = self.controller.delete()
        return result

    def __delete_by_id(self, article_id, author_id) -> dict or str:
        if article_id.isdigit() and author_id.isdigit():
            result = self.controller.delete_by_id(article_id, author_id)
            return result
        else:
            result = ("Неправильный article_id", 400)
            return result

    def __delete_by_name(self, title, name) -> dict:
        result = self.controller.delete_by_name(title, name)
        return result
