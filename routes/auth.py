from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import sqlite3
from models import db

auth_bp = Blueprint('auth', __name__)

def get_user_by_username(username):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username, email, password):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
                   (username, email, password))
    conn.commit()
    conn.close()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if get_user_by_username(username) or get_user_by_email(email):
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    create_user(username, email, hashed_password)

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = get_user_by_username(username)
    if not user or not check_password_hash(user[3], password):  # password is index 3
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user[0])  # id is index 0
    return jsonify({'access_token': access_token, 'role': user[4]}), 200  # role is index 4

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    # This would need JWT, but for simplicity, assume user_id from somewhere
    return jsonify({'message': 'Profile endpoint'}), 200