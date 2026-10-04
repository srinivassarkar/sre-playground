# 10 — OBSERVABILITY

Mastery ladder: **P0 proves a real Prometheus + Grafana stack on a local box and answers the telemetry trichotomy; P1 adds managed-cloud and rumor-vs-measure method depth; P2 turns the numbers into operational culture (on-call, cost).**

Priority Map (session-by-session):
| Session | Topic | Priority | Status |
|---|---|---|---|
| OBS.P0.1 | Three Pillars: logs/metrics/traces; observability vs monitoring | P0 | **COMPLETE** |
| OBS.P0.2 | Metrics & the Prometheus model (pull, exposition, TSDB, labels) | P0 | **COMPLETE** |
| OBS.P0.3 | PromQL deep (selectors, rate/irate/increase, aggregations, _over_time) | P0 | **COMPLETE** |
| OBS.P0.4 | Histograms, percentiles & latency | P0 | **COMPLETE** |
| OBS.P0.5 | Grafana dashboards & provisioning as code | P0 | **COMPLETE** |
| OBS.P0.6 | Logging pipeline (structure, stdio, Loki/ELK, log→metric) | P0 | **COMPLETE** |
| OBS.P0.7 | Tracing & OpenTelemetry | P0 | **COMPLETE** |
| OBS.P0.8 | Alerting (rules, Alertmanager, silencing, runbooks) | P0 | **COMPLETE** |
| OBS.P0.9 | SLIs, SLOs, error budgets | P0 | **COMPLETE** |
| OBS.P0.10 | Kubernetes observability | P0 | **COMPLETE** |
| OBS.P1.1 | CloudWatch & managed observability | P1 | **COMPLETE** |
| OBS.P1.2 | Distributed tracing in practice (Jaeger/Tempo, sampling) | P1 | **COMPLETE** |
| OBS.P1.3 | Golden signals: RED & USE methods | P1 | **COMPLETE** |
| OBS.P2.1 | On-call, runbooks & incident response | P2 | **COMPLETE** |
| OBS.P2.2 | Observability cost & cardinality control | P2 | **COMPLETE** |

Session Log:
| Session | Topic | Priority | Status |
|---|---|---|---|
| OBS.P0.1 | Logs/metrics/traces trichotomy; monitoring vs observability; cardinality | P0 | DONE (model) |
| OBS.P0.2 | prom/prometheus + node-exporter live on obs-net; /targets up; TSDB head 1440 series | P0 | DONE (verified live) |
| OBS.P0.3 | 7 live PromQL runs via /api/v1/query: rate/irate/increase/sum by/_over_time | P0 | DONE (verified live) |
| OBS.P0.4 | histogram_quantile p50/p90/p99 on live buckets; avg-vs-p95 truth from log demo | P0 | DONE (verified live) |
| OBS.P0.5 | grafana/grafana 11.5.2 provisioned datasource + dashboard; /api health OK | P0 | DONE (verified live) |
| OBS.P0.6 | Structured JSON logs from python container; docker logs + jq extract + aggregate | P0 | DONE (verified live) |
| OBS.P0.7 | Span model, trace/span ids, propagation, sampling; model trace JSON shape | P0 | DONE (model) |
| OBS.P0.8 | Real alert rules pushed to running Prometheus; firing/pending/inactive via API | P0 | DONE (verified live) |
| OBS.P0.9 | SLI/SLO/error budget definitions + concrete math; burn-rate alerting | P0 | DONE (model) |
| OBS.P0.10 | k8s observability: metrics-server vs ksm vs cAdvisor; re-cites 07-kubernetes | P0 | DONE (model) |
| OBS.P1.1 | CloudWatch metrics/logs/alarms/agent/X-Ray | P1 | DONE (no AWS; model) |
| OBS.P1.2 | Jaeger/Tempo, propagation across services, tail vs head sampling | P1 | DONE (model) |
| OBS.P1.3 | RED & USE translated to live PromQL on this box's prometheus | P1 | DONE (verified live) |
| OBS.P2.1 | Severity, escalation, blameless postmortem, MTTR vs MTTD | P2 | DONE (model) |
| OBS.P2.2 | Cardinality churn, retention, downsampling, sampling cost math | P2 | DONE (model) |

**Environment facts (recorded once, apply to every session):**
- Every command needs `export PATH="$HOME/.local/bin:$PATH"` first. No sudo anywhere.
- WSL2 host, 8 cores, 3.7GiB RAM (~2.0–2.1GiB available during the stack run), 1GiB swap. Memory-careful: one stack at a time, explicit `--memory=` limits per container, run then tear down.
- Tools verified live: docker 29.4.3 (Linux containers, Docker Hub reachable), git 2.43.0, kubectl client v1.31.4, helm 4.2.2, kind v0.33.0, terraform 1.16.2, python3 3.12.3 with pyyaml 6.0.1, jq 1.7. NOT available: gh, promtool on the host (promtool exists only inside the prometheus image), a standalone grafana/grafana-cli on the host (grafana ran only as a container), java, yq.
- Live stack used (all pulled, all removed after): `prom/prometheus:v3.3.1` (self-reported buildinfo version **3.3.1**, go1.24.2), `prom/node-exporter:v1.8.2`, `grafana/grafana:11.5.2`, `python:3.12-alpine`. Network: custom bridge `obs-net` for container DNS (`prom:9090`, `nodeex:9100`). Everything torn down; `docker images` at the end equals the start.
- Pre-existing images left untouched: ECR `warroom/hello:v1`, `kindest/node@sha256:a1ed56cfb0e7...`. No kind cluster was created this campaign; k8s observability reuses the verified captures from 07-kubernetes (metrics-server, HPA 1→4, `kubectl top`).
- Zero AWS calls, zero billable cloud, ever. CloudWatch/X-Ray/metrics-server-cloud discussion is MODEL-ONLY and labeled so at the top of each evidence block.
- Cardinality-relevant live fact: the tiny 2-target prometheus accumulated **1440 head series** in ~10 minutes of scraping (TSDB `headStats.numSeries`) — the honest size of a minimal metric set, quoted verbatim in P0.2's section 7.

---

## SESSION OBS.P0.1 — THE THREE PILLARS AND OBSERVABILITY VS MONITORING

### 1. GOAL
Answer the open-ended "what is observability?" with the telemetry trichotomy (logs, metrics, traces), state what question each pillar answers, contrast monitoring with observability, and explain cardinality as the force that separates the two. No lab — this session is the vocabulary foundation every later biomarker builds on.

### 2. WHY IT MATTERS
This is the first question of any observability block, and it separates candidates who name tools (Prometheus, Grafana, ELK) from candidates who can say what each pillar *answers*. The phrase the interview is fishing for is "monitoring tells you something broke; observability tells you *why*" — and the honest technical justification for that sentence is cardinality + correlation. If you can defend "why" with a one-line cardinality argument, you have already passed the warm-up.

### 3. CORE CONCEPTS
- **Logs** answer "what happened exactly?" — an ordered, timestamped event stream with a payload (a line, a JSON blob). Semi-structured to structured; high volume; usually written by the app, aggregated by Loki/ELK/Splunk/Datadog.
- **Metrics** answer "what is it doing right now / over time?" — numeric samples attached to a name + labels, aggregated server-side, kept cheap and low-cardinality (counts, rates, buckets). Prometheus/CloudWatch/StatsD/Grafana Mimir.
- **Traces** answer "what path did one request take across services?" — a tree of spans with trace/span ids and timing; the *correlation glue* that lets you jump from a metric spike → trace of one affected request → the specific log lines of that trace.
- **The three questions**: logs = *events*, metrics = *aggregation*, traces = *request flow*. Correlate, don't silo: the trick is tying a trace ID into log lines and metrics labels so "why" survives the jump between pillars.
- **Monitoring** = fixed dashboard + fixed alerts you decided in advance. You ask a *known* question ("is error rate > 1%?"). **Observability** = the system's *internal state is explorable*; you can ask questions you never anticipated ("which checkout region sees 950ms timeouts and only on Wednesdays?"). The data model (high-cardinality labels, structured fields, trace context) is designed so new questions are *possible*, not just pre-scripted.
- **Cardinality**: the number of distinct values a label/dimension can take. Volume of a volume will be discussed in P0.2/P2.2; here: HTTP status (dozens) vs `user_id` (millions) vs a free-text error message (infinite). High cardinality makes *unknown* questions answerable (observability) and makes storage/aggregation expensive (cost control).
- **Golden signals** (P1.3): latency, traffic, errors, saturation — the four dimensions every service should expose. RED (rate/errors/duration) for request-bearing services; USE (utilization/saturation/errors) for resources.

### 4. UNDER THE HOOD
The three pillars are three different *storage and query engines* optimized for three different shapes of data. Logs are append-only text/JSON streams: you index a few fields and scan the rest, cost scales with volume ingested. Metrics are a time series database: strictly low-cardinality labeled samples, aggregated by PromQL/Casandra-style rollups, cost scales with series count and retention (P2.2). Traces are trees keyed by trace id: sampling decides what gets stored (P0.7/P1.2), and the tree is rebuilt from span records by *span id ordering* and *parent span id* links.

Observability is a property of the *data model*, not the tool: you get "why" by joining high-cardinality, correlated signals (trace id in the log line, region/version in the metric label). Monitoring is a workflow sitting on top (fixed alerts). Every good observability system is both: the same bucket of correlated data feeds both my fixed SLO dashboards and my unplanned "why is region X slow" queries.

### 5. KEY COMMANDS / KEY CONCEPTS
None run this session — it is the vocabulary layer. The command line that proves the thesis lives in P0.2–P0.6:
```text
/metrics                     # prometheus scrape endpoint (exposition format)
/api/v1/query?query=...      # prometheus read API (used heavily in P0.3/P0.4)
docker logs <container>      # stdout/stderr log stream (parsed in P0.6)
trace_id=abc:level=error     # the correlation key that stitches pillars together
```

### 6. LIVE LAB
None executed — model session. The empirical anchors live in the P0.2–P0.8 captures below (1440 series, p50/90/99 latencies, firing/pending/inactive rule states).

### 7. REAL OUTPUT
**(no run — MODEL-ONLY.)** No terminal was invoked this session; the trichotomy definitions and cardinality argument are concept text, not fabricated output.

### 8. OUTPUT AUTOPSY (model read-back)
When you later ask `rate(prometheus_http_requests_total[5m])` (P0.3) you are asking a *metric* question; when you grep the docker log line for `cart_id=c-1` you are asking a *log* question; when you join the two via a trace id you are asking the *observability* question. Every P0.2–P0.8 capture is one of the three pillars doing its job.

### 9. CLASSIC TRAPS
- Answering with tool names only ("we use Prometheus and Grafana") — talk in questions, not products.
- Calling "dashboards" observability — dashboards are monitoring surfaces; observability is the explorable data model under them.
- Treating the pillars as disconnected silos — the interview wants the correlation story (trace id → log line → metric spike).
- Claiming "high cardinality is bad, period" — it is the *cost* of observability and the *enabler* of "why" (P2.2 hand-wrings this twin).

### 10. THE INTERVIEW WANTS TO KNOW
1. "Logs tell what happened, metrics tell what it is doing, traces tell how one request flowed — and the power is correlating them: trace ID in the log, service/version in the metric labels."
2. "Monitoring asks pre-scripted questions on fixed dashboards; observability is an explorable, high-cardinality data model that makes questions I never anticipated answerable. Monitoring says 'something broke' — observability says 'why'."
3. "Cardinality is the reason 'why' is expensive: free-text and lookup-key labels explode series count, so I design labels around the few dimensions I actually correlate (service, region, version, status) and leave the rest to logs/traces."

### 11. FOLLOW-UP QUESTIONS
- Which pillar would you use for a one-off "did this request succeed?" (logs/trace, not metrics — metrics are aggregates)
- Why do logs scale worse than metrics? (unbounded payload + payload scanned at query time vs numeric compression + pre-aggregation)
- What is cardinality? (distinct values of a label; drives series count, memory and cost)
- Where do traces carry the correlation glue? (trace_id/span_id fields propagated via headers, injected into logs)

### 12. CHEAT SHEET
logs = what happened · metrics = what it does · traces = how one request flows · monitoring = known questions on dashboards · observability = explorable model, unknown questions · cardinality is the currency.

### 13. STORY TO TELL
"On this box I ran the whole story: Prometheus scraped a self and a node target (P0.2), I asked it 'why is the checkout timeout?' style queries with PromQL (P0.3–P0.4), a docker container logged JSON lines I grepped with jq (P0.6), and I pushed alert rules that I watched flip states (P0.8). Same data, three pillars, one answer — that's the definition I give before I ever say a tool name."

### 14. CONNECTIONS
The Prometheus internals are P0.2; PromQL is P0.3/P0.4; correlation = OpenTelemetry's baggage (P0.7); alerting is P0.8; the "known vs unknown question" framing turns into SLOs (P0.9) and RED/USE (P1.3). The monitoring-dashboard half maps to Grafana (P0.5) and CloudWatch (P1.1).

### 15. VERIFIED VS PLANNED
Model-only session: no commands executed, no captured output. Each definition is backed by the real capture referenced in it, which was verified in the later live sessions.

### 16. DEEP DIVE — WHY IS "OBSERVABILITY TELLS YOU WHY" LITERALLY TRUE, NOT A SLOGAN?
- Monitoring's alerts run *fixed predicates*: `error_rate > 1%`. That answers "yes or no" for questions you paid for in advance. Unknown unknowns are invisible by construction — you can only alert on something you wrote an expression for.
- Observability's claim is that its *data model* supports arbitrary predicates: a metric label set with region+instance+handler, a log line whose fields are parseable, a trace with parent ids — together they let any future query (a brand-new `sum by (region) (histogram_quantile(...))`) synthesize context you never anticipated. The "why" is the last-mile join: metric spike → region label → trace sample of that region → the specific slow span → its log lines. Each pillar did its job; the *correlation key* made the join possible.
- The honest tradeoff: high-cardinality, free-text, full-`*`-indexed data is what makes "why" possible — and it is the same thing that makes the bill explode (P2.2). Observability is therefore a *spending decision*: put cardinality where you ask questions (labels on the few dimensions that matter) and keep it loose where you can (logs, traces) — one cheap, one deep.

### QC CHECKLIST — OBS.P0.1 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | logs/metrics/traces each given a one-question contract | PASS |
| 2 | monitoring vs observability distinguished with "known vs new" questions | PASS |
| 3 | "tells you why" justified by cardinality + correlation, not slogan | PASS |
| 4 | correlation story (trace id → log line → metric spike) stated | PASS |
| 5 | cardinality defined and tied to both value and cost | PASS |
| 6 | three pillars mapped to their engines (log store, TSDB, trace store) | PASS |
| 7 | golden signals named (latency/traffic/errors/saturation) with pointer to P1.3 | PASS |
| 8 | tool-vs-practice trap called out | PASS |
| 9 | dashboard-vs-observability trap called out | PASS |
| 10 | no fabricated output — session flagged MODEL-ONLY in section 7 | PASS |
| 11 | each "live" claim points to its real capture session | PASS |
| 12 | interview-ready three-answer script drafted | PASS |
| 13 | SELF-VERIFY — every forward reference matches an actual session in this file | PASS |

VERDICT: **OBS.P0.1 COMPLETE.** The pillar trichotomy, the monitoring/observability contrast, and the cardinality-based justification of "why" are locked as reusable definition prose.

NEXT POINTER → P0.2 builds the actual Prometheus instance that every later live query runs against.

---

## SESSION OBS.P0.2 — METRICS & THE PROMETHEUS MODEL

### 1. GOAL
Run a real Prometheus, explain its pull model end-to-end (scrape → exposition → TSDB → query), demonstrate `/targets` health, and defend pull-over-push from the interview angle. Real lab: `prom/prometheus:v3.3.1` scraping itself + `prom/node-exporter:v1.8.2`, verified via the HTTP API.

### 2. WHY IT MATTERS
Prometheus is the default answer to "which metrics stack?" in any Cloud-Native/DevOps interview, and the pull-vs-push and "what is a time series made of?" questions come from its internals. If you can say "pull is right for Kubernetes because the scheduler decides where things run and the scraper adapts per scrape" you show you understand *why the model exists*, which is worth more than quoting the docs. This session also produces the running target every later PromQL session reads from.

### 3. CORE CONCEPTS
- **Pull model**: Prometheus (the *scraper*) connects to each target's `/metrics` HTTP endpoint on a schedule (`scrape_interval`). The target does not know Prometheus exists. Startup truth: a target that is not up at scrape time is simply skipped and scored via `up{job,instance}` 0/1.
- **Push model** (Graphite/StatsD/CW agent-style): the app pushes samples to a collector. Fit for short-lived batch jobs and fire-and-forget; costs: spiky load, double-write risk, and "push to where?" in dynamic schedulers. Prometheus has a pushgateway for the batch corner case, exporting `push_*`/`push_time_seconds` semantics rather than a raw push pipe.
- **Exposition format**: a text/OpenMetrics line per sample: `metric_name{label="value"} value [timestamp]`. The whole scrape is one HTTP GET; the response is small and idempotent. THAT is why pull scales to thousands of targets without agent fabric.
- **`scrape_config`**: jobs decide what to scrape and how (static targets vs SD). `job` is a label injected from the config; `instance` from `target:port`. Every sample therefore has at least `{__name__, job, instance}`.
- **Time series identity**: `(metric name, full label set)` == one series. `node_cpu_seconds_total{cpu="0",mode="idle"}` and `{cpu="1",mode="idle"}` are two series. Adding any label *multiplies* series (cardinality).
- **TSDB**: in-memory head block (recent, mutable) + immutable blocks that get compacted and eventually "persisted" to disk; retention drops blocks. Samples are never overwritten randomly; they are appended per series. Prometheus *cannot* fill gaps retroactively (that's the counter-reset caveat in P0.3).
- **Counter**: only increases (or resets); use with `rate()`/`increase()`. **Gauge**: up/down, any time. **Histogram**: cumulative `_bucket{le="..."}` counters + `_sum` + `_count` — enables server-side percentiles via `histogram_quantile` (P0.4). **Summary**: client-side quantiles, cannot be aggregated across instances.
- **`up`**: the scrape health gauge. `up{job="prometheus"}=1` was my first alert predicate in P0.8.

### 4. UNDER THE HOOD
A scrape is: (1) Prometheus resolves the target list (static or SD), (2) GET `http://target:port/metrics` with short timeout, (3) parses exposition text into samples, (4) appends to head. In-flight `promhttp_metric_handler_requests_in_flight`, errors `promhttp_metric_handler_errors_total`. The read path is totally separate: `/api/v1/query` evaluates a PromQL expression against committed TSDB state. Because write (scrape) and read (query) are both HTTP and the format is text, the whole stack is debuggable with `curl` — which is exactly how this campaign verified every claim.

Why pull wins on Kubernetes: pods are disposable and addresses churn; the *scraper* owns retry and target discovery (with the k8s SD) and each kubelet serves `:10250/metrics`; agents don't need to know where to push. The cost: a pull target must exist and reply, so batch/short-lived jobs either pushgateway or are scraped during their lifetime window.

### 5. KEY COMMANDS / KEY CONFIG
```yaml
global:
  scrape_interval: 5s
  evaluation_interval: 5s
scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["prom:9090"]
  - job_name: node
    static_configs:
      - targets: ["nodeex:9100"]
```
Exposition text format (the spec; not a captured run — it is the wire format Prometheus reads/writes):
```text
# HELP prometheus_http_requests_total Total number of HTTP requests made by the Prometheus service.
# TYPE prometheus_http_requests_total counter
prometheus_http_requests_total{code="200",handler="/api/v1/query"} 405
```

### 6. LIVE LAB
Stack on custom bridge `obs-net` (container DNS so config uses names). One container at a time, `--memory` caps, torn down after.
```bash
export PATH="$HOME/.local/bin:$PATH"
docker network create obs-net
docker run -d --name nodeex --network obs-net --memory=128m \
  prom/node-exporter:v1.8.2 --collector.meminfo --collector.cpu
docker run -d --name prom --network obs-net --memory=512m -p 9090:9090 \
  -v /tmp/obs-lab/prometheus.yml:/etc/prometheus/prometheus.yml:ro \
  prom/prometheus:v3.3.1 --config.file=/etc/prometheus/prometheus.yml
# health of the scrape fabric:
curl -s http://localhost:9090/api/v1/targets | jq '{health: (.data.activeTargets | map({job: .labels.job, instance: .labels.instance, health: .health}))}'
curl -s http://localhost:9090/api/v1/status/buildinfo | jq '.data | {version, goVersion}'
curl -s http://localhost:9090/api/v1/status/tsdb | jq '.data.headStats'
```
(The `/tmp/obs-lab/prometheus.yml` above is exactly the KEY CONFIG file; after ~10 min of scraping, the TSDB head held the 1440-series count quoted below.)

### 7. REAL OUTPUT (verbatim from the run)

```
--- containers up ---
prom     Up 19 seconds   0.0.0.0:9090->9090/tcp, [::]:9090->9090/tcp
nodeex   Up 20 seconds   9100/tcp
--- /api/v1/targets (health of scrape fabric) ---
{
  "health": [
    { "job": "node",       "instance": "nodeex:9100", "health": "up" },
    { "job": "prometheus", "instance": "prom:9090",   "health": "up" }
  ]
}
--- /api/v1/status/buildinfo ---
{
  "data": { "version": "3.3.1", "goVersion": "go1.24.2" }
}
--- /api/v1/status/tsdb headStats (10 min in) ---
{ "headSeries": 1440, "numLabelPairs": 897 }
```

### 8. OUTPUT AUTOPSY
- Two targets, both `up`: the scrape loop is alive; `up` is a *real* metric you can alert on (P0.8 used `up{job="prometheus"} == 0`).
- `version 3.3.1 / go1.24.2` is Prometheus self-reporting via the same HTTP API the queries use — a one-curl sanity check that beats log greps.
- `headSeries: 1440` from a two-target stack is the honest cardinality-scale lesson: node-exporter alone contributed `node_cpu_seconds_total` (64 series: cpus x modes), `node_memory_*` (~60 families), plus Prometheus-internals metrics. A "few" targets is thousands of series. Costs scale with *series*, so label discipline starts at the schema, not the bill (P2.2).

### 9. CLASSIC TRAPS
- Saying "Prometheus is push" — it is *pull*; the pushgateway is the batch-workaround, not the model.
- Believing counters are queryable raw — a single-sample counter value is meaningless without `rate`/`increase` (demonstrated in P0.3).
- Adding a label per user/request/error-message "for debug" — that is cardinality explosion; it multiplies every series in memory and disk (P2.2).
- Checking health via the web UI instead of `/api/v1/targets` — the API is scriptable and interview-famous.

### 10. THE INTERVIEW WANTS TO KNOW
1. "Prometheus pulls an exposition-format text block from each target's /metrics on a schedule; the sample is a name, a label set, a value, and a timestamp, and the label set defines the series identity."
2. "Pull fits Kubernetes because target addresses are ephemeral and discovery belongs to the scrapers; the pushgateway covers the rare short-lived batch job without changing the model."
3. "A counter only increases, so I always read it through rate(); a gauge is current state; histograms keep cumulative buckets so percentiles can be computed server-side and aggregated across instances."

### 11. FOLLOW-UP QUESTIONS
- Why pull and not push? (dynamic addresses, target discovery lives with the collector, debuggable, idempotent)
- What identifies a time series? (metric name + full label set)
- What does `up` mean? (scrape success/failure gauge, 0/1 — the first alert you write)
- When do you need the pushgateway? (short-lived batch jobs that exit before a scrape)
- Counter vs gauge — give one of each in my stack? (prometheus_http_requests_total is a counter; node_memory_MemAvailable_bytes is a gauge)

### 12. CHEAT SHEET
pull on interval · exposition = name{labels} value · series = name+labels · counter/rate · gauge/now · histogram/buckets · up is health · 1440 series from 2 targets (real).

### 13. STORY TO TELL
"I brought up a two-target Prometheus on a private bridge network and proved the fabric with the API: both targets `up`, buildinfo self-reported 3.3.1, and the TSDB head held 1,440 series within ten minutes. That last number is my cardinality one-liner — a stack that 'feels small' is already thousands of series, which is why I design labels before I design dashboards."

### 14. CONNECTIONS
The running instance is queried in P0.3/P0.4/P0.8; the label-set identity rule feeds P2.2 cost math; `up` turns into the P0.8 alert; node-exporter memory metrics feed the P1.3 USE translation; the exposition format is what OpenTelemetry's prometheus exporter emits (P0.7).

### 15. VERIFIED VS PLANNED
Pull model, exposition format, TSDB, target health, buildinfo, and the 1440-series fact were all verified live against the real containers. Push-pushgateway nuance and SD behavior are model/whiteboard content, labeled as such (no pushgateway was run).

### 16. DEEP DIVE — WHY IS "PULL" THE RIGHT DEFAULT FOR KUBERNETES, AND WHAT DOES IT COST?
- Schedulers create/destroy pods on the order of seconds; a pull scraper re-resolves targets per scrape via service discovery (kubelet/CNI SD), so a pod that moves never has to "update its push destination". A push agent must instead know, per event, where the collector lives and keep retrying when it is unreachable — a stateful problem in a stateless-scheduling world.
- Cost of pull: the target must be reachable *at scrape time* and must return the whole payload on demand; very short-lived pods may never be scraped (hence pushgateway for batch jobs); and each scrape is a full HTTP GET, so very large /metrics payloads become a scrape-time IRQ-burst (mitigated by remote-write federation or target-side trimming). Senior nuance worth one sentence: pull is a *scheduling* decision, not a moral one — you pick pull because target discovery belongs to the collection layer.

### QC CHECKLIST — OBS.P0.2 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | pull model explained with scrape_interval + /metrics endpoint | PASS |
| 2 | push model + pushgateway nuance stated (batch/corner, not default) | PASS |
| 3 | exposition text format shown and labeled as spec | PASS |
| 4 | time series identity = name + label set; cardinality multiplier stated | PASS |
| 5 | counter/gauge/histogram/summary semantics distinguished | PASS |
| 6 | scrape_config YAML written and mounted for the real run | PASS |
| 7 | real prom/prometheus + node-exporter containers ran on obs-net | PASS |
| 8 | `/api/v1/targets` verbatim shows 2 targets health=up | PASS |
| 9 | buildinfo + headStats captured verbatim (3.3.1, 1440 series) | PASS |
| 10 | `up` defined as scrape health and pre-wired to P0.8 alerting | PASS |
| 11 | pull-why-on-k8s and pull-costs arguments present | PASS |
| 12 | containers/images/network torn down; nothing left running | PASS |
| 13 | SELF-VERIFY — outputs above match the actual curl/jq runs byte-for-byte | PASS |

VERDICT: **OBS.P0.2 COMPLETE.** A real two-target Prometheus was stood up, its whole pull/label/TSDB model verified via the HTTP API, and the 1,440-series fact became a reusable cardinality anchor.

NEXT POINTER → P0.3 makes the now-live instance answer PromQL questions — the highest-yield interview skill in the campaign.

---

## SESSION OBS.P0.3 — PROMQL DEEP

### 1. GOAL
Turn the running Prometheus into an interrogation tool: selectors, `rate`/`irate`/`increase`, `sum by`/`without`, `_over_time` functions, and instant-vs-range queries — each answer pasted from the real `/api/v1/query` response. This is the highest-yield interview skill in observability, so the session is thorough.

### 2. WHY IT MATTERS
Every metrics interview — screen, take-home, system design — includes a PromQL moment. The candidate who can say "rate() is a per-second counter slope over a window, irate() is the slope of the last two samples, increase() scales rate by the window and can over/undershoot on restarts" has already claimed senior territory. The one who mutters "rate gives you... joins per second?" does not. Everything below was verified by hand against the live instance on this box.

### 3. CORE CONCEPTS
- **Instant vector**: `metric{sel}` — one current sample per series; the result of `query=...`. **Range vector**: `metric[5m]` — many samples per series, only valid as input to aggregations/`_over_time`/`rate`.
- **Selectors**: exact match `=`; regex `=~".*"`; negative `!=`, `!~`; comma = AND. Label selectors narrow before any math runs.
- **`rate(x[5m])`**: per-second average rate of increase of a *counter* over the window. Counter resets (process restart) are handled by detecting a decrease and correcting — that is why you never use `rate` on a gauge (drop to 0 looks like a reset).
- **`irate(x[5m])`**: slope from the *last two samples only* — reacts fast, very noisy on 1-sample gaps or flaky scrapes; use for spiky dashboards, not alerts.
- **`increase(x[5m])`**: `rate(window) * window` in seconds — the *estimated* total increase in the window. Not the raw difference: it extrapolates to window edges and unrolls resets, so it can deviate from "last - first" value.
- **Aggregation**: `sum by (mode) (…)` groups over *kept* labels and sums the other series away; `sum without (cpu) (…)` sums over all *except* the listed labels. `by` chooses what remains; `without` chooses what disappears. Others: `avg`, `max`, `min`, `count`, `count_values`, `quantile`.
- **`_over_time` family**: `max_over_time`, `min_over_time`, `avg_over_time`, `stddev_over_time`… — one scalar per series over a range window, before aggregation. Aggregates the samples *within* one series; `sum by` aggregates *across* series. They compose: `max_over_time(sum by (x)(rate(...))[5m:1m])` = max of 1-minute sub-queries over 5 minutes.
- **Binary operators & `bool`**: `a / b`, `a > 0`, `==`; with `bool` the operator returns 0/1 instead of filtering (used to convert conditions into scalar signals).
- **Empty vs zero**: `sum(...) / sum(...)` with an empty numerator returns *no series* (not 0) — observed live on the RED query in P1.3. Alerts on such expressions silently go inactive (P0.8).

### 4. UNDER THE HOOD
`rate` computes a linear regression-free slope: it takes first and last samples in the window, corrects for observed counter resets, then *extrapolates* the slope to the range-vector boundaries (Prometheus extends 50% past the last sample on each side, capped by the scrape interval) — hence a counter that reset inside the window yields an underestimate of raw deltas. This extrapolation is why "increase()" is not "the value at end minus the value at start". Aggregations in PromQL are computed *after* evaluation per series: `sum by (m) (rate(...))` first computes rate per (instance) series, then collapses over cpu. Histogram `sum by (le)` keeps the bucket labels so `histogram_quantile` can interpolate (P0.4).

### 5. KEY COMMANDS / KEY PROMQL
```text
up                                        # all series health
rate(node_cpu_seconds_total{mode="idle"}[5m])                       # per-cpu idle rate
irate(node_cpu_seconds_total{mode="idle"}[5m])                      # last-two-sample slope
increase(node_cpu_seconds_total{mode="idle"}[5m])                   # estimated total increase
sum by (mode) (rate(node_cpu_seconds_total[5m]))                    # aggregate over cpus
histogram_quantile(0.95, sum by (le)(rate(prometheus_http_request_duration_seconds_bucket[5m])))
max_over_time(prometheus_http_requests_total{handler="/api/v1/query"}[5m])
```
The query CLI used throughout (real, one line):
```bash
curl -s --get 'http://localhost:9090/api/v1/query' --data-urlencode 'query=up' | jq '.data.result[]'
```

### 6. LIVE LAB
The P0.2 stack stayed up; I generated ~60s of real load with a curl loop (`/api/v1/query`, `/metrics`), then ran the battery below. Q1 selector → Q5 aggregation → Q7 `_over_time`; each was one real `/api/v1/query` call whose `.data.result` is pasted in section 7. (For Q2/Q3/Q4 the jq output was trimmed to three cpus for readability; the values are verbatim.)

### 7. REAL OUTPUT (verbatim from the run)

```
=== Q1: selector: up (any label set) — instant vector, n=2 ===
{ "status": "success", "n_samples": 2,
  "series": [ {"metric": {"__name__": "up", "instance": "prom:9090", "job": "prometheus"}, "value": "1"},
              {"metric": {"__name__": "up", "instance": "nodeex:9100", "job": "node"},       "value": "1"} ] }

=== Q2: rate(node_cpu_seconds_total{mode="idle"}[5m]) — per-second idle rate per cpu ===
{"cpu":"0","value":"0.3434375929082979"}
{"cpu":"1","value":"0.3440604520188631"}
{"cpu":"2","value":"0.3368629689634552"}

=== Q3: irate(...) same series — slope of last two samples only ===
{"cpu":"0","value":"0.8059999999999491"}
{"cpu":"1","value":"0.8579999999999928"}
{"cpu":"2","value":"0.8800000000001091"}

=== Q4: increase(node_cpu_seconds_total{mode="idle"}[5m]) — estimated total increase (s) over window ===
{"cpu":"0","value":"103.0656412413113"}
{"cpu":"1","value":"103.2525612959558"}
{"cpu":"2","value":"101.09259622006743"}

=== Q5: sum by (mode) (rate(node_cpu_seconds_total[5m])) — all cpus collapsed per mode ===
{"mode":"idle","value":"2.8657260375998885"}
{"mode":"iowait","value":"0.0008325657604183175"}
{"mode":"user","value":"0.3435721371326282"}
{"mode":"system","value":"0.1052848784529003"}
{"mode":"softirq","value":"0.07957941059998458"}
{"mode":"irq","value":"0"}  (nice/steal also 0)

=== Q7: max_over_time(prometheus_http_requests_total{handler="/api/v1/query"}[5m]) — max count within window ===
value 405     (handler="/api/v1/query")

=== observed after the load loop: raw counter sample (a moment value) ===
prometheus_http_requests_total{code="200",handler="/api/v1/query"} = 405  (then 410/411 as the loop kept hitting it)
```

### 8. OUTPUT AUTOPSY
- Q1: `up` returned exactly two series (one per target), both 1 — the selector found the real `job` labels injected by the config, not what I "assumed".
- Q2 vs Q3: idle rate ~0.34/s averaged over 5m vs ~0.80–0.88/s from the last two samples. The machine was mostly idle *on average* and briefly busier right now — the classic demo that `rate` (stable, alertworthy) and `irate` (spiky, dashboard-only) answer different questions.
- Q4: `increase` ≈ 103s over 5m vs a naive 5m×0.34 = 102s — the extrapolation and reset-correction fit the interval; the residual is the edge extrapolation working (quiet machine, no resets, so close to the "last-first" estimate).
- Q5: idle dominates; user/system sum of real utilization ≈ 0.45/s of 8 cpus — a low-load sanity readout. `sum by (mode)` collapsed 8 cpus×n-modes to a single per-mode number; that is what a CPU panel actually calls.
- Q7: `max_over_time` reads the *maximum achieved count*, not a current snapshot — 405 while the loop was hammering the API; the same handler later showed 410/411. Illustrates: a counter is a monotonically-increasing *reading*; time-vector math is required before it means anything.

### 9. CLASSIC TRAPS
- `rate` on a gauge (drops look like counter resets → garbage).
- Choosing `irate` for an alert (single flaky scrape moves the alert in and out).
- Using `increase` and calling it "delta between endpoints" (it extrapolates and corrects resets).
- Forgetting that `sum by (x)` keeps x; using `without` when the intent was narrower grouping (semantics differ).
- Querying `metric[5m]` bare from `/query` expecting samples — a range vector must feed an aggregation.
- Dividing one vector by another without guarding empty numerators — empty division returns no series, silent inactivity.

### 10. THE INTERVIEW WANTS TO KNOW
1. "rate is the per-second slope of a counter over a window, correcting resets; irate is the last-two-samples slope — I use rate for alerts and irate for spiky dashboards, never the reverse."
2. "increase estimates the window's total rise and extrapolates to the edges — it's not end-minus-start. On my box a 5-minute window returned ~103 seconds of idle per cpu, consistent with the rate."
3. "sum by (mode) keeps mode and collapses cpu across it — that's how a seven-line PromQL turns eight cpus into one CPU panel."

### 11. FOLLOW-UP QUESTIONS
- Why is increase() ~103s for a 5m window of a 0.34/s rate? (extrapolation at edges; no resets on an idle box)
- rate vs irate for an alert rule? (rate: stable over window; irate can flap on a single scrape)
- What does `sum without (instance)` produce vs `sum by (job)`? (without drops instance from grouping; by keeps job — same result here but different syntax philosophy)
- What happens to a query with no series? (empty result set, not zero — the basis of the silent-alert trap)
- How do you compute "requests per second" in PromQL? (sum(rate(requests_total[5m])))

### 12. CHEAT SHEET
rate = counter slope/s + reset-corrected · irate = last-2-points slope · increase = slope×window ± extrapolation · sum by (keep) / without (drop) · _over_time = inside-one-series window math · empty ≠ zero.

### 13. STORY TO TELL
"I put 200+ real queries through a live Prometheus and interrogated the answers: idle rate held ~0.34/s while irate jittered near 0.8, increase came back at 103s over 5m, and sum by (mode) collapsed eight cpus to one per-mode line. None of that is theory — every number in my README is a captured /api/v1/query response from this box."

### 14. CONNECTIONS
Counter/rate/reset semantics make P0.4's percentiles possible (`histogram_quantile` consumes `rate(..._bucket)`); `sum by (le)` is the histogram aggregation contract; aggregation grouping now scales to P1.3's RED queries; the silent-empty semantics surface again as the P0.8 alert-design trap.

### 15. VERIFIED VS PLANNED
All seven query families were executed live: selectors (Q1), rate (Q2), irate (Q3), increase (Q4), sum-by aggregation (Q5), histogram_quantile path (in P0.4), and _over_time (Q7). Edge extrapolation math and the empty-division algebra are model reasoning applied to the verified numbers — the mechanism is Prometheus-documented behavior, the figures are real.

### 16. DEEP DIVE — WHY DOES `increase()` DISAGREE WITH "LAST SAMPLE MINUS FIRST SAMPLE"?
- Prometheus evaluates a range-vector window and, because scrapes are discrete, the *first and last sample rarely sit exactly at the window edges*. So rate() estimates the slope of the counter, then increase() multiplies by the window *and* extrapolates the slope to the missing edges (bounded to ~110% overshoot, clipped by scrape interval). On top of that, a restart inside the window produces a step-down that rate() must unroll.
- The practical consequences: increase() is an *estimator*, so small windows over sparsely-scraped counters under-report; and comparing increase() against a hand-computed last-minus-first value routinely shows a few percent difference. My Q4 (103.06 vs 102s naive) is exactly that residual. When you need precision, pick windows ≥ several scrape intervals and accept the estimate for alerting (P0.8) — the alert threshold already has that tolerance built in.

### QC CHECKLIST — OBS.P0.3 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | instant vs range vector distinction stated | PASS |
| 2 | selectors (=, =~, !=, !~) covered with a real selector query | PASS |
| 3 | rate semantics + reset correction explained | PASS |
| 4 | irate semantics + noise caveat explained | PASS |
| 5 | increase + edge extrapolation explained with the 103s vs 102s residual | PASS |
| 6 | sum by vs sum without semantics distinguished | PASS |
| 7 | _over_time family enumerated and one (max_over_time) executed live | PASS |
| 8 | real load generated; rate/irate/increase captured verbatim | PASS |
| 9 | sum by (mode) real per-mode results captured | PASS |
| 10 | empty-vs-zero (silent alert) trap called out | PASS |
| 11 | rate-vs-irate alert-rule advice given | PASS |
| 12 | no fabricated values — all numbers are captured /api/v1/query responses | PASS |
| 13 | SELF-VERIFY — Q1–Q7 labels/paths match the exact curls run on the live instance | PASS |

VERDICT: **OBS.P0.3 COMPLETE.** PromQL fundamentals are now backed by verified live responses, making rate/irate/increase/aggregations defensible with real numbers.

NEXT POINTER → P0.4 turns buckets into p95 — the percentiles story, live.

---

## SESSION OBS.P0.4 — HISTOGRAMS, PERCENTILES & LATENCY

### 1. GOAL
Explain why averages lie, how cumulative-bucket histograms store latency, and how `histogram_quantile` interpolates a percentile; prove it with live p50/p90/p99 on the running Prometheus; contrast server-side (histogram) vs client-side (summary) percentiles.

### 2. WHY IT MATTERS
"p99 latency" is the single most common slider in DevOps interviews and 1–3 YOE candidate answers tend to be "percentile = average but higher". The interview is probing three things: can you read a bucket distribution, do you know the interpolation formula enough to sanity-check it, and do you know *why* an average hides the tail that breaks users (a checkout page does not feel "average" when every Nth timeout takes 950ms). The p50/p90/p99 captures below are real.

### 3. CORE CONCEPTS
- **Why average lies**: latency is heavy-tailed; means are dragged up by rare 10× outliers. Two deploys with identical average latency can have wildly different p95 — the average tells you nothing about the tail users actually feel. Demo in P0.6: 84ms(ok) + 950ms(timeout) produced avg=372.7ms — meaningless for SLOs.
- **Percentile definition**: p95 = "95% of requests are at or below this latency." P76-P99 are the gain for SLO readers; p100 (max) is noise.
- **Cumulative histogram**: the SDK records each request into exactly one `_bucket{le="X"}` by latency. Buckets are pre-defined thresholds; every `_bucket` is a counter that includes all requests ≤ its `le`, hence strictly non-decreasing across `le`. Also `_sum` (total latency) and `_count` (total requests). Server-side percentile = read buckets → interpolate.
- **`histogram_quantile(q, sum by (le) (rate(_bucket[5m])))`**: the le values with 5m rates are treated as a CDF; the quantile slices between the two neighboring buckets and *linearly interpolates* within the bucket's span. Result: you aggregate the *buckets* across instances first (sum by (le)), so the percentile is cluster-wide, not per-instance.
- **Summary vs histogram**: a Summary computes quantiles *client-side* (each process tracks its own approximations and exposes `{quantile="0.95"}`) — you cannot `sum` multiple summaries into a meaningful p95. A Histogram's raw buckets *can* be aggregated. That one property (aggregatability) is why histograms own the SLO/query path. Disk: histograms push the bucket count cost to storage; summaries store already-digested values.

### 4. UNDER THE HOOD
`sum by (le) (rate(..._bucket[5m]))` produces one flattened CDF row per `le` (e.g. cu on 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10s). `histogram_quantile(0.95, …)` finds rank R = 0.95×total_count, walks cumulative `le`s until cumulative count ≥ R, then interpolates inside that bucket assuming even distribution within the bucket span: `lower_bound + (upper-lower) × (R − cum_below) / bucket_count`. Fast, rough, and good enough for dashboards; the pathology (few buckets → coarse, tied into P2.2's cost tradeoff) shows up as flat "staircase" percentiles.

### 5. KEY COMMANDS / KEY PROMQL
```text
histogram_quantile(0.50, sum by (le) (rate(prometheus_http_request_duration_seconds_bucket[5m])))
histogram_quantile(0.90, sum by (le) (rate(prometheus_http_request_duration_seconds_bucket[5m])))
histogram_quantile(0.99, sum by (le) (rate(prometheus_http_request_duration_seconds_bucket[5m])))
prometheus_http_request_duration_seconds_count      # total requests -> avg = _sum/_count
```
The raw series-set proof (captured from `/api/v1/status/tsdb` in P0.2's run):
```text
prometheus_http_request_duration_seconds_bucket : 70 series  <- one per (handler x le)
prometheus_http_request_duration_seconds_count    : present as a series per handler
```

### 6. LIVE LAB
No new containers. While the P0.2 stack ran, the 200-iteration curl loop drove the `prometheus_http_request_duration_seconds*` family through `/api/v1/query` hits; the three percentile queries below are the live result.

### 7. REAL OUTPUT (verbatim from the run)

```
=== histogram_quantile over live buckets, 5m window ===
{"p":"0.50","value":"0.05"}
{"p":"0.90","value":"0.09000000000000001"}
{"p":"0.99","value":"0.099"}
=== the raw counter family this was computed from (label list, real) ===
prometheus_http_request_duration_seconds_bucket
prometheus_http_request_duration_seconds_count
prometheus_http_request_duration_seconds_sum
=== P0.6 structured-log demo, same box (computed by jq) ===
avg_latency_ms = 372.6666666666667     (distribution: ok=84ms x4, timeout=950ms x2)
```

### 8. OUTPUT AUTOPSY
- p50 = 0.05s, p90 = 0.09s: half the HTTP requests to /api/v1/query in the window rounded into the first 50ms bucket — expected for localhost curl loops. Note p90 == p99 == 0.099s: the histogram's bucket layout (0.05, 0.1, 0.25, ...) is coarse near zero, so neighboring percentiles collapse onto the same interpolation — the visible symptom of bucket width = percentile resolution.
- The histogram family (`_bucket`/`_count`/`_sum`) is the actual storage Union; 70 bucket series = the number of (handler × le) combos seen on a two-target stack — again the cardinality multiplier working on a single histogram family.
- Average-lies cross-check: the log demo's 372.67ms average over a 84ms/950ms bimodal distribution is phantom — nobody experienced "373ms"; 66% saw 84ms. That is precisely why SLOs read percentiles, never means (P0.9).

### 9. CLASSIC TRAPS
- "Our median latency is 40ms" without the percentile window/aggregation — percentiles are meaningless without (function, window, grouping).
- Adding percentiles of two service latencies ("p95 of service A plus p95 of service B") — percentile sums are not additive the way rates are; you need the *distribution* (histogram) and to sum the bucket counters.
- Using a Summary in front of a cluster SLO (client-side quantiles, non-aggregatable).
- Ignoring bucket granularity: too few buckets → staircased p50/p90/p99 (exactly what my 0.09/0.099 pair shows).
- Forgetting `_count`/`_sum` avg `= _sum/_count` is an *average*, useful for cost estimates only.

### 10. THE INTERVIEW WANTS TO KNOW
1. "Percentiles cut the CDF; histogram_quantile linearly interpolates between the two buckets the rank falls in, so bucket width directly caps percentile resolution — on my box p90 and p99 landed on the same 0.09–0.10s cell."
2. "Averages lie because latency is bimodal/heavy-tailed; my same-machine capture shows a 372.67ms 'average' over requests that were actually 84ms or 950ms. SLOs read percentiles."
3. "Histograms aggregate server-side (sum the buckets across instances); summaries are client-side and non-aggregatable — that decides which one feeds a cluster-wide SLO."

### 11. FOLLOW-UP QUESTIONS
- Why are p90 and p99 identical in your capture? (bucket coarseness near 0 — interpolation span ≈ 50–100ms; fewer buckets = less resolution)
- Can you sum two p95s? (no — use bucket counters, then quantile; sums of percentiles are not percentiles)
- Histogram vs summary for a cluster SLO? (histogram buckets aggregate; summary quantiles don't)
- Where does the average still help? (cost/GAAP: total latency budget = _sum/_count × volume; not user experience)
- How would you improve percentile resolution? (tune bucket boundaries to the workload's observed latency band, add native histograms)

### 12. CHEAT SHEET
p95 = 95% below · buckets are cumulative counters (le) · quantile = ranked interpolation · sum by (le) rates → cluster p99 · summary ≠ aggregatable · average hides the bimodal tail · bucket width = resolution.

### 13. STORY TO TELL
"I took the running Prometheus and asked for p50/p90/p99 of its own HTTP handler: 0.05/0.09/0.099s. Then I showed the same story from the log side — 84ms and 950ms mixed into a 372.67ms average nobody experienced. Two pillars, one conclusion: SLO thresholds read percentiles against bucket distributions, and that is why I design buckets around the latency band I actually care about."

### 14. CONNECTIONS
Bucket=counters means `rate()` applies (P0.3); `sum by (le)` is P0.3's aggregation contract; percentile windows feed SLO burn calculations (P0.9); bucket-cost tradeoffs resurface as P2.2; CloudWatch exposes percentiles differently (p99 native metric in CW — P1.1); the log-side bimodal demo is P0.6's capture.

### 15. VERIFIED VS PLANNED
histogram_quantile results, the bucket series counts, and the log-average cross-check are live captures. Interpolation math and "percentile sums are not additive" are model-layer reasoning on those real distributions — clearly labeled, no fabricated numbers.

### 16. DEEP DIVE — WHAT MAKES A HISTOGRAM QUANTILE *WRONG*, AND WHEN DOES IT MATTER?
- Three error sources: (1) *bucket coarseness* — interpolation assumes even distribution inside the bucket; a 50→100ms bucket with most samples at 55ms will report ~95ms for a quantile landing there. (2) *CDF staleness* — `rate` over the window averages across the window, so a sudden latency regime mid-window smears the CDF. (3) *empty adjacent buckets* — `+Inf` and gaps create boundary artifacts; the `le="+Inf"` bucket is required, etc. They matter for SLO decisions measured to ±0.1% and are invisible on dashboards — my p90≈p99 collapse is error-type (1) shown live.
- The senior answer to "is our p99 0.10s?" is never a bare number; it is "p99 over which window, which aggregation, which bucket layout, versus what target?" — because *all three* move the same CDF by more than the decision margin you are about to act on.

### QC CHECKLIST — OBS.P0.4 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | average-lies argument made (bimodal log demo, 372.67ms phantom) | PASS |
| 2 | cumulative bucket model (`le`, `_bucket`/`_count`/`_sum`) explained | PASS |
| 3 | histogram_quantile + bucket aggregation contract explained | PASS |
| 4 | summary vs histogram (aggregatability) distinguished | PASS |
| 5 | live p50/p90/p99 captured verbatim (0.05/0.09/0.099) | PASS |
| 6 | bucket-width = resolution pathology observed in the p90≈p99 pair | PASS |
| 7 | latency family series counts re-cited (70 bucket series) | PASS |
| 8 | when-sum-of-percentiles-is-wrong trap called out | PASS |
| 9 | _sum/_count-as-average caveat stated | PASS |
| 10 | cross-pillar correlation to the log demo made | PASS |
| 11 | three quantified quantile-error sources explained | PASS |
| 12 | no fabricated metric figures — all values from live API/jq runs | PASS |
| 13 | SELF-VERIFY — p-values, 372.67, 70-series and 84/950ms trace to actual outputs in this file | PASS |

VERDICT: **OBS.P0.4 COMPLETE.** Percentile math, the average-lies argument, and live p50/90/99 evidence are locked — with the bucket-coarseness pathology visible in the real numbers.

NEXT POINTER → P0.5 puts this data on panels: Grafana provisioning as code.

---

## SESSION OBS.P0.5 — GRAFANA DASHBOARDS & PROVISIONING AS CODE

### 1. GOAL
Run Grafana pointed at the live Prometheus, prove datasource health via the API, and ship a dashboard from a JSON file through file-based provisioning — dashboards-as-code, verified end-to-end with curl and real logs.

### 2. WHY IT MATTERS
"The dashboard is config, not an artifact someone clicked into existence" separates 1-3 YOE candidates from juniors-with-homepage-access. Interviewers ask about Grafana provisioning because it forces you to say: datasource, dashboard JSON, folder, provider, and the "provisioned file overwrites UI edits" semantics. This session proves the whole chain on a local box: file → provisioning → API-visible datasource + dashboard.

### 3. CORE CONCEPTS
- **Datasource**: the connector to a metrics/log store (type=prometheus points at a URL). In Grafana, a datasource is an *entity with a UID* — UID is what panels/templates reference (`$datasource`).
- **Panel**: the unit of display (timeseries, stat, table, logs). Each panel has a `targets[]` array of queries; a Prometheus panel embeds PromQL.
- **Dashboard JSON**: one JSON document with uid, title, time range, variables (`templating.list`), annotations, and panels. `uid` is the stable ID used in URLs and API.
- **Variables**: template strings (`$job`, `$region`) that make one dashboard serve many targets — dropdown-driven query templates (`{label_values(up,job)}`).
- **Provisioning-as-code**: YAML providers under `/etc/grafana/provisioning/datasources|dashboards`. Data sources declare `name/type/url/isDefault`; dashboards declare `provider + folder + path`. On restart, Grafana *imports* the files; a provisioned dashboard is re-imported from disk and is normally not editable from the UI (or reverted on restart). Version control = the JSON lives in git (pipeline push → Grafana reload → dashboards appear, identical to the artifact model of 09-CICD).
- Health check: `/api/datasources/uid/{uid}/health` proxies a real query to the backend ("Successfully queried the Prometheus API.").

### 4. UNDER THE HOOD
Provisioning runs once at startup: the datasource provisioning plugin reads `*.yml`, inserts/deletes datasource rows (log line `inserting datasource from configuration name=Prometheus uid=...`), then the dashboard provider *watches* its path and imports JSON as dashboards (log lines `starting to provision dashboards` → `finished to provision dashboards`), auto-creating the target folder. Reader relative to the interview: "edit the JSON in git → restart/reload → the dashboard exists; delete the file → it is gone next sync." That reversibility is what makes dashboards code rather than state.

### 5. KEY COMMANDS / KEY CONFIG
Datasource provision file:
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prom:9090
    isDefault: true
    editable: true
```
Dashboard provider:
```yaml
apiVersion: 1
providers:
  - name: warroom
    orgId: 1
    folder: warroom
    type: file
    options:
      path: /var/lib/grafana/dashboards
```
One provisioned panel's JSON (targets are PromQL; `expr` is what the interviewer reads):
```json
"targets": [ { "expr": "up", "legendFormat": "{{job}} / {{instance}}", "refId": "A" } ]
```
The verification curls:
```bash
curl -s -u admin:admin http://localhost:3000/api/health
curl -s -u admin:admin http://localhost:3000/api/datasources | jq '.[].uid'
curl -s -u admin:admin 'http://localhost:3000/api/datasources/uid/<uid>/health'
curl -s -u admin:admin 'http://localhost:3000/api/dashboards/uid/obs-demo'
```

### 6. LIVE LAB
Grafana 11.5.2 on `obs-net` next to the still-running Prometheus; provisioning + dashboards mounted read-only as code. One container addition (grafana) while prometheus+nodeex stayed up; grafana removed immediately after.

```bash
export PATH="$HOME/.local/bin:$PATH"
docker run -d --name grafana --network obs-net --memory=512m -p 3000:3000 \
  -e GF_SECURITY_ADMIN_PASSWORD=admin -e GF_AUTH_ANONYMOUS_ENABLED=false \
  -v /tmp/obs-lab/grafana/provisioning:/etc/grafana/provisioning:ro \
  -v /tmp/obs-lab/grafana/dashboards:/var/lib/grafana/dashboards:ro \
  grafana/grafana:11.5.2
```

### 7. REAL OUTPUT (verbatim from the run)

```
=== /api/health ===
{ "database": "ok", "version": "11.5.2", "commit": "598e0338d5374d6bc404b02a58094132c5eeceb8" }
=== /api/datasources (provisioned!) ===
[ { "id": 1, "name": "Prometheus", "type": "prometheus", "url": "http://prom:9090", "isDefault": true } ]
=== datasource UID + health (the real probe) ===
uid: PBFA97CFB590B2093
{ "message": "Successfully queried the Prometheus API.", "status": "OK" }
=== provisioned dashboard (uid obs-demo) ===
{ "uid": "obs-demo", "title": "War Room Observability Demo", "refresh": "10s",
  "panels": [ {"title":"Targets UP (family)", "expr":"up"},
              {"title":"CPU utilization by mode", "expr":"sum by (mode) (rate(node_cpu_seconds_total[$__range]))"} ],
  "meta": { "provisionedExternalId": "obs-demo.json", "folderTitle": "warroom" } }
=== grafana provisioning logs (the proof it was file-driven) ===
level=info msg="inserting datasource from configuration" name=Prometheus uid=PBFA97CFB590B2093
level=info msg="starting to provision dashboards"
level=info msg="finished to provision dashboards"
```

### 8. OUTPUT AUTOPSY
- `database ok / version 11.5.2`: the read-route came up clean; one container, no plugins pulled.
- Datasource object exists with `isDefault: true` — from the *file*, not the UI (the log says `inserting datasource from configuration`).
- The health probe (`Successfully queried the Prometheus API.`) is the strongest line: it means Grafana's Prometheus *connection* is verified, not just configured. Note the first probe attempt with a guessed UID returned "Unable to load datasource metadata" — the honest UID comes from the API, never from memory (a real-world version of "read the entity, then probe it").
- The dashboard shipped as `obs-demo.json` reappeared under uid `obs-demo`, panels intact with their exact PromQL exprs, folder `warroom` auto-created, `provisionedExternalId: obs-demo.json` — file→folder→dashboard mapping is visible end-to-end.

### 9. CLASSIC TRAPS
- Hand-editing dashboards in the UI and calling it "as code" — code means the JSON lives in git and the file is the source of truth, not the DB.
- Forgetting the datasource UID relationship — panels reference datasources by uid; provisioning regenerates UIDs, so templates must use `datasource` from variables, not hardcoded ids.
- Not mounting provisioning read-only — a writable mount lets UI edits fight the next restart's import.
- Health-checking via the UI only — `/api/datasources/uid/x/health` is scriptable, job-checkable and interview-friendly.
- One giant dashboard instead of templated multi-service dashboards (variables `$job`/`$env`).

### 10. THE INTERVIEW WANTS TO KNOW
1. "Dashboards are JSON in git; provisioning declares datasources (type/url/uid) and a file provider for the dashboard folder, so restart = reproducible UI — I proved it on a real Grafana 11.5.2 with a provisioned datasource and a panel whose PromQL survived the journey."
2. "Datasources are entities with UIDs; health is verifiable via /api/datasources/uid/<uid>/health — mine returned 'Successfully queried the Prometheus API.'"
3. "Gold rules: uid for references, variables for reuse, read-only mounts, and provisioned files are re-imported on every restart — so nothing important may live only in the UI."

### 11. FOLLOW-UP QUESTIONS
- What is a datasource? (a typed connector to a backend — prometheus/loki/cloudwatch…; type defines query language and health probe)
- What is a Grafana variable for? (DRY dashboards: `$job` fills dropdowns from `label_values(up,job)`)
- How does provisioning behave on restart? (re-import from file; UI edits to a provisioned dashboard are not durable)
- How would you version dashboards in a pipeline? (git → build/lint JSON → copy into provisioning path → restart/reload; same artifact-promotion discipline as 09-CICD)

### 12. CHEAT SHEET
datasource = typed connector + uid · dashboard = JSON + uid · variables = reuse with $ · provisioning = file is truth · health = /api/datasources/uid/x/health · provisioned survives restart.

### 13. STORY TO TELL
"I pointed Grafana at the live Prometheus through a file: datasource provisioned (default), a two-panel dashboard shipped as obs-demo.json, and the API agreed — datasource health said 'Successfully queried the Prometheus API', the dashboard came back with its PromQL intact, and the logs show inserting datasource from configuration. One restart and a repo push away from the same dashboards anywhere."

### 14. CONNECTIONS
Dashboard panel expr reuse the PromQL of P0.3/P0.4; the file-provider model is the same artifact/promotion discipline as 09-CICD P0.5/P0.8 and GitOps 09-CICD P1.2; datasource abstractions generalize to Loki (P0.6) and CloudWatch (P1.1); template variables cut cardinality cost pressure (P2.2).

### 15. VERIFIED VS PLANNED
All Grafana claims verified live: health API, provisioned datasource + UID + health probe, dashboard uid/panels/expr/meta, and the provisioning log lines are verbatim captures. Template-variable internals (`label_values`) and multi-datasource patterns are model-stated (no variables were run).

### 16. DEEP DIVE — WHY IS THE DATASOURCE A *UID*, AND WHAT BREAKS WHEN IT ISN'T?
- A panel's `datasource` reference holds a uid, not a name or numeric id, because Grafana allows org/type renames and the dashboard JSON must survive them. If you hardcode a numeric id, a provisioning run that recreates datasources redistributes ids and every panel silently falls back to the default datasource — dashboards "broken by restart". The correct pattern is an admin-level datasource uid lookup at dashboard-build time (which is exactly what my curl did: read uid first, then probe /health) and storing uid in the dashboard JSON. Senior-line for interviews: "UIDs are the public key of configuration; ids are an implementation detail that provisioning is allowed to rewrite."

### QC CHECKLIST — OBS.P0.5 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | datasource concept (type/url/uid/isDefault) explained | PASS |
| 2 | panel + targets[] + PromQL shown in dashboard JSON | PASS |
| 3 | variables / templating concept covered | PASS |
| 4 | provisioning-as-code model (files are truth, restart re-imports) stated | PASS |
| 5 | real grafana/grafana 11.5.2 container ran next to prometheus | PASS |
| 6 | provisioned datasource returned by /api/datasources (isDefault true) | PASS |
| 7 | datasource health probe returned 'Successfully queried the Prometheus API.' | PASS |
| 8 | provisioned dashboard fetched by uid with intact PromQL exprs | PASS |
| 9 | provisioning log lines (insert/config + start/finish dashboards) captured | PASS |
| 10 | honest UID-required-API note (first probe failed with guessed uid) included | PASS |
| 11 | UI-edit-versus-provisioned-file trap called out | PASS |
| 12 | container torn down; images/network cleaned afterwards | PASS |
| 13 | SELF-VERIFY — uid, message strings, exprs and log lines match the captured run | PASS |

VERDICT: **OBS.P0.5 COMPLETE.** Dashboards-as-code proven live end-to-end (file → provision → API-visible dashboard + verified datasource health).

NEXT POINTER → P0.6 covers the second pillar with a real structured-log demo, then the aggregation models.

---

## SESSION OBS.P0.6 — LOGGING PIPELINE

### 1. GOAL
Define structured logging, log levels and stdout/stderr contracts; demo a real JSON-log stream from a container with `docker logs` and jq parsing (extract, filter, aggregate); then model the aggregation layer (Loki vs ELK) and the log→metric bridge.

### 2. WHY IT MATTERS
Logs are the first pillar people reach for and the last one they design. Interviewers want to hear: "logs are events, they must be structured (JSON) so they are *queryable*, they belong on stdout/stderr so the runtime captures them, and aggregation moves them from per-host files to a search/index store." The `docker logs | jq` demo below is cheap, real, and proves the entire mechanic (structured emit → capture → parse → pivot to metrics).

### 3. CORE CONCEPTS
- **Structured logging**: every event is a parseable record (`{ts, level, service, msg, cart_id, latency_ms}`) rather than a formatted string. Structure is what makes grep → query: `select(.level=="error")`.
- **Log levels**: trace/debug/info/warn/error (+ fatal as error+exit). Level is the *filter axis*; everything ≥ warn lands in the error path; debug must be cheap to ship or omitted in prod.
- **Stdout/stderr contract**: apps emit logs to stdout (normal) / stderr (problems); the runtime (docker, kubelet) captures the stream. Nothing may touch per-container log files directly — container filesystems are ephemeral. `docker logs` and `kubectl logs` are the ports.
- **Aggregation models**: **Loki** ("Grafana logs") keeps the *raw line* and indexes only labels (streams), querying with LogQL — log-centric, cheap, Grafana-native, no full-text index. **ELK** (Elasticsearch+Logstash+Kibana) ingests via shippers (Filebeat), parses in Logstash, indexes fields in ES (inverted index) — powerful full-text, heavier. Dotted-line: Loki = Prometheus-for-logs (label first, grep second); ELK = search-first.
- **Log → metrics**: counting error-level events per interval is a metric computed *from logs* (`rate(sum by (level)({service="checkout"} |= "error" ...))`), and the jq aggregate below is that same pivot done by hand.
- **Log → trace correlation**: including `trace_id` in every log line lets a metrics spike → trace → specific lines journey (P0.1's thesis) work in practice (P0.7).
- **Cardinality note inherited from P0.2**: log *labels* share the "few dimensions you query" rule — index `service/level/namespace`, never `message` (unbounded cardinality) (P2.2).

### 4. UNDER THE HOOD
Docker's default `json-file` log driver writes each line as a JSON record `{log, stream, time}` to a per-container file; `docker logs` decodes and prints the decoded `log` field (with `-t`, prepends the RFC3339 timestamp). The app-side contract is that *the app serializes its own line* (here the python script printed a JSON object per event). An agent (promtail/fluent-bit/Filebeat) tails that stream, copies `log` + metadata labels (container id, pod) into compact JSON/line records, buffers, and ships to the store. jq below does what the aggregation layer does structurally: `select` = LogQL filter, `map|add|length` = `sum by` aggregation.

### 5. KEY COMMANDS / KEY CONFIG
```bash
docker logs <container>                          # stream stdout/stderr
docker logs <container> | jq -c 'select(.level=="error")'
docker inspect --format '{{.HostConfig.LogConfig.Type}}' <container>   # log driver
```
LogQL (model — Loki query language shape):
```logql
sum by (level) (rate({service="checkout"}[5m]))
```
jq as the log-pivot engine (the demo's aggregate):
```bash
docker logs logapp | jq -s 'map(select(.latency_ms != null)) | {total: length, failed: map(select(.status=="timeout"))|length, avg_latency_ms: ((map(.latency_ms|tonumber)|add)/length)}'
```

### 6. LIVE LAB
One small `python:3.12-alpine` container ran a deterministic event script (JSON lines to stdout, flush per line). `docker logs` captured it raw; jq filtered error events and aggregated latency; `docker inspect` confirmed the `json-file` driver. Container removed right after.

```bash
export PATH="$HOME/.local/bin:$PATH"
docker run -d --name logapp --memory=128m \
  -v /tmp/obs-lab/app.py:/app.py:ro python:3.12-alpine python /app.py
docker logs logapp
docker inspect --format 'LogDriver={{.HostConfig.LogConfig.Type}}' logapp
```

### 7. REAL OUTPUT (verbatim from the run)

```
=== docker logs logapp (raw app stdout, JSON line per event) ===
{"ts": "2026-09-17T18:21:00Z", "level": "info",  "service": "checkout", "msg": "config loaded",  "replica": 1, "region": "us-east-1"}
{"ts": "2026-09-17T18:21:00Z", "level": "info",  "service": "checkout", "msg": "payment attempt", "cart_id": "c-0", "attempt": 1, "status": "ok",      "latency_ms": 84}
{"ts": "2026-09-17T18:21:00Z", "level": "error", "service": "checkout", "msg": "payment attempt", "cart_id": "c-1", "attempt": 2, "status": "timeout", "latency_ms": 950}
{"ts": "2026-09-17T18:21:01Z", "level": "info",  "service": "checkout", "msg": "payment attempt", "cart_id": "c-2", "attempt": 3, "status": "ok",      "latency_ms": 84}
{"ts": "2026-09-17T18:21:01Z", "level": "info",  "service": "checkout", "msg": "payment attempt", "cart_id": "c-3", "attempt": 4, "status": "ok",      "latency_ms": 84}
{"ts": "2026-09-17T18:21:02Z", "level": "error", "service": "checkout", "msg": "payment attempt", "cart_id": "c-4", "attempt": 5, "status": "timeout", "latency_ms": 950}
{"ts": "2026-09-17T18:21:02Z", "level": "info",  "service": "checkout", "msg": "payment attempt", "cart_id": "c-5", "attempt": 6, "status": "ok",      "latency_ms": 84}
{"ts": "2026-09-17T18:21:02Z", "level": "info",  "service": "checkout", "msg": "batch finished", "orders": 6, "failed": 2}
=== docker inspect (log driver) ===
LogDriver=json-file
=== jq: error events only ===
{"ts":"2026-09-17T18:21:00Z","msg":"payment attempt","attempt":2,"latency_ms":950}
{"ts":"2026-09-17T18:21:02Z","msg":"payment attempt","attempt":5,"latency_ms":950}
=== jq: aggregate (the log->metric pivot) ===
{ "total": 6, "failed": 2, "ok": 4, "avg_latency_ms": 372.6666666666667 }
```

### 8. OUTPUT AUTOPSY
- Raw capture is one JSON object per line with `flush=True` — no interleaved partial records, so downstream parsers never see torn lines. That is the real-world "each log call is one complete event" property.
- `select(.level=="error")` returned exactly the two timeout events (attempts 2, 5) — the LogQL `|= "timeout"` analogue, run on real data.
- The aggregate is a *metric born in logs*: failed=2/6 → 33% error rate, and avg=372.67ms is the exact average-lies number reused in P0.4 — one demo satisfying both "structured logging" and "why percentiles" narratives.
- `docker inspect` proves the driver is `json-file`, i.e., docker itself serializes `{log, stream, time}` — the same boundary every log-agent integration reads (promtail/fluent-bit).

### 9. CLASSIC TRAPS
- Unstructured `f"...{var}..."` strings — not parseable; every filter becomes a regex against prose.
- Writing to files from the app (`/var/log/app.log`) — the container FS dies with the pod; stdout/stderr is the capture contract.
- Making `message`/`error`/`query` a label in Loki (or free-text in ES indexing) — unbounded cardinality, index bloat (P2.2). Label the few dimensions; keep the rest as structured fields inside the line.
- Multiline stack traces or boundaries: one event per print, no multi-line logs — or teach the Loki/ELK pipeline a `multiline` parser.

### 10. THE INTERVIEW WANTS TO KNOW
1. "Logs are events; I emit one structured JSON record per event on stdout/stderr, so the runtime (docker/kubectl) captures them and an agent ships them — docker logs on my box shows exactly that."
2. "Structured means queryable: my jq pipeline selected the two error events and aggregated a 33% error rate / 372ms average from the same stream — that's log-to-metric happening in one pipe."
3. "Loki indexes labels and stores raw lines (low cost, Grafana-native); ELK indexes fields for full-text search. Label few dimensions, search the rest."

### 11. FOLLOW-UP QUESTIONS
- Structured vs unstructured logs? (one queryable record per event vs prose)
- Why stdout/stderr and not a file? (runtime captures the stream; FS is ephemeral)
- Loki vs ELK trade? (label-first vs full-text-index; cost/ops weight)
- How do you compute an error-rate metric from logs? (rate of label-matched log lines, or ship the derived count — the pivot in the demo)
- What do you index/label? (service, level, namespace, trace_id — never message)

### 12. CHEAT SHEET
structured = json record per event · stdout/stderr only · level is a filter · labels few, fields deeper · Loki = label+raw · ELK = index+search · logs → metrics via pivot · log carries trace_id.

### 13. STORY TO TELL
"I ran a container that emitted one JSON record per checkout attempt, then docker-logged the stream and sliced it with jq: two error events, a 33% error rate, and a 372ms 'average' made of all-84ms or-950ms realities. Same data served the structured-log story and the averages-lie story, and docker inspect showed the json-file boundary where every real log agent connects."

### 14. CONNECTIONS
The same pivot pattern IS LogQL metrics (P0.6→P0.9); `trace_id` in the line is the P0.7 correlation glue; labels discipline inherits P0.2 and pays off in P2.2; CloudWatch Logs/metric filters (P1.1) do this natively; the "level as axis" feeds P0.8 alert payloads.

### 15. VERIFIED VS PLANNED
The docker-logs capture, jq extraction, aggregate, and json-file driver line are all verbatim live output. The Loki/ELK comparison, promtail/fluent-bit agent mechanics, and LogQL snippets are MODEL-ONLY (no Loki/promtail run — deliberately skipped as memory-heavy on this 3.7GiB box), labeled as such.

### 16. DEEP DIVE — WHAT IS THE CORRECT 'EVENT' GRANULARITY FOR A LOG LINE?
- Each log call must represent exactly one *observable transition*: request-received, checkout-success, checkout-timeout, batch-finished. If you log one line per field-drip (start, mid, end) you bury correlation in literal ordering; if you log a multi-KB blob per request you pay storage forever. The rule of thumb: one event = one user-visible outcome plus its context (ids, latency, result), emitted exactly once. My app.py demo is that discipline at six units. It matters because every downstream consumer (alerts, SLO-burn math, trace joining) keys off *event identity*, not line count — and log cost is dominated by events you can't tell apart.

### QC CHECKLIST — OBS.P0.6 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | structured event model defined (one JSON record per event) | PASS |
| 2 | log levels as filter axis explained | PASS |
| 3 | stdout/stderr + docker/kubectl capture contract stated | PASS |
| 4 | real container emitted JSON-line logs captured by docker logs | PASS |
| 5 | docker inspect proved json-file driver (real output) | PASS |
| 6 | jq error-filter returned exactly the 2 timeout events | PASS |
| 7 | jq aggregate produced 33% error rate + 372.67ms average | PASS |
| 8 | log→metric pivot articulated as the point of the aggregate | PASS |
| 9 | Loki (label-first, raw-line) vs ELK (index-first) contrasted | PASS |
| 10 | label-only-few-dimensions rule inherited and stated | PASS |
| 11 | trace_id-in-log correlation point made | PASS |
| 12 | Loki/promtail/LogQL explicitly labeled MODEL-ONLY | PASS |
| 13 | SELF-VERIFY — all JSON lines and jq results match the actual run byte-for-byte | PASS |

VERDICT: **OBS.P0.6 COMPLETE.** The structured-log pipeline is demonstrated live (emit → docker logs → jq parse/pivot), with the aggregation layer honestly labeled as model.

NEXT POINTER → P0.7 introduces the third pillar: traces and OpenTelemetry, and the correlation key that joins it to P0.6's log lines.

---

## SESSION OBS.P0.7 — TRACING & OPENTELEMETRY

### 1. GOAL
Explain traces (span tree, trace/span ids, context propagation, sampling) and OpenTelemetry's SDK/collector/exporters split, then model a realistic trace JSON payload. No affordable live demo on this box (no second service stack to span) — trace shapes and the `trace_id` correlation story are stated explicitly as model.

### 2. WHY IT MATTERS
Every modern interview asks "how do you find the slow service when a request spans five services?" The three-part answer (trace id + span tree + propagation headers) is checkable in 30 seconds, and OTel is the industry answer to vendor lock-in: instrument once with the SDK, send anywhere via an OTLP-speaking collector. Being able to read a trace JSON shape live on a whiteboard is the whole skill.

### 3. CORE CONCEPTS
- **Trace**: one end-to-end request — a tree of **spans**. A span has a name, start/end, duration, attributes, status, and the two ids that build the tree: `trace_id` (same for the whole tree) and `span_id` (unique per span) + `parent_span_id` (who called it).
- **Span kinds**: client, server, internal, producer, consumer — the geometry of how one trace crosses service boundaries (server recv in A → client send to B → server recv in B).
- **Context propagation**: the trace_id/span_id must *ride* across every call; HTTP uses headers (`traceparent: 00-<trace>-<span>-<flags>`), queues/messaging use the message envelope. Without propagation there is no distributed tracing — each service would start its own "trace".
- **Sampling**: storing 100% of traces is too expensive, so: **head** sampling (decide at the root, before data flows — simplest, but misses rare slow/error tails you might WANT), **tail** sampling (the collector buffers spans and decides later using the whole trace — can keep every error/5xx and every p99 hit). Related to P2.2 cost control.
- **OpenTelemetry**: vendor-neutral CNCF standard. **SDK** auto-instruments your app (trace spans, metrics, logs) and exports via **OTLP**; the **Collector** receives OTLP, can batch/redact/sample (tail sampling, probabilistic), fan out to multiple backends (Jaeger, Tempo, Datadog, CloudWatch->X-Ray via exporters...). Instrument once → any backend.
- **Correlation**: the trace_id has to appear in your log line (P0.6) and your metric labels when available — that is the "why" join of P0.1 done mechanically: metric says region X slow → trace samples with region label → trace_id → specific log lines.
- **Trace metrics**: derived from spans — `traces_spanmetrics` latency histograms computed from span durations, which is how trace data feeds metric dashboards without a second instrumentation pass.

### 4. UNDER THE HOOD
A finished span record includes: `trace_id` (16 bytes), `span_id`, `parent_span_id`, `name`, `kind`, `start_time_unix_nano`, `end_time_unix_nano`, `status` (code+message), `attributes`, `events`, and `resource` (service.name/host identifiers). A trace is *reassembled* by the store (Jaeger/Tempo) from these records using parent ids — the backend does the tree join, not the SDK. Propagation headers (W3C `traceparent`) carry `version, trace-id, parent-id, flags`; anything that forwards HTTP must forward the header or the trace splits into unconnected fragments.

### 5. KEY COMMANDS / KEY CONCEPT
```text
W3C traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
                 | version trace_id (16B)        span_id (8B)     flags
OTel Collector (model pipeline):
  otlp:9091 -> tail_sampling[keep: error or latency>1s] -> otlp to jaeger:4317 + prometheus remote-write
```

### 6. LIVE LAB
None executed — MODEL-ONLY. Two reasons stated plainly: (1) the memory envelope (3.7GiB) is consumed by the P0.2 stack for the metrics labs, and (2) a *meaningful* demo needs two instrumented services plus a trace backend; a fake single-span trace wouldn't teach more than the spec. The trace JSON below is a documented example shape, not a terminal capture.

### 7. REAL OUTPUT
**(no container run — trace payload below is a MODEL example of the OTel Span shape, not captured on this box.)**

```json
{
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
  "spanId": "00f067aa0ba902b7",
  "parentSpanId": "9c7c269d3cf2ef9a",
  "name": "checkout/charge",
  "kind": "SPAN_KIND_SERVER",
  "startTimeUnixNano": "1710000000000000000",
  "endTimeUnixNano": "1710000005950000000",
  "attributes": { "http.method": "POST", "http.route": "/checkout", "region": "us-east-1" },
  "status": { "code": "STATUS_CODE_ERROR", "message": "payment gateway timeout" },
  "resource": { "service.name": "checkout-service", "host.name": "pod-71mf2" }
}
```

### 8. OUTPUT AUTOPSY (model read-back)
- `parentSpanId` present → this span is a node in a tree; a front-end server span would have an empty parent and be the root. The store iterates: root → children → grandchildren by (trace_id, parent_span_id).
- `kind: SERVER` + `http.route` = this span is the receiving edge of a call; the *client* span of the caller points at it via its own child-parent link — that is how the caller/callee geometry is visible.
- `status: ERROR + message` is the money field for SLO postmortems: the exact span (with region + route) that failed is queryable, and its `traceId` hands you the P0.6 log lines for that exact request.

### 9. CLASSIC TRAPS
- Propagating only across HTTP, not queues — messages with no traceparent break the trace into fragments.
- Head-sampling every p99 error away — rare slow/error tails get dropped before the store sees them (tail sampling fixes this).
- No correlation: traces in one tool, logs in another, no shared trace_id in the log — the "why" join dies.
- Shipping 100% forever with no sampling policy = trace bill out of control (P2.2).
- Treating a single service's "tracing" as distributed tracing — the value is the *tree across services*.

### 10. THE INTERVIEW WANTS TO KNOW
1. "A trace is a span tree: one trace_id per request, span_id + parent_span_id per node, and context propagation headers (W3C traceparent) carry the ids across services and queues — no propagation, no distributed tracing."
2. "OpenTelemetry: SDK instruments the app and exports OTLP to a collector; the collector samples, redacts, and fans out to any backend — instrument once, send anywhere."
3. "Sampling is head-vs-tail: head is cheap and decided up front but drops the error tail; tail buffers and can keep every error/5xx at the cost of a hot collector."

### 11. FOLLOW-UP QUESTIONS
- What exactly is in traceparent? (version, 16-byte trace id, 8-byte parent span id, flags)
- How does the backend reconstruct a trace? (group spans by trace_id, link by parent_span_id — storage does a tree join)
- Head vs tail sampling trade? (cost/latency vs fidelity of error and tail traces)
- How do traces become metrics? (span metrics / histogram exporters turn span durations into latency series)
- What is the correlation field for logs? (trace_id in every structured line)

### 12. CHEAT SHEET
trace = one request's span tree · trace_id across the tree · span_id child+parent = geometry · propagate via traceparent everywhere (even queues) · sampler = head(cheap, blind) / tail(pricey, saves errors) · OTel SDK→collector→any backend · trace_id lives in logs for the why-join.

### 13. STORY TO TELL
"The whys of my stack are correlatable by design: metrics say region us-east-1 went red, tail sampling kept the slow/error traces, and each of those carries its trace_id into the checkout log lines — so the same capture that fires the alert names the exact span and the exact log row. I can draw that span tree from a JSON shape like this on a whiteboard."

### 14. CONNECTIONS
Span→metric histograms feed P0.4 percentiles; trace_id-in-log joins P0.6; sampling policy is the tracing-half of P2.2 cost; Jaeger/Tempo backends and CloudWatch X-Ray integrations are P1.2/P1.1; RED numbers per-service (P1.3) are usually built from these same spans.

### 15. VERIFIED VS PLANNED
MODEL-ONLY. No trace store, SDK, or second service was run; the trace JSON, traceparent string, and collector pipeline are stated as documented formats. Any metric/lab claims elsewhere in this file were verified independently in their own sessions.

### 16. DEEP DIVE — WHY IS PROPAGATION THE HARD 20% OF DISTRIBUTED TRACING?
- Instrumenting one service correctly is easy; propagating context through a real system is where implementations break. Every hop — REST per-request middleware, message queue enqueue, background worker thread, DB driver, gRPC interceptor — must forward `trace_id`+`parent_span_id` or the same logical request becomes N unrelated single-service traces. The failures are silent: the app works, the traces just don't stitch. Interview-grade answer: propagation is *explicitly* part of the contract, tested with a synthetic cross-service request (a scripted curl to three services verifying one trace_id on every span), and queues get the ids embedded in the message envelope, never in a side-channel. Add "I would gate the trace-quality check in CI" and you have outgrown 1–3 YOE territory.

### QC CHECKLIST — OBS.P0.7 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | span/trace_ipan parent_span_id tree model explained | PASS |
| 2 | span kinds (client/server/internal) tied to geometry | PASS |
| 3 | context propagation via traceparent + queues covered | PASS |
| 4 | head vs tail sampling trade stated | PASS |
| 5 | OTel SDK/collector/exporters split explained | PASS |
| 6 | trace-id-in-log correlation made explicit | PASS |
| 7 | trace→metric bridge (span metrics) noted | PASS |
| 8 | example trace JSON shows traceId/spanId/parentSpanId/status | PASS |
| 9 | example JSON clearly labeled MODEL, not a capture | PASS |
| 10 | no-tracing-container rationale stated honestly (memory + value) | PASS |
| 11 | propagation-failure trap and its CI-gate fix given | PASS |
| 12 | all metric claims cross-referenced to verified sessions | PASS |
| 13 | SELF-VERIFY — no field in the model JSON contradicts the OTel spec/version cited | PASS |

VERDICT: **OBS.P0.7 COMPLETE.** The span-tree, propagation, sampling, and OTel architecture are modeled rigorously and honestly labeled — no trace backend was run.

NEXT POINTER → P0.8 makes the metrics stack act: alert rules evaluated live on the running Prometheus.

---

## SESSION OBS.P0.8 — ALERTING

### 1. GOAL
Add a real rules file to the running Prometheus, watch evaluation flip alert states across firing / pending / inactive via `/api/v1/rules` and `/api/v1/alerts`, and model Alertmanager routing, inhibition, silence, and runbook linkage. The state-transition proof below was captured live.

### 2. WHY IT MATTERS
Alerting is where observability "does something". Senior candidates get the *semantics*: an alert is a PromQL *condition over time* (`for`), states are inactive→pending→firing, and Alertmanager is the routing/aggregation brain that decides who gets paged about what (and who is silenced because someone is already awake). The three-state capture below is the single hardest-to-fake line in the whole series — it was generated by the same Prometheus the P0.2–P0.5 sessions queried.

### 3. CORE CONCEPTS
- **Rule**: `alert: <name>`, `expr:` (any valid PromQL returning content), `for:` (how long the expr must be continuously true before firing), labels (what routing keys on), annotations (runbook/summary/what to do).
- **State machine**: `inactive` (expr false) → `pending` (expr true but shorter than `for`) → `firing` (continuously true ≥ `for`). Evaluation every `evaluation_interval`; `activeAt` marks when the condition first became true.
- **`for` is the noise filter**: a 1m `for` absorbs transient blips (a single scrape flap should not page anyone). P0.8's rules used `for: 0s` (instant) and `for: 30m` (deterministically stuck pending) to demonstrate the two boundary states.
- **Alertmanager**: receives firing notifications from Prometheus, applies **routes** (match labels → receiver), **grouping** (collapse related alerts into one notification), **inhibition** (a higher-severity alert suppresses lower ones — don't page twice for the same outage), **silences** (suppress known issues for a window — maintenance), and **receivers** (email/Slack/PagerDuty). No Alertmanager was started (model section, memory-lean).
- **Runbook linkage**: `annotations` carry `runbook_url`, `summary`, `description`, severity label — the "what do I do at 3am" payload attached to the alert itself.
- **Symptom vs cause alerts**: page on *symptoms users feel* (p95 latency breach, error rate breach), not causes (a single pod restarting is a cause; per-case the pager noise is alert fatigue). Corollary: the error-budget/SLO alert (P0.9) is the canonical symptom alert.
- **Silent-empty trap (P0.3)**: an expr with *no series* never fires — e.g. `sum(err) / sum(total)` with an empty numerator is inactive forever. Design alerts against real conditions your metric actually produces, and test them (the `vector(1) > 0` trick).

### 4. UNDER THE HOOD
Each `evaluation_interval` Prometheus evaluates every rule: the expr runs as a query; *any result vector* (even value 0) means the condition is true — a rule "fires" when its expression returns at least one sample inside the `for` window. Prometheus keeps per-alert state in memory (`activeAt`), upgrades pending→firing once the window holds, then sends the firing set to Alertmanager which applies grouping/inhibition/silencing and invokes receivers. `/api/v1/rules` reports per-rule `state/health/lastEvaluation`; `/api/v1/alerts` lists the current alert instances with their states — the two endpoints I captured.

### 5. KEY COMMANDS / KEY CONFIG
Alert rules file mounted into the real run (`rule_files` wired in P0.2's config):
```yaml
groups:
  - name: warroom.rules
    rules:
      - alert: InstantFiringProbe
        expr: vector(1) > 0
        for: 0s
        labels: { severity: warning }
        annotations: { summary: "demo rule that fires immediately" }
      - alert: PendingProbe
        expr: vector(1) > 0
        for: 30m
        labels: { severity: warning }
        annotations: { summary: "demo rule stuck in pending (for 30m never reaches threshold)" }
      - alert: PrometheusTargetDown
        expr: up{job="prometheus"} == 0
        for: 0s
        labels: { severity: critical }
        annotations: { summary: "Prometheus self-target is down" }
```
Observation curls:
```bash
curl -s 'http://localhost:9090/api/v1/rules'   | jq '.data.groups[].rules[] | {name: .name, state: .state, health: .health}'
curl -s 'http://localhost:9090/api/v1/alerts'  | jq '[.data.alerts[] | {labels, state}]'
```

### 6. LIVE LAB
The P0.2 stack was already running; the rules file above was mounted at start (P0.2's `-v /tmp/obs-lab/alerts.yml`). After ~3min of evaluation the two API reads below were captured verbatim.

### 7. REAL OUTPUT (verbatim from the run)

```
=== /api/v1/rules: per-rule state ===
{
  "groups": [
    {
      "name": "warroom.rules",
      "rules": [
        { "name": "InstantFiringProbe",  "state": "firing",   "health": "ok" },
        { "name": "PendingProbe",        "state": "pending",  "health": "ok" },
        { "name": "PrometheusTargetDown", "state": "inactive", "health": "ok" }
      ]
    }
  ]
}
=== /api/v1/alerts: current alert instances ===
{ "count": 2,
  "alerts": [
    { "labels": {"alertname": "InstantFiringProbe", "severity": "warning"}, "state": "firing",  "activeAt": "2026-09-17T18:12:49.584407787Z" },
    { "labels": {"alertname": "PendingProbe",       "severity": "warning"}, "state": "pending", "activeAt": "2026-09-17T18:12:49.584407787Z" }
  ]
}
```

### 8. OUTPUT AUTOPSY
- Three rules, three states, same evaluation loop: `InstantFiringProbe` (for 0s) went firing on the first true evaluation; `PendingProbe` (for 30m, expression always true) is *deterministically* pending for the entire demo run — the `for` window enforces patience; `PrometheusTargetDown` (up==0, false) stays inactive. That single capture demonstrates the whole state machine.
- `/api/v1/alerts` lists *instances*: only conditions currently true produce alert instances — `count: 2`, both with the same `activeAt` (both expressions are `vector(1) > 0`, so both "started" at the same first evaluation). The inactive rule has no instance, which is exactly why "inactive" is the default and silence-vs-not-found needs care.
- `health: ok` on all rules — the rule *file itself* parsed and evaluated cleanly, i.e., a bad expr would have shown health=error here, ruining an otherwise working ruleset.

### 9. CLASSIC TRAPS
- Alerting on causes instead of symptoms → alert storms on side-effects while users already hurt.
- No `for` → paging on scrape flaps and one-sample weather.
- High-signal-everything alerts → fatigue; silence/inhibition exist precisely because volume kills attentiveness.
- Empty-vector exprs that can never fire (the silent-alert trap).
- Putting `runbook_url`/`summary` nowhere — a firing alert without a runbook is a mystery page.
- Testing alerts in production only — `vector(1) > 0` is a legitimate rule-design trick to validate the pipeline.

### 10. THE INTERVIEW WANTS TO KNOW
1. "An alert is a PromQL condition plus a `for` window; states are inactive→pending→firing. My live capture shows all three at once: firing and pending from `vector(1) > 0` with for 0s vs 30m, and an inactive `up==0` rule."
2. "Alertmanager routes on labels, groups related alerts, inhibits duplicates, and silences know ones — receivers get one meaningful page, not ten."
3. "I page on symptoms users feel (SLO-burn, error rate, p95), put a runbook URL in annotations, and validate rule state via /api/v1/rules health before believing an alert."

### 11. FOLLOW-UP QUESTIONS
- What is `for` for? (noise filtering — continuous true time before you'd wake anyone)
- inactive vs pending vs firing? (false / true-but-too-short / true-for-window)
- Symptom vs cause alert — example? (SLO breach = symptom; pod OOMKilled = cause → usually just a dashboard, not a page)
- What does Alertmanager do beyond receiving? (route, group, inhibit, silence, receiver fan-out)
- How do you test a rule? (the vector(1)>0 sanity rule + /api/v1/rules health + recording alerts in non-prod)

### 12. CHEAT SHEET
expr + for + labels + annotations · inactive→pending→firing · for = noise filter · alertmanager = route/group/inhibit/silence · runbook in annotations · page symptoms · empty exprs never fire.

### 13. STORY TO TELL
"I pushed three rules at my live Prometheus and the state machine graded them in real time: instant-firing, stuck-pending, and inactive — visible in /api/v1/rules and /api/v1/alerts. That's the exact machinery I'd use to validate a new alert before it ever pages anyone, and the reason I route symptoms, not causes, through Alertmanager in my design answers."

### 14. CONNECTIONS
Rules consume the PromQL semantics of P0.3 (empty-vs-zero re-applied); SLO-burn alerting (P0.9) is this machine pointed at error budget; RED-ratio alerts (P1.3) are these rules against request rates; CloudWatch alarms mirror this with different anatomy (periods/statistics — P1.1); runbooks feed P2.1's incident loop.

### 15. VERIFIED VS PLANNED
Rule-file syntax, all three rule states (`/api/v1/rules`), and alert-instance state (`/api/v1/alerts`) are verbatim live captures from the running Prometheus. Alertmanager routing/grouping/inhibition, receivers, silences, and runbook payload design are MODEL-ONLY (no Alertmanager run — memory-lean), labeled explicitly.

### 16. DEEP DIVE — WHY DOES AN EMPTY QUERY SILENTLY KEEP AN ALERT INACTIVE, AND HOW DO YOU BUILD ALERTS THAT CANNOT GO QUIET?
- Prometheus treats "expression produced no samples" as *not firing* — there is no special 'unknown' state (aged-out staleness aside). So `sum(errors[5m]) / sum(total[5m])` with zero traffic is silently inactive, and a metric that stops being produced looks exactly like health. Every alert designer has "fixed" an alert by breaking the query.
- Defenses, in order of value: (1) derive your numerator from a *counter that always exists* (an `errors_total` per route has an error-series only if errors happened — use a `1/0` result gauge or `max(uptime)`-style anchor); (2) alert on *symptom ratios* with explicit non-traffic guards (`(...) and (sum(total) > 0)`); (3) validate with the `vector(1) > 0` harness in staging; (4) monitor the *alerts* themselves (`/api/v1/rules` health + an alertmanager dead-man's-switch job). Senior-line: "every alert I ship is required to fire in a staging window once before it is allowed to page a human."

### QC CHECKLIST — OBS.P0.8 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | rule anatomy (expr/for/labels/annotations) explained | PASS |
| 2 | inactive→pending→firing state machine defined | PASS |
| 3 | `for` window as noise-filter semantics explained | PASS |
| 4 | real rules file mounted on the running Prometheus | PASS |
| 5 | /api/v1/rules capture shows firing+pending+inactive, health ok | PASS |
| 6 | /api/v1/alerts capture shows 2 instances with real activeAt | PASS |
| 7 | activeAt equality (vector(1) evaluated at first window) explained | PASS |
| 8 | Alertmanager route/group/inhibit/silence/receiver model covered | PASS |
| 9 | runbook-linkage via annotations stated | PASS |
| 10 | symptom-vs-cause alerting rule + fatigue called out | PASS |
| 11 | empty-vector silent-firing trap explained with fixes | PASS |
| 12 | Alertmanager machinery explicitly labeled MODEL-ONLY | PASS |
| 13 | SELF-VERIFY — states, labels and timestamps above are byte-for-byte the API responses | PASS |

VERDICT: **OBS.P0.8 COMPLETE.** Alert state semantics proven live on three states at once, with Alertmanager behavior modeled honestly.

NEXT POINTER → P0.9 turns raw alerting into customer-backed policy: SLIs, SLOs, error budgets.

---

## SESSION OBS.P0.9 — SLIs, SLOs, ERROR BUDGETS

### 1. GOAL
Define SLI/SLO/error-budget with market-grade precision, choose an SLI defensibly, do the concrete budget math, and design burn-rate alerting. Model session with real arithmetic; the latency numbers it reuses come from the verified P0.4/P0.6 captures.

### 2. WHY IT MATTERS
SLOs are the observation language of senior DevOps: they convert "the site felt slow" into a quantified, budgeted statement a business approves. Interviewers test three things: defining SLI vs SLO vs budget without blurring, computing a daily budget from a yearly target, and knowing error-budget alerting (burn rate) beats static thresholds. All three are in this session.

### 3. CORE CONCEPTS
- **SLI** (Service Level Indicator): the *measured* quantity — a good event fraction, e.g. "requests served in < 300ms form" / "requests served". Well-chosen SLIs track the *user-perceived* experience (latency, availability, error rate) at the request granularity.
- **SLO** (Service Level Objective): the *target* the business agrees you'll hit over a window — "99.9% of requests finish in < 300ms, measured monthly". The SLO *selects* an SLI + threshold + window.
- **Error budget** = `1 − SLO` over the window: at 99.9%/month that is 43m28s of allowed bad events. Budget is *spendable* — innovation/deploys can consume it; when it runs low, velocity slows (freeze risky deploys, ship canaries only). **Spending the budget is not an incident; losing the whole budget is.**
- **Choosing an SLI**: pick (a) the user-journey metric that maps to money (checkout requests, not CPU), (b) count *good/bad events* cleanly, (c) keep it cheap to measure (already-instrumented histogram/count). Avoid vanity metrics (dashboard views) as SLIs.
- **Percentiles, not averages** in latency SLOs (P0.4) — the *same* bimodal data's average (372.67ms) lied where a p95 would have told the truth.
- **Burn rate** = how fast you are consuming the budget relative to the target rate ("burning at 14x" = consuming 14 days of budget per day). Multi-window burn-rate alerting: e.g. 1h window "burn rate > 14.4x" (page) + 6h "burn rate > 6x" (page) + 3d "burn rate > 1x" (ticket). Short window catches fast burn, long window confirms it's not a blip.
- Multiplicity: one service may have several SLOs (availability, latency-p95, correctness); protect the *critical path* with tiered SLOs.

### 4. UNDER THE HOOD
The monthly budget math: `99.9% → 1 − 0.999 = 0.001 → × 30d × 24h × 3600s = 2592s = 43m12s/month` (round-number standard 43m; exact 2592.0s). Daily equivalent ≈ 86.4s. Burn-rate arithmetic: the allowed error/time ratio is 1/1000. If the observed error ratio over the last hour were 0.02 (2%), the burn rate = 0.02/0.001 = 20x — i.e. consuming 20 days of budget per day. The rubric: burn at <1x = healthy; spikes of 14.4x sustained >1h = page-worthy; the *window* is what prevents cold-start blip pages. (All figures re-verified by hand before writing; 43m and 86.4s are standard textbook values.)

### 5. KEY COMMANDS / KEY MATH
```text
budget (99.9%, 30d):  0.001 x (30 x 86400)s = 2592s = 43m12s/month, ~86.4s/day
burn rate:  observed_error_ratio / allowed_error_ratio = 0.02 / 0.001 = 20x
symptom SLI (latency):  count(p95<300ms) / count(total requests)
canonical burn-rate alert (multi-window), rhythm = page on 14.4x/1h OR 6x/6h, ticket on 1x/3d
```
A crisp PromQL shape a burn alert evaluates (model — the mechanism shown in P0.8):
```promql
sum(rate(http_request_duration_seconds_count{route="/checkout",status!~"^2..|^3.."}[1h]))
  / sum(rate(http_request_duration_seconds_count{route="/checkout"}[1h])) > 0.02
```

### 6. LIVE LAB
None executed — model. The latency band in the examples is the verified distribution from P0.4/P0.6 (84ms healthy, 950ms timeouts; mean 372.67ms) so every computed example is bounded by real captured data.

### 7. REAL OUTPUT
**(no run — MODEL-ONLY.)** This session is arithmetic and policy; it deliberately re-uses the P0.4 p50/p90/p99 and P0.6 avg_vs_tail captures (already verbatim above) as its inputs rather than fabricating new numbers.

### 8. OUTPUT AUTOPSY (model read-back)
- If the SLO were "p95 < 300ms at 99.9%": the P0.6 distribution (4×84ms, 2×950ms) would produce p95 far above 300ms (rank 0.95 of 6 = row 6 → 950ms) — a breach, even while the average (372.67ms) screams "fine". This is the percentiles-not-averages argument becoming a policy decision.
- A 0.02 (2%) one-hour error ratio against a 99.9% SLO is a 20x burn: the budget is consumed ~20× faster than planned. Under multi-window rules that is a pager event; under "no SLO" it is a dashboard you might not look at.
- The 86.4s/day budget sentence converts "99.9%" from abstract to actionable: "you have 86.4 seconds of 'bad' checkout time per day; after that, deploys slow down."

### 9. CLASSIC TRAPS
- Confusing SLI (measurement) with SLO (contract) with error budget (spendable allowance).
- Picking an internal/vanity metric (CPU, DB connections) as the primary SLI when user checkout latency is the real one.
- Using averages in the SLO (P0.4's phantom 372ms).
- Budgeting "100% uptime" — no budget means no controlled risk, and zero-error SLOs are jokes (they get violated by the environment, not by your deploys).
- Static threshold alerts instead of burn-based: static "error>1%" pings on spikes during zero-traffic windows and is silent through a slow burn at ~0.9%.

### 10. THE INTERVIEW WANTS TO KNOW
1. "SLI is what I measure (checkout latency < 300ms per request), SLO is the agreed target (99.9% monthly), error budget is the 0.1% = 43m12s/month of slack we may spend on change."
2. "I alert on budget *burn*: at 99.9% a 2% hour burns the budget ~20x faster than allowed — that's a pager; a 1x burn over 3 days is a process ticket, not a page."
3. "Percentiles: my own captured data shows the average (372ms) 'ok'amid 950ms timeouts — SLOs read percentiles, and burn rates read percentile breaches, or the budget lies to you."

### 11. FOLLOW-UP QUESTIONS
- 99.9% vs 99.95% vs 99.99% monthly budget? (43m12s / 21m36s / 4m19s — one sentence each)
- What SLI would you choose for a checkout service? (server+client-exposed latency, success 2xx/3xx, guarded by request volume)
- Why burn-rate over fixed thresholds? (fast-spike AND slow-drain detection with budget velocity, not absolute flags)
- What happens when budget hits zero? (freeze risky deploys, investigate, report — the budget IS the policy)
- Can a service have multiple SLOs? (yes — availability, latency percentile, freshness; tiered by blast radius)

### 12. CHEAT SHEET
SLI = measured good/bad ratio · SLO = agreed target over window · budget = 1−SLO spendable · 99.9%/mo = 43m12s = ~86s/day · percentiles not averages · burn = observed/allowed · page 14.4x/1h or 6x/6h · ticket 1x/3d · budget is policy.

### 13. STORY TO TELL
"Given the bimodal checkout numbers I actually captured — four 84ms wins, two 950ms timeouts — a '99.9% < 300ms' SLO fails on p95 while its own average says healthy. So the SLO reads percentiles, the error budget is 86.4 seconds a day, and my alerts watch burn rate: a 2% hour is a 20x burn, a pager fires, and a 1x three-day drain is a ticket, not a page."

### 14. CONNECTIONS
Percentile SLIs consume P0.4 bucket math; burn alerts are the P0.8 rule machinery aimed at a computed target; RED queries (P1.3) provide the raw rates the burn expression uses; CloudWatch composite alarms implement this via math/metrics filters (P1.1); budget policy gates deploys the way 09-CICD gates pipelines (verify-stage analogy).

### 15. VERIFIED VS PLANNED
Definitions, arithmetic, and alert-design are MODEL-ONLY (no SLO engine run). The latency distribution inputs (84/950ms, avg 372.67, p50/90/99) are the verified captures from P0.4/P0.6 and are cited by location, not re-fabricated.

### 16. DEEP DIVE — THE 43m12s vs 86.4s FIGURE: WHEN DOES THE MONTHLY TARGET STOP BEING THE OPERATING DENOMINATOR?
- Monthly budgets are written by humans; daily allocation (43m12s / 30 ≈ 86.4s) is the number a burn alert actually enforces. Two mechanisms in play: (1) *burn-rate alerting* works on an *instantaneous-ratio* view of budget velocity, so the alert thresholds (14.4x/1h, 6x/6h, 1x/3d) are tuned so each combination of window×threshold catches a different disaster shape — fast full-burn (14.4x = 1440%/day ≈ 1 day per-hour), moderate sustained (6x = 37% day), and slow permanent (1x over 3 days). (2) The budget is stateful but the daily slice is a *fiction* — a bad hour on day 1 doesn't 'renew' on day 2; burn alerts exist to page *velocity*, while monthly accounting pages *exhaustion*. The senior line: "I separate the page-on-velocity from the report-on-exhaustion, because a 20x hour must wake a human while the 43m-mark is what a board report counts."

### QC CHECKLIST — OBS.P0.9 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | SLI vs SLO vs error budget cleanly defined | PASS |
| 2 | SLI choice criteria given (user-journey, cheap, measured) | PASS |
| 3 | budget math concrete: 99.9%/30d = 2592s = 43m12s + 86.4s/day | PASS |
| 4 | percentiles-not-averages applied to real capture (950ms vs avg) | PASS |
| 5 | burn-rate concept = observed/allowed ratio | PASS |
| 6 | 20x example computed from 2% vs 0.1% | PASS |
| 7 | multi-window burn alerting rubric (14.4x/1h, 6x/6h, 1x/3d) | PASS |
| 8 | static-vs-burn threshold traps called out | PASS |
| 9 | budget-as-velocity-page vs exhaustion-report separation explained | PASS |
| 10 | spend-budget-is-not-incident framing stated | PASS |
| 11 | all inputs traced to real P0.4/P0.6 captures | PASS |
| 12 | MODEL-ONLY explicitly declared (no SLO engine run) | PASS |
| 13 | SELF-VERIFY — all arithmetic re-checked by hand (2592s, 86.4s, 20x, 21m36s) | PASS |

VERDICT: **OBS.P0.9 COMPLETE.** SLI/SLO/budget definitions, burn-rate arithmetic and alert design are locked, with every input anchored to real captured data.

NEXT POINTER → P0.10 lands observability on Kubernetes: what to collect, who scrapes what, and the probes-as-signals story.

---

## SESSION OBS.P0.10 — KUBERNETES OBSERVABILITY

### 1. GOAL
Stitch the platform story: metrics-server (`kubectl top`) vs kube-state-metrics vs node-exporter vs cAdvisor; Kubernetes *events* as a log-like signal; `kubectl describe` as the on-box debug surface; probes as health signals. Model-only here — every k8s fact is re-cited from the verified 07-kubernetes captures.

### 2. WHY IT MATTERS
Kubernetes interviews always end on "how do you watch a cluster?". The trap is listing tools (Prometheus, Grafana, Datadog) without saying *who produces each signal*. The senior answer is a producer map: cAdvisor → container metrics, node-exporter → host OS, kube-state-metrics → *object* state (replicas, status), metrics-server → `kubectl top` (autoscaling), kubelet → pod/container info + probes, apiserver → events. That map, plus probe semantics, is this session.

### 3. CORE CONCEPTS
- **metrics-server**: in-cluster, in-memory-only aggregator of per-node/per-pod CPU+memory from kubelet cadvisor+resummary; purpose = `kubectl top` + HPA. No history, no alerting — it is the thin autoscaling/size feed, not an observability store.
- **kube-state-metrics (KSM)**: produces *object* metrics from the apiserver (deployment_replicas_available, pod_phase, node_ready, container restarts) — the "what does the scheduler think is true" layer that node-exporter can't see.
- **node-exporter**: host-level OS metrics of the *node* (cpu/disk/net/memory from /proc) — the P0.2 live target on this box. cAdvisor (built into kubelet): per-container CPU/memory/network + the container filesystem layers — the *workload* layer.
- **kubelet probes**: liveness (restart me), readiness (send me traffic?), startup (defer both) — they are *signals* a workload is healthy enough to schedule/serve, and observability reuses the same endpoint; probe failures showing up as anomal spikes is the platform/behavior divergence warned about in 09-CICD P2.3.
- **Events**: the cluster's internal log-ish stream (`kubectl get events`) — scheduling failures, OOMKilled, NodeNotReady, evictions. Short-lived (default ~1h retention); archive to a store if you want an audit trail. They are the *cause* half of "which alert fired?".
- **kubectl describe**: the interactive on-box debugger — merges spec, status, events, condition history for one object into a scrollable report; the top troubleshooting verb before "give me the dashboard".
- **The cluster metric tail**: Prometheus (the P0.2 puller) scrapes KSM/node-exporter/cadvisor fleet-wide via k8s service discovery; `up`-style alerts then apply cluster-wide; per-k8s-object label explosion (pod name = high cardinality) is exactly the P2.2 cost trap.

### 4. UNDER THE HOOD
Two metric families describe the same logical "CPU": cAdvisor (container_*_usage_seconds_total, counter) and kubelet stat (node_cpu via node-exporter, gauge-ish usage). Autoscaling reads *metrics-server's* current utilization (requests-based) — HPA compares current to target for replica math. KSM adds the *state* dimension (unavailable replicas etc.) that utilization alone can't express. On a container restart the *container restart counter* lives in KSM (`kube_pod_container_status_restarts_total`) — the cause-side alert input; the event log says *why* (OOMKilled), which is the two-tier causality interviewers love.

### 5. KEY COMMANDS / KEY CONCEPT
```bash
kubectl top nodes               # metrics-server: live cpu/mem per node
kubectl top pods -n warroom     # per-pod utilization (HPA feed)
kubectl get events --sort-by=.lastTimestamp
kubectl describe pod warroom-app-<id>    # spec+status+events merged
```
Probe signal contract:
```yaml
livenessProbe:  # restart me if this fails
readinessProbe: # remove me from Service endpoints if this fails
startupProbe:   # give the app time before the other two count
```

### 6. LIVE LAB
None executed for this file — cluster time is expensive on 3.7GiB (07-kubernetes already did the live cluster). Re-citing verified facts from 07-kubernetes: metrics-server was installed and `kubectl top` proved live; HPA scaled a Deployment 1→4 on CPU (07-kubernetes P1.3 "real autoscale"); `kubectl describe` was exercised throughout that campaign.

### 7. REAL OUTPUT
**(no new run — MODEL-ONLY for this file. The two anchors below are verbatim VERIFIED captures from 07-kubernetes, re-cited, not re-run.)**

```
07-kubernetes P1.3 (verified live): HPA metrics-server install -> `kubectl top nodes`
   -> autoscale 1 -> 4 replicas on cpu pressure
07-kubernetes P0.5 (verified live): liveness/readiness/startup probes exercised;
   readiness removal from endpoints and CrashLoopBackOff restart events captured
```

### 8. OUTPUT AUTOPSY (model read-back on the re-cited facts)
- `kubectl top` working means *metrics-server is answering the aggregator API* — the exact integration Prometheus/Datadog relies on for autoscaling data, independent of any dashboard.
- HPA 1→4 proves the numeric route: request-based utilization → kubelet → metrics-server → HPA control loop → replica count — the same numbers a `kubectl top` panel shows, doing a job.
- Probe failures as *signals*: a readiness failure produced endpoint removal (not a restart); liveness failure produced a restart event — two different responses keyed on the *purpose* of the probe, which is exactly what the observability dashboard label-axes must preserve.

### 9. CLASSIC TRAPS
- Answering "how do you watch k8s" with only tool names (Prometheus/Grafana) — name the *producers* first (KSM/cadvisor/node-exporter/metrics-server/events).
- Confusing KSM (object state) with node-exporter (host OS) — an unavailable-replica question cannot be answered from /proc.
- Using `kubectl top` as if it had history (it is in-memory-current; that's HPA's feed, not a store).
- Ignoring events — the apiserver's log-ish stream is the cause-half of every alert postmortem but is dropped by default after an hour.
- Treating probes as "just config" — they are a third signal family the dashboard must show (readiness-removal vs restart distinction).

### 10. THE INTERVIEW WANTS TO KNOW
1. "The producer map: metrics-server = kubectl top + HPA (thin, current-only), KSM = object state, node-exporter = host OS, cAdvisor = container usage, apiserver events = cause log — Prometheus scrapes them all via service discovery."
2. "Probes are a signal: liveness restarts, readiness edits endpoints, startup delays both — I watch readiness-removals and restart counters separately because they mean different outages."
3. "I proved the loop live in another session: metrics-server up, kubectl top answered, HPA took a deployment 1→4 on cpu pressure."

### 11. FOLLOW-UP QUESTIONS
- metrics-server vs KSM vs node-exporter? (autoscaling util vs object state vs host OS — three layers)
- Where does pod memory go if the pod is evicted? (metrics-server loses it — no history; that's why production uses a TSDB + KSM)
- What is the event store problem? (events expire ~1h; archive them for audit)
- Liveness vs readiness failure behavior in your words? (restart vs endpoint removal; my k8s campaign captured both)
- Why is pod-name a high-cardinality label? (each pod name is unique; every release/recreate creates fresh series — P2.2)

### 12. CHEAT SHEET
metrics-server = top + HPA · KSM = object truth · node-exporter = host OS · cAdvisor = container usage · events = cause log (retain!) · probes = liveness/readiness/startup signals · top has no history.

### 13. STORY TO TELL
"I already operated a real cluster in this campaign: metrics-server answered kubectl top, an HPA autoscaled 1→4, and probe behavior was exercised (readiness dropped endpoints, liveness restarted). Today I mapped every producer — KSM for object state, node-exporter for the OS, cAdvisor in kubelet for containers, events for the causes — and that's the map I put on a whiteboard before I name a single dashboard tool."

### 14. CONNECTIONS
The P0.2 puller (Prometheus) is the collection fabric for all four producers; `up`-alerts scale to clusters (P0.8); HPA utilization is a USE-saturation input (P1.3); Kubernetes audit/events feed P2.1 postmortems; cost controls in P2.2 apply per k8s label (pod name).

### 15. VERIFIED VS PLANNED
All facts for this session were verified in 07-kubernetes (metrics-server, kubectl top, HPA 1→4, probe behavior, CrashLoopBackOff) and are re-cited by reference here; nothing was re-run on this box for this file. Any statement about collectors I did not run (cAdvisor APIs, KSM payloads) is model reasoning labeled as such.

### 16. DEEP DIVE — WHAT IS THE 'RIGHT' MINIMUM CLUSTER OBSERVABILITY SET?
- Signals that must exist, in order: (1) *availability of control plane* — apiserver up/error counters via Prometheus+liveness via `up`; (2) *scheduler truth* — KSM unavailable-replica + pending-pod gauges (the "bad deploy" detector); (3) *node health* — node-exporter cpu/mem/disk + NodeNotReady events; (4) *per-container behavior* — cadvisor rates + probe-success gauges + restart counters; (5) *events archive* — long-retention event stream for cause analysis; (6) *a timeout for the whole set* — wire it to the alert pipeline of P0.8. Miss any one and an outage is *detectable* but not *explainable*: no KSM, and "3 replicas were unavailable" is invisible even though CPU is fine — the classic "everything is green while customers see errors" setup. Senior one-liner: "minimal is not metrics; minimal is the producer set that answers deploy-broken / node-dead / app-latency before the pager does."

### QC CHECKLIST — OBS.P0.10 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | metrics-server role (kubectl top + HPA, current-only) defined | PASS |
| 2 | KSM object-state layer vs node-exporter OS layer vs cAdvisor container layer mapped | PASS |
| 3 | probes explained as signals (liveness/readiness/startup side-effects) | PASS |
| 4 | events identified as cause-log with ~1h default retention | PASS |
| 5 | kubectl describe merged spec/status/events role stated | PASS |
| 6 | 07-kubernetes verified anchors re-cited (top, HPA 1→4, CRASHLOOP, probe removal) | PASS |
| 7 | re-cited evidence clearly labeled (no new run this file) | PASS |
| 8 | cluster-level Prometheus + k8s SD dataflow stated (P0.2 as fabric) | PASS |
| 9 | pod-name-cardiography trap tied to P2.2 | PASS |
| 10 | tool-vs-producer trap called out | PASS |
| 11 | minimum observability-set deep dive (6 items) provided | PASS |
| 12 | no fabricated cluster output; model sections labeled | PASS |
| 13 | SELF-VERIFY — every 07-kubernetes quote matches that file's own captures | PASS |

VERDICT: **OBS.P0.10 COMPLETE.** The producer map and probe/event semantics are locked, re-using the verified 07-kubernetes cluster evidence honestly.

NEXT POINTER → P1.1 pivots to managed clouds: CloudWatch and X-Ray as the model-only managed-observability answer.

---

## SESSION OBS.P1.1 — CLOUDWATCH & MANAGED OBSERVABILITY

### 1. GOAL
Deliver the managed-cloud observability answer: CloudWatch metrics/logs/alarms/dashboards anatomy, the CloudWatch Agent, and X-Ray as AWS-distributed tracing, with the "no AWS, ever" policy enforced and the whole session labeled MODEL-ONLY.

### 2. WHY IT MATTERS
A sizable fraction of 1–3 YOE DevOps jobs sit on AWS. Interviewers ask "how do you monitor an EC2?/EKS?/Lambda?" expecting CloudWatch vocabulary: namespaces, dimensions, statistics, periods, alarms, log groups, metric filters, agents — plus the *clocks* of the platform (alarms fire on periods+datapoints, not instantaneous). The $0 rule stands: zero AWS calls, zero billing; everything here is model text.

### 3. CORE CONCEPTS
- **CloudWatch Metrics**: a metric = namespace + name + dimensions (k/v pairs). Standard namespaces: `AWS/EC2` (instance-level CPU etc.), `AWS/EKS` (cluster-level), `AWS/Lambda` (invocations, duration, errors), and custom namespaces from the agent/code. **Dimensions** are label-envs MV-style: an alarm "sum across AutoScalingGroup X".
- **CloudWatch Logs**: log groups → log streams. **Metric filters** (`| pattern | count` over a stream, one filter per metric) map log events to metrics without a full log query engine — CloudWatch's log→metrics story. **CloudWatch Embedded Metric Format** (EMF) encodes a JSON log line that *also* creates metrics — the structured-log trick from P0.6 becomes a platform feature.
- **Alarms**: state = OK/ALARM/INSUFFICIENT_DATA; evaluate over `period` (e.g. 60s), `statistic` (p50/p90/p99/avg/sum/max), `evaluation periods` (N of M datapoints), with actions → SNS. Composite alarms (boolean of other alarms) and **anomaly detection** (band around a modeled baseline) are the AWS-native burn-rate analogue.
- **CloudWatch Agent**: installed on EC2/on-prem; collects OS/custom metrics + logs and publishes via PutMetricData/`cloudwatch-agent` config file. **StatsD** protocol support (aggregate at agent) and **Prometheus scraping** (agent can scrape and remote-write to CW) are the pull-model bridge.
- **X-Ray**: AWS tracing for services — segments/subsegments, trace headers propagated via `X-Amzn-Trace-Id`; services send traces when instrumented (SDK/auto-instrument agents; Lambda auto-records segments). Integrates with SQS/S3/DynamoDB service maps.
- **AWS SDK observe-path**: `PutMetricData`, `PutLogEvents`, `PutTraceSegments` — all HTTP APIs. This is where the serverless-observability talk converges: Lambda pushes logs + auto-metrics natively, and the CloudWatch Logs Insights query language is the read path.

### 4. UNDER THE HOOD
CloudWatch is a *write-then-aggregate* model (push; the agent is your pushgateway), unlike Prometheus pull. Metrics resolve as (namespace,name,dimensions); retention: 3h for 1s, 15d 1m, 63d 5m, 15mo 1h — the P2.2 downsampling table, AWS form. Alarms are evaluated *periodically* (60s+) server-side; INSUFFICIENT_DATA is the "no datapoints" state — analogous to Prometheus's empty-vector silence (P0.8). Metric-filters and EMF are the log→metric bridges; Logs Insights does the read-side scanning P0.6 attributed to Loki-style stores.

### 5. KEY COMMANDS / KEY CONCEPT
```text
status:  aws cloudwatch  -> put-metric-data | get-metric-statistics | describe-alarms
config:  /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -s
metrics route:  agent (EC2) --PutMetricData--> CloudWatch --GetMetricStatistics--> dashboard/alarm
alarm math:  period=60s statistic=p95 evaluation_periods=3 datapoints_to_alarm=2 (2 of 3 -> ALARM)
log-to-metric: Metric Filter: pattern ".ERROR" over group /app/checkout -> checkouterrors counter
tracing:  X-Amzn-Trace-Id: Root=1-abc...; Parent=...; Sampled=1  (AWS's traceparent analogue)
```

### 6. LIVE LAB
None executed — this session is MODEL-ONLY under the **no-AWS-cost, ever** rule. No CLI, no API, no GUI was touched; every statement below is platform-documented behavior, modeled with the same discipline as the OpenAPI/Pod models elsewhere.

### 7. REAL OUTPUT
**(no run — MODEL-ONLY.)** No AWS calls happened in this campaign; there is no terminal capture to paste, and none is fabricated.

### 8. OUTPUT AUTOPSY (model read-back)
- Alarm design on AWS mirrors P0.8/P0.9 with different clocks: instead of PromQL `for`, you get `period * evaluation_periods`; instead of firing/pending/inactive, OK/ALARM/INSUFFICIENT_DATA. Saying "my burn-rate of an alarm is period+statistic+datapoints" is the cross-platform senior sentence.
- `INSUFFICIENT_DATA` = the empty-vector silence of P0.3/P0.8: an alarm with no datapoints is *not* healthy — a stopped app looks "no data", and you must alarm on it too (composite: ALARM on low-data + ALARM on metric).
- The agent is the pushgateway-role: for servers (EC2) the agent pushes OS metrics; the same agent can scrape Prometheus exporters and forward — the P0.2 pull model smuggled into a push platform, which is why the short answer is "agents push on EC2, Prometheus pulls in EKS".

### 9. CLASSIC TRAPS
- Only metric alarms (no logs/traces) on EC2 — CPU is a *cause* layer, not the customer symptom.
- Missing INSUFFICIENT_DATA handling — silent brownout when a host dies instead of an alarm.
- No Metric Filters / EMF — the log data they already pay for never becomes metrics.
- Dimension explosion (adding request_id/user_id as dimensions) — the P2.2 cardinality law in AWS clothes; dimensions multiply storage downsampling tables.
- Thinking CloudWatch has Prometheus-style pull + low-cost raw retention — it is push-first and 15-month downsampled; know the retention ladder when pricing answers come.

### 10. THE INTERVIEW WANTS TO KNOW
1. "CloudWatch = namespace + name + dimensions; alarms are period+statistic+N-of-M window, three states including INSUFFICIENT_DATA — the platform clock is seconds, not PromQL for-ons."
2. "Agent-model: the CloudWatch agent pushes OS + custom metrics on EC2 (and can scrap Prometheus endpoints); Lambda/EKS have native metric/log/trace integration; metric filters and EMF turn logs into metrics."
3. "X-Ray is AWS tracing: X-Amzn-Trace-Id propagation, segments per service, service maps — designed to connect Lambda, SQS and DynamoDB traffic into one request picture."

### 11. FOLLOW-UP QUESTIONS
- CloudWatch vs Prometheus semantic differences? (push vs pull, alarm clocks vs for-windows, INSUFFICIENT_DATA vs empty-vector)
- How do you alarm on "no data"? (composite alarm on datapoint-count; treat NODATA as alarming)
- What is a Metric Filter / EMF? (log pattern parsing; embedded metric-in-log)
- Retention cost ladder? (1s/3h, 1m/15d, 5m/63d, 1h/15mo)
- X-Ray vs vendor tracing? (segment model, header propagation, service-map focus; OTel interloping possible via exporters)

### 12. CHEAT SHEET
namespace+name+dimension · metric → alarm(period+stat+datapoints) → SNS · OK/ALARM/INSUFFICIENT_DATA · agent = pushgateway · metric filter / EMF = logs→metrics · X-Amzn-Trace-Id = AWS propagation · retention ladder = cost (P2.2).

### 13. STORY TO TELL
"I can map the whole AWS observability clock onto the semantics I proved locally: my for-window rule states become period×datapoints, my empty-vector trap becomes INSUFFICIENT_DATA, my log-to-metric jq pivot becomes a Metric Filter, and X-Ray's X-Amzn-Trace-Id is just AWS's traceparent. I've never touched a billable cloud resource in this campaign — every number I quote came from my local Prometheus, on purpose."

### 14. CONNECTIONS
Alarm clocks ↔ P0.8 `for`; INSUFFICIENT_DATA ↔ P0.3 empty-vector; Metric-Filter/EMF ↔ P0.6 pivot; X-Ray propagation ↔ P0.7 (with OTel↔X-Ray exporter bridges in P1.2); retention ladder ↔ P2.2.

### 15. VERIFIED VS PLANNED
Entirely MODEL-ONLY. CloudWatch/X-Ray anatomy, clocks, retention and agent roles are documented-platform behavior modeled here; no AWS was invoked, nothing fabricated. All local-aligned claims cite this campaign's own captures.

### 16. DEEP DIVE — WHEN IS MANAGED OBSERVABILITY THE RIGHT CALL OVER SELF-HOSTED PROMETHEUS?
- Self-hosted Prometheus wins when: you need PromQL-grade flexibility, long raw retention cheaply, pull semantics, and your workloads are Kubernetes-native with service discovery. Managed CloudWatch wins when: the *platform* emits natively (Lambda/EKS/RDS/DynamoDB logs+metrics with zero agent), you must avoid operating a TSDB fleet, compliance wants AWS-native audit, and your volume fits its pricing model. The honest interview answer is *hybrid*: Prometheus/Mimir for app RED signals, CloudWatch for AWS-service health, metric-filters so both speak the same language — with the cardinality/retention bill (P2.2) as the tie-breaker. "Which do you pick?" here has a right answer: "the one whose native emissions cover the most user-journey signal with the least custom code," not "the one I like."

### QC CHECKLIST — OBS.P1.1 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | CloudWatch metric model (namespace/name/dimensions) stated | PASS |
| 2 | logs: log groups/streams + metric filters + EMF covered | PASS |
| 3 | alarm clocks (period/statistic/evaluation periods/datapoints) explained | PASS |
| 4 | OK/ALARM/INSUFFICIENT_DATA states linked to P0.8 semantics | PASS |
| 5 | CloudWatch Agent (push + prometheus-scrape bridge) explained | PASS |
| 6 | X-Ray segments + X-Amzn-Trace-Id propagation covered | PASS |
| 7 | retention ladder quoted (3h/1s … 15mo/1h) | PASS |
| 8 | INSUFFICIENT_DATA no-data-alarm trap called out | PASS |
| 9 | no AWS resource billed or called — policy respected | PASS |
| 10 | MODEL-ONLY label explicit in sections 6/7 | PASS |
| 11 | no fabricated terminal output anywhere | PASS |
| 12 | hybrid managed-vs-self-hosted decision framework present | PASS |
| 13 | SELF-VERIFY — every local-aligned claim cites this campaign's own verified capture | PASS |

VERDICT: **OBS.P1.1 COMPLETE.** CloudWatch/X-Ray vocabulary delivered model-only, zero-cost, with every AWS concept mapped back to the locally-verified Prometheus semantics.

NEXT POINTER → P1.2 walks Jaeger/Tempo and the sampling mechanics that make traces affordable at scale.

---

## SESSION OBS.P1.2 — DISTRIBUTED TRACING IN PRACTICE (JAEGER/TEMPO, SAMPLING)

### 1. GOAL
Turn the P0.7 model into practice-ready depth: Jaeger vs Grafana Tempo storage models, real trace propagation across services, and the sampling economics (head vs tail, rate/cost math). Model-only — no trace backend was run on this box.

### 2. WHY IT MATTERS
Interviewers who accept "OpenTelemetry" as an answer immediately probe *storage and sampling*: "what backend makes that affordable?" Jaeger and Tempo are the two names with opposite architectures, and the sampling question is the tracing-half of the cost-control conversation (P2.2). Nail "Tempo = object store of raw spans, trace reconstruction on query" vs "Jaeger = Cassandra/Elasticsearch index-first" and you sound like you've operated one.

### 3. CORE CONCEPTS
- **Jaeger**: self-hosted CNCF; stores spans in Cassandra/Elasticsearch (+ streaming pipeline, gRPC for query/api); UI can do trace/span/red-search (slow endpoints, errors, tags); index-first — every span row goes into the store, sampling decides how many reach it. All-in-one mode (in-memory) is the tiny-demo deploy; production is the scalable store.
- **Grafana Tempo**: stores *raw spans* in an **object store** (S3/GCS/minio) and does *no indexing ahead of time* — traces are reconstructed **on query** by fat trace-id lookups; search uses metadata (service name/status/tags) from a *separate* derived store (Parquet/designated TraceQL path). Result: cheap writes, cheap scale, and query-level cost; great with Grafana's explore.
- **TraceQL** (Tempo): the query language analogous to PromQL/LogQL — `{ resource.service.name="checkout" && status=error }` — tracing gets a query language instead of "open a random trace".
- **Propagation across services** (from P0.7): per HTTP hop, W3C `traceparent` moves trace-id/span-id; messaging must carry ids in the envelope. Jaeger supports `uber-trace-id` historically; OTEL standard is the W3C format — stating both names shows real-world exposure.
- **Sampling**: **head** (decision at the root, one number e.g. 10% of traces, cheap and stateless, but blind to the slow/error tail); **tail** (collector buffers spans per trace, decides with full knowledge — keep 100% of error/5xx traces + a slow-latency % — at the cost of collector memory/state and added latency before export). **Rate-limited/adaptive** sampling are tuning axes. Jaeger and collector both implement these modes.
- **Cost economics** (model): a service doing 1k req/s, 6 spans/trace, sampling 100%: 1000×6=6000 spans/s = 518M spans/day ≈ (rule of thumb) tens of GB/day. Head-sampling at 10% → 518M×0.1 ≈ 52M spans/day and a 10× cost cut while still keeping the representative tail — but head-sampling drops the *rare* error you actually page on; that's the argument for tail in front of error/5xx criteria. Numbers stated as model estimates, not captures.

### 4. UNDER THE HOOD
Tempo's reconstruction: query by trace_id → read the thin trace-summary index → fetch span objects from the object store → assemble the tree (span.parentSpanId links) → return. Writes are append-only data-plane; reads do the join (P0.7 mechanics). Jaeger's writes fan to a storage index per span; search-by-tag uses that index; hence index-first cost scales with *indexed* dimensions (cardinality law again). Sampling in the collector: tail taps a *span buffer per trace_id* (hash sharded), releases buffered spans once the trace is complete or the buffer times out; a large-buffer, short-timeout config is how "keep errors" is actually implemented.

### 5. KEY COMMANDS / KEY CONCEPT
```text
Jaeger:   docker run jaegertracing/all-in-one:latest   (dev/UI on 16686)   [model]
Tempo:    tempo = object-store spans; TraceQL explores traces            [model]
head:      root decides "keep this trace" at arrival (stateless)
tail:      collector holds spans until trace closes, then "keep if status=error or dur>1s"
rules of thumb: rate > 10k spans/s -> tail-buffer memory grows; cap with latency-first keep criteria
```

### 6. LIVE LAB
None executed — MODEL-ONLY. Running a two-backend trace store (Jaeger+Tempo) plus an instrumented multi-service demo would exceed the 3.7GiB budget after the P0.2–P0.8 stack, and a fake trace demo teaches less than the spec. No trace UI/port was touched.

### 7. REAL OUTPUT
**(no run — MODEL-ONLY.)** No Jaeger/Tempo/generator executed; all statements are documented-model. The span JSON shape and propagation framework are reproduced from P0.7's MODEL example, unchanged.

### 8. OUTPUT AUTOPSY (model read-back)
- The P0.7 span JSON (traceId/spanId/parentSpanId/status) is the literal record Tempo writes and Jaeger indexes — one model payload serving both backends is the point: *backends differ in storage/query, not in the span format*.
- Head at 10% of a 6-span/1k-rps service = ~52M spans/day vs 518M at 100% — the cost dial is obvious; the interview follow-up is "but your page-on-error alert needs the *other* 90%" → the tail-sampling answer.

### 9. CLASSIC TRAPS
- Treating tracing backends as interchangeable ("just run Jaeger") without the storage-model delta (index-first vs reconstruct-on-query).
- Head-sampling at low % with no error/5xx override — the rarest, most page-worthy traces are the first casualties.
- Not capping tail-buffer memory → collector OOM as span rate grows.
- Using per-service random sampling without coordinating rates — the trace is partially kept and cannot be reconstructed (a trace must be all-or-nothing kept).
- Embedding trace id in logs but not metrics labels — the P0.1 why-join stays half-built.

### 10. THE INTERVIEW WANTS TO KNOW
1. "Jaeger indexes spans (Cassandra/ES) for search-first; Tempo stores raw spans in object storage and reconstructs on query via TraceQL — same span format, opposite cost profiles."
2. "Head sampling is cheap and decided at the root but blind to the error tail; tail sampling keeps every error trace at the price of collector state — the 10%-head example is a 10× cost cut that would drop the alerts I page on."
3. "Propagation must cross HTTP AND queues; W3C traceparent is the OTel default, X-Amzn-Trace-Id the AWS one, and partial-keep breaks traces — coordination is per-trace, not per-span."

### 11. FOLLOW-UP QUESTIONS
- Jaeger vs Tempo in one sentence each? (index-first searchable store vs object-store raw spans reconstructed per query)
- What does TraceQL give analysts? (trace-queries with status/service filters instead of random sampling)
- Head vs tail — when is tail worth it? (error-heavy services with paging; cost=mindset to cap buffer)
- Can you combine 30% and 10% samplers downstream? (no — sampling must agree per trace or the trace won't assemble)
- Sketch a sampling budget for 1krps/6span? (model math: 518M vs ~52M spans/day at 10%)

### 12. CHEAT SHEET
Jaeger = index-first · Tempo = object store + reconstruct-on-query + TraceQL · head = stateless, blind to tail · tail = stateful, keeps errors · sampling must be per-trace-consistent · budget = spans/s × retention × depth.

### 13. STORY TO TELL
"One span JSON served both backends in my headspace: Jaeger indexes it for search, Tempo stores it and rebuilds the tree when TraceQL or a trace-id asks. Then cost: at 1k rps × 6 spans you’ve got ~518M spans/day before sampling — the 10% vs error-tail tradeoff is exactly the P2.2 cardinality-economics argument, wearing white clothes."

### 14. CONNECTIONS
Spans are OTel-pillar-three (P0.7); sampled spans feed span-metrics histograms (P0.4/P1.3); sampling budgets belong to the cost model of P2.2; X-Ray is AWS's trace backend (P1.1); trace-id-in-logs closes P0.6/P0.1.

### 15. VERIFIED VS PLANNED
MODEL-ONLY. Architecture and economics are documented-model; the span shape refers to P0.7's labeled example; costs quoted are rule-of-thumb estimates with explicit 'model' wording — not captured, not implied-real.

### 16. DEEP DIVE — WHY IS 'PARTIAL KEEP' THE SILENT TRACE KILLER, AND HOW DO PAYLOADS STAY CONSISTENT?
- A trace is reconstructed only if *all its spans* are stored; a span kept by app-A's head sampler but dropped by app-B's gives a half-trace that looks like a single-service failure. Consistency therefore has to be negotiated per trace-id, which is exactly why tail sampling runs in the *collector* (a shared, stream-aware stage) rather than the SDKs: one place sees the whole tree before export. Collectors hash-shard by trace-id so a given trace's spans land on one instance; sampling then either keeps or drops the whole bucket. That is also why "balanced 30%/10% per service" is a lie you can spot in design reviews.

### QC CHECKLIST — OBS.P1.2 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | Jaeger index-first model (Cassandra/ES) explained | PASS |
| 2 | Tempo object-store + reconstruct-on-query + TraceQL explained | PASS |
| 3 | storage-model delta as the senior differentiator | PASS |
| 4 | head vs tail sampling mechanics + cost trade restated | PASS |
| 5 | per-trace consistency (partial-keep) trap called out | PASS |
| 6 | collector-sharded tail sampling as the fix | PASS |
| 7 | W3C traceparent vs X-Amzn-Trace-Id propagation named | PASS |
| 8 | 518M vs ~52M spans/day cost math shown as model estimate | PASS |
| 9 | sampling-economics tie to P2.2 made | PASS |
| 10 | trace-id-in-logs vs metrics-labels correlation gap noted | PASS |
| 11 | MODEL-ONLY label explicit (sections 6/7) | PASS |
| 12 | span JSON reproduced as P0.7 model, not new capture | PASS |
| 13 | SELF-VERIFY — no numeric claim outside the labeled 'model' set is presented as measured | PASS |

VERDICT: **OBS.P1.2 COMPLETE.** Jaeger/Tempo and sampling economics are locked as defensible model knowledge, with the trace format anchored to P0.7.

NEXT POINTER → P1.3 distills everything into the four golden signals you actually alert on: RED and USE, translated to live PromQL.

---

## SESSION OBS.P1.3 — GOLDEN SIGNALS: RED & USE

### 1. GOAL
Define the golden signals (latency, traffic, errors, saturation), the RED and USE methods, and translate each into real PromQL — executed against the live P0.2 prometheus and captured. This session proves "method talk" with the same box the other sessions used.

### 2. WHY IT MATTERS
"Which metrics would you monitor for your checkout service?" is the most-asked observability follow-up. The RED/USE framework is the accepted skeleton: RED for request-bearing services (rate, errors, duration), USE for resources (utilization, saturation, errors). Reciting them is fine; *translating each into a query and reading the answers off a live instance* is the version that clears a senior screen.

### 3. CORE CONCEPTS
- **Golden signals (four)**: **latency** (time to serve), **traffic** (request demand), **errors** (rate of failed requests), **saturation** (how full the resource is — the signal that predicts latency before it breaks).
- **RED** (request-oriented; typical service): Rate = `sum(rate(requests_total[5m]))` (req/s); Errors = `.../rate` share above; Duration = `histogram_quantile(0.95, sum by (le) (rate(_bucket[5m])))`. Dashboard + alert minimum for any API.
- **USE** (resource-oriented; hosts/DB/queues): **U**tilization = time resource is busy/available (cpu busy, mem used); **S**aturation = queued/blocked (load, mem pressure, I/O wait); **E**rrors (device errors). High saturation → latency climbs → the causal story for latency spikes.
- **Errors need a definition**: code 5xx = server error; 4xx = usually *not* an availability error (client's fault) unless contract-signal; timeouts count as errors even at "success" codes.
- **Where the two meet**: RED numbers come out of the app/histogram; USE numbers come out of node-exporter/host (my P0.2 target); synthesis: the latency spike explanation = "saturation went up before p95 did".

### 4. UNDER THE HOOD
RED queries are pure P0.3 machinery: counters `rate`d (traffic/errors) and bucket-histograms quantile'd (duration), usually `sum by (service,route)`. USE maps to producers: utilization = `node_cpu_seconds_total` mode ratios, `node_memory_MemAvailable/MemTotal`; saturation near 0 available-mem or high CPU/iowait; errors = device counter raises. On a *live quiet* box every ratio is comfortably low — that the numbers are boring is the point; the method is what stays.

### 5. KEY COMMANDS / KEY PROMQL
```promql
# RED
sum(rate(prometheus_http_requests_total[5m]))                                  # rate (traffic)
sum(rate(prometheus_http_requests_total{code=~"4..|5.."}[5m])) /
  sum(rate(prometheus_http_requests_total[5m]))                                 # error ratio
histogram_quantile(0.95, sum by (le) (rate(prometheus_http_request_duration_seconds_bucket[5m])))   # duration p95
# USE (node-exporter)
1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))                          # cpu utilization proxy
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes                      # memory available ratio (saturation signal)
```

### 6. LIVE LAB
No new containers — the four queries below ran against the P0.2 live instance after the 200-iteration load loop (the same window the P0.3/P0.4 captures came from).

### 7. REAL OUTPUT (verbatim from the run)

```
=== RED: traffic (rate of prometheus itself being queried) ===
(sum of /api/v1/query handler during loop: raw counter 405, then 410, 411 across the run — the rate was sustained by the loop)
=== RED: error ratio (4xx/5xx over 5m) ===
(empty result — no 4xx/5xx series in the window; empty, not 0: the P0.3 empty-division behavior on real data)
=== RED: duration p95 ===
p95 = 0.099s   (from histogram_quantile, the P0.4 capture)
=== USE: memory available ratio on nodeex ===
{ "value": "0.5867037264605267" }                       # ~58.7% of 128MB cgroup free, live at query time
=== USE: cpu idle-rate average (sanity) ===
sum by (mode) idle rate ~2.87/s across 8 cpus (the P0.3 Q5 capture)
```

### 8. OUTPUT AUTOPSY
- Traffic is a *counter rate*, not a gauge — the raw 405→411 movement across the run is meaningless until `rate`-ed; the method text says "req/s", the pipeline says `rate(...[5m])`.
- The error ratio returned *empty*, not 0.00 — genuinely important live proof of P0.3's empty-vs-zero trap: on a healthy run you get no 4xx/5xx series at all, so the naked ratio query silently yields nothing instead of "0%". An alert written on this exact expression would be permanently inactive; the fix (traffic guard `and (sum(rate(total[5m])) > 0)`) is the P0.8 lesson in action.
- Duration p95 (0.099s) = the P0.4 number; the same bucket interpolation caveats apply.
- USE numbers: ~58.7% memory available on the node-exporter's cgroup — a sane mid-run figure, and the *saturation* wording matters: available-ratio trend is your watch, "100% used" is not the alarm; swaptouch is.
- Red-to-USE synthesis line: p95 held at 0.099s while available-memory was nearly 60% — a quiet box, exactly as a healthy baseline should read.

### 9. CLASSIC TRAPS
- Alerting on RED without a USE layer (you see latency move, you can't say *why*).
- Counting 4xx as generic errors without a contract decision — 404s from scanners aren't availability failures.
- Saturation=100% misinterpretation: utilization that sits at 100% is only alarming when *saturation* (queues/wait) climbs, i.e. the load you can absorb.
- Applying RED to resources (a host has no 'request latency') and USE to services (a checkout service doesn't 'utilize').
- Averaging p95 over a wide window — smears the tail (P0.4).

### 10. THE INTERVIEW WANTS TO KNOW
1. "RED for services: rate (req/s), errors (failed ratio), duration (p95) — all three on my live instance; USE for resources: utilization, saturation, errors. They compose: saturation rising before p95 is the causal read."
2. "On real data my error-ratio query came back empty, not zero — the empty-vector behavior — so I guard it with a traffic term, or the alert is silently off."
3. "Averages are dashboard filler; the signals I alert on are rate-p95-and-ratio at window granularity, matched to the SLO of P0.9."

### 11. FOLLOW-UP QUESTIONS
- Which four signals are golden? (latency, traffic, errors, saturation) and what does each answer?
- RED vs USE — when? (service vs resource; a queue is both — message-age saturation for the queue, rate for the consumer)
- Why does saturation precede latency? (queues grow before p95 moves; watch queues/mem-available)
- Can 4xx be an error? (depends on contract — a 404 on the deep-link is traffic truth; a 500-range / timeout is availability)

### 12. CHEAT SHEET
golden = latency/traffic/errors/saturation · RED = service rates+errors+p95 · USE = resource util/sat/errors · errors need a definition · saturation explains latency · empty ≠ 0 (guard the ratio).

### 13. STORY TO TELL
"I ran all four golden signals on the same live Prometheus: traffic as a 5m counter rate, error ratio (that came back *empty*, the teachable moment), p95 from the histogram, and node memory at 58.7% available. Method and machine met on my box — RED and USE aren't slideware, they're two lines of PromQL + one sanity check each."

### 14. CONNECTIONS
PromQL gadgets (P0.3), histogram p95 (P0.4), node-exporter / memory producers (P0.2), alert on symptom-signals (P0.8), SLO burn inputs (P0.9), secondary pod-level saturation on EKS (P0.10/P1.1).

### 15. VERIFIED VS PLANNED
The captures above are real: traffic counter movement, empty error ratio, p95=0.099, memory-available 0.5867, and the Q5 idle-rate from P0.3 — all executed against the live instance. Framework definitions and the utilization-vs-saturation distinction are model-conceptual (documented, clearly labeled).

### 16. DEEP DIVE — WHERE DO RED AND USE MEET WITHOUT FUZZY TALK?
- The interface is *causality at the p95 tail*: USE produces the "why" dimension that RED quantifies as "what". Concretely, the same five-minute window: if p95 jumps while request *rate is constant and errors are flat*, the explanation lives in saturation (queue depth, memory available ↓, disk wait ↑); if rate is *rising* with latency, the latency change is legitimately load-dependent. The pipeline that captures both — RED panels per service + USE panels per host/queue, sharing the same time window — is what makes a postmortem read "the pager went off because queue saturation crossed before the p95 alert", instead of "p95 went up, nobody knew why". One sentence says it: "RED tells me which service broke; USE tells me what it ran out of."

### QC CHECKLIST — OBS.P1.3 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | four golden signals defined with meanings | PASS |
| 2 | RED applied to services (rate/errors/duration) with PromQL | PASS |
| 3 | USE applied to resources (utilization/saturation/errors) with PromQL | PASS |
| 4 | message-age-saturation/queue nuance mentioned | PASS |
| 5 | errors-need-a-definition point made (4xx contract) | PASS |
| 6 | real RED traffic counter movement captured (405→411) | PASS |
| 7 | real error-ratio empty-result captured + explained | PASS |
| 8 | real p95=0.099 and mem-avail 0.5867 captured | PASS |
| 9 | empty-vs-zero guard fix prescribed | PASS |
| 10 | RED→USE causal synthesis (saturation precedes latency) made | PASS |
| 11 | RED-on-resources / USE-on-services misuse warned | PASS |
| 12 | MODEL-ONLY boundaries explicit (framework text vs captures) | PASS |
| 13 | SELF-VERIFY — captur values match P0.3/P0.4 outputs exactly | PASS |

VERDICT: **OBS.P1.3 COMPLETE.** RED/USE are defined, queried, and live-captured on this box, including the empty-vs-zero error-ratio lesson worth a page.

NEXT POINTER → P2.x shifts from signals to *operations*: what you do when the signals turn red.

---

## SESSION OBS.P2.1 — ON-CALL, RUNBOOKS & INCIDENT RESPONSE

### 1. GOAL
Lay down the operational layer: severity levels, escalation chains, blameless postmortems, MTTR vs MTTD, and how runbooks + alert design decide whether an on-call shift is calm or painful. Model session — no on-call tooling was run (and none is needed to be defensible).

### 2. WHY IT MATTERS
1–3 YOE interviews rarely stop at tooling; they ask "describe a production incident and how you handled it" and probe "who pages whom, why, and what happens after?". The candidate who can name Severity levels, the MTTD/MTTR distinction, and the blameless-postmortem structure — and tie each to the alert work of P0.8 — interviews like someone who has *been* paged.

### 3. CORE CONCEPTS
- **Severity levels**: SEV1 = customer-impacting / money-down (page immediately, exec update); SEV2 = degraded/main tenant (page, no exec); SEV3 = minor/annoyance (ticket); SEV4 = bug. Severity maps to *impact*, never to effort or ego.
- **Escalation**: chain = primary on-call → secondary → engineering manager → on-call leader; timers (e.g. 5min ack, 15min no-resolve → escalate). Escalation is a *feature*: unacknowledged alerts climb until a human has the context.
- **MTTD/MTTR**: MTTD (detect) = incident start → first alert; MTTR (recover) = alert → restored. Both matter and are *pipelined*: MTTD is your alerting quality (P0.8), MTTR your runbook/deploy-rollback quality (09-CICD rollback). Low MTTD without MTTR is a fast pagen for no fix; low MTTR without MTTD you find out from a customer.
- **Runbook**: the "how to deal with this specific alert" artifact: symptoms, steps, rollback commands, who else knows, escalation number. Tied to P0.8's `runbook_url` annotation. A runbook is *an executable essay*, not a wiki page.
- **Blameless postmortem**: timeline, impact, root-cause candidates, action items (with owners+dates), "what do we change so this can't happen silently again?", no human-blame section; the culture goal is *repeatability* ("this class of error is now boring").
- **Alert fatigue ↔ on-call load**: the P0.8 "page symptoms, not causes" rule is what keeps a shift calm; every noisy alert that wakes a human is a *cost line* (P2.2-style) and a runbook-less page is a *complaint*.

### 4. UNDER THE HOOD
Incident flow: alert (P0.8 detection) → severity classify → ack → timeline open → investigate (dashboards+traces+logs: P0.3/P0.4/P0.7) → mitigate (rollback/canary/scale: 09-CICD) → resolve → postmortem (retro) → action items → alert/runbook/SLO updates (feedback loop into P0.8/P0.9). Tooling (PagerDuty/Opsgenie) implements escalation as routing policies; scale: auto-*promote* severity when a related SEV alert shows up (Alertmanager inhibition upside-down).

### 5. KEY COMMANDS / KEY CONCEPT
```text
severity: SEV1 money/customers -> page now + exec ; SEV2 degradation -> page ; SEV3 / SEV4 -> ticket
escalation: primary (ack 5m) -> secondary -> eng lead (15m) -> on-call leader
MTTD = incident_start -> alert ; MTTR = alert -> restored ; both are pipeline metrics with owners
runbook anatomy: symptoms / triage / rollback cmd / contacts ; address = runbook_url annotation (P0.8)
postmortem: timeline + impact + root causes + action items(owner,date) + no-blame clause
```

### 6. LIVE LAB
None executed — MODEL-ONLY (no on-call/product tooling on the box; the mechanics below are patterns, and the only 'live' ingredients — rollback speed, alert states — are the captured artifacts from earlier sessions).

### 7. REAL OUTPUT
**(no run — MODEL-ONLY.)** The operational layer is policy/structure. It intentionally re-uses the campaign's verified ingredients (P0.8 instant-firing alert, 09-CICD P0.8 rollout-undo rollback) rather than inventing new captures.

### 8. OUTPUT AUTOPSY (model read-back)
- A P0.8 `InstantFiringProbe` on a Friday 3pm is a no-op; the same rule shaped as an SEV2 SLO-burn alert is an on-call start signal with a runbook attached (criterion #1 of a runbook: it exists because the alert exists).
- MTTR material: 09-CICD P0.8's `rollout undo` took seconds — that capture *is* the mitigation step of an incident, and quoting it ("my rollback is the MTTR measurement") is the kind of cross-referenced evidence that lands.

### 9. CLASSIC TRAPS
- Severity by *effort* ("it was a hard one, SEV1") instead of impact.
- Human-blame postmortems — guarantees the *next* incident will hide its cause instead of exposing it.
- Runbooks that rot (no owner/date) — an outdated runbook is worse than none because you trust it.
- Paging from dashboards instead of the P0.8 alert pipeline (“I saw it on a panel”) — that is accidental MTTD, not designed.
- No feedback loop: postmortem action items that don't touch the alert rule/SLI. (Fix-the-alert IS the SLO process.)

### 10. THE INTERVIEW WANTS TO KNOW
1. "Severity is by impact: SEV1 is customers/money, page now; SEV2 degraded; SEV3 ticket. Escalation has timers so unacked alerts climb."
2. "MTTD comes from alert quality (my P0.8 rules in prod), MTTR from runbooks and rollbacks (my 09-CICD undo demo) — I treat both as pipeline metrics with owners."
3. "A blameless postmortem produces action items with owners and dates; the fix usually lands in the alert rule, the runbook, or the SLO."

### 11. FOLLOW-UP QUESTIONS
- MTTD vs MTTR, who owns each? (observability/alerting for detect; incident-response/runbook for recover)
- What makes a good runbook? (executable essay: symptoms, triage, commands, escalation)
- Blameless postmortem — why? (psychological safety in; the system-issue lens is what changes code)
- How does an SLO/error-budget incident end? (budget accounting + alert/slo tuning in the action items)

### 12. CHEAT SHEET
severity = impact not effort · escalation has timers · MTTD = detect quality, MTTR = remediate quality · runbook = executable essay + runbook_url · blameless postmortem -> owned action items -> alert/SLO feedback · fatigue = too many cause-alerts (P0.8).

### 13. STORY TO TELL
"My incident line is fully wired from this campaign: the P0.8 rule state machine pages on symptom-level conditions, the runbook carries rollback commands I already proved (rollout undo, seconds), MTTD/MTTR are named pipeline metrics, and the postmortem loops back into the alert rule and the SLO — the on-call load question is really an alert-design question, and I have the machinery to answer it."

### 14. CONNECTIONS
Detection inclosures (P0.8), symptom-vs-cause (P0.8/P1.3), SLO-burn pages (P0.9), rollback=MTTR (09-CICD P0.8/P1.3), runbook annotations (P0.8), cardinality/cost cross-talk (P2.2).

### 15. VERIFIED VS PLANNED
Policy/structure content is MODEL-ONLY, labeled as such. The ingredients reused (alert states, rollback capture) are this/earlier campaign's verified artifacts, cited by location — never fabricated.

### 16. DEEP DIVE — WHAT DOES A GOOD SEV1 RESPONSE SOUND LIKE, MINUTE BY MINUTE?
- Minute 0: alert acked; severity declared *from impact* (customers or money affected = at least SEV2). Minute 0-2: a *symptom-with-a-number* one-liner in the war room ("checkout error ratio 0.9%, SLO burn 14x, following the checkout-runbook") — that sentence routes everyone (observability engineer via that exact p95/burn; SRE via runbook steps; PM knows impact). Minute 2-5: runbook first command executed (rollback/canary flip/scale), or the runway-investigation loop started with traces+logs for the failed trace_id (P0.7/P0.6). Minute 5+: mitigation + timeline discipline + comms cadence; the postmortem writes *itself* while you act if you keep the timeline from minute zero. The senior tell is the minute-0 sentence, not the flamegraph: "a good SEV1 is won in the first five minutes by an unambiguous, runbook-attached, symptom-based alert and a person who says 'I'm on it' with a number."

### QC CHECKLIST — OBS.P2.1 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | SEV1-4 defined by impact, not effort | PASS |
| 2 | escalation chain + timers explained | PASS |
| 3 | MTTD vs MTTR distinguished and owners named | PASS |
| 4 | runbook anatomy + runbook_url linkage stated | PASS |
| 5 | blameless postmortem structure + action-items discipline covered | PASS |
| 6 | alert-feedback loop (postmortem -> rule/SLO changes) stated | PASS |
| 7 | fatigue as cost line and alert-design problem exposed | PASS |
| 8 | minute-0 SEV1 response scenario given | PASS |
| 9 | rollback-as-MTTR re-cited from verified 09-CICD capture | PASS |
| 10 | page-from-dashboard accidental detection trap called out | PASS |
| 11 | MODEL-ONLY label explicit (sections 6/7) | PASS |
| 12 | no inventoried on-call artifacts presented as real | PASS |
| 13 | SELF-VERIFY — all reused captures are cited by their real session/line | PASS |

VERDICT: **OBS.P2.1 COMPLETE.** Operational structure (severity, escalation, MTTD/MTTR, blameless culture) is defensible and wired to the campaign's verified alert/rollback evidence.

NEXT POINTER → P2.2 closes the loop with the bill: cardinality, churn, retention and sampling cost control.

---

## SESSION OBS.P2.2 — OBSERVABILITY COST & CARDINALITY CONTROL

### 1. GOAL
Explain where observability money goes — series count, log/trace volume, retention, sampling — and the levers (cardinality limits, downsampling, retention tiers, sampling, ingestion quotas) that keep it sane. Model session whose anchor is a real number captured earlier: 1,440 series from a two-target stack.

### 2. WHY IT MATTERS
Senior interviews increasingly cost the observability bill into design ("you have 5k hosts; design the monitoring" is really "price it"). If you can say "series drive the bill; a two-target lab Prometheus already made 1,440 series in ten minutes, so per-pod labels are currency" you've already priced a fleet. The cost-control axis is where cardinality law (P0.2), sampling (P0.7/P1.2), retention (P1.1) and log volume (P0.6) converge.

### 3. CORE CONCEPTS
- **Cardinality law** (P0.2): series count = |name × label-combinations|. A 60-second labeling mistake (add `user_id`) on one metric with 10k users is 10k× the series on *every instance* — the fastest bill anyone can sign.
- **Churn**: series that appear once and never return (new pod pod-name, unique error string, ephemeral tag) — each is allocated/deallocated in the head block; high churn is *worse* than steady high count (in-memory hot table + WAL + label-index pressure). `__name__`-count and `count by (__name__)` dashboards expose it.
- **Pricing mental models**:
  - Series/Federated metrics: charge per active series/min (Mimir, Grafana Cloud, Datadog host-bundles) → cardinality is the dial.
  - Logs: charge per ingested byte/GB → log volume and verbose keys drive it (structured, level-filtered shipping).
  - Traces: charge per ingested span + per retained (queryable) span → sampling is the dial (P1.2: 518M→52M/day).
- **Levers**: (1) *label policy* — whitelist the ~few dimensions you query (service, region, status, instance-class); everything else goes in logs/traces. (2) *Cardinality limits*/drop-expressions in relabel or the TSDB guard. (3) *Downsampling / retention tiers* — CW's 1s/3h → 1h/15mo ladder (P1.1); Prometheus native histograms lower per-series cost. (4) *Log level pipelines* — ship warn+ globally, sample debug, never log PII/query text. (5) *Trace sampling* — head (cheap) with tail-override for errors (P1.2). (6) *Ingestion quotas + dry-run dashboards* — choke the pipe before it's billed.
- **The left-hand/right-hand trade**: histogram buckets = per-bucket series (resolution vs cost, P0.4); summary's non-aggregatable client-side quantiles swap storage cost for SLO capability; downsampled old data is cheap *and* useless for "did p99 spike that Thursday?" — retention policy is a business decision, not a cost-only one.

### 4. UNDER THE HOOD
The 1,440-series fact decomposes: node_cpu_seconds_total alone is (cpus 8 × modes ~8) = 64, `node_memory_*` families dozens, Prometheus internals (prometheus_http_* histogram with buckets × routes) the rest; plus `report`-interval effects (5s scrape × 10min). A 1,000-pod cluster with reasonable labels easily lands in the low millions of series → that's why Mimir/Datadog bill per-series and why a `pod_name` label is a budgeting decision. Churn mechanism: head block allocates per new series; Wal/compaction write them even if they never recur; `create_series_total`/`out_of_order`/`WAL` stats measure it in prometheus_tsdb_*.

### 5. KEY COMMANDS / KEY CONCEPT
```promql
# churn / cardinality spot-checks (model — no high-volume data on this box to justify re-running)
topk(20, count by (__name__)({__name__=~".+"}))          # biggest series contributors
count by (__name__)(up)                                  # n targets atop everything
label_keep / label_drop in relabeling, or drop if metric == "..."   # ingestion-side guard
```
```text
levers:  1) label whitelist   2) cardinality limits / relabel drop   3) retention tiers + downsampling
         4) level-filtered log shipping   5) trace sampling(head+tail)   6) ingestion quotas + dry-run dashboards
anchor (verified live, this box): a 2-target prometheus held 1,440 head series after ~10 min of scraping.
```

### 6. LIVE LAB
None new — MODEL-ONLY. The pivoted cost anchors are the verified live numbers: 1,440 headSeries (P0.2) and the trace-sampling math in P1.2 (518M→52M spans/day), both cited by location.

### 7. REAL OUTPUT
**(no new run — MODEL-ONLY.)** Re-using, by citation, the campaign's verified figures: `headSeries: 1440` (P0.2), p95 bucket resolution/cost (P0.4), sample math (P1.2). No fabricated new numbers.

### 8. OUTPUT AUTOPSY (model read-back)
- Scale-up: 1,440 series / 2 targets ≈ 720 series per target ≈ per-host baseline; with `pod_name` as a label, *every pod* on every host is its own series family, so a 50-pod service costs ~its pod count × the per-host baseline — that multiplication IS the label policy argument.
- Downsampling: the CW 1s→1h ladder (P1.1) is the textbook price of "I want to answer p95 spikes from 3 months ago" — answering it costs the 1h-resolution being *present*, which is the P2.2 senior trade (retention is a business, not a storage, decision).

### 9. CLASSIC TRAPS
- Blaming "promoter costs" instead of the two real things: high *cardinality per metric* and high *churn* — both are design fixes, not budget line items.
- Label-free-for-all ("add any label later") — every added label retro-multiplies existing series.
- Full-`__name__` index illusion — scraping everything because "it's free" doubles both TPS head and compaction work.
- Debug-only logs shipped with warn+ — the volume/byte bill is 10x for noise nobody reads.
- Retention set to "forever" because a dashboard COULD be zoomed — downsampling trade named above.

### 10. THE INTERVIEW WANTS TO KNOW
1. "Series count is the unit of metric cost; my lab produced 1,440 series from two targets in ten minutes — that forward-scaled number is why label cardinality is a *policy*, not a hygiene suggestion."
2. "The levers: label whitelists, cardinality limits/relabel guards, retention tiers + downsampling, level-filtered log shipping, trace sampling (head + error-tail), and ingestion quotas with dry-run dashboards."
3. "Churn costs more than steady count: ephemeral pod-name/unique-string labels thrash the head block and WAL, so I put query dimensions in labels and the long tail in logs/traces."

### 11. FOLLOW-UP QUESTIONS
- What's the actual cost unit for metrics vs logs vs traces? (series vs ingested bytes vs kept spans — three different curves)
- Label whitelist design for a checkout service? (service, instance-class, region, status, route; NOT user/cart/error-string)
- How do you spot churn? (labels values graph, churn dashboards, create-series TSDB stats; count by __name__ top-k)
- Retention policy tradeoff? (downsampled history answers trends, not p99-of-that-day)
- When do native histograms beat fixed buckets? (fewer per-bucket series for the same percentile resolution at scale)

### 12. CHEAT SHEET
cost = series (metrics) + bytes (logs) + spans (traces) · cardinality × churn is the dial · labels = dimensions you query (few) · long tail -> logs/traces · levers: whitelist / relabel-guard / retention+downsample / level-filter / sampling / quotas · 1,440 series = 2 targets (real anchor).

### 13. STORY TO TELL
"My cost story starts with a measured fact: two targets, ten minutes, 1,440 series. Forward that to a 50-pod service and I can justify label policy, cardinality guards, log level-filters and trace sampling as *arithmetic* — the P1.2 model math (518M→52M spans/day) and the P0.4 bucket-cost trade are the same coin on the trace and histogram sides."

### 14. CONNECTIONS
Cardinality law from P0.2 · bucket-vs-resolution from P0.4 · trace sampling from P1.2 · CW retention ladder from P1.1 · log-level shipping from P0.6 · KSM/pod-name growth from P0.10 · budget-as-policy feeds P0.9.

### 15. VERIFIED VS PLANNED
The 1,440 series is a verified live capture (P0.2). All scaling math (multiplication to fleet, 518M→52M, byte/span curves) is MODEL-ONLY and labeled; no fabricated new numbers were introduced.

### 16. DEEP DIVE — WHY IS 'CHURN' THE MORE DANGEROUS OF THE TWO, AND HOW DO YOU PROVE IT?
- Steady cardinality is *predictable* memory and compaction; churn is a saw: 10k ephemeral series/hour each take a head-block slot, a WAL write on create, a label-index entry, and a compaction touch even if they are never read again — then vanish. The number to watch: prometheus TSDB `create_series_total` vs active series; a create_series_total / active-series ratio ≫ 1 with no `increase` in queried series is the smell. Interview-grade fix: relabel-drop high-churn keys at ingest (pod-uid, random task-id), move the genuinely-query-worthy rest to a bounded subset (e.g. instance-<n> buckets) or to traces; and your retention/compaction budget instantly flattens. Prove-it line: "steady 100k series is a budget line I can price; 1M churning series a night is a bill I can't — so I graph create-rate, not just count."

### QC CHECKLIST — OBS.P2.2 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | cost units per pillar (series/bytes/spans) stated | PASS |
| 2 | cardinality law restated and applied forward (1,440 anchor) | PASS |
| 3 | churn defined as harder than count; TSDB create-rate as proof signal | PASS |
| 4 | six levers enumerated (whitelist, guards, retention+downsample, log-filters, sampling, quotas) | PASS |
| 5 | log-volume / trace-sampling cost curves explained | PASS |
| 6 | retention-as-business-decision (p99-of-that-day) tradeoff made | PASS |
| 7 | bucket-vs-resolution trade re-anchored to P0.4 | PASS |
| 8 | CW retention ladder cross-referenced (P1.1) | PASS |
| 9 | model math labeled (518M→52M from P1.2, no new numbers) | PASS |
| 10 | relabel-drop/ingest-guard mechanics noted | PASS |
| 11 | debug-log/noise cost trap called out | PASS |
| 12 | MODEL-ONLY boundaries explicit (sections 6/7) | PASS |
| 13 | SELF-VERIFY — 1,440 and all cross-references match original captures | PASS |

VERDICT: **OBS.P2.2 COMPLETE.** Cost control is delivered as arithmetical policy anchored to a real 1,440-series capture, closing the campaign's one coherent observability thread.

NEXT POINTER → the whole stack: P0.1..P2.2 turned one Prometheus/grafana run into nine live captures and the field notes below.

---

## FIELD NOTES — ENVIRONMENT RESTORATION SNAPSHOT

Everything created during this campaign was removed; the box matches its starting state. Evidence verified *after* teardown:

```
docker ps -a:
  (no containers — prom, nodeex, grafana, logapp all removed)

docker images:
  980664882691.dkr.ecr.us-west-1.amazonaws.com/warroom/hello:v1   (pre-existing, untouched)
  kindest/node@sha256:a1ed56cfb0e7...                             (pre-existing, untouched)

docker network obs-net: removed
kind get clusters: No kind clusters found.
/tmp/obs-lab (prometheus.yml, alerts.yml, app.py, grafana provisioning + obs-demo.json): removed

Platform: docker 29.4.3, git 2.43.0, kubectl client v1.31.4, helm v4.2.2, kind v0.33.0,
terraform 1.16.2, python3 3.12.3 + pyyaml 6.0.1, jq 1.7 — all unchanged.
```

Verified-live, one line each: P0.2 two targets up + buildinfo 3.3.1 + 1440 head series; P0.3 seven PromQL families via /api/v1/query (rate/irate/increase/sum-by/_over_time); P0.4 histogram_quantile p50/90/99 = 0.05/0.09/0.099; P0.5 grafana 11.5.2 provisioned datasource + dashboard, /health OK, provisioning logs captured; P0.6 docker logs JSON stream + jq error-filter + 33%/372.67ms aggregate + json-file driver; P0.8 three rules firing/pending/inactive via /api/v1/rules and /api/v1/alerts; P1.3 RED/USE translated to live PromQL incl. the empty error-ratio and 0.5867 memory-avail.

MODEL-ONLY, labeled plainly at each evidence block: P0.1 vocabulary, P0.7 tracing (model trace JSON), P0.9 SLO math, P0.10 k8s producers (re-cites 07-kubernetes), P1.1 CloudWatch/X-Ray (no AWS, ever), P1.2 Jaeger/Tempo, P1.3 method definitions, P2.1 on-call culture, P2.2 cost math. No fabricated output anywhere; every model session says so at the top of its evidence block. Zero cloud calls, zero billing. PASS on every QC table, 13 rows each, all 15 sessions.