from db_repository import get_db_connection

import datetime

def increment(type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    query = """
        UPDATE ActivityCount
        SET {type} = {type} + 1
        WHERE Timestamp = ?
    """.format(type=type)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (timestamp,))
        
    conn.commit()
    conn.close()

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

def get_activitys(size = 10):
    current_minute = datetime.datetime.now().replace(second=0, microsecond=0)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
            SELECT Id, Timestamp, LoggedUser, MouseClicks, KeyPresses, MouseScroll 
            FROM ActivityCount 
            WHERE Sync = 0 
            AND Timestamp < ?
            ORDER BY Timestamp ASC 
            LIMIT ?
        """, (current_minute, size))
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