# Hardware Prerequisites


## Operating System
Ubuntu Server 20.04


## Step by step installation guide
1. Install Ubuntu Server 20.04.
2. Install OpenSSH and net-tools.
3. Install Python, PIP and venv.
4. Install and configure git.
5. Install docker engine and docker-compose.
6. Run command
```
docker-compose up -d
```
7. Create user and password for each application.
8. Configure cronjobs to run scripts.


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
2. Error using miiocli.
```
Traceback (most recent call last):
  File "/usr/local/bin/miiocli", line 5, in <module>
    from miio.cli import create_cli
  File "/usr/local/lib/python3.9/site-packages/miio/cli.py", line 43, in <module>
    cli.add_command(device_class.get_device_group())
  File "/usr/local/lib/python3.9/site-packages/miio/integrations/vacuum/roborock/vacuum.py", line 932, in get_device_group
    @dg.resultcallback()
AttributeError: 'DeviceGroup' object has no attribute 'resultcallback'
```
To fix this issue, @resultcallback has to be removed from above mentioned line.