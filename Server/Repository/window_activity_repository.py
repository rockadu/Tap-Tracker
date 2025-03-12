from repository.base_repository import get_db_connection
from models.window_model import WindowData
from typing import List

def insert_window_data(window_list: List[WindowData]):
    """Insere uma lista de objetos WindowData no banco de dados"""
    conn = get_db_connection()
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
