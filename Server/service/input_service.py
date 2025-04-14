from repository.input_activity_repository import insert_activity_data, get_weekly_activity_count, get_active_users_count, get_interactions_today_grouped_by_minute_count
from models.activity_model import ActivityData
from typing import List

def insert_activities(activity_list: List[ActivityData]):
    insert_activity_data(activity_list)

def get_weekly_activity():
    return get_weekly_activity_count()

def get_active_users():
    return get_active_users_count()

def get_interactions_today_grouped_by_minute():
    data = get_interactions_today_grouped_by_minute_count()

    cumulative = []
    total = 0
    for timestamp, count in data:
        total += count
        cumulative.append({
            "timestamp": timestamp,
            "total": total
        })

    return cumulative