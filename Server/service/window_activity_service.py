from repository.window_activity_repository import insert_window_data
from models.window_model import WindowData
from typing import List

def insert_window_activities(window_list: List[WindowData]):
    insert_window_data(window_list)