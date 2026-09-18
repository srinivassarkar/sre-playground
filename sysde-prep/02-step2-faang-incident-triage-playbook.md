# Step 2: FAANG Incident Triage Playbook & Live Debugging Guide
**Target Roles:** Amazon Systems Development Engineer (SysDE) / Apple Site Reliability Engineer (SRE)  
**Philosophy:** Triage Fast $\to$ Mitigate Customer Impact $\to$ Isolate Root Cause $\to$ Post-Mortem & Prevent Recurrence

---

## 1. Amazon SysDE Interview Philosophy: The 2-Phase Response

In an Amazon SysDE scenario interview, the interviewer is **NOT** just looking for the technical command. They are evaluating your **Leadership Principles**:
* **Customer Obsession & Bias for Action:** Mitigate customer pain **first** (drain traffic, restart daemon, scale up, roll back) before spending 3 hours doing forensics.
* **Dive Deep & Ownership:** Once customers are safe, isolate the exact root cause (trace logs, inspect kernel state, reproduce bug) and implement a permanent safeguard so it never recurs.

---

## 2. The 5 Classic FAANG Incident Scenarios

### Scenario 1: High Load Average, Low CPU Usage
**Interviewer Prompt:** *"Monitoring alerts on a production host with 8 vCPUs. The 1-minute load average is 28, but `top` shows `%idle` is 90% and `%user` is 8%. What is happening, and how do you triage it?"*

#### The Mental Model:
Load average counts threads in **R state (Runnable)** + **D state (Uninterruptible Sleep)**. Since CPU is 90% idle, the runnable queue is near zero. Therefore, 25+ threads are trapped in the **D state** waiting on synchronous disk I/O, NFS locks, or kernel hardware waits.

#### Triage Steps & Commands:
1. **Confirm I/O Wait:**
   ```bash
   vmstat 1 5
   # Look at the 'b' column (processes blocked in D state) and 'wa' (iowait %).
   # If 'b' > 10 and 'wa' > 40%, the storage subsystem is severely bottlenecked.
   ```
2. **Identify the Storage Device:**
   ```bash
   iostat -xz 1 5
   # Check '%util' (is a disk pinned at 99-100%?)
   # Check 'await' (average time in ms for I/O requests. Normal: < 5ms. Bottleneck: > 50-100ms).
   ```
3. **Identify the Stuck Processes:**
   ```bash
   ps aux | awk '$8 ~ /D/'
   # Pinpoint the PID and binary name of the threads in D state.
   ```
4. **Check Kernel Traces & Mounts:**
   ```bash
   # Check if an NFS mount or EBS volume hung:
   dmesg -T | tail -n 20
   cat /proc/<PID>/stack
   # /proc/<PID>/stack shows the exact kernel function where the thread is blocked!
   ```
5. **Interview Talk-Track:**
   > *"Because the CPU idle time is 90% while the load is 28, the load is driven by processes in the uninterruptible sleep state (`D-state`). I would run `vmstat 1` to check the blocked process column and `iostat -xz 1` to check disk saturation. If `await` is excessive, I'll identify the offending process with `ps aux | awk '$8 ~ /D/'`. If it's a hung NFS mount or EBS volume, I will fail over the traffic to healthy replicas before unmounting or rebooting the host."*

---

### Scenario 2: `df -h` Shows 100% Disk Full, but `du -sh` Shows Minimal Usage
**Interviewer Prompt:** *"Disk alerts fire at 3 AM: `/var/log` is 100% full according to `df -h`. You run `du -sh /var/log/*` and the total is only 15 GB on a 100 GB volume. What happened, and how do you fix it without crashing production?"*

#### The Mental Model:
Linux filesystem storage is tracked by inodes and data blocks. When a running process has an open file descriptor (FD) to a file and someone executes `rm /var/log/app.log`, the filename is unlinked from the directory tree, but the kernel **does not free the disk blocks** until the file descriptor count drops to 0 (when the process exits or closes the handle).

#### Triage Steps & Commands:
1. **Find the Open Deleted Files:**
   ```bash
   lsof +L1
   # Or:
   lsof /var/log | grep -i deleted
   # Output displays: COMMAND, PID, USER, FD, SIZE, and "(deleted)"
   ```
2. **Immediate Mitigation (Reclaim Disk Space Instantly):**
   * **Do NOT kill the service blindly if it handles critical user transactions.**
   * Truncate the file via its open file descriptor in `/proc`:
   ```bash
   # Locate the descriptor number (e.g. fd 4):
   > /proc/<PID>/fd/<FD_NUM>
   # Example: > /proc/14231/fd/4
   # This immediately zeroes the underlying disk blocks, dropping usage from 100% to 0%!
   ```
3. **Graceful Service Restart & Log Rotation Fix:**
   ```bash
   # Gracefully reload the daemon to release the FD cleanly:
   systemctl reload <service_name>
   
   # Permanent safeguard: Verify logrotate configuration:
   # Ensure 'copytruncate' is set in /etc/logrotate.d/<app> so daemons don't keep deleted FDs.
   ```

---

### Scenario 3: Production 502 Bad Gateway / 504 Gateway Timeout
**Interviewer Prompt:** *"Users are reporting intermittent 502 and 504 errors on our web application. Walk me through your diagnostic sequence from edge to backend."*

#### The Mental Model (The 502 vs 504 Distinction):
* **502 Bad Gateway:** The reverse proxy / load balancer reached the backend host, but the backend **refused the connection**, dropped the connection immediately (TCP RST), or returned a malformed response.
* **504 Gateway Timeout:** The reverse proxy connected to the backend, but the backend took **longer than the proxy timeout threshold** (e.g. 60s) to return an HTTP response.

#### Triage Ladder:
```
Client  -->  Route53 (DNS)  -->  ALB / CloudFront  -->  Nginx / Reverse Proxy  -->  App (Node.js/Python/Go)  -->  Database
```

1. **Verify at Edge (Proxy / ALB Logs):**
   ```bash
   # Check Nginx error log:
   tail -n 50 /var/log/nginx/error.log
   # Look for: "connect() failed (111: Connection refused)" -> Backend is dead.
   # Look for: "upstream timed out (110: Connection timed out)" -> Backend is slow/hanging.
   ```
2. **Check Backend Process Health:**
   ```bash
   # Is the application process running?
   ps aux | grep -i node
   systemctl status backend-app
   
   # Has it been crashing and restarting in a loop?
   journalctl -u backend-app -n 100 --no-pager
   ```
3. **Test Local Socket Connectivity:**
   ```bash
   # Is the app listening on its expected local port (e.g. 3000)?
   ss -tulpn | grep 3000
   
   # Bypass the reverse proxy and curl localhost directly:
   curl -Iv http://127.0.0.1:3000/health
   ```
4. **Check Backend Bottlenecks (DB & Thread Pool):**
   * If `curl localhost` hangs: The app event loop is blocked (CPU bound) or all database connection pool handles are exhausted waiting on slow queries.
   * Check open connections:
     ```bash
     ss -ant '( sport = :3000 or dport = :3306 )' | wc -l
     ```

---

### Scenario 4: Silent Process Crash with Exit Code 137 (OOM Killer)
**Interviewer Prompt:** *"A containerized Python inference service or Node.js backend mysteriously vanished with exit code 137. There are no application error logs. How do you prove what happened?"*

#### The Mental Model:
Exit Code $137 = 128 + 9$ (`SIGKILL`). When a process exits 137 with zero stack trace, it was forcibly terminated by an external actor. 99% of the time, that actor is the Linux kernel **Out-of-Memory (OOM) Killer**.

#### Triage Steps & Commands:
1. **Search Kernel Ring Buffer:**
   ```bash
   dmesg -T | grep -iE 'oom[-_]killer|killed process'
   # Look for lines like:
   # "Out of memory: Killed process 4192 (python3) total-vm:8291040kB, anon-rss:4192000kB"
   ```
2. **Check Systemd & cgroup limits:**
   ```bash
   # If running in systemd or Docker/K8s:
   journalctl -u <service> -e
   # Check if MemoryMax or pod memory limits were exceeded.
   ```
3. **Mitigation & Fix:**
   * **Immediate:** Increase host/cgroup memory limit, or enable temporary swap.
   * **Permanent Root Cause:** Profile memory allocations. Look for unbounded memory leaks (e.g., in-memory caching without TTL, massive database query results loaded into memory at once).

---

### Scenario 5: Intermittent Connection Drops & "Cannot Assign Requested Address"
**Interviewer Prompt:** *"Under peak traffic, your service logs show: `connect(): Cannot assign requested address`. The server has plenty of CPU and RAM. What is exhausted?"*

#### The Mental Model:
**Ephemeral Port Exhaustion.** When an outgoing service (e.g. reverse proxy or API gateway) makes tens of thousands of rapid HTTP requests to an upstream microservice without connection pooling / keep-alive:
* Every connection allocates an ephemeral port from the range (e.g. 32768–60999 = ~28,000 ports).
* When closed, sockets stay in `TIME_WAIT` for 60 seconds.
* If throughput exceeds ~500 new connections/sec, all ephemeral ports are trapped in `TIME_WAIT`, and new outgoing connections fail with `EADDRNOTAVAIL` (`Cannot assign requested address`).

#### Triage Steps & Commands:
1. **Check TIME_WAIT Counts:**
   ```bash
   ss -ant state time-wait | wc -l
   ```
2. **Check Ephemeral Port Range:**
   ```bash
   cat /proc/sys/net/ipv4/ip_local_port_range
   # Default is usually: 32768 60999
   ```
3. **Fixes:**
   * **Application Level (Best):** Enable HTTP Keep-Alive / connection pooling so connections are reused rather than opened and closed for every request.
   * **Kernel Level (Tuning):**
     ```bash
     # Enable TCP time-wait reuse for outgoing sockets:
     sysctl -w net.ipv4.tcp_tw_reuse=1
     
     # Expand local port range:
     sysctl -w net.ipv4.ip_local_port_range="10240 65535"
     ```

---

## 3. The 4 Golden Signals (Google SRE & Amazon Operational Excellence)

Always frame monitoring and RCA answers using the **4 Golden Signals**:
1. **Latency:** Time taken to service a request (distinguish p50, p90, p99; never rely solely on average).
2. **Traffic:** Demand placed on system (requests per second, concurrent connections, I/O bandwidth).
3. **Errors:** Rate of requests that fail (explicit 5xx errors, implicit malformed payloads, timeouts).
4. **Saturation:** How "full" the system is (CPU run queue, memory available, disk %util, connection pool depth).
