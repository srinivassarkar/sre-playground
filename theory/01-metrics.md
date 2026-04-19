# Metrics — Prometheus + Grafana + Alertmanager

## Overview

Metrics tell you the **state of your system** over time — CPU, memory, disk, request counts, etc.

### Stack
```
[App Server + Node Exporter] → [Prometheus] → [Grafana]
                                     ↓
                              [Alertmanager] → [PagerDuty / Slack / Email]
```

---

## Dynamic Discovery Problem (ASG)

In an Auto Scaling Group, EC2 instances get recreated and IPs change constantly.

**Solution:** Use **AWS EC2 Service Discovery** with tags instead of static IPs.

```yaml
ec2_sd_configs:
  - region: us-east-1
    port: 9100
    filters:
      - name: "tag:Name"
        values: ["node-server"]
```

Prometheus dynamically discovers all EC2s tagged `node-server` and scrapes them — no hardcoded IPs needed.

> **Alternative:** Use **Amazon CloudWatch + Grafana** instead of Prometheus + Grafana.

---

## Infrastructure Setup

| Server | What's on it |
|--------|-------------|
| server-1 (App Server) | Application + Node Exporter + Alertmanager |
| server-2 (Monitoring Server) | Prometheus (9090) + Grafana (3000) + Alertmanager + Node Exporter |

**IAM Role:** Attach EC2 admin rights to server-2 so Prometheus can use EC2 service discovery.

---

## How Prometheus Works — Step by Step

### Step 1: Scrape Metrics
Prometheus makes an HTTP `GET` to `/metrics` on each target (Node Exporter port `9100`).

Raw response from Node Exporter:
```
node_cpu_seconds_total{instance="server1", mode="idle"} 12345.67
node_memory_usage_bytes{instance="server1"} 567890
```

Prometheus parses these into **time series**: `metric + labels + timestamp + value`.

---

### Step 2: Store in TSDB

Prometheus stores all data in its built-in **Time Series Database (TSDB)**.

| Metric Name | Labels | Timestamp | Value |
|-------------|--------|-----------|-------|
| node_cpu_seconds_total | instance="server1", mode="idle" | 12:00 | 12345.7 |
| node_cpu_seconds_total | instance="server1", mode="idle" | 12:15 | 12346.1 |

- TSDB is **append-only** — new samples are just added sequentially
- Default retention: **15 days** (configurable, e.g., 90 days)
- Data stored on EBS volume at `/var/lib/prometheus/`

---

### Step 3: Evaluate Rules

At every `evaluation_interval` (default 15s), Prometheus evaluates rules:

**Alerting Rule Example:**
```yaml
- alert: HighCPUUsage
  expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 40
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "High CPU on {{ $labels.instance }}"
    description: "CPU > 40% for 2+ minutes. VALUE = {{ $value }}%"
```

**Recording Rule Example** (precomputes heavy queries for dashboards):
```yaml
- record: instance:cpu_usage:rate5m
  expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

---

### Step 4: Send Alerts to Alertmanager

Prometheus fires alerts → sends to Alertmanager via HTTP API.

Alertmanager handles:
- **Grouping** — combine related alerts
- **Deduplication** — don't send the same alert twice
- **Silencing** — mute during maintenance
- **Routing** — send to PagerDuty, Slack, email, etc.

---

### Step 5: Serve Metrics to Grafana

Grafana queries Prometheus via **PromQL** at `http://localhost:9090`.

```
connections → data sources → Prometheus → save → import dashboard
```

You can also connect CloudWatch directly as a Grafana data source:
```
connections → data source → CloudWatch → region → save → import dashboards
```

---

### Step 6: Repeat Continuously

```
Scrape every scrape_interval (15s)
Evaluate rules every evaluation_interval (15s)
Send alerts + update TSDB continuously
```

---

## PromQL — Querying Prometheus

PromQL is the query language you use in Grafana dashboards and Prometheus alerts. You need to know this to build anything useful.

### Metric Types

| Type | Description | Example |
|------|-------------|---------|
| **Counter** | Only goes up, resets on restart | `http_requests_total` |
| **Gauge** | Goes up and down | `node_memory_MemAvailable_bytes` |
| **Histogram** | Samples observations into buckets | `http_request_duration_seconds` |
| **Summary** | Like histogram but calculates quantiles client-side | `rpc_duration_seconds` |

---

### Essential PromQL Queries

**CPU Usage %**
```promql
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```
> `irate` = instant rate over last 2 data points in the window. Use for fast-moving counters.

**Memory Usage %**
```promql
100 - ((node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100)
```

**Disk Usage %**
```promql
100 - ((node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes{fstype!~"tmpfs|overlay"}) * 100)
```

**HTTP Request Rate (per second over 5m)**
```promql
rate(http_requests_total[5m])
```
> `rate` = average per-second rate over the window. Use for counters in dashboards.

**HTTP Error Rate %**
```promql
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) * 100
```

**p99 Latency (from histogram)**
```promql
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```
> `histogram_quantile(0.99, ...)` = 99th percentile — 99% of requests are faster than this value.

**Count of instances currently down**
```promql
count(up == 0)
```

**Top 5 memory-consuming instances**
```promql
topk(5, node_memory_MemAvailable_bytes)
```

---

### rate() vs irate()

| Function | Use When | Window |
|----------|----------|--------|
| `rate()` | Dashboards, smooth graphs, counters | wider window (5m, 15m) |
| `irate()` | Alerting, spikes, fast-moving counters | shorter window (1m, 5m) |

---

### Label Filtering

```promql
# exact match
node_cpu_seconds_total{instance="server1"}

# regex match
node_cpu_seconds_total{mode=~"idle|iowait"}

# exclude
node_cpu_seconds_total{mode!="idle"}
```

---

## TSDB Internals

### Chunks

A **chunk** is a small, contiguous block of consecutive metric samples stored on disk.

**Why chunks?**
- Writing each sample individually to disk is inefficient
- Chunks allow batch writes, compression, and fast sequential reads

**Example:** 5 scrapes of CPU usage stored in one chunk:

| Timestamp | Value |
|-----------|-------|
| 12:00 | 5 |
| 12:15 | 7 |
| 12:30 | 6 |
| 12:45 | 8 |
| 13:00 | 5 |

Key properties:
- One chunk = one time series only
- Append-only
- Has metadata: start time, end time
- Older chunks get **compacted** into larger chunks

---

### Index

The **index** maps `metric name + labels → chunk locations on disk`.

Without an index, Prometheus would have to scan ALL chunks to find data for `node_cpu_seconds_total{instance="server1"}` — extremely slow at scale.

**Flow:**
```
[Scrape metrics]
      ↓
[Time series samples] → stored in [chunks]
      ↓
[index] keeps track: metric+labels → chunk locations
      ↓
[PromQL query] → check index → load chunks → return samples
```

> **Analogy:** Chunks = pages of a notebook. Index = table of contents.

---

## Alert Rules Configured

| Alert | Condition | Severity |
|-------|-----------|----------|
| InstanceDown | `up == 0` for 1m | critical |
| HighCPUUsage | CPU > 40% for 2m | critical |
| UnauthorizedRequests | 401/403 responses in 5m | warning |
| HighDiskUsage | Disk > 80% for 2m | warning |

---

## Alertmanager — Routing Logic Deep Dive

Alertmanager is not just a notification forwarder. It's a **routing engine** with grouping, deduplication, silencing, and inhibition.

### Full Config Structure

```yaml
global:
  resolve_timeout: 5m

route:
  receiver: default-receiver       # fallback if no child route matches
  group_by: [alertname, instance]  # group alerts with same values together
  group_wait: 10s                  # wait before sending first notification (collect related alerts)
  group_interval: 5m               # wait before sending new alerts in same group
  repeat_interval: 1h              # how long before re-notifying if still firing

  routes:
    - match:
        severity: critical
      receiver: pagerduty           # critical → PagerDuty

    - match:
        severity: warning
      receiver: slack               # warnings → Slack

    - match:
        team: database
      receiver: db-team-email       # DB-specific alerts → DB team

receivers:
  - name: pagerduty
    pagerduty_configs:
      - routing_key: "<KEY>"
        severity: "critical"

  - name: slack
    slack_configs:
      - api_url: "https://hooks.slack.com/services/..."
        channel: "#alerts"
        text: "Alert: {{ .CommonAnnotations.summary }}"

  - name: db-team-email
    email_configs:
      - to: "db-team@company.com"
        from: "alerts@company.com"
        smarthost: "smtp.company.com:587"

inhibit_rules:
  - source_match:
      severity: critical
    target_match:
      severity: warning
    equal: [instance]
    # if critical fires for an instance, suppress warnings for same instance
```

### Key Concepts

| Concept | What it does |
|---------|-------------|
| `group_by` | Groups alerts with matching label values into one notification |
| `group_wait` | Buffer time to collect related alerts before sending (avoid alert storms) |
| `group_interval` | Cooldown before adding new alerts to an existing group notification |
| `repeat_interval` | Re-notify if alert is still firing after this duration |
| `inhibit_rules` | Suppress lower-priority alerts when a higher-priority one is firing for the same target |
| `silences` | Manually mute alerts for a time window (e.g., during planned maintenance) |

### Routing Decision Tree
```
Incoming alert
      ↓
Does it match any child route?
  YES → use that receiver
  NO  → use root receiver (default-receiver)
```

> **Real-world pattern:** Use `inhibit_rules` to silence `HighMemory` warnings when `InstanceDown` is already firing for the same instance — no point alerting on memory when the whole server is down.

---

## PagerDuty Integration

1. Create a service in PagerDuty with default settings
2. Get the **Integration Key** (routing key)
3. Add to `alertmanager.yml`:

```yaml
route:
  receiver: pagerduty
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h

receivers:
  - name: pagerduty
    pagerduty_configs:
      - routing_key: "<YOUR_INTEGRATION_KEY>"
        severity: "critical"
```

> You can trigger PagerDuty alerts from **both Prometheus and Grafana** — you can eliminate one if needed.

---

## Shell Scripts

| Script | Purpose | Run on |
|--------|---------|--------|
| `server2-setup.sh` | Installs Prometheus + Grafana + Alertmanager + Node Exporter | server-2 |
| `server1-setup.sh` | Installs Alertmanager + Node Exporter | server-1 |

---

## Prometheus Analogy

> Prometheus is like a **watchful scientist**:
> - **Measures** everything periodically (scraping)
> - **Records** observations in a notebook (TSDB)
> - **Checks** if conditions are dangerous (alert rules)
> - **Calls** a responder if something is wrong (Alertmanager)
> - **Shares** results with observers (Grafana)