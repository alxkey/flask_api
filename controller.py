from flask import jsonify

from models import UserModels, ArticleModels, LikeModels, CommentModels, AuthModel
from dataclass import User, Article, ArticleUpdate, Like, LikeGetById, CommentCreate, CommentById, CommentByName


class AuthController:
    def __init__(self):
        self.auth = AuthModel()

    def authorization(self, token):
        authorized = self.auth.authorization(token)
        return authorized


class UserController:
    def __init__(self):
        self.models = UserModels()

    def get(self):
        all_users = self.models.get()
        serializer = jsonify(all_users)
        response = serializer, 200
        return response

    def get_by_id(self, user_id: str):
        user_by_id = self.models.get_by_id(user_id)
        serializer = jsonify(user_by_id)
        response = serializer, 200
        return response

    def get_by_name(self, name: str):
        user_by_name = self.models.get_by_name(name)
        serializer = jsonify(user_by_name)
        response = serializer, 200
        return response

    def post(self, new_user_data: dict):
        new_user = self.__to_user_dataclass(new_user_data)
        user_cred = self.models.create(new_user)
        serializer = jsonify(user_cred)
        response = serializer, 200
        return response

    def put(self, update_user_data: dict):
        update_user = self.__to_user_dataclass(update_user_data)
        result_of_update = self.models.update(update_user)
        if result_of_update:
            response_of_update = "Ok", 200
            return response_of_update

    def __to_user_dataclass(self, data: dict) -> User:
        user = User(name=data['name'], password=data['password'], first_name=data['first_name'],
                    last_name=data['last_name'], age=data['age'])
        return user

    def delete(self):
        result_of_delete = self.models.delete()
        if result_of_delete:
            response = "Ok", 200
            return response

    def delete_by_name(self, name: str):
        result_of_delete = self.models.delete_by_name(name)
        if result_of_delete:
            response = "Ok", 200
            return response

    def delete_by_id(self, user_id: str):
        result_of_delete = self.models.delete_by_id(user_id)
        if result_of_delete:
            response = "Ok", 200
            return response


class ArticleController:
     def __init__(self):
         self.models = ArticleModels()

     def get(self):
         all_articles = self.models.get()
         if all_articles:
             serializer = jsonify(all_articles)
             response = serializer, 200
             return response

     def get_by_id(self, article_id: str):
         article_by_id = self.models.get_by_id(article_id)
         if article_by_id:
             serializer = jsonify(article_by_id)
             response = serializer, 200
             return response

     def get_by_name(self, name: str):
         article_by_name = self.models.get_by_name(name)
         if article_by_name:
             serializer = jsonify(article_by_name)
             response = serializer, 200
             return response

     def post(self, new_article_data: dict):
         new_article = self. __to_article_create_dataclass(new_article_data)
         article_id = self.models.create(new_article)
         if article_id:
             serializer = jsonify(article_id)
             response = serializer, 200
             return response

     def put(self, update_article_data: dict):
         update_article = self.__to_article_update_dataclass(update_article_data)
         result_of_update = self.models.update(update_article)
         if result_of_update:
             response = "Ok", 200
             return response

     def __to_article_create_dataclass(self, data: dict) -> Article:
         article = Article(name=data['name'], text=data['text'], date=data['date'], user_id=data['author_id'])
         return article

     def __to_article_update_dataclass(self, data: dict) -> ArticleUpdate:
         article = ArticleUpdate(article_id=data['article_id'], name=data['name'], text=data['text'], date=data['date'])
         return article

     def delete(self):
         result_of_delete = self.models.delete()
         if result_of_delete:
             response = "Ok", 200
             return response

     def delete_by_name(self, name: str):
         result_of_delete = self.models.delete_by_name(name)
         if result_of_delete:
             response = "Ok", 200
             return response

     def delete_by_id(self, article_id: str):
         result_of_delete = self.models.delete_by_id(article_id)
         if result_of_delete:
             response = "Ok", 200
             return response


class LikeController:
     def __init__(self):
         self.models = LikeModels()

     def get(self):
         all_likes = self.models.get()
         if all_likes:
             serializer = jsonify(all_likes )
             response = serializer, 200
             return response

     def get_by_id(self, article_id: str):
         like_by_id = self.models.get_by_id(article_id)
         if like_by_id:
             serializer = jsonify(like_by_id)
             response = serializer, 200
             return response

     def get_by_name(self, name: str):
         like_by_name = self.models.get_by_name(name)
         if like_by_name:
             serializer = jsonify(like_by_name)
             response = serializer, 200
             return response

     def post(self, new_like_data: dict):
         new_like = self.__to_like_dataclass(new_like_data)
         result_of_create = self.models.create(new_like)
         if result_of_create:
             response = "Ok", 200
             return response

     def __to_like_dataclass(self, data: dict) -> Like:
         like = Like(article_id=data['article_id'], user_id=data['user_id'])
         return like

     def delete(self):
         result_of_delete = self.models.delete()
         if result_of_delete:
             response = "Ok", 200
             return response

     def delete_by_name(self, title: str, name: str):
         data_like = LikeGetById(article_name=title, user_name=name)
         result_of_delete = self.models.delete_by_name(data_like)
         if result_of_delete:
             response = "Ok", 200
             return response

     def delete_by_id(self, article_id: int, user_id: int):
         data_like = Like(article_id=article_id, user_id=user_id)
         result_of_delete = self.models.delete_by_id(data_like)
         if result_of_delete:
             response = "Ok", 200
             return response


class CommentController:
    def __init__(self):
        self.models = CommentModels()

    def get(self):
        all_comments = self.models.get()
        if all_comments:
            serializer = jsonify(all_comments)
            response = serializer, 200
            return response

    def get_by_id(self, article_id: str):
        comment_by_id = self.models.get_by_id(article_id)
        if comment_by_id:
            serializer = jsonify(comment_by_id)
            response = serializer, 200
            return response

    def get_by_name(self, name: str):
        comment_by_name = self.models.get_by_name(name)
        if comment_by_name:
            serializer = jsonify(comment_by_name)
            response = serializer, 200
            return response

    def post(self, new_comment_data: dict):
        new_comment = self.__to_comment_dataclass(new_comment_data)
        result_of_create = self.models.create(new_comment)
        if result_of_create:
            response = "Ok", 200
            return response

    def put(self, update_comment_data: dict):
        update_comment = self.__to_comment_dataclass(update_comment_data)
        result_of_update = self.models.update(update_comment)
        if result_of_update:
            response = "Ok", 200
            return response

    def __to_comment_dataclass(self, data: dict) -> CommentCreate: # bad naming
        comment = CommentCreate(article_id=data['article_id'], user_id=data['user_id'], comment=data['comment'])
        return comment

    def __to_comment_id_dataclass(self, article_id, author_id) -> CommentById:
        comment_by_id = CommentById(article_id=article_id, user_id=author_id)
        return comment_by_id

    def __to_comment_name_dataclass(self, title, name) -> CommentByName:
        comment_by_name = CommentByName(article_name=title, user_name=name)
        return comment_by_name

    def delete(self):
        result_of_delete = self.models.delete()
        if result_of_delete:
            response = "Ok", 200
            return response

    def delete_by_name(self, title: str, name: str):
        delete_comment = self.__to_comment_name_dataclass(title, name)
        result_of_delete = self.models.delete_by_name(delete_comment)
        if result_of_delete:
            response = "Ok", 200
            return response

    def delete_by_id(self, article_id: str, author_id: str):
        delete_comment = self.__to_comment_id_dataclass(article_id, author_id)
        result_of_delete = self.models.delete_by_id(delete_comment)
        if result_of_delete:
            response = "Ok", 200
            return response



