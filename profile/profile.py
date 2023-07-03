# ========= Flask import ===========
from flask import Flask, request, jsonify
from flask import Blueprint
from profile.profile_data import ProfileDataDropdown
from database.database import data_base

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
    dbObj = data_base(connection)

    @profile.route('/dropdown-data', methods=["GET"])
    def getDropDownData():
        try:
            dropDownData = profileDropDownObj.getProfileDropDown()
            return jsonify({"data": dropDownData, "error": False}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500
        

    @profile.route('/table_data',methods=["GET"])
    def getTableData():
        try:
            id = request.args.get('id')
            query = f"SELECT q.url, q.topic,q.question,q.level, q.platform,CASE WHEN uq.user_id IS NOT NULL THEN TRUE ELSE FALSE END AS completed FROM questions q LEFT JOIN user_questions uq ON q.question_id = uq.question_id AND uq.user_id = '{id}' WHERE( uq.user_id = '{id}' OR uq.user_id IS NULL ) ORDER BY topic asc"
            data = dbObj.selectQuery(query,False)
            data = profileDropDownObj.getQueTableData(data)
            print(data)
            return jsonify({"data": data, "error": False}), 200
        except Exception as e:
            print(e)
            return jsonify({"data": 'Error Occured', "error": True}), 500
        
    return profile 