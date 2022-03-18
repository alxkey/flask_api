from marshmallow import Schema, fields, validate


class SchemaAddArticle(Schema):
    name = fields.Str(validate=validate.Length(min=4), required=True)
    text = fields.Str(validate=validate.Length(min=4), required=True)
    date = fields.DateTime(format='%d.%m.%Y', required=True)
    author_id = fields.Number(as_string=True, required=True)


class SchemaUpdateArticle(Schema):
    id = fields.Number(as_string=True, required=True)
    name = fields.Str(validate=validate.Length(min=4))
    text = fields.Str(validate=validate.Length(min=4))
    date = fields.DateTime(format='%d.%m.%Y')


class SchemaAddLike(Schema):
    article_id = fields.Number(as_string=True, required=True)
    author_id = fields.Number(as_string=True, required=True)


class SchemaAddComment(Schema):
    article_id = fields.Number(as_string=True, required=True)
    author_id = fields.Number(as_string=True, required=True)
    comment = fields.Str(validate=validate.Length(min=4), required=True)


