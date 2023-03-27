import os
import json
import logging
from dotenv import load_dotenv


# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# absolute path to log file
LOG_FILE = os.path.join(BASE_DIR, "scripts.log")

# logging configuration
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")

# loading envinronmental variables
load_dotenv(os.path.join(BASE_DIR, ".env"))

# database configuration
DB = {
    "influx" : {
        "url": "http://localhost:8086",
        "api_token": os.environ.get("INFLUXDB_TOKEN"),
        "organization": "boolhub"
    },
    "sqlite": {
        "path": os.path.join(BASE_DIR, "central", "db.sqlite3")
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
    "MESSENGER": {
        "NOTIFIES": {
            "UNKNOWN_DEVICE": False,
            "TEMPERATURE": True,
            "AQI": True,
            "HUMIDITY": True
        },
        "THRESHOLDS": {
            "TEMPERATURE": 20.0,
            "AQI": 50,
            "HUMIDITY": {
                "UP": 85,
                "BOTTOM": 20
            }
        }
    }
}
