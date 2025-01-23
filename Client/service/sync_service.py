import json
import requests
import time

from repository.input_activity_repository import get_activitys, update_synced_activity
from repository.window_activity_repository import get_window_activitys, update_synced_window

MAX_RETRIES = 5

# Recupera o Json de config
with open("config.json", "r") as file:
    print("Recuperando config json")
    data = json.load(file)  
    print("Config json recuperado")

server_url = data["server"]

# Recupera os dados de mouse não sincronizados e envia para o servidor
def sync_activity_data():
    records = get_activitys()

    if not records:
        return

    data_batch = []
    record_ids = []

    for record in records:
        record_id, timestamp, logged_user, mouse_clicks, key_presses, mouse_scroll = record
        data_batch.append({
            "Timestamp": timestamp,
            "LoggedUser": logged_user,
            "MouseClicks": mouse_clicks,
            "KeyPresses": key_presses,
            "MouseScroll": mouse_scroll
        })
        record_ids.append(record_id)

    try:
        print("Enviando registros de input para o servidor")
        response = requests.post(server_url, json=data_batch)
        if response.status_code == 200:
            update_synced_activity(record_ids)
            print(f"{len(record_ids)} registros sincronizados")
            retries = 0
        else:
            print(f"Falha ao sincronizar dados de mouse. Status code: {response.status_code}")
            retries += 1
            if retries > MAX_RETRIES:
                print("Maximo de tentatias de sincronização de input alcançadas, será tentado posteriormente.")
                return
            time.sleep(5 * (2 ** retries))
    except requests.ConnectionError:
        print("Erro no envio de registros para o servidor")
        return

# Recupera os dados de janela não sincronizados e envia para o servidor
def sync_window_activity_data():
    records = get_window_activitys()

    if not records:
        return

    data_batch = []
    record_ids = []

    for record in records:
        record_id, timestamp, logged_user, window_title, application_name = record
        data_batch.append({
            "Timestamp": timestamp,
            "LoggedUser": logged_user,
            "WindowTitle": window_title,
            "ApplicationName": application_name
        })
        record_ids.append(record_id)

    try:
        print("Enviando registros de janela para o servidor")
        response = requests.post(f"{server_url}/window-activity", json=data_batch)
        if response.status_code == 200:
            update_synced_window(record_ids)
            print(f"{len(record_ids)} registros de janela sincronizados.")
        else:
            print(f"Falha ao enviar os registros de janela para o servidor. Status code: {response.status_code}")
    except requests.ConnectionError:
        print("Falha na conexão, será tentado posteriormente")
        return