import os
import logging
import json
import pathlib
from datetime import timedelta

################### Get logger ###################
# set up basic config - logging to console
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s: %(name)s: %(message)s',
                    # datefmt='%m-%d %H:%M',
                    # filename='/temp/myapp.log',
                    # filemode='w'
                    )

# Create console handlers
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_format = logging.Formatter('%(levelname)s: %(asctime)s: %(name)s: %(message)s')
c_handler.setFormatter(c_format)

# Create file handler
log_f_path = os.environ.get("APP_LOG_PATH", os.path.dirname(__file__))
log_f_p = pathlib.Path(log_f_path) / "logs"
log_f_p.mkdir(parents=True, exist_ok=True)
log_f = log_f_p / "app_flask.log"
f_handler = logging.FileHandler(log_f)
f_handler.setLevel(logging.ERROR)
f_format = logging.Formatter('%(levelname)s: %(asctime)s: %(name)s: %(message)s')
f_handler.setFormatter(f_format)

# Add hanlder to root logger.
logging.getLogger('').addHandler(f_handler)

# Create a custom logger
logger = logging.getLogger("DEFAULT API LOGGER")

logger.setLevel(logging.INFO)


class DBConfig(object):
    HOST = os.getenv("DB_HOST", '127.0.0.1')
    USER = os.getenv("DB_USER", "root")
    PASSWORD = os.getenv("DB_PASSWORD")
    SCHEMA = os.getenv("DB_SCHEMA", "MOCKIDP")

