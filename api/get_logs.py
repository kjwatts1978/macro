# api/get_logs.py
from . import create_app, get_db_connection
from flask import request, jsonify

app = create_app()

@app.route('/api/get_logs', methods=['GET'])
def get_logs():
    conn = get_db_connection()
    try:
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
    finally:
        conn.close()

if __name__ == '__main__':
    app.run()