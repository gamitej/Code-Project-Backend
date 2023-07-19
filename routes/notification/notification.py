# ======= Flask imports ===========
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
# ======= File imports ===========
from routes.database.database import data_base
from routes.notification.notification_db import NotificationDb

noti = Blueprint('noti', __name__)

def notification_routes(connection,limiter):
    dataBaseObj = data_base(connection)
    notiObj = NotificationDb(connection)

    # =============================== GET NOTIFICATION ============================

    @noti.route('/notifications', methods=["GET"])
    @limiter.limit("30/minute")
    @jwt_required() 
    def getNotification():
        try:
            id = request.args.get('id')
            data = notiObj.getNotificationOfUser(id)
            return jsonify({"data":data,"error":False}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Something went wrong","error":True}), 500
    
    return noti

