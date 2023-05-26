import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv


###
### GENERAL CONFIGURATION
###

# current system version
VERSION = "0.3.0"

# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# absolute path to log file
LOG_FILE = os.path.join(BASE_DIR, "scripts.log")

# size of single log file (in megabytes)
LOG_FILE_SIZE = 50

# logging configuration
rfh = logging.handlers.RotatingFileHandler(
    filename=LOG_FILE, mode="a", maxBytes=LOG_FILE_SIZE * 1024 * 1024
)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[rfh],
)

# loading envinronmental variables
load_dotenv(os.environ.get("VARIABLES_PATH"))


###
### SCRIPTS CONFIGURATION
###

# databases configuration
DATABASE = {
    "INFLUX": {
        "URL": "http://localhost:8086",
        "API_TOKEN": os.environ.get("INFLUXDB_TOKEN"),
        "ORGANIZATION": os.environ.get("INFLUXDB_ORGANIZATION"),
    },
    "SQLITE": {"PATH": os.path.join(BASE_DIR, "central", "db.sqlite3")},
}

# devices configuration
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
            "TEMPERATURE": 19.0,
            "AQI": 50,
            "HUMIDITY": {"UP": 85, "BOTTOM": 20},
        },
    },
    "MESSENGER": {"NTFY_SERVER_URL": "https://ntfy.sh/boolhub"},
}
