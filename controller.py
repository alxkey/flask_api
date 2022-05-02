from flask import jsonify

from models import UserModels, ArticleModels, LikeModels, CommentModels, AuthModel
from dataclass import User, UserUpdate,  Article, ArticleUpdate, Like, LikeGetById, CommentCreate, CommentById,\
                      CommentByName

class AuthController:
    def __init__(self):
        self.auth = AuthModel()

    def authorization(self, token):
        '''
        Check token
        :param token: user token
        :return: user_id corresponding to the token
        '''
        authorized = self.auth.authorization(token)
        return authorized


class UserController:
    def __init__(self):
        self.models = UserModels()

    def get(self) -> tuple:
        '''
        Getting data from all users.
        :return: data from all users
        '''
        all_users = self.models.get()
        serializer = jsonify(all_users)
        response = serializer, 200
        return response

    def get_by_id(self, user_id: str) -> tuple:
        '''
        Handles a get request to get user data by id
        :param user_id: - unique user identifier
        :return: user data
        '''
        user_by_id = self.models.get_by_id(user_id)
        serializer = jsonify(user_by_id)
        response = serializer, 200
        return response

    def get_by_name(self, name: str) -> tuple:
        '''
        Handles a get request to get user data by nic name
        :param name: - unique user nic name
        :return: user data
        '''
        user_by_name = self.models.get_by_name(name)
        serializer = jsonify(user_by_name)
        response = serializer, 200
        return response

    def post(self, new_user_data: dict) -> tuple:
        '''
        Creating new user
        :param new_user_data: dict from request body
        :return:  - unique user identifier
        '''
        new_user = self.__to_user_dataclass(new_user_data)
        user_cred = self.models.create(new_user)
        serializer = jsonify(user_cred)
        response = serializer, 200
        return response

    def put(self, update_user_data: dict) -> tuple:
        '''
        User updating
        :param update_user_data: dict from request body
        :return: - successful updating response
        '''
        update_user = self.__to_user_update_dataclass(update_user_data)
        self.models.update(update_user)
        response_of_update = "Ok", 200
        return response_of_update

    def __to_user_dataclass(self, data_user: dict) -> User:
        '''
        Convert dict from request body to user dataclass
        :param data_user: dict from request body
        :return: instance of user dataclass
        '''
        user = User(name=data_user.get('name'),
                    password=data_user.get('password'),
                    first_name=data_user.get('first_name'),
                    last_name=data_user.get('last_name'),
                    age=data_user.get('age'))
        return user

    def __to_user_update_dataclass(self, data_user: dict) -> UserUpdate:
        '''
        Convert dict from request body to user dataclass
        :param data_user: dict from request body
        :return: instance of user dataclass
        '''
        user = UserUpdate(user_id=data_user.get('user_id'),
                    name=data_user.get('name'),
                    password=data_user.get('password'),
                    first_name=data_user.get('first_name'),
                    last_name=data_user.get('last_name'),
                    age=data_user.get('age'))
        return user

    def delete(self) -> tuple:
        '''
        Removing data from all users.
        :return:  - successful delete response
        '''
        self.models.delete()
        response = "Ok", 200
        return response

    def delete_by_name(self, name: str) -> tuple:
        '''
        User removing by name
        :param name: - unique user nic name
        :return:  - successful delete response
        '''
        self.models.delete_by_name(name)
        response = "Ok", 200
        return response

    def delete_by_id(self, user_id: str) -> tuple:
        '''
        User removing by id
        :param user_id: - unique user identifier
        :return:  - successful delete response
        '''
        self.models.delete_by_id(user_id)
        response = "Ok", 200
        return response


class ArticleController:
     def __init__(self):
         self.models = ArticleModels()

     def get(self) -> tuple:
         '''
         Getting data from all articles.
         :return: data from all articles
         '''
         all_articles = self.models.get()
         serializer = jsonify(all_articles)
         response = serializer, 200
         return response

     def get_by_id(self, article_id: str) -> tuple:
         '''
         Handles a get request to get article by id
         :param article_id:- unique article identifier
         :return: data of article
         '''
         article_by_id = self.models.get_by_id(article_id)
         serializer = jsonify(article_by_id)
         response = serializer, 200
         return response

     def get_by_name(self, name: str) -> tuple:
         '''
         Handles a get request to get article by title
         :param name: - article title
         :return: data of article
         '''
         article_by_name = self.models.get_by_name(name)
         serializer = jsonify(article_by_name)
         response = serializer, 200
         return response

     def post(self, new_article_data: dict) -> tuple:
         '''
         Creating new article
         :param new_article_data: dict from request body
         :return: - unique article identifier
         '''
         new_article = self. __to_article_create_dataclass(new_article_data)
         article_id = self.models.create(new_article)
         serializer = jsonify(article_id)
         response = serializer, 200
         return response

     def put(self, update_article_data: dict) -> tuple:
         '''
         Updating article
         :param update_article_data:  dict from request body
         :return: - successful update response
         '''
         update_article = self.__to_article_update_dataclass(update_article_data)
         self.models.update(update_article)
         response = "Ok", 200
         return response

     def __to_article_create_dataclass(self, data_article: dict) -> Article:
         '''
         Convert dict from request body to article dataclass
         :param data_article: dict from request body
         :return: instance of article dataclass
         '''
         article = Article(name=data_article['name'],
                           text=data_article['text'],
                           date=data_article['date'],
                           user_id=data_article['author_id'])
         return article

     def __to_article_update_dataclass(self, data_article: dict) -> ArticleUpdate:
         '''
         Convert dict from request body to article dataclass
         :param data_article:  dict from request body
         :return: instance of article dataclass
         '''
         article = ArticleUpdate(article_id=data_article.get('article_id'),
                                 name=data_article.get('name'),
                                 text=data_article.get('text'),
                                 date=data_article.get('date'),
                                 user_id=data_article['author_id'])
         return article

     def delete(self) -> tuple:
         '''
         Removing data from all articles.
         :return: - successful delete response
         '''
         self.models.delete()
         response = "Ok", 200
         return response

     def delete_by_name(self, name: str) -> tuple:
         '''
         Article removing by title
         :param name: - article title
         :return: - successful delete response
         '''
         self.models.delete_by_name(name)
         response = "Ok", 200
         return response

     def delete_by_id(self, article_id: str) -> tuple:
         '''
         Article removing by id
         :param article_id: - unique article identifier
         :return: - successful delete response
         '''
         self.models.delete_by_id(article_id)
         response = "Ok", 200
         return response


class LikeController:
     def __init__(self):
         self.models = LikeModels()

     def get(self) -> tuple:
         '''
         Getting data from all likes.
         :return: data from all likes
         '''
         all_likes = self.models.get()
         serializer = jsonify(all_likes )
         response = serializer, 200
         return response

     def get_by_id(self, article_id: str) -> tuple:
         '''
         Handles a get request to get like  by articles identifier
         :param article_id: - unique article identifier
         :return: data of likes
         '''
         like_by_id = self.models.get_by_id(article_id)
         serializer = jsonify(like_by_id)
         response = serializer, 200
         return response

     def get_by_name(self, name: str) -> tuple:
         '''
         Handles a get request to get like  by articles title
         :param name: - article title
         :return: data of likes
         '''
         like_by_name = self.models.get_by_name(name)
         serializer = jsonify(like_by_name)
         response = serializer, 200
         return response

     def post(self, new_like_data: dict) -> tuple:
         '''
         Creating new like
         :param new_like_data: dict from request body
         :return: - successful creating response
         '''
         new_like = self.__to_like_dataclass(new_like_data)
         self.models.create(new_like)
         response = "Ok", 200
         return response

     def __to_like_dataclass(self, data_like: dict) -> Like:
         '''
         Convert dict from request body to like dataclass
         :param data_like: dict from request body
         :return: instance of like dataclass
         '''
         like = Like(article_id=data_like['article_id'],
                     user_id=data_like['user_id'])
         return like

     def delete(self) -> tuple:
         '''
         Removing data from all likes.
         :return: - successful delete response
         '''
         self.models.delete()
         response = "Ok", 200
         return response

     def delete_by_name(self, title: str, name: str) -> tuple:
         '''
         Like removing by article title and user nic name
         :param title: - article title
         :param name: - unique user nic name
         :return: - successful delete response
         '''
         data_like = LikeGetById(article_name=title,
                                 user_name=name)
         self.models.delete_by_name(data_like)
         response = "Ok", 200
         return response

     def delete_by_id(self, article_id: str, user_id: str) -> tuple:
         '''
         Like removing by article id and user id
         :param article_id: - unique article identifier
         :param user_id: - - unique user identifier
         :return: - successful delete response
         '''
         data_like = Like(article_id=article_id,
                          user_id=user_id)
         self.models.delete_by_id(data_like)
         response = "Ok", 200
         return response


class CommentController:
    def __init__(self):
        self.models = CommentModels()

    def get(self) -> tuple:
        '''
        Getting data from all comments.
        :return: data from all articles comments and code response
        '''
        all_comments = self.models.get()
        serializer = jsonify(all_comments)
        response = serializer, 200
        return response

    def get_by_id(self, article_id: str) -> tuple:
        '''
        Handles a get request to get comment  by articles identifier
        :param article_id: unique article identifier
        :return: data of comment and code response
        '''
        comment_by_id = self.models.get_by_id(article_id)
        serializer = jsonify(comment_by_id)
        response = serializer, 200
        return response

    def get_by_name(self, name: str) -> tuple:
        '''
        Handles a get request to get comment  by articles title
        :param name: article title
        :return: data of comment and code response
        '''
        comment_by_name = self.models.get_by_name(name)
        serializer = jsonify(comment_by_name)
        response = serializer, 200
        return response

    def post(self, new_comment_data: dict) -> tuple:
        '''
        Creating new comment
        :param new_comment_data: dict from request body
        :return: - successful creating response
        '''
        new_comment = self.__to_comment_dataclass(new_comment_data)
        self.models.create(new_comment)
        response = "Ok", 200
        return response

    def put(self, update_comment_data: dict) -> tuple:
        '''
        Comment updating
        :param update_comment_data: dict from request body
        :return: - successful updating response
        '''
        update_comment = self.__to_comment_dataclass(update_comment_data)
        self.models.update(update_comment)
        response = "Ok", 200
        return response

    def __to_comment_dataclass(self, data_comment: dict) -> CommentCreate:
        '''
        Convert dict from request body to comment dataclass
        :param data_comment: dict from request body
        :return: instance of comment dataclass
        '''
        comment = CommentCreate(article_id=data_comment['article_id'],
                                user_id=data_comment['user_id'],
                                comment=data_comment['comment'])
        return comment

    def __to_comment_id_dataclass(self, article_id: str, author_id: str) -> CommentById:
        '''
        Convert article_id, author_id to comment dataclass
        :param article_id: unique article identifier
        :param author_id: unique user identifier
        :return: instance of comment dataclass
        '''
        comment_by_id = CommentById(article_id=article_id,
                                    user_id=author_id)
        return comment_by_id

    def __to_comment_name_dataclass(self, title: str, name: str) -> CommentByName:
        '''
        Convert article title, user nic name to comment dataclass
        :param title: article title
        :param name: unique user nic name
        :return: instance of comment dataclass
        '''
        comment_by_name = CommentByName(article_name=title,
                                        user_name=name)
        return comment_by_name

    def delete(self) -> tuple:
        '''
        Removing data from all comments.
        :return: - successful delete response
        '''
        self.models.delete()
        response = "Ok", 200
        return response

    def delete_by_name(self, title: str, name: str) -> tuple:
        '''
        Comment removing by article title and user nic name
        :param title: article title
        :param name: unique user nic name
        :return: - successful delete response
        '''
        delete_comment = self.__to_comment_name_dataclass(title, name)
        self.models.delete_by_name(delete_comment)
        response = "Ok", 200
        return response

    def delete_by_id(self, article_id: str, author_id: str) -> tuple:
        '''
        Comment removing by article_id and author_id
        :param article_id: unique article identifier
        :param author_id: unique user identifier
        :return: - successful delete response
        '''
        delete_comment = self.__to_comment_id_dataclass(article_id, author_id)
        self.models.delete_by_id(delete_comment)
        response = "Ok", 200
        return response



