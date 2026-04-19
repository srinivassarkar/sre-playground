# Traces — OpenTelemetry + Tempo + Grafana

## Overview

A **trace** represents the **entire journey of a single request** as it travels through your application and its services.

| Signal | What it shows |
|--------|--------------|
| Logs | What happened in the application (events, errors) |
| Traces | **How** the request flowed — service to service, with timing at each step |

### Stack
```
[App Server + OpenTelemetry] → [Grafana Tempo] → [Grafana]
```

**Alternatives:**
- OpenTelemetry collector → Jaeger collector
- Tempo → Jaeger

---

## Key Concepts

### Trace
The full end-to-end record of a single request. Made up of multiple **spans**.

### Span
A single unit of work within a trace (e.g., "hit /users endpoint", "query database"). Each span has:
- A name
- Start time + duration
- Parent span reference (to build the tree)
- Attributes/tags

### Example
A request to `/users` might produce:
```
Trace: GET /users
  └── users-span (Flask route handler)  ~50ms
        └── DB query span               ~45ms
```

---

## How It Works — Flow

```
1. App makes a request → OpenTelemetry SDK creates a Span
2. Span is exported via OTLP to Tempo (port 4318 HTTP / 4317 gRPC)
3. Tempo indexes and stores the trace data
4. Grafana queries Tempo → displays trace waterfall view
```

---

## OpenTelemetry (OTel)

OpenTelemetry is the **instrumentation agent**. It lives in your application code (or as an auto-instrumentation wrapper) and creates spans automatically or manually.

### Auto-instrumentation (Flask)
```python
FlaskInstrumentor().instrument_app(app)
# Automatically creates spans for every incoming HTTP request
```

### Manual spans
```python
with tracer.start_as_current_span("users-span"):
    time.sleep(0.05)  # simulate DB query
    return "Users data"
```

### OTLP Exporter
```python
exporter = OTLPSpanExporter(
    endpoint="http://127.0.0.1:4318/v1/traces"  # sends to Tempo
)
```

---

## Tempo

Tempo is the **trace storage backend**. It receives traces from OpenTelemetry, indexes them, and serves them to Grafana.

### Configuration (`/etc/tempo/config.yaml`)

```yaml
server:
  http_listen_port: 3200    # Grafana connects here to query traces
  grpc_listen_port: 9096

distributor:
  receivers:
    otlp:
      protocols:
        grpc:             # accepts traces on 4317
        http:             # accepts traces on 4318

ingester:
  trace_idle_period: 10s
  max_block_duration: 5m

compactor:
  compaction:
    block_retention: 1h   # keep traces for 1 hour (increase for prod)

storage:
  trace:
    backend: local
    local:
      path: /var/lib/tempo/traces
```

---

## Flask App with Tracing (`app.py`)

```python
from flask import Flask
import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

exporter = OTLPSpanExporter(endpoint="http://127.0.0.1:4318/v1/traces")
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(exporter))

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def home():
    with tracer.start_as_current_span("home-span"):
        return "Hello from EC2 + Python + OpenTelemetry + Grafana!"

@app.route("/users")
def users():
    with tracer.start_as_current_span("users-span"):
        time.sleep(0.05)   # simulate DB query delay
        return "Users data"
```

---

## Viewing Traces in Grafana

```
Connections → Data Sources → Tempo → URL: http://localhost:3200 → Save
Explore → Select Tempo → Search by Trace ID or Service Name → Run
```

Grafana shows a **waterfall view** — each span displayed as a bar showing duration and nesting.

---

## Setup Script

`applications-tracings.sh` does the following on the app server:

1. Installs Python3 + venv
2. Creates project directory `~/tracing-demo`
3. Sets up a virtual environment
4. Installs Flask + OpenTelemetry packages
5. Creates `app.py` with full OTel instrumentation
6. Runs the Flask app on port `5000`

**Python packages installed:**
- `flask`
- `opentelemetry-api`
- `opentelemetry-sdk`
- `opentelemetry-exporter-otlp`
- `opentelemetry-instrumentation`
- `opentelemetry-instrumentation-flask`

---

## Ports Reference

| Service | Port | Protocol |
|---------|------|----------|
| Flask App | 5000 | HTTP |
| Tempo HTTP API (Grafana) | 3200 | HTTP |
| Tempo gRPC | 9096 | gRPC |
| OTel OTLP HTTP receiver | 4318 | HTTP |
| OTel OTLP gRPC receiver | 4317 | gRPC |

---

## Trace Context Propagation — How Traces Cross Service Boundaries

This is the **core concept** that makes distributed tracing useful. Without it, each service would create its own isolated trace with no connection to the others.

### The Problem
```
User → Service A → Service B → Service C
```
If each service creates its own span independently, you get 3 disconnected traces. You can't tell they belong to the same request.

### The Solution: Trace Context Headers

When Service A calls Service B, it injects a **trace context header** into the HTTP request. Service B reads this header and creates its span as a **child** of Service A's span.

**W3C `traceparent` header (standard format):**
```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             │  │                                │                │
             │  └── Trace ID (16 bytes)          └── Span ID      └── Flags
             └── Version
```

- **Trace ID** — unique ID for the entire request journey (same across ALL services)
- **Span ID** — unique ID for this specific service's work
- **Flags** — sampling decision (01 = sampled/recorded)

### How It Flows
```
Service A receives request
  → OTel creates Span A (new Trace ID generated)
  → Service A calls Service B
      → OTel injects traceparent: TraceID + SpanA_ID
  → Service B reads header
      → OTel creates Span B (same TraceID, parent = Span A)
  → Service B calls Service C
      → OTel injects traceparent: TraceID + SpanB_ID
  → Service C creates Span C (same TraceID, parent = Span B)

Result in Grafana waterfall:
Trace ID: 4bf92f35...
  └── Span A: Service A /checkout       120ms
        └── Span B: Service B /payment   95ms
              └── Span C: DB query       80ms
```

### Auto Propagation in Python

When using `FlaskInstrumentor` + `RequestsInstrumentor`, context propagation is **fully automatic**:

```python
from opentelemetry.instrumentation.requests import RequestsInstrumentor
RequestsInstrumentor().instrument()

# Any requests.get/post now automatically injects traceparent header
import requests
response = requests.get("http://service-b/payment")  # traceparent injected ✅
```

### Sampling — Not Every Request Needs Tracing

| Strategy | Description | Use When |
|----------|-------------|----------|
| Always on | Trace 100% of requests | Dev / debugging |
| Head-based (probabilistic) | Decide at start — trace X% | High traffic prod |
| Tail-based | Decide after completion — always trace errors | Best for production |

```python
# Sample 10% of requests
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
provider = TracerProvider(sampler=TraceIdRatioBased(0.1))
```

---

## Key Concepts Summary

| Concept | Description |
|---------|-------------|
| Trace | Full end-to-end record of one request across all services |
| Span | Single unit of work within a trace |
| Trace ID | Unique ID shared by all spans in one request — links services together |
| Span ID | Unique ID for one specific span |
| Parent Span | The span that triggered the current one — builds the tree |
| `traceparent` header | W3C standard HTTP header that carries Trace ID + Span ID across services |
| OTel SDK | Instrumentation library that creates spans inside your app |
| OTLP | OpenTelemetry Protocol — how spans are exported to Tempo |
| Tempo | Trace storage and query backend |
| Auto-instrumentation | OTel wraps Flask/requests automatically — no manual code needed |
| Manual spans | Wrap specific code blocks to track custom operations |
| Head-based sampling | Decide to trace at request start — simple, low overhead |
| Tail-based sampling | Decide after request completes — smarter, captures all errors |