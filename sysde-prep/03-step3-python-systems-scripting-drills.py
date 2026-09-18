#!/usr/bin/env python3
"""
Step 3: Python Systems Scripting Drills for SysDE / SRE Interviews
Target: Amazon SysDE / Apple SRE Live Coding & Automation Rounds

These 4 scripts solve the most frequent live coding challenges in FAANG systems interviews.
All scripts use ONLY Python standard library (no pip dependencies required).
"""

import sys
import re
import os
import time
import random
import json
import math
from collections import Counter, defaultdict
import urllib.request
import urllib.error


# ==============================================================================
# DRILL 1: Production Access Log Parser & Top Error Aggregator
# Common Interview Prompt: "Given an access.log file, find the top 5 client IPs
# causing 5xx server errors and calculate p95 latency."
# ==============================================================================

LOG_SAMPLE = """
192.168.1.10 - - [18/Sep/2026:12:00:01 +0000] "GET /api/v1/checkout HTTP/1.1" 500 234 120
10.0.0.15 - - [18/Sep/2026:12:00:02 +0000] "GET /health HTTP/1.1" 200 45 5
192.168.1.10 - - [18/Sep/2026:12:00:03 +0000] "POST /api/v1/orders HTTP/1.1" 503 128 350
172.16.0.4 - - [18/Sep/2026:12:00:04 +0000] "GET /items HTTP/1.1" 200 1024 15
192.168.1.10 - - [18/Sep/2026:12:00:05 +0000] "GET /api/v1/checkout HTTP/1.1" 500 234 95
10.0.0.22 - - [18/Sep/2026:12:00:06 +0000] "POST /login HTTP/1.1" 502 512 800
10.0.0.22 - - [18/Sep/2026:12:00:07 +0000] "POST /login HTTP/1.1" 502 512 650
"""

# Regex pattern for Common Log Format + Status + Bytes + ResponseTimeMs
LOG_REGEX = re.compile(
    r'^(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+"(?P<method>\S+)\s+(?P<path>\S+)\s+[^"]+"\s+(?P<status>\d{3})\s+(?P<bytes>\S+)\s+(?P<duration>\d+)'
)

def parse_access_logs(log_lines, top_n=5):
    """
    Parses web access logs, aggregates 5xx errors by IP, and calculates p50, p95, p99 latency.
    """
    error_ip_counter = Counter()
    status_counter = Counter()
    durations = []

    for line in log_lines:
        line = line.strip()
        if not line:
            continue
        match = LOG_REGEX.match(line)
        if not match:
            continue

        ip = match.group('ip')
        status = int(match.group('status'))
        duration = int(match.group('duration'))

        status_counter[status] += 1
        durations.append(duration)

        if 500 <= status <= 599:
            error_ip_counter[ip] += 1

    durations.sort()
    count = len(durations)

    def percentile(p):
        if not durations:
            return 0
        idx = int(math.ceil((p / 100.0) * count)) - 1
        return durations[max(0, min(idx, count - 1))]

    results = {
        "total_requests": count,
        "status_distribution": dict(status_counter),
        "top_5xx_ips": error_ip_counter.most_common(top_n),
        "latency_ms": {
            "p50": percentile(50),
            "p95": percentile(95),
            "p99": percentile(99),
            "max": durations[-1] if durations else 0,
        }
    }
    return results


# ==============================================================================
# DRILL 2: Resilient HTTP Health Poller with Exponential Backoff & Full Jitter
# Common Interview Prompt: "Implement a health check client that queries a service,
# handles transient 5xx errors/timeouts, and retries with backoff and jitter."
# ==============================================================================

def check_endpoint_with_backoff(url, max_retries=4, base_backoff_sec=0.5, max_backoff_sec=5.0, timeout_sec=2.0):
    """
    Polls an HTTP URL with Exponential Backoff and Full Jitter (Amazon AWS standard algorithm).
    Algorithm: sleep = random_between(0, min(max_backoff, base * 2 ** attempt))
    """
    attempt = 0
    while attempt <= max_retries:
        print(f"[*] [Attempt {attempt + 1}/{max_retries + 1}] Polling {url}...")
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'AmazonSysDE-HealthChecker/1.0'}
            )
            with urllib.request.urlopen(req, timeout=timeout_sec) as response:
                status = response.status
                if 200 <= status < 300:
                    print(f"[+] SUCCESS: {url} returned HTTP {status}")
                    return True, status
                else:
                    print(f"[-] WARNING: {url} returned non-2xx status: {status}")
        except urllib.error.HTTPError as e:
            print(f"[-] HTTP Error {e.code}: {e.reason}")
            # Do not retry 4xx client errors (400, 401, 403, 404)
            if 400 <= e.code < 500:
                print("[!] Client error detected; aborting retries.")
                return False, e.code
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"[-] Network/Timeout Error: {e.reason if hasattr(e, 'reason') else e}")

        attempt += 1
        if attempt <= max_retries:
            # Amazon Full Jitter formula
            ceiling = min(max_backoff_sec, base_backoff_sec * (2 ** attempt))
            sleep_duration = random.uniform(0, ceiling)
            print(f"    [~] Backing off for {sleep_duration:.2f}s before retry...")
            time.sleep(sleep_duration)

    print(f"[!] FAILED: {url} remained unreachable after {max_retries + 1} attempts.")
    return False, None


# ==============================================================================
# DRILL 3: Zero-Dependency Linux /proc System Telemetry Poller
# Common Interview Prompt: "Write a script to collect CPU load and Memory stats
# directly from Linux /proc without importing external libraries."
# ==============================================================================

def collect_proc_telemetry():
    """
    Reads directly from /proc/loadavg and /proc/meminfo on Linux.
    Falls back gracefully if run on non-Linux development machines (macOS/Windows).
    """
    telemetry = {
        "timestamp": int(time.time()),
        "os": sys.platform,
        "load_average": {},
        "memory_mb": {}
    }

    # 1. Read Load Average (/proc/loadavg)
    if os.path.exists("/proc/loadavg"):
        with open("/proc/loadavg", "r") as f:
            parts = f.read().split()
            telemetry["load_average"] = {
                "1m": float(parts[0]),
                "5m": float(parts[1]),
                "15m": float(parts[2]),
                "runnable_threads": parts[3]
            }
    else:
        # Fallback simulation for non-Linux OS
        telemetry["load_average"] = {"1m": 0.42, "5m": 0.58, "15m": 0.65, "simulated": True}

    # 2. Read Memory Info (/proc/meminfo)
    if os.path.exists("/proc/meminfo"):
        mem_data = {}
        with open("/proc/meminfo", "r") as f:
            for line in f:
                key, val = line.split(":", 1)
                val_num = val.strip().split()[0]
                mem_data[key.strip()] = int(val_num)

        total_kb = mem_data.get("MemTotal", 0)
        free_kb = mem_data.get("MemFree", 0)
        avail_kb = mem_data.get("MemAvailable", free_kb)

        telemetry["memory_mb"] = {
            "total": round(total_kb / 1024, 2),
            "free": round(free_kb / 1024, 2),
            "available": round(avail_kb / 1024, 2),
            "used_pct": round(((total_kb - avail_kb) / total_kb) * 100, 2) if total_kb else 0
        }
    else:
        telemetry["memory_mb"] = {"total": 16384.0, "available": 8192.0, "used_pct": 50.0, "simulated": True}

    return telemetry


# ==============================================================================
# DRILL 4: Safe Log File Cleanup & Disk Reclaimer
# Common Interview Prompt: "Write a script to find and clean up .log files in a
# directory older than X days or larger than Y MB, with a --dry-run option."
# ==============================================================================

def clean_old_logs(directory, max_age_days=7, min_size_mb=100, dry_run=True):
    """
    Scans directory for logs matching criteria and either reports or truncates/deletes them safely.
    """
    now = time.time()
    age_threshold_sec = max_age_days * 86400
    size_threshold_bytes = min_size_mb * 1024 * 1024

    candidates = []
    total_bytes_reclaimable = 0

    if not os.path.exists(directory):
        return {"error": f"Directory {directory} does not exist"}

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.log', '.txt')):
                filepath = os.path.join(root, file)
                try:
                    stat = os.stat(filepath)
                    age_sec = now - stat.st_mtime
                    size_bytes = stat.st_size

                    if age_sec > age_threshold_sec or size_bytes > size_threshold_bytes:
                        candidates.append({
                            "path": filepath,
                            "size_mb": round(size_bytes / (1024 * 1024), 2),
                            "age_days": round(age_sec / 86400, 1)
                        })
                        total_bytes_reclaimable += size_bytes

                        if not dry_run:
                            # SAFE TRUNCATION (does not break open file descriptors held by running processes!)
                            with open(filepath, 'w') as f:
                                f.truncate(0)
                            print(f"[CLEANED] Truncated {filepath}")
                except (PermissionError, FileNotFoundError):
                    continue

    return {
        "dry_run": dry_run,
        "candidates_found": len(candidates),
        "reclaimable_mb": round(total_bytes_reclaimable / (1024 * 1024), 2),
        "files": candidates
    }


# ==============================================================================
# SELF-TEST RUNNER
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print(">>> RUNNING DRILL 1: Log Parsing & Latency Percentiles")
    print("=" * 70)
    log_results = parse_access_logs(LOG_SAMPLE.strip().split("\n"))
    print(json.dumps(log_results, indent=2))

    print("\n" + "=" * 70)
    print(">>> RUNNING DRILL 3: Linux /proc Telemetry Collector")
    print("=" * 70)
    telemetry = collect_proc_telemetry()
    print(json.dumps(telemetry, indent=2))

    print("\n" + "=" * 70)
    print(">>> RUNNING DRILL 4: Safe Log Cleanup Simulation (Dry-Run)")
    print("=" * 70)
    cleanup_result = clean_old_logs(".", max_age_days=1, min_size_mb=1, dry_run=True)
    print(f"Found {cleanup_result['candidates_found']} files, reclaimable: {cleanup_result['reclaimable_mb']} MB")
    print("=" * 70)
    print("[ALL DRILLS EXECUTED CLEANLY]")
