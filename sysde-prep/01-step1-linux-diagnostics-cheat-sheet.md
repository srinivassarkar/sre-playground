# Step 1: Linux Systems Diagnostics & Internals Cheat Sheet
**Target Roles:** Amazon Systems Development Engineer (SysDE) / Apple Site Reliability Engineer (SRE)  
**Methodology:** The USE Method (Utilization, Saturation, Errors) & First-Principles Diagnostics

---

## 1. The SysDE First 60 Seconds: The Universal Diagnostic Sequence

When an interviewer says: *"A production host is degrading or unresponsive. You just SSH'd in. What do you run?"*

Never guess. Run this exact sequence:

```bash
# 1. Check uptime, users, and load average (1m, 5m, 15m)
uptime

# 2. Check process run queues, blocked tasks, swap in/out, and CPU breakdown (every 1 sec)
vmstat 1 5

# 3. Check memory breakdown (Physical RAM, Buffers, Cached, Available, Swap)
free -m

# 4. Check disk capacity and inode exhaustion
df -h
df -i

# 5. Check disk I/O utilization and wait times (%util, await, r/s, w/s)
iostat -xz 1 5

# 6. Check top processes by CPU and Memory
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 10
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%mem | head -n 10

# 7. Check listening ports and TCP sockets
ss -tulpn

# 8. Check kernel ring buffer for hardware faults, OOM kills, segfaults
dmesg -T | grep -iE 'oom|kill|error|segfault' | tail -n 20
```

---

## 2. Core Subsystems Breakdown (The 4 Pillars)

### Pillar 1: CPU & Scheduling

#### Key Concept: What is Load Average REALLY?
* On Linux, **Load Average** is **NOT** just CPU utilization.
* It is the average number of threads that are in:
  1. **R State (Running / Runnable):** Actively running on a core or waiting in the CPU run queue.
  2. **D State (Uninterruptible Sleep):** Usually blocked waiting for disk I/O, network filesystem (NFS), or kernel lock.
* **Golden Rule:** If `uptime` shows load average = `32` on an `8-core` machine:
  * Check CPU idle percentage in `top` or `vmstat`:
    * If `%id` is low (e.g. 0-5%), CPU is saturated by computation.
    * If `%id` is high and `%wa` (iowait) is high, the CPU is idling while threads are stuck waiting on disk or network storage!

#### Essential Commands:
```bash
# Breakdown of CPU time: %user, %sys, %idle, %iowait, %steal (virtualization steal)
mpstat -P ALL 1

# Find processes stuck in D state (uninterruptible sleep):
ps aux | awk '$8 ~ /D/'
```

---

### Pillar 2: Memory & The OOM Killer

#### Key Concept: `free` vs `available` & Page Cache
* Linux aggressively uses free RAM for **Buffers** (filesystem metadata) and **Cached** (file contents read from disk).
* **Do NOT panic if `free` shows only 100MB.** Look at **`available`**.
  * `available` = free memory + page cache memory that the kernel can immediately reclaim without swapping.
* When physical memory + swap are completely exhausted, the Linux kernel invokes the **Out-of-Memory (OOM) Killer**.
  * It calculates badness scores in `/proc/<PID>/oom_score` and sends `SIGKILL (9)` to terminate the process with the highest memory footprint.
  * Exit code will be **137** (`128 + 9 = 137`).

#### Essential Commands:
```bash
# Human readable memory
free -h

# Check if OOM Killer ran recently:
dmesg -T | grep -i oom
journalctl -k -g oom

# Inspect process memory mapping and virtual vs resident memory:
# VIRT: Virtual memory allocated (including lazy allocations)
# RES: Resident memory (actual physical RAM currently occupied)
# SHR: Shared memory
top -b -n 1 -o %MEM | head -n 20

# Check process OOM score:
cat /proc/<PID>/oom_score
```

---

### Pillar 3: Storage, Disk I/O & Inodes

#### Key Concept: `df -h` vs `du -sh` Discrepancy
* **Interview Classic:** *"Why does `df -h` say root disk is 100% full, but `du -sh /*` only adds up to 30GB?"*
* **Root Cause:** A process (e.g. Nginx, Node.js, PM2) is holding an open file descriptor to a deleted log file.
  * When you run `rm app.log`, the filename is unlinked from the directory entry.
  * However, the inode and disk data blocks are **not freed** until the process holding the file descriptor closes it or the process terminates.

#### Essential Commands:
```bash
# Find deleted files still held open by running processes:
lsof +L1
# or
lsof | grep -i deleted

# Inspect disk utilization and queue wait times:
# Look for %util close to 100% or await > 20ms
iostat -xz 1 3

# Check inode exhaustion (disk can have free gigabytes but 0 free inodes!):
df -i

# Safely truncate an open log file without breaking the process handle:
> /path/to/busy_app.log
# (Never use 'rm' on an active log file held by a daemon!)
```

---

### Pillar 4: Networking & TCP Sockets

#### Key Concept: TCP Connection Lifecycles & Exhaustion
* **TIME_WAIT:** Normal state after a socket is actively closed by the host. Sockets stay in `TIME_WAIT` for $2 \times \text{MSL}$ (typically 60 seconds) to ensure delayed packets don't corrupt a new connection.
  * Excessive `TIME_WAIT` sockets can exhaust ephemeral port ranges (`/proc/sys/net/ipv4/ip_local_port_range`).
* **CLOSE_WAIT:** The remote side closed the connection, but the local application has **not** closed its socket.
  * If you see thousands of `CLOSE_WAIT` sockets, this is an **application bug** (leaked socket handle / missing `.close()`).

#### Essential Commands:
```bash
# Socket summary (counts of ESTAB, TIME_WAIT, CLOSE_WAIT):
ss -s

# All listening TCP ports with process name and PID:
ss -tulpn

# Count connections per state:
ss -ant | awk '{print $1}' | sort | uniq -c | sort -nr

# Live network packet capture (DNS and HTTP):
tcpdump -nn -i any port 53 or port 80 -c 20

# Trace DNS resolution step-by-step:
dig +trace example.com
```

---

## 3. Linux Signals Reference (SysDE Must-Know)

| Signal | Number | Name | Can be Caught/Blocked? | SysDE Context |
|---|---|---|---|---|
| 1 | `SIGHUP` | Hangup | Yes | Reload config files without restarting daemon (e.g., `kill -HUP <nginx_pid>`). |
| 2 | `SIGINT` | Interrupt | Yes | Sent by terminal on `Ctrl+C`. Graceful termination request. |
| 9 | `SIGKILL` | Kill | **NO** | Immediately terminated by the kernel. Cannot be intercepted, logged, or cleaned up. |
| 15 | `SIGTERM` | Terminate | Yes | Default `kill <pid>`. Clean shutdown signal; gives process time to finish in-flight requests. |
| 17 | `SIGCHLD` | Child status | Yes | Sent to parent when child terminates. If parent ignores, child becomes a **Zombie (`Z`)**. |

### Understanding Exit Codes:
* If a process exits with code $> 128$, it was killed by a signal:
  $$\text{Exit Code} = 128 + \text{Signal Number}$$
  * `137` = $128 + 9$ (Killed by `SIGKILL` / OOM Killer).
  * `143` = $128 + 15$ (Killed by `SIGTERM` / graceful timeout).

---

## 4. The Magic of `/proc` (Kernel Interface)

In Linux, everything is a file. `/proc` is a virtual filesystem reflecting live kernel state:

| Path | What it Reveals |
|---|---|
| `/proc/loadavg` | Current 1m, 5m, 15m load average + runnable/total threads + last PID. |
| `/proc/meminfo` | Detailed kernel memory stats (`MemTotal`, `MemAvailable`, `Dirty`, `SwapTotal`). |
| `/proc/cpuinfo` | Physical & logical core counts, model, flags, cache sizes. |
| `/proc/net/dev` | Network interface byte and packet counters (check for drops and FIFO errors). |
| `/proc/<PID>/cmdline` | Exact command line used to launch process `<PID>`. |
| `/proc/<PID>/fd/` | List of all open file descriptors for that process (`ls -la /proc/<PID>/fd`). |
| `/proc/<PID>/status` | Memory usage (`VmRSS`, `VmSize`), thread count, state (`R`, `S`, `D`, `Z`). |
| `/proc/<PID>/net/tcp` | Network sockets open specifically by that process namespace. |
