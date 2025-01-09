from repository.db_repository import save_entry 
from pynput import keyboard

def on_press(key):
    try:
        print(f'Tecla pressionada: {key}')
        save_entry('KeyPresses')
    except Exception as e:
        print(f"Erro ao salvar entrada: {e}")

def start_keyboard_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()