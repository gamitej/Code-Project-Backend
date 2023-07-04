# ======= Flask imports ===========
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
# ======= File imports ===========
from routes.database.database import data_base
from routes.auth.auth_db import AuthDb


auth = Blueprint('auth', __name__)

def auth_routes(connection,limiter):
    dataBaseObj = data_base(connection)
    authDbObj = AuthDb(connection)

    @auth.route('/login', methods=["POST"])
    @limiter.limit("10/minute")
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
                    # jwt access token 
                    access_token = create_access_token(identity=username)
                    data = {"id":res[0],"name":username,"token":access_token}
                    return jsonify({"message": "Login Successfull", "data": data ,"error":False}), 200
                else:
                    return jsonify({"message": "Something went wrong","error":True}), 400
        except Exception as e:
            print(e)
            return jsonify({"message": "Something went wrong","error":False}), 500

    @auth.route('/signup', methods=["POST"])
    @limiter.limit("10/minute")
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

