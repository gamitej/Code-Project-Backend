# ============ Flask imports ===========
from flask import Flask, request, jsonify
from flask import Blueprint
from flask_limiter import Limiter
from flask_jwt_extended import jwt_required
from flask_limiter.util import get_remote_address
# ============== Libs imports ===========
import os
import json
from threading import Thread
# ============ File imports =============
from routes.database.database import data_base
from routes.explore.create_excel import createExcel
from routes.explore.explore_db import ExploreDatabase

explore = Blueprint('explore', __name__)

def explore_routes(connection,limiter):
    dataBaseObj = data_base(connection)
    exploreDbObj = ExploreDatabase(connection)

    @explore.route('/topics', methods=["GET"])
    @limiter.limit("30/minute")
    @jwt_required() 
    def getTopic():
        # -- /topic?id=<string:id>
        try:
            id = request.args.get('id')
            data = exploreDbObj.topicsInfoUser(id)
            # -- return response
            return jsonify({"data": data, "error": False}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500


    @explore.route('/selected_topic', methods=["GET"])
    @limiter.limit("30/minute")
    @jwt_required() 
    def getSelectedTopicData():
        # -- /selected_topic/topic?id=<string:id>&topic=<string:topic>
        try:
            id, topic = request.args.get('id'), request.args.get('topic')
            data = exploreDbObj.selectedTopicUserData(id,topic)
            # -- return response
            return jsonify({"data": data, "error": False}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500
        
    @explore.route("/markQuestion",methods=["POST"])
    @limiter.limit("30/minute")
    @jwt_required() 
    def markQuestion():
        try:
            req = request.get_json()
            id,question_id =  req["user_id"],req["question_id"]
            dataBaseObj.execute_query(f"insert into user_questions (user_id, question_id) values ('{id}', '{question_id}')")
            return jsonify({"data": "Mark question as done","error":False}),200            
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500
    
    @explore.route('/add-questions', methods=["POST"])
    @limiter.limit("30/minute")
    @jwt_required() 
    def addQuestions():
        try:
            req = request.get_json()
            # -- req body
            url, level, question, topic, platform = req["url"], req[
                "level"], req["question"], req["topic"], req["platform"]
            # -- check que is already present
            query = f"select url from questions where url = '{url}'"
            resQuery = dataBaseObj.selectQuery(query,True)
            if resQuery != None:
                return jsonify({"message": "Question present already", "error": False}), 200
            # -- inserting to table
            res = exploreDbObj.addQuestionToTable(url,topic,question,level,platform)
            if res:
                return jsonify({"message": res, "error": False}), 400
            # -- update to excel
            # thread = Thread(target=createExcel)
            # thread.start()
            return jsonify({"message": "Question Added Successfully", "error": True}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500

    return explore