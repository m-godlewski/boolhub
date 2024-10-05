#!/bin/bash

echo '##################################################'
echo '###                                            ###'
echo '###                                            ###'
echo '###             BoolHub Installation           ###'
echo '###                                            ###'
echo '###                                            ###'
echo '##################################################'

printf "\n\nStep 0. Update System\n"
apt-get update -y
apt-get upgrade -y

printf "\n\nStep 1. OpenSSH Installation\n"
apt-get install openssh-client

printf "\n\nStep 2. Net Tools Installation\n"
apt-get install net-tools

printf "\n\nStep 3. Installing Python PIP and VENV\n"
apt-get install python3-pip -y
apt-get install python3.8-venv -y

printf "\n\nStep 4. Configuring Time Zone\n"
# echo "To display list of available timezones use command '$ timedatectl list-timezones'."
# read -p "Enter your timezone in format <Region>/<City> (i.e. Europe/Warsaw): " timezone
# timedatectl set-timezone $timezone

printf "\n\nStep 5. Installing Docker\n"
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do apt-get remove -y $pkg; done
apt-get update -y
apt-get install ca-certificates curl -y
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -y
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
apt-get install docker-compose -y
groupadd docker
usermod -aG docker $USER

printf "\n\nStep 6. Preparing .env file\n"

> .env

echo "Setting BOOLHUB_CENTRAL_PATH variable to '$PWD/central'"
echo "BOOLHUB_CENTRAL_PATH=$PWD/central" >> .env

echo "Setting BOOLHUB_BRAINSTONE_PATH variable to '$PWD/brainstone'"
echo "BOOLHUB_BRAINSTONE_PATH=$PWD/brainstone" >> .env

echo -n "Enter location where system backups will be stored: "
read backup_path
echo "BOOLHUB_BACKUPS_PATH=${backup_path}" >> .env

echo -n "Enter PostgreSQL username: "
read postgresql_username
echo "POSTGRE_USER=${postgresql_username}" >> .env

echo "Enter PostgreSQL password: "
read -s postgresql_password
echo "POSTGRE_PASSWORD=${postgresql_password}" >> .env

echo "Enter Redis password: "
read -s redis_password
echo "REDIS_PASSWORD=${redis_password}" >> .env
