import os
import threading
import time
from typing import BinaryIO

import requests
import schedule
from app.logging_config import logger
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

EXTRACTOR_URL = os.getenv("EXTRACTOR_URL", "http://localhost:8081")


# Checks health endpoint of Extractor service
def healthcheck():
    try:
        response = requests.get(f"{EXTRACTOR_URL}/actuator/health", timeout=5)
        if response.status_code != 200 or response.json()["status"] != "UP":
            logger.error(f"Bad response from Text Extractor: {response.json()}")
            return False
    except requests.RequestException as e:
        logger.error(f"Error connecting to Text Extractor:\n{e}")
        return False

    return True


# Calls Extractor service to extract text from provided file
def call_pdf_extractor(file: BinaryIO):
    file.seek(0)
    files = {"file": ("file.pdf", file, "application/pdf")}
    logger.info(" Calling text extractor service")
    try:
        response = requests.post(f"{EXTRACTOR_URL}/extract", files=files)
    except requests.RequestException as e:
        logger.error(f"Error calling text extractor: {e}")
        raise HTTPException(
            status_code=500,
            detail="There was an error calling the backend text extractor service",
        )
    else:
        return response


# Runs the healthcheck scheduler in a loop
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Test the extractor service every 1 minute
schedule.every(1).minutes.do(healthcheck)

# Kick off the health check in the background
thread = threading.Thread(target=run_scheduler, daemon=True)
thread.start()
