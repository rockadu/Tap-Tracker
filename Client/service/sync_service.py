import schedule
import json
import requests
import time

from repository.db_repository import get_activitys, update_synced_activity

MAX_RETRIES = 5

with open("config.json", "r") as file:
    data = json.load(file)  

server_url = data["server"]

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
            response = requests.post(server_url, json=data_batch)
            if response.status_code == 200:
                # Marcar os registros do lote como sincronizados
                update_synced_activity(record_ids)
                print(f"Successfully synced {len(record_ids)} records.")
                retries = 0  # Resetar contagem de retentativas após sucesso
            else:
                print(f"Failed to sync records. Status code: {response.status_code}")
                retries += 1
                if retries > MAX_RETRIES:
                    print("Max retries reached. Sync will resume later.")
                    return
                time.sleep(5 * (2 ** retries))  # Backoff exponencial
        except requests.ConnectionError:
            print("Connection error. Sync will resume later.")
            return

schedule.every(1).minutes.do(sync_activity_data)

def run_sync():
    while True:
        schedule.run_pending()
        time.sleep(1)