# =============== Flask import ==============
from flask import Flask, request, jsonify
from flask import Blueprint
from flask_jwt_extended import jwt_required
# ========= Datatbase file import ============
from routes.profile.profile_data import ProfileDataDropdown
from routes.database.database import data_base
from routes.profile.profile_db import ProfileDatabase

profile = Blueprint('profile', __name__)

def profile_routes(connection,limiter):

    profileDropDownObj = ProfileDataDropdown()
    dbObj = data_base(connection)
    profileDbObj = ProfileDatabase(connection)

    # ======================== DROPDOWN DATA ============================

    @profile.route('/dropdown-data', methods=["GET"])
    @limiter.limit("30/minute")
    @jwt_required()
    def getDropDownData():
        try:
            dropDownData = profileDropDownObj.getProfileDropDown()
            return jsonify({"data": dropDownData, "error": False}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500
        
    # ========================= TABLE DATA ===============================

    @profile.route('/table_data',methods=["GET"])
    @limiter.limit("30/minute")
    @jwt_required()
    def getTableData():
        try:
            id = request.args.get('id')
            query = f"SELECT q.url, q.topic,q.question,q.level, q.platform,CASE WHEN uq.user_id IS NOT NULL THEN TRUE ELSE FALSE END AS completed FROM questions q LEFT JOIN user_questions uq ON q.question_id = uq.question_id AND uq.user_id = '{id}' WHERE( uq.user_id = '{id}' OR uq.user_id IS NULL ) ORDER BY q.topic asc"
            data = dbObj.selectQuery(query,False)
            data = profileDropDownObj.getQueTableData(data)
            return jsonify({"data": data, "error": False}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500
        
    # ========================= USER STATUS DATA ===============================

    @profile.route('/user_status',methods=["GET"])
    @limiter.limit("30/minute")
    @jwt_required()
    def getUserStatus():
        try:
            id = request.args.get('id')
            query = "select level, count(question_id) AS totalQue from questions GROUP BY level;"
            data = dbObj.selectQuery(query,False)
            print(data)
            data = profileDbObj.calcUserStatus(data,id)
            print(data)
            # data = profileDropDownObj.getQueTableData(data)
            return jsonify({"data": {}, "error": False}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500
        
    return profile 