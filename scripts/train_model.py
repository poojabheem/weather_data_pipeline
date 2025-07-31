import sys, os
import psycopg2
import pandas as pd
from prophet import Prophet
from joblib import dump

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

conn = psycopg2.connect(**config.DB_CONFIG)
df = pd.read_sql("SELECT datetime, temperature FROM weather_data", conn)
conn.close()

df.rename(columns={'datetime': 'ds', 'temperature': 'y'}, inplace=True)

model = Prophet()
model.fit(df)

dump(model, "data/prophet_model.pkl")
print("Prophet model saved at data/prophet_model.pkl")
