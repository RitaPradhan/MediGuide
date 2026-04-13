import sqlite3
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
# Import these only if you are actually using them in this file:
# from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database Helper
def get_db_connection():
    # Path based on your 'database' folder
    conn = sqlite3.connect('database/healthcare.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- PAGE ROUTES ---
@app.route('/')
def home():
    return send_from_directory('../Mediguide', 'index.html')

@app.route('/doctors')
def doctor_page():
    return send_from_directory('../Mediguide', 'doctor.html')

@app.route('/hospitals')
def hospital_page():
    return send_from_directory('../Mediguide', 'Hospital.html')

@app.route('/symptoms')
def symptom_page():
    return send_from_directory('../Mediguide', 'symptom checker 2.html')

# --- API ENDPOINTS ---

@app.route('/api/doctors')
def api_doctors():
    conn = get_db_connection()
    doctors = conn.execute('''
        SELECT d.*, h.name as hospital_name
        FROM doctor d
        LEFT JOIN hospital h ON d.hospital_id = h.id
    ''').fetchall()
    conn.close()
    return jsonify([dict(row) for row in doctors])

@app.route('/api/hospitals')
def api_hospitals():
    conn = get_db_connection()
    hospitals = conn.execute('SELECT * FROM hospital').fetchall()
    conn.close()
    return jsonify([dict(row) for row in hospitals])

@app.route('/api/health-tips')
def api_tips():
    conn = get_db_connection()
    tips = conn.execute('SELECT * FROM health_tip ORDER BY RANDOM() LIMIT 3').fetchall()
    conn.close()
    return jsonify([dict(row) for row in tips])

@app.route('/api/predict', methods=['POST'])
def predict_symptoms():
    data = request.json
    user_id = data.get('user_id', 1)
    symptoms = data.get('symptoms')
    
    predicted_disease = "General Fatigue"
    if symptoms and "fever" in symptoms.lower():
        predicted_disease = "Viral Infection"
    elif symptoms and "chest pain" in symptoms.lower():
        predicted_disease = "Cardiovascular Issue"

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO symptom_history (user_id, symptoms, predicted_disease, timestamp)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', (user_id, symptoms, predicted_disease))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "prediction": predicted_disease})

@app.route('/api/history/<int:user_id>')
def get_history(user_id):
    conn = get_db_connection()
    history = conn.execute('''
        SELECT symptoms, predicted_disease, timestamp 
        FROM symptom_history 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in history])

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() 
    email = data.get('email')
    password = data.get('password')
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user WHERE email = ? AND password = ?', 
                        (email, password)).fetchone()
    conn.close()
    
    if user:
        # Returning 'name' matches your schema
        return jsonify({"status": "success", "message": "Welcome!", "user_name": user['name']})
    else:
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401

@app.route('/api/auth/register', methods=['POST'])
def register_with_profile():
    data = request.get_json()
    username = data.get('username')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    age = data.get('age', 0)
    gender = data.get('gender', 'Not Specified')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Ensure 'username' is included to avoid NOT NULL error
        cursor.execute('''
            INSERT INTO user (username, name, email, password, role)
            VALUES (?, ?, ?, ?, 'user')
        ''', (username, name, email, password))
        
        new_user_id = cursor.lastrowid

        # Automatic Health Profile creation
        cursor.execute('''
            INSERT INTO health_profile (user_id, age, gender, medical_history, allergies)
            VALUES (?, ?, ?, 'None', 'None')
        ''', (new_user_id, age, gender))

        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Account created!"})
    
    except sqlite3.IntegrityError as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(debug=True)