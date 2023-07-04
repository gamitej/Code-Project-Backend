# ======= Libs imports =========
import atexit
import sqlite3
import logging
from sqlite3 import dbapi2 as sqlite
# ======= Flask imports ======== 
from flask_cors import CORS
from flask import Flask, jsonify,request
from flask_limiter import Limiter
from flask_compress import Compress
from flask_limiter.util import get_remote_address
# ======== Routes imports =======
from routes.auth.auth import auth_routes
from routes.topic.topic import topic_routes
from routes.explore.explore import explore_routes
from routes.profile.profile import profile_routes
# ========= File imports ======== 
from routes.auth.auth_db import AuthDb

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])
CORS(app)
compress = Compress()
compress.init_app(app)

# Create a file handler for logging
file_handler = logging.FileHandler('flask.log')

# Set the log format
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s - IP: %(client_ip)s')
file_handler.setFormatter(formatter)

# Add the file handler to the Flask logger
app.logger.addHandler(file_handler)

# Custom log filter to include client IP address
class ClientIPFilter(logging.Filter):
    def filter(self, record):
        if hasattr(request, 'remote_addr'):
            record.client_ip = request.remote_addr
        else:
            record.client_ip = 'Unknown'
        return True

# Apply the log filter to the Flask logger
app.logger.addFilter(ClientIPFilter())

# =============== Databse Connection Started ===============

def connect_to_db():
    print("\n💻 Connecting to database ...\n")
    connection = sqlite3.connect('data.db')
    print("✅ Connected to database 💻 ...\n")
    # Enable foreign key constraint exceptions
    sqlite.enable_callback_tracebacks(True)
    return connection

connection = connect_to_db()
authDbObj = AuthDb(connection)

# =================== ROUTES START =========================

# Log incoming requests before handling them
@app.before_request
def log_request():
    app.logger.info(f"Incoming request: {request.method} {request.path}")


app.register_blueprint(auth_routes(connection,limiter), url_prefix='/')
app.register_blueprint(explore_routes(connection,limiter), url_prefix='/')
app.register_blueprint(topic_routes(connection,limiter), url_prefix='/topic')
app.register_blueprint(profile_routes(connection,limiter), url_prefix='/profile')


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

