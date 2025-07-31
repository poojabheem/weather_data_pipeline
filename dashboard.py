import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import psycopg2
import pandas as pd
from joblib import load
from datetime import datetime, timedelta
import config
import plotly.express as px
from sqlalchemy import create_engine

from sqlalchemy import create_engine
from urllib.parse import quote_plus
import sqlite3
conn = sqlite3.connect("data/weather.db")
df = pd.read_sql("SELECT * FROM weather_data", conn)


def load_data():
    # Safely encode username and password for special characters
    user = quote_plus(config.DB_CONFIG['user'])
    password = quote_plus(config.DB_CONFIG['password'])
    host = config.DB_CONFIG['host']
    port = config.DB_CONFIG['port']
    dbname = config.DB_CONFIG['dbname']

    # SQLAlchemy connection string
    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(db_url)

    # Load data using SQLAlchemy engine
    df = pd.read_sql("SELECT * FROM weather_data ORDER BY datetime DESC", engine)
    return df


# --- Load trained Prophet model ---
def load_forecast():
    try:
        model = load("data/prophet_model.pkl")
        future = pd.DataFrame({'ds': [datetime.now() + timedelta(days=i) for i in range(1, 8)]})
        forecast = model.predict(future)
        return forecast[['ds', 'yhat']]
    except:
        return pd.DataFrame(columns=['ds', 'yhat'])

# --- Streamlit App ---
st.title("Weather Data Dashboard 🌦")
st.write("Real-time weather data and forecast")

# ---- Load data first ----
data = load_data()
forecast = load_forecast()

# --- Current Weather Summary ---
if not data.empty:
    latest = data.groupby('city').first().reset_index()
    st.subheader("Current Weather Summary")
    cols = st.columns(len(latest))
    for idx, row in latest.iterrows():
        with cols[idx]:
            st.metric(row['city'], f"{row['temperature']}°C", help=f"Humidity: {row['humidity']}%, Wind: {row['wind_speed']} m/s")
else:
    st.warning("No weather data available. Please fetch data first.")

# --- Display Data Table ---
st.subheader("Recent Weather Data")
st.dataframe(data)

# --- Forecast ---
st.subheader("7-Day Forecast")
st.dataframe(forecast)

if not forecast.empty:
    fig = px.line(forecast, x='ds', y='yhat', title="7-Day Temperature Forecast", labels={'ds': 'Date', 'yhat': 'Temperature (°C)'})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No forecast available. Train the model first.")
