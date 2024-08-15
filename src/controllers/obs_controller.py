import os
import time
import asyncio
from dataclasses import dataclass
from obswebsocket import obsws, requests
from dotenv import load_dotenv
import pyautogui as pg
import utils.pull_meta as pm

load_dotenv()


@dataclass
class ObsWebConnection:
    """
    Defines details for obs websocket connection.
    """

    host: str
    port: int
    password: str


def setup_ws():
    """
    Sets up obs connection.
    """
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", "4444"))
    password = os.getenv("PASSWORD", "default_password")
    if not host or not password or not port:
        raise ValueError(
            "Please provide all required info to connect to obs websocket."
        )
    return ObsWebConnection(host, port, password)


async def check_end():
    """
    Checks for location of skip button to determine if end of episode.
    """
    location = None

    while location is None:
        meta_puller = pm.MetaPuller()
        location = meta_puller.find_skip()


async def record(obs_ws, episode_length):
    """
    Connects to obs websocket and starts and stops recording for given time.
    """
    ws = obsws(obs_ws.host, obs_ws.port, obs_ws.password)
    ws.connect()

    try:
        ws.call(requests.ToggleRecord())
        print("Recording started")
        await asyncio.sleep(episode_length - 90)
        await check_end()
        print("End detected stopping recording.")
        ws.call(requests.ToggleRecord())
        print("Recording stopped")
    finally:
        ws.disconnect()
