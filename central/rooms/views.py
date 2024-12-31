from rest_framework.decorators import api_view
from rest_framework.response import Response
from influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError

from .models import Room
from .serializer import RoomSerializer
from django.conf import settings


@api_view(["GET"])
def rooms(request) -> Response:
    """Returns a list of all Room objects."""
    query_result = Room.objects.all()
    serializer = RoomSerializer(query_result, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def rooms_air(request) -> Response:
    """Returns a list of all Rooms objects with their air data combined."""
    # empty list that will stores final results
    results = []
    try:
        # retrieves each room object
        rooms_query_result = Room.objects.all()
        rooms_serializer = RoomSerializer(rooms_query_result, many=True)
        rooms = rooms_serializer.data
        # initializes conneciton to influxdb
        influx_client = InfluxDBClient(
            url=settings.DATABASES.get("influxdb").get("URL"),
            token=settings.DATABASES.get("influxdb").get("API_TOKEN"),
            org=settings.DATABASES.get("influxdb").get("ORGANIZATION"),
        )
        influx_query_api = influx_client.query_api()
        # iterates over rooms
        for room in rooms:
            # initializes dictionary that should store air data of current iteration room
            air_data = {"aqi": None, "temperature": None, "humidity": None}
            # queries influxdb for most recent air data from current iteration room
            # query asks for data from last 15 minutes in case air device has problem with fetching air data
            air_query_result = influx_query_api.query_stream(
                query=f"""
                from(bucket: "air")
                |> range(start: -15m)
                |> filter(fn: (r) => r["_measurement"] == "air")
                |> filter(fn: (r) => r["_field"] == "aqi" or r["_field"] == "humidity" or r["_field"] == "temperature")
                |> filter(fn: (r) => r["room"] == "{room.get("name")}")
                |> aggregateWindow(every: 5m, fn: last, createEmpty: false)
                |> last()
                """
            )
            # updates air data dictionary
            for table in air_query_result:
                air_data[table.get_field()] = table.get_value()
            # combines roum data with air data
            results.append({**room, "airData": air_data})
    except InfluxDBError as e:
        print(f"Error ocurred during connection to InfluxDB\n{e}")
    except Exception as e:
        print(f"Unexpected error ocurred\n{e}")
    finally:
        # closing connection to influx database
        influx_client.close()
    return Response(results)
