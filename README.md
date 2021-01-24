# api-republicamovil

## The <i>unofficial</i> API for the Spanish operator República Móvil
This API consists in a Python script which scrapes the customer section of their website and then writes the output in a JSON file.

### Example
Requesting `<YOUR_IP>:<PORT>/api-republicamovil/data.json` will return
```
{
  "min_used": "0",
  "min_available": "150",
  "cel_used": "2.64",
  "cel_available": "3",
  "promo_used": "0.00",
  "promo_available": "20"
}
```

### Instalation
``` bash
git clone "https://github.com/jchicano/api-republicamovil.git"
cd api-republicamovil
sudo pip install -r requirements.txt
touch .env
# Then open the .env file and store your username, password and file path. Use the provided format at the bottom of this README.
```
The ChromeDriver version I am using is 88.0.4324.96

### Usage
To simply run the script once, run in terminal
```
python api-republicamovil.py
```

<br>

This script should be continuously called by your server in order to get the most recent data (in my case a Raspberry Pi 4B with a Cron job executing the script every 5 minutes).

My cron job looks like this, change your own at your convenience:
```
*/5 * * * * { printf "\%s: " "$(date "+\%F \%T")"; /usr/bin/python <ABSOLUTE_PATH_TO YOUR SCRIPT>api-republicamovil.py; } >> /home/pi/logs/cronlog 2>&1
```

Here I am executing the script every 5 minutes and saving a log every time the job runs, printing the timestamp as well as the output.

### Env File Format
```
RM_USERNAME="<YOUR_USERNAME>"
RM_PASSWORD="<YOUR_PASSWORD>"
API_STORAGE_FILE="<ABSOLUTE_PATH_TO_THE_JSON_FILE>"
```
In my case the last line is `API_STORAGE_FILE="/home/pi/docker/apache/api-republicamovil/data.json"`
