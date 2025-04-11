from repository.base_repository import get_db_connection
from models.activity_model import ActivityData
from datetime import datetime, timedelta
from typing import List

def insert_activity_data(activity_list: List[ActivityData]):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.executemany("""
            INSERT INTO ActivityCount (Timestamp, LoggedUser, MouseClicks, KeyPresses, MouseScroll)
            VALUES (?, ?, ?, ?, ?)
        """, [(activity.timestamp, activity.logged_user, activity.mouse_clicks, activity.key_presses, activity.mouse_scroll)
              for activity in activity_list])

        conn.commit()
        print(f"{len(activity_list)} registros inseridos/atualizados com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados de atividade: {e}")
    finally:
        conn.close()

def get_weekly_activity_count():
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM ActivityCount 
            WHERE Timestamp >= ?
        """, (start_of_week.strftime('%Y-%m-%d %H:%M'),))

        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Erro ao obter contagem de atividades da semana: {e}")
        conn.close()
        return 0
    
def get_active_users_count():
    now = datetime.now()
    two_minutes_ago = now - timedelta(minutes=2)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT COUNT(DISTINCT LoggedUser)
            FROM ActivityCount
            WHERE Timestamp >= ?
        """, (two_minutes_ago.strftime('%Y-%m-%d %H:%M'),))

        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Erro ao obter contagem de usuários ativos: {e}")
        conn.close()
        return 0