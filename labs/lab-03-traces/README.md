# Lab 03 — Traces

**Stack:** OpenTelemetry · Tempo · Grafana

**You will learn:**
1. How a trace is created and exported from the app to Tempo
2. How to find a trace by service name and read the waterfall view
3. How to identify which span is the bottleneck
4. What nested spans look like and what they tell you
5. How a broken/errored span appears vs a healthy one

---

## How traces flow in this lab

```
app receives request
    ↓
OTel SDK creates a root span (auto via FlaskInstrumentor)
    ↓
app code creates child spans manually (db-query, cache-lookup etc.)
    ↓
BatchSpanProcessor batches completed spans
    ↓
OTLPSpanExporter HTTP POST → Tempo :4318
    ↓
Tempo indexes by Trace ID, stores span blocks in /var/tempo (tmpfs)
    ↓
Grafana queries Tempo → waterfall view
```

The only difference from Labs 01 + 02: `OTLP_ENDPOINT=http://tempo:4318` is set in the compose file. The same image, same app — tracing just switches on.

---

## Zero-trace design

| Service | Data path | Storage |
|---------|-----------|---------|
| Tempo traces | `/var/tempo/traces` | tmpfs |
| Tempo WAL | `/var/tempo/wal` | tmpfs |
| Grafana | `/var/lib/grafana` | tmpfs |

`docker compose down` leaves nothing.

---

## Start the lab

```bash
cd lab-03-traces
docker compose up -d
```

Wait 20 seconds, then verify:

```bash
docker compose ps
```

Check the app started with tracing enabled:

```bash
docker logs lab03-app | head -5
```

You should see:
```json
{"level": "INFO", "message": "Tracing enabled", "otlp_endpoint": "http://tempo:4318"}
```

Generate some traces:

```bash
curl localhost:5000/
curl localhost:5000/users
curl localhost:5000/orders
curl localhost:5000/slow
curl localhost:5000/error
```

Open Grafana: http://localhost:3000 → Explore → Tempo.

---

## Step 1 — Understand what a trace actually is

**What:** A trace is the complete record of one request's journey through your system. It's made of spans — each span is one unit of work with a name, start time, duration, and optional child spans.

**Why:** Metrics tell you error rate is 40%. Logs tell you which endpoint is failing. Traces tell you *exactly which function call inside that endpoint* is taking 2 seconds. That's the level of precision you need to fix the right thing.

**How:**

Hit the `/users` endpoint:

```bash
curl localhost:5000/users
```

Watch the app logs — you'll see the `trace_id` in the JSON:

```bash
docker logs lab03-app --tail=5
```

```json
{"level": "INFO", "message": "200 GET /users", "trace_id": "dd84c3b617...", "span_id": "51f82a4ff2..."}
```

Copy the `trace_id`. Go to **Grafana → Explore → Tempo**, paste it into the **TraceID** search box and hit Run.

You'll see the waterfall: two bars — `users-handler` (parent) and `db-query` (child). The child span represents the simulated database call. The parent can't complete until the child does.

> **SRE insight:** Every trace has one root span and zero or more child spans. The root span duration = total request time. Child spans show where that time was spent.

---

## Step 2 — Find traces by service name

**What:** In production you won't have a specific trace ID to search for. You'll search by service name, then filter by duration or status to find problematic traces.

**Why:** This is the real-world workflow. Alert fires → you know which service → you search its recent traces for slow or errored ones → you find the root cause.

**How:**

Go to **Grafana → Explore → Tempo**.

Change the query type to **Search** (not TraceID).

Set:
- **Service Name:** `sre-lab-app`
- **Span Name:** leave empty (search all spans)
- **Duration:** min `800ms` (to find only slow traces)

Hit Run. You'll see a list of traces from `/slow` — each one took 800ms+.

Click any trace. The waterfall opens. You'll see:
```
GET /slow                           ~1.2s  ← root span (Flask auto-instrumented)
  └── slow-handler                  ~1.2s  ← manual span wrapping the route
        └── db-query-slow           ~1.1s  ← child span — THIS is where the time went
```

The `db-query-slow` span takes 90%+ of the total request time. In a real system this tells you exactly which database call to optimise.

Now filter for errors:
- **Status:** `Error`

You'll see traces from `/error` and `/flaky`. Click one — the errored span is highlighted in red.

> **SRE insight:** Duration filtering is your fastest path to slow traces. Set min duration to your SLO latency threshold and you'll immediately see only the traces that are breaching it.

---

## Step 3 — Read the waterfall and find the bottleneck

**What:** The waterfall shows spans as horizontal bars. Width = duration. Indentation = nesting (parent → child). The widest child span is your bottleneck.

**Why:** A request can be slow for many reasons — network, DB, external API, serialisation. The waterfall makes it visually obvious which one is responsible without any guesswork.

**How:**

Run the load generator:

```bash
docker compose run k6
```

While it runs, go to Tempo Search, service `sre-lab-app`, and look at traces from different endpoints side by side.

**`/` — single span:**
```
GET /                    ~15ms
  └── home-handler       ~15ms
```
No children. All time in the handler itself.

**`/users` — two spans:**
```
GET /users               ~120ms
  └── users-handler      ~120ms
        └── db-query     ~110ms   ← bottleneck
```
The DB query takes 90% of the time. The handler itself is nearly instant.

**`/orders` — three spans:**
```
GET /orders              ~100ms
  └── orders-handler     ~100ms
        ├── db-query      ~70ms
        └── cache-lookup  ~25ms   ← runs after db-query, not parallel
```
Two sequential child spans. Note: they run one after the other (sequential), not at the same time (parallel). You can tell because they don't overlap horizontally in the waterfall.

**`/slow` — the obvious bottleneck:**
```
GET /slow                ~1.5s
  └── slow-handler       ~1.5s
        └── db-query-slow ~1.4s  ← 93% of total time
```

> **SRE insight:** The widest bar in the waterfall is the bottleneck. If it's a DB span, talk to the DB team. If it's an external API call, check that dependency's SLO. The waterfall tells you who to call.

---

## Step 4 — What nested spans tell you

**What:** Child spans represent work done *inside* a parent operation. They let you break down "the request took 1.5 seconds" into "DB query: 1.4s, serialisation: 0.05s, network: 0.05s".

**Why:** Without child spans, you know a request was slow but not why. With them, you can attribute time to specific operations and fix the right one. A 1.4s DB query needs a different fix than a 1.4s external API call.

**How:**

Look at the app code that produces these spans (`app.py` in the Docker image):

```python
@app.route("/orders")
def orders():
    with tracer.start_as_current_span("orders-handler"):
        with tracer.start_as_current_span("db-query"):
            time.sleep(random.uniform(0.03, 0.1))     # DB read
        with tracer.start_as_current_span("cache-lookup"):
            time.sleep(random.uniform(0.01, 0.04))    # Cache check
```

Two sequential `with` blocks = two sequential child spans. They appear side by side in the waterfall (db-query finishes, then cache-lookup starts).

Now compare: what if the DB query and cache lookup ran in parallel (threads)? The total time would be `max(db, cache)` instead of `db + cache`. The waterfall would show them overlapping horizontally. That's a common optimisation pattern you can spot in traces.

Now click into any span in Grafana. Expand the **Span Attributes** section. You'll see:
- `http.method`, `http.url`, `http.status_code` — added automatically by FlaskInstrumentor
- Any custom attributes added via `span.set_attribute()` in the code

> **SRE insight:** Good span naming and attributes are as important as good log messages. "db-query" is useful. "query" is not. "db-query-slow" tells you immediately what to look at.

---

## Step 5 — Errored spans vs healthy spans

**What:** When a span ends in an error, Tempo marks it with status `Error` and highlights it red in the waterfall. This is separate from HTTP status codes — it's the OTel span status.

**Why:** In a distributed system you might have 10 services in a trace. One fails. Without error status on spans, you'd have to read through all span attributes to find which one. The red highlight takes you straight there.

**How:**

Hit the error endpoint a few times:

```bash
for i in {1..5}; do curl -s localhost:5000/error > /dev/null; done
for i in {1..5}; do curl -s localhost:5000/flaky > /dev/null; done
```

Go to Tempo Search → Status: `Error`.

Click a trace from `/error`. The root span is red — the error happened at the top level, not in a child. Click the span — look at the attributes for `http.status_code: 500` and `otel.status_code: ERROR`.

Now click a trace from `/flaky` where the error happened. The structure is:
```
GET /flaky                    ERROR
  └── flaky-handler           ERROR
        └── upstream-call     ERROR  ← where it actually failed
```

The error propagated up from `upstream-call` → `flaky-handler` → root span. This is trace context propagation working correctly — you can see exactly where in the call chain the failure originated.

Compare with a successful `/flaky` trace:
```
GET /flaky                    OK
  └── flaky-handler           OK
        └── upstream-call     OK
```

Same structure, different outcome. The span tree tells the story.

> **SRE insight:** Always look at the deepest red span first — that's where the error originated. The parent spans are red because they inherited the error status from their child.

---

## Build your trace dashboard

Grafana → Dashboards → New → Add visualisation → Tempo.

| Panel | Config | Type |
|-------|--------|------|
| Trace search | Service: `sre-lab-app` | Table (shows list of traces) |
| Rate of traces | Switch to Prometheus datasource: `rate(tempo_distributor_spans_received_total[1m])` | Time series |
| Slow traces | Service: `sre-lab-app`, Min duration: `500ms` | Table |
| Error traces | Service: `sre-lab-app`, Status: `Error` | Table |

The trace table panels let you click any row to open the waterfall directly — useful for a live incident board.

---

## Tear down

```bash
docker compose down
```

Verify:
```bash
docker volume ls | grep lab03   # empty
docker ps -a | grep lab03       # empty
```

---

## Trace concepts reference

| Concept | Description |
|---------|-------------|
| Trace | Complete record of one request — made of spans |
| Span | Single unit of work: name + start time + duration + status |
| Root span | First span in a trace — total duration = total request time |
| Child span | Work done inside a parent span — shows where time was spent |
| Trace ID | 32-character hex ID shared by all spans in one request |
| Span ID | 16-character hex ID unique to one span |
| `traceparent` | W3C header that carries Trace ID across service boundaries |
| OTLP | OpenTelemetry Protocol — how spans are exported to Tempo |
| BatchSpanProcessor | Buffers spans and sends in batches — more efficient than one-by-one |
| Status: Error | Span ended in failure — highlighted red in Grafana waterfall |
| Auto-instrumentation | FlaskInstrumentor creates root spans automatically for every request |
| Manual spans | `with tracer.start_as_current_span("name"):` — wraps specific code blocks |

---

→ **Next: Lab 04 — Production** — all three pillars together. A real incident fires, you investigate using the full metrics → logs → traces loop.
