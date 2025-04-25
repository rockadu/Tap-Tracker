from datetime import datetime, timedelta
import repository.base_repository as base_repo

def get_user_list_resume():
    conn = base_repo.get_db_connection()
    cursor = conn.cursor()
    now = datetime.now()
    
    two_minutes_ago = now - timedelta(minutes=2)
    fifteen_minutes_ago = now - timedelta(minutes=15)
    one_hour_ago = now - timedelta(hours=1)
    
    try:
        cursor.execute("""
            SELECT
                ac.LoggedUser AS Usuario,
                SUM(CASE WHEN DATE(ac.Timestamp) = DATE('now', 'localtime') THEN ac.MouseClicks + ac.KeyPresses + ac.MouseScroll ELSE 0 END) AS TotalDia,
                SUM(CASE WHEN ac.Timestamp >= ? THEN ac.MouseClicks + ac.KeyPresses + ac.MouseScroll ELSE 0 END) AS UltimaHora,
                SUM(CASE WHEN ac.Timestamp >= ? THEN ac.MouseClicks + ac.KeyPresses + ac.MouseScroll ELSE 0 END) AS Ultimos15Min,
                    CASE WHEN MAX(CASE WHEN ac.Timestamp >= ? THEN ac.Timestamp ELSE NULL END) IS NOT NULL THEN 'Sim'
                    ELSE 'Não'
                END AS EstaAtivo,
                (
                    SELECT wa.ProgramName
                    FROM WindowActivity wa
                    WHERE wa.LoggedUser = ac.LoggedUser
                    ORDER BY wa.StartTime DESC
                    LIMIT 1
                ) AS UltimoPrograma
            FROM ActivityCount ac
            GROUP BY ac.LoggedUser
            ORDER BY TotalDia DESC;
                    """, (one_hour_ago.strftime('%Y-%m-%d %H:%M'), fifteen_minutes_ago.strftime('%Y-%m-%d %H:%M'), two_minutes_ago.strftime('%Y-%m-%d %H:%M')))

        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Erro ao obter contagem de atividades da semana: {e}")
        conn.close()