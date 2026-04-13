import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path='database/healthcare.db'):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        ''')

        # Health Profile
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                age INTEGER,
                gender TEXT,
                medical_history TEXT,
                allergies TEXT,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')

        # Symptom History
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS symptom_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                symptoms TEXT NOT NULL,
                predicted_disease TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')

        # Hospitals
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hospital (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                contact TEXT,
                timings TEXT,
                emergency BOOLEAN DEFAULT 0,
                departments TEXT
            )
        ''')

        # Doctors
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialization TEXT NOT NULL,
                hospital_id INTEGER,
                contact TEXT,
                availability TEXT DEFAULT 'open',
                FOREIGN KEY (hospital_id) REFERENCES hospital (id)
            )
        ''')

        # Diseases
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS disease (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                symptoms TEXT NOT NULL,
                prevention TEXT,
                when_to_see_doctor TEXT,
                medicine_precautions TEXT
            )
        ''')

        # Health Tips
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS health_tip (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT
            )
        ''')

        conn.commit()
        conn.close()

db = Database()