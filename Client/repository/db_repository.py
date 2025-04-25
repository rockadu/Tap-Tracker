import sqlite3
import json
import os

with open("config.json", "r") as file:
    data = json.load(file)  

db_name = data["db_name"]

# Cria um conexão com o banco de dados local
def get_db_connection():
    conn = sqlite3.connect(db_name,
                           timeout=30, # espera até 30s por lock
                           check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;") # modo Write-Ahead Logging
    conn.execute("PRAGMA busy_timeout = 5000;") # até 5s antes de falhar
    return conn

# Prepara a base de dados se ainda não existe
def setup_database():
    with get_db_connection() as db_connection:
        cursor = db_connection.cursor()
        
        print("Criando tabela ActivityCount")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ActivityCount (
                Timestamp TEXT PRIMARY KEY,
                LoggedUser TEXT,
                MouseClicks INTEGER DEFAULT 0,
                KeyPresses INTEGER DEFAULT 0,
                MouseScroll INTEGER DEFAULT 0,
                Sync INTEGER DEFAULT 0
            )
        """)
        print("Tabela ActivityCount criada")

        print("Criando tabela WindowActivity")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS WindowActivity (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                LoggedUser TEXT NOT NULL,
                StartTime TEXT NOT NULL,
                WindowTitle TEXT NOT NULL,
                ProgramName TEXT NOT NULL,
                ActivityDuration INTEGER DEFAULT 0,
                Sync INTEGER DEFAULT 0
            )
        """)
        print("Tabela WindowActivity criada")

        db_connection.commit()

# Cria a base de dados se ainda não existe
if os.path.exists(db_name) == False:
    print("Base não encontrada, criando...")
    setup_database()