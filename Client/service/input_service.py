import datetime
import threading
import service.buffer_event_service as buffer
from pynput import mouse, keyboard
import crosscutting.user_crosscutting as user

# ——— Callbacks —————

logged_user = user.get_user()

def on_click(x, y, button, pressed):
    if pressed:
        try:
            buffer.add_input_event('MouseClicks', logged_user)
        except Exception as e:
            print(f"Erro ao salvar click: {e}")

_scroll_lock = threading.Lock()
_last_scroll_time: dict[str, datetime.datetime] = {}

def on_scroll(x, y, dx, dy):
    now = datetime.datetime.now()
    with _scroll_lock:
        prev = _last_scroll_time.get(logged_user)
        if prev is None or (now - prev).seconds >= 1:
            try:
                buffer.add_input_event('MouseScroll', logged_user)
            except Exception as e:
                print(f"Erro ao salvar scroll: {e}")
            _last_scroll_time[logged_user] = now

pressed_keys: set[keyboard.Key] = set()

def on_press(key):
    if key not in pressed_keys:
        pressed_keys.add(key)
        try:
            buffer.add_input_event('KeyPresses', logged_user)
        except Exception as e:
            print(f"Erro ao salvar keypress: {e}")

def on_release(key):
    pressed_keys.discard(key)

# ——— Startup dos listeners —————

def start_input_listeners():
    print("Iniciando sensores de input")
    k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    m_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
    k_listener.start()
    m_listener.start()
    # mantém o programa rodando
    k_listener.join()
    m_listener.join()