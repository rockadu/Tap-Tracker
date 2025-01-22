from service.input_service import start_moviment_listners
from service.thread_service import ensure_cicle, running
from service.window_service import start_window_monitor
from service.sync_service import run_sync
import threading
import time

def start_monitoring():
    start_window_monitor()
    start_moviment_listners()

if __name__ == "__main__":
    try:
        ensure_thread = threading.Thread(target=ensure_cicle)
        ensure_thread.start()
        
        start_monitoring()

        sync_thread = threading.Thread(target=run_sync)
        sync_thread.start()

        while running:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Encerrando threads...")
        running = False
        ensure_thread.join()
        print("Programa encerrado.")