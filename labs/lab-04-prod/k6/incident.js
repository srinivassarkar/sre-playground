/**
 * k6 — Incident Traffic
 *
 * Simulates a realistic production incident:
 *
 *   WHAT HAPPENS:
 *   A downstream dependency (payment-service) starts failing.
 *   Traffic to /flaky (which calls the upstream) spikes in error rate.
 *   /slow starts getting hammered — p99 latency climbs past SLO.
 *   Error budget burns fast. SLOBurnRateCritical alert fires.
 *
 *   WHAT YOU WILL SEE:
 *   Metrics  → error rate spike, p99 latency jump, error budget draining
 *   Logs     → flood of DependencyError and Slow query detected lines
 *   Traces   → upstream-call spans turning red, db-query-slow spans wide
 *
 *   YOUR JOB:
 *   Follow the README investigation steps to find root cause using
 *   the metrics → logs → traces loop.
 *
 * Run: docker compose run k6-incident
 */

import http from "k6/http";
import { sleep } from "k6";

const BASE = "http://app:5000";

export const options = {
  stages: [
    { duration: "30s", target: 5  },   // start gentle
    { duration: "1m",  target: 20 },   // ramp up — incident begins
    { duration: "2m",  target: 20 },   // hold at peak — alerts fire here
    { duration: "1m",  target: 5  },   // partial recovery
    { duration: "30s", target: 0  },   // ramp down
  ],
};

export default function () {
  // Still some healthy traffic — this is realistic.
  // Not everything breaks during an incident.
  http.get(`${BASE}/`);
  http.get(`${BASE}/users`);

  // The broken dependency — hammered hard during incident
  // 40% failure rate × high VUs = error rate explodes
  http.get(`${BASE}/flaky`);
  http.get(`${BASE}/flaky`);   // hit twice per iteration — doubles the pressure

  // Slow endpoint under load — latency degrades further
  http.get(`${BASE}/slow`);

  // Auth failures spike during incidents (retries, token expiry)
  http.get(`${BASE}/login`);

  // Always-error endpoint — keeps error rate elevated
  http.get(`${BASE}/error`);

  sleep(0.5);   // faster than normal — simulates retry storm
}
