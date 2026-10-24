# sre-playground

Hands-on production observability labs covering the 3 pillars of SRE monitoring.
One Docker image. Four labs. Zero persistence: `docker compose down` leaves nothing behind.

---

## Architecture & Structure

```
sre-playground/
├── theory/               # Concepts before touching production infrastructure
│   ├── 00-architecture.md
│   ├── 01-metrics.md
│   ├── 02-logs.md
│   └── 03-traces.md
└── labs/                 # Self-contained Docker Compose telemetry testbeds
    ├── lab-01-metrics    # Prometheus + Alertmanager + Grafana (PromQL SLOs)
    ├── lab-02-logs       # Promtail + Loki + Grafana (LogQL structured logging)
    ├── lab-03-traces     # OpenTelemetry + Tempo + Grafana (Distributed waterfall tracing)
    └── lab-04-prod       # All 3 pillars integrated + live incident triage
```

---

## Production Observability Labs

| Lab | Stack | What You Learn & Verify |
| :--- | :--- | :--- |
| **01 - Metrics** | Prometheus + Alertmanager + Grafana | PromQL syntax, alert rules, error budgets, `rate()` vs `irate()`, cardinality guards |
| **02 - Logs** | Promtail + Loki + Grafana | LogQL parsing, label cardinality limits, log-to-metric aggregation queries |
| **03 - Traces** | OpenTelemetry Collector + Tempo + Grafana | Trace context propagation, spans, waterfall view, bottleneck identification |
| **04 - Prod** | All 3 Pillars Combined | Full incident loop: alert firing -> metric correlation -> log inspection -> trace root cause |

Each lab includes a detailed `README.md` walking through 5-7 real-world SRE scenarios with diagnostic workflows and postmortems.

---

## App Image

All four labs pull a standardized, pre-instrumented test application:

```bash
wizardxx7/sre-lab-app:1.0
```

Instrumented with Prometheus metrics, structured JSON logs, and OpenTelemetry traces. Tracing activates automatically when `OTLP_ENDPOINT` is configured.

---

## Execution Workflow

```bash
# Lab 01 - Metrics & Alerting
cd labs/lab-01-metrics && docker compose up -d && docker compose run k6

# Lab 02 - Structured Logging
cd labs/lab-02-logs    && docker compose up -d && docker compose run k6

# Lab 03 - Distributed Tracing
cd labs/lab-03-traces  && docker compose up -d && docker compose run k6

# Lab 04 - Production Incident Simulation
cd labs/lab-04-prod && docker compose up -d
docker compose run k6-normal
docker compose run k6-incident
```

Always run `docker compose down` before advancing to the next lab.

---

## Prerequisites

- Docker Engine & Docker Compose
- Host ports available: `3000`, `3100`, `3200`, `4317`, `4318`, `5000`, `9090`, `9093`, `9100`
