from repository.db_repository import ensure_minute_entry
import time

running = True 

def ensure_cicle():
    while running:
        ensure_minute_entry()  # Garante que entradas vazias sejam salvas
        time.sleep(1)