from marshmallow import Schema, validate, fields


class VideoSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=250))
    description = fields.String(required=False, validate=validate.Length(min=1, max=250))
    message = fields.String(dump_only=True)


class UserSchema(Schema):
    # id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=20))
    email = fields.String(required=True, validate=validate.Length(min=1, max=30))
    password = fields.String(required=True, validate=validate.Length(min=1, max=18), load_only=True)
    videos = fields.Nested(VideoSchema, many=True, dump_only=True)


class AuthSchema(Schema):
    access_token = fields.String(dump_only=True)
    message = fields.String(dump_only=True)
