#!/bin/bash

# Set up X server permissions
xhost +local:

# Set up audio
pactl load-module module-null-sink sink_name=VirtualSink sink_properties=device.description=VirtualSink
pactl load-module module-virtual-source source_name=VirtualSource master=VirtualSink.monitor

python3 ./src/main.py

# Clean up after the script finishes
xhost -local:
