from repository.db_repository import save_entry 
from pynput import keyboard

def on_press(key):
    save_entry('KeyPresses')

def start_keyboard_listener():
        with keyboard.Listener(on_press=on_press) as keyboard_listener:
            keyboard_listener.join()