# ============ Flask imports ===========
from flask import Flask, request, jsonify
from flask import Blueprint
# ============== Libs imports ===========
import os
import json
from threading import Thread
# ============ File imports =============
from database.database import data_base
from explore.create_excel import createExcel
from explore.explore_db import ExploreDatabase

explore = Blueprint('explore', __name__)

def explore_routes(connection):
    dataBaseObj = data_base(connection)
    exploreDatabaseObj = ExploreDatabase(connection)

    # reading json
    json_file_path = os.path.join(explore.root_path, 'dummy.json')

    with open(json_file_path) as file:
        data = json.load(file)

    topicsData, selectedTopicData = data.get(
        'topicsData'), data.get('selectedTopicData')

    @explore.route('/topics', methods=["GET"])
    def getTopic():
        # -- /topic?id=<string:id>
        try:
            id = request.args.get('id')
            # -- return response
            return jsonify({"data": topicsData, "error": True}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": False}), 500


    @explore.route('/selected_topic', methods=["GET"])
    def getSelectedTopicData():
        # -- /selected_topic/topic?id=<string:id>&topic=<string:topic>
        try:
            id, topic = request.args.get('id'), request.args.get('topic')
            # -- return response
            return jsonify({"data": selectedTopicData, "error": False}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500
    
    @explore.route('/add-questions', methods=["POST"])
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
            res = exploreDatabaseObj.addQuestionToTable(url,topic,question,level,platform)
            if res:
                return jsonify({"message": res, "error": False}), 400
            # -- update to excel
            thread = Thread(target=createExcel)
            thread.start()
            return jsonify({"message": "Question Added Successfully", "error": True}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500

    return explore