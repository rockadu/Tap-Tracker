from repository.db_repository import get_db_connection
from datetime import datetime, timedelta

# Incrementa em 1 o evento (Mouse/Scroll/Tecla) sensorizado
def increment(type):
    print(f"Inserindo um incremento de input para o evento {type}")
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

# Garante a existencia do minuto mesmo sem haver input
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

# Recupera do banco os eventos de input que ainda não foram sincronizados com o servidor
def get_activitys(size = 100):
    print("Recuperando eventos para sincronizar com servidor")
    cutoff_minute = (datetime.now() - timedelta(minutes=1)).replace(second=0, microsecond=0)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
            SELECT Timestamp, LoggedUser, MouseClicks, KeyPresses, MouseScroll 
            FROM ActivityCount 
            WHERE Sync = 0 
            AND Timestamp < ?
            ORDER BY Timestamp ASC 
            LIMIT ?
        """, (cutoff_minute, size))
    records = cursor.fetchall()
    conn.commit()
    conn.close()
    print("Eventos recuperados")
    return records;

# Atualiza os eventos que foram sincronizados com o servidor
def update_synced_activity(times):
    print(f"Marcando eventos como sincronizados {times}")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executemany("UPDATE ActivityCount SET Sync = 1 WHERE Timestamp = ?", [(time,) for time in times])
    conn.commit()
    conn.close()
    print("Eventos marcados")