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
                getting_all_users = self.__get()
                response = make_response(getting_all_users)
                return response
            elif name is None:
                getting_user_by_id = self.__get_by_id(user_id)
                response = make_response(getting_user_by_id)
                return response
            else:
                getting_user_by_name = self.__get_by_name(name)
                response = make_response(getting_user_by_name)
                return response
        else:
            err_authorization = "Ошибка авторизации", 401
            response = make_response(err_authorization)
            return response

    def __get(self) -> dict:
        getting_all_users = self.controller.get()
        return getting_all_users

    def __get_by_id(self, user_id) -> dict or str:
        if user_id.isdigit():
            getting_user_by_id = self.controller.get_by_id(user_id)
            return getting_user_by_id
        else:
            err_request = "Неправильный article_id", 400
            return err_request

    def __get_by_name(self, name):
        getting_user_by_name = self.controller.get_by_name(name)
        return getting_user_by_name

    def post(self) -> dict or str:
        body_of_request = request.get_json()
        try:
            SchemaAddUser().load(body_of_request)
        except ValidationError as err:
            error = err, 400
            response = make_response(error)
        else:
            user_crad = self.controller.post(body_of_request)
            response = make_response(user_crad)
        return response

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaUpdateUser().load(body_of_request)
            except ValidationError as err:
                error = err, 400
                response = make_response(error)
            else:
                result_of_update = self.controller.put(body_of_request)
                response = make_response(result_of_update)
            return response
        else:
            error = "Ошибка авторизации", 401
            response = make_response(error)
            return response

    def delete(self, user_id: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if user_id is None and name is None:
                result_of_delete = self.__delete()
                response = make_response(result_of_delete)
                return response
            elif name is None:
                result_of_delete = self.__delete_by_id(user_id)
                response = make_response(result_of_delete)
                return response
            else:
                result_of_delete = self.__delete_by_name(name)
                response = make_response(result_of_delete)
                return response
        else:
            err_authorization = "Ошибка авторизации", 401
            response = make_response(err_authorization)
            return response

    def __delete(self):
        result_of_delete = self.controller.delete()
        return result_of_delete

    def __delete_by_name(self, name):
        result_of_delete = self.controller.delete_by_name(name)
        return result_of_delete

    def __delete_by_id(self, user_id) -> dict or str:
        if user_id.isdigit():
            result_of_delete = self.controller.delete_by_id(user_id)
            return result_of_delete
        else:
            err_request = "Неправильный article_id", 400
            return err_request


class ArticleView(MethodView):
    def __init__(self):
        self.controller = ArticleController()
        self.auth = AuthController()

    def get(self, article_id: str, name: str):
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                getting_all_articles = self.__get()
                response = make_response(getting_all_articles)
                return response
            elif name is None:
                getting_article_by_id = self.__get_by_id(article_id)
                response = make_response(getting_article_by_id)
                return response
            else:
                getting_article_by_name = self.__get_by_name(name)
                response = make_response(getting_article_by_name)
                return response
        else:
            err_authorization = "Ошибка авторизации", 401
            response = make_response(err_authorization)
            return response

    def __get(self) -> dict:
        getting_all_articles = self.controller.get()
        return getting_all_articles

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            getting_article_by_id = self.controller.get_by_id(article_id)
            return getting_article_by_id
        else:
            err_request = "Неправильный article_id", 400
            return err_request

    def __get_by_name(self, name):
        getting_article_by_name = self.controller.get_by_name(name)
        return getting_article_by_name

    def post(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaAddArticle().load(body_of_request)
            except ValidationError as err:
                error = err, 400
                response = make_response(error)
            else:
                article_id_and_code_resp = self.controller.post(body_of_request)
                response = make_response(article_id_and_code_resp)
            return response
        else:
            err_authorization = "Ошибка авторизации", 401
            response = make_response(err_authorization)
            return response

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaUpdateArticle().load(body_of_request)
            except ValidationError as err:
                error = err, 400
                response = make_response(error)
            else:
                 result_of_update = self.controller.put(body_of_request)
                 response = make_response(result_of_update)
            return response
        else:
            err = "Ошибка авторизации", 401
            response = make_response(err)
            return response

    def delete(self, article_id: str, name: str):
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                result_of_delete = self.__delete()
                response = make_response(result_of_delete)
            elif name is None:
                result_of_delete = self.__delete_by_id(article_id)
                response = make_response(result_of_delete)
            else:
                result_of_delete = self.__delete_by_name(name)
                response = make_response(result_of_delete)
            return response
        else:
            err_authorization = "Ошибка авторизации", 401
            response = make_response(err_authorization)
            return response

    def __delete(self):
        result_of_delete = self.controller.delete()
        return result_of_delete

    def __delete_by_name(self, name) -> dict:
        result_of_delete = self.controller.delete_by_name(name)
        return result_of_delete

    def __delete_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            result_of_delete = self.controller.delete_by_id(article_id)
            return result_of_delete
        else:
            err_request = "Неправильный article_id", 400
            return err_request


class LikeView(MethodView):
    def __init__(self):
        self.controller = LikeController()
        self.auth = AuthController()

    def get(self, article_id: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                getting_all_likes = self.__get()
                response = make_response(getting_all_likes)
            elif name is None:
                getting_like_by_id = self.__get_by_id(article_id)
                response = make_response(getting_like_by_id)
            else:
                getting_like_by_name = self.__get_by_name(name)
                response = make_response(getting_like_by_name)
            return response
        else:
            err_authorization = "Ошибка авторизации", 401
            response = make_response(err_authorization)
            return response

    def __get(self) -> dict:
        getting_all_likes = self.controller.get()
        return getting_all_likes

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            getting_like_by_id = self.controller.get_by_id(article_id)
            return getting_like_by_id
        else:
            err_request = "Неправильный article_id", 400
            return err_request

    def __get_by_name(self, name) -> dict or str:
        getting_like_by_name = self.controller.get_by_name(name)
        return getting_like_by_name

    def post(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaAddLike().load(body_of_request)
            except ValidationError as err:
                error =err, 400
                response = make_response(error)
            else:
                result_of_create = self.controller.post(body_of_request)
                response = make_response(result_of_create)
            return response
        else:
            error = "Ошибка авторизации", 401
            response = make_response(error)
            return response

    def delete(self, article_id: str, author_id: str, title: str,  name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and title is None:
                result_of_delete = self.__delete()
                response = make_response(result_of_delete)
            elif name is None and title is None:
                result_of_delete = self.__delete_by_id(article_id, author_id)
                response = make_response(result_of_delete)
            else:
                result_of_delete = self.__delete_by_name(title, name)
                response = make_response(result_of_delete)
            return response
        else:
            err_authorization = "Ошибка авторизации", 401
            result = make_response(err_authorization)
            return result

    def __delete(self) -> dict:
        result_of_delete = self.controller.delete()
        return result_of_delete

    def __delete_by_id(self, article_id, author_id) -> dict or str:
        if article_id.isdigit() and author_id.isdigit():
            result_of_delete = self.controller.delete_by_id(article_id, author_id)
            return result_of_delete
        else:
            err_request = "Неправильный article_id", 400
            return err_request

    def __delete_by_name(self, title, name) -> dict:
        result_of_delete = self.controller.delete_by_name(title, name)
        return result_of_delete


class CommentView(MethodView):
    def __init__(self):
        self.controller = CommentController()
        self.auth = AuthController()

    def get(self, article_id: str, name: str) -> dict and str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                getting_all_comments = self.__get()
                response = make_response(getting_all_comments)
            elif name is None:
                getting_comment_by_id = self.__get_by_id(article_id)
                response = make_response(getting_comment_by_id)
            else:
                getting_comment_by_name = self.__get_by_name(name)
                response = make_response(getting_comment_by_name)
            return response
        else:
            err_authorization = "Ошибка авторизации", 401
            response = make_response(err_authorization)
            return response

    def __get(self) -> dict:
        getting_all_comments = self.controller.get()
        return getting_all_comments

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            getting_comment_by_id  = self.controller.get_by_id(article_id)
            return getting_comment_by_id
        else:
            err_request = "Неправильный article_id", 400
            return err_request

    def __get_by_name(self, name) -> dict or str:

        getting_comment_by_name = self.controller.get_by_name(name)
        return getting_comment_by_name

    def post(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaAddComment().load(body_of_request)
            except ValidationError as err:
                error = err, 400
                response = make_response(error)
            else:
                result_of_create = self.controller.post(body_of_request)
                response = make_response(result_of_create)
            return response
        else:
            err_authorization = "Ошибка авторизации", 401
            response = make_response(err_authorization)
            return response

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaAddComment().load(body_of_request)
            except ValidationError as err:
                error = err, 400
                response = make_response(error)
            else:
                result_of_update = self.controller.put(body_of_request)
                response = make_response(result_of_update)
            return response
        else:
            err_authorization = "Ошибка авторизации", 401
            response = make_response(err_authorization)
            return response

    def delete(self, article_id: str, author_id: str, title: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and title is None:
                result_of_delete = self.__delete()
                response = make_response(result_of_delete)
            elif name is None and title is None:
                result_of_delete = self.__delete_by_id(article_id, author_id)
                response = make_response(result_of_delete)
            else:
                result_of_delete = self.__delete_by_name(title, name)
                response = make_response(result_of_delete)
            return response
        else:
            err_authorization = "Ошибка авторизации", 401
            response = make_response(err_authorization)
            return response

    def __delete(self) -> dict:
        result_of_delete = self.controller.delete()
        return result_of_delete

    def __delete_by_id(self, article_id, author_id) -> dict or str:
        if article_id.isdigit() and author_id.isdigit():
            result_of_delete = self.controller.delete_by_id(article_id, author_id)
            return result_of_delete
        else:
            err_request = ("Неправильный article_id", 400)
            return err_request

    def __delete_by_name(self, title, name) -> dict:
        result_of_delete = self.controller.delete_by_name(title, name)
        return result_of_delete
