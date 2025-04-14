from repository.window_activity_repository import insert_window_data, get_weekly_window_activity_count, get_top_program_week
from models.window_model import WindowData
from typing import List

def insert_window_activities(window_list: List[WindowData]):
    insert_window_data(window_list)

def get_weekly_window_activity():
    return get_weekly_window_activity_count()

def get_top_program():
    return get_top_program_week()