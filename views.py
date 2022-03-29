from flask import request
from flask.views import MethodView
from marshmallow import ValidationError
from flask import make_response

from controller import ArticleController, LikeController, CommentController, UserController , AuthController
from validation import SchemaAddArticle, SchemaUpdateArticle, SchemaAddLike, SchemaAddComment, SchemaAddUser
from tokens import token_extraction


class UserView(MethodView):
    def __init__(self):
        self.controller = UserController()
        self.auth = AuthController()

    def get(self, user_id: str, name: str) -> dict or str:
        token = token_extraction()
        print(token)
        authorized = self.auth.authorization(token)
        if authorized:
            if user_id is None and name is None:
                result = self.__get()
                result = make_response(result)
                return result
            elif name is None:
                result = self.__get_by_id(user_id)
                result = make_response(result)
                return result
            else:
                result = self.__get_by_name(name)
                result = make_response(result, 200)
                return result
        else:
            res = ("Ошибка авторизации", 401)
            result = make_response(res)
            return result

    def __get(self) -> dict:
        result = self.controller.get()
        return result

    def __get_by_id(self, user_id) -> dict or str:
        if user_id.isdigit():
            result = self.controller.get_by_id(user_id)
            result = (result, 200)
            return result
        else:
            result = ("Неправильный article_id", 400)
            return result

    def __get_by_name(self, name):
        result = self.controller.get_by_name(name)
        result = (result, 200)
        return result

    def post(self) -> dict or str:
        data = request.get_json()
        try:
            SchemaAddUser().load(data)
        except ValidationError as err:
            result = (err, 400)                            #   response
        else:
            result = self.controller.post(data)
            if result == "Ошибка сервера":
                result = (result, 500)
            else:
                result = (result, 200)
        result = make_response(result)
        return result

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            data = request.get_json()
            try:
                SchemaUpdateArticle().load(data)
            except ValidationError as err:
                result = (err, 400)
            else:
                result = self.controller.put(data)
                if result == "Ошибка сервера":
                    result = (result, 500)
                else:
                    result = (result, 200)
            result = make_response(result)
            return result
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result


def delete(self, user_id: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if user_id is None and name is None:
                result = self.__delete()
                return result
            elif name is None:
                result = self.__delete_by_id(user_id)
                return result
            else:
                result = self.__delete_by_name(name)
                return result
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result

    def __delete(self):
        result = self.controller.delete()
        return result

    def __delete_by_name(self, name) -> dict:
        result = self.controller.delete_by_name(name)
        return result

    def __delete_by_id(self, user_id) -> dict or str:
        if user_id.isdigit():
            result = self.controller.delete_by_id(user_id)
            return result
        else:
            return "Error 400 , article_id is not digit"


class ArticleView(MethodView):
    def __init__(self):
        self.controller = ArticleController()
        self.auth = AuthController()

    def get(self, article_id: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                result = self.__get()
                return result
            elif name is None:
                result = self.__get_by_id(article_id)
                return result
            else:
                result = self.__get_by_name(name)
                return result
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result

    def __get(self) -> dict:
        result = self.controller.get()
        return result

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            result = self.controller.get_by_id(article_id)
            return result
        else:
            return "Error 400 , article_id is not digit"

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
                return err
            else:
                result = self.controller.post(data)
                return result
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            data = request.get_json()
            try:
                SchemaUpdateArticle().load(data)
            except ValidationError as err:
                return err
            else:
                result = self.controller.put(data)
                return result
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result

    def delete(self, article_id: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                result = self.__delete()
                return result
            elif name is None:
                result = self.__delete_by_id(article_id)
                return result
            else:
                result = self.__delete_by_name(name)
                return result
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result

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
            return "Error 400 , article_id is not digit"


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
                return result
            elif name is None:
                result = self.__get_by_id(article_id)
                return result
            else:
                result = self.__get_by_name(name)
                return result
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result

    def __get(self) -> dict:
        result = self.controller.get()
        return result

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            result = self.controller.get_by_id(article_id)
            return result
        else:
            return "Error 400 , article_id is not digit"

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
                return err
            else:
                result = self.controller.post(data)
                return result
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result

    def delete(self, article_id: str, author_id: str, title: str,  name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and title is None:
                result = self.__delete()
                return result
            elif name is None and title is None:
                result = self.__delete_by_id(article_id, author_id)
                return result
            else:
                result = self.__delete_by_name(title, name)
                return result
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
            return "Error 400 , article_id is not digit"

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
                return result
            elif name is None:
                result = self.__get_by_id(article_id)
                return result
            else:
                result = self.__get_by_name(name)
                return result
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result

    def __get(self) -> dict:
        result = self.controller.get()
        return result

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            result = self.controller.get_by_id(article_id)
            return result
        else:
            return "Error 400 , article_id is not digit"

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
                return err
            else:
                result = self.controller.post(data)
                return result
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            data = request.get_json()
            try:
                SchemaAddComment().load(data)
            except ValidationError as err:
                return err
            else:
                result = self.controller.put(data)
                return result
        else:
            result = ("Ошибка авторизации", 401)
            result = make_response(result)
            return result

    def delete(self, article_id: str, author_id: str, title: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and title is None:
                result = self.__delete()
                return result
            elif name is None and title is None:
                result = self.__delete_by_id(article_id, author_id)
                return result
            else:
                result = self.__delete_by_name(title, name)
                return result
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
            return "Error 400 , article_id is not digit"

    def __delete_by_name(self, title, name) -> dict:
        result = self.controller.delete_by_name(title, name)
        return result
