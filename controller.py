from flask import jsonify

from models import UserModels, ArticleModels, LikeModels, CommentModels, AuthModel


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
        return serializer

    def get_by_id(self, user_id: str):
        user = self.models.get_by_id(user_id)
        serializer = jsonify(user)
        return serializer

    def get_by_name(self, name: str):
        user = self.models.get_by_name(name)
        serializer = jsonify(user)
        return serializer

    def post(self, new_user: dict):
        result = self.models.create(new_user)
        if result:
            serializer = jsonify(result)
            return serializer
        else:
            result = "Ошибка сервера"
            return result

    def put(self, update_user: dict):
        result = self.models.update(update_user)
        if result:
            result = "Все ок"
        else:
            result = "Ошибка сервера"
        return result

    def delete(self):
        response = self.models.delete()
        return response

    def delete_by_name(self, name: str):
        response = self.models.delete_by_name(name)
        return response

    def delete_by_id(self, user_id: str):
        response = self.models.delete_by_id(user_id)
        return response


class ArticleController:
     def __init__(self):
         self.models = ArticleModels()

     def get(self):
         all_articles = self.models.get()
         serializer = jsonify(all_articles)
         return serializer

     def get_by_id(self, article_id: str):
         article = self.models.get_by_id(article_id)
         serializer = jsonify(article)
         return serializer

     def get_by_name(self, name: str):
         article = self.models.get_by_name(name)
         serializer = jsonify(article)
         return serializer

     def post(self, new_article: dict):
         article_id = self.models.create(new_article)
         serializer = jsonify(article_id)
         return serializer

     def put(self, update_article: dict):
         article_id = self.models.update(update_article)
         serializer = jsonify(article_id)
         return serializer

     def delete(self):
         response = self.models.delete()
         return response

     def delete_by_name(self, name: str):
         response = self.models.delete_by_name(name)
         return response

     def delete_by_id(self, article_id: str):
         response = self.models.delete_by_id(article_id)
         return response


class LikeController:
     def __init__(self):
         self.models = LikeModels()

     def get(self):
         all_articles = self.models.get()
         serializer = jsonify(all_articles)
         return serializer

     def get_by_id(self, article_id: str):
         article = self.models.get_by_id(article_id)
         serializer = jsonify(article)
         return serializer

     def get_by_name(self, name: str):
         article = self.models.get_by_name(name)
         serializer = jsonify(article)
         return serializer

     def post(self, data: dict):
         response = self.models.create(data)
         return response

     def delete(self):
         response = self.models.delete()
         return response

     def delete_by_name(self, title: str, name: str):
         response = self.models.delete_by_name(title, name)
         return response

     def delete_by_id(self, article_id: str, author_id: str):
         response = self.models.delete_by_id(article_id, author_id)
         return response


class CommentController:
    def __init__(self):
        self.models = CommentModels()

    def get(self):
        all_articles = self.models.get()
        serializer = jsonify(all_articles)
        return serializer

    def get_by_id(self, article_id: str):
        article = self.models.get_by_id(article_id)
        serializer = jsonify(article)
        return serializer

    def get_by_name(self, name: str):
        article = self.models.get_by_name(name)
        serializer = jsonify(article)
        return serializer

    def post(self, data: dict):
        article_id = self.models.create(data)
        serializer = jsonify(article_id)
        return serializer

    def put(self, data: dict):
        article_id = self.models.update(data)
        serializer = jsonify(article_id)
        return serializer

    def delete(self):
        response = self.models.delete()
        return response

    def delete_by_name(self, title: str, name: str):
        response = self.models.delete_by_name(title, name)
        return response

    def delete_by_id(self, article_id: str, author_id: str):
        response = self.models.delete_by_id(article_id, author_id)
        return response



