import asyncio
import sys
from dotenv import load_dotenv
import pull_meta as pm
import obs_controller

load_dotenv()


def main():
    """
    Runs the automated screen recorder.
    """
    meta_puller = pm.MetaPuller()
    meta_puller.run()
    episode_length = meta_puller.length
    print(f"Seconds to record: {episode_length}")

    if not episode_length or episode_length == 0:
        print("Episode length not correct.")
        sys.exit

    try:
        obs_ws = obs_controller.setup_ws()
    except ValueError as e:
        print(str(e))
        sys.exit(1)

    asyncio.run(obs_controller.record(obs_ws, episode_length))


if __name__ == "__main__":
    main()
