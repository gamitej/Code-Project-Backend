# flask import
from flask import Flask, request, jsonify
from flask import Blueprint
from profile.comp.data import getProfileDropDown

profile = Blueprint('profile', __name__)

sqlQuery = '''
        CREATE TABLE IF NOT EXISTS user_questions (
            mark_date TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) PRIMARY KEY,
            user_id text,
            question_id text,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (question_id) REFERENCES quentions (question_id),
        )
        '''


@profile.route('/dropdown-data', methods=["GET"])
def getDropDownData():
    try:
        dropDownData = getProfileDropDown()
        return jsonify({"data": dropDownData, "success": True}), 200
    except Exception as e:
        print(e)
        return jsonify({"data": 'Error Occured'}), 500
