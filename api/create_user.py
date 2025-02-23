# api/create_user.py
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

@app.route('/api/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    if len(username) < 5:
        return jsonify({'success': False, 'message': 'Username must be at least 5 characters'})
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
        conn.commit()
        cursor.close()
        return jsonify({'success': True})
    except psycopg2.IntegrityError:
        conn.rollback()
        cursor.close()
        return jsonify({'success': False, 'message': 'Username already exists'})

if __name__ == '__main__':
    app.run()