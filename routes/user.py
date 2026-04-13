from flask import Blueprint, request, jsonify
import sqlite3
from models import db

user_bp = Blueprint('user', __name__)

def get_health_profile(user_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM health_profile WHERE user_id = ?', (user_id,))
    profile = cursor.fetchone()
    conn.close()
    return profile

def update_health_profile(user_id, data):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM health_profile WHERE user_id = ?', (user_id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute('''
            UPDATE health_profile SET age = ?, gender = ?, medical_history = ?, allergies = ?
            WHERE user_id = ?
        ''', (data.get('age'), data.get('gender'), data.get('medical_history'), data.get('allergies'), user_id))
    else:
        cursor.execute('''
            INSERT INTO health_profile (user_id, age, gender, medical_history, allergies)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, data.get('age'), data.get('gender'), data.get('medical_history'), data.get('allergies')))

    conn.commit()
    conn.close()

def get_symptom_history(user_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT symptoms, predicted_disease, timestamp FROM symptom_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10', (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    data = request.get_json() or {}
    user_id = data.get('user_id')  # For simplicity

    if request.method == 'POST':
        update_health_profile(user_id, data)
        return jsonify({'message': 'Profile updated'}), 200

    profile = get_health_profile(user_id)
    if not profile:
        return jsonify({}), 200

    return jsonify({
        'age': profile[2],
        'gender': profile[3],
        'medical_history': profile[4],
        'allergies': profile[5]
    }), 200

@user_bp.route('/history', methods=['GET'])
def history():
    user_id = request.args.get('user_id')
    histories = get_symptom_history(user_id)
    return jsonify([{
        'symptoms': h[0],
        'predicted_disease': h[1],
        'timestamp': h[2]
    } for h in histories]), 200