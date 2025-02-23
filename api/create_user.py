# api/create_user.py
from . import create_app, get_db_connection
from flask import request, jsonify
import psycopg2

app = create_app()

@app.route('/api/create_user', methods=['POST'])
def create_user():
    conn = get_db_connection()
    try:
        data = request.get_json()
        username = data.get('username')
        if len(username) < 5:
            return jsonify({'success': False, 'message': 'Username must be at least 5 characters'})
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
        conn.commit()
        cursor.close()
        return jsonify({'success': True})
    except psycopg2.IntegrityError:
        conn.rollback()
        cursor.close()
        return jsonify({'success': False, 'message': 'Username already exists'})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run()