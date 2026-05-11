# Observability Labs

## Lab 01: Metrics
```bash
cd labs/lab-01-metrics
docker compose up -d
docker compose run k6
```

## Lab 02: Logs
```bash
cd labs/lab-02-logs
docker compose up -d
docker compose run k6
```

## Lab 03: Traces
```bash
cd labs/lab-03-traces
docker compose up -d
docker compose run k6
```

## Lab 04 (Final Boss)
```bash
cd labs/lab-04-prod
docker compose up -d
docker compose run k6-normal    # baseline first
docker compose run k6-incident  # then trigger the incident
```