from repository.db_repository import ensure_minute_entry
from service.sync_service import sync_activity_data
import os
import time

running = True 
loggedUser = os.getlogin()

def ensure_cicle():
    while running:
        ensure_minute_entry(loggedUser)
        sync_activity_data()
        time.sleep(1)