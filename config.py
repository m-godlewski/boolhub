import os
import json
from dotenv import load_dotenv


# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# loading envinronmental variables
load_dotenv(os.path.join(BASE_DIR, ".env"))

# database configuration
DB = {
    "INFLUX" : {
        "URL": "http://localhost:8086",
        "API_TOKEN": os.environ.get("INFLUXDB_TOKEN"),
        "ORGANIZATION": "boolhub"
    },
    "SQLITE": {
        "PATH": os.path.join(BASE_DIR, "central", "db.sqlite3")
    }
}

# devices configuration
DEVICES = {
    "TOKENS":{
        "Mi Air Purifier 3H": os.environ.get("XIAOMI_PURIFIER_TOKEN")
    }
}

# loading known devices mac addresses from json
with open(os.path.join(BASE_DIR, "known_devices.json")) as known_devices_file:
    DEVICES["KNOWN_LIST"] = json.load(known_devices_file)
