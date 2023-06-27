from flask import Flask, request, jsonify
from flask import Blueprint
from auth.auth_db import getUsers, insertUser, checkUserValidity
from db import selectQuery

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["POST"])
def login():
    try:
        req = request.get_json()
        userId, passwd = req["username"], req["password"]
        # === check if user & passwd match
        res = checkUserValidity(userId, passwd)
        if res == False:
            return jsonify({"msg": "Username/Password is incorrect"}), 400
        else:
            # === return user_id
            query = f"select user_id from users where username =  '{userId}'"
            res = selectQuery(query, True)
            if res is not None:
                return jsonify({"msg": "success", "id": res[0]}), 200
            else:
                return jsonify({"msg": "Something went wrong"}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Something went wrong"}), 500


@auth.route('/signup', methods=["POST"])
def singup():
    try:
        req = request.get_json()
        username, passwd = req["username"], req["password"]
        # === check if user
        res = getUsers(username)
        if res:
            return jsonify({"msg": "Username already exists"}), 400
        else:
            res = insertUser(username, str(passwd))
            return jsonify({"msg": "success"}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Something went wrong"}), 500


@auth.route('/pin-api', methods=["GET"])
def pins():
    return jsonify({"data": {
        "content": [
            {
                "name": "1",
                "id": "1",
                "username": "anupam",
                "created": "01-22-2023",
                "hashtags": "",
                "caption": "q",
            },
            {
                "name": "2",
                "id": "2",
                "username": "amitej",
                "created": "01-22-2023",
                "hashtags": "",
                "caption": "q",
            },
            {
                "name": "3",
                "id": "3",
                "username": "adarsh",
                "created": "01-22-2023",
                "hashtags": "",
                "caption": "q",
            },
            {
                "name": "4",
                "id": "4",
                "username": "pagal",
                "created": "01-22-2023",
                "hashtags": "",
                "caption": "q",
            },
        ],
    }}), 200
