from repository.input_activity_repository import insert_activity_data
from models.activity_model import ActivityData
from typing import List

def insert_activities(activity_list: List[ActivityData]):
    insert_activity_data(activity_list)