from service.keyboard_service import start_keyboard_listener
from service.mouse_service import start_mouse_listener
from service.thread_service import ensure_cicle, running
import threading
import time

def start_listeners():
    """Inicia os ouvintes de mouse e teclado."""
    start_mouse_listener()
    start_keyboard_listener()

if __name__ == "__main__":
    try:
        listeners_thread = threading.Thread(target=start_listeners)
        listeners_thread.start()

        ensure_thread = threading.Thread(target=ensure_cicle)
        ensure_thread.start()

        while True:
            time.sleep(1)  # Mantém o programa principal rodando
    except KeyboardInterrupt:
        print("Encerrando threads...")
        running = False  # Sinaliza para as threads encerrarem
        ensure_thread.join()  # Aguarda o término da thread ensure_cicle
        print("Programa encerrado.")