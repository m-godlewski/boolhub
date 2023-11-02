"""
Script used for performing backups and managing archives.
"""

import asyncio
import logging
import os
import shutil
import sys
import traceback
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import config
import scripts.utils.docker as docker


async def backup_influx(backup_directory: str) -> bool:
    command = f"docker exec -it influxdb influxd backup -portable {os.path.join(backup_directory)}"
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, output = await process.communicate()
    print(_)
    print(output)


def backup_logs(backup_directory: str) -> bool:
    """Makes copy of log file. Returns True if operation succeed, otherwise returns False."""
    try:
        shutil.copyfile(
            src=config.LOG_FILE, dst=os.path.join(backup_directory, "scripts.log")
        )
    except Exception:
        logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
        return False
    else:
        return True


def backup_postgresql(backup_directory: str) -> bool:
    pass


def __prepare_directory(overwrite: bool = False) -> str:
    """Creates backup subdirectory for current scheduled backup.
    If there is no root backup directory creates it first."""
    # creates root backup directory if it does not exist
    if not os.path.isdir(config.BACKUPS["PATH"]):
        os.mkdir(os.path.join(config.BACKUPS["PATH"]))
    # path of backup subdirectory
    subdirectory_path = os.path.join(
        config.BACKUPS["PATH"], date.today().strftime("%Y_%m_%d")
    )
    # checks if subdirectory exists
    if not os.path.isdir(subdirectory_path):
        os.mkdir(os.path.join(subdirectory_path))
        return subdirectory_path
    # otherwise create subdirectory
    else:
        # or overwrite existing one
        if overwrite:
            shutil.rmtree(subdirectory_path)
            os.mkdir(os.path.join(subdirectory_path))
            return subdirectory_path
        else:
            raise FileExistsError(
                "Backup subdirectory already exists, consider using overwrite argument!"
            )


#
if __name__ == "__main__":
    """
    1. docker-compose down
    2. perform backups
    3. docker-compose up -d / sudo reboot
    IDEAS:
        - add overwrite argument to backups
    """
    # current scheduled backup subdirectory
    # backup_directory = __prepare_directory(overwrite=True)
    # stops all containers
    # asyncio.run(docker.docker_compose_down())
    # makes log file backup
    # backup_logs(backup_directory)
    # asyncio.run(backup_influx(backup_directory))
    # backup_postgresql(backup_directory)
    # starts all containers
    # asyncio.run(docker.docker_compose_up())
