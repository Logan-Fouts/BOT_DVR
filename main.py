import asyncio
import os
import sys
import pull_meta as pm
import obs_controller
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
        response = webhook.execute()
        if response.status_code != 204 or response.status_code != 200:
            print(
                f"Failed to send Discord notification. Status code: {response.status_code}"
            )
    else:
        print("Discord webhook URL not set. Skipping notification.")


async def run_recording_session(obs_ws, episode_length):
    """
    Runs a single recording session.
    """
    print(f"Starting recording session for {episode_length} seconds")
    await obs_controller.record(obs_ws, episode_length)
    print("Recording session completed")


async def main():
    """
    Runs the automated screen recorder multiple times.
    """
    pltfrm = int(input("What platform? (0: Disney, 1: Netflix [more to come :)])"))
    num_runs = int(input("How many episodes? "))
    break_duration = int(input("How long breaks between episodes? "))

    for i in range(num_runs):
        meta_puller = pm.MetaPuller(slctd_pltfrm=pltfrm)
        meta_puller.run()
        episode_length = meta_puller.length

        try:
            obs_ws = obs_controller.setup_ws()
        except ValueError as e:
            print(str(e))
            sys.exit(1)

        print(f"\n~~~~~~~~~~\nStarting recording session {i+1} of {num_runs}")
        await run_recording_session(obs_ws, episode_length)

        message = (
            f"Episode {i+1} complete, it was {meta_puller.length // 60} mins long."
        )
        send_discord_notification(message)

        if i < num_runs - 1:
            print(
                f"Taking a {break_duration}-second break before the next session\n~~~~~~~~~~\n\n"
            )
            await asyncio.sleep(break_duration)

    message = "Recording session finished!"
    send_discord_notification(message)

    print("\nAll recording sessions completed")


if __name__ == "__main__":
    asyncio.run(main())
