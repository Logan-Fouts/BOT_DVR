FROM ubuntu:22.04

# Set non-interactive frontend and timezone
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

# Install required packages
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    ffmpeg software-properties-common \
    xvfb x11vnc xauth \
    chromium-browser \
    pulseaudio alsa-utils libpulse0 libasound2 \
    portaudio19-dev libportaudio2 \
    libx11-dev libxtst-dev libpng-dev libfreetype6-dev \
    dbus-x11 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Add OBS Studio repository and install
RUN add-apt-repository ppa:obsproject/obs-studio && \
    apt-get update && \
    apt-get install -y obs-studio && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m dockeruser
USER dockeruser
ENV HOME=/home/dockeruser
WORKDIR /home/dockeruser

# Copy requirements file
COPY --chown=dockeruser:dockeruser requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=dockeruser:dockeruser ./src ./src
COPY --chown=dockeruser:dockeruser run.sh .

RUN chmod +x ./run.sh

# Set up environment variables
ENV DISPLAY=:99
ENV PULSE_SERVER=unix:/tmp/pulseaudio.socket
ENV XDG_RUNTIME_DIR=/tmp/runtime-dockeruser
ENV PATH="/home/dockeruser/.local/bin:${PATH}"

# Start Xvfb, x11vnc, PulseAudio, OBS Studio, and Chromium
CMD mkdir -p $XDG_RUNTIME_DIR && \
    Xvfb $DISPLAY -screen 0 1920x1080x24 & \
    sleep 1 && \
    x11vnc -display $DISPLAY -forever -nopw & \
    pulseaudio --start & \
    obs & \
    chromium-browser --no-sandbox --start-maximized & \
    ./run.sh
