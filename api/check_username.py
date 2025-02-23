# api/check_username.py
from . import create_app, get_db_connection
from flask import request, jsonify

app = create_app()

@app.route('/api/check_username', methods=['GET'])
def check_username():
    conn = get_db_connection()
    try:
        username = request.args.get('username')
        cursor = conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username = %s)", (username,))
        exists = cursor.fetchone()[0]
        cursor.close()
        return jsonify({'exists': exists})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run()