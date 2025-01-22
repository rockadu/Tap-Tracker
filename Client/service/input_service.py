from repository.input_activity_repository import increment 
from pynput import mouse, keyboard

def on_click(x, y, button, pressed):
    if pressed:
        increment('MouseClicks')

def on_scroll(x, y, dx, dy):
        increment("MouseScroll")

def on_press(key):
    try:
        increment('KeyPresses')
    except Exception as e:
        print(f"Erro ao salvar entrada: {e}")


def start_moviment_listners():
    mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_press)
    
    mouse_listener.start()
    keyboard_listener.start()