# api-republicamovil

## The <i>unofficial</i> API for the Spanish operator República Móvil

This API consists in a Python script which scrapes the customer section of their website and then writes the output in a JSON file.

<br>

### Example

Requesting `<YOUR_IP>:<PORT>/api-republicamovil/data.json` will return

```
{
  "min_used": "0",
  "min_available": "150",
  "cel_used": "2.64",
  "cel_available": "3",
  "cel_used_format": "GB",
  "promo_used": "0.00",
  "promo_available": "20",
  "promo_used_format": "GB",
  "last_request": "27/03/2021 17:13:59"
}
```

<br>

### Installation

```bash
git clone "https://github.com/jchicano/api-republicamovil.git"
cd api-republicamovil
sudo pip install -r requirements.txt
touch .env
# Then open the .env file and store your username, password and file path. Use the provided format at the bottom of this README.
```

The ChromeDriver version I am using is 88.0.4324.96

<br>

### Usage

To simply run the script once, run in terminal

```
python api-republicamovil.py
```

This script should run in background by your server in order to get the most recent data (in my case a Raspberry Pi 4B with a service running the script).

Create one with `sudo systemctl edit --force --full api-republicamovil.service` and enable boot start with `sudo systemctl enable api-republicamovil.service`

My service looks like this, change your own at your convenience:

```
[Unit]
Description=API Republica Movil
Wants=network-online.target
After=network.target

[Service]
ExecStart=/usr/bin/python /home/pi/tgbot/api-republicamovil.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

<br>

### Env File Format

```
RM_USERNAME="<YOUR_USERNAME>"
RM_PASSWORD="<YOUR_PASSWORD>"
API_STORAGE_FILE="<ABSOLUTE_PATH_TO_THE_JSON_FILE>"
```

In my file the last line is `API_STORAGE_FILE="/home/pi/docker/apache/api-republicamovil/data.json"`
