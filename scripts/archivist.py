"""
Script used for performing backups and managing archives.
"""

import argparse
import asyncio
import logging
import os
import shutil
import sys
import traceback
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import config


async def backup_influx(backup_directory: str) -> bool:
    """Makes backup of each InfluxDB bucket.
    Returns True if operation succeed, otherwise returns False.
    """
    try:
        logging.info("InfluxDB backup process started!")
        # command that will be executed inside docker container
        command = f"""
        docker exec influxdb influx backup \
        -t {config.DATABASE['INFLUX']['API_TOKEN']} \
        {os.path.join(backup_directory, "influxdb")}
        """
        # create subprocess that calls shell command
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        output, _ = await process.communicate()
    except Exception:
        logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
        return False
    else:
        logging.info(
            f"{output.decode('utf-8')}InfluxDB backup process has completed successfully!"
        )
        return True


async def backup_postgresql(backup_directory: str) -> bool:
    try:
        logging.info("PostgreSQL backup process started!")
        # command that will be executed inside docker container
        command = f"""
        docker exec postgresql pg_dumpall -c \
        -U {config.DATABASE['POSTGRE']['USER']} \
        > {os.path.join(backup_directory, "postgresql" ,"postgres_dump.sql")}
        """
        # create subprocess that calls shell command
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        output, _ = await process.communicate()
    except Exception:
        logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
        return False
    else:
        logging.info(
            f"{output.decode('utf-8')}PostgreSQL backup process has completed successfully!"
        )
        return True


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
    # otherwise create subdirectory
    else:
        # or overwrite existing one
        if overwrite:
            shutil.rmtree(subdirectory_path)
            os.mkdir(os.path.join(subdirectory_path))
        else:
            raise FileExistsError(
                "Backup subdirectory already exists, consider using overwrite argument!"
            )
    # create subdirectories for each database
    for name in ("influxdb", "postgresql"):
        os.mkdir(os.path.join(subdirectory_path, name))
    return subdirectory_path


def __archive_directory(backup_directory: str) -> bool:
    """Archive backup directory defined in backup_directory argument.
    Archive name is based on current date in 'YEAR/MONTH/DAY' format.
    """
    try:
        # make archive using shutil library
        shutil.make_archive(
            os.path.join(config.BACKUPS["PATH"], date.today().strftime("%Y_%m_%d")),
            "zip",
            root_dir=backup_directory,
        )
    except Exception:
        logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
        return False
    else:
        # clear backup directory after successful backup
        if arguments.clean:
            shutil.rmtree(backup_directory)
        return True


# main section of script
if __name__ == "__main__":
    # parses script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--overwrite", default=False)
    parser.add_argument("-c", "--clean", default=True)
    arguments = parser.parse_args()

    # current scheduled backup subdirectory
    backup_directory = __prepare_directory(overwrite=arguments.overwrite)
    # backup influx database
    asyncio.run(backup_influx(backup_directory))
    # backup postgresql database
    asyncio.run(backup_postgresql(backup_directory))
    # archive backup subdirectory
    __archive_directory(backup_directory)
