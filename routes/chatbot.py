from flask import Blueprint, request, jsonify
import sqlite3
from models import db
from utils.predictor import predict_disease

chatbot_bp = Blueprint('chatbot', __name__)

def get_disease(name):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM disease WHERE name = ?', (name,))
    disease = cursor.fetchone()
    conn.close()
    return disease

def get_health_tips():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT title, content FROM health_tip LIMIT 3')
    tips = cursor.fetchall()
    conn.close()
    return tips

def save_symptom_history(user_id, symptoms, predicted):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO symptom_history (user_id, symptoms, predicted_disease) VALUES (?, ?, ?)',
                   (user_id, symptoms, predicted))
    conn.commit()
    conn.close()

@chatbot_bp.route('/check_symptoms', methods=['POST'])
def check_symptoms():
    data = request.get_json()
    symptoms = data.get('symptoms', '')
    user_id = data.get('user_id')  # For simplicity, pass user_id in request

    # Predict disease
    predicted = predict_disease(symptoms)

    # Save history
    save_symptom_history(user_id, symptoms, predicted)

    # Get disease info
    disease = get_disease(predicted)
    tips = get_health_tips()

    response = {
        'predicted_disease': predicted,
        'advice': disease[4] if disease else 'Consult a doctor',  # when_to_see_doctor
        'tips': [{'title': t[0], 'content': t[1]} for t in tips]
    }

    return jsonify(response), 200

@chatbot_bp.route('/first_aid/<disease_name>', methods=['GET'])
def first_aid(disease_name):
    disease = get_disease(disease_name)
    if not disease:
        return jsonify({'message': 'Disease not found'}), 404

    return jsonify({
        'prevention': disease[3],  # prevention
        'medicine_precautions': disease[5]  # medicine_precautions
    }), 200