from datetime import datetime
import repository.input_activity_repository as input_repository
from service.sync_service import run_sync
import service.buffer_event_service as buffer
import os
import time

running = True 
loggedUser = os.getlogin()

# Garante a existencia da linha no minuto atual e sincroniza os dados com o servidor a cada segundo
def ensure_cicle():
    last_sync_time = time.time()  # Marca o tempo inicial
    sync_interval = 15  # Intervalo em segundos para sincronização

    while running:
        now = datetime.now()
        
        if now.second == 0:  # Chegou início de um novo minuto
            data = buffer.flush_buffer()
            input_repository.save_buffered_events(data)
            
        # Verifica se passaram 15 segundos desde a última sincronização
        if time.time() - last_sync_time >= sync_interval:
            run_sync()
            last_sync_time = time.time()  # Atualiza o tempo da última sincronização
        
        time.sleep(1) 