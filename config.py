import os
import logging


#############################
### GENERAL CONFIGURATION ###
#############################

# current system version
VERSION = "0.12.1"

# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# absolute path to log file
LOG_FILE = os.path.join(BASE_DIR, "scripts.log")

# number of logs retention days
LOG_RETENTION_DAYS = 1

# logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE)
    ],
)
