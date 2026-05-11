/**
 * k6 load generator — Lab 02 Logs
 *
 * Designed to produce a rich mix of log levels in Loki:
 *   INFO    → /, /users, /orders, /login (success)
 *   WARNING → /slow (slow query detected), /login (401s), job saturation
 *   ERROR   → /error (always), /flaky (40% of hits)
 *
 * Traffic shape is deliberately uneven so you can spot patterns:
 * error spikes, slow query warnings, auth failure clusters.
 *
 * Run: docker compose run k6
 */

import http from "k6/http";
import { sleep, check } from "k6";

const BASE = "http://app:5000";

export const options = {
  stages: [
    { duration: "30s", target: 5  },   // ramp up
    { duration: "3m",  target: 15 },   // steady — watch logs flow in Grafana
    { duration: "30s", target: 30 },   // spike — error rate climbs, warnings spike
    { duration: "1m",  target: 5  },   // cooldown
    { duration: "30s", target: 0  },   // ramp down
  ],
};

export default function () {
  // INFO logs — healthy traffic
  check(http.get(`${BASE}/`),       { "home 200":   r => r.status === 200 });
  check(http.get(`${BASE}/users`),  { "users 200":  r => r.status === 200 });
  check(http.get(`${BASE}/orders`), { "orders 200": r => r.status === 200 });

  // WARNING logs — slow query warning fires on every hit
  http.get(`${BASE}/slow`);

  // ERROR logs — always 500
  http.get(`${BASE}/error`);

  // ERROR logs — 40% failure rate
  http.get(`${BASE}/flaky`);

  // WARNING logs — 30% produce 401 unauthorized warnings
  http.get(`${BASE}/login`);

  sleep(1);
}
