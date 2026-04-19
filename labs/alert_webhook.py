#!/usr/bin/env python3
"""
Alert Webhook — receives Alertmanager notifications and prints them clearly.
In prod this would be PagerDuty/Slack. In the lab, this shows you alerts firing.
"""
from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s"
)
logger = logging.getLogger("alert-webhook")

app = Flask(__name__)

@app.route("/alert", methods=["POST"])
def receive_alert():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400

    for alert in data.get("alerts", []):
        status    = alert.get("status", "unknown").upper()
        name      = alert.get("labels", {}).get("alertname", "unknown")
        severity  = alert.get("labels", {}).get("severity", "unknown")
        summary   = alert.get("annotations", {}).get("summary", "")
        desc      = alert.get("annotations", {}).get("description", "")

        if status == "FIRING":
            logger.info(f"🔥 ALERT FIRING  | [{severity.upper()}] {name}")
        else:
            logger.info(f"✅ ALERT RESOLVED | [{severity.upper()}] {name}")

        if summary:
            logger.info(f"   Summary     : {summary}")
        if desc:
            logger.info(f"   Description : {desc}")
        logger.info(f"   ─────────────────────────────────────────")

    return jsonify({"status": "received"}), 200

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    logger.info("Alert webhook receiver started on port 5001")
    app.run(host="0.0.0.0", port=5001)
