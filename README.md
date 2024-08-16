# NEXRAD File Grabber

A Python application for downloading NEXRAD L2 data from AWS S3, which houses data from NOAA/NWS.

## Features

- User-friendly GUI built with customtkinter
- Select specific year, month, day, radar site, and time range for data retrieval
- Download multiple NEXRAD scans simultaneously
- Progress tracking for downloads
- Logging functionality for debugging and tracking operations

## Requirements

- Python 3.12.x
- Consistent internet connection
- Required Python packages (see `requirements.txt`)

## Installation

There are two ways to run this program. The first is to use the executable file that is provided in the releases portion of the repository. The second is to download the source code directly.

1. Executable File:
    1. Download the executable file from the releases section of the repository.
    2. Run the executable file.

2. Source Code:
    1. Clone this repository or download the source code.
    2. Install the required packages:
        pip install -r requirements.txt  &  [CTkScrollableDropdown](https://github.com/Akascape/CTkScrollableDropdown)           

## Usage

1. Run the `gui.py` script to start the application:
    python NEXRAD-File-Grabber/gui.py
2. Use the GUI to select the desired year, month, day, radar site, and time range.
3. Click "Find Scans" to search for available NEXRAD scans.
4. Select the scans you want to download and click "Download Selected Scans".

## Important Notes

- When selecting scan indexes, only enter the numbers you want to use. Do not include spaces, commas, or any other separators.
- Download progress is displayed in real-time.

## Project Structure

- `gui.py`: Contains the main GUI implementation
- `main.py`: Includes backend logic for NEXRAD data retrieval and processing
- `requirements.txt`: Lists all required Python packages

## License

This project is licensed under the CC0 1.0 Universal (CC0 1.0) Public Domain Dedication. For more details, see [Creative Commons CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)

## Contributing

Contributions to improve NEXRAD File Grabber are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.
