from service.input_service import start_listners
from service.thread_service import ensure_cicle, running
import threading
import time

def start_monitoring():
    start_listners()

if __name__ == "__main__":
    try:
        # Inicie os ouvintes diretamente na main thread

        ensure_thread = threading.Thread(target=ensure_cicle)
        ensure_thread.start()
        start_monitoring()  

        while True:
            time.sleep(1)  # Mantém o programa principal rodando
    except KeyboardInterrupt:
        print("Encerrando threads...")
        running = False  # Sinaliza para as threads encerrarem
        ensure_thread.join()  # Aguarda o término da thread ensure_cicle
        print("Programa encerrado.")