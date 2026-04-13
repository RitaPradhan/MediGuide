from flask import Blueprint, request, jsonify
import sqlite3
from models import db

admin_bp = Blueprint('admin', __name__)

def is_admin(user_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM user WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user and user[0] == 'admin'

@admin_bp.route('/hospitals', methods=['POST'])
def add_hospital():
    data = request.get_json()
    user_id = data.get('user_id')  # For simplicity

    if not is_admin(user_id):
        return jsonify({'message': 'Admin access required'}), 403

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO hospital (name, address, latitude, longitude, contact, timings, emergency, departments)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['address'], data.get('latitude'), data.get('longitude'),
          data.get('contact'), data.get('timings'), data.get('emergency', False), str(data.get('departments', []))))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Hospital added'}), 201

@admin_bp.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.get_json()
    user_id = data.get('user_id')

    if not is_admin(user_id):
        return jsonify({'message': 'Admin access required'}), 403

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO doctor (name, specialization, hospital_id, contact, availability)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['name'], data['specialization'], data.get('hospital_id'),
          data.get('contact'), data.get('availability', 'open')))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Doctor added'}), 201

@admin_bp.route('/diseases', methods=['POST'])
def add_disease():
    data = request.get_json()
    user_id = data.get('user_id')

    if not is_admin(user_id):
        return jsonify({'message': 'Admin access required'}), 403

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO disease (name, symptoms, prevention, when_to_see_doctor, medicine_precautions)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['name'], data['symptoms'], data.get('prevention'),
          data.get('when_to_see_doctor'), data.get('medicine_precautions')))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Disease added'}), 201

@admin_bp.route('/tips', methods=['POST'])
def add_tip():
    data = request.get_json()
    user_id = data.get('user_id')

    if not is_admin(user_id):
        return jsonify({'message': 'Admin access required'}), 403

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO health_tip (title, content, category)
        VALUES (?, ?, ?)
    ''', (data['title'], data['content'], data.get('category')))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Tip added'}), 201