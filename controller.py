from flask import jsonify

from models import ArticleModels, LikeModels, CommentModels


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
         article_id = self.models.post(new_article)
         serializer = jsonify(article_id)
         return serializer

     def put(self, update_article: dict):
         article_id = self.models.put(update_article)
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
         response = self.models.post(data)
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
        article_id = self.models.post(data)
        serializer = jsonify(article_id)
        return serializer

    def put(self, data: dict):
        article_id = self.models.put(data)
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



