# Lab 01 — Metrics

**Stack:** Prometheus · Alertmanager · Grafana · Node Exporter · k6

**You will learn:**
1. How to verify scrape targets are healthy using `up`
2. How to read request rate and what a traffic drop means
3. How to calculate and alert on error rate %
4. How to read p99 latency from a histogram
5. The difference between `rate()` and `irate()` and when to use each
6. How to watch error budget drain in real time
7. How to trace an alert end-to-end: rule → Prometheus → Alertmanager → receiver

---

## Zero-trace design

No named volumes anywhere. All storage is `tmpfs` (RAM-backed):

| Service | Data path | Storage |
|---------|-----------|---------|
| Prometheus | `/prometheus` | tmpfs |
| Grafana | `/var/lib/grafana` | tmpfs |
| Alertmanager | `/alertmanager` | tmpfs |

`docker compose down` leaves nothing. No volumes to prune. No orphan data.

---

## Start the lab

```bash
cd lab-01-metrics
docker compose up -d
```

Wait 15 seconds, then verify all 4 services are running:

```bash
docker compose ps
```

Open these in your browser now — leave them open:

| UI | URL |
|----|-----|
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |
| Alertmanager | http://localhost:9093 |
| App | http://localhost:5000 |

---

## Step 1 — Verify scrape targets are healthy

**What:** Prometheus has a built-in `up` metric. `1` = scrape succeeded, `0` = target unreachable.

**Why:** Before you look at any application metric, you need to know if Prometheus can actually *reach* the thing it's monitoring. A missing target means all your dashboards are silently lying to you.

**How:**

Go to **Prometheus → Status → Targets** (http://localhost:9090/targets).

You should see 3 targets all `UP`:
- `flask-app` → your app on port 5000
- `node` → node-exporter on port 9100
- `prometheus` → Prometheus monitoring itself

Now run this in the Prometheus query box:

```promql
up
```

All values should be `1`. Now simulate a failure — stop the app:

```bash
docker compose stop app
```

Wait 30 seconds. Refresh the targets page. `flask-app` turns `DOWN`. Go to **Alerts** — `InstanceDown` is now `FIRING`. Also notice: `HighErrorRate` and `ErrorBudgetBurning` are **suppressed** by the inhibition rule (no point alerting on error rate when the whole instance is down).

Bring it back:

```bash
docker compose start app
```

> **SRE rule:** `up` is always your first dashboard panel. If it's red, everything else is noise.

---

## Step 2 — Generate traffic and watch request rate

**What:** `rate(http_requests_total[2m])` calculates requests per second, averaged over 2 minutes.

**Why:** Request rate is your throughput signal. A sudden drop means traffic stopped — that's often an outage. A sudden spike is either real load or a retry storm (a broken client hammering a dead endpoint).

**How:**

Open a second terminal and start the load generator:

```bash
docker compose run k6
```

k6 ramps: `5 → 15 → 30 → 10 → 0` VUs over ~4.5 minutes.

While it runs, go to **Grafana → Explore** (compass icon), select **Prometheus**, and run:

```promql
sum by(endpoint) (rate(http_requests_total[2m]))
```

You'll see a line per endpoint. Watch the spike when k6 hits 30 VUs. Watch it drop back down.

Now try a label filter — only show errors:

```promql
sum by(endpoint) (rate(http_requests_total{status="500"}[2m]))
```

> **SRE rule:** Set an alert on *zero* request rate for services that should always have traffic. Silence is a failure mode.

---

## Step 3 — Calculate error rate %

**What:** Error rate = (500 responses / all responses) × 100.

**Why:** This is what your SLO is built on. Raw error *count* is meaningless — 100 errors at 10,000 req/sec is 1%. 100 errors at 200 req/sec is 50%. Rate is what matters.

**How:**

In Prometheus or Grafana Explore, run:

```promql
sum(rate(http_requests_total{status="500"}[2m]))
/
sum(rate(http_requests_total[2m])) * 100
```

You'll see a number above 10% because `/error` always returns 500 and `/flaky` fails 40% of the time. This should have triggered the `HighErrorRate` alert.

Check **Prometheus → Alerts** (http://localhost:9090/alerts). You should see:
- `HighErrorRate` → FIRING
- `ErrorBudgetBurning` → FIRING

Now break it down by endpoint:

```promql
sum by(endpoint) (rate(http_requests_total{status="500"}[2m]))
/
sum by(endpoint) (rate(http_requests_total[2m])) * 100
```

`/error` will show 100%. `/flaky` will hover around 40%. The rest will be 0%.

> **SRE rule:** Never alert on error count. Alert on error rate. Always.

---

## Step 4 — Read p99 latency from a histogram

**What:** `histogram_quantile(0.99, ...)` computes the 99th percentile from the `_bucket` series. 99% of requests completed faster than this value.

**Why:** Averages lie. Average latency could be 50ms while 1% of users wait 3 seconds. SLOs target percentiles because every percentile point is a real user experience.

**How:**

Run this:

```promql
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint)
)
```

You'll see:
- `/`, `/users`, `/orders` → fast, under 200ms
- `/slow` → p99 shooting to 2+ seconds

The `le` label is the key — it's the "less than or equal" bucket boundary that `histogram_quantile` reads across to compute the percentile.

Now compare p50 vs p99 to see the spread:

```promql
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))
```

A large gap between p50 and p99 means high variance — some requests are much slower than others. That's a reliability problem even if the average looks fine.

> **SRE rule:** Define your SLO on p99. If p99 is good, 99% of your users are happy. Use p999 to find the extreme outliers.

---

## Step 5 — CPU saturation: rate() vs irate()

**What:** `irate()` uses only the last 2 data points — it reacts immediately to spikes. `rate()` averages across the full window — it gives a smoother trend.

**Why:** Using the wrong one costs you. `rate()` in an alert rule smooths out a real CPU spike and delays the page. `irate()` in a dashboard makes the graph jittery and hard to read.

**How:**

Run both side by side during the k6 spike (30 VUs):

```promql
# Smooth — use this in dashboards
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Fast-reacting — use this in alert rules
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

During the 30 VU spike, `irate()` will climb sharply and immediately. `rate()` will climb slowly and lag behind. Now check the alert rule in `prometheus/alerts.yml` — `HighCPU` uses `irate()`. That's intentional.

> **SRE rule:** `irate()` in alert rules. `rate()` in dashboards. Write this on a sticky note.

---

## Step 6 — Watch error budget drain

**What:** SLO = 99% success rate. Error budget = 1%. When error rate exceeds 1%, the budget is burning.

**Why:** Error budget is the mechanism that balances reliability work against feature work. When it's gone, you stop shipping features and fix reliability. Watching it drain makes this concrete.

**How:**

Run this — it shows how much error budget is remaining over the last 30 minutes:

```promql
100 - (
  sum(rate(http_requests_total{status="500"}[30m]))
  /
  sum(rate(http_requests_total[30m]))
  * 100
)
```

While k6 is running with `/error` traffic, this will drop well below 99%. That means the budget is burning.

In production this window would be 28 or 30 days. The lab compresses it to 30 minutes so you can watch it move in real time.

Now create a gauge panel in Grafana to visualise it:

1. **Grafana → Dashboards → New → Add visualisation**
2. Select **Prometheus** as datasource
3. Paste the query above
4. Change visualisation type to **Gauge**
5. Set thresholds: `0` = red, `98` = yellow, `99` = green
6. Title: `Error Budget Remaining %`
7. Save

> **SRE rule:** When error budget hits 0%, all new feature work stops. Reliability is the only priority until the budget recovers.

---

## Step 7 — Trace an alert end-to-end

**What:** The full alert pipeline: rule evaluation → PENDING → FIRING → Alertmanager → receiver.

**Why:** Most SREs inherit broken alert pipelines. Knowing what a healthy alert looks like at every stage lets you diagnose why one isn't arriving.

**How:**

**Stage 1 — Rule evaluation:**

Go to http://localhost:9090/alerts. You'll see alerts in three possible states:
- `inactive` — condition is false right now
- `pending` — condition is true but hasn't held for the `for` duration yet
- `firing` — condition has been true long enough, alert is sent to Alertmanager

Click on `HighErrorRate` and expand it. Note the labels and annotations — these are what get sent to Alertmanager and eventually to PagerDuty/Slack in production.

**Stage 2 — Alertmanager:**

Go to http://localhost:9093. You'll see alerts grouped by `alertname`. Click one to expand it. Note:
- Alerts with the same `alertname + instance` are grouped into one notification
- `inhibit_rules` are suppressing lower-severity alerts when a critical one is firing

**Stage 3 — Receiver logs:**

In this lab the receiver is the `/health` endpoint on the app (a dummy — we just need something that returns 200). The real insight is in Alertmanager's own debug logs:

```bash
docker logs lab01-alertmanager -f 2>&1 | grep -i "notify\|dispatch\|alert"
```

You'll see Alertmanager dispatching to the receiver, grouping delays, and repeat intervals.

**Stage 4 — Inhibition in action:**

Stop the app:

```bash
docker compose stop app
```

Wait 30s. Go to Alertmanager. `InstanceDown` is `ACTIVE`. `HighErrorRate` is **inhibited** — the label shows it. Restart the app:

```bash
docker compose start app
```

Wait 5 minutes. `InstanceDown` resolves. `HighErrorRate` becomes active again.

> **SRE rule:** Test your alert pipeline regularly. A firing alert that nobody receives is worse than no alert — it creates false confidence.

---

## Build your dashboard

Rather than loading a pre-built dashboard, build the key panels yourself. Each one takes 2 minutes.

Go to **Grafana → Dashboards → New → Add visualisation**.

| Panel | Query | Type |
|-------|-------|------|
| Target health | `up` | Stat |
| Request rate | `sum by(endpoint) (rate(http_requests_total[2m]))` | Time series |
| Error rate % | `sum(rate(http_requests_total{status="500"}[2m])) / sum(rate(http_requests_total[2m])) * 100` | Time series |
| p99 latency | `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))` | Time series |
| CPU usage | `100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` | Time series |
| Memory usage | `100 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100)` | Gauge |
| Error budget | `100 - (sum(rate(http_requests_total{status="500"}[30m])) / sum(rate(http_requests_total[30m])) * 100)` | Gauge |
| Active jobs | `app_active_jobs` | Time series |

Save the dashboard. This is your SRE golden signals view.

---

## Tear down

```bash
docker compose down
```

Verify nothing is left:

```bash
docker volume ls | grep lab01    # should be empty
docker ps -a | grep lab01        # should be empty
```

---

## PromQL reference

| What | Query |
|------|-------|
| Target health | `up` |
| Request rate per endpoint | `sum by(endpoint) (rate(http_requests_total[2m]))` |
| Error rate % | `sum(rate(http_requests_total{status="500"}[2m])) / sum(rate(http_requests_total[2m])) * 100` |
| p99 latency | `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))` |
| CPU usage % | `100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` |
| Memory usage % | `100 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100)` |
| Error budget remaining | `100 - (sum(rate(http_requests_total{status="500"}[30m])) / sum(rate(http_requests_total[30m])) * 100)` |
| Active jobs | `app_active_jobs` |
| Count of down instances | `count(up == 0)` |

---

→ **Next: Lab 02 — Logs** — same app, now we add Promtail + Loki and trace errors back to the exact log line that caused them.
