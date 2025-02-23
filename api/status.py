from . import create_app, get_db_connection
from flask import jsonify

app = create_app()

@app.route('/api/status', methods=['GET'])
def status():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return jsonify({'connected': True})
    except Exception as e:
        return jsonify({'connected': False, 'error': str(e)})
