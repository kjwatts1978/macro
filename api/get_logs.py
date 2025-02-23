# api/get_logs.py
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection
conn = psycopg2.connect(
    dbname="your_db",
    user="your_user",
    password="your_password",
    host="your_host"
)

@app.route('/api/get_logs', methods=['GET'])
def get_logs():
    username = request.args.get('username')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'logs': []})
    user_id = user[0]
    cursor.execute("SELECT timestamp, description, protein, carbs, fat, calories FROM logs WHERE user_id = %s ORDER BY timestamp DESC", (user_id,))
    logs = cursor.fetchall()
    cursor.close()
    logs_list = [{'timestamp': log[0], 'description': log[1], 'protein': log[2], 'carbs': log[3], 'fat': log[4], 'calories': log[5]} for log in logs]
    return jsonify({'logs': logs_list})

if __name__ == '__main__':
    app.run()