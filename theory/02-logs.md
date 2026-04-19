# Logs — Promtail + Loki + Grafana

## Overview

Logs capture the **detailed story of what happened** in your application — errors, events, user actions, service responses.

### Stack
```
[App Server + Promtail] → [Grafana Loki] → [Grafana]
```

> **Push mechanism** — unlike Prometheus which pulls, Promtail actively **pushes** logs to Loki.

**Alternatives:**
- Promtail → Fluentd, FluentBit
- Loki → Elasticsearch

---

## How It Works — Flow

```
1. Promtail watches log files on disk (e.g., /var/log/python-app/*.log)
2. Adds labels to each log line (job, host, etc.)
3. Pushes logs to Loki's HTTP API (localhost:3100/loki/api/v1/push)
4. Loki ingester buffers in memory → writes chunks to disk
5. Metadata (labels → chunk mapping) stored in BoltDB index
6. Grafana queries Loki → fetches logs from chunks using the index
```

---

## Loki

### Directory Structure

| Path | Purpose |
|------|---------|
| `/etc/loki` | Config file |
| `/var/lib/loki/index` | BoltDB index files (metadata) |
| `/var/lib/loki/chunks` | Actual log data |
| `/var/lib/loki/wal` | Write-ahead logs for durability |

### Configuration Explained (`/etc/loki-config.yaml`)

```yaml
auth_enabled: false        # no auth — any client can push/query
server:
  http_listen_port: 3100   # Loki HTTP port (Promtail and Grafana connect here)
```

**Ingester** — buffers logs in memory before writing to disk:
```yaml
ingester:
  chunk_idle_period: 5m    # close chunk if no new logs for 5 min
  max_chunk_age: 1h        # force flush chunk after 1 hour max
```

**Schema Config** — defines storage format:
```yaml
schema_config:
  configs:
    - from: 2025-09-23
      store: boltdb           # index/metadata in BoltDB
      object_store: filesystem # actual logs as files
      schema: v11
      index:
        prefix: index_
        period: 24h           # new index file every day
```

**Limits:**
```yaml
limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h   # reject logs older than 7 days
```

---

## Promtail

### What It Does

Promtail is the **log collection agent** that runs on your application servers. It:
- Watches specified log file paths
- Adds labels (job, host) to each log line
- Tracks its position in each file (`positions.yaml`) so logs aren't re-sent on restart
- Pushes log lines to Loki

### Configuration Explained (`/etc/promtail/config.yaml`)

```yaml
positions:
  filename: /tmp/positions.yaml    # tracks last read line per file

clients:
  - url: http://localhost:3100/loki/api/v1/push   # Loki endpoint
```

**Scrape configs — define what to collect:**

```yaml
scrape_configs:
  - job_name: python-app
    static_configs:
      - targets: [localhost]
        labels:
          job: python-app
          host: ${HOSTNAME}
          __path__: /var/log/python-app/*.log   # watch all .log files here
```

> Add a new `scrape_config` block for every log source you want to track (Apache, systemd journal, app logs, etc.)

---

## Test Scripts

### `logs-test-error.py` — Simulates RDS Connection Failures

Simulates 5 connection attempts to a dummy RDS instance, randomly succeeding or failing.

Writes to: `/var/log/python-app/app.log`

Sample log output:
```
2025-11-25 12:00:01 [INFO] [Attempt 1] Attempting to connect to RDS: host=dummy-db... port=3306
2025-11-25 12:00:03 [ERROR] [Attempt 1] Failed to connect to RDS: Connection timed out after 30 seconds.
```

---

### `logs-test-success.py` — Generates Random Number Logs

Generates 20 random numbers, logging even numbers as INFO and odd numbers as ERROR.

Writes to: `/var/log/python-app/app.log`

Sample log output:
```
2025-11-25 12:01:00 [INFO] [1] Random number: 42 (success)
2025-11-25 12:01:01 [ERROR] [2] Random number: 13 (error)
```

---

## LogQL — Querying Loki

LogQL is Loki's query language, similar to PromQL but for logs. You need this to build log dashboards and alerts in Grafana.

### Two Types of Queries

| Type | Purpose | Returns |
|------|---------|---------|
| **Log query** | Find and filter log lines | Raw log lines |
| **Metric query** | Count/rate logs over time | Numbers for graphing |

---

### Log Queries

**Basic label selector (required — always start with this):**
```logql
{job="python-app"}
```

**Filter by text (case-sensitive):**
```logql
{job="python-app"} |= "ERROR"
```

**Exclude lines containing a string:**
```logql
{job="python-app"} != "DEBUG"
```

**Regex filter:**
```logql
{job="python-app"} |~ "timeout|connection refused"
```

**Multiple filters chained:**
```logql
{job="python-app", host="server1"} |= "ERROR" != "healthcheck"
```

**Parse structured logs (key=value format):**
```logql
{job="python-app"} | logfmt | level="error"
```

**Parse JSON logs:**
```logql
{job="python-app"} | json | status_code="500"
```

---

### Metric Queries (for dashboards/alerts)

**Count of error log lines per minute:**
```logql
sum(rate({job="python-app"} |= "ERROR" [1m]))
```

**Count errors by host:**
```logql
sum by(host) (rate({job="python-app"} |= "ERROR" [5m]))
```

**Total log volume per job:**
```logql
sum by(job) (rate({job=~".+"}[5m]))
```

---

### Loki vs Elasticsearch

| Feature | Loki | Elasticsearch |
|---------|------|---------------|
| Indexing | Labels only (not full text) | Full text index |
| Storage cost | Low | High |
| Query speed | Fast for label-filtered queries | Fast for any text search |
| Best for | Kubernetes/cloud-native logs | Complex log analytics |
| Learning curve | Simple (like PromQL) | Steeper (EQL/KQL) |

> Loki is intentionally "log storage, not search engine" — it indexes *labels*, not log content. This keeps it cheap. If you need full-text search across all logs, use Elasticsearch.

---

## Viewing Logs in Grafana

```
Connections → Data Sources → Loki → URL: http://localhost:3100 → Save
Explore → Select Loki → Query: {job="python-app"} → Run
```

---

## Shell Script

`logs-tracings.sh` installs on the monitoring server:
- Grafana
- Loki
- Promtail
- Tempo (for traces)

---

## Key Concepts Summary

| Concept | Description |
|---------|-------------|
| Push vs Pull | Promtail **pushes** to Loki (unlike Prometheus which pulls) |
| Positions file | Tracks last read line so logs aren't duplicated on restart |
| Labels | Key-value pairs attached to logs for filtering in Grafana |
| Chunks | Batches of log lines stored on disk |
| BoltDB Index | Maps labels → chunk locations for fast lookup |
| Log path | Must be explicitly defined in Promtail config per application |