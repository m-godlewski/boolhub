import os
import logging

from dotenv import load_dotenv


# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# path to module variables
VARIABLES_PATH = os.path.join(BASE_DIR, ".env")

# absolute path to log file
LOG_FILE = os.path.join(os.sep, "var", "log", "cron.log")

# logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE)],
)

# imported libraries logging configuration
logging.getLogger("miio").setLevel(logging.WARNING)

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
}
