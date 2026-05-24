/**
 * k6 — Anomaly Detection Load Scenario
 *
 * This scenario tests both reactive and predictive anomaly alerting.
 *
 * Reactive alert: Fires AFTER CPU/error rate exceeds threshold for N minutes
 *                 "The problem is already here"
 *
 * Predictive alert: Fires BEFORE threshold is breached based on trend
 *                   "We're trending toward the problem"
 *
 * The load pattern:
 *   - Ramp up baseline
 *   - Normal traffic for 30s (establish baseline)
 *   - Sudden spike to 30 VUs (reactive alert triggers after 2 min)
 *   - Hold spike for 2 min
 *   - Gradual ramp to 50 VUs (predictive alert detects trend)
 *   - Peak load for 2 min
 *   - Cool down back to baseline
 *
 * Run: docker compose run k6-anomaly-detection
 */

import http from "k6/http";
import { sleep, check } from "k6";

const BASE = "http://app:5000";

export const options = {
  stages: [
    // Ramp up from 0 to baseline
    { duration: "1m", target: 5 },

    // Establish baseline — normal traffic only
    { duration: "30s", target: 5 },

    // REACTIVE PHASE: Sudden spike
    // This triggers the reactive alert after 2 minutes of sustained high load
    { duration: "1m", target: 30 },  // Jump to 30 VUs
    { duration: "2m", target: 30 },  // Hold for 2 min (reactive alert fires around here)

    // PREDICTIVE PHASE: Gradual increase to test trend forecasting
    // Predictive alert should fire when linear regression detects trending toward 75%
    { duration: "2m", target: 50 },  // Ramp up to 50 VUs
    { duration: "2m", target: 50 },  // Hold peak

    // Cool down phase
    { duration: "1m", target: 10 },  // Drop back
    { duration: "1m", target: 0 },   // Ramp to zero
  ],
};

export default function () {
  // Mix of endpoints to create realistic traffic pattern
  const endpoint_choice = __VU % 5;

  let response;
  let url;

  switch (endpoint_choice) {
    case 0:
      // Fast endpoint
      url = `${BASE}/`;
      break;
    case 1:
      // Another fast endpoint
      url = `${BASE}/users`;
      break;
    case 2:
      // Slow endpoint (contributes to p99 latency issues)
      url = `${BASE}/slow`;
      break;
    case 3:
      // Error endpoint (always 500)
      url = `${BASE}/error`;
      break;
    default:
      // Flaky endpoint (40% fail rate)
      url = `${BASE}/flaky`;
  }

  response = http.get(url, {
    tags: { name: url },
  });

  // Just check that we got a response
  check(response, {
    "status is not error": (r) => r.status < 600,
  });

  // Small think time between requests
  sleep(0.5);
}
