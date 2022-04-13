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
        user = User(name=data['name'], password=data['password'], first_name=data['first_name'],
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
         data = self. __to_dataclass(new_article)
         result = self.models.create(data)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             serializer = jsonify(result)
             response = (serializer, 200)
         return response

     def put(self, update_article: dict):
         data = self.__to_update_dataclass(update_article)
         result = self.models.update(data)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response

     def __to_dataclass(self, data: dict) -> Article:
         article = Article(name=data['name'], text=data['text'], date=data['date'], user_id=data['author_id'])
         return article

     def __to_update_dataclass(self, data: dict) -> ArticleUpdate:
         article = ArticleUpdate(article_id=data['article_id'], name=data['name'], text=data['text'], date=data['date'])
         return article

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

     def post(self, new_like: dict):
         data = self.__to_dataclass(new_like)
         result = self.models.create(data)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response

     def __to_dataclass(self, data: dict) -> Like:
         like = Like(article_id=data['article_id'], user_id=data['user_id'])
         return like

     def delete(self):
         result = self.models.delete()
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response

     def delete_by_name(self, title: str, name: str):
         data = LikeGetById(article_name=title, user_name=name)
         result = self.models.delete_by_name(data)
         if result is None:
             response = ("Ошибка сервера", 500)
         else:
             response = ("Все Ok", 200)
         return response

     def delete_by_id(self, article_id: int, user_id: int):
         data = Like(article_id=article_id, user_id=user_id)
         result = self.models.delete_by_id(data)
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
        comment = self.__to_dataclass(data)
        result = self.models.create(comment)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response

    def put(self, data: dict):
        comment = self.__to_dataclass(data)
        result = self.models.update(comment)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response

    def __to_dataclass(self, data: dict) -> CommentCreate: # bad naming
        comment = CommentCreate(article_id=data['article_id'], user_id=data['user_id'], comment=data['comment'])
        return comment

    def __to_dataclass_id(self, article_id, author_id) -> CommentById:
        comment_by_id = CommentById(article_id=article_id, user_id=author_id)
        return comment_by_id

    def __to_dataclass_name(self, title, name) -> CommentByName:
        comment_by_name = CommentByName(article_name=title, user_name=name)
        return comment_by_name

    def delete(self):
        result = self.models.delete()
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response

    def delete_by_name(self, title: str, name: str):
        comment = self.__to_dataclass_name(title, name)
        result = self.models.delete_by_name(comment)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response

    def delete_by_id(self, article_id: str, author_id: str):
        comment = self.__to_dataclass_id(article_id, author_id)
        result = self.models.delete_by_id(comment)
        if result is None:
            response = ("Ошибка сервера", 500)
        else:
            response = ("Все Ok", 200)
        return response



