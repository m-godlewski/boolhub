# Troubleshooting

### Extending operating system usage to 100% of disk space.

```
root@util:~# vgdisplay
<snip>
root@util:~# lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv
<snip>
root@util:~# resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
<snip>
```

### Error using miiocli.

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

**Solution:**  
Remove @resultcallback decorator from line pointed in error message.

### Error during psycopg2 installation.

```
Error: pg_config executable not found.
```

**Solution:**

```
sudo apt-get install libpq-dev
```

```
sudo apt-get install python3.8-dev
```

### Error during bluepy installation.

When you are facing errors during bluepy installation. Follow installation guide on [official github repository](https://github.com/IanHarvey/bluepy).

### Gatherer.py cannot read data from Xiaomi Monitor 2

```
$ sudo apt install bluez
```

### Setting static IP for server

https://www.freecodecamp.org/news/setting-a-static-ip-in-ubuntu-linux-ip-address-tutorial/

### Set up SSH key authorization.

https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04
