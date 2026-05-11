# Lab 04 — Production

**Stack:** Prometheus · Alertmanager · Loki · Promtail · Tempo · Grafana

This is the complete observability stack. All three pillars run together.
The lab simulates a realistic production incident and walks you through
the full SRE investigation loop: alert → metrics → logs → traces → root cause.

---

## The Incident

> **Scenario:** It is 14:32 on a Tuesday. PagerDuty fires.  
> Alert: `SLOBurnRateCritical` — error budget burning 14x faster than allowed.  
> You have no idea what changed. The investigation starts now.

Your job is to find:
1. Which endpoint is failing
2. What type of error it is
3. Which internal operation is the root cause
4. How long it has been happening

---

## How the pillars work together

```
Alert fires (Prometheus)
    ↓
You open Grafana — which endpoint has the highest error rate? (Metrics)
    ↓
Filter logs for that endpoint — what error type is appearing? (Logs)
    ↓
Copy trace_id from a log line — open the waterfall (Traces)
    ↓
Find the red span — that is your root cause
```

This is the real SRE investigation loop. Each pillar answers one question:

| Pillar | Question it answers |
|--------|-------------------|
| Metrics | When did it start? How bad is it? Which endpoint? |
| Logs | What is the error message? What fields tell the story? |
| Traces | Which internal operation failed? Where exactly in the call chain? |

---

## Zero-trace design

| Service | Data path | Storage |
|---------|-----------|---------|
| Prometheus TSDB | `/prometheus` | tmpfs |
| Loki chunks | `/loki` | tmpfs |
| Tempo traces | `/var/tempo` | tmpfs |
| Grafana state | `/var/lib/grafana` | tmpfs |
| Alertmanager | `/alertmanager` | tmpfs |

`docker compose down` leaves nothing.

---

## Start the lab

```bash
cd lab-04-prod
docker compose up -d
```

Wait 30 seconds — more services to initialise this time.

```bash
docker compose ps
```

All 8 services should be `Up`. If Tempo or Loki take longer, wait another 15 seconds and check again.

Verify tracing is active:
```bash
docker logs lab04-app | grep -i "tracing"
# Expected: {"message": "Tracing enabled", "otlp_endpoint": "http://tempo:4318"}
```

Open all of these now — you will need them during the investigation:

| UI | URL | Purpose |
|----|-----|---------|
| Grafana | http://localhost:3000 | Main investigation tool |
| Prometheus | http://localhost:9090 | Raw metric queries + alert state |
| Alertmanager | http://localhost:9093 | Alert routing + grouping |

---

## Phase 1 — Establish a baseline (5 minutes)

**Why:** You cannot spot an anomaly without knowing what normal looks like.
Every SRE investigation starts with baseline context.

Start normal traffic:

```bash
docker compose run k6-normal
```

While it runs, go to **Grafana → Explore** and build a mental picture of normal:

**Normal request rate:**
```promql
sum by(endpoint) (rate(http_requests_total[1m]))
```

**Normal error rate (should be near 0%):**
```promql
sum(rate(http_requests_total{status="500"}[2m])) / sum(rate(http_requests_total[2m])) * 100
```

**Normal p99 latency:**
```promql
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[2m])) by (le, endpoint))
```

**Normal log volume:**
```logql
sum by(level) (rate({job="sre-lab-app"}[1m]))
```

Memorise or screenshot these baselines. You'll compare against them during the incident.

---

## Phase 2 — The incident begins

Open a second terminal. While k6-normal is still running (or just after it finishes), start the incident:

```bash
docker compose run k6-incident
```

Watch Alertmanager for alerts firing:

```bash
docker logs lab04-alertmanager -f 2>&1 | grep -i "level=info"
```

Also watch Prometheus alerts page: http://localhost:9090/alerts

Within 2 minutes you should see:
- `HighErrorRate` → FIRING
- `ErrorBudgetBurning` → FIRING
- `HighP99Latency` → FIRING
- `SLOBurnRateCritical` → FIRING (the serious one)

---

## Phase 3 — Investigation: Metrics first

**Step 1 — How bad is it?**

```promql
sum(rate(http_requests_total{status="500"}[2m])) / sum(rate(http_requests_total[2m])) * 100
```

You'll see a number well above 10%. Compare to your baseline (near 0%). That's the magnitude of the incident.

**Step 2 — Which endpoint is responsible?**

```promql
sum by(endpoint) (rate(http_requests_total{status="500"}[2m]))
/
sum by(endpoint) (rate(http_requests_total[2m])) * 100
```

One or two endpoints will stand out with high error rates. Note them.

**Step 3 — When did it start?**

Zoom out the Grafana time range to the last 30 minutes. Find the exact minute the error rate spiked. This tells you what to look for in logs.

**Step 4 — Is latency affected too?**

```promql
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))
```

If `/slow` p99 has climbed past 1s and `/flaky` is also elevated, you have both a latency and error rate problem — two separate issues or one common root cause.

**Step 5 — Error budget status:**

```promql
100 - (
  sum(rate(http_requests_total{status="500"}[30m]))
  / sum(rate(http_requests_total[30m]))
  * 100
)
```

This tells you how much budget you have left and how urgently you need to act.

> **At this point you know:** error rate is high, which endpoints are affected, when it started, and how fast the budget is burning. Now you need to know *what* the error is.

---

## Phase 4 — Investigation: Logs second

Switch to **Grafana → Explore → Loki**.

**Step 1 — Filter for errors on the affected endpoint.**

Replace `/flaky` with whichever endpoint your metrics identified:

```logql
{job="sre-lab-app", level="ERROR", endpoint="/flaky"}
```

Scroll through the log lines. You'll see repeated entries like:
```json
{"level": "ERROR", "message": "Upstream dependency failed", "error_type": "DependencyError", "upstream": "payment-service", "trace_id": "abc123..."}
```

**Step 2 — Confirm the error type and upstream.**

```logql
{job="sre-lab-app", level="ERROR"} | json | line_format "{{.error_type}} | upstream={{.upstream}} | endpoint={{.endpoint}}"
```

This reshapes the log output to show only what matters. You'll see `DependencyError | upstream=payment-service` repeating — that's your signal.

**Step 3 — How often is this error occurring?**

```logql
sum by(endpoint) (rate({job="sre-lab-app", level="ERROR"}[1m]))
```

Compare this rate to your baseline log volume. The jump is the incident.

**Step 4 — Are there any WARNING logs that preceded the ERRORs?**

```logql
{job="sre-lab-app", level="WARNING"} | json | line_format "{{.message}} | {{.endpoint}}"
```

You'll see slow query warnings mixed in. Check if they started before the errors — slow queries under load can cascade into timeouts and then errors.

**Step 5 — Grab a trace_id.**

Click on any ERROR log line in Grafana. Expand it. Find the `trace_id` field. Click **"View trace in Tempo"** — Grafana jumps directly to the trace waterfall using the correlation link configured in `datasources.yml`.

> **At this point you know:** the error is a `DependencyError` from `payment-service` upstream. You know it started at a specific time. Now you need to see exactly which internal operation failed inside the request.

---

## Phase 5 — Investigation: Traces last

You're now in **Grafana → Explore → Tempo**, looking at the waterfall for the trace you just jumped to from the log line.

**Step 1 — Read the waterfall.**

```
GET /flaky                     ERROR    ~280ms
  └── flaky-handler            ERROR    ~280ms
        └── upstream-call      ERROR    ~250ms   ← root cause span
```

The `upstream-call` span is red. That's where the failure originated. The parent spans are red because the error propagated up.

**Step 2 — Click the upstream-call span.**

Expand the span attributes:
- `http.status_code`: 500
- `otel.status_code`: ERROR
- Duration: ~250ms — it didn't time out instantly, it ran and then failed

**Step 3 — Compare with a successful trace.**

Go back to Tempo Search, find a successful `/flaky` trace (Status: OK). Open it. The `upstream-call` span is green. Same structure, same duration range, different outcome. The code path is identical — the failure is intermittent at the upstream, not a code bug.

**Step 4 — Check the slow traces too.**

Search for service `sre-lab-app`, min duration `800ms`. Open a `/slow` trace:

```
GET /slow                      OK       ~1.4s
  └── slow-handler             OK       ~1.4s
        └── db-query-slow      OK       ~1.3s   ← 93% of request time
```

The DB query is the bottleneck for latency. This is a separate issue from the dependency errors — two problems happening simultaneously during the incident.

**Step 5 — Use Tempo's "Logs for this span" button.**

Click any span. Look for the **"Logs"** button in the span detail panel. Grafana queries Loki for log lines with the matching `trace_id` and shows them alongside the trace. This is the full correlation — one click from a trace span to the exact log lines generated during that request.

> **Root cause found:**  
> **Error:** `upstream-call` span in `/flaky` failing intermittently — payment-service dependency is unstable.  
> **Latency:** `db-query-slow` span in `/slow` — DB query taking 800ms–2.5s, unrelated to the errors.  
> **Action:** Page the payment-service team. File a latency ticket for the slow DB query. Watch error budget recovery as the dependency stabilises.

---

## Phase 6 — Build the production dashboard

This is the dashboard you'd have open during any incident. Build it panel by panel.

**Grafana → Dashboards → New → Add visualisation**

Row 1 — Golden Signals:

| Panel | Query | Type |
|-------|-------|------|
| Request rate | `sum by(endpoint) (rate(http_requests_total[2m]))` | Time series |
| Error rate % | `sum(rate(http_requests_total{status="500"}[2m])) / sum(rate(http_requests_total[2m])) * 100` | Time series |
| p99 latency | `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))` | Time series |
| Error budget | `100 - (sum(rate(http_requests_total{status="500"}[30m])) / sum(rate(http_requests_total[30m])) * 100)` | Gauge |

Row 2 — Saturation:

| Panel | Query | Type |
|-------|-------|------|
| CPU usage | `100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` | Time series |
| Memory usage | `100 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100)` | Gauge |
| Active jobs | `app_active_jobs` | Time series |

Row 3 — Logs (switch datasource to Loki):

| Panel | Query | Type |
|-------|-------|------|
| Error log stream | `{job="sre-lab-app", level="ERROR"}` | Logs |
| Error rate from logs | `sum by(endpoint) (rate({job="sre-lab-app", level="ERROR"}[1m]))` | Time series |
| Log volume by level | `sum by(level) (rate({job="sre-lab-app"}[1m]))` | Time series |

Save as `Lab 04 — Production`.

During the incident phase, all three rows tell the story simultaneously:
- Row 1 shows the error rate spike and budget drain
- Row 2 shows if the system is also under resource pressure
- Row 3 shows the exact error messages as they happen

---

## Tear down

```bash
docker compose down
```

Verify nothing remains:
```bash
docker volume ls | grep lab04    # empty
docker ps -a | grep lab04        # empty
```

---

## The full investigation loop — summary

```
Alert fires
    ↓
Metrics  →  which endpoint? how bad? when did it start?
    ↓
Logs     →  what is the error? what upstream? what error_type?
    ↓
Traces   →  which span failed? where in the call chain?
    ↓
Root cause identified → page the right team → watch recovery
```

Each pillar is useless alone. Together they give you the full picture in minutes instead of hours.

---

## What you have built across all 4 labs

```
lab-01-metrics   Prometheus + Alertmanager + Grafana
                 → learned: scraping, PromQL, alert rules, error budget

lab-02-logs      Promtail + Loki + Grafana
                 → learned: LogQL, label cardinality, log volume alerting

lab-03-traces    OpenTelemetry + Tempo + Grafana
                 → learned: spans, waterfall, bottleneck identification

lab-04-prod      All 3 pillars + correlation + incident investigation
                 → learned: the full SRE investigation loop end to end
```

The image `wizardxx7/sre-lab-app:1.0` ran in all 4 labs unchanged.
The only difference between labs was which backends were wired up.
That is how real observability stacks work.
