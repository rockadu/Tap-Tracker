import sqlite3
from datetime import datetime
import json
import os

with open("config.json", "r") as file:
    data = json.load(file)  

db_name = data["db_name"]

def get_db_connection():
    """Retorna uma nova conexão com o banco de dados."""
    return sqlite3.connect(db_name)

def setup_database():
    """Cria o banco de dados se ele não existir."""
    with get_db_connection() as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ActivityCount (
                Timestamp TEXT PRIMARY KEY,
                MouseClicks INTEGER DEFAULT 0,
                KeyPresses INTEGER DEFAULT 0,
                MouseScroll INTEGER DEFAULT 0
            )
        """)
        db_connection.commit()
        db_connection.close()

def ensure_minute_entry():
    """Garante que haja uma entrada no banco para o minuto atual, mesmo que não tenha interação."""
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO ActivityCount (Timestamp, MouseClicks, KeyPresses, MouseScroll)
        VALUES (?, 0, 0, 0)
        ON CONFLICT(Timestamp) DO NOTHING
    """, (timestamp,))

    conn.commit()
    conn.close()
    
def save_entry(type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        UPDATE ActivityCount
        SET {type} = {type} + 1
        WHERE Timestamp = ?
    """.format(type=type)

    with get_db_connection() as db_connection:
        cursor = db_connection.cursor()
        cursor.execute(query, (timestamp,))
        
    conn.commit()
    conn.close()
    
if os.path.exists(db_name) == False:
    setup_database()