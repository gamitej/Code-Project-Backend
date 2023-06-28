# ======= Flask imports ==========
from flask_cors import CORS
from flask import Flask, jsonify
from flask_compress import Compress
# ======= Libs imports ==========
import sqlite3
import atexit
# ======= Routes imports ========
from auth.auth import auth
from explore.explore import explore
from profile.profile import profile

app = Flask(__name__)
CORS(app)
compress = Compress()
compress.init_app(app)

# =============== Databse Connection Started ===============

def connect_to_db():
    print("💻 Connecting to database ...\n")
    connection = sqlite3.connect('data.db')
    print("✅ Connected to database 💻 ...")
    return connection

connection = connect_to_db()
cursor = connection.cursor()

# =============== Databse Connection Closed ===============

def cleanup():
    print("❌ Closed database connection...")
    connection.close()

# cursor.execute(query)
# connection.commit()
# connection.close()

# ============== ROUTES START ======================

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(explore, url_prefix='/')
app.register_blueprint(profile, url_prefix='/profile')

@app.errorhandler(404)
def error(e):
    return jsonify({"msg": "Wrong Route"}), 404

# ============== ROUTES END ========================

atexit.register(cleanup)

if __name__ == '__main__':
    app.run(debug=True, port=5000,)

