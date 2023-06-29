# Libs imports
import atexit
import sqlite3
# Flask imports 
from flask_cors import CORS
from flask import Flask, jsonify
from flask_compress import Compress
# Routes imports 
from auth.auth import auth_routes
from topic.topic import topic_routes
from explore.explore import explore_routes
from profile.profile import profile_routes
# File imports 
from auth.auth_db import AuthDb

app = Flask(__name__)
CORS(app)
compress = Compress()
compress.init_app(app)

# =============== Databse Connection Started ===============

def connect_to_db():
    print("\n💻 Connecting to database ...\n")
    connection = sqlite3.connect('data.db')
    print("✅ Connected to database 💻 ...\n")
    return connection

connection = connect_to_db()
authDbObj = AuthDb(connection)

# =================== ROUTES START =========================

app.register_blueprint(auth_routes(connection), url_prefix='/')
app.register_blueprint(explore_routes(connection), url_prefix='/')
app.register_blueprint(profile_routes(connection), url_prefix='/profile')
app.register_blueprint(topic_routes(connection), url_prefix='/topic')


@app.errorhandler(404)
def error(e):
    return jsonify({"msg": "Wrong Route"}), 404

# =================== ROUTES END ============================

def cleanup():
    print("\n❌ Closed database connection...\n")
    connection.close()

atexit.register(cleanup)

if __name__ == '__main__':
    app.run(debug=True, port=5000,)

