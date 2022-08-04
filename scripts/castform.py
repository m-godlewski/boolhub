import config
import os
from datetime import datetime

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


BUCKET = "air"

influx = influxdb_client.InfluxDBClient(
    url = config.DB["INFLUX"]["URL"],
    token = config.DB["INFLUX"]["API_TOKEN"],
    org = config.DB["INFLUX"]["ORGANIZATION"]
)
influxdb_api = influx.write_api(
    write_options=SYNCHRONOUS
)

air_status = os.popen(
    f"miiocli airpurifiermiot --ip 192.168.0.101 --token {config.DEVICES['TOKENS']['Mi Air Purifier 3H']} status"
).read()
air_status = air_status.split("\n")

aqi = int(air_status[2].split(":")[1].strip().split(" ")[0])

humidity = int(air_status[4].split(":")[1].strip().split(" ")[0])

temperature = float(air_status[5].split(":")[1].strip().split(" ")[0])

point = influxdb_client.Point("air").tag("room", "bedroom").field("aqi", aqi).field("humidity", humidity).field("temperature", temperature)
influxdb_api.write(
    bucket=BUCKET,
    org=config.DB["INFLUX"]["ORGANIZATION"],
    record=point
)
print(f"{datetime.now()} \t\t METRIC: bedroom \t\t VALUES: {aqi}, {humidity}, {temperature}")
