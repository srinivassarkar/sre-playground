#!/bin/bash
# ─────────────────────────────────────────────────────────────
# BREAK SCENARIO 3: High Latency
# What happens: hammers /orders which has a 30% chance of 1-2.5s delay
#               p99 latency alert fires
# What to watch: Grafana → histogram_quantile query, HighLatency alert
# How to fix: stop this script
# ─────────────────────────────────────────────────────────────

echo "💥 BREAK: Generating high latency on /orders..."
echo "   Watch → Grafana → Explore → Prometheus"
echo "   Query: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))"
echo ""
echo "   Press Ctrl+C to stop"
echo ""

while true; do
  curl -s http://localhost:5000/orders > /dev/null &
  curl -s http://localhost:5000/orders > /dev/null &
  curl -s http://localhost:5000/orders > /dev/null &
  sleep 0.3
done
