# test_db.py
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

POSTGRES_URL = os.getenv('POSTGRES_URL')

try:
    conn = psycopg2.connect(POSTGRES_URL)
    print("Successfully connected to the database!")
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    print("Query executed successfully:", cursor.fetchone())
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")