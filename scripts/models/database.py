"""
"""


class PostgreSQL:
    pass


class InfluxDB:
    pass


"""
The idea behing moving whole db logic to this script is to
remove creation of object in gatherer base class and 
only using those classes as context managers only if connection with DB is needed.
"""
