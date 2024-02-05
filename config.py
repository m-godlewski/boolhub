import os
import logging
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv


#############################
### GENERAL CONFIGURATION ###
#############################

# current system version
VERSION = "0.10.0"

# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# absolute path to log file
LOG_FILE = os.path.join(BASE_DIR, "scripts.log")

# number of logs retention days
LOG_RETENTION_DAYS = 1

# logging configuration
rtfh = TimedRotatingFileHandler(
    filename=LOG_FILE, when="D", interval=1, backupCount=LOG_RETENTION_DAYS, delay=False
)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[rtfh],
)

# loading environmental variables
load_dotenv(os.environ.get("VARIABLES_PATH"))


#############################
### SCRIPTS CONFIGURATION ###
#############################

# databases configuration
DATABASE = {
    "INFLUX": {
        "URL": f"http://{os.environ.get('INFLUXDB_HOST')}:{os.environ.get('INFLUXDB_PORT')}",
        "API_TOKEN": os.environ.get("INFLUXDB_TOKEN"),
        "ORGANIZATION": os.environ.get("INFLUXDB_ORGANIZATION"),
    },
    "POSTGRE": {
        "NAME": os.environ.get("POSTGRE_NAME"),
        "USER": os.environ.get("POSTGRE_USER"),
        "PASSWORD": os.environ.get("POSTGRE_PASSWORD"),
        # until scripts are not running inside docker container
        # host has to be set as 'localhost'
        "HOST": "localhost",
        "PORT": os.environ.get("POSTGRE_PORT"),
    },
    "REDIS": {
        "PASSWORD": os.environ.get("REDIS_PASSWORD"),
        # until scripts are not running inside docker container
        # host has to be set as 'localhost'
        "HOST": "localhost",
        "PORT": os.environ.get("REDIS_PORT"),
        "DB_ID": os.environ.get("REDIS_DB_ID"),
    },
}

# scripts configuration
SCRIPTS = {
    "SENTRY": {
        "NOTIFIES": {
            "UNKNOWN_DEVICE": False,
            "NETWORK_OVERLOAD": False,
            "TEMPERATURE": False,
            "AQI": False,
            "HUMIDITY": False,
            "DIAGNOSTICS": False,
        },
        "THRESHOLDS": {
            "MAX_NUMBER_OF_DEVICES": 10,
            "BATTERY_FILTER_LEVEL": 15,
            "TEMPERATURE": {"UP": 27.0, "BOTTOM": 19.0},
            "AQI": 50,
            "HUMIDITY": {"UP": 85, "BOTTOM": 20},
        },
    },
    "MESSENGER": {"NTFY_SERVER_URL": os.environ.get("NTFY_SERVER_URL")},
    "GATHERER": {
        "VIRTUAL_THERMOMETER": {
            "API_URL": os.environ.get("WEATHER_API_URL"),
            "LATITUDE": os.environ.get("LATITUDE"),
            "LONGITUDE": os.environ.get("LONGITUDE"),
        }
    },
}

# backups configuration
BACKUPS = {"PATH": os.environ.get("BOOLHUB_BACKUPS_PATH")}
