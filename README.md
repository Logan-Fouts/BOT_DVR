# Bot_DVR

This is just a test project to play with making some sort of bot. It is not intended for "real" use. This is a Python-based project designed to automatically record series from various streaming platforms using OBS Websockets. The project leverages machine learning to extract timestamps and locate timestamp positions on the screen. It also used system audio to determine exactly when a new episode it starting. It is also capable of fixing its own issues such as incorrect timestamp interpretation, down websites, and episodes starting partially already through.

This is an early wip. So things are likely to chance significantly.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- Automatic recording of series episodes from multiple streaming platforms.
- Uses OBS Websockets to control OBS Studio for recording.
- Machine learning to detect and extract timestamps from the screen.

## Prerequisites
- Linux with pipewire and xhost
- Python 3.6+
- OBS Studio with OBS Websockets plugin installed, and enabled
- easyocr

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Logan-Fouts/SIP.git
   cd BOT_DVR
   ```

2. **Create a virtual environment and activate it:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required Python packages:**

   ```sh
   pip install -r requirements.txt
   ```

## Configuration

1. **Create a `.env` file** in the root directory to store your OBS Websocket credentials:

   ```env
   HOST=your_obs_websocket_host
   PORT=your_obs_websocket_port
   PASSWORD=your_obs_websocket_password
   ```

## Usage

1. **Start OBS Studio** and ensure the OBS Websocket server is running.

2. Start the media

3. **Run the script:**

   ```sh
   chmod +X run.sh
   ./run.sh
   ```

   The script will automatically:
   - Setup audio sinks.
   - Fix xhost permissions.
   - Connect to the OBS Websocket.
   - Detect and locate timestamps on the streaming platform.
   - Start and stop recording based on the extracted timestamps.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
