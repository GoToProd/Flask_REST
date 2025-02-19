from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from config import Config
from models import *
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from schemas import VideoSchema, UserSchema, AuthSchema
from flask_apispec import use_kwargs, marshal_with

app = Flask(__name__)
app.config.from_object(Config)
client = app.test_client()
jwt = JWTManager(app)
docs = FlaskApiSpec()
docs.init_app(app)
app.config.update(
    {
        'APISPEC_SPEC': APISpec(
            title='videoblog',
            version='v1',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_URL': '/swagger',
    }
)


@app.route("/tutorials", methods=['GET', 'POST'])
@jwt_required()
@marshal_with(VideoSchema(many=True))
def handle_tutorials():
    user_id = int(get_jwt_identity())

    if request.method == "GET":
        videos = Video.query.filter(Video.user_id == user_id).all()
        return videos

    elif request.method == "POST":
        new_one = Video(user_id=user_id, **request.json)
        session.add(new_one)
        session.commit()
        return [new_one], 201


@app.route("/tutorials/<int:tutorial_id>", methods=["PUT", "DELETE"])
@jwt_required()
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_or_delete_tutorial(tutorial_id, **kwargs):
    user_id = int(get_jwt_identity())

    if request.method == "PUT":
        item = Video.query.filter_by(id=tutorial_id, user_id=user_id).first()
        if not item:
            return jsonify({"message": "Item not found"}), 404

        params = request.json
        for key, value in params.items():
            setattr(item, key, value)

        session.commit()
        return item

    elif request.method == "DELETE":
        item = Video.query.filter_by(id=tutorial_id, user_id=user_id).first()
        if not item:
            return jsonify({"message": "Item not found"}), 404

        session.delete(item)
        session.commit()
        return jsonify({"message": "Item deleted"}), 204


@app.route("/register", methods=["POST"])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register(**kwargs):
    user = User(**kwargs)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {"access_token": token}, 201


@app.route("/login", methods=["POST"])
@use_kwargs(UserSchema(only=('email', 'password')))
@marshal_with(AuthSchema)
def login(**kwargs):
    print(f"Received login data: {kwargs}")
    user = User.authenticate(**kwargs)
    if not user:
        return {"message": "Invalid email or password"}, 401
    token = user.get_token()
    return {"access_token": token}, 201


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


docs.register(handle_tutorials)
docs.register(update_or_delete_tutorial)
docs.register(register)
docs.register(login)

if __name__ == "__main__":
    app.run(debug=True)
