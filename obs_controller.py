import os
import asyncio
from dataclasses import dataclass
from obswebsocket import obsws, requests
from dotenv import load_dotenv

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
    print(f"Connecting to host: {host} on port: {port} with password: {password}")
    return ObsWebConnection(host, port, password)


async def record(obs_ws, episode_length):
    """
    Connects to obs websocket and starts and stops recording for given time.
    """
    ws = obsws(obs_ws.host, obs_ws.port, obs_ws.password)
    ws.connect()
    try:
        response = ws.call(requests.ToggleRecord())
        print("Recording started:", response.status)
        await asyncio.sleep(episode_length - 5)
        ws.call(requests.ToggleRecord())
        print("Recording stopped")
    finally:
        ws.disconnect()
