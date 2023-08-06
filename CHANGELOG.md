# Changelog

## 0.4.2
- Database logic moved to separated script.

## 0.4.1
- Saving unknown mac addresses to database added.

## 0.4.0
- All system modules (except scripts) are now dockerized.

## 0.3.1
- Temperature threshold splitted into upper and lower one.

## 0.3.0
- Central database has been migrated to PostgreSQL.

## 0.2.1
- Limited script log size to 50 megabytes.

## 0.2.0
- Notification for diagnostical data has been implemented.

## 0.1.5
- Sentry will now send notification if number of active devices in network exceeds value defined in config.py

## 0.1.4
- Both metrics of "network" gatherer process has been merged into single one process.

## 0.1.3
- Added MiMonitor2 device class to device.py script.

## 0.1.2
- The functions responsible for communication with devices have been moved to the devices.py script (only for purifier device so far).

## 0.1.1
- Minor configuration changes, some variables moved to config.py and .env files.

## 0.1.0
- Initial version.