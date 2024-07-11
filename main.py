import asyncio
import sys
import pull_meta as pm
import obs_controller


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
    num_runs = 1
    break_duration = 7

    for i in range(num_runs):
        meta_puller = pm.MetaPuller(slctd_pltfrm=0)
        meta_puller.run()
        episode_length = meta_puller.length
        print(f"Seconds to record: {episode_length}")

        try:
            obs_ws = obs_controller.setup_ws()
        except ValueError as e:
            print(str(e))
            sys.exit(1)

        print(f"\nStarting recording session {i+1} of {num_runs}")
        await run_recording_session(obs_ws, episode_length)

        if i < num_runs - 1:
            print(f"Taking a {break_duration}-second break before the next session")
            await asyncio.sleep(break_duration)

    print("\nAll recording sessions completed")


if __name__ == "__main__":
    asyncio.run(main())
