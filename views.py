from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from controller import ArticleController, LikeController, CommentController
from validation import SchemaAddArticle, SchemaUpdateArticle, SchemaAddLike, SchemaAddComment


class UserView(MethodView):
    pass


class ArticleView(MethodView):
    def __init__(self):
        self.controller = ArticleController()

    def get(self, article_id: str, name: str) -> dict:
        if article_id is None and name is None:
            result = self.__get()
            return result
        elif name is None:
            result = self.__get_by_id(article_id)
            return result
        else:
            result = self.__get_by_name(name)
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
        data = request.get_json()
        try:
            SchemaAddArticle().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.post(data)
            return result

    def put(self) -> dict or str:
        data = request.get_json()
        try:
            SchemaUpdateArticle().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.put(data)
            return result

    def delete(self, article_id: str, name: str) -> dict:
        if article_id is None and name is None:
            result = self.__delete()
            return result
        elif name is None:
            result = self.__delete_by_id(article_id)
            return result
        else:
            result = self.__delete_by_name(name)
            return result

    def __delete(self):
        result = self.controller.delete()
        return result

    def __delete_by_name(self, name) -> dict:
        result = self.controller.delete_by_name(name)
        return result

    def __delete_by_id(self, article_id)-> dict or str:
        if article_id.isdigit():
            print(type(article_id))
            result = self.controller.delete_by_id(article_id)
            return result
        else:
            return "Error 400 , article_id is not digit"


class LikeView(MethodView):
    def __init__(self):
        self.controller = LikeController()

    def get(self, article_id: str, name: str) -> dict:
        if article_id is None and name is None:
            result = self.__get()
            return result
        elif name is None:
            result = self.__get_by_id(article_id)
            return result
        else:
            result = self.__get_by_name(name)
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
        data = request.get_json()
        try:
            SchemaAddLike().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.post(data)
            return result

    def delete(self, article_id: str, author_id: str, title: str,  name: str) -> dict:
        if article_id is None and title is None:
            result = self.__delete()
            return result
        elif name is None and title is None:
            result = self.__delete_by_id(article_id, author_id)
            return result
        else:
            result = self.__delete_by_name(title, name)
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

    def get(self, article_id: str, name: str) -> dict:
        if article_id is None and name is None:
            result = self.__get()
            return result
        elif name is None:
            result = self.__get_by_id(article_id)
            return result
        else:
            result = self.__get_by_name(name)
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
        data = request.get_json()
        try:
            SchemaAddComment().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.post(data)
            return result

    def put(self) -> dict or str:
        data = request.get_json()
        try:
            SchemaAddComment().load(data)
        except ValidationError as err:
            return err
        else:
            result = self.controller.put(data)
            return result

    def delete(self, article_id: str, author_id: str, title: str, name: str) -> dict:
        if article_id is None and title is None:
            result = self.__delete()
            return result
        elif name is None and title is None:
            result = self.__delete_by_id(article_id, author_id)
            return result
        else:
            result = self.__delete_by_name(title, name)
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

