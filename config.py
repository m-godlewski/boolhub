import os
import json
from dotenv import load_dotenv


# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

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
    "tokens":{
        "purifier": os.environ.get("XIAOMI_PURIFIER_TOKEN")
    }
}

# messanger script configuration
MESSENGER = {
    "notifies": {
        "unknown_devices": True
    }
}
