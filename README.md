# SIP (Stealing Isn't Piracy)

SIP is a Python-based project designed to automatically record series from various streaming platforms using OBS Websockets. The project leverages machine learning to extract timestamps and locate timestamp positions on the screen. This ensures accurate and efficient recording of your favorite series episodes.

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

- Python 3.6+
- OBS Studio with OBS Websockets plugin installed, and enabled
- easyocr

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Logan-Fouts/SIP.git
   cd SIP
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

2. **Create a `platforms.json` file** in the root directory to configure the streaming platforms:

   ```json
   [
     {
       "name": "Disney",
       "img_ll": "~/Code/GimmieDat/ll_images/disney_ll.png",
       "move_left": 30,
       "move_top": 25
     },
     {
       "name": "Netflix",
       "img_ll": "~/Code/GimmieDat/ll_images/netflix_ll.png",
       "move_left": 0,
       "move_top": -70
     }
   ]
   ```

## Usage

1. **Start OBS Studio** and ensure the OBS Websocket server is running.

2. Start the media

3. **Run the script:**

   ```sh
   python main.py
   ```

   The script will automatically:

   - Connect to the OBS Websocket.
   - Detect and locate timestamps on the streaming platform.
   - Start and stop recording based on the extracted timestamps.

## Directory Structure

```plaintext
SIP /
├── ll_images/
│   ├── disney_ll.png
│   ├── netflix_ll.png
├── main.py
├── platforms.json
├── pull_meta.py
├── requirements.txt
├── README.md
└── .env
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
