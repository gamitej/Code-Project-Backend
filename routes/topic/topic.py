# Flask imports
from flask import Flask, request, jsonify
from flask import Blueprint
# Libs imports
import os
import json
from threading import Thread
# File import
from routes.database.database import data_base
from routes.explore.create_excel import createExcel
from routes.explore.explore_db import ExploreDatabase

topic = Blueprint('topic', __name__)

def topic_routes(connection,limiter):
    dataBaseObj = data_base(connection)
    
    @topic.route('/markQue', methods=["POST"])
    @limiter.limit("10/minute")
    def markQueDown():
        # -- /markQue?id=<string:id>&topic_id=<string:topic>
        try:
            req = request.get_json()
            user_id,topic_id =req['id'],req['topic_id']
            # date_time  = request.args.get('date_time')
            query =  F"INSERT INTO user_questions (user_id, topic_id) VALUES ('{topic_id}','{user_id}')"
            dataBaseObj.execute_query(query)
            return jsonify({"data": "Que marked as done", "error": False}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured'}), 500

    return topic