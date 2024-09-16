echo '##################################################'
echo '###                                            ###'
echo '###                                            ###'
echo '###             BoolHub Installation           ###'
echo '###                                            ###'
echo '###                                            ###'
echo '##################################################'

echo "\n\n\nStep 0. Update System"
apt-get update -y
apt-get upgrade -y

echo "\n\n\nStep 1. OpenSSH Installation"
apt-get install openssh-client

echo "\n\n\nStep 2. Net Tools Installation"
apt-get install net-tools

echo "\n\n\nStep 3. Installing Python PIP and VENV"
apt-get install python3-pip -y
apt-get install python3.8-venv -y

echo "\n\n\nStep 4. Configuring Time Zone"
# echo "To display list of available timezones use command '$ timedatectl list-timezones'."
# read -p "Enter your timezone in format <Region>/<City> (i.e. Europe/Warsaw): " timezone
# timedatectl set-timezone $timezone

echo "\n\n\nStep 5. Installing Docker"
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do apt-get remove $pkg; done
apt-get update -y
apt-get install ca-certificates curl
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
newgrp docker
