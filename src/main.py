"""
Automated Screen Recording Session Manager

This module manages multiple automated screen recording sessions,
integrating with OBS, Discord notifications, and platform-specific metadata.
"""

import asyncio
import os
import sys
from typing import Dict, Any
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv

from controllers import obs_controller
import utils.timing as tm
import utils.pull_meta as pm

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


class RecordingSessionManager:
    """Manages the execution of multiple recording sessions."""

    def __init__(self, platform: int, num_episodes: int, shortest_episode: int):
        self.platform = platform
        self.num_episodes = num_episodes
        self.shortest_episode = shortest_episode

    async def run_sessions(self):
        """Executes all recording sessions."""
        for i in range(self.num_episodes):
            await self.run_single_session(i)

    async def run_single_session(self, session_number: int):
        """Runs a single recording session."""
        if session_number > 0:
            self._detect_new_episode()

        episode_length = self._get_episode_length()

        try:
            obs_ws = obs_controller.setup_ws()
        except ValueError as e:
            self._handle_error(f"OBS WebSocket setup failed: {str(e)}")
            return

        self.send_notification(
            f"Episode {session_number + 1}/{self.num_episodes} starting, it is {episode_length // 60} mins long."
        )

        print(
            f"\n{'~' * 10}\nStarting recording session {session_number + 1} of {self.num_episodes}"
        )
        await self._record_episode(obs_ws, episode_length)

        self.send_notification(f"Episode {session_number + 1} complete!")

    def _detect_new_episode(self):
        """Detects the start of a new episode."""
        detector = tm.Ep_Detector()
        detector.init_stream()
        if detector.run():
            print("New episode start detected!")

    def _get_episode_length(self) -> int:
        """Retrieves and validates the episode length."""
        meta_puller = pm.MetaPuller(slctd_pltfrm=self.platform)
        i = 0
        while True:
            if i > 4:
                self.shortest_episode = self.shortest_episode - 5
            meta_puller.run()
            length = meta_puller.length // 60
            if self.shortest_episode <= length <= self.shortest_episode * 3:
                return meta_puller.length
            self.send_notification(
                f"Unusual episode length detected, {meta_puller.length // 60} mins. Rechecking..."
            )
            print("Unusual episode length detected. Rechecking...")
            meta_puller.reset_run()
            i += 1

    async def _record_episode(self, obs_ws: Any, episode_length: int):
        """Records a single episode."""
        print(f"Starting recording session for {episode_length} seconds")
        await obs_controller.record(obs_ws, episode_length)
        print("Recording session completed")

    def send_notification(self, message: str):
        """Sends a notification to Discord."""
        if DISCORD_WEBHOOK_URL:
            webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)
            webhook.execute()
        else:
            print("Discord webhook URL not set. Skipping notification.")

    def _handle_error(self, error_message: str):
        """Handles errors by logging and exiting."""
        print(f"Error: {error_message}")
        sys.exit(1)


def get_user_input() -> Dict[str, int]:
    """Collects and validates user input."""

    def get_valid_input(prompt: str, valid_options: list = None) -> int:
        while True:
            try:
                user_input = int(input(prompt))
                if valid_options and user_input not in valid_options:
                    raise ValueError
                return user_input
            except ValueError:
                print(
                    f"Invalid input. Please enter a valid integer{' from these options: ' + str(valid_options) if valid_options else ''}."
                )

    platforms = {0: "Disney", 1: "Netflix"}
    platform_prompt = "What platform?\n" + "\n".join(
        f"{key}: {value}" for key, value in platforms.items()
    )
    platform_prompt += "\nEnter the number of your choice: "

    return {
        "platform": get_valid_input(platform_prompt, list(platforms.keys())),
        "num_episodes": get_valid_input("How many episodes? "),
        "shortest_episode": get_valid_input(
            "What is the shortest episode in minutes? "
        ),
        "sleep": get_valid_input("Sleep when done? (0: No, 1: Yes): ", [0, 1]),
    }


async def main():
    """Main function to run the automated screen recorder."""

    user_input = get_user_input()

    manager = RecordingSessionManager(
        user_input["platform"],
        user_input["num_episodes"],
        user_input["shortest_episode"],
    )

    await manager.run_sessions()

    manager.send_notification("Recording session finished!")
    print("\nAll recording sessions completed")

    if user_input["sleep"] == 1:
        os.system("systemctl suspend -i")


if __name__ == "__main__":
    asyncio.run(main())
