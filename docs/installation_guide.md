# Installation Guide

## Prerequisites
Server machine should match minimum requirements of running Ubuntu Server 20.04.6 LTS.

## Step-by-step installation guide
1. Install Ubuntu Server 20.04.6 LTS using [official image](https://releases.ubuntu.com/focal/).
2. Install OpenSSH.
```
sudo apt-get install openssh-client
```
3. Install net-tools.
```
sudo apt-get install net-tools
```
4. Set server timezone. [Guide](https://linuxize.com/post/how-to-set-or-change-timezone-in-linux/)
5. Set static IP. [Guide](https://www.freecodecamp.org/news/setting-a-static-ip-in-ubuntu-linux-ip-address-tutorial/)
6. Clone repository (this Ubuntu Server version has git installed by default).
7. Install docker engine following [official documentation](https://docs.docker.com/engine/install/) and perform [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).
8. Configure environmental variables by creating .env file (base on .env_template).
9. Deploy docker containers.
```
docker compose up -d
```

?. Install Python, PIP and venv.   
?. Create user and password for each application.   
?. Configure "gatherer" script in cronjob.   
?. Configure connection between Grafana and Influx.   
?. Deploy "central" application and create superuser.   
?. Create "House" object, using Django shell.   
