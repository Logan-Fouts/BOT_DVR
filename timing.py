import time
import sys
import pyaudio
import numpy as np


class Ep_Detector:
    """
    Ep_Detector class to detect audio episodes from a virtual audio input device.
    """

    def __init__(self):
        """
        Initializes the Ep_Detector with default values and sets up the PyAudio object.
        """
        self.silence_time = 0.1
        self.silence_thresh = 0.0000001
        self.last_audio_time = time.time()
        self.silence_notified = False
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.new_episode_start = False

    def audio_callback(self, in_data, frame_count, time_info, status):
        """
        Callback function for processing audio data from the stream.
        """
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        volume = np.linalg.norm(audio_data)
        current_time = time.time()

        if volume > self.silence_thresh:
            # print("Audio detected")
            self.last_audio_time = current_time
            if self.silence_notified:
                # print("New ep")
                self.silence_notified = False
                self.new_episode_start = True
        # Check if silence duration exceeds the threshold
        if (
            current_time - self.last_audio_time > self.silence_time
            and not self.silence_notified
        ):

            print("Silence")
            self.silence_notified = True

        return (in_data, pyaudio.paContinue)

    def init_stream(self):
        """
        Initializes the audio stream using a virtual audio input device.

        Finds the virtual device and opens the audio stream with the appropriate settings.
        """
        # Find the virtual device
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if "VirtualSink" in dev["name"]:
                dev_index = i
                print(f"Found Virtual1 device: {dev['name']}")
                break
        else:
            print("Virtual device not found")
            sys.exit(1)

        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=2,
            rate=48000,
            input=True,
            input_device_index=dev_index,
            stream_callback=self.audio_callback,
        )

    def run(self):
        """
        Starts the audio stream and monitors for new episodes.

        Runs the stream until a new episode is detected or interrupted by the user.
        """
        self.stream.start_stream()
        try:
            while self.stream.is_active():
                if self.new_episode_start:
                    self.stream.stop_stream()
                    self.stream.close()
                    self.p.terminate()
                    return True
                time.sleep(0.2)  # Sleep to prevent high CPU usage
        except KeyboardInterrupt:
            pass
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return False


# A quick test
# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#     dev = p.get_device_info_by_index(i)
#     print(f"Device {i}: {dev['name']}")
# p.terminate()
# detector = Ep_Detector()
# detector.init_stream()
# if detector.run():
#     print("New episode start detected.")
#
# p.terminate()


# pactl load-module module-null-sink sink_name=VirtualSink sink_properties=device.
# description=VirtualSink
#
# pactl load-module module-virtual-source source_name=VirtualSource master=Virtual
# Sink.monitor
