# Installation Guide

## Prerequisites
Server machine should match minimum requirements of running Ubuntu Server 20.04.6 LTS.   
Solution has been developed and tested on Fujitsu Q920 8GB/256GB i5-4590T.

## Step-by-step installation guide
1. Install Ubuntu Server 20.04.6 LTS using [official image](https://releases.ubuntu.com/focal/).
2. Run installation script.
```
$ sudo ./install.sh
```
(Optionak)To make installation script executable run:
```
$ sudo chmod +x install.sh
```
3. Configure environmental variables by creating .env file (base on .env_template).
4. Deploy docker containers.
```
$ docker compose up -d
```
5. Create superuser for central panel.
```
$ docker compose run central python manage.py createsuperuser
```
6. Set admin password for Grafana.   
To set password for Grafana admin user, just log in for the first time using admin/admin credentials.
After successful login, Grafana will as you for new password.
7. Set up admin user for InfluxDB.  
Set organization name to boolhub and initial bucket to network.   
Add other data buckets manually.
8. Configure connection between Grafana and Influx.  
9. Configure data gathering
Create venv and install all libraries listed in requirements.txt in scripts directory
```
$ cd scripts
$ python3 -m venv venv
$ source venv venv
$ (venv) pip install -r requirements.txt
```
Set up (sudo user for this moment )cronjob for runing gatherer.py script.
```
$ sudo crontab -e
```
