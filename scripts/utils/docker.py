"""
Script contains method used for managing docker containers.
"""

import asyncio
import logging
import traceback

import config


async def docker_compose_down(rmi: bool = False) -> bool:
    """Stops each running docker container using 'docker compose down' command.
    When 'rmi' argument is set to True, local custom images will be removed.
    Returns True if operation succeed, otherwise returns False.
    """
    try:
        logging.critical("Stopping all running containers")
        # bash command
        if rmi:
            command = f"docker compose -f {config.BASE_DIR}/docker-compose.yml down"
        else:
            command = f"docker compose -f {config.BASE_DIR}/docker-compose.yml down --rmi local"
        # create subprocess that calls shell command
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, output = await process.communicate()
    except Exception:
        logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
        return False
    else:
        logging.critical(f"All containers has been stopped\n{output.decode('utf-8')}")
        return True


async def docker_compose_up() -> bool:
    """Starts each container using 'docker compose up -d' command.
    Returns True if operation succeed, otherwise returns False."""
    try:
        logging.critical("Starts all containers")
        # create subprocess that calls shell command
        process = await asyncio.create_subprocess_shell(
            f"docker compose -f {config.BASE_DIR}/docker-compose.yml up -d",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, output = await process.communicate()
    except Exception:
        logging.error(f"Unknown error occurred!\n{traceback.format_exc()}")
        return False
    else:
        logging.critical(f"All containers has been started\n{output.decode('utf-8')}")
        return True
