import asyncio
import os
import sys
import pull_meta as pm
import obs_controller
import timing as tm
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def send_discord_notification(message):
    """
    Sends a notification to Discord.
    """
    if DISCORD_WEBHOOK_URL:
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)
        webhook.execute()
    else:
        print("Discord webhook URL not set. Skipping notification.")


async def run_recording_session(obs_ws, episode_length):
    """
    Runs a single recording session.
    """
    print(f"Starting recording session for {episode_length} seconds")
    await obs_controller.record(obs_ws, episode_length)
    print("Recording session completed")


async def run_sessions(num_runs, pltfrm, shortest):
    """
    Runs all episode recording sessions.
    """
    for i in range(num_runs):

        if i > 0:
            detector = tm.Ep_Detector()
            detector.init_stream()
            if detector.run():
                print("New episode start detected!")

        meta_puller = pm.MetaPuller(slctd_pltfrm=pltfrm)
        meta_puller.run()

        while (
            meta_puller.length // 60 < shortest
            or meta_puller.length // 60 > shortest * 3
        ):
            print("Short episode, checking if this is correct.")
            meta_puller.reset_run()

        episode_length = meta_puller.length

        try:
            obs_ws = obs_controller.setup_ws()
        except ValueError as e:
            print(str(e))
            sys.exit(1)

        message = f"Episode {i+1}/{num_runs} starting, it is {episode_length // 60} mins long."
        send_discord_notification(message)

        print(f"\n~~~~~~~~~~\nStarting recording session {i+1} of {num_runs}")
        await run_recording_session(obs_ws, episode_length)

        message = f"Episode {i+1} complete!"
        send_discord_notification(message)


async def main():
    """
    Runs the automated screen recorder multiple times.
    """
    pltfrm = int(input("What platform? (0: Disney, 1: Netflix [more to come :)])"))
    num_runs = int(input("How many episodes? "))
    shortest_ep = int(input("What is the shortest episode in mins? "))
    sleep = int(input("Sleep when done? 0-No 1-Yes "))

    await run_sessions(num_runs, pltfrm, shortest_ep)

    message = "Recording session finished!"
    send_discord_notification(message)

    print("\nAll recording sessions completed")

    if sleep == 1:
        os.system("systemctl suspend -i")


if __name__ == "__main__":
    asyncio.run(main())
