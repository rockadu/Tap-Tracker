from repository.db_repository import get_db_connection

from datetime import datetime

# Insere um evento de nova tela ativa
def insert_window_activity(logged_user, window_title, program_name):
    print(f"Inserindo novo regitro de janela ativa para {window_title}")
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO WindowActivity (LoggedUser, StartTime, WindowTitle, ProgramName)
        VALUES (?, ?, ?, ?)
    """, (logged_user, timestamp, window_title, program_name))
    conn.commit()
    conn.close()
    print(f"Evento de janela ativa realizada {window_title}")

# Recupera os eventos de tela que não estão sincronizados com o servidor
def get_window_activitys(size=10):
    print("Recuperando registros de janelas não sincronizados")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Id, StartTime, LoggedUser, WindowTitle, ProgramName
        FROM WindowActivity
        WHERE Sync = 0
        ORDER BY StartTime ASC
        LIMIT ?
    """, (size,))
    records = cursor.fetchall()
    conn.commit()
    conn.close()
    print("Registros de janelas recuperados")
    return records

def get_last_window_activity():
    print("Recuperando último registro de janela")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Id, StartTime
        FROM WindowActivity
        ORDER BY StartTime DESC
        LIMIT 1
    """)
    record = cursor.fetchone()
    conn.commit()
    conn.close()
    print("Último registro de janela recuperado")
    return record

def update_duration_lastWindow_activity(duration, record_id):
    print(f"Atualizando duração: {duration} segundos para o registro {record_id}")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE WindowActivity SET ActivityDuration = ? WHERE Id = ?", (int(duration), int(record_id)))
    conn.commit()
    conn.close()
    print("Duração do último registro de janela atualizado")

# Atualiza os eventos que já foram sincronizados no servidor
def update_synced_window(record_ids):
    print("Atualizando registro de janelas para sincronizado")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executemany("UPDATE WindowActivity SET Sync = 1 WHERE Id = ?", [(record_id,) for record_id in record_ids])
    conn.commit()
    conn.close()
    print("Registros de janelas atualizados")