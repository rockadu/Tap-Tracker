from repository.base_repository import get_db_connection

def get_active_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Username FROM Users WHERE IsActive = 1
    """)

    users = cursor.fetchall()
    conn.close()

    return users