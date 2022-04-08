Weather

#!/usr/bin/python

import weatherhat
import requests
import json
import time

sensor = weatherhat.WeatherHAT()

while True:
    time.sleep(6.0)
    sensor.update(interval=6.0)
    wind_direction_cardinal = sensor.degrees_to_cardinal(sensor.wind_direction)

    url='https://<hostname>:<port>/services/collector/event'
    authHeader = {'Authorization': 'Splunk <HEC Token>'}
    jsonDict = {
            "event": "metric",
            "source": "metrics",
            "sourcetype": "weather",
            "host": "weather_station",
            "fields": {
                  "metric_name:ws.deviceTemp": str(round(sensor.device_temperature,2)),
                  "metric_name:ws.temp": str(round(sensor.temperature,2)),
                  "metric-name:ws.humid":    str(round(sensor.humidity,2)),
                  "metric_name:ws.dewPoint":   str(round(sensor.dewpoint,2)),
                  "metric_name:ws.light":       str(round(sensor.lux,2)),
                  "metric_name:ws.pressure":    str(round(sensor.pressure,2)),
                  "metric_name:ws.windAvg":    str(round(sensor.wind_speed,2)),
                  "metric_name:ws.rain":        str(round(sensor.rain,2)),
                  "metric_name:ws.windDeg":    str(round(sensor.wind_direction,2))
                },
                }

    r = requests.post(url, headers=authHeader, json=jsonDict, verify=False)