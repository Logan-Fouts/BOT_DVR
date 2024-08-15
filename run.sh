#!/bin/bash

# Set up X server permissions
xhost +local:

# Set up audio
pactl load-module module-null-sink sink_name=VirtualSink sink_properties=device.description=VirtualSink
pactl load-module module-virtual-source source_name=VirtualSource master=VirtualSink.monitor

# Run bot
python3 ./src/main.py

# Clean up after the script finishes
xhost -local:
pactl unload-module module-null-sink
pactl unload-module module-virtual-source
