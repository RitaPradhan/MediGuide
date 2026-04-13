from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes.auth import auth_bp
from routes.chatbot import chatbot_bp
from routes.hospital import hospital_bp
from routes.disease import disease_bp
from routes.user import user_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
app.register_blueprint(hospital_bp, url_prefix='/hospital')
app.register_blueprint(disease_bp, url_prefix='/disease')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def home():
    return {'message': 'Smart Healthcare System API'}

if __name__ == '__main__':
    app.run(debug=True)
