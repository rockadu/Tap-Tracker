import datetime
import os
import threading
from repository.input_activity_repository import increment 
import service.buffer_event_service as buffer
from pynput import mouse, keyboard

logged_user = os.getlogin()

# Aciona o sensor de click
def on_click(x, y, button, pressed):
    try:
        if pressed:
            buffer.add_input_event('MouseClicks', logged_user)
    except Exception as e:
        print(f"Erro ao salvar entrada: {e}")

# Lock dedicado para checar/atualizar o último scroll
_scroll_lock = threading.Lock()
# Guarda datetime do último scroll por usuário
_last_scroll_time: dict[str, datetime.datetime] = {}

# Aciona o sensor de scroll
def on_scroll(x, y, dx, dy):
    try:
        now = datetime.datetime.now()
        with _scroll_lock:
            prev = _last_scroll_time.get(logged_user)
            # se nunca scrollou ou já passou >= 1s, aceita; senão ignora
            if prev is None or (now - prev).seconds >= 1:
                buffer.add_input_event("MouseScroll", logged_user)
                _last_scroll_time[logged_user] = now
            # else: descarta scroll extra no mesmo segundo
    except Exception as e:
        print(f"Erro ao salvar entrada: {e}")
        
# Aciona o sensor de tecla
def on_press(key):
    try:
        buffer.add_input_event('KeyPresses', logged_user)
    except Exception as e:
        print(f"Erro ao salvar entrada: {e}")

# Inicia os sensores de input
def start_moviment_listners():
    print("Iniciando sensores de input")
    mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_press)
    
    mouse_listener.start()
    keyboard_listener.start()
    print("Sensores de input iniciado")