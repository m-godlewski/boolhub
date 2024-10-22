# Changelog

## 0.14.1
- Major bugfixes in installation script.

## 0.14.0
- Whole installation process now can be performed usign install.sh script.
- Requirements files has been updated due to vulnerabilities issues.

## 0.13.0
- Storing battery/filter (health) data info InfluxDB.
- Properties and methods moved from AirData subclasses to AirData class itself.
- Limit float values in dataclasses.
- Change in configuration to make archivist script work.
- Logging improved.

## 0.12.1
- Replaced CLI command with miio library in communication with Xiaomi Purifier.
- Logs from miio library has been limited.
- Replaced unused TimedRotatingFileHandler with basic stream/file logging configuration.

## 0.12.0
- Created brainstone module that contains each script that previously was running on crontab.

## 0.11.1
- Moved scripts configuration from config.py file to constance in django-admin.

## 0.11.0
- Added lighting module. Basic panel and integration with yeelight bulb implemented.

## 0.10.1
- Fixed error that recognized devices that has no location assigned as unknown devices.

## 0.10.0
- Application-wide settings now can be modified by django-constance in django admin panel.

## 0.9.0
- Fetching weather forecast to InfluxDB implemented.

## 0.8.0
- Landing page reworked to work on tablet device.

## 0.7.0
- Prometheus and Node Exporter added to monitor internal host's statistics

## 0.6.0
- Implemented virtual outside thermometer.

## 0.5.5
- Archivist module implemented.
- Archivist - backup modes added for InfluxDB and PostgreSQL.
- Archivist - recovery mode added for InfluxDB and PostgreSQL.
- Minor changes.

## 0.5.4
- Installation guide and troubleshooting updated.
- Added init-user-db.sh script used for main postgres user database initialization.
- First functionalities implemented in archivist.py script.
- Utils script - docker.py added.

## 0.5.3
- Favicon added.
- Whole database logic moved to database.py script.

## 0.5.2
- Added 'token' field to device model.

## 0.5.1
- Configuration and test unit fixes.

## 0.5.0
- Custom dataset has been implemented in form of Python dataclasses.
- Logs retention changed to daily.
- Minor changes in database module.

## 0.4.5
- Unit test updated, sentry and messenger module methods moved out of class.
- Comments spelling corrected.
- Index page refresh has been set to 60 seconds.
- Some configuration values has been moved to .env file.

## 0.4.4
- Implemented updating of last_time column in unknown_devices table.

## 0.4.3
- Unit tests classes added. Sentry script improved. Script paths logic reworked.

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
- Notification for diagnostic data has been implemented.

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