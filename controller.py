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

    def get(self) -> tuple:
        all_users = self.models.get()
        serializer = jsonify(all_users)
        response = serializer, 200
        return response

    def get_by_id(self, user_id: str) -> tuple:
        user_by_id = self.models.get_by_id(user_id)
        serializer = jsonify(user_by_id)
        response = serializer, 200
        return response

    def get_by_name(self, name: str) -> tuple:
        user_by_name = self.models.get_by_name(name)
        serializer = jsonify(user_by_name)
        response = serializer, 200
        return response

    def post(self, new_user_data: dict) -> tuple:
        new_user = self.__to_user_dataclass(new_user_data)
        user_cred = self.models.create(new_user)
        serializer = jsonify(user_cred)
        response = serializer, 200
        return response

    def put(self, update_user_data: dict) -> tuple:
        update_user = self.__to_user_dataclass(update_user_data)
        result_of_update = self.models.update(update_user)
        if result_of_update:
            response_of_update = "Ok", 200
            return response_of_update

    def __to_user_dataclass(self, data_user: dict) -> User:
        user = User(name=data_user.get('name'), password=data_user.get('password'),
                    first_name=data_user.get('first_name'),last_name=data_user.get('last_name'),
                    age=data_user.get('age'))
        return user

    def delete(self) -> tuple:
        result_of_delete = self.models.delete()
        if result_of_delete:
            response = "Ok", 200
            return response

    def delete_by_name(self, name: str) -> tuple:
        result_of_delete = self.models.delete_by_name(name)
        if result_of_delete:
            response = "Ok", 200
            return response

    def delete_by_id(self, user_id: str) -> tuple:
        result_of_delete = self.models.delete_by_id(user_id)
        if result_of_delete:
            response = "Ok", 200
            return response


class ArticleController:
     def __init__(self):
         self.models = ArticleModels()

     def get(self) -> tuple:
         all_articles = self.models.get()
         if all_articles:
             serializer = jsonify(all_articles)
             response = serializer, 200
             return response

     def get_by_id(self, article_id: str) -> tuple:
         article_by_id = self.models.get_by_id(article_id)
         if article_by_id:
             serializer = jsonify(article_by_id)
             response = serializer, 200
             return response

     def get_by_name(self, name: str) -> tuple:
         article_by_name = self.models.get_by_name(name)
         if article_by_name:
             serializer = jsonify(article_by_name)
             response = serializer, 200
             return response

     def post(self, new_article_data: dict) -> tuple:
         new_article = self. __to_article_create_dataclass(new_article_data)
         article_id = self.models.create(new_article)
         if article_id:
             serializer = jsonify(article_id)
             response = serializer, 200
             return response

     def put(self, update_article_data: dict) -> tuple:
         update_article = self.__to_article_update_dataclass(update_article_data)
         result_of_update = self.models.update(update_article)
         if result_of_update:
             response = "Ok", 200
             return response

     def __to_article_create_dataclass(self, data_article: dict) -> Article:
         article = Article(name=data_article['name'], text=data_article['text'], date=data_article['date'],
                           user_id=data_article['author_id'])
         return article

     def __to_article_update_dataclass(self, data_article: dict) -> ArticleUpdate:
         article = ArticleUpdate(article_id=data_article.get('article_id'), name=data_article.get('name'),
                                 text=data_article.get('text'), date=data_article.get('date'))
         return article

     def delete(self) -> tuple:
         result_of_delete = self.models.delete()
         if result_of_delete:
             response = "Ok", 200
             return response

     def delete_by_name(self, name: str) -> tuple:
         result_of_delete = self.models.delete_by_name(name)
         if result_of_delete:
             response = "Ok", 200
             return response

     def delete_by_id(self, article_id: str) -> tuple:
         result_of_delete = self.models.delete_by_id(article_id)
         if result_of_delete:
             response = "Ok", 200
             return response


class LikeController:
     def __init__(self):
         self.models = LikeModels()

     def get(self) -> tuple:
         all_likes = self.models.get()
         if all_likes:
             serializer = jsonify(all_likes )
             response = serializer, 200
             return response

     def get_by_id(self, article_id: str) -> tuple:
         like_by_id = self.models.get_by_id(article_id)
         if like_by_id:
             serializer = jsonify(like_by_id)
             response = serializer, 200
             return response

     def get_by_name(self, name: str) -> tuple:
         like_by_name = self.models.get_by_name(name)
         if like_by_name:
             serializer = jsonify(like_by_name)
             response = serializer, 200
             return response

     def post(self, new_like_data: dict) -> tuple:
         new_like = self.__to_like_dataclass(new_like_data)
         result_of_create = self.models.create(new_like)
         if result_of_create:
             response = "Ok", 200
             return response

     def __to_like_dataclass(self, data_like: dict) -> Like:
         like = Like(article_id=data_like['article_id'], user_id=data_like['user_id'])
         return like

     def delete(self) -> tuple:
         result_of_delete = self.models.delete()
         if result_of_delete:
             response = "Ok", 200
             return response

     def delete_by_name(self, title: str, name: str) -> tuple:
         data_like = LikeGetById(article_name=title, user_name=name)
         result_of_delete = self.models.delete_by_name(data_like)
         if result_of_delete:
             response = "Ok", 200
             return response

     def delete_by_id(self, article_id: str, user_id: str) -> tuple:
         data_like = Like(article_id=article_id, user_id=user_id)
         result_of_delete = self.models.delete_by_id(data_like)
         if result_of_delete:
             response = "Ok", 200
             return response


class CommentController:
    def __init__(self):
        self.models = CommentModels()

    def get(self) -> tuple:
        all_comments = self.models.get()
        if all_comments:
            serializer = jsonify(all_comments)
            response = serializer, 200
            return response

    def get_by_id(self, article_id: str) -> tuple:
        comment_by_id = self.models.get_by_id(article_id)
        if comment_by_id:
            serializer = jsonify(comment_by_id)
            response = serializer, 200
            return response

    def get_by_name(self, name: str) -> tuple:
        comment_by_name = self.models.get_by_name(name)
        if comment_by_name:
            serializer = jsonify(comment_by_name)
            response = serializer, 200
            return response

    def post(self, new_comment_data: dict) -> tuple:
        new_comment = self.__to_comment_dataclass(new_comment_data)
        result_of_create = self.models.create(new_comment)
        if result_of_create:
            response = "Ok", 200
            return response

    def put(self, update_comment_data: dict) -> tuple:
        update_comment = self.__to_comment_dataclass(update_comment_data)
        result_of_update = self.models.update(update_comment)
        if result_of_update:
            response = "Ok", 200
            return response

    def __to_comment_dataclass(self, data_comment: dict) -> CommentCreate:
        comment = CommentCreate(article_id=data_comment['article_id'], user_id=data_comment['user_id'],
                                comment=data_comment['comment'])
        return comment

    def __to_comment_id_dataclass(self, article_id: str, author_id: str) -> CommentById:
        comment_by_id = CommentById(article_id=article_id, user_id=author_id)
        return comment_by_id

    def __to_comment_name_dataclass(self, title: str, name: str) -> CommentByName:
        comment_by_name = CommentByName(article_name=title, user_name=name)
        return comment_by_name

    def delete(self) -> tuple:
        result_of_delete = self.models.delete()
        if result_of_delete:
            response = "Ok", 200
            return response

    def delete_by_name(self, title: str, name: str) -> tuple:
        delete_comment = self.__to_comment_name_dataclass(title, name)
        result_of_delete = self.models.delete_by_name(delete_comment)
        if result_of_delete:
            response = "Ok", 200
            return response

    def delete_by_id(self, article_id: str, author_id: str) -> tuple:
        delete_comment = self.__to_comment_id_dataclass(article_id, author_id)
        result_of_delete = self.models.delete_by_id(delete_comment)
        if result_of_delete:
            response = "Ok", 200
            return response



