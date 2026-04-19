#!/bin/bash
# ─────────────────────────────────────────────────────────────
# FIX: Restore everything to healthy state
# Run this after any break scenario to recover
# ─────────────────────────────────────────────────────────────

echo "🔧 Restoring all services..."

# Restart app if stopped
docker start python-app 2>/dev/null && echo "  ✅ python-app started" || echo "  ℹ️  python-app already running"

# Restart load generator
docker restart load-generator 2>/dev/null && echo "  ✅ load-generator restarted"

echo ""
echo "⏳ Wait ~60s for Prometheus to detect recovery and resolve alerts"
echo "   Watch → http://localhost:9090/alerts (should go green)"
echo "   Watch → docker logs alertwebhook -f (should see RESOLVED messages)"
