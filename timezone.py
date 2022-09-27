import datetime
# time_in_millis = 1664106028661
def convert_milli_to_datetime(time_in_millis):
    dt = datetime.datetime.fromtimestamp(time_in_millis / 1000.0, tz=datetime.timezone.utc)
    return dt


import pandas as pd
import numpy as np
from pages.Chatbot_Realtime_DB_Dashboard import query_crate

df = query_crate()
df.time = df.time.apply(lambda x: convert_milli_to_datetime(x))
print(df)