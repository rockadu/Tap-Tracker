import sqlite3
from datetime import datetime
import json
import os

with open("config.json", "r") as file:
    data = json.load(file)  

db_name = data["db_name"]

def get_db_connection():
    return sqlite3.connect(db_name)

def setup_database():
    with get_db_connection() as db_connection:
        cursor = db_connection.cursor()
    
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                UserId INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE,
                PasswordHash TEXT NOT NULL,
                Email TEXT NOT NULL UNIQUE,
                CreatedAt TEXT DEFAULT CURRENT_TIMESTAMP,
                IsActive INTEGER DEFAULT 1
            )
        """)

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
    db_connection.close()

if os.path.exists(db_name) == False:
    print("Base não encontrada, criando...")
    setup_database()