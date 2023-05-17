import os
import logging
from dotenv import load_dotenv


###
### GENERAL CONFIGURATION
###

# current system version
VERSION = "0.2.0"

# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# absolute path to log file
LOG_FILE = os.path.join(BASE_DIR, "scripts.log")

# logging configuration
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")

# loading envinronmental variables
load_dotenv(os.path.join(BASE_DIR, ".env"))

###
### SCRIPTS CONFIGURATION
###

# databases configuration
DATABASE = {
    "INFLUX" : {
        "URL": "http://localhost:8086",
        "API_TOKEN": os.environ.get("INFLUXDB_TOKEN"),
        "ORGANIZATION": os.environ.get("INFLUXDB_ORGANIZATION")
    },
    "SQLITE": {
        "PATH": os.path.join(BASE_DIR, "central", "db.sqlite3")
    }
}

# devices configuration
DEVICES = {
    "TOKENS": {
        "69:90:c1:7f:e2:0c": os.environ.get("XIAOMI_PURIFIER_TOKEN")
    }
}

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
            "HUMIDITY": {
                "UP": 85,
                "BOTTOM": 20
            }
        }
    },
    "MESSENGER": {
        "NTFY_SERVER_URL": "https://ntfy.sh/boolhub"
    }
}
