# api/add_log.py
from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Database connection
conn = psycopg2.connect(
    dbname="your_db",
    user="your_user",
    password="your_password",
    host="your_host"
)

@app.route('/api/add_log', methods=['POST'])
def add_log():
    data = request.get_json()
    username = data.get('username')
    description = data.get('description')
    protein = data.get('protein')
    carbs = data.get('carbs')
    fat = data.get('fat')
    calories = data.get('calories')
    
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})
    user_id = user[0]
    
    timestamp = datetime.now()
    cursor.execute(
        "INSERT INTO logs (user_id, timestamp, description, protein, carbs, fat, calories) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (user_id, timestamp, description, protein, carbs, fat, calories)
    )
    conn.commit()
    cursor.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run()