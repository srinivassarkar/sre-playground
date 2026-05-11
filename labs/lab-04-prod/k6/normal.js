/**
 * k6 — Normal Traffic (run this first)
 *
 * Establishes a healthy baseline so you can clearly see the incident
 * when it hits. Low error rate, normal latency, predictable throughput.
 *
 * Run: docker compose run k6-normal
 * Then immediately open Grafana and watch metrics stabilise.
 * Once you see steady lines, run k6-incident in another terminal.
 */

import http from "k6/http";
import { sleep, check } from "k6";

const BASE = "http://app:5000";

export const options = {
  stages: [
    { duration: "30s", target: 8  },   // ramp up
    { duration: "2m",  target: 8  },   // hold — establish baseline
    { duration: "30s", target: 0  },   // ramp down
  ],
};

export default function () {
  // Healthy traffic only — no /error, minimal /flaky
  check(http.get(`${BASE}/`),       { "home 200":   r => r.status === 200 });
  check(http.get(`${BASE}/users`),  { "users 200":  r => r.status === 200 });
  check(http.get(`${BASE}/orders`), { "orders 200": r => r.status === 200 });
  check(http.get(`${BASE}/login`),  { "login ok":   r => r.status !== 0   });

  sleep(1);
}
