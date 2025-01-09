from repository.db_repository import insert_window_activity
import win32gui
import win32process
import psutil
import time
import threading

def get_active_window_title():
    window_handle = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window_handle)

def get_active_window_program():
    # Obtém o handle da janela ativa
    window_handle = win32gui.GetForegroundWindow()
    
    # Obtém o PID (Process ID) associado à janela ativa
    _, pid = win32process.GetWindowThreadProcessId(window_handle)
    
    # Obtém o nome do processo usando psutil
    process = psutil.Process(pid)
    return process.name()  # Retorna o nome do programa

def monitor_window_changes():
    last_window_title = None
    while True:
        program_name = get_active_window_program()
        current_window_title = get_active_window_title()
        if current_window_title != last_window_title and current_window_title:
            insert_window_activity(current_window_title, program_name)
            last_window_title = current_window_title
        time.sleep(1)  # Verifica a cada segundo

def start_window_monitor():
    monitor_thread = threading.Thread(target=monitor_window_changes, daemon=True)
    monitor_thread.start()