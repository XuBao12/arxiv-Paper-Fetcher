import schedule
import time
from arxiv_fetcher import main
import logging

def job():
    logging.info("Starting daily arXiv fetch")
    main()
    logging.info("Daily arXiv fetch completed")

def main():
    # Schedule the job to run at 8:00 AM every day
    schedule.every().day.at("08:00").do(job)

    logging.info("Scheduler started. Will run daily at 8:00 AM")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()