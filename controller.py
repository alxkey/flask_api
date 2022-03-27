from flask import jsonify

from models import UserModels, ArticleModels, LikeModels, CommentModels
from tokens import TokenGen, TokenCheck

class UserController:
    def __init__(self):
        self.models = UserModels()

    def get(self, token):
        all_users = self.models.get(token)
        serializer = jsonify(all_users)
        return serializer

    def get_by_id(self, user_id: str, token: str):
        user = self.models.get_by_id(user_id, token)
        serializer = jsonify(user)
        return serializer

    def get_by_name(self, name: str, token: str):
        user = self.models.get_by_name(name, token)
        serializer = jsonify(user)
        return serializer

    def post(self, new_user: dict):
        user_id = self.models.post(new_user)
        token_obj = TokenGen()
        token = token_obj.generate(user_id)
        result = self.models.save_token(user_id, token)
        if result:
            serializer = jsonify({'user_id': user_id, 'token': token})
            return serializer
        else:
            return("500")

    def put(self, update_user: dict, token: str):
        user_id = self.models.put(update_user, token)
        serializer = jsonify(user_id)
        return serializer

    def delete(self, token: str):
        response = self.models.delete(token)
        return response

    def delete_by_name(self, name: str, token: str):
        response = self.models.delete_by_name(name, token)
        return response

    def delete_by_id(self, user_id: str, token: str):
        response = self.models.delete_by_id(user_id, token)
        return response


class ArticleController:
     def __init__(self):
         self.models = ArticleModels()

     def get(self, token: str):
         all_articles = self.models.get(token)
         serializer = jsonify(all_articles)
         return serializer

     def get_by_id(self, article_id: str, token: str):
         article = self.models.get_by_id(article_id, token)
         serializer = jsonify(article)
         return serializer

     def get_by_name(self, name: str, token: str):
         article = self.models.get_by_name(name, token)
         serializer = jsonify(article)
         return serializer

     def post(self, new_article: dict, token: str):
         article_id = self.models.post(new_article, token)
         serializer = jsonify(article_id)
         return serializer

     def put(self, update_article: dict, token: str):
         article_id = self.models.put(update_article, token)
         serializer = jsonify(article_id)
         return serializer

     def delete(self, token: str):
         response = self.models.delete(token)
         return response

     def delete_by_name(self, name: str, token: str):
         response = self.models.delete_by_name(name, token)
         return response

     def delete_by_id(self, article_id: str, token: str):
         response = self.models.delete_by_id(article_id, token)
         return response


class LikeController:
     def __init__(self):
         self.models = LikeModels()

     def get(self, token: str):
         all_articles = self.models.get(token)
         serializer = jsonify(all_articles)
         return serializer

     def get_by_id(self, article_id: str, token: str):
         article = self.models.get_by_id(article_id, token)
         serializer = jsonify(article)
         return serializer

     def get_by_name(self, name: str, token: str):
         article = self.models.get_by_name(name, token)
         serializer = jsonify(article)
         return serializer

     def post(self, data: dict, token: str):
         response = self.models.post(data, token)
         return response

     def delete(self, token: str):
         response = self.models.delete(token)
         return response

     def delete_by_name(self, title: str, name: str, token: str):
         response = self.models.delete_by_name(title, name, token)
         return response

     def delete_by_id(self, article_id: str, author_id: str, token: str):
         response = self.models.delete_by_id(article_id, author_id, token)
         return response


class CommentController:
    def __init__(self):
        self.models = CommentModels()

    def get(self, token: str):
        all_articles = self.models.get(token)
        serializer = jsonify(all_articles)
        return serializer

    def get_by_id(self, article_id: str, token: str):
        article = self.models.get_by_id(article_id, token)
        serializer = jsonify(article)
        return serializer

    def get_by_name(self, name: str, token: str):
        article = self.models.get_by_name(name, token)
        serializer = jsonify(article)
        return serializer

    def post(self, data: dict, token: str):
        article_id = self.models.post(data, token)
        serializer = jsonify(article_id)
        return serializer

    def put(self, data: dict, token: str):
        article_id = self.models.put(data, token)
        serializer = jsonify(article_id)
        return serializer

    def delete(self, token: str):
        response = self.models.delete(token)
        return response

    def delete_by_name(self, title: str, name: str, token: str):
        response = self.models.delete_by_name(title, name, token)
        return response

    def delete_by_id(self, article_id: str, author_id: str, token: str):
        response = self.models.delete_by_id(article_id, author_id, token)
        return response



