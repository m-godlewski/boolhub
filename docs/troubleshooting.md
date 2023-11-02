# Troubleshooting
### 1. Extending operating system usage to 100% of disk space.
```
root@util:~# vgdisplay
<snip>
root@util:~# lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv
<snip>
root@util:~# resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
<snip>
```
### 2. Error using miiocli.
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
__Solution:__   
Remove @resultcallback decorator from line pointed in error message.

### 3. Grafana container is crashing when starting.
```
grafana_1        | GF_PATHS_DATA='/var/lib/grafana' is not writable.
grafana_1        | You may have issues with file permissions, more information here: http://docs.grafana.org/installation/docker/#migration-from-a-previous-version-of-the-docker-container-to-5-1-or-later
grafana_1        | mkdir: cannot create directory '/var/lib/grafana/plugins': Permission denied
```
__Solution:__   
Change ownership of grafana mapped directory.
```
sudo chown 472:472 /data/grafana/
```
### 4. Error during psycopg2 installation.
```
Error: pg_config executable not found.
```
__Solution:__   
```
sudo apt-get install libpq-dev
```

### 5. Error during bluepy installation.
When you are facing errors during bluepy installation. Follow installation guide on [official github repository](https://github.com/IanHarvey/bluepy).
