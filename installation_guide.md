# Installation Guide

## Prerequisites
Server machine should match minimum requirements of running Ubuntu Server 20.04.6 LTS.   
Solution has been developed and tested on Fujitsu Q920 8GB/256GB i5-4590T.

## Step-by-step installation guide
0. Install Ubuntu Server 20.04.6 LTS using [official image](https://releases.ubuntu.com/focal/).
1. Make installation script executable by running:
```
$ sudo chmod +x install.sh
```
2. Run installation script:
```
$ sudo ./install.sh
```
3. Deploy docker containers:
```
$ docker compose up -d
```
4. Set admin password for Grafana.   
To set password for Grafana admin user, just log in for the first time using admin/admin credentials.
After successful login, Grafana will as you for new password.
5. Configure connection between Grafana and Influx.  
