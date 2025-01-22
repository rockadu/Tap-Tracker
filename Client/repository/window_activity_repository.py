from db_repository import get_db_connection

import datetime

# Insere um evento de nova tela ativa
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

# Recupera os eventos de tela que não estão sincronizados com o servidor
def get_window_activitys(size=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Id, StartTime, LoggedUser, WindowTitle, ProgramName
        FROM WindowActivity
        WHERE Sync = 0
        ORDER BY StartTime ASC
        LIMIT ?
    """, (size))
    records = cursor.fetchall()
    conn.commit()
    conn.close()
    return records

# Atualiza os eventos que já foram sincronizados no servidor
def update_synced_window(record_ids):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executemany("UPDATE WindowActivity SET Sync = 1 WHERE Id = ?", [(record_id,) for record_id in record_ids])
    conn.commit()
    conn.close()