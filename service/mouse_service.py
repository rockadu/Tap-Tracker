from repository.db_repository import save_entry 
from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:
        save_entry('MouseClicks')

def start_mouse_listener():
        with mouse.Listener(on_click=on_click) as mouse_listener:
            mouse_listener.join()