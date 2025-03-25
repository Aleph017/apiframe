# APIframe
A script that fetches and displays current Warframe cycles, Void Trader status, and active invasions for PC server.

## Features:
- Displays cycles (Plains of Eidolon, Orb Vallis, Cambion Drift, Duviri)
- Fetches Void trader status (when and where he will be)
- Lists active invasions (location, factions, rewards, time left)

## Requirements:
- Python 3
- `requests` module

## How to install:
1. Install the requests module if not installed
  ```
  pip install requests
  ```
2. Clone the repository
  ```
  git clone https://github.com/Aleph017/apiframe.git
  cd apiframe
  ```
3. Make the script executable and rename it
  ```
  chmod +x apiframe.py
  mv apiframe.py apiframe
  ```

4. Put the script in your $PATH if you want, e.g. ~/bin 
  ```
  mv apiframe ~/bin/
  ```
## Usage:
Run the script from the terminal
  ```
  apiframe
  ```
## Credits:
- **Warframe** is developed by [Digital Extremes](https://www.digitalextremes.com/).
- This script uses data from the [Warframe API](https://docs.warframestat.us/) provided by [warframestat.us](https://docs.warframestat.us/).
## Disclaimer:
The data provided by this script is fetched from the [Warframe API](https://docs.warframestat.us/). Any inaccuracies or discrepancies in the data should be attributed to the API source and not the script itself.
