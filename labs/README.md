# SRE Observability Lab

A full local observability stack using Docker Compose.
**Real app → real traffic → real alerts → real dashboards.**
No cloud bill. Start and stop whenever you want.

---

## What's Running

| Container | Purpose | Port |
|-----------|---------|------|
| `python-app` | Flask app emitting metrics + logs + traces | 5000 |
| `load-generator` | Continuously hits all endpoints (real traffic) | — |
| `alertwebhook` | Receives Alertmanager alerts (simulates PagerDuty) | 5001 |
| `prometheus` | Scrapes metrics, evaluates alert rules | 9090 |
| `alertmanager` | Routes and delivers alerts | 9093 |
| `loki` | Stores logs | 3100 |
| `promtail` | Collects Docker container logs → sends to Loki | — |
| `tempo` | Stores traces | 3200 |
| `grafana` | Unified dashboard (all 3 datasources pre-wired) | 3000 |
| `node-exporter` | Host-level metrics (CPU, memory, disk) | 9100 |
| `cadvisor` | Container-level metrics | 8080 |

---

## Prerequisites

```bash
# Verify these are installed
docker --version       # Docker 24+
docker compose version # Compose v2+
```

---

## Step 1 — Start the Stack

```bash
# From the repo root
cd labs/

docker compose up -d --build

# Watch everything come up
docker compose ps
```

Wait about **30 seconds** for all services to be healthy, then verify:

```bash
# App is responding
curl http://localhost:5000/health

# Prometheus is up
curl http://localhost:9090/-/healthy

# Loki is up
curl http://localhost:3100/ready

# Tempo is up
curl http://localhost:3200/ready
```

---

## Step 2 — Open Grafana

Go to **http://localhost:3000**

- Username: `admin`
- Password: `admin`

All 3 datasources (Prometheus, Loki, Tempo) are **already configured** — no setup needed.

---

## Step 3 — Explore the 3 Pillars

### Metrics (Prometheus)

Open **http://localhost:9090** and try these PromQL queries:

```promql
# Request rate per endpoint
rate(http_requests_total[5m])

# Error rate %
rate(http_requests_total{status="500"}[5m]) / rate(http_requests_total[5m]) * 100

# p99 latency per endpoint
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))

# Which endpoints have the most errors?
topk(5, rate(app_errors_total[5m]))

# Is the app up?
up{job="python-app"}
```

In Grafana: **Explore → Prometheus → paste any query above**

---

### Logs (Loki)

In Grafana: **Explore → Loki**

```logql
# All logs from python-app
{service="python-app"}

# Only errors
{service="python-app"} |= "ERROR"

# Payment errors specifically
{service="python-app"} |= "payments" |= "ERROR"

# Error rate over time (metric query — switch to Metrics mode)
sum(rate({service="python-app"} |= "ERROR" [1m]))

# All containers — see everything
{container=~".+"}
```

---

### Traces (Tempo)

In Grafana: **Explore → Tempo → Search**

- Service Name: `python-app`
- Hit **Search** — you'll see all traces
- Click any trace → see the **waterfall view** (span tree)
- Click a span → see duration, attributes, parent/child relationship

**Pro tip:** In Loki, if a log line contains a `trace_id`, you can click it to jump directly to that trace in Tempo.

---

## Step 4 — Watch Alerts

```bash
# Watch the alert webhook (simulates PagerDuty receiving alerts)
docker logs alertwebhook -f
```

Visit **http://localhost:9090/alerts** — all alert rules and their current state.
Visit **http://localhost:9093** — Alertmanager UI.

---

## Step 5 — Break Things (The Real Learning)

Run these from the `labs/` directory. Each script breaks something specific.

### Scenario 1: Spike Error Rate
```bash
bash logs/break-scenarios/01-spike-errors.sh
```
**What fires:** `HighErrorRate` alert, `PaymentErrors` alert
**Where to watch:**
- `docker logs alertwebhook -f` → alerts arriving
- Grafana → Loki → `{service="python-app"} |= "ERROR"`
- Prometheus → http://localhost:9090/alerts

**What you'll see:** alert goes from `INACTIVE → PENDING → FIRING` over ~1 minute.

---

### Scenario 2: Kill the App
```bash
bash logs/break-scenarios/02-kill-app.sh
```
**What fires:** `AppDown` alert (critical)
**Key concept:** `inhibit_rules` — once AppDown fires, HighErrorRate and HighLatency alerts are **suppressed** automatically. No alert storm.

**To fix:**
```bash
docker compose start python-app
```
Watch the `RESOLVED` notification arrive in alertwebhook logs.

---

### Scenario 3: High Latency
```bash
bash logs/break-scenarios/03-high-latency.sh
```
**What fires:** `HighLatency` alert
**Where to watch:** Grafana → Explore → Prometheus
```promql
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))
```
Watch p99 climb above 1.0s on `/orders`.

---

### Fix Everything
```bash
bash logs/break-scenarios/00-fix-all.sh
```

---

## Step 6 — Build a Grafana Dashboard

Create your own dashboard to solidify the learning:

1. Grafana → **Dashboards → New → Add Visualization**
2. Select **Prometheus** datasource
3. Add these panels:

| Panel | Query | Visualization |
|-------|-------|--------------|
| Request Rate | `sum(rate(http_requests_total[5m])) by (endpoint)` | Time series |
| Error Rate % | `rate(http_requests_total{status="500"}[5m]) / rate(http_requests_total[5m]) * 100` | Gauge |
| p99 Latency | `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))` | Time series |
| App Up/Down | `up{job="python-app"}` | Stat |
| Error Logs | `{service="python-app"} \|= "ERROR"` (Loki) | Logs panel |

---

## Step 7 — Correlate Across Pillars

This is the **real SRE skill** — using all 3 pillars together.

**Scenario:** Payment errors are spiking. Walk through the investigation:

```
1. METRICS → you see error rate spike on /payments
   Query: rate(http_requests_total{status="500",endpoint="/payments"}[5m])

2. LOGS → filter for payment errors to see what's happening
   LogQL: {service="python-app"} |= "payments" |= "ERROR"
   → You see: "payment gateway timeout"

3. TRACES → click a trace_id from the log line
   → You see: payments-handler span took 2.3s, payment-service-call span timed out
   → Now you know EXACTLY which span is the bottleneck
```

---

## Tear Down

```bash
# Stop everything (keep volumes/data)
docker compose down

# Stop and DELETE all data (clean slate)
docker compose down -v
```

---

## Lab Directory Structure

```
labs/
├── docker-compose.yml
├── apps/
│   ├── python-app/
│   │   ├── app.py              # Flask app — metrics + logs + traces
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── load-generator/
│       ├── load_gen.py         # traffic generator
│       ├── alert_webhook.py    # simulated PagerDuty receiver
│       └── Dockerfile
├── infra/
│   ├── prometheus/
│   │   ├── prometheus.yml      # scrape config + alertmanager target
│   │   └── alert.rules.yml     # all alert rules
│   ├── alertmanager/
│   │   └── alertmanager.yml    # routing + inhibit rules
│   ├── loki/
│   │   └── loki-config.yaml
│   ├── promtail/
│   │   └── promtail-config.yaml
│   ├── tempo/
│   │   └── tempo-config.yaml
│   └── grafana/
│       └── provisioning/
│           └── datasources/
│               └── datasources.yaml  # all 3 datasources auto-configured
└── logs/
    └── break-scenarios/
        ├── 00-fix-all.sh
        ├── 01-spike-errors.sh
        ├── 02-kill-app.sh
        └── 03-high-latency.sh
```
