import crosscutting.json_crosscutting as json
import os

def get_user():    
    user = json.get_app_config()["user"]

    if (user == "" or user == None):
        return os.getlogin()
    else:
        return user