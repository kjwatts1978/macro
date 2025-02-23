# api/check_username.py
from flask import Flask, request, jsonify
import psycopg2  # Assuming PostgreSQL as the database

app = Flask(__name__)

# Database connection (replace with your credentials)
conn = psycopg2.connect(
    dbname="your_db",
    user="your_user",
    password="your_password",
    host="your_host"
)

@app.route('/api/check_username', methods=['GET'])
def check_username():
    username = request.args.get('username')
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username = %s)", (username,))
    exists = cursor.fetchone()[0]
    cursor.close()
    return jsonify({'exists': exists})

if __name__ == '__main__':
    app.run()