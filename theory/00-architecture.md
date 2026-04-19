# Observability & Monitoring - Architecture Overview

## SLI / SLO / SLA — The SRE Foundation

These three concepts are the **reason you're doing observability in the first place**. Everything — metrics, alerts, dashboards — exists to protect these commitments.

| Term | Full Name | Definition | Example |
|------|-----------|------------|---------|
| **SLI** | Service Level Indicator | A specific metric you measure to reflect service health | 99.2% of requests completed in under 300ms |
| **SLO** | Service Level Objective | The *target* you set for an SLI — your internal goal | 99.9% of requests must complete in under 300ms |
| **SLA** | Service Level Agreement | A *contract* with customers — breach = penalty/refund | "We guarantee 99.5% uptime or you get a refund" |

### How They Relate
```
SLI (what you measure) → compared against → SLO (your internal goal)
SLO is stricter than SLA so you have a buffer before breaching the customer contract
```

### Error Budget
When you define an SLO, you automatically get an **error budget** — the amount of allowed failure.

Example: SLO = 99.9% uptime over 30 days
- Total minutes in 30 days = 43,200
- Allowed downtime = 0.1% × 43,200 = **43.2 minutes**
- If you've used 40 minutes, your error budget is almost gone → freeze deployments, focus on reliability

> **SRE Rule:** When error budget is exhausted, reliability work takes priority over new features.

### Common SLIs to Track

| SLI Type | What to Measure |
|----------|----------------|
| Availability | `% of successful requests (non-5xx)` |
| Latency | `% of requests under Xms (e.g., p99 < 300ms)` |
| Error Rate | `% of requests returning errors` |
| Throughput | `requests per second the system handles` |
| Saturation | `% CPU / memory / disk used` |

---

## Monitoring vs Observability

| Term | Definition |
|------|-----------|
| **Monitoring** | Tells you **when** something is wrong in your system |
| **Observability** | Helps you understand **why** the issue occurs |

---

## The 3 Pillars

1. **Metrics** — numerical measurements over time (CPU, memory, request count)
2. **Logs** — detailed records of events and errors
3. **Traces** — end-to-end journey of a request across services

### Real-World Example: Payment Gateway Failure

- **Metrics** → spike in CPU/memory due to constant requests on the service
- **Logs** → which service is failing, error codes, what the user sent, what response it tried to give
- **Traces** → exact step-by-step trace of service-to-service calls showing *where* and *why* it failed

---

## Grafana

> Grafana is a **visualization board** — not just for metrics, but also for logs and traces.

---

## High-Level Architecture Flow

Each pillar follows the same pattern:

```
Application Server
  └── Agent (collects raw data)
        └── Backend (indexes, labels, timestamps, stores)
              └── Grafana (visualizes)
```

### Metrics
```
Server → Node Exporter → Prometheus (TSDB) → Grafana
```

### Logs
```
Server → Promtail → Grafana Loki → Grafana
         (alt: Fluentd, FluentBit)   (alt: Elasticsearch)
```

### Traces
```
Server → OpenTelemetry → Tempo → Grafana
         (alt: Jaeger)    (alt: Jaeger)
```

---

## What Lives on Each Server

Every application server has:
- The **application** itself
- **Agents** installed alongside it: Node Exporter, Promtail, OpenTelemetry

Agents are installed dynamically via **EC2 userdata** or baked into an **AMI**. Paths and ports are pre-configured.

---

## Tool Summary

| Tool | Role |
|------|------|
| Node Exporter | Collects node-level metrics (CPU, memory, disk) |
| Promtail | Collects and ships logs to Loki |
| OpenTelemetry | Collects and ships traces to Tempo |
| Prometheus | Pulls metrics, stores in TSDB |
| Grafana Loki | Receives and stores logs |
| Grafana Tempo | Receives and stores traces |
| Grafana | Unified visualization dashboard |
| Alertmanager | Groups, deduplicates, routes alerts |
| PagerDuty | Receives alert notifications and triggers on-call |