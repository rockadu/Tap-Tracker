import sqlite3

# Conectar ao banco de dados
db_connection = sqlite3.connect("tap_tracker.db")

# Criar um cursor para executar comandos SQL
cursor = db_connection.cursor()

# Executar uma query para selecionar todos os registros da tabela
cursor.execute("SELECT * FROM ActivityCount")

# Ler todos os resultados
rows = cursor.fetchall()

# Exibir os resultados
for row in rows:
    print(row)

# Fechar a conexão
db_connection.close()