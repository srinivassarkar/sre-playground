# Lab 02 — Logs

**Stack:** Promtail · Loki · Grafana

**You will learn:**
1. How logs flow from your app through Docker → Promtail → Loki → Grafana
2. How to tail live logs and filter by label in Grafana Explore
3. How to search log content with LogQL (`|=`, `!=`, `|~`)
4. How to count error rate over time from logs (metric queries)
5. How to correlate a metrics spike to the exact log line that caused it
6. What log volume anomaly looks like — and why silence is an alert
7. Why label cardinality matters and what breaks when you get it wrong

---

## How logs flow in this lab

```
app stdout (JSON)
    ↓
Docker log driver
    ↓  writes to /var/lib/docker/containers/<id>/<id>-json.log
Promtail
    ↓  reads file, parses JSON, adds labels, pushes via HTTP POST
Loki
    ↓  indexes labels, stores log chunks in /loki (tmpfs)
Grafana
       queries via LogQL
```

The key difference from Lab 01: **Promtail pushes, Prometheus pulls.**
Prometheus goes to the app and asks for metrics. Promtail watches a file
and sends logs to Loki without being asked.

---

## Zero-trace design

| Service | Data path | Storage |
|---------|-----------|---------|
| Loki | `/loki` | tmpfs |
| Grafana | `/var/lib/grafana` | tmpfs |
| Promtail positions | `/tmp/positions.yaml` | tmpfs |

`docker compose down` leaves nothing. Positions reset on restart — fine for a lab, use a persistent path in production so logs aren't re-shipped.

---

## Start the lab

```bash
cd lab-02-logs
docker compose up -d
```

Wait 20 seconds (Loki takes a moment to initialise), then verify:

```bash
docker compose ps
```

All 4 services should be `Up`. Check Promtail is shipping logs:

```bash
docker logs lab02-promtail -f
```

You should see Promtail discovering `lab02-app` and tailing its log file.

Open these and leave them open:

| UI | URL |
|----|-----|
| Grafana | http://localhost:3000 |
| Loki API | http://localhost:3100/ready |

---

## Step 1 — Understand how logs get from stdout to Loki

**What:** Before you query anything, trace the path a single log line takes from the app to Grafana.

**Why:** When logs aren't showing up, you need to know exactly which step in the pipeline broke. Is the app logging? Is Docker capturing it? Is Promtail reading it? Is Loki receiving it?

**How:**

**Step 1a — The app logs to stdout:**

```bash
docker logs lab02-app -f
```

You'll see structured JSON on every line:
```json
{"timestamp": "2026-05-10T18:00:01Z", "level": "INFO", "message": "200 GET /", "endpoint": "/", "status": 200, "duration": 0.012}
```

This is the raw output. Docker captures it automatically.

**Step 1b — Docker writes it to disk:**

```bash
sudo ls /var/lib/docker/containers/$(docker inspect lab02-app --format '{{.Id}}')/
```

You'll see a `*-json.log` file. That's what Promtail reads.

**Step 1c — Check Loki received it:**

```bash
curl -s "http://localhost:3100/loki/api/v1/labels" | python3 -m json.tool
```

You should see labels including `job`, `container`, `level`, `endpoint`. If this returns an empty list, Promtail hasn't shipped anything yet — check its logs.

**Step 1d — Query it in Grafana:**

Go to **Grafana → Explore**, select **Loki**, and run:

```logql
{job="sre-lab-app"}
```

You should see log lines flowing in. If not, generate some traffic first:

```bash
curl localhost:5000/
curl localhost:5000/users
curl localhost:5000/error
```

> **SRE rule:** When logs are missing, walk the pipeline. App → Docker → Promtail → Loki → Grafana. The break is always at one specific step.

---

## Step 2 — Tail live logs and filter by label

**What:** LogQL always starts with a label selector `{label="value"}`. Labels are indexed — they're fast. Log content is not indexed — it's slower to search.

**Why:** Loki's design philosophy is "label first, content second". This keeps storage cheap. In Elasticsearch you'd search free text immediately. In Loki you always narrow by labels first.

**How:**

Start the load generator in a second terminal:

```bash
docker compose run k6
```

Now in Grafana Explore, try these label selectors one by one and observe the results:

**All logs from the app:**
```logql
{job="sre-lab-app"}
```

**Only ERROR logs:**
```logql
{job="sre-lab-app", level="ERROR"}
```

**Only a specific endpoint:**
```logql
{job="sre-lab-app", endpoint="/slow"}
```

**Multiple label values using regex:**
```logql
{job="sre-lab-app", level=~"ERROR|WARNING"}
```

Notice how filtering by `level` and `endpoint` is instant — these are indexed labels. Now try the same with content filtering (next step) and feel the difference.

> **SRE rule:** Put things you filter on constantly (level, service, env, team) as labels. Put high-cardinality things (trace_id, user_id, request_id) as log fields, not labels.

---

## Step 3 — Search log content with LogQL

**What:** After selecting by label, you filter log line *content* with pipeline stages: `|=` (contains), `!=` (not contains), `|~` (regex match).

**Why:** Labels cover the broad category. Content filtering finds the specific event inside that category. Together they let you go from "show me all errors" to "show me errors on /flaky that mention payment-service".

**How:**

**Find lines containing a specific string:**
```logql
{job="sre-lab-app"} |= "DependencyError"
```

**Exclude lines you don't want:**
```logql
{job="sre-lab-app", level="ERROR"} != "werkzeug"
```

**Regex — match multiple patterns:**
```logql
{job="sre-lab-app"} |~ "timeout|DependencyError|InternalServerError"
```

**Parse the JSON fields and filter on a parsed value:**
```logql
{job="sre-lab-app"} | json | duration > 1.0
```

This last one is powerful — it parses the JSON log line and lets you filter on any field value. Find all requests that took longer than 1 second:

```logql
{job="sre-lab-app"} | json | duration > 1.0
```

Find all 500 responses with a duration over 0.1s:
```logql
{job="sre-lab-app"} | json | status = 500 | duration > 0.1
```

> **SRE rule:** `| json` is your sharpest tool in Loki. Once fields are parsed, you can filter, format, and compute on any value in the log line.

---

## Step 4 — Count error rate over time from logs

**What:** LogQL can produce metrics from logs using `rate()` and `count_over_time()`. This lets you graph error frequency, alert on it, and compare it against your Prometheus metrics.

**Why:** Sometimes you don't have a Prometheus counter for a specific error type, but you have a log line for it. Loki metric queries let you turn those log lines into a time series without changing the application code.

**How:**

**Count of ERROR lines per minute:**
```logql
sum(rate({job="sre-lab-app", level="ERROR"}[1m]))
```

**Count errors broken down by endpoint:**
```logql
sum by(endpoint) (rate({job="sre-lab-app", level="ERROR"}[1m]))
```

**Rate of slow query warnings:**
```logql
sum(rate({job="sre-lab-app"} |= "Slow query detected" [1m]))
```

**Total log volume by level — useful for spotting anomalies:**
```logql
sum by(level) (rate({job="sre-lab-app"}[1m]))
```

Switch the panel type to **Time series** in Grafana Explore to see these as graphs. You'll see `/error` driving a flat ERROR line and `/slow` driving a WARNING line that spikes during the k6 load test.

> **SRE rule:** You don't always need to instrument a new metric counter. If you already have the log line, Loki metric queries give you the time series for free.

---

## Step 5 — Correlate a metrics spike to a log line

**What:** When you see an anomaly in a metric (error rate spike, latency jump), the next step is finding the log line that explains it. This is the most common SRE investigation workflow.

**Why:** Metrics tell you *something is wrong*. Logs tell you *what exactly went wrong*. The skill is pivoting between them fast.

**How:**

This exercise simulates a real investigation.

**Observation:** Error rate has spiked (you saw this in Lab 01).

**Step 1 — Narrow the time window.** In Grafana Explore, zoom into the time period where the spike happened. Both Loki and Prometheus respect the time range selector.

**Step 2 — Filter for errors in that window:**
```logql
{job="sre-lab-app", level="ERROR"}
```

**Step 3 — Identify the error type from the log fields:**
```logql
{job="sre-lab-app", level="ERROR"} | json | line_format "{{.error_type}} on {{.endpoint}}"
```

`line_format` lets you reshape the log line output to show only the fields you care about.

**Step 4 — Find how often each error type appears:**
```logql
sum by(endpoint) (count_over_time({job="sre-lab-app", level="ERROR"}[5m]))
```

**Step 5 — Pinpoint the exact log line.** Click on any log line in Grafana. Expand it. You'll see all parsed JSON fields: `endpoint`, `error_type`, `duration`, `trace_id`.

The `trace_id` field is there in every error log (when tracing is on in Labs 03+04 it becomes a clickable link to Tempo). For now, note it's present and would let you jump to the full request trace.

> **SRE rule:** Metrics → alert → logs → trace. That's the investigation loop. Each pillar answers a different question: metrics say *when*, logs say *what*, traces say *where*.

---

## Step 6 — Log volume anomaly — silence is an alert

**What:** A sudden drop in log volume is as serious as a spike. If your app normally logs 50 lines/minute and suddenly logs 0, it's either crashed or stopped receiving traffic.

**Why:** Most people alert on errors. Fewer people alert on missing logs. But a silent app is often a dead app.

**How:**

First, establish a baseline. With k6 running, check log volume:
```logql
sum(rate({job="sre-lab-app"}[1m]))
```

Note the number — it'll be around 10–20 lines/second.

Now stop the app:
```bash
docker compose stop app
```

Re-run the same query. Volume drops to 0. In production, this is where you'd have a Loki alert rule:

```yaml
# Example Loki alert rule (not wired up in this lab — illustrative)
- alert: LogVolumeDrop
  expr: |
    sum(rate({job="sre-lab-app"}[5m])) < 0.1
  for: 2m
  annotations:
    summary: "sre-lab-app has stopped logging — possible crash or traffic loss"
```

Restart the app and watch volume recover:
```bash
docker compose start app
```

Also look for the opposite — a sudden *spike* in log volume. Run this to watch volume by level in real time:
```logql
sum by(level) (rate({job="sre-lab-app"}[30s]))
```

During the k6 30 VU spike, ERROR volume climbs noticeably. That's your signal.

> **SRE rule:** Alert on log volume, not just log content. `rate({job="your-service"}[5m]) < threshold` catches silent failures that no error log will ever surface.

---

## Step 7 — Label cardinality — what breaks Loki when you get it wrong

**What:** Loki indexes labels, not log content. Each unique combination of label values is a **stream**. Too many streams = high cardinality = Loki slows down or crashes.

**Why:** This is the most common Loki mistake in production. Someone adds `trace_id` or `user_id` as a label. Millions of unique values. Millions of streams. Loki falls over.

**How:**

Look at the Promtail config (`promtail/config.yml`). In the pipeline stages, these fields are promoted to labels:

```yaml
- labels:
    level:    ""     # 4 values: DEBUG, INFO, WARNING, ERROR
    endpoint: ""     # ~8 values: /, /users, /orders, /slow, /error, /flaky, /login, /metrics
```

And `trace_id` is deliberately NOT a label — it stays as a log field.

**Why trace_id can't be a label:**

Every request has a unique `trace_id`. If it were a label, Loki would create one new stream per request. A service doing 100 req/sec creates 100 new streams per second = 360,000 new streams per hour = Loki out of memory.

**Check how many streams you currently have:**
```bash
curl -s "http://localhost:3100/loki/api/v1/series" \
  -d 'match[]={job="sre-lab-app"}' | python3 -m json.tool | grep -c "stream"
```

With only `level` and `endpoint` as labels, this stays small (around 20–30 streams max). If you added `trace_id` as a label it would grow without bound.

**The rule:**
- Labels: things you filter on, low cardinality (env, level, service, endpoint, team)
- Log fields: everything else (trace_id, user_id, request_id, payload content)

> **SRE rule:** Every label you add multiplies your stream count. Think "how many unique values can this label have?" before adding it. If the answer is "millions", it's a log field, not a label.

---

## Build your log dashboard

Go to **Grafana → Dashboards → New → Add visualisation**, select **Loki**.

| Panel | Query | Type |
|-------|-------|------|
| Live log stream | `{job="sre-lab-app"}` | Logs |
| Error logs only | `{job="sre-lab-app", level="ERROR"}` | Logs |
| Error rate over time | `sum(rate({job="sre-lab-app", level="ERROR"}[1m]))` | Time series |
| Log volume by level | `sum by(level) (rate({job="sre-lab-app"}[1m]))` | Time series |
| Slow queries | `{job="sre-lab-app"} \|= "Slow query detected"` | Logs |
| Errors by endpoint | `sum by(endpoint) (rate({job="sre-lab-app", level="ERROR"}[1m]))` | Time series |

Save as `Lab 02 — Logs`.

---

## Tear down

```bash
docker compose down
```

Verify:
```bash
docker volume ls | grep lab02   # empty
docker ps -a | grep lab02       # empty
```

---

## LogQL reference

| What | Query |
|------|-------|
| All app logs | `{job="sre-lab-app"}` |
| Error logs | `{job="sre-lab-app", level="ERROR"}` |
| Content search | `{job="sre-lab-app"} \|= "DependencyError"` |
| Exclude content | `{job="sre-lab-app"} != "werkzeug"` |
| Regex match | `{job="sre-lab-app"} \|~ "timeout\|DependencyError"` |
| Parse JSON fields | `{job="sre-lab-app"} \| json \| duration > 1.0` |
| Error rate/min | `sum(rate({job="sre-lab-app", level="ERROR"}[1m]))` |
| Volume by level | `sum by(level) (rate({job="sre-lab-app"}[1m]))` |
| Errors by endpoint | `sum by(endpoint) (count_over_time({job="sre-lab-app", level="ERROR"}[5m]))` |
| Reshape output | `{job="sre-lab-app"} \| json \| line_format "{{.error_type}} on {{.endpoint}}"` |

---

→ **Next: Lab 03 — Traces** — same app, now we add OpenTelemetry + Tempo and see the full request journey across service spans.
