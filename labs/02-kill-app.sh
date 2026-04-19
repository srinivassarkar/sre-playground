#!/bin/bash
# ─────────────────────────────────────────────────────────────
# BREAK SCENARIO 2: Kill the App (AppDown alert)
# What happens: stops python-app container → AppDown alert fires
#               inhibit_rules suppress other alerts automatically
# What to watch: Prometheus alerts, alertwebhook logs
# How to fix: docker compose start python-app
# ─────────────────────────────────────────────────────────────

echo "💥 BREAK: Stopping python-app container..."
echo "   Watch → Prometheus: http://localhost:9090/alerts"
echo "   Watch → docker logs alertwebhook -f"
echo ""
echo "   You should see:"
echo "   1. AppDown alert fires after ~30s"
echo "   2. HighErrorRate/HighLatency alerts are SUPPRESSED (inhibit_rules)"
echo ""
echo "   To fix: docker compose -f labs/docker-compose.yml start python-app"
echo ""

docker stop python-app
echo "✅ python-app stopped. Waiting for Prometheus to detect it..."
