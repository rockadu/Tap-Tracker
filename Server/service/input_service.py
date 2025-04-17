import repository.input_activity_repository as repo
from models.activity_model import ActivityData
from typing import List

def insert_activity_data(activity_list: List[ActivityData]):
    repo.insert_activity_data(activity_list)

def get_weekly_activity():
    return repo.get_weekly_activity_count()

def get_active_users():
    return repo.get_active_users_count()

def get_interactions_today_grouped_by_minute():
    data = repo.get_interactions_today_grouped_by_minute_count()

    cumulative = []
    total = 0
    for timestamp, count in data:
        total += count
        cumulative.append({
            "timestamp": timestamp,
            "total": total
        })

    return cumulative

def get_interactions_today_grouped_by_user():
    return repo.get_interactions_today_grouped_by_user_count()