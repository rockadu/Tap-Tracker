import sqlite3
from datetime import datetime
import json
import os

with open("config.json", "r") as file:
    data = json.load(file)  

db_name = data["db_name"]

def get_db_connection():
    return sqlite3.connect(db_name)

def setup_database():
    with get_db_connection() as db_connection:
        cursor = db_connection.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ActivityCount (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Timestamp TEXT,
                LoggedUser TEXT,
                MouseClicks INTEGER DEFAULT 0,
                KeyPresses INTEGER DEFAULT 0,
                MouseScroll INTEGER DEFAULT 0,
                Sync INTEGER DEFAULT 0 
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS WindowActivity (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                LoggedUser TEXT NOT NULL,
                StartTime TEXT NOT NULL,
                WindowTitle TEXT NOT NULL,
                ProgramName TEXT NOT NULL,
                Sync INTEGER DEFAULT 0 
            )
        """)

        db_connection.commit()

def ensure_minute_entry(loggedUser):
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO ActivityCount (Timestamp, MouseClicks, KeyPresses, MouseScroll, LoggedUser)
        VALUES (?, 0, 0, 0, ?)
        ON CONFLICT(Timestamp) DO NOTHING
    """, (timestamp, loggedUser))

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

def insert_window_activity(logged_user, window_title, program_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO WindowActivity (LoggedUser, StartTime, WindowTitle, ProgramName)
        VALUES (?, ?, ?, ?)
    """, (logged_user, timestamp, window_title, program_name))
    conn.commit()
    conn.close()

def get_activitys(size = 10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
            SELECT Id, Timestamp, LoggedUser, MouseClicks, KeyPresses, MouseScroll 
            FROM ActivityCount 
            WHERE Sync = 0 
            LIMIT ?
        """, (size,))
    records = cursor.fetchall()
    conn.commit()
    conn.close()
    return records;

def update_synced_activity(record_ids):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executemany("UPDATE ActivityCount SET Sync = 1 WHERE Id = ?", [(record_id,) for record_id in record_ids])
    conn.commit()
    conn.close()
    
if os.path.exists(db_name) == False:
    setup_database()