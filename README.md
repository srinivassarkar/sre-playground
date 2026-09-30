# sre-playground

Hands-on observability labs covering the 3 pillars of SRE monitoring.
One Docker image. Four labs. Zero persistence — `docker compose down` leaves nothing.

---

## Structure

```
sre-playground/
├── theory/          # concepts before you touch anything
├── labs/
│   ├── lab-01-metrics    # Prometheus · Alertmanager · Grafana
│   ├── lab-02-logs       # Promtail · Loki · Grafana
│   ├── lab-03-traces     # OpenTelemetry · Tempo · Grafana
│   └── lab-04-prod       # All 3 pillars · full incident investigation
├── inference-labs/  # 4 hands-on production inference engineering labs
├── sysde-prep/      # Amazon SysDE / Apple SRE triage drills & cheat sheets
│   ├── 01-step1-linux-diagnostics-cheat-sheet.md
│   ├── 02-step2-faang-incident-triage-playbook.md
│   └── 03-step3-python-systems-scripting-drills.py
└── interviewQs/     # 65 master SRE interview questions
```

---

## Level 1: Production Observability Labs

| Lab | Stack | What you learn |
|-----|-------|---------------|
| 01 — Metrics | Prometheus + Alertmanager | PromQL, alert rules, error budget, rate() vs irate() |
| 02 — Logs | Promtail + Loki | LogQL, label cardinality, log→metric queries |
| 03 — Traces | OpenTelemetry + Tempo | Spans, waterfall view, bottleneck identification |
| 04 — Prod | All 3 combined | Full incident loop: alert → metrics → logs → traces |

Each lab has a `README.md` that walks you through 5–7 SRE scenarios with what, why, and how for every step.

---

## Level 2: AI Infrastructure & LLM Inference Labs (`inference-labs/`)

Blueprint: **[Level-2: AI Infrastructure & Systems Engineering Blueprint](inference-labs/LEVEL-2-AI-INFRA-BLUEPRINT.md)**

| Lab | Focus | Silicon & Systems Verification |
|-----|-------|--------------------------------|
| 01 — VRAM Budgeting | Memory Topology & GQA | Predicted 1,412 MiB $\implies$ measured 1,418 MiB on GTX 1050 Ti (99.6% accuracy). Measured +836 MiB context expansion at 32K context. |
| 02 — Serving Daemons | Supervisors & Layer Offload | Standardized on `/v1/chat/completions`. Proved automated `systemd` recovery from `kill -9` in 3 seconds. |
| 03 — Streaming Telemetry | Latency Profiling (TTFT vs TPOT) | Dissected cold TTFT (1,619 ms) vs warm TTFT (152 ms). Discovered Head-of-Line prefill queue inflation under 8 concurrent streams. |
| 04 — Streaming Proxy | Edge Ingress & Nginx Tuning | Bypassed the 10-second proxy buffering hang using `proxy_buffering off;` and tuned read timeouts for zero 504s. |

---

## App Image

All 4 labs pull the same image — no local builds needed.

```
wizardxx7/sre-lab-app:1.0
```

Instrumented with Prometheus metrics, structured JSON logs, and OpenTelemetry traces.
Tracing activates automatically when `OTLP_ENDPOINT` is set — Labs 01 and 02 leave it unset.

---

## Run order

```bash
cd labs/lab-01-metrics && docker compose up -d && docker compose run k6
cd labs/lab-02-logs    && docker compose up -d && docker compose run k6
cd labs/lab-03-traces  && docker compose up -d && docker compose run k6

# Lab 04 — run baseline first, then trigger the incident
cd labs/lab-04-prod && docker compose up -d
docker compose run k6-normal
docker compose run k6-incident
```

Always `docker compose down` before moving to the next lab.

---

## Prerequisites

- Docker + Docker Compose
- Ports free: `3000` `3100` `3200` `4317` `4318` `5000` `9090` `9093` `9100`

---

## SysDE & SRE Interview Crash Course (`sysde-prep/`)

Targeted preparation modules for **Amazon Systems Development Engineer (SysDE)** and **Apple SRE / Systems** interviews:

1. **[01-step1-linux-diagnostics-cheat-sheet.md](sysde-prep/01-step1-linux-diagnostics-cheat-sheet.md):** The USE method, top 10 diagnostic commands, `/proc` deep dive, signals, and process states (R vs D vs Z).
2. **[02-step2-faang-incident-triage-playbook.md](sysde-prep/02-step2-faang-incident-triage-playbook.md):** Step-by-step diagnostic trees and interview talk-tracks for the 5 classic FAANG incident scenarios (I/O wait, open deleted files, 502/504 errors, OOM 137, ephemeral port exhaustion).
3. **[03-step3-python-systems-scripting-drills.py](sysde-prep/03-step3-python-systems-scripting-drills.py):** Standard-library Python automation scripts solving log parsing, latency percentiles, resilient HTTP polling with exponential backoff & jitter, and zero-dependency `/proc` telemetry collection.

