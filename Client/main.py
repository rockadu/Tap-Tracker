from service.input_service import start_moviment_listners
from service.thread_service import ensure_cicle, running
from service.window_service import start_window_monitor
import threading
import time

def start_monitoring():
    start_window_monitor()
    start_moviment_listners()

if __name__ == "__main__":
    try:
        # Inicie os ouvintes diretamente na main thread

        ensure_thread = threading.Thread(target=ensure_cicle)
        ensure_thread.start()
        start_monitoring()

        while running:
            time.sleep(1)  # Mantém o programa principal rodando
    except KeyboardInterrupt:
        print("Encerrando threads...")
        running = False  # Sinaliza para as threads encerrarem
        ensure_thread.join()  # Aguarda o término da thread ensure_cicle
        print("Programa encerrado.")