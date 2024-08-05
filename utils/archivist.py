"""
Script used for performing backups, recovers and managing archives.
"""

import argparse
import asyncio
import datetime
import logging
import os
import shutil
import sys
import traceback
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import config


class Backup:
    """Contains method used for data backups."""

    @staticmethod
    async def influx(backup_directory: str) -> bool:
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
            output, errors = await process.communicate()
        except Exception:
            logging.error(f"ARCHIVIST | BACKUP | INFLUX\n{traceback.format_exc()}")
            return False
        else:
            logging.info(
                f"{output.decode('utf-8')}InfluxDB backup process has been completed successfully!"
            )
            return True
        finally:
            logging.debug(output)
            logging.debug(errors)

    @staticmethod
    async def postgresql(backup_directory: str) -> bool:
        try:
            logging.info("PostgreSQL backup process started!")
            # command that will be executed inside docker container
            command = f"""
            docker exec postgresql \
            pg_dump --clean -Fc \
            --username {config.DATABASE['POSTGRE']['USER']} \
            {config.DATABASE['POSTGRE']['NAME']} > {os.path.join(backup_directory, "postgresql" ,"postgres_dump.dump")}
            """
            # create subprocess that calls shell command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            output, errors = await process.communicate()
        except Exception:
            logging.error(f"ARCHIVIST | BACKUP | POSTGRESQL\n{traceback.format_exc()}")
            return False
        else:
            logging.info(
                f"{output.decode('utf-8')}PostgreSQL backup process has been completed successfully!"
            )
            return True
        finally:
            logging.debug(output)
            logging.debug(errors)

    @staticmethod
    def archive_directory(backup_directory: str) -> bool:
        """Archive backup directory defined in backup_directory argument.
        Archive name is based on current date in 'YEAR_MONTH_DAY' format.
        """
        try:
            # make archive using shutil library
            shutil.make_archive(
                os.path.join(config.BACKUPS["PATH"], date.today().strftime("%Y_%m_%d")),
                "zip",
                root_dir=backup_directory,
            )
        except Exception:
            logging.error(f"ARCHIVIST\n{traceback.format_exc()}")
            return False
        else:
            # clear backup directory after successful backup
            if arguments.clean:
                shutil.rmtree(backup_directory)
            return True

    @staticmethod
    def prepare_directory(overwrite: bool = False) -> str:
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


class Recovery:
    """Contains method used for data recovery."""

    @staticmethod
    async def influx() -> bool:
        """Recovers whole Influx database. Returns True if operation succeed, otherwise returns False."""
        try:
            logging.info("InfluxDB recovery process started!")
            # command that will be executed inside docker container
            command = f"""
            docker exec influxdb influx restore \
            -t {config.DATABASE['INFLUX']['API_TOKEN']} \
            {os.path.join(config.BACKUPS["PATH"], "influxdb")} \
            --full
            """
            # create subprocess that calls shell command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            output, errors = await process.communicate()
        except Exception:
            logging.error(f"ARCHIVIST | RECOVERY | INFLUX\n{traceback.format_exc()}")
            return False
        else:
            logging.info(
                f"{output.decode('utf-8')}InfluxDB recovery process has been completed successfully!"
            )
            return True
        finally:
            logging.debug(output)
            logging.debug(errors)

    @staticmethod
    async def postgresql() -> bool:
        """Recovers whole PostgreSQL database. Returns True if operation succeed, otherwise returns False."""
        try:
            logging.info("PostgreSQL recovery process started!")
            # command that will be executed inside docker container
            command = f"""
            docker exec postgresql \
            pg_restore --clean \
            --username {config.DATABASE['POSTGRE']['USER']} \
            --database {config.DATABASE['POSTGRE']['NAME']} \
            -1 {os.path.join(config.BACKUPS["PATH"], "postgresql", "postgres_dump.dump")}
            """
            # create subprocess that calls shell command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            output, errors = await process.communicate()
        except Exception:
            logging.error(f"ARCHIVIST | RECOVERY | POSTGRESQL\n{traceback.format_exc()}")
            return False
        else:
            logging.info(
                f"{output.decode('utf-8')}PostgreSQL recovery process has been completed successfully!"
            )
            return True
        finally:
            logging.debug(output)
            logging.debug(errors)

    @staticmethod
    def cleanup() -> bool:
        """Removing temporary files and directories (unpacked from backup archive) used in recovery process."""
        try:
            # list of temporary directories to delete
            directories_to_delete = [
                entry
                for entry in os.listdir(config.BACKUPS["PATH"])
                if not entry.endswith(".zip")
            ]
            # removing temporary directories
            for directory in directories_to_delete:
                shutil.rmtree(os.path.join(config.BACKUPS["PATH"], directory))
        except Exception:
            logging.error(f"ARCHIVIST | RECOVERY\n{traceback.format_exc()}")
            return False
        else:
            return True

    @staticmethod
    def unpack_directory(backup_date: str) -> bool:
        """Unpacks backup archive from date given by argument."""
        try:
            # check if given date matches format
            # if not, exception will be risen
            datetime.datetime.strptime(backup_date, "%Y_%m_%d").date()
            # path to backup archive
            backup_archive_path = os.path.join(
                config.BACKUPS["PATH"], f"{backup_date}.zip"
            )
            # unpack archive to general backup path
            shutil.unpack_archive(backup_archive_path, config.BACKUPS["PATH"], "zip")
        except ValueError:
            logging.error(
                f"Given date '{backup_date}' did not match format '%Y_%m_%d'!"
            )
            return False
        except Exception:
            logging.error(f"ARCHIVIST | RECOVERY | INFLUX\n{traceback.format_exc()}")
            return False
        else:
            return True


# main section of script
if __name__ == "__main__":
    # parses script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="Work mode - 'backup' or 'recovery'")
    parser.add_argument(
        "-d",
        "--date",
        help="[RECOVERY] Date of backup to use for recovery. Date should be given in format YEAR_MONTH_DAY.",
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        default=True,
        help="[BACKUP] Overwrite backup if one already exists?",
    )
    parser.add_argument(
        "-c",
        "--clean",
        default=True,
        help="[BACKUP] Delete directory after making archive?",
    )
    arguments = parser.parse_args()

    # if 'backup' mode has been chosen
    if arguments.mode == "backup":
        # current scheduled backup subdirectory
        backup_directory = Backup.prepare_directory(arguments.overwrite)
        # backup influx database
        asyncio.run(Backup.influx(backup_directory))
        # backup postgresql database
        asyncio.run(Backup.postgresql(backup_directory))
        # archive backup subdirectory
        Backup.archive_directory(backup_directory)
    # if 'recovery' mode has been chosen
    elif arguments.mode == "recovery":
        # unpack archive
        Recovery.unpack_directory(backup_date=arguments.date)
        # influxdb recovery
        asyncio.run(Recovery.influx())
        # postgresql recovery
        asyncio.run(Recovery.postgresql())
        # cleanup after recovery
        Recovery.cleanup()
