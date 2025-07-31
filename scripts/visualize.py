import sys, os, sqlite3, pandas as pd, matplotlib.pyplot as plt, logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def visualize_data():
    conn = sqlite3.connect(config.DB_PATH)
    df = pd.read_sql_query("SELECT datetime, temperature FROM weather_data ORDER BY datetime", conn)
    conn.close()

    if df.empty:
        logging.warning("No data to visualize.")
        return

    plt.plot(df['datetime'], df['temperature'], marker='o')
    plt.title("Temperature Over Time")
    plt.xlabel("Datetime")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    os.makedirs("data", exist_ok=True)
    plt.savefig("data/temperature_trend.png")
    logging.info("Chart saved to data/temperature_trend.png")

if __name__ == "__main__":
    visualize_data()
