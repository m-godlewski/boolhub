import os
import logging
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv


#############################
### GENERAL CONFIGURATION ###
#############################

# current system version
VERSION = "0.12.0"

# absolute path to scripts directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# absolute path to log file
LOG_FILE = os.path.join(BASE_DIR, "scripts.log")

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
