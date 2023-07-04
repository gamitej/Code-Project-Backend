# ======= Libs imports =========
import os
import atexit
import sqlite3
import logging
from dotenv import load_dotenv
from sqlite3 import dbapi2 as sqlite
# ======= Flask imports ======== 
from flask_cors import CORS
from flask import Flask, jsonify,request
from flask_limiter import Limiter
from flask_compress import Compress
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
# ======== Routes imports =======
from routes.auth.auth import auth_routes
from routes.topic.topic import topic_routes
from routes.explore.explore import explore_routes
from routes.profile.profile import profile_routes
# ========= File imports ======== 
from routes.auth.auth_db import AuthDb

# .env 
load_dotenv()
secret_key = os.getenv('SECRET_KEY')
port = os.getenv('PORT')

# ======================= App config ========================

app = Flask(__name__)
# logger
app.logger.setLevel(logging.INFO)
# rate limit
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])
CORS(app)
# res compress
compress = Compress()
compress.init_app(app)

# ==================== JWT Configuration =====================
app.config['JWT_SECRET_KEY'] = secret_key  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 120  
jwt = JWTManager(app)

# ==================== Logging ==============================

file_handler = logging.FileHandler('flask.log')

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s - IP: %(client_ip)s')
file_handler.setFormatter(formatter)

app.logger.addHandler(file_handler)

# custom log filter to include client IP address
class ClientIPFilter(logging.Filter):
    def filter(self, record):
        if hasattr(request, 'remote_addr'):
            record.client_ip = request.remote_addr
        else:
            record.client_ip = 'Unknown'
        return True

app.logger.addFilter(ClientIPFilter())

# =============== Databse Connection ===============

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
    app.run(debug=True, port=port,)

