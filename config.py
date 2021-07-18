import os
import logging
import json
from datetime import timedelta


class DBConfig(object):
    HOST = os.getenv("DB_HOST", '127.0.0.1')
    USER = os.getenv("DB_USER", "root")
    PASSWORD = os.getenv("DB_PASSWORD")
    SCHEMA = os.getenv("DB_SCHEMA", "MOCKIDP")

