from repository.base_repository import get_db_connection
from models.activity_model import ActivityData
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