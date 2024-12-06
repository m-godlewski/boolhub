#!/bin/bash

echo "  ____                    _   _    _           _     "
echo " |  _ \                  | | | |  | |         | |    "
echo " | |_) |   ___     ___   | | | |__| |  _   _  | |__  "
echo " |  _ <   / _ \   / _ \  | | |  __  | | | | | | '_ \ "
echo " | |_) | | (_) | | (_) | | | | |  | | | |_| | | |_) |"
echo " |____/   \___/   \___/  |_| |_|  |_|  \__,_| |_.__/ "
echo "                                                     "



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
echo "To display list of available timezones use command '$ timedatectl list-timezones'."
read -p "Enter your timezone in format <Region>/<City> (i.e. Europe/Warsaw): " timezone
timedatectl set-timezone $timezone



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
echo "- Removing content of  old .env file"
> .env
echo "- PATHS"
echo "- - Setting 'BOOLHUB_CENTRAL_PATH' variable to '$PWD/central'"
echo "BOOLHUB_CENTRAL_PATH=$PWD/central" >> .env
echo "- - Setting 'BOOLHUB_CENTRAL_FRONTEND_PATH' variable to '$PWD/central_frontend'"
echo "BOOLHUB_CENTRAL_FRONTEND_PATH=$PWD/central_frontend" >> .env
echo "- - Setting 'BOOLHUB_BRAINSTONE_PATH' variable to '$PWD/brainstone'"
echo "BOOLHUB_BRAINSTONE_PATH=$PWD/brainstone" >> .env
echo -n "- - Enter location where backups should be stored: "
read backup_path
echo "BOOLHUB_BACKUPS_PATH=${backup_path}" >> .env

echo "- POSTGRESQL"
echo -n "- - PostgreSQL username: "
read postgresql_username
echo "POSTGRE_USER=${postgresql_username}" >> .env
echo "- - PostgreSQL password: "
read -s postgresql_password
echo "POSTGRE_PASSWORD=${postgresql_password}" >> .env

echo "- INFLUX"
echo -n "- - Influx username: "
read influx_user
echo "INFLUX_USER=${influx_user}" >> .env
echo "- - Influx password: "
read -s influx_password
echo "INFLUX_PASSWORD=${influx_password}" >> .env
echo "- - Influx token (https://it-tools.tech/token-generator): "
read -s influx_token
echo "INFLUX_TOKEN=${influx_token}" >> .env

echo "- CENTRAL"
echo -n "- - Central username: "
read central_user
echo "CENTRAL_USER=${central_user}" >> .env
echo "- - Central password: "
read -s central_password
echo "CENTRAL_PASSWORD=${central_password}" >> .env



printf "\n\nStep 7. Generating binary shell script\n"

# binary script name
BINARY_SCRIPT="bh"

# remove file if existing
if [ -f "$BINARY_SCRIPT" ]; then
  rm "$BINARY_SCRIPT"
fi

# create file
touch "$BINARY_SCRIPT"

# fill command file with content
cat > "$BINARY_SCRIPT" <<EOF1
#!/bin/bash

DOCKERFILE_PATH=$PWD/docker-compose.yml

case \$1 in
  "stop")
    docker compose -f \$DOCKERFILE_PATH stop
  ;;
  "start")
    docker compose -f \$DOCKERFILE_PATH start
  ;;
  "restart")
    docker compose -f \$DOCKERFILE_PATH restart
  ;;
  "rebuild")
    docker compose -f \$DOCKERFILE_PATH down --rmi local
    docker compose -f \$DOCKERFILE_PATH up -d
  ;;
  "logs")
    docker compose -f \$DOCKERFILE_PATH logs -f 
  ;;
  "uninstall")
    docker compose -f \$DOCKERFILE_PATH down --rmi local
    rm -rf /data/central
    rm -rf /data/influxdb
    rm -rf /data/portainer_data
    rm -rf /data/postgres
    rm -rf /data/central
  ;;
esac

EOF1
# make binary script executable
chmod +x $BINARY_SCRIPT

# move script to /usr/bin
mv $BINARY_SCRIPT /usr/bin/$BINARY_SCRIPT

echo "Script has been generated"



printf "\n\nStep 8. Build and run docker containers\n"
docker compose up -d
# to solve problem with superuser and settings initialization
# central module container has to be restarted
docker restart central
