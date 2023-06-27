# flask import
from flask import Flask, request, jsonify
from flask import Blueprint
# libs
import os
import json
from threading import Thread
# function import
from explore.explore_db import addQuestionToTable, delRemark, updateRemark
from explore.create_excel import createExcel

explore = Blueprint('explore', __name__)


# reading json
json_file_path = os.path.join(explore.root_path, 'dummy.json')

with open(json_file_path) as file:
    data = json.load(file)
topicsData, selectedTopicData = data.get(
    'topicsData'), data.get('selectedTopicData')


@explore.route('/add-questions', methods=["POST"])
def addQuestions():
    try:
        req = request.get_json()
        # -- req body
        url, level, question, topic, platform = req["url"], req[
            "level"], req["question"], req["topic"], req["platform"]
        # -- inserting to table
        res = addQuestionToTable(
            topic, question, url, level, platform)
        if res:
            # -- return response
            return jsonify({"message": res, "error": False}), 400
        # -- update to excel
        thread = Thread(target=createExcel)
        thread.start()
        # -- return response
        return jsonify({"message": "Question Added Successfully", "error": True}), 200
    except Exception as e:
        print(e)
        return jsonify({"data": 'Error Occured'}), 500


@explore.route('/topics', methods=["GET"])
def getTopic():
    # -- /topic?id=<string:id>
    try:
        id = request.args.get('id')
        # -- return response
        return jsonify({"data": topicsData, "error": True}), 200
    except Exception as e:
        print(e)
        return jsonify({"data": 'Error Occured'}), 500


@explore.route('/selected_topic', methods=["GET"])
def getSelectedTopicData():
    # -- /selected_topic/topic?id=<string:id>&topic=<string:topic>
    try:
        id, topic = request.args.get('id'), request.args.get('topic')
        # -- return response
        return jsonify({"data": selectedTopicData, "error": True}), 200
    except Exception as e:
        print(e)
        return jsonify({"data": 'Error Occured'}), 500


@explore.route('/remarks/<string:id>', methods=["DELETE", "PUT"])
def putDeleteRemark(id):
    try:
        if request.method == "DELETE":
            res = delRemark(id)
            if res:
                return jsonify({"message": "Remark Deleted Already"}), 200
            return jsonify({"message": "Remark Deleted Successfully"}), 200
        if request.method == "PUT":
            req = request.get_json()
            study, remarkText, day = req["study"], req["remark"], req["day"]
            res = updateRemark(study, remarkText, day, id)
            if res:
                return jsonify({"message": res}), 500
            return jsonify({"message": "Remark Updated successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"data": 'Error Occured'}), 500
