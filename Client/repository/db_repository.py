import sqlite3
import json
import os

with open("config.json", "r") as file:
    data = json.load(file)  

db_name = data["db_name"]

# Cria um conexão com o banco de dados local
def get_db_connection():
    return sqlite3.connect(db_name)

# Prepara a base de dados se ainda não existe
def setup_database():
    with get_db_connection() as db_connection:
        cursor = db_connection.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ActivityCount (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Timestamp TEXT,
                LoggedUser TEXT,
                MouseClicks INTEGER DEFAULT 0,
                KeyPresses INTEGER DEFAULT 0,
                MouseScroll INTEGER DEFAULT 0,
                Sync INTEGER DEFAULT 0 
            )
        """)

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

        db_connection.commit()

# Cria a base de dados se ainda não existe
if os.path.exists(db_name) == False:
    setup_database()