from flask import Blueprint, request, jsonify
import sqlite3
import json
from models import db
from utils.gps import get_distance

hospital_bp = Blueprint('hospital', __name__)

def get_hospitals():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hospital')
    hospitals = cursor.fetchall()
    conn.close()
    return hospitals

def get_doctors(hospital_id, speciality=None):
    conn = db.get_connection()
    cursor = conn.cursor()
    if speciality:
        cursor.execute('SELECT * FROM doctor WHERE hospital_id = ? AND specialization = ?', (hospital_id, speciality))
    else:
        cursor.execute('SELECT * FROM doctor WHERE hospital_id = ?', (hospital_id,))
    doctors = cursor.fetchall()
    conn.close()
    return doctors

@hospital_bp.route('/nearby', methods=['GET'])
def nearby_hospitals():
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))
    speciality = request.args.get('speciality')
    emergency = request.args.get('emergency', 'false').lower() == 'true'

    hospitals = get_hospitals()
    nearby = []

    for h in hospitals:
        if h[3] and h[4]:  # latitude, longitude
            dist = get_distance(lat, lng, h[3], h[4])
            if dist <= 50:  # within 50km
                if emergency and not h[7]:  # emergency
                    continue
                doctors = get_doctors(h[0], speciality)  # h[0] is id
                nearby.append({
                    'id': h[0],
                    'name': h[1],
                    'address': h[2],
                    'contact': h[5],
                    'timings': h[6],
                    'distance': dist,
                    'departments': json.loads(h[8]) if h[8] else [],
                    'doctors': [{'name': d[1], 'specialization': d[2]} for d in doctors]
                })

    nearby.sort(key=lambda x: x['distance'])
    return jsonify(nearby[:10]), 200

@hospital_bp.route('/emergency', methods=['GET'])
def emergency_hospitals():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hospital WHERE emergency = 1')
    hospitals = cursor.fetchall()
    conn.close()

    return jsonify([{
        'name': h[1],
        'address': h[2],
        'contact': h[5],
        'latitude': h[3],
        'longitude': h[4]
    } for h in hospitals]), 200