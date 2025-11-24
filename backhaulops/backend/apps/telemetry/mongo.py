from pymongo import MongoClient
from django.conf import settings
from functools import lru_cache

@lru_cache(maxsize=1)
def get_mongo_client():
    return MongoClient(settings.MONGO_URI, connect=True)

def get_db():
    client = get_mongo_client
    return client[settings.MONGO_DB_NAME]

def telemetry_col():
    return get_db()["telemetry_events"]

def ensure_indexes():
    col = telemetry_col
    col.create_index([("device_id", 1), ("ts", -1)], name="device_ts")
    col.create_index([("site_slug", 1), ("ts", -1)], name="site_ts")
    col.create_index([("type", 1), ("ts", -1)], name="type_ts")

