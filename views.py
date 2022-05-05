from flask import make_response, Response
from flask import request
from flask.views import MethodView
from typing import Optional

from controller import ArticleController, LikeController, CommentController, UserController, AuthController
from tokens import token_extraction
from validation import SchemaAddArticle, SchemaUpdateArticle, SchemaAddLike, SchemaAddComment, SchemaAddUser, \
    SchemaUpdateUser


class UserView(MethodView):
    def __init__(self):
        self.controller = UserController()
        self.auth = AuthController()

    def get(self, user_id: Optional[str], name: Optional[str]) -> Response:
        '''
        Processes a get request to get user data:
        without parameter - getting data from all users,
        :param user_id: - unique user identifier
        :param name: - unique user nic name
        :return: data from all users or user data
        '''
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

    def __get(self) -> tuple:
        '''
        Processes a get request to get user data:
        without parameter - getting data from all users.
        :return: data from all users
        '''
        all_users = self.controller.get()
        return all_users

    def __get_by_id(self, user_id: str) -> tuple:
        '''
        Handles a get request to get user data by id
        :param user_id: - unique user identifier
        :return: user data
        '''
        if user_id.isdigit():
            user_by_id = self.controller.get_by_id(user_id)
            return user_by_id
        else:
            raise SystemError("Get user by id, wrong user_id")

    def __get_by_name(self, name: str) -> tuple:
        '''
        Handles a get request to get user data by nic name
        :param name: - unique user nic name
        :return: user data
        '''
        user_by_name = self.controller.get_by_name(name)
        return user_by_name

    def post(self) -> Response:
        '''
        Creating a new user
        :return: - unique user identifier
        '''
        body_of_request = request.get_json()
        SchemaAddUser().load(body_of_request)
        user_cred = self.controller.post(body_of_request)
        response = make_response(user_cred)
        return response

    def put(self) -> Response:
        '''
        User updating
        :return: - successful update response
        '''
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            SchemaUpdateUser().load(body_of_request)
            result_of_update = self.controller.put(body_of_request)
            response = make_response(result_of_update)
            return response
        else:
            raise SystemError("Update user, authorization error")

    def delete(self, user_id: Optional[str], name: Optional[str]) -> Response:
        '''
        User removing process
        without parameter - removing data from all users.
        :param user_id: - unique user identifier
        :param name: - unique user nic name
        :return: - successful delete response
        '''
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

    def __delete(self) -> tuple:
        '''
        User removing process
        without parameter - deleting data from all users.
        :return: - successful delete response
        '''
        result_of_delete = self.controller.delete()
        return result_of_delete

    def __delete_by_name(self, name: str) -> tuple:
        '''
        User removing by name
        :param name: - unique user nic name
        :return: - successful delete response
        '''
        result_of_delete = self.controller.delete_by_name(name)
        return result_of_delete

    def __delete_by_id(self, user_id: str) -> tuple:
        '''
        User removing by id
        :param user_id: - unique user identifier
        :return: - successful delete response
        '''
        if user_id.isdigit():
            result_of_delete = self.controller.delete_by_id(user_id)
            return result_of_delete
        else:
            raise SystemError("Delete user by id, wrong user_id")


class ArticleView(MethodView):
    def __init__(self):
        self.controller = ArticleController()
        self.auth = AuthController()

    def get(self, article_id: Optional[str], name: Optional[str]) -> Response:
        '''
        Processes a get request to get articles:
        without parameter - getting data from all articles,
        :param article_id:  - unique article identifier
        :param name:   - article title
        :return:  all articles or article
        '''
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

    def __get(self) -> tuple:
        '''
        Processes a get request to get articles:
        without parameter - getting data from all articles.
        :return: data from all articles
        '''
        all_articles = self.controller.get()
        return all_articles

    def __get_by_id(self, article_id: str) -> tuple:
        '''
        Handles a get request to get article by id
        :param article_id:  - unique article identifier
        :return: data of article
        '''
        if article_id.isdigit():
            article_by_id = self.controller.get_by_id(article_id)
            return article_by_id
        else:
            raise SystemError("Get article by id, wrong article_id")

    def __get_by_name(self, name: str) -> tuple:
        '''
        Handles a get request to get article by title
        :param name:   - article title
        :return:  data of article
        '''
        article_by_name = self.controller.get_by_name(name)
        return article_by_name

    def post(self) -> Response:
        '''
        Creating new article
        :return:  - unique article identifier
        '''
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            SchemaAddArticle().load(body_of_request)
            article_id_and_code_resp = self.controller.post(body_of_request)
            response = make_response(article_id_and_code_resp)
            return response
        else:
            raise SystemError("Create article, authorization error")

    def put(self) -> Response:
        '''
        Article updating
        :return:  - successful updating response
        '''
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            SchemaUpdateArticle().load(body_of_request)
            result_of_update = self.controller.put(body_of_request)
            response = make_response(result_of_update)
            return response
        else:
            raise SystemError("Update article, authorization error")

    def delete(self, article_id: Optional[str], name: Optional[str]) -> Response:
        '''
        Articles removing process
        without parameter - removing all articles.
        :param article_id: - unique article identifier
        :param name:  - article title
        :return:  - successful delete response
        '''
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

    def __delete(self) -> tuple:
        '''
        Article removing process
        without parameter - deleting all articles.
        :return:  - successful delete response
        '''
        result_of_delete = self.controller.delete()
        return result_of_delete

    def __delete_by_name(self, name: str) -> tuple:
        '''
        Article removing by title
        :param name:  -  article title
        :return:  - successful delete response
        '''
        result_of_delete = self.controller.delete_by_name(name)
        return result_of_delete

    def __delete_by_id(self, article_id: str) -> tuple:
        '''
        Article removing by id
        :param article_id:  - unique article identifier
        :return:  - successful delete response
        '''
        if article_id.isdigit():
            result_of_delete = self.controller.delete_by_id(article_id)
            return result_of_delete
        else:
            raise SystemError("Delete article by id, wrong article_id")


class LikeView(MethodView):
    def __init__(self):
        self.controller = LikeController()
        self.auth = AuthController()

    def get(self, article_id: Optional[str], name: Optional[str]) -> Response:
        '''
        Processes a get request to get likes of articles:
        without parameter - getting  all likes,
        :param article_id: - unique article identifier
        :param name: - article title
        :return: all likes or like
        '''
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

    def __get(self) -> tuple:
        '''
        Processes a get request to get likes:
        without parameter - getting all likes.
        :return: data all likes
        '''
        all_likes = self.controller.get()
        return all_likes

    def __get_by_id(self, article_id: str) -> tuple:
        '''
        Handles a get request to get likes by id
        :param article_id: - unique article identifier
        :return: data of likes
        '''
        if article_id.isdigit():
            like_by_id = self.controller.get_by_id(article_id)
            return like_by_id
        else:
            raise SystemError("Get like by id, wrong article_id")

    def __get_by_name(self, name: str) -> tuple:
        '''
        Handles a get request to get likes by title
        :param name: - article title
        :return: data of likes
        '''
        like_by_name = self.controller.get_by_name(name)
        return like_by_name

    def post(self) -> Response:
        '''
        Creating new like
        :return: - successful creating response
        '''
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            SchemaAddLike().load(body_of_request)
            result_of_create = self.controller.post(body_of_request)
            response = make_response(result_of_create)
            return response
        else:
            raise SystemError("Create like, authorization error")

    def delete(self, article_id: Optional[str], author_id: Optional[str], title: Optional[str],  name: Optional[str])\
            -> Response:
        '''
        Likes removing process
        without parameter - removing all likes.
        :param article_id: - unique article identifier
        :param author_id: - unique user identifier
        :param title: - article title
        :param name: - unique user nic name
        :return: - successful delete response
        '''
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

    def __delete(self) -> tuple:
        '''
        Likes removing process
        without parameter - removing all likes.
        :return: - successful delete response
        '''
        result_of_delete = self.controller.delete()
        return result_of_delete

    def __delete_by_id(self, article_id: str, author_id: str) -> tuple:
        '''
        Likes removing by id
        :param article_id: - unique article identifier
        :param author_id: - unique user identifier
        :return: - successful delete response
        '''
        if article_id.isdigit() and author_id.isdigit():
            result_of_delete = self.controller.delete_by_id(article_id, author_id)
            return result_of_delete
        else:
            raise SystemError("Delete like by id, wrong article_id")

    def __delete_by_name(self, title: str, name: str) -> tuple:
        '''
        Likes removing by name
        :param title: article title
        :param name: unique user nic name
        :return: - successful delete response
        '''
        result_of_delete = self.controller.delete_by_name(title, name)
        return result_of_delete


class CommentView(MethodView):
    def __init__(self):
        self.controller = CommentController()
        self.auth = AuthController()

    def get(self, article_id: Optional[str], name: Optional[str]) -> Response:
        '''
        Processes a get request to get comments of articles:
        without parameter - getting  all comments,
        :param article_id: - unique article identifier
        :param name:  article title
        :return: all comments or comment
        '''
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

    def __get(self) -> tuple:
        '''
        Processes a get request to get comments:
        without parameter - getting all comments.
        :return: all comments
        '''
        all_comments = self.controller.get()
        return all_comments

    def __get_by_id(self, article_id: str) -> tuple:
        '''
        Handles a get request to get comment by id
        :param article_id: - unique article identifier
        :return: data of comment
        '''
        if article_id.isdigit():
            comment_by_id = self.controller.get_by_id(article_id)
            return comment_by_id
        else:
            raise SystemError("Get comment by id, wrong article_id")

    def __get_by_name(self, name: str) -> tuple:
        '''
        Handles a get request to get comment by title
        :param name: - article title
        :return: data of comment
        '''
        comment_by_name = self.controller.get_by_name(name)
        return comment_by_name

    def post(self) -> Response:
        '''
        Creating new comment
        :return: - successful creating response
        '''
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            SchemaAddComment().load(body_of_request)
            result_of_create = self.controller.post(body_of_request)
            response = make_response(result_of_create)
            return response
        else:
            raise SystemError("Create comment, authorization error")

    def put(self) -> Response:
        '''
        Updating comments
        :return: - successful updating response
        '''
        token = token_extraction()
        authorized = self.auth.authorization(token)
        if authorized:
            body_of_request = request.get_json()
            SchemaAddComment().load(body_of_request)
            result_of_update = self.controller.put(body_of_request)
            response = make_response(result_of_update)
            return response
        else:
            raise SystemError("Update comment, authorization error")

    def delete(self, article_id: Optional[str], author_id: Optional[str], title: Optional[str], name: Optional[str])\
            -> Response:
        '''
        Comments removing process
        without parameter - removing all comments.
        :param article_id: - unique article identifier
        :param author_id: - unique user identifier
        :param title: - article title
        :param name: - unique user nic name
        :return: - successful delete response
        '''
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

    def __delete(self) -> tuple:
        '''
        Comments removing process
        without parameter - removing all comments.
        :return: - successful delete response
        '''
        result_of_delete = self.controller.delete()
        return result_of_delete

    def __delete_by_id(self, article_id: str, author_id: str) -> tuple:
        '''
        Comment removing by id
        :param article_id: - unique article identifier
        :param author_id: - unique user identifier
        :return: - successful delete response
        '''
        if article_id.isdigit() and author_id.isdigit():
            result_of_delete = self.controller.delete_by_id(article_id, author_id)
            return result_of_delete
        else:
            raise SystemError("Delete comment by id, wrong article_id")

    def __delete_by_name(self, title: str, name: str) -> tuple:
        '''
        Comment removing by name
        :param title: - article title
        :param name: - unique user nic name
        :return: - successful delete response
        '''
        result_of_delete = self.controller.delete_by_name(title, name)
        return result_of_delete
