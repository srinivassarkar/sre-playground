/**
 * k6 load generator — Lab 01 Metrics
 *
 * Hits every endpoint so all metric types get real data:
 *   /          → baseline healthy traffic
 *   /users     → medium latency
 *   /orders    → medium latency, two spans
 *   /slow      → drives p99 latency up
 *   /error     → drives error rate, fires HighErrorRate alert
 *   /flaky     → intermittent failures
 *   /login     → 401s, auth failure pattern
 *
 * Traffic shape:
 *   0→5 VUs over 30s   ramp up
 *   5→15 VUs over 2m   steady load — watch dashboards stabilise
 *   15→30 VUs over 30s spike — watch CPU + latency react
 *   30→10 VUs over 1m  recovery
 *   10→0 VUs over 30s  ramp down
 *
 * Run: docker compose run k6
 */

import http from "k6/http";
import { sleep, check } from "k6";

const BASE = "http://app:5000";

export const options = {
  stages: [
    { duration: "30s", target: 5  },
    { duration: "2m",  target: 15 },
    { duration: "30s", target: 30 },
    { duration: "1m",  target: 10 },
    { duration: "30s", target: 0  },
  ],
  thresholds: {
    // k6 will report these in the summary — good habit to define them
    http_req_failed: ["rate<0.5"],        // overall failure rate < 50% (error endpoint skews this)
    http_req_duration: ["p(95)<3000"],    // 95% of requests under 3s
  },
};

export default function () {
  // Healthy baseline — most traffic should be here
  check(http.get(`${BASE}/`),      { "home 200":   r => r.status === 200 });
  check(http.get(`${BASE}/users`), { "users 200":  r => r.status === 200 });
  check(http.get(`${BASE}/orders`),{ "orders 200": r => r.status === 200 });

  // Slow endpoint — drives p99 latency, triggers HighP99Latency alert
  check(http.get(`${BASE}/slow`),  { "slow alive": r => r.status !== 0 });

  // Always 500 — drives HighErrorRate + ErrorBudgetBurning alerts
  http.get(`${BASE}/error`);

  // 40% failure rate — intermittent errors
  http.get(`${BASE}/flaky`);

  // Auth failures — 30% 401
  http.get(`${BASE}/login`);

  sleep(1);
}
