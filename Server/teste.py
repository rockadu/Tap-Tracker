import sqlite3

# Conectar ao banco de dados
db_connection = sqlite3.connect("tap_tracker_server.db")

# Criar um cursor para executar comandos SQL
cursor = db_connection.cursor()

print("Registros da tabela ActivityCount:")
cursor.execute("SELECT * FROM Users")
activity_count_rows = cursor.fetchall()
for row in activity_count_rows:
    print(row)

print("Registros da tabela ActivityCount:")
cursor.execute("SELECT * FROM ActivityCount")
activity_count_rows = cursor.fetchall()
for row in activity_count_rows:
    print(row)

print("\nRegistros da tabela WindowActivity:")
cursor.execute("SELECT * FROM WindowActivity")
window_activity_rows = cursor.fetchall()
for row in window_activity_rows:
    print(row)

# Fechar a conexão
db_connection.close()
