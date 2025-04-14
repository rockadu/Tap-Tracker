from repository.window_activity_repository import insert_window_data, get_weekly_window_activity_count, get_top_program_week, get_activity_by_program_week_count
from models.window_model import WindowData
from dataclasses import dataclass
from typing import List

@dataclass
class TopProgram:
    program_name: str
    total_duration: int

def insert_window_activities(window_list: List[WindowData]):
    insert_window_data(window_list)

def get_weekly_window_activity():
    return get_weekly_window_activity_count()

def get_top_program():
    row = get_top_program_week()

    if row:
        return {
            "program": row[0],
            "duration_minutes": row[1]
        }
    else:
        return {
            "program": "Nenhum na semana",
            "duration_minutes": 0
    }

def get_activity_by_program_week():
    rows = get_activity_by_program_week_count()

    labels = [row[0] for row in rows]
    data = [round(row[1]/60) for row in rows]

    return {
        "labels": labels,
        "data": data
    }