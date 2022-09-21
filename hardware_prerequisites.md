# Hardware Prerequisites


## Operating System
Ubuntu Server 20.04


## Step by step installation guide
1. Install Ubuntu Server 20.04.
2. Install OpenSSH and net-tools.
3. Install Python, PIP and venv.
4. Install docker engine and docker-compose.
5. Run command
```
docker-compose up -d
```
6. Create user and password for each application.


## Troubleshooting
1. Extending operating system usage to 100% of disk space.
```
root@util:~# vgdisplay
<snip>
root@util:~# lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv
<snip>
root@util:~# resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
<snip>
```