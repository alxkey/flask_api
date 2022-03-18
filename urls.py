

api = ApiView.as_view('apiview')
app.add_url_rule('/articles', defaults={'article_id': None}, view_func=api, methods=['GET', ])
app.add_url_rule('/articles/<article_id>',  view_func=api, methods=['GET', ])
app.add_url_rule('/articles/article',  view_func=api, methods=['POST', ])