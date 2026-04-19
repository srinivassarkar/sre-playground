import logging
import os
import random
import time

from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("python-app")

# ── OpenTelemetry Tracing ─────────────────────────────────────────────────────
provider = TracerProvider()
otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://tempo:4318/v1/traces")
)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# ── Flask App ─────────────────────────────────────────────────────────────────
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# ── Prometheus Metrics ────────────────────────────────────────────────────────
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)
ERROR_COUNT = Counter(
    "app_errors_total",
    "Total application errors",
    ["endpoint", "error_type"]
)

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    start = time.time()
    with tracer.start_as_current_span("home-handler"):
        logger.info("GET / - home endpoint hit")
        REQUEST_COUNT.labels(method="GET", endpoint="/", status="200").inc()
        REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)
        return jsonify({"status": "ok", "service": "python-app"})


@app.route("/users")
def users():
    start = time.time()
    with tracer.start_as_current_span("users-handler"):
        with tracer.start_as_current_span("db-query"):
            # simulate DB query delay
            delay = random.uniform(0.05, 0.3)
            time.sleep(delay)
            logger.info(f"GET /users - db query completed in {delay:.3f}s")

        REQUEST_COUNT.labels(method="GET", endpoint="/users", status="200").inc()
        REQUEST_LATENCY.labels(endpoint="/users").observe(time.time() - start)
        return jsonify({"users": ["alice", "bob", "charlie"], "count": 3})


@app.route("/orders")
def orders():
    start = time.time()
    with tracer.start_as_current_span("orders-handler"):
        # simulate occasional slow response
        if random.random() < 0.3:
            delay = random.uniform(1.0, 2.5)
            time.sleep(delay)
            logger.warning(f"GET /orders - slow response: {delay:.3f}s")
        else:
            time.sleep(random.uniform(0.01, 0.1))
            logger.info("GET /orders - response ok")

        REQUEST_COUNT.labels(method="GET", endpoint="/orders", status="200").inc()
        REQUEST_LATENCY.labels(endpoint="/orders").observe(time.time() - start)
        return jsonify({"orders": [101, 102, 103]})


@app.route("/payments")
def payments():
    start = time.time()
    with tracer.start_as_current_span("payments-handler"):
        with tracer.start_as_current_span("payment-service-call"):
            time.sleep(random.uniform(0.05, 0.15))

        # simulate payment failures ~20% of the time
        if random.random() < 0.2:
            logger.error("GET /payments - payment processing FAILED: gateway timeout")
            ERROR_COUNT.labels(endpoint="/payments", error_type="gateway_timeout").inc()
            REQUEST_COUNT.labels(method="GET", endpoint="/payments", status="500").inc()
            REQUEST_LATENCY.labels(endpoint="/payments").observe(time.time() - start)
            return jsonify({"error": "payment gateway timeout"}), 500

        logger.info("GET /payments - payment processed successfully")
        REQUEST_COUNT.labels(method="GET", endpoint="/payments", status="200").inc()
        REQUEST_LATENCY.labels(endpoint="/payments").observe(time.time() - start)
        return jsonify({"status": "payment_ok", "transaction_id": random.randint(10000, 99999)})


@app.route("/crash")
def crash():
    """
    Break scenario: intentionally causes errors.
    Hit this endpoint to see alerts fire.
    """
    logger.error("GET /crash - intentional crash triggered!")
    ERROR_COUNT.labels(endpoint="/crash", error_type="intentional").inc()
    REQUEST_COUNT.labels(method="GET", endpoint="/crash", status="500").inc()
    raise Exception("Intentional crash for lab purposes")


@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({"error": str(e)}), 500


@app.route("/metrics")
def metrics():
    """Prometheus scrape endpoint."""
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    logger.info("Starting python-app on port 5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
