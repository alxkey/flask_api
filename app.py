from flask import Flask

from views import ArticleView, LikeView, CommentView, UserView

app = Flask(__name__)

api_user = UserView.as_view('user_view')
app.add_url_rule('/users', defaults={'user_id': None, 'name': None}, view_func=api_user, methods=['GET', ])
app.add_url_rule('/users/<user_id>', defaults={'name': None}, view_func=api_user, methods=['GET', ])
app.add_url_rule('/users/name/<name>', defaults={'user_id': None}, view_func=api_user, methods=['GET', ])
app.add_url_rule('/users/user',  view_func=api_user, methods=['POST', ])
app.add_url_rule('/users/user',  view_func=api_user, methods=['PUT', ])
app.add_url_rule('/users', defaults={'user_id': None, 'name': None}, view_func=api_user, methods=['DELETE', ])
app.add_url_rule('/users/name/<name>', defaults={'user_id': None}, view_func=api_user, methods=['DELETE', ])
app.add_url_rule('/users/<user_id>', defaults={'name': None}, view_func=api_user, methods=['DELETE', ])

api_articles = ArticleView.as_view('article_view')
app.add_url_rule('/articles', defaults={'article_id': None, 'name': None}, view_func=api_articles, methods=['GET', ])
app.add_url_rule('/articles/<article_id>', defaults={'name': None}, view_func=api_articles, methods=['GET', ])
app.add_url_rule('/articles/name/<name>', defaults={'article_id': None}, view_func=api_articles, methods=['GET', ])
app.add_url_rule('/articles/article',  view_func=api_articles, methods=['POST', ])
app.add_url_rule('/articles/article',  view_func=api_articles, methods=['PUT', ])
app.add_url_rule('/articles', defaults={'article_id': None, 'name': None}, view_func=api_articles, methods=['DELETE', ])
app.add_url_rule('/articles/name/<name>', defaults={'article_id': None}, view_func=api_articles, methods=['DELETE', ])
app.add_url_rule('/articles/<article_id>', defaults={'name': None}, view_func=api_articles, methods=['DELETE', ])

api_like = LikeView.as_view('like_view')
app.add_url_rule('/likes', defaults={'article_id': None, 'name': None}, view_func=api_like, methods=['GET', ])
app.add_url_rule('/likes/<article_id>', defaults={'name': None}, view_func=api_like, methods=['GET', ])
app.add_url_rule('/likes/name/<name>', defaults={'article_id': None}, view_func=api_like, methods=['GET', ])
app.add_url_rule('/likes/like',  view_func=api_like, methods=['POST', ])
app.add_url_rule('/likes', defaults={'article_id': None, 'author_id': None, 'title': None, 'name': None},\
                 view_func=api_like, methods=['DELETE', ])
app.add_url_rule('/likes/name/<title>&<name>', defaults={'article_id': None, 'author_id': None}, view_func=api_like,\
                 methods=['DELETE', ])
app.add_url_rule('/likes/<article_id>&<author_id>', defaults={'title': None, 'name': None}, view_func=api_like,\
                 methods=['DELETE', ])

api_comment = CommentView.as_view('comment_view')
app.add_url_rule('/comments', defaults={'article_id': None, 'name': None}, view_func=api_comment, methods=['GET', ])
app.add_url_rule('/comments/<article_id>', defaults={'name': None}, view_func=api_comment, methods=['GET', ])
app.add_url_rule('/comments/name/<name>', defaults={'article_id': None}, view_func=api_comment, methods=['GET', ])
app.add_url_rule('/comments/comment',  view_func=api_comment, methods=['POST', ])
app.add_url_rule('/comments/comment',  view_func=api_comment, methods=['PUT', ])
app.add_url_rule('/comments', defaults={'article_id': None, 'author_id': None, 'title': None, 'name': None},\
                 view_func=api_comment, methods=['DELETE', ])
app.add_url_rule('/comments/name/<title>&<name>', defaults={'article_id': None, 'author_id': None},\
                 view_func=api_comment, methods=['DELETE', ])
app.add_url_rule('/comments/<article_id>&<author_id>', defaults={'title': None, 'name': None}, view_func=api_comment,\
                 methods=['DELETE', ])

if __name__ == '__main__':
    app.run()



