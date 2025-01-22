from repository.window_activity_repository import insert_window_activity
import win32gui
import win32process
import psutil
import time
import threading
import os

# Busca o titulo da janela ativa
def get_active_window_title():
    window_handle = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window_handle)

# Busca o nome do programa ativo
def get_active_window_program():
    window_handle = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(window_handle)
    process = psutil.Process(pid)
    return process.name()

# Monitora a mudança de janela ativa a cada 1 segundo
def monitor_window_changes():
    last_window_title = None
    while True:
        program_name = get_active_window_program()
        current_window_title = get_active_window_title()
        loggedUser = os.getlogin()
        if current_window_title != last_window_title and current_window_title:
            insert_window_activity(loggedUser, current_window_title, program_name)
            last_window_title = current_window_title
        time.sleep(1)

# Inicia uma thread para monitorar a mudança de janela
def start_window_monitor():
    monitor_thread = threading.Thread(target=monitor_window_changes, daemon=True)
    monitor_thread.start()