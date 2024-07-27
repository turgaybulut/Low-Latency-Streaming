# Low Latency Streaming

## Description

This project aims to provide a low latency streaming solution by using OBS Studio, FFmpeg and GPAC.

## Requirements

- Python 3.x
- FFmpeg, compiled for low latency streaming
- GPAC, modified to support low latency DASH streaming
- OBS Studio

## Installation

1. Clone this repository.
2. Install the required Python packages: `pip install -r requirements.txt`
3. Ensure FFmpeg and GPAC are installed.
4. Modify the `main.py` file to configure the parameters.
5. Modify the source and stream settings in the OBS Studio.

## Usage

Run the main script with Python in terminal as root: `python3 main.py`

This will:

- Generate a QR code and save it as `qr.png`.
- Start an HTTP server serving the QR code at a specified port.
- Start FFmpeg using a specified command.
- Start a GPAC DASH server using a specified command and path.
- Start an HTTP server for the low latency DASH stream.

After running the script, start streaming from the OBS Studio. The stream will be available at `http://localhost:<PLAYER_PORT>`.

To terminate the script, press `Ctrl+C` in the terminal and stop streaming from the OBS Studio.

## Authors

- [Turgay Bulut](https://github.com/turgaybulut)
- [Azra Oymaağaç](https://github.com/azraoymaagac)