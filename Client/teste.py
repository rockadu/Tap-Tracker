import sqlite3

# Conectar ao banco de dados
db_connection = sqlite3.connect("tap_tracker.db")

# Criar um cursor para executar comandos SQL
cursor = db_connection.cursor()

# Exibir registros da tabela ActivityCount
print("Registros da tabela ActivityCount:")
##cursor.execute("UPDATE ActivityCount SET Sync = 0")
cursor.execute("SELECT * FROM ActivityCount")
activity_count_rows = cursor.fetchall()
for row in activity_count_rows:
    print(row)

# print("\nRegistros da tabela WindowActivity:")
# # Exibir registros da tabela WindowActivity
# cursor.execute("SELECT * FROM WindowActivity")
# window_activity_rows = cursor.fetchall()
# for row in window_activity_rows:
#     print(row)

##Fechar a conexão
db_connection.close()