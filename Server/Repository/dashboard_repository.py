import repository.base_repository as base_repo

def get_user_list_resume():
    conn = base_repo.get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                ac.LoggedUser AS Usuario,

                -- Interações do dia
                SUM(CASE WHEN DATE(ac.Timestamp) = DATE('now', 'localtime') THEN ac.MouseClicks + ac.KeyPresses + ac.MouseScroll ELSE 0 END) AS TotalDia,

                -- Interações da última hora
                SUM(CASE WHEN ac.Timestamp >= DATETIME('now', '-1 hour') THEN ac.MouseClicks + ac.KeyPresses + ac.MouseScroll ELSE 0 END) AS UltimaHora,

                -- Interações dos últimos 15 minutos
                SUM(CASE WHEN ac.Timestamp >= DATETIME('now', '-15 minutes') THEN ac.MouseClicks + ac.KeyPresses + ac.MouseScroll ELSE 0 END) AS Ultimos15Min,

                -- Está ativo nos últimos 2 minutos?
                CASE 
                    WHEN MAX(CASE WHEN ac.Timestamp >= DATETIME('now', '-2 minutes') THEN ac.Timestamp ELSE NULL END) IS NOT NULL THEN 'Sim'
                    ELSE 'Não'
                END AS EstaAtivo,

                -- Último programa usado (via WindowActivity)
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
                    """)

        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Erro ao obter contagem de atividades da semana: {e}")
        conn.close()