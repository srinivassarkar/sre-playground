/**
 * k6 load generator — Lab 03 Traces
 *
 * Low VU count (5) — we care about trace quality not volume.
 * Each endpoint produces a different span structure:
 *
 *   /          → single span (home-handler)
 *   /users     → parent + child (users-handler → db-query)
 *   /orders    → parent + 2 children (orders-handler → db-query + cache-lookup)
 *   /slow      → parent + slow child (slow-handler → db-query-slow 800ms-2.5s)
 *   /error     → single span, status ERROR
 *   /flaky     → parent + child, 40% end in ERROR status
 *
 * In Grafana Explore → Tempo, search by service name "sre-lab-app"
 * and compare the waterfall shapes across these endpoints.
 *
 * Run: docker compose run k6
 */

import http from "k6/http";
import { sleep } from "k6";

const BASE = "http://app:5000";

export const options = {
  stages: [
    { duration: "30s", target: 5  },   // ramp up
    { duration: "4m",  target: 5  },   // steady — explore traces in Grafana
    { duration: "30s", target: 0  },   // ramp down
  ],
};

export default function () {
  // Single span
  http.get(`${BASE}/`);

  // Two spans — parent + db-query child
  http.get(`${BASE}/users`);

  // Three spans — parent + db-query + cache-lookup
  http.get(`${BASE}/orders`);

  // Two spans — slow child makes this easy to spot in waterfall
  http.get(`${BASE}/slow`);

  // Error span
  http.get(`${BASE}/error`);

  // Intermittent error span
  http.get(`${BASE}/flaky`);

  sleep(2);   // slightly longer sleep — gives time to explore each trace
}
