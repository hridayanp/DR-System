# For now we simulate a store using in-memory or simple logic (in prod use DB)
from typing import Dict
user_db_configs: Dict[int, dict] = {}

def store_user_db_config(user_id: int, config: dict):
    user_db_configs[user_id] = config

def get_user_db_config(user_id: int) -> dict:
    return user_db_configs.get(user_id)


