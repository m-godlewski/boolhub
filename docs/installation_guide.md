# Installation Guide

## Prerequisites
Server machine should match minimum requirements of running Ubuntu Server 20.04.6 LTS.

## Step-by-step installation guide
1. Install Ubuntu Server 20.04.6 LTS using [official image](https://releases.ubuntu.com/focal/).
2. Install OpenSSH.
```
$ sudo apt-get install openssh-client
```
3. Install net-tools.
```
$ sudo apt-get install net-tools
```
4. Install python pip and venv.
```
$ sudo apt-get install python3-pip
$ sudo apt-get install python3.8-venv
```
5. Configure server timezone. [Guide](https://linuxize.com/post/how-to-set-or-change-timezone-in-linux/)
6. Set static IP. [Guide](https://www.freecodecamp.org/news/setting-a-static-ip-in-ubuntu-linux-ip-address-tutorial/)
7. Clone repository.
8. Install docker engine following [official documentation](https://docs.docker.com/engine/install/) and perform [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).
9. Configure environmental variables by creating .env file (base on .env_template).
10. Deploy docker containers.
```
$ docker compose up -d
```
11. Create superuser for central panel.
```
$ docker compose run central python manage.py createsuperuser
```
12. Set admin password for Grafana.   
To set password for Grafana admin user, just log in for the first time using admin/admin credentials.
After successfull login, Grafana will as you for new password.
13. Set up admin user for InfluxDB.  
Set organization name to boolhub and initial bucket to network.   
Add other data buckets manually.
14. Configure connection between Grafana and Influx.  
15. Configure data gathering
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

### Optional configuration
1. Set up SSH key authorization. [Guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04)
