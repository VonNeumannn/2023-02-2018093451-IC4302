import hashlib
import json
import datetime


current_timestamp = datetime.datetime.now()
print(current_timestamp)

timestamp_str = current_timestamp.strftime("%Y-%m-%dT%H:%M:%S")
print(timestamp_str)
