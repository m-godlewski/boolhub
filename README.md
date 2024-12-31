# BoolHub [![version](https://img.shields.io/badge/version-0.21.0-blue.svg)](https://semver.org)

Intelligent house hub.

## Technology Stack

- Central (Django 4.1)
- Brainstone (Python 3.8)
- PostgreSQL 15.3.0
- InfluxDB 2.2.0
- Portainer 2.9.3

## Prerequisites

Server machine should match minimum requirements of running Ubuntu Server 20.04.6 LTS.  
Solution has been developed and tested on Fujitsu Q920 8GB/256GB i5-4590T.

## Installation

Make installation script executable by running:

```
$ sudo chmod +x install.sh
```

Run installation script:

```
$ sudo ./install.sh
```

## Currently supported devices for data gathering

- Mi Temperature & Humidity Monitor 2
- Xiaomi Mi Purifier 3H
