import schedule, time, subprocess, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline():
    logging.info("Fetching weather data...")
    subprocess.run(["python", "scripts/fetch_data.py"])
    logging.info("Loading into database...")
    subprocess.run(["python", "scripts/load_db.py"])
    logging.info("Generating visualization...")
    subprocess.run(["python", "scripts/visualize.py"])

schedule.every(1).hours.do(run_pipeline)

if __name__ == "__main__":
    logging.info("Scheduler started. Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(1)
