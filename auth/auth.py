# ======= Flask imports ===========
from flask import Blueprint, request, jsonify
# ======= File imports ===========
from database.database import data_base
from auth.auth_db import AuthDb

auth = Blueprint('auth', __name__)

def auth_routes(connection):
    dataBaseObj = data_base(connection)
    authDbObj = AuthDb(connection)

    @auth.route('/login', methods=["POST"])
    def login():
        try:
            req = request.get_json()
            username, passwd = req["username"], req["password"]
            # === check if user & passwd match
            res = authDbObj.checkUserValidity(username, passwd)
            if not res:
                return jsonify({"message": "Username/Password is incorrect","error":False}), 400
            else:
                # === return user_id
                query = f"select user_id from users where username =  '{username}'"
                res = dataBaseObj.selectQuery(query, True)
                if res is not None:
                    return jsonify({"message": "Login Successfull", "id": res[0],"error":False}), 200
                else:
                    return jsonify({"message": "Something went wrong","error":True}), 400
        except Exception as e:
            print(e)
            return jsonify({"message": "Something went wrong","error":False}), 500

    @auth.route('/signup', methods=["POST"])
    def signup():
        try:
            req = request.get_json()
            username, passwd = req["username"], req["password"]
            # === check if user
            res = authDbObj.getUsers(username)
            if res:
                return jsonify({"message": "Username already exists","error":True}), 400
            else:
                res = authDbObj.insertUser(username, str(passwd))
                return jsonify({"message": "Sign-up Successfully","error":False}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Something went wrong","error":True}), 500

    return auth

