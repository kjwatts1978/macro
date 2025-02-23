from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Get the database connection string from environment variables
conn_string = os.getenv('POSTGRES_URL')

@app.route('/api/status', methods=['GET'])
def status():
    try:
        # Attempt to connect and execute a simple query
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return jsonify({'connected': True})
    except Exception as e:
        return jsonify({'connected': False, 'error': str(e)})

if __name__ == '__main__':
    app.run()