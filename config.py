import os
import logging

from dotenv import load_dotenv


# current system version
VERSION = "0.14.0"

# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# path to module variables
VARIABLES_PATH = os.path.join(BASE_DIR, ".env")

# absolute path to log file
LOG_FILE = os.path.join(BASE_DIR, "scripts.log")

# logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE)
    ],
)

# loading environmental variables
load_dotenv(VARIABLES_PATH)

# databases configuration
DATABASE = {
    "INFLUX": {
        "URL": f"http://localhost:8086",
        "API_TOKEN": os.environ.get("INFLUX_TOKEN"),
        "ORGANIZATION": "boolhub",
    },
    "POSTGRE": {
        "NAME": "central",
        "USER": os.environ.get("POSTGRE_USER"),
        "PASSWORD": os.environ.get("POSTGRE_PASSWORD"),
        "HOST": "localhost",
        "PORT": 5432,
    },
    "REDIS": {
        "PASSWORD": os.environ.get("REDIS_PASSWORD"),
        "HOST": "localhost",
        "PORT": 6379,
        "DB_ID": 0,
    },
}

# backups configuration
BACKUPS = {"PATH": os.environ.get("BOOLHUB_BACKUPS_PATH")}
