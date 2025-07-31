import sys
import os
import psycopg2
import pandas as pd
import glob
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_to_db():
    files = glob.glob("data/*.csv")
    if not files:
        logging.warning("No CSV files found. Run fetch_data.py first.")
        return

    latest_file = max(files, key=os.path.getctime)
    logging.info(f"Loading data from {latest_file}")
    df = pd.read_csv(latest_file)

    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**config.DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                            city TEXT,
                            temperature REAL,
                            humidity INT,
                            pressure INT,
                            weather TEXT,
                            wind_speed REAL,
                            datetime TIMESTAMP
                        )''')

        for _, row in df.iterrows():
            cursor.execute('''INSERT INTO weather_data
                              (city, temperature, humidity, pressure, weather, wind_speed, datetime)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           (row['city'], row['temperature'], row['humidity'], row['pressure'],
                            row['weather'], row['wind_speed'], row['datetime']))
        conn.commit()
        logging.info("Data successfully loaded into PostgreSQL database.")

    except Exception as e:
        logging.error(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_to_db()
