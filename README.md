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
  "promo_used_format": "GB"
}
```

<br>

### Instalation

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

This script should be continuously called by your server in order to get the most recent data (in my case a Raspberry Pi 4B with a Cron job running the script every 10 minutes).

My cron job looks like this, change your own at your convenience:

```
# Request at random time between 15 and 30 https://unix.stackexchange.com/a/140752
* * * * * { sleep $(( RANDOM % (30 - 15 + 1 ) + 15 ))m ; printf "\%s: " "$(date "+\%F \%T")"; /usr/bin/python /home/pi/tgbot/api-republicamovil.py; } >> /home/pi/logs/cronlog 2>&1

```

Here I am executing the script every 10 minutes and saving a log every time the job runs, printing the timestamp as well as the output.

<br>

### Env File Format

```
RM_USERNAME="<YOUR_USERNAME>"
RM_PASSWORD="<YOUR_PASSWORD>"
API_STORAGE_FILE="<ABSOLUTE_PATH_TO_THE_JSON_FILE>"
```

In my case the last line is `API_STORAGE_FILE="/home/pi/docker/apache/api-republicamovil/data.json"`
