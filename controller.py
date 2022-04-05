from flask import jsonify

from models import UserModels, ArticleModels, LikeModels, CommentModels, AuthModel
from dataclass import User


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
        result = self.models.get()
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            serializer = jsonify(result)
            response = (serializer, 200)
        return response

    def get_by_id(self, user_id: str):
        result = self.models.get_by_id(user_id)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            serializer = jsonify(result)
            response = (serializer, 200)
        return response

    def get_by_name(self, name: str):
        result = self.models.get_by_name(name)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            serializer = jsonify(result)
            response = (serializer, 200)
        return response

    def post(self, user: dict):
        print(user)
        data = self.__to_dataclass(user)
        result = self.models.create(data)
        print(result)
        print(type(result))
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            serializer = jsonify(result)
            print(serializer)
            print(type(serializer))
            response = (serializer, 200)
        return response

    def put(self, update_user: dict):
        data = self.__to_dataclass(update_user)
        result = self.models.update(data)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response

    def __to_dataclass(self, data: dict) -> User:
        user = User(name=data['name'], password=data['password'], first_name=data['first_name'],\
                    last_name=data['last_name'], age=data['age'])
        return user

    def delete(self):
        result = self.models.delete()
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response

    def delete_by_name(self, name: str):
        result = self.models.delete_by_name(name)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response

    def delete_by_id(self, user_id: str):
        result = self.models.delete_by_id(user_id)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response


class ArticleController:
     def __init__(self):
         self.models = ArticleModels()

     def get(self):
         result = self.models.get()
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             serializer = jsonify(result)
             response = (serializer, 200)
         return response

     def get_by_id(self, article_id: str):
         result = self.models.get_by_id(article_id)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             serializer = jsonify(result)
             response = (serializer, 200)
         return response

     def get_by_name(self, name: str):
         result = self.models.get_by_name(name)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             serializer = jsonify(result)
             response = (serializer, 200)
         return response

     def post(self, new_article: dict):
         result = self.models.create(new_article)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             serializer = jsonify(result)
             response = (serializer, 200)
         return response

     def put(self, update_article: dict):
         result = self.models.update(update_article)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response

     def delete(self):
         result = self.models.delete()
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response

     def delete_by_name(self, name: str):
         result = self.models.delete_by_name(name)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response

     def delete_by_id(self, article_id: str):
         result = self.models.delete_by_id(article_id)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response


class LikeController:
     def __init__(self):
         self.models = LikeModels()

     def get(self):
         result = self.models.get()
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             serializer = jsonify(result)
             response = (serializer, 200)
         return response

     def get_by_id(self, article_id: str):
         result = self.models.get_by_id(article_id)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             serializer = jsonify(result)
             response = (serializer, 200)
         return response

     def get_by_name(self, name: str):
         result = self.models.get_by_name(name)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             serializer = jsonify(result)
             response = (serializer, 200)
         return response

     def post(self, data: dict):
         result = self.models.create(data)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response

     def delete(self):
         result = self.models.delete()
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response

     def delete_by_name(self, title: str, name: str):
         result = self.models.delete_by_name(title, name)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response

     def delete_by_id(self, article_id: str, author_id: str):
         result = self.models.delete_by_id(article_id, author_id)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response


class CommentController:
    def __init__(self):
        self.models = CommentModels()

    def get(self):
        result = self.models.get()
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            serializer = jsonify(result)
            response = (serializer, 200)
        return response

    def get_by_id(self, article_id: str):
        result = self.models.get_by_id(article_id)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            serializer = jsonify(result)
            response = (serializer, 200)
        return response

    def get_by_name(self, name: str):
        result = self.models.get_by_name(name)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            serializer = jsonify(result)
            response = (serializer, 200)
        return response

    def post(self, data: dict):
        result = self.models.create(data)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response

    def put(self, data: dict):
        result = self.models.update(data)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response

    def delete(self):
        result = self.models.delete()
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response

    def delete_by_name(self, title: str, name: str):
        result = self.models.delete_by_name(title, name)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response

    def delete_by_id(self, article_id: str, author_id: str):
        result = self.models.delete_by_id(article_id, author_id)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response



