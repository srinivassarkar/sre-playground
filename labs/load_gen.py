#!/usr/bin/env python3
"""
Load Generator — simulates real traffic against python-app.
Hits all endpoints at different rates to produce interesting metrics/logs/traces.
"""
import os
import random
import time
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("load-generator")

TARGET = os.getenv("TARGET_URL", "http://python-app:5000")

ENDPOINTS = [
    ("/",         0.10),   # 10% of traffic
    ("/users",    0.35),   # 35% of traffic
    ("/orders",   0.30),   # 30% of traffic
    ("/payments", 0.20),   # 20% of traffic
    ("/health",   0.05),   # 5%  of traffic
]

def weighted_endpoint():
    endpoints, weights = zip(*ENDPOINTS)
    return random.choices(endpoints, weights=weights, k=1)[0]

def run():
    logger.info(f"Load generator started → targeting {TARGET}")
    time.sleep(5)  # wait for app to be ready

    request_count = 0
    while True:
        endpoint = weighted_endpoint()
        url = f"{TARGET}{endpoint}"
        try:
            start = time.time()
            resp = requests.get(url, timeout=5)
            duration = time.time() - start
            logger.info(f"{resp.status_code} {endpoint} ({duration:.3f}s)")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed {endpoint}: {e}")

        request_count += 1

        # every 50 requests, log a summary
        if request_count % 50 == 0:
            logger.info(f"── {request_count} total requests sent ──")

        # small random delay between requests (0.5s to 2s)
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    run()
