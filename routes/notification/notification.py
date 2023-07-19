# ======= Flask imports ===========
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
# ======= File imports ===========
from routes.database.database import data_base


noti = Blueprint('noti', __name__)

def notification_routes(connection,limiter):
    dataBaseObj = data_base(connection)

    # =============================== LOGIN ============================

    @noti.route('/notifications', methods=["GET"])
    @limiter.limit("30/minute")
    @jwt_required() 
    def getNotification():
        try:
            return jsonify({"data": [{"id":1,"text":"tree added","seen":False},{"id":2,"text":"dp added","seen":True}],"error":False}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Something went wrong","error":False}), 500
    
    return noti

