import json

def get_app_config():
    with open("config.json", "r") as file:
        data = json.load(file)  
    return data