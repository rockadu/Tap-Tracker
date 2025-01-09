from repository.db_repository import save_entry 
from pynput import mouse, keyboard

def on_click(x, y, button, pressed):
    if pressed:
        save_entry('MouseClicks')

def on_scroll(x, y, dx, dy):
    save_entry("MouseScroll")

def on_press(key):
    save_entry('KeyPresses')


def start_listners():
    with mouse.Listener(on_click=on_click, on_scroll=on_scroll) as mouse_listener, \
            keyboard.Listener(on_press=on_press) as keyboard_listener:
        mouse_listener.join()
        keyboard_listener.join()