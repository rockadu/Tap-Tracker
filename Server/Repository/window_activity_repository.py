import repository.base_repository as base_repo
from datetime import datetime, timedelta
from models.window_model import WindowData
from typing import List

def insert_window_data(window_list: List[WindowData]):
    """Insere uma lista de objetos WindowData no banco de dados"""
    conn = base_repo.get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.executemany("""
            INSERT INTO WindowActivity (StartTime, LoggedUser, WindowTitle, ProgramName, ActivityDuration)
            VALUES (?, ?, ?, ?, ?)
        """, [(window.timestamp, window.logged_user, window.window_title, window.application_name, window.activity_duration)
              for window in window_list])

        conn.commit()
        print(f"{len(window_list)} registros de janela inseridos/atualizados com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados de janela: {e}")
    finally:
        conn.close()

def get_weekly_window_activity_count():
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    conn = base_repo.get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT COUNT(DISTINCT ProgramName) 
            FROM WindowActivity 
            WHERE StartTime >= ?
        """, (start_of_week.strftime('%Y-%m-%d %H:%M:%S'),))

        count = cursor.fetchone()[0]
        conn.close()

        return count
    except Exception as e:
        print(f"Erro ao obter contagem de janelas da semana: {e}")


def get_top_program_week():
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    conn = base_repo.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ProgramName, SUM(ActivityDuration) as TotalDuration
        FROM WindowActivity
        WHERE StartTime >= ?
        GROUP BY ProgramName
        ORDER BY TotalDuration DESC
        LIMIT 1
    """, (start_of_week.strftime('%Y-%m-%d %H:%M:%S'),))

    row = cursor.fetchone()
    conn.close()

    return row

def get_activity_by_program_week_count():
    now = datetime.now()
    start_datetime = now.replace(hour=0, minute=0, second=0, microsecond=0)
    conn = base_repo.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ProgramName, SUM(ActivityDuration)
        FROM WindowActivity
        WHERE StartTime >= ?
        GROUP BY ProgramName
        ORDER BY SUM(ActivityDuration) DESC
    """, (start_datetime.strftime('%Y-%m-%d %H:%M:%S'),))
    
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_total_duration_by_user():
    now = datetime.now()
    start_datetime = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT LoggedUser, SUM(ActivityDuration)
        FROM WindowActivity
        WHERE StartTime >= ?
        GROUP BY LoggedUser
    """, (start_datetime.strftime('%Y-%m-%d %H:%M:%S'),))
    result = cursor.fetchall()
    conn.close()
    return dict(result)