import os
import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv


#############################
### GENERAL CONFIGURATION ###
#############################

# current system version
VERSION = "0.4.5"

# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# absolute path to log file
LOG_FILE = os.path.join(BASE_DIR, "scripts.log")

# size of single log file (in megabytes)
LOG_FILE_SIZE = 50

# logging configuration
rfh = RotatingFileHandler(
    filename=LOG_FILE, mode="a", maxBytes=LOG_FILE_SIZE * 1024 * 1024
)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[rfh],
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
        "HOST": os.environ.get("POSTGRE_HOST"),
        "PORT": os.environ.get("POSTGRE_PORT"),
    },
}

# devices configuration
# TOOD - move this to database field
DEVICES = {"TOKENS": {"69:90:c1:7f:e2:0c": os.environ.get("XIAOMI_PURIFIER_TOKEN")}}

# scripts configuration
SCRIPTS = {
    "SENTRY": {
        "NOTIFIES": {
            "UNKNOWN_DEVICE": False,
            "NETWORK_OVERLOAD": True,
            "TEMPERATURE": True,
            "AQI": True,
            "HUMIDITY": True,
            "DIAGNOSTICS": True,
        },
        "THRESHOLDS": {
            "MAX_NUMBER_OF_DEVICES": 10,
            "BATTERY_FILTER_LEVEL": 15,
            "TEMPERATURE": {"UP": 28.0, "BOTTOM": 18.0},
            "AQI": 50,
            "HUMIDITY": {"UP": 85, "BOTTOM": 20},
        },
    },
    "MESSENGER": {"NTFY_SERVER_URL": os.environ.get("NTFY_SERVER_URL")},
}
