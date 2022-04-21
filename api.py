"""
@Author Marco A. Gallegos
@Date   2020/10/09
@Update 2020/10/09
@Description
    Main Api file
"""
from config.config import APP_CONFIG
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import (get_jwt_identity, jwt_required, JWTManager)
import os
from config.config import APP_CONFIG
import requests
from repository.mongorepository.main_repository import store_comic

# controladores
import controllers

# TODO use app_name from .env
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Setup the Flask-JWT-Extended extension
# TODO use .env secret
app.config["JWT_SECRET_KEY"] = "super-secret-XD"  # Change this!
jwt = JWTManager(app)


# se pueden agregar rutas nativas de flask que regresen json
@app.route("/login", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    json = jsonify(logged_in_as=current_user)
    print(json, type(json))
    return json, 200


@app.route("/addToLayaway", methods=["POST"])
@jwt_required()
def store_comics():
    data = request.get_json(force=True)
    comics = None
    try:
        comics = data["comics"]
    except Exception as e:
        print(e)
    if comics == {} or comics is None or comics == "":
        return {"error": "comics is required"}, 400
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    authorizathion_header = request.headers.get("Authorization")

    comic_list = comics.split(",")

    commics_to_add = []

    # print(comic_list)

    for comic in comic_list:
        # print(comic)
        # validate comics to store
        comic_request = requests.get(
            f"{APP_CONFIG['API_GET_COMICS']}/comicexist",
            headers={"Authorization": authorizathion_header},
            params={"idcomic": comic}
        )
        if comic_request.status_code != 200:
            return {"message": f"the comic {comic} does not exist"}, 404
        else:
            commics_to_add.append({
                "user_id": current_user["_id"],
                "idcomic": comic,
                "comic": comic_request.json()
            })

    for comic in commics_to_add:
        stored = store_comic(comic)
        if not stored:
            return {"message": f"problems storing {comic['idcomic']} "}, 400
        comic["_id"] = str(comic["_id"])
    return jsonify(commics_to_add), 200


# Setup the flask restful api
api = Api(app)

# rutas resource de flask restful
api.add_resource(controllers.HelloWorld, '/')


if __name__ == '__main__':
    host = os.getenv('APP_HOST') if os.getenv('APP_HOST') else '0.0.0.0'
    port = 5002
    app.run(debug=True, host=host, port=port)
