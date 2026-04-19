#!/bin/bash
# ─────────────────────────────────────────────────────────────
# BREAK SCENARIO 1: Spike Error Rate
# What happens: hammers /crash endpoint → error rate alert fires
# What to watch: Prometheus alert "HighErrorRate", Loki ERROR logs
# How to fix: stop this script
# ─────────────────────────────────────────────────────────────

echo "💥 BREAK: Spiking error rate on python-app..."
echo "   Watch → Prometheus: http://localhost:9090/alerts"
echo "   Watch → Alert webhook logs: docker logs alertwebhook -f"
echo "   Watch → Grafana Explore → Loki → {service=\"python-app\"} |= \"ERROR\""
echo ""
echo "   Press Ctrl+C to stop"
echo ""

while true; do
  curl -s http://localhost:5000/crash > /dev/null
  curl -s http://localhost:5000/payments > /dev/null
  curl -s http://localhost:5000/payments > /dev/null
  sleep 0.2
done
