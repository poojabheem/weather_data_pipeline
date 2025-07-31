import psycopg2
import pandas as pd
from datetime import timedelta
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


conn = psycopg2.connect(**config.DB_CONFIG)
cur = conn.cursor()

# Fetch existing rows
cur.execute("SELECT city, temperature, humidity, pressure, weather, wind_speed, datetime FROM weather_data;")
rows = cur.fetchall()

# Duplicate data for 7 extra days
for day in range(1, 8):
    for row in rows:
        new_datetime = row[6] + timedelta(days=day)
        cur.execute("""
            INSERT INTO weather_data(city, temperature, humidity, pressure, weather, wind_speed, datetime)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (row[0], row[1], row[2], row[3], row[4], row[5], new_datetime))

conn.commit()
conn.close()
print("Simulated 7 days of extra data added!")
