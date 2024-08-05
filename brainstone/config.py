import os
import logging
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv


#############################
### GENERAL CONFIGURATION ###
#############################

# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# path to module variables
VARIABLES_PATH = os.path.join(BASE_DIR, ".env")

# absolute path to log file
LOG_FILE = os.path.join(os.sep, "var", "log", "cron.log")

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
load_dotenv(VARIABLES_PATH)


#############################
### SCRIPTS CONFIGURATION ###
#############################

# databases configuration
DATABASE = {
    "INFLUX": {
        "URL": f"http://localhost:8086",
        "API_TOKEN": os.environ.get("INFLUXDB_TOKEN"),
        "ORGANIZATION": "boolhub",
    },
    "POSTGRE": {
        "NAME": os.environ.get("POSTGRE_NAME"),
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
