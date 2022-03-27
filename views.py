from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from controller import ArticleController, LikeController, CommentController, UserController
from validation import SchemaAddArticle, SchemaUpdateArticle, SchemaAddLike, SchemaAddComment, SchemaAddUser


class UserView(MethodView):
    def __init__(self):
        self.controller = UserController()

    def get(self, user_id: str, name: str) -> dict:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        print(token)
        if user_id is None and name is None:
            result = self.__get(token)
            return result
        elif name is None:
            result = self.__get_by_id(user_id, token)
            return result
        else:
            result = self.__get_by_name(name, token)
            return result

    def __get(self, token) -> dict:
        result = self.controller.get(token)
        return result

    def __get_by_id(self, user_id, token) -> dict or str:
        if user_id.isdigit():
            result = self.controller.get_by_id(user_id, token)
            return result
        else:
            return "Error 400 , article_id is not digit"

    def __get_by_name(self, name, token):
        result = self.controller.get_by_name(name, token)
        return result

    def post(self) -> dict or str:
        data = request.get_json()
        try:
            SchemaAddUser().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.post(data)
            return result

    def put(self) -> dict or str:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        data = request.get_json()
        try:
            SchemaUpdateArticle().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.put(data, token)
            return result

    def delete(self, user_id: str, name: str) -> dict:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        if user_id is None and name is None:
            result = self.__delete(token)
            return result
        elif name is None:
            result = self.__delete_by_id(user_id, token)
            return result
        else:
            result = self.__delete_by_name(name, token)
            return result

    def __delete(self, token):
        result = self.controller.delete(token)
        return result

    def __delete_by_name(self, name, token) -> dict:
        result = self.controller.delete_by_name(name, token)
        return result

    def __delete_by_id(self, user_id, token) -> dict or str:
        if user_id.isdigit():
            result = self.controller.delete_by_id(user_id, token)
            return result
        else:
            return "Error 400 , article_id is not digit"


class ArticleView(MethodView):
    def __init__(self):
        self.controller = ArticleController()

    def get(self, article_id: str, name: str) -> dict:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        if article_id is None and name is None:
            result = self.__get(token)
            return result
        elif name is None:
            result = self.__get_by_id(article_id, token)
            return result
        else:
            result = self.__get_by_name(name, token)
            return result

    def __get(self, token) -> dict:
        result = self.controller.get(token)
        return result

    def __get_by_id(self, article_id, token) -> dict or str:
        if article_id.isdigit():
            result = self.controller.get_by_id(article_id, token)
            return result
        else:
            return "Error 400 , article_id is not digit"

    def __get_by_name(self, name, token):
        result = self.controller.get_by_name(name, token)
        return result

    def post(self) -> dict or str:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        data = request.get_json()
        try:
            SchemaAddArticle().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.post(data, token)
            return result

    def put(self) -> dict or str:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        data = request.get_json()
        try:
            SchemaUpdateArticle().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.put(data, token)
            return result

    def delete(self, article_id: str, name: str) -> dict:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        if article_id is None and name is None:
            result = self.__delete(token)
            return result
        elif name is None:
            result = self.__delete_by_id(article_id, token)
            return result
        else:
            result = self.__delete_by_name(name, token)
            return result

    def __delete(self, token):
        result = self.controller.delete(token)
        return result

    def __delete_by_name(self, name, token) -> dict:
        result = self.controller.delete_by_name(name, token)
        return result

    def __delete_by_id(self, article_id, token) -> dict or str:
        if article_id.isdigit():
            result = self.controller.delete_by_id(article_id, token)
            return result
        else:
            return "Error 400 , article_id is not digit"


class LikeView(MethodView):
    def __init__(self):
        self.controller = LikeController()

    def get(self, article_id: str, name: str) -> dict:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        if article_id is None and name is None:
            result = self.__get(token)
            return result
        elif name is None:
            result = self.__get_by_id(article_id, token)
            return result
        else:
            result = self.__get_by_name(name, token)
            return result

    def __get(self, token) -> dict:
        result = self.controller.get(token)
        return result

    def __get_by_id(self, article_id, token) -> dict or str:
        if article_id.isdigit():
            result = self.controller.get_by_id(article_id, token)
            return result
        else:
            return "Error 400 , article_id is not digit"

    def __get_by_name(self, name, token) -> dict or str:
            result = self.controller.get_by_name(name, token)
            return result

    def post(self) -> dict or str:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        data = request.get_json()
        try:
            SchemaAddLike().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.post(data, token)
            return result

    def delete(self, article_id: str, author_id: str, title: str,  name: str) -> dict:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        if article_id is None and title is None:
            result = self.__delete(token)
            return result
        elif name is None and title is None:
            result = self.__delete_by_id(article_id, author_id, token)
            return result
        else:
            result = self.__delete_by_name(title, name, token)
            return result

    def __delete(self, token) -> dict:
        result = self.controller.delete(token)
        return result

    def __delete_by_id(self, article_id, author_id, token) -> dict or str:
        if article_id.isdigit() and author_id.isdigit():
            result = self.controller.delete_by_id(article_id, author_id, token)
            return result
        else:
            return "Error 400 , article_id is not digit"

    def __delete_by_name(self, title, name, token) -> dict:
        result = self.controller.delete_by_name(title, name, token)
        return result


class CommentView(MethodView):
    def __init__(self):
        self.controller = CommentController()

    def get(self, article_id: str, name: str) -> dict:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        if article_id is None and name is None:
            result = self.__get(token)
            return result
        elif name is None:
            result = self.__get_by_id(article_id, token)
            return result
        else:
            result = self.__get_by_name(name, token)
            return result

    def __get(self, token) -> dict:
        result = self.controller.get(token)
        return result

    def __get_by_id(self, article_id, token) -> dict or str:
        if article_id.isdigit():
            result = self.controller.get_by_id(article_id, token)
            return result
        else:
            return "Error 400 , article_id is not digit"

    def __get_by_name(self, name, token) -> dict or str:
            result = self.controller.get_by_name(name, token)
            return result

    def post(self) -> dict or str:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        data = request.get_json()
        try:
            SchemaAddComment().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.post(data, token)
            return result

    def put(self) -> dict or str:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        data = request.get_json()
        try:
            SchemaAddComment().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.put(data, token)
            return result

    def delete(self, article_id: str, author_id: str, title: str, name: str) -> dict:
        auth = request.headers.get('Authorization')
        list_auth = auth.split()
        token = list_auth[1]
        if article_id is None and title is None:
            result = self.__delete(token)
            return result
        elif name is None and title is None:
            result = self.__delete_by_id(article_id, author_id, token)
            return result
        else:
            result = self.__delete_by_name(title, name, token)
            return result

    def __delete(self, token) -> dict:
        result = self.controller.delete(token)
        return result

    def __delete_by_id(self, article_id, author_id, token) -> dict or str:
        if article_id.isdigit() and author_id.isdigit():
            result = self.controller.delete_by_id(article_id, author_id, token)
            return result
        else:
            return "Error 400 , article_id is not digit"

    def __delete_by_name(self, title, name, token) -> dict:
        result = self.controller.delete_by_name(title, name, token)
        return result

