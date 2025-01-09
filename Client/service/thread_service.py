from repository.db_repository import ensure_minute_entry
import os
import time

running = True 
loggedUser = os.getlogin()

def ensure_cicle():
    while running:
        ensure_minute_entry(loggedUser)  # Garante que entradas vazias sejam salvas
        time.sleep(1)