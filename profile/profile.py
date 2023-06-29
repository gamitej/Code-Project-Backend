# ========= Flask import ===========
from flask import Flask, request, jsonify
from flask import Blueprint
from profile.profile_data import ProfileDataDropdown

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

def profile_routes(connection):

    profileDropDownObj = ProfileDataDropdown()

    @profile.route('/dropdown-data', methods=["GET"])
    def getDropDownData():
        try:
            dropDownData = profileDropDownObj.getProfileDropDown()
            return jsonify({"data": dropDownData, "error": False}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500
        
    return profile 