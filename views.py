from flask import make_response
from flask import request
from flask.views import MethodView
from marshmallow import ValidationError

from controller import ArticleController, LikeController, CommentController, UserController, AuthController
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
                all_users = self.__get()
                response = make_response(all_users)
                return response
            elif name is None:
                user_by_id = self.__get_by_id(user_id)
                response = make_response(user_by_id)
                return response
            else:
                user_by_name = self.__get_by_name(name)
                response = make_response(user_by_name)
                return response
        else:
            raise SystemError("Get user, authorization error")

    def __get(self) -> dict:
        all_users = self.controller.get()
        return all_users

    def __get_by_id(self, user_id) -> dict or str:
        if user_id.isdigit():
            user_by_id = self.controller.get_by_id(user_id)
            return user_by_id
        else:
            raise SystemError("Get user by id, wrong user_id")

    def __get_by_name(self, name):
        user_by_name = self.controller.get_by_name(name)
        return user_by_name

    def post(self) -> dict or str:
        body_of_request = request.get_json()
        try:
            SchemaAddUser().load(body_of_request)
        except ValidationError as err:
            raise SystemError(f"Create user, ValidationError: {err}")
        else:
            user_cred = self.controller.post(body_of_request)
            response = make_response(user_cred)
        return response

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaUpdateUser().load(body_of_request)
            except ValidationError as err:
                raise SystemError(f"Update user, ValidationError: {err}")
            else:
                result_of_update = self.controller.put(body_of_request)
                response = make_response(result_of_update)
            return response
        else:
            raise SystemError("Update user, authorization error")

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
            raise SystemError("Delete user, authorization error")

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
            raise SystemError("Delete user by id, wrong user_id")


class ArticleView(MethodView):
    def __init__(self):
        self.controller = ArticleController()
        self.auth = AuthController()

    def get(self, article_id: str, name: str):
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                all_articles = self.__get()
                response = make_response(all_articles)
                return response
            elif name is None:
                article_by_id = self.__get_by_id(article_id)
                response = make_response(article_by_id)
                return response
            else:
                article_by_name = self.__get_by_name(name)
                response = make_response(article_by_name)
                return response
        else:
            raise SystemError("Get article, authorization error")

    def __get(self) -> dict:
        all_articles = self.controller.get()
        return all_articles

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            article_by_id = self.controller.get_by_id(article_id)
            return article_by_id
        else:
            raise SystemError("Get article by id, wrong article_id")

    def __get_by_name(self, name):
        article_by_name = self.controller.get_by_name(name)
        return article_by_name

    def post(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaAddArticle().load(body_of_request)
            except ValidationError as err:
                raise SystemError(f"Create article, ValidationError: {err}")
            else:
                article_id_and_code_resp = self.controller.post(body_of_request)
                response = make_response(article_id_and_code_resp)
            return response
        else:
            raise SystemError("Create article, authorization error")

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaUpdateArticle().load(body_of_request)
            except ValidationError as err:
                raise SystemError(f"Update article, ValidationError: {err}")
            else:
                 result_of_update = self.controller.put(body_of_request)
                 response = make_response(result_of_update)
            return response
        else:
            raise SystemError("Update article, authorization error")

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
            raise SystemError("Delete article, authorization error")

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
            raise SystemError("Delete article by id, wrong article_id")


class LikeView(MethodView):
    def __init__(self):
        self.controller = LikeController()
        self.auth = AuthController()

    def get(self, article_id: str, name: str) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            if article_id is None and name is None:
                all_likes = self.__get()
                response = make_response(all_likes)
            elif name is None:
                like_by_id = self.__get_by_id(article_id)
                response = make_response(like_by_id)
            else:
                like_by_name = self.__get_by_name(name)
                response = make_response(like_by_name)
            return response
        else:
            raise SystemError("Get like, authorization error")

    def __get(self) -> dict:
        all_likes = self.controller.get()
        return all_likes

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            like_by_id = self.controller.get_by_id(article_id)
            return like_by_id
        else:
            raise SystemError("Get like by id, wrong article_id")

    def __get_by_name(self, name) -> dict or str:
        like_by_name = self.controller.get_by_name(name)
        return like_by_name

    def post(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaAddLike().load(body_of_request)
            except ValidationError as err:
                raise SystemError(f"Create like, ValidationError: {err}")
            else:
                result_of_create = self.controller.post(body_of_request)
                response = make_response(result_of_create)
            return response
        else:
            raise SystemError("Create like, authorization error")

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
            raise SystemError("Delete like, authorization error")

    def __delete(self) -> dict:
        result_of_delete = self.controller.delete()
        return result_of_delete

    def __delete_by_id(self, article_id, author_id) -> dict or str:
        if article_id.isdigit() and author_id.isdigit():
            result_of_delete = self.controller.delete_by_id(article_id, author_id)
            return result_of_delete
        else:
            raise SystemError("Delete like by id, wrong article_id")

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
                all_comments = self.__get()
                response = make_response(all_comments)
            elif name is None:
                comment_by_id = self.__get_by_id(article_id)
                response = make_response(comment_by_id)
            else:
                comment_by_name = self.__get_by_name(name)
                response = make_response(comment_by_name)
            return response
        else:
            raise SystemError("Get comment, authorization error")

    def __get(self) -> dict:
        all_comments = self.controller.get()
        return all_comments

    def __get_by_id(self, article_id) -> dict or str:
        if article_id.isdigit():
            comment_by_id = self.controller.get_by_id(article_id)
            return comment_by_id
        else:
            raise SystemError("Get comment by id, wrong article_id")

    def __get_by_name(self, name) -> dict or str:

        comment_by_name = self.controller.get_by_name(name)
        return comment_by_name

    def post(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaAddComment().load(body_of_request)
            except ValidationError as err:
                raise SystemError(f"Create comment, ValidationError: {err}")
            else:
                result_of_create = self.controller.post(body_of_request)
                response = make_response(result_of_create)
            return response
        else:
            raise SystemError("Create comment, authorization error")

    def put(self) -> dict or str:
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            try:
                SchemaAddComment().load(body_of_request)
            except ValidationError as err:
                raise SystemError(f"Update comment, ValidationError: {err}")
            else:
                result_of_update = self.controller.put(body_of_request)
                response = make_response(result_of_update)
            return response
        else:
            raise SystemError("Update comment, authorization error")

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
            raise SystemError("Delete comment, authorization error")

    def __delete(self) -> dict:
        result_of_delete = self.controller.delete()
        return result_of_delete

    def __delete_by_id(self, article_id, author_id) -> dict or str:
        if article_id.isdigit() and author_id.isdigit():
            result_of_delete = self.controller.delete_by_id(article_id, author_id)
            return result_of_delete
        else:
            raise SystemError("Delete comment by id, wrong article_id")

    def __delete_by_name(self, title, name) -> dict:
        result_of_delete = self.controller.delete_by_name(title, name)
        return result_of_delete
