from config.global_constants import USE_AIVEN
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("host"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "database": os.getenv("database")
}

AIVEN_DB_CONFIG = {
    "host": os.getenv("AIVEN_HOST"),
    "user": os.getenv("AIVEN_TOMORROW_ROOT_USERNAME"),
    "password": os.getenv("AIVEN_TOMORROW_ROOT_USER_PASSWORD"),
    "database": os.getenv("AIVEN_DATABASE"),
    "port": os.getenv("AIVEN_PORT"),
}

def get_connection():
    CONFIG = AIVEN_DB_CONFIG if USE_AIVEN else DB_CONFIG
    return mysql.connector.connect(**CONFIG)
