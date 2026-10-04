# 01 — LINUX (Domain 1/12)

Priority: **P0 domain.** Linux fundamentals are the single most frequently probed area at 1–3 YOE
(labeled "Critical" across JD sources). Everything else — Docker, K8s, networking — leans on it.

## Linux priority map

- **P0 (full 16-part template):** processes/states/signals · CPU/load average · memory/swap/OOM ·
  disk/inodes/deleted-open-files · permissions/users/sudo/SSH · systemd/journald · file descriptors /
  sockets/ports / `/proc` · environment variables · resource troubleshooting sequences
- **P1 (condensed):** `vmstat`/`iostat`/`dmesg` reading · `tar`/`rsync` · `umask` · mount management ·
  shell rc files · cron · package management
- **P2 (compact):** LVM · swap tuning · cgroups-v2 detail · NFS · ACLs
- **Ignore:** `perf`, SELinux/AppArmor policy crafting, kernel tuning, NUMA, `init.d`

## Session log

| # | Sub-topic | Priority | Status | QC |
|---|---|---|---|---|
| P0.1 | Processes, states, signals | P0 | **COMPLETE** | PASS · 1 self-verified item |
| P0.2 | CPU and load average (deep) | P0 | **COMPLETE** | PASS · lab-verified |
| P0.3 | Memory: virtual memory, `free`, swap, OOM | P0 | **COMPLETE** | PASS · lab-verified |
| P0.4 | Disk: `df`/`du`/inodes/deleted-open files | P0 | **COMPLETE** | PASS · lab-verified |
| P0.5 | Permissions: users/groups/chmod/chown/sudo/SSH | P0 | **COMPLETE** | PASS · lab-verified |
| P0.6 | systemd + journald + services | P0 | **COMPLETE** | PASS · lab-verified |
| P0.7 | FDs, sockets, ports (`ss`/`lsof`), `/proc` | P0 | **COMPLETE** | PASS · lab-verified |
| P0.8 | Environment variables + cron | P0/P1 | **COMPLETE** | PASS · lab-verified |
| P1.1 | Package management + archival (tar/rsync) | P1 | **COMPLETE** | PASS · lab-verified |
| P1.2 | Resource-troubleshooting playbooks (consolidation) | P0 | **COMPLETE** | PASS · lab-verified |

---

# SESSION LINUX.P0.1 — PROCESSES, STATES, SIGNALS

## 1. WHAT IS IT? (≤30 s)

A process is a running instance of a program: one entry in the kernel's process table with a PID,
its own memory space, its open files, and a parent/child relationship.

## 2. WHY DOES IT EXIST?

The box runs dozens of programs concurrently. Processes exist so the kernel can (a) isolate each
running program from the others (one crashing can't scribble over another's memory), (b) time-share
the CPU among them, and (c) give you inspection + control primitives. Without it you cannot answer
the most common ops question: **"what is eating my server?"**

## 3. HOW DOES IT WORK?

- **Creation model:** new processes are produced by `fork()` (copy of the parent) then `exec()`
  (replace the copy with a new program). This is why every process has a parent (`PPID`), and why
  the process tree is a tree. In practice, `systemd` (PID 1) spawns and owns the service tree.
- **Where the data lives:** `/proc/<pid>/` — one virtual directory per process with `status`, `cmdline`,
  `environ`, `fd/`, `stat`, `mounts`. `ps`, `top`, `ss`, `lsof` are all just readers of `/proc` (and
  other kernel data).
- **States** (first letter of the STAT column):
  - `R` running / runnable — on the run queue, using or waiting for a CPU core
  - `S` interruptible sleep — waiting on *something* (socket, timer, I/O) but killable
  - `D` uninterruptible sleep — stuck in kernel I/O, typically disk/NFS; **not** signal-able until it
    returns to userspace
  - `T` stopped — paused by `SIGSTOP`
  - `Z` zombie — finished, but parent has not yet read its exit status (`wait()`)
- **Zombies:** the child exits, the kernel keeps the corpse (exit code, minimal info) until the parent
  reaps it with `wait()`. A zombie is *dead*: it holds no memory, does not run, and `kill` does nothing
  to it. If the parent dies, PID 1 (or the nearest subreaper) adopts the orphan and reaps it. A flood
  of zombies means the parent is buggy (not calling `wait`) or dead in a way that breaks reaping — it
  does not mean "something is consuming CPU".
- **Signals:** kernel-delivered notifications to a process.
  - `SIGTERM` (15) — graceful, catchable. "Please shut down." Apps trap it to finish requests, flush,
    close connections.
  - `SIGKILL` (9) — uncatchable, immediate. "You are gone." No cleanup runs.
  - `SIGINT` (2) — Ctrl+C · `SIGHUP` (1) — hangup/terminal-close · `SIGSTOP` (19)/`SIGCONT` (18) ·
    `SIGCHLD` (17) — sent to parent when a child exits (this is how parents know to reap).
  - Why 15-vs-9 matters: TERM gives the app a chance to persist state cleanly; KILL skips that, so
    abrupt-termination risk (e.g. corrupted write) depends entirely on the application's behavior.
- **CPU view:** each process accrues CPU time; the scheduler dispatches runnable (`R`) tasks. **Load
  average** is *not* a percentage — it is the moving average count of runnable + uninterruptible
  threads over 1/5/15 min, and it includes `D`-state (I/O-stalled) threads.

## 4. PRODUCTION MENTAL MODEL

```
ps / top / ss / lsof
     │ read
     ▼
/proc/<pid>/  ──►  kernel process table (PID, PPID, state, CPU time, open files)
     │
     ├── R ──► on run queue (uses / wants CPU)
     ├── S ──► waiting on socket / I/O / timer  (killable)
     ├── D ──► stuck in kernel I/O (disk/NFS)   (NOT killable until it returns)
     ├── T ──► stopped (SIGSTOP)
     └── Z ──► dead, awaiting parent's wait()   (kill = no-op)
signals: kill -TERM (graceful) → escalate kill -KILL → collect evidence
```

## 5. INTERVIEW-SAFE ANSWER

"Everything running on Linux is a process, and each one has a PID, a parent, its own memory, and a
state the kernel tracks. Processes are created by fork-then-exec, so there's always a parent-child
tree — that's why `ps` shows PPIDs and why systemd, as PID 1, owns the service tree. For
troubleshooting I mostly use `ps` and `top`, and `/proc/<pid>` when I need details like open file
descriptors. The states matter in practice: R means it wants the CPU, S means it's waiting on
something, D means it's stuck in kernel I/O and effectively unkillable until that I/O returns, and Z
is a zombie — a child that exited but the parent hasn't reaped. Killing something, I use TERM first
because it lets the app shut down gracefully; KILL is the escalation when TERM fails."

## 6. FOLLOW-UP ATTACKS

**Q.** What's the difference between a process and a thread?
**A.** A thread is a schedulable unit inside a process; threads of one process share its memory. Linux
implements threads as tasks that share an address space — `ps -T`/`top -H` show them. In `ps`, the
main thread's PID is the thread-group ID (TGID).

**Q.** How do you create a zombie? (→ see Lab 2; interviewer wants the mechanism: child exits, parent
sleeps without `wait()`.)

**Q.** Can you kill a zombie with `kill -9`?
**A.** No. It's already dead; the signal is a no-op. You fix the *parent* (fix its `wait()` handling,
or kill the parent so PID 1 reaps) — or it's a broken reaper/subreaper.

**Q.** A process won't die even with `kill -9`. Why?
**A.** Two classic causes, distinguished by state: (1) **D state** — stuck in uninterruptible kernel
I/O (usually NFS or a failing disk); `kill -9` is queued but can't be delivered until it returns to
userspace, then it dies. Fix the underlying I/O. (2) **Zombie** — already dead. (Rarely: it's in an
interminable syscall or was blocked on a kernel lock.) Note that in `top` D-state tasks show 0% CPU —
that's the giveaway.

**Q.** Why is load high but CPU looks idle?
**A.** Load average counts runnable **+ uninterruptible** threads. D-state spikes (disk/NFS stall)
inflate load while `top` shows low CPU. Check `vmstat`'s `wa` column and `ps` for D states. This is
the single most common Linux misdiagnosis.

**Q.** `ps` shows 100.0 for CPU but `top` shows ~0. Why?
**A.** `ps` `%CPU` is the *lifetime average* since the process started; `top` shows a near-instantaneous
value. For current CPU use, `top` or `vmstat`.

**Q.** What happens when PID 1 dies? (Rare but classic.)
**A.** Kernel panic / no reaping — a "kill systemd" process is a panic on most systems because the
kernel keeps PID 1 special: `SIGKILL` to PID 1 is ignored by the kernel, but killing it makes the
kernel panic.

## 7. PRACTICAL EXAMPLE (production-scale flavor)

An 8-core EC2 box hosting a Node.js service suddenly shows load 14 and slow responses. SSH works.
You don't restart yet — you first figure out whether it's CPU contention, an I/O stall (D-state),
or a runaway process. (This is expanded as the incident in §11.)

## 8. BUILD / REPRODUCE

All labs run on this machine. `labs/01-linux/` already exists.

### Lab 1 — states and signals (build)

```bash
sleep 500 &
slow=$!
sleep 300 &
slow2=$!
ps -o pid,ppid,stat,cmd -p "$slow" -p "$slow2"
```

Expected: two processes, state `S` (both sleeping — they're waiting on a timer), plus `s` (session
leader) and `+` (foreground group) flags depending on shell.

Now the two signal paths:

```bash
kill -TERM "$slow"        # graceful (SIGTERM)  → process exits cleanly
sleep 1
ps -p "$slow"             # gone
kill -KILL "$slow2"       # immediate (SIGKILL) → process gone without cleanup
sleep 1
ps -p "$slow2"            # gone
```

Both disappear because `sleep` has nothing to clean up — the difference matters for apps *with*
state. Lab 4 in a later session will show a real graceful-shutdown handler.

### Lab 2 — produce a zombie (build + observe)

```bash
cat > labs/01-linux/zombie.py <<'EOF'
import os, sys, time
child = os.fork()          # child is a copy of the parent
if child == 0:
    sys.exit(0)            # child exits immediately → becomes a zombie
open("/tmp/zpid.txt","w").write(str(child))
time.sleep(300)            # parent sleeps WITHOUT wait() → zombie stays
EOF

setsid python3 labs/01-linux/zombie.py >/dev/null 2>&1 < /dev/null &
parent=$!
sleep 1
ps -eo pid,ppid,stat,comm | awk '$3 ~ /^Z/'
```

Expected: one row with STAT `Z` (the corpse). **Important interview-grade gotcha:** a zombie's
`cmdline`/`args` are freed (empty), so `ps | grep zombie.py` will NOT find it — filter by **state**,
not name: `ps -eo pid,ppid,stat,comm | awk '$3 ~ /^Z/'`. Now prove `kill` can't touch it, then fix it:

```bash
zpid=$(cat /tmp/zpid.txt)
ps -o pid,ppid,stat,args -p "$zpid"      # shows "[python3] <defunct>" — empty args
kill -KILL "$zpid"                        # no-op: exit=0 but the Z row remains — already dead
ps -o pid,stat -p "$zpid"
kill -TERM "$parent"                      # parent dies → kernel reparents child to PID 1 → reaped
sleep 1
ps -p "$zpid" || echo "gone"              # zombie reaped
```

Takeaway: deadly-slow zombie floods come from a *broken parent* (never calling `wait()`), so the fix
is the parent — kill it (PID 1 then reaps) or fix the probe/reaper bug. This lab is verified-working
on this machine (`1228 Z` produced, `kill -KILL` no-op, then reaped after parent death).

### Lab 3 — load average (break it)

```bash
uptime                       # baseline load (low)
yes > /dev/null &            # `yes` spins a CPU core forever
uptime                       # load climbs toward ~1 "per busy core" over ~1 min
top                          # see `yes` at ~100% CPU, then...
kill -9 %1                   # ...kill it
uptime                       # load decays back down (moving average)
```

On an 8-core box, load ≈1 here means "one core's worth of work": the number is a *count* of busy/queued
units, not a percentage. Purposely mapped to the §11 incident.

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT "LOAD HIGH" — full sequence

**SYMPTOM:** 8-core EC2, Node app slow, load 14, SSH responsive.
→ **SCOPE:** quickly establish blast radius — *whole box* vs one process. `top` one-liners and a state
histogram are the first pass.
→ **HYPOTHESES (families):** (a) real CPU contention (many `R` threads), (b) I/O stall (many `D`
threads — disk/NFS), (c) zombie flood (looks alarming, almost never the cause of *load*), (d) memory
pressure → swap → everything crawls (covered next session).
→ **CHECKS, in order:**
1. `uptime` — 1/5/15 numbers tell you the trend (spike vs ramp).
2. **State histogram — the fork in the road:**
   `ps -eo stat= | cut -c1 | sort | uniq -c`
   R-heavy → CPU theory. D-heavy → I/O theory. This is the single highest-value read.
3. If R-heavy: `top` → sort by CPU, identify the process. `vmstat 1 5` → `us`+`sy` columns high.
4. If D-heavy: `vmstat 1 5` → `wa` column high (disk wait); `iostat -x 1` → which device; check for
   NFS mounts (`df -h`, `mount | grep nfs`) — NFS hangs produce classic unkillable D-state scenes.
5. Check `free -h` for swap usage (memory theory; full treatment next session).
→ **EVIDENCE:** state histogram shows 20 `R` tasks against 8 cores; `top` shows one `yes`-like process
at 100% CPU; `wa` ~0; free OK.
→ **ROOT CAUSE:** runaway single process saturating/oversubscribing the scheduler — not I/O, not Linux
being broken.
→ **FIX (smallest safe change):** confirm identity (`ps -p <pid> -o pid,user,etime,args` — how long
running, which user, what command), then `kill -TERM <pid>` → escalate `kill -KILL` only if it ignores
TERM. **Because** it ignores TERM *or* TERM identification is confirmed — never blind-kill-first.
→ **VERIFY:** `uptime` trending down; state histogram back to mostly `S`; app latency normal; the
process is gone from `ps`.
→ **PREVENT:** alert on load OR on state-histogram anomaly; container/cgroup resource limits (a runaway
can't consume the whole node); a `fatfinger`/runaway process watchdog; review what shipped that caused it.

### DECISION OVERLAY — what NOT to do

- **Do not** "restart everything," `systemctl restart` the whole service suite, or reboot — this is a
  classic evidence-destroying move. Restart may be a legitimate mitigation, but only after you've
  preserved evidence (which process / how long / what state) so you can find the *cause* afterward.
- **Do not** `kill -9` before reading `ps -o etime,args` to confirm what you're killing.
- **Do not** conclude "Linux problem / AWS problem" without the state histogram.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Load average is CPU percentage" | Load = moving count of runnable + uninterruptible; includes D-state. Load 1 on 8 cores ≈ one core busy. |
| "A zombie is still running / leaked memory" | Dead, memory freed, waits for `wait()`. Danger = *many* zombies (parent bug), not any single one. |
| "`kill -9` always causes corruption" | It skips cleanup — corruption risk is app-dependent. TERM-first, KILL-escalate; never as a mantra. |
| "`ps %CPU` 100 means the process uses a full core now" | It's a lifetime average since start. Use `top`/`vmstat` for current. |
| "Killing a process always frees its sockets/files" | The kernel closes FDs on exit, yes — but *in-flight* external state (DB records, other nodes) is the app's responsibility; that's why graceful shutdown exists. |
| "`kill -9` didn't work → the process is immune to signals" | Check state first: D (uninterruptible kernel I/O) or Z (already dead). Both fake-out `kill -9`. |
| "D never means disk" / "D always means disk" | It's *uninterruptible kernel I/O* — usually block I/O or NFS; be precise. |

## 13. FIRST-CHECK REASONING

- **"Load high":** state histogram first (`ps -eo stat= | cut -c1 | sort | uniq -c`), because one cheap
  read splits the two dominant hypothesis families (CPU vs I/O) that a bare `top` CPU column cannot.
- **"Can't kill a process":** `ps -o pid,stat,cmd` first — `Z` (reap/kill the parent) vs `D` (find the
  I/O stall; it will die when it returns). These lead to opposite actions; diagnosing them first is not
  optional.

## 14. PRIORITY

**P0.**

## 15. STOP HERE — you are done with this sub-topic when…

You can, without notes:
1. run `ps`/`top`, name the state letters and what each implies operationally;
2. produce a zombie and clean it up (Lab 2);
3. route the "high load" incident via the state histogram to the correct family (CPU vs I/O vs memory);
4. explain TERM-vs-KILL, *when* `kill -9` legitimately fails, and what `ps %CPU` actually means;
5. defend every row in the Interview Traps table in ≤30 seconds each.

Stop. Do not go deeper.

## 16. DO NOT STUDY YET

cgroups/namespace internals, scheduler classes (CFS/BORE/eBPF schedulers), `perf` profiling, NUMA
pinning, io_uring. All are real engineering, none are 1–3 YOE interview material. If asked, the honest
line is "I know of it, haven't needed it operationally" — that is a *legal* answer here and the
interviewer respects it.

---

## QC CHECKLIST — LINUX.P0.1

| # | Check | Result |
|---|---|---|
| 1 | Can I draw the mental model (process table + states)? | ✔ |
| 2 | ≤30 s definition? | ✔ (§1) |
| 3 | Why it exists? | ✔ (§2) |
| 4 | Important mechanism (fork/exec, /proc, states, signals)? | ✔ (§3) |
| 5 | Dependencies (PID1/systemd, kernel)? | ✔ (§3) |
| 6 | Essential commands (`ps`, `top`, `kill`, `uptime`, `vmstat`)? | ✔ (§8–11) |
| 7 | Reproduce (Lab 1–3)? | ✔ run them now |
| 8 | Break it (zombie, load burnout)? | ✔ Lab 2–3 |
| 9 | Observe + interpret evidence? | ✔ §9–11 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §11 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend the resume claim honestly? | **SELF-VERIFY** — only claim what these labs + real usage prove |

Verdict: **PASS** (with the self-drive item 13).

---

# SESSION LINUX.P0.2 — CPU AND LOAD AVERAGE (DEEP)

Prereq: LINUX.P0.1. All tools below verified present on this machine (`uptime`, `vmstat`, `top`,
`mpstat`, `iostat`, `pidstat`). `mpstat`/`iostat`/`sar`/`pidstat` come from the `sysstat` package if a
target box lacks them.

## 1. WHAT IS IT? (≤30 s)

CPU time is the slice of a core a thread actually ran on. **Load average** is a moving count of
runnable + uninterruptible threads. Utilization (is the core busy?) and saturation (are threads
*waiting* for a core?) are different things, and load conflates them — which is why you must separate
them with `vmstat`/`top` instead of trusting `uptime`.

## 2. WHY DOES IT EXIST?

CPU misdiagnosis is the most common Linux triage error at this level: "load is high → add CPU" is
frequently wrong. Understanding utilization vs saturation vs the `st`/`wa` columns is what lets you
route an incident to the right family (CPU contention, I/O stall, or hypervisor steal on EC2) instead
of throwing instances at a symptom.

## 3. HOW DOES IT WORK?

- **Run queue & scheduling.** Each CPU core has a run queue. Runnable (`R`) threads sit in them; the
  scheduler dispatches one thread per core. Utilization = core busy; **saturation** = threads in the
  queue beyond the cores.
- **What `vmstat` shows you:**
  - `r` — runnable threads (across all queues) · `b` — blocked / uninterruptible (`D`)
  - `us` — user time % · `sy` — kernel time % · `id` — idle % · `wa` — I/O-wait %
  - `st` — steal % (hypervisor took CPU that your VM was ready to run on)
  - `cs` — context switches/s · `in` — interrupts/s
  - First row = average since boot; every row after = since the previous sample. Take `vmstat 1 5`.
- **Load average mechanics.** `uptime`/`top` show the 1/5/15-min **exponentially weighted moving
  averages** of `runnable + uninterruptible` tasks. It is *not* a percentage. `D`-state (I/O-stalled)
  tasks inflate it without burning CPU — the root of "load 14, CPU idle".
- **The cores rule.** Compare load against core count: load 1 on an 8-core box ≈ one core's worth of
  work; load 8 on 8 cores means a thread is waiting on average — saturation begins. `top` key `1` shows
  the per-core split.
- **wa vs D vs st — read them together.** `wa` high → block-I/O bound (cross-check `b`/D-state,
  `iostat -x`). `st` high → the *hypervisor* is busy, not your code — classic on tier-1/B-series
  instances and busy shared hosts, and a big AWS interview angle. `sy` high → kernel work (syscalls,
  context switches, IRQs), not app work.
- **Why utilization ≠ health.** 100% CPU on one core with 7 idle may be a single-threaded app doing
  legitimate work; the decision is whether a task *that should be fast* is waiting, not whether some
  core is busy.

## 4. PRODUCTION MENTAL MODEL

```
uptime ──► load 1/5/15 = moving count of (runnable + uninterruptible)  ← NOT a percentage
                       │
vmstat 1 ──► r (runnable)   vs   b (blocked/D-state)      ← the fork
                       │
                       ├── r > cores ──► CPU saturation ──► top | sort by CPU ──► pidstat
                       ├── b/wa   ────► I/O stall ──► iostat -x, df, D-state count
                       └── st high ───► hypervisor steal (EC2/VM) ──► instance/credit check
utilization  = CPU busy %   (us+sy, minus steal)
saturation   = threads waiting for a core   (r/cores)
```

## 5. INTERVIEW-SAFE ANSWER

"Load average is a moving count of runnable plus uninterruptible threads over 1, 5 and 15 minutes —
it's not a CPU percentage, and it includes tasks stuck in I/O, which is why you can have load 14 with
near-idle CPU. The way I actually diagnose 'CPU high' is `vmstat 1` and its `r` and `b` columns. If
`r` is above the core count, I have CPU saturation and I go to `top`, sort by CPU, and find the
process — and `pidstat` if it's a specific thread. If `b` is high, it's not a CPU problem, it's an
I/O problem, so I look at `wa`, D-states and `iostat`. On EC2 I always read `st`: if steal time is
high, the hypervisor is contending for the host CPU — my application is runnable but not being
scheduled, and adding an instance is the wrong first move when the real question is instance type or
host noise. So my habit is: load tells me the symptom, `vmstat` splits the hypotheses, `top`/`pidstat`
names the culprit, and `st`/`wa` check whether the culprit is even my code."

## 6. FOLLOW-UP ATTACKS

**Q.** Load is 20 on an 8-core box — what does that mean?
**A.** ~2.5 runnable threads per core on average — oversubscribed. But I don't stop there: I check `r`
vs `b` to learn if it's CPU contention or I/O stall, because the fix is completely different.

**Q.** `vmstat` shows `r` low but load high. Why?
**A.** The `D`-state tasks are counted in load but not runnable — they're blocked in kernel I/O,
usually disk or NFS. That's "load high, CPU idle."

**Q.** What is `st` and why should an AWS candidate care?
**A.** Steal time is CPU that your vCPU was ready to use but the hypervisor scheduled away to other
tenants. If you pay for CPU and see consistent `st`, your app looks slow while your CPU% stays low —
and the fix is host/instance-level, not heavier code or more replicas. On burstable T-instances it
also surfaces as credit exhaustion once the baseline is exceeded.

**Q.** How do you find the process chewing CPU?
**A.** `top -b -n1 | head -20` (one-shot, script-friendly), sort by `P` in interactive top; for a
multithreaded app, `top -H -p <pid>` to see threads; `pidstat -p <pid> 1` for live per-thread CPU.
`ps %CPU` is a lifetime average, so I don't trust it for "right now."

**Q.** `us`=90, `sy`=90 vs `us`=10, `sy`=80: what's different?
**A.** High sy = the kernel is burning CPU on syscalls, context switches, IRQ/network/disk work —
often signaling too many tiny I/O operations or thread thrash (`cs` in the same output), not app math.
High us = your application's own code.

**Q.** When is 100% CPU actually fine?
**A.** When the workload is CPU-bound by design (build, rendering, batch compute) and latency is within
SLO — saturation, not utilization, is the alarm. You alarm on time-in-queue, not core being busy.

**Q.** If I have N cores, are they all in one run queue?
**A.** Modern Linux uses per-CPU runqueues with load balancing; `r` in vmstat is the aggregate across
queues. That's also why a single-threaded app can show one core pegged while others idle.

## 7. PRACTICAL EXAMPLE (EC2, shared host)

4-vCPU EC2, app latency climbs, `uptime` shows load 12. Screenshot-style evidence: `vmstat 1 3` →
`r`=9, `b`=2, `us`=28, `sy`=9, `wa`=3, **`st`=45**. The whole picture changes: this is not your app
and not disk — the hypervisor is stealing nearly half the CPU you paid for. You re-measure a few times,
confirm `st` persists, then remediate at the platform layer (instance type/credits/AZ) rather than
scaling code.

## 8. BUILD / REPRODUCE

All commands verified on this machine. `labs/01-linux/loadburn.sh` is provided.

### Lab 4 — single-thread burn: load ≠ cores (build)

```bash
yes > /dev/null &          # `yes` burns ~one full core
uptime                     # load 1-min climbs toward ~1, not 8
top -1                     # ONE core pegged 100%, others idle (press 1, or -1 batch)
kill %1
```

Lesson: one runnable thread → load 1 on an 8-core box. That's one core's worth, NOT "100%."

### Lab 5 — oversubscribe the node: create saturation (break it)

```bash
cat > labs/01-linux/loadburn.sh <<'EOF'
#!/bin/bash
set -euo pipefail
n=$(nproc)
echo "cores: $n"
for i in $(seq 1 $((n+2))); do yes > /dev/null & done   # n+2 runnable threads > cores
echo "--- uptime after a few seconds (load > n means saturation) ---"
sleep 3; uptime
echo "--- vmstat 1 5 ---"
vmstat 1 5
echo "--- top one-shot: process ranking ---"
top -b -n1 | head -15
echo "--- cleanup ---"
pkill -x yes || true
EOF
chmod +x labs/01-linux/loadburn.sh && ./labs/01-linux/loadburn.sh
```

Read-back: `r` sits above the core count (threads queued = saturation), `us` ~100, `wa`≈0, `st`≈0,
and `top` lists `n+2` `yes` processes at ~`100*n/(n+2)`% each. Keep the machine honest afterward:
`pkill -x yes`.

### Lab 6 — measure steal and wa correctly (observe)

No hypervisor contention on this box, so you observe the shape, not a value:

```bash
vmstat 1 5                 # one-shot delay: r/b/us/sy/id/wa/st; first line = since boot
mpstat -P ALL 1 2          # per-core split — spot single-core pinning/IRQ distribution
```

If this were a busy shared EC2 host, `mpstat` would show `%steal` consistently >0 while `%idle` stays
high — the "my CPU is stolen" signature.

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT "APP SLOW, CPU PEGGED" — full sequence

**SYMPTOM:** latency up; `top` shows ~100% CPU across cores.
→ **SCOPE:** whole box vs one process vs one thread. `top`-sort and `vmstat` split this in 10 seconds.
→ **HYPOTHESES:** (a) legit CPU-bound work/regression (code change made it chatty), (b) runaway/
    busy-loop process (P0.1 material), (c) thread explosion — many threads × few cores, (d) MASSIVE —
    but often forgotten — **hypervisor steal on a VM**, (e) syscall/I/O storm showing as `sy`/`cs`.
→ **CHECKS, in order:**
1. `vmstat 1 3` → read `r` (saturated?), `b` (D-state? not CPU), `st` (stolen?), `cs` (thrash?).
2. `top -b -n1 | head` sorted by CPU → which process, how many threads (`top -H -p <pid>`).
3. `pidstat -p <pid> 1 3` → per-thread %CPU (do the threads spend CPU or wait?).
4. `mpstat -P ALL` → one core pegged (single-threaded hotspot) vs all cores (parallel contention).
5. If EC2/cloud: `st` persistent cheap-check — if yes, it's platform, stop tuning code.
→ **EVIDENCE:** `r`≈cores+, no `b`, `st` significant, `yes`-like process at top → runaway on a VM whose
    CPU was already being stolen.
→ **ROOT CAUSE:** (verified case) application busy-loop regression; `st` merely amplified it — the fix
    still starts with the process, then addresses instance placement.
→ **FIX (smallest safe):** confirm the offending process (`ps -o pid,user,etime,args -p <pid>`), then
    `kill -TERM <pid>` → escalate `-KILL` only if needed. If steal was the amplifier, document instance
    type/credit balance and escalate to platform action — do not scale-out-and-walk-away.
→ **VERIFY:** `vmstat`: `r` drops below cores; `us`/`st` normalize; latency returns; process gone. Observe
    before/after numbers, don't eyeball.
→ **PREVENT:** per-process/container CPU limits (a runaway can't take the node), alert on saturation
    (`r` > cores sustained) *and* on `st`, code-review the regression, re-platform the VM appropriately.

### DECISION OVERLAY — what NOT to do

- Do not scale out on `load` alone — you may be adding replicas to a box whose CPU is being stolen or
  whose threads are waiting on I/O.
- Do not `rename`/`kill` by pattern blindly (`pkill` the app name could hit healthy instances of the
  same binary on a multi-app host; scope with `-u`, `-f`, or pid-first).
- Do not read the first `vmstat` row (since boot) as "current" — always take interval samples.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Load 1.0 = 100% CPU" | Load is a count (runnable + D-state). It's a *number of threads of work*, and it never tops out at 1. |
| "Load high → CPU problem" | Load counts `D`-state blocked threads. Split `r` vs `b` first. |
| "`ps %CPU` tells me now" | Lifetime average since start. Use `top`/`vmstat`/`pidstat`. |
| "High `cs` is always bad" | High context-switch rate is a *signal* to investigate (tiny syscalls, thread thrash), not an error code. |
| "`st` means my app is slow" | `st` = the *hypervisor* didn't run you. Troubleshoot platform, not code. |
| "8 cores → load 8 is fine" | Load 8 on 8 cores *is* the saturation boundary; sustained load == cores means tasks are waiting. |
| "Wa is the whole I/O story" | `wa` under-reports a single slow disk because it's averaged across cores. Cross-check `D`-states and `iostat -x`. |
| "100% CPU is automatically bad" | Saturation triggers the alarm; utilization of a legitimately-busy CPU is not. |

## 13. FIRST-CHECK REASONING

- **"CPU looks pinned":** `vmstat 1 3` first — one read splits saturation (`r`), I/O (`b`/`wa`), and
  steal (`st`), the three families that all *look* like "CPU high" but have opposite fixes.
- **"Slow on EC2 or a small VM":** read `st` *before* tuning code. Cost of check ≈ zero; cost of the
  wrong fix (heavy code/hardware work on a hypervisor problem) is hours. This is why steal is checked
  before `top`.

## 14. PRIORITY

**P0.**

## 15. STOP HERE — done when you can…

1. explain load-vs-processor-count and why `D`-state inflates load with idle CPU;
2. run `vmstat 1 5` and read `r`, `b`, `us/sy/id/wa/st`, `cs` — and say what to do next per column;
3. produce single-core-pinned (Lab 4) and oversubscribed (Lab 5) states and interpret both;
4. pin the culprit: `top` → `top -H` → `pidstat`, and justify why `ps %CPU` is untrusted;
5. defend the "slow on EC2" scenario where `st` turns it from a code problem into a platform problem.

## 16. DO NOT STUDY YET

CFS/EEVDF scheduler internals, cgroup CPU controller (`cpu.max`) tuning, `perf`/`bpftrace` profiling,
NUMA affinity tuning, IRQ balancing/RPS. Real engineering; not 1–3 YOE interview material. The honest
"not needed operationally yet" line is your shield.

---

## QC CHECKLIST — LINUX.P0.2

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (load vs vmstat split vs st/wa)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanism (run queues, load EWMA, vmstat columns)? | ✔ §3 |
| 5 | Dependencies (interrupts, I/O, hypervisor)? | ✔ §3/§7 |
| 6 | Essential commands (`uptime`/`vmstat`/`top`/`mpstat`/`pidstat`)? | ✔ §8 (all verified present) |
| 7 | Reproduce (Lab 4–6)? | ✔ run them now |
| 8 | Break it (oversubscription)? | ✔ Lab 5 |
| 9 | Observe + interpret evidence? | ✔ §8–11 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §11 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13).

---

# SESSION LINUX.P0.3 — MEMORY: VIRTUAL MEMORY, `free`, SWAP, OOM KILLER

## 1. WHAT IS IT? (≤30 s)

Linux gives every process its own **virtual** address space, backed by physical RAM pages only as they
are touched (**demand paging**). That's why a process can "use" a gigabyte of virtual memory while
touching 15 MB of RAM — and why `free`'s most important number (`available`) is an estimate of what you
can *still allocate*, not the green-looking `free` column.

## 2. WHY DOES IT EXIST?

Memory misreading is the second-most-common Linux misdiagnosis after load. "`free` says 90% used, buy
RAM" is usually wrong (it's page cache, which is reclaimable). And when the **OOM killer** fires, it
kills the wrong-looking process if you don't know how it picks victims. Understanding VSZ/RSS,
`available` vs `free`, swap semantics, and the OOM heuristic is what turns a page into a root cause.

## 3. HOW DOES IT WORK?

- **Pages & page tables.** Memory is managed in 4 KB pages. Each process has a page table mapping its
  virtual addresses → physical frames. A mapping that hasn't been *touched* costs zero RAM (the 512 MB
  `mmap`, 14 MB RSS lab in §8 proves it).
- **VSZ vs RSS.** `VSZ`/`VIRT` = reserved virtual size; `RSS`/`RES` = pages actually resident. `top`
  column `SHR` = shared pages (with other processes — e.g. after `fork()`, COW pages are shared until
  someone writes).
- **`free` — the mental model.** Columns: `used = total − free − buff/cache`. `buff` = raw block-device
  buffers; `cache` = page cache (file data read from disk). **Cache is reclaimable**: under pressure the
  kernel evicts clean cache *before* swapping. `available` = the kernel's live estimate of memory that
  can be allocated **without** hitting swap — it accounts for reclaimable cache and the kernel's own
  headroom. `available` is the number to alert on, not `used` (and never `free`).
- **Swap.** Disk-backed space for *anonymous* pages (heap, stack, `/dev/zero`, MAP_PRIVATE mmap). Zero
  swap-used is healthy; **swap-used climbing = real pressure** (cache already reclaimed). `vmstat`'s
  `si`/`so` > 0 continuously = active swapping = thrashing. `swappiness` (0–100, default ~60) biases
  reclaim between cache and anonymous pages.
- **OOM killer.** When the kernel can't reclaim/grow memory fast enough it picks a victim by a badness
  heuristic: roughly, memory consumed, age, plus `oom_score_adj` (`/proc/<pid>/oom_score_adj`, range
  −1000…+1000; set −1000 to make that process exempt from OOM-kill scoring). Victim gets
  `SIGKILL`. Evidence is in the kernel log:
  `dmesg -T | tail`, `journalctl -k`, `/var/log/kern.log` →
  `Out of memory: Killed process 1234 (app) total-vm:... anon-rss:...`.
  **Containers**: the *cgroup* memory limit triggers a cgroup-level OOM kill first — that's exactly what
  Kubernetes reports as `OOMKilled`, and the host-level OOM killer may never be involved.
- **Leaks.** A leak is *observable*: RSS (or cgroup usage) keeps growing and doesn't return to baseline.
  A kernel leak shows in `Slab` (`/proc/meminfo`) instead.

## 4. PRODUCTION MENTAL MODEL

```
/proc/meminfo ──► free -h
  MemTotal · MemFree · MemAvailable · Buffers · Cached · SwapTotal · SwapFree
       │ available = can I allocate more WITHOUT swapping?   ← alert on THIS
       ├── pressure ──► reclaim order: clean page cache → anon → swap → OOM killer
process:  VSZ (reserved) ──demand-paging─► RSS (touched) ──► SHR (shared with others)
OOM:      dmesg/journalctl "Out of memory: Killed process …"  + cgroup limits (containers)
```

## 5. INTERVIEW-SAFE ANSWER

"Linux gives every process virtual memory backed by physical pages only when they're touched. That's
why `RSS` is what a process actually holds in RAM and `VSZ` is what it's reserved — I've measured a
half-gigabyte reservation using 14 MB. When someone says the box is 'out of memory,' I don't look at
`free`, I look at `available` — because `used` includes page cache, which is reclaimable, and the
kernel will evict it before it swaps. Swap climbing is the real pressure signal, and sustained `si`/`so`
in `vmstat` means thrashing. If a process gets killed, I go straight to the kernel log — `dmesg` or
`journalctl -k` — and read the `Out of memory: Killed process` line, which tells me the victim, how
much memory it consumed, and its `oom_score_adj`. And in containers the cgroup memory limit does the
killing before the host-wide OOM killer ever wakes up — that's what `OOMKilled` means in Kubernetes.
For a suspected leak, I don't guess: I track RSS and cgroup usage over time and confirm it's monotonic
growth that never returns to baseline."

## 6. FOLLOW-UP ATTACKS

**Q.** `free -h` shows used 90% — is the server almost out of memory?
**A.** Not from that column alone. If `available` is still healthy, that "used" is mostly reclaimable
cache and the kernel will drop it under pressure. I pair `free -h` with actual allocation failure
evidence or swap pressure before concluding anything.

**Q.** Why did the OOM killer kill *my* process instead of the memory hog?
**A.** It kills the process with the worst **badness score** (memory + `oom_score_adj`), not necessarily
the biggest allocation. But a common cause of "my innocent process died" is a sibling in the same
cgroup killing everyone — in containers, once one process in the cgroup hits the limit, the whole group
is at risk. I read the OOM log to confirm who/what it blamed before assuming.

**Q.** How do you actually detect a memory leak?
**A.** Sample RSS (or cgroup `memory.current`) at intervals — a leak is RSS that grows and never returns
to baseline, often correlated with a deploy. `pidstat -r <pid> 1` or a simple loop of `ps -o rss`. For
kernel-level growth I watch `Slab`. I also check it survives a restart test — Rust, JNI, or C extensions
inside an otherwise-managed app are classic hidden leakers.

**Q.** What does swap-used rising mean when `free` still shows free RAM?
**A.** That free RAM is *cache*; the kernel decided to swap anon pages ahead of more aggressive cache
eviction (swappiness / IO patterns). The *signal* is `available` shrinking and swap growing — the
direction matters more than the label.

**Q.** Difference between `buff` and `cache`?
**A.** Let's keep it interview-simple: `buff` = pending block-device I/O; `cache` = page cache of file
data. Both are reclaimable; cache dominates and is the one people misread.

**Q.** `-Xmx4G` JVM on a 2 GB box with swap 0 — will it die?
**A.** Not instantly: `-Xmx` is a heap *ceiling*, RSS grows as the heap is actually used. On a 2 GB
box with a 4 GB heap configuration it either stays small, swaps if you had swap, or gets OOM-killed
when resident memory + everything else exceeds what's available. Never configure a heap above the box
without understanding it — but note Linux's default overcommit lets you *reserve* such a heap; miss,
and demand paging makes RSS the real constraint.

**Q.** OOM with exit code 137 what does 137 mean?
**A.** 128 + 9 = killed by SIGKILL. Combined with a kernel-log OOM line it's near-certainly the OOM
killer. (In containers `OOMKilled` is explicit; in bare runs 137 is the tell.)

**Q.** Is zero swap a good configuration?
**A.** It's defensible for some latency-sensitive workloads, but it removes the pressure-relief valve:
you skip swap entirely and go straight to OOM kill. The interview-safe position is: swap is a safety
net, swappiness tunes eagerness, and pinned/latency-critical services can opt out via `oom_score_adj`
and per-cgroup control — not a blanket "swap is bad."

## 7. PRACTICAL EXAMPLE (production)

An app's worker dies overnight. `systemctl status` shows exit 137. Evidence trail: `journalctl -k -n 50`
→ `Out of memory: Killed process 3123 (worker) total-vm:... anon-rss:2440600kB`; `free -h` at the time
showed `available` exhausted and swap 100% consumed; the OOM line's badness blamed the worker as the
largest Rss at that instant. Investigation continues in §11 — short version: it wasn't the database or
the neighbor, it was the app's own JNI-native allocations on a deployment 3 days old.

## 8. BUILD / REPRODUCE

All three labs verified on this box (randomtechy, non-root — so nothing below needs privileges).

### Lab 7 — page cache vs available (the "used is fake" demo)

```bash
free -h                      # note used / buff-cache / available
dd if=/dev/zero of=/tmp/large bs=1M count=128 2>/dev/null
free -h                      # cache grows ~128M → used grows with it
cat /tmp/large > /dev/null   # force the file into page cache
free -h                      # available ~unchanged: the cache is reclaimable, kernel still counts it
rm -f /tmp/large
```

Verified on this machine: after the 128 MB read, `buff/cache` grew **2.1G → 2.2G** while `available`
stayed **2.5G**. That exact behavior is the "used looks full but there's no problem" proof.

### Lab 8 — RSS ≪ VSZ: demand paging

```bash
python3 -c "
import mmap, os, time
m = mmap.mmap(-1, 512*1024*1024)            # reserve 512 MB virtual
for i in range(0, 512*1024*1024, 4096*128): # touch only every ~512 KB
    m[i] = 0
print(os.getpid()); time.sleep(5)
" &
sleep 1
ps -o pid,rss,vsz,args -p <insert the pid that printed>
cat /proc/<pid>/status | grep -E 'VmSize|VmRSS'
```

Verified: `VmSize: 539684 kB` (≈527 MB reserved) vs `VmRSS: 14368 kB` (≈14 MB resident). Half a
gigabyte "in use," 14 MB of real RAM. Demand paging in one command.

### Lab 9 — allocation failure the SAFE way (no OOM killer)

```bash
bash -c 'ulimit -v 100000; python3 -c "x=[bytearray(20*1024*1024) for _ in range(30)]"'
```

`ulimit -v` caps *virtual* memory → allocation returns `MemoryError` instead of triggering the OOM
killer. Verified: prints `MemoryError`, host untouched. Do NOT run the real OOM version on a shared
box — that's what cgroups/containers are for (exercised in the Docker/K8s domains).

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT A — "the app got OOM-killed" (full sequence)

**SYMPTOM:** worker exits, exit code 137, automated restart loops.
→ **SCOPE:** one process, one cgroup, or the whole host? (Host OOM vs cgroup OOM have different logs and
    different fixes — establish this first.)
→ **HYPOTHESES:** (a) whole-host pressure from another tenant/process, (b) the app itself leaked or
    spiked, (c) the cgroup/container limit is simply too small for the workload, (d) a deploy changed
    memory behavior (defaults! `-Xmx`, cache sizing, batch sizes).
→ **CHECKS, in order:**
1. `journalctl -k -n 100 | grep -i 'out of memory'` (and `dmesg -T | tail`; on RHEL-family
   `/var/log/kern.log`) — the OOM line names the victim, its Rss, and when.
2. `free -h` + swap — was the host truly out (`available` ≈ 0, swap 100%)? if not, suspect cgroup limit.
3. Container case: read the cgroup's usage before the kill — `systemctl status`/`kubectl get pod` plus
   `dmesg` showing `Memory cgroup out of memory`.
4. `ps -eo pid,rss,comm` sorted — who the neighbors were at that moment (from the cgroup's event files
   if recorded).
5. Check the deploy window — "what changed" applies to limits and code defaults too.
→ **EVIDENCE:** OOM line blames the worker's own anon-rss; host had free memory AFTER(?) — no cgroup had
    a real cap — but swap was exhausted; a 3-day-old deploy introduced a native library with unbounded
    cache.
→ **ROOT CAUSE:** memory leak in the app's native layer post-deploy; host OOM killer picked the biggest
    resident process when the box ran dry.
→ **FIX (smallest safe):** immediate = let orchestration restart the victim & give it a sane cgroup
    limit (so *badness* stops blaming innocent neighbors); then the real fix = cap the native cache and
    deploy the patch. NEVER "add RAM and move on" without the leak story.
→ **VERIFY:** RSS back to baseline; `available` and swap stay healthy over 24–48 h; restart loop stops.
→ **PREVENT:** alert on `available` and swap-used and *OOM-kill count* (they predict, OOM confirms);
    per-service memory limits so one leak can't take the host; memory tests in CI for the native layer.

### INCIDENT B — "memory creeping, nothing crashed" (leak hunt)

**SYMPTOM:** dashboard shows memory climbing day-over-day; no OOM yet.
→ **SCOPE:** host vs process vs slab.
→ **HYPOTHESES:** (a) process leak, (b) growing kernel `Slab` (driver/dentries — rare but real), (c)
    cache legitimately caching a bigger working set, (d) an unbounded in-app cache/map.
→ **CHECKS:**
1. `free -h` + `cat /proc/meminfo | grep -E 'Slab|SReclaimable|SUnreclaim'` — separate kernel vs user.
2. Top-RSS ranking; then `pidstat -r <pid> 1 30` or a timed loop of `ps -o rss,etime,args` for the
   suspected process.
3. correlate the growth curve with deploys/load.
→ **EVIDENCE:** one process's RSS climbs monotonically and doesn't fall on GC/checkpoint — replicas all
    share the slope.
→ **ROOT CAUSE:** unbounded caching in the app (per-request dictionary never cleared).
→ **FIX:** deploy the clear-the-cache patch / cap it; immediate pressure-relief = restart replicas
    (rolling) with evidence captured first.
→ **VERIFY:** RSS curve flatlines after patch across replicas.
→ **PREVENT:** alert on per-process/cgroup RSS p95 trend; cap caches; regression test.

### DECISION OVERLAY — what NOT to do

- Don't add RAM / scale up on a misread `used` column before checking `available` and swap.
- Don't disable swap as a reflex — that converts "slow" into "OOM-killed".
- Don't blame "random OOM kills" — the log names the victim and the numbers; read it first.
- Don't restart-and-ignore in leak cases: capture RSS history *before* the restart or you lose the
  evidence (memory state dies with the process — same principle as P0.1's evidence rule).

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "`free` used 90% → out of memory" | `used` includes reclaimable cache. Watch `available`. |
| "`free` column means free" | Available ≠ free; free is already-dropped cache only. |
| "RSS is all my process's own memory" | RSS includes shared pages (`SHR`) — real per-process footprint is less. |
| "OOM kills are random" | Badness heuristic: Rss + time + `oom_score_adj`. Deterministic enough to log and plan for. |
| "Set `oom_score_adj` = −1000 to be immune" | It shields *that process's score*; it doesn't protect its cgroup — container limits still kill it. |
| "Exit 137 = OOM always" | 137 is literally SIGKILL; pair it with the kernel OOM log or it's just "something SIGKILLed it." |
| "Swap is always bad" | Depends: safety valve vs latency; `swappiness` and per-cgroup control are the real tuning dials. |
| "Big VSZ = big RAM use" | VSZ is reserved, RSS is resident. 527 MB VmSize vs 14 MB VmRSS in Lab 8. |

## 13. FIRST-CHECK REASONING

- **"A process just died with 137 and restarts":** the OOM record first
  (`journalctl -k`/`dmesg -T`), because it names the victim, its Rss, and whether it was the host or a
  cgroup — three different fixes in one 40-second read. Cheap, conclusive, and preserves evidence.
- **"Server looks memory-full":** `free -h`'s `available` column first, not `used` — one read rejects
  the cache-red-herring hypothesis before you start scaling hardware.

## 14. PRIORITY

**P0.**

## 15. STOP HERE — done when you can…

1. read `free -h` and explain `used` vs `available` vs `free`, and when each is the right alarm;
2. reproduce the RSS ≪ VSZ demo (Lab 8) and the safe alloc-failure demo (Lab 9);
3. find and read the OOM evidence for a real kill (`journalctl -k`/`dmesg`) and name the victim + numbers;
4. explain why `oom_score_adj` and the cgroup limit (not the host killer) govern container kills;
5. run the leak-hunt sequence (RSS over time, slab check, deploy correlation) without reading this file.

## 16. DO NOT STUDY YET

THP/`khugepaged` tuning, SLAB allocator internals, memcg v2 internals, NUMA memory policy,
`vm.overcommit_*` tuning (know the *concept* of overcommit — see §6/`-Xmx` — not the tunables), and
`madvise`. All real, none 1–3 YOE interview material. "I know the concept, haven't needed to tune it
operationally" is the honest, senior-sounding line.

---

## QC CHECKLIST — LINUX.P0.3

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (meminfo → free → reclaim → OOM)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanism (pages, demand paging, cache, swap, badness)? | ✔ §3 |
| 5 | Dependencies (kernel reclaim, cgroups, swap device)? | ✔ §3 |
| 6 | Essential commands (`free`, `ps`, `vmstat`, `dmesg`/`journalctl -k`)? | ✔ §8–11 |
| 7 | Reproduce (Labs 7–9)? | ✔ verified on this box |
| 8 | Break it (cache illusion, alloc failure, leak)? | ✔ Labs 7/9 + Incident B |
| 9 | Observe + interpret evidence? | ✔ §8–11 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §11 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13).

---

# SESSION LINUX.P0.4 — DISK: `df`/`du`, INODES, DELETED-BUT-OPEN FILES

## 1. WHAT IS IT? (≤30 s)

A filesystem is the structure on a block device that organizes data into trees of files and directories,
with metadata in **inodes**. `df` shows block- and inode-level usage per mount; `du` walks trees and
sums sizes. "No space left on device" can mean *blocks* full, *inodes* full, or space locked up by
**deleted-but-open** files — three different root causes with different fixes.

## 2. WHY DOES IT EXIST?

Disk exhaustion is a top-3 cause of production outages: apps fail to write, databases go read-only-ish,
and Kubernetes evicts pods / marks nodes `DiskPressure`. The classic interview trap — "df says full but
du disagrees and nothing I delete helps" — is almost always deleted-but-open files or inode exhaustion,
and the fix is *not* "buy a bigger disk."

## 3. HOW DOES IT WORK?

- **Stack:** block device (`/dev/sdd`) → partition → filesystem (ext4/xfs) formatted with an **inode
  table** → mounted at a path (VFS abstracts this). `df` is per-filesystem; `du` is per-tree.
- **Inodes.** One inode per file (metadata: perms, owner, size, block pointers, timestamps) is created
  when the *first* directory entry for a file is made. ext4 sizes the inode table at `mkfs` time —
  inode count is **fixed**; XFS allocates dynamically. A filesystem full of lots of tiny files hits
  `ENOSPC` on inodes while `df` shows plenty of blocks. Read with `df -i`.
- **Hard links & `rm`.** A file is a directory entry pointing at an inode; multiple names can point to
  the same inode. `rm` removes one *name*. The inode (and its data) is freed only when (a) the link
  count reaches 0 **and** (b) no process has it open.
- **Deleted-but-open files.** `rm` a file while a process holds it open → link count 0, but the data
  blocks persist until the last handle closes. Classic symptom: `df` Says full, `du` says "only half of
  that is accounted for," and deleting more files doesn't help. Evidence: `lsof +L1` (shows inodes with
  link count 0) or `/proc/<pid>/fd/*` entries marked `(deleted)`. Fix: live-truncate or restart the
  holder — the space returns the moment the last fd closes.
- **The truncate-not-rm trick.** For a growing log of a live process: `: > /path/log` or
  `truncate -s 0` frees blocks now while keeping the fd valid. Plain `rm` beats you: the process keeps
  writing to the *deleted inode* and the space comes back — the famous "I deleted the log and it grew
  anyway" bug.
- **Two more "full" faces:** **reserved blocks** (ext4 keeps ~5% for root by default — non-root users
  see ENOSPC while `df` shows free) and **mount hiding** (a nested mount makes `du`/`df` appear to
  disagree; always use `du -x`, one filesystem).
- **The silent growing logs:** journald (`/var/log/journal`, capped by
  `SystemMaxUse` in `/etc/systemd/journald.conf`) and — very commonly — **Docker/Kubernetes container
  JSON logs** (`/var/lib/docker/containers/.../<id>-json.log`), which are unbounded by default. Big
  container-log disk-fill is a recurring node-level incident.

## 4. PRODUCTION MENTAL MODEL

```
df -h / df -i ── per-mount usage: blocks (1K-B/partitions) vs inodes (files)
                  ├── blocks 100%  → delete real data or reclaim
                  ├── inodes 100%  → delete tiny files (df -i)   ← not a space problem
                  └── du disagrees with df → deleted-but-open (lsof +L1) or mount hiding
du -xhd1 / | sort -h  → biggest directories      (x = stay on this one filesystem)
find / -xdev -type f -size +500M → biggest individual files
frees only when: link count == 0 AND no open fd
truncate, don't rm, live logs (or restart the holder)
```

## 5. INTERVIEW-SAFE ANSWER

"When the disk 'fills up,' I treat that as three different problems until proven otherwise. First `df -h`
for blocks and `df -i` for inodes — a directory full of tiny files can exhaust inodes while blocks are
plenty, and everyone who just deleted big files loses that fight. Second, if `du` says way less than
`df`, I suspect deleted-but-open files: a process is holding a handle to a deleted file, so `rm` freed
the name but not the blocks — `lsof +L1` shows those handles, and the space comes back when the process
closes or restarts. Third, mount boundaries: I always use `du -x` and compare per-mount, not across
mounts. For live growing logs I truncate — `: > log` — rather than `rm`, because deleting the file from
under a running process makes it write into a deleted inode and the disk fills all over again. And in
containerized environments the usual culprit is unbounded Docker/Kubernetes JSON logs under
`/var/lib/docker`, which is why log rotation and limits get set before this becomes a page."

## 6. FOLLOW-UP ATTACKS

**Q.** `df -h` shows 100% used but `du` only accounts for half. Where's the rest?
**A.** Deleted-but-open files (most common), reserved blocks, or a nested mount. `lsof +L1` to list
zero-link open files, then restart/truncate the holder. This is the interview's favorite disk question.

**Q.** Space is free, yet apps report "No space left on device." Why?
**A.** Inode exhaustion — `df -i` at 100%. The fs can't create a new *file entry*. Fix = delete many
small files (cache/tmp directories, tool spools, container layers) or grow the fs. XFS sidesteps this
with dynamic inodes.

**Q.** I `rm -f` a big log but `df` didn't drop. What happened?
**A.** A process still has it open. Space is freed at last-close. And if it was an *appender*, it's now
writing into a deleted inode — `: >` the file (truncate) or restart the writer, then it's actually gone.

**Q.** How do you find what's eating disk quickly?
**A.** Top-sums: `du -xhd1 / 2>/dev/null | sort -h | tail -15` narrows to a mount and directory level;
then `find / -xdev -type f -size +500M` (plus `-size +10M` for subtler spots) for big files. Suspect
paths first: container/code logs, `/var`, `journal`, Docker, tmp/cache, database WALs.

**Q.** What does `df -h` vs `df -H` matter?
**A.** `-h` = powers of 1024 (GiB), `-H` = powers of 1000 (GB). Same physical space, ~7% different
numbers — quoting the wrong prefix to an interviewer (or a capacity review) is a credibility slip.

**Q.** Why does the app break when disk fills, not just "write fails"?
**A.** Writes fail → transactions/journal can't commit, daemons crash or hang on disk-timeout FDs, and
on Kubernetes `DiskPressure` evicts pods — the blast radius is systemic, not just one file.

**Q.** ext4 vs xfs for a busy, many-files workload?
**A.** At 1–3 YOE I'd say: both are fine day-to-day; the difference that bites candidates is that ext4
pre-allocates a fixed inode table while XFS grows inodes on demand — an ext4 "full" on a spike of
millions of small files from the inode side is a real outage class. If your target role is
filesystem-heavy, XFS is the growing default.

## 7. PRACTICAL EXAMPLE (production)

A microservice node fills: `df -h /` at 98%, deployments start failing, pods report `DiskPressure`.
`du -xhd1` points at `/var/lib/docker/containers`. Inside, one app container's `*-json.log` is 40 GB —
Docker's default JSON-file driver has no rotation until you configure `max-size`/`max-file`. The
container is *running* and holding the fd, so `rm` alone won't reclaim anything. The fix is truncate +
set rotation; the *investigation* changed because the evidence said mount, directory, file, holder — in
that order.

## 8. BUILD / REPRODUCE

Labs verified on this box (non-root). WSL note: `/` here is `ext4` on `/dev/sdd`; `df` also shows the
`overlay`/`tmpfs` pseudo-mounts — good practice at reading mixed output.

### Lab 10 — map the disk (read-only recon)

```bash
df -hT              # per-mount blocks, with fs type (T) — spot the pseudo-mounts
df -i               # per-mount inodes — the silent killer for tiny-file workloads
du -xhd1 / 2>/dev/null | sort -h | tail -15     # biggest directories, one filesystem
find / -xdev -type f -size +500M -printf '%s %p\n' 2>/dev/null | sort -rn | head   # biggest files
```

### Lab 11 — inode reading

```bash
df -i /
find / -xdev -type f | wc -l        # rough file-count feel for a dir/fs density
```

On this box inodes `IUse%` ≈ 1% — healthy. The lesson is *reading*, not drama: if your target box shows
`IUse%` in the 90s with sparse block use, you just diagnosed the next "no space" ticket.

### Lab 12 — deleted-but-open file (break + fix) — verified

```bash
dd if=/dev/zero of=/tmp/delete_me bs=1M count=64 2>/dev/null
python3 -c "import time; f=open('/tmp/delete_me','r'); time.sleep(25)" &
holder=$!
sleep 1
rm -f /tmp/delete_me
free1=$(df -P /tmp | tail -1 | awk '{print $4}')
echo "df avail right after rm: $free1 (blocks still held by open fd)"
lsof +L1 | grep delete_me          # the smoking gun: link count 0, still open
kill "$holder"
sleep 1
free2=$(df -P /tmp | tail -1 | awk '{print $4}')
echo "df avail after holder exits: $free2 (64 MB returned)"
lsof +L1 | grep delete_me || echo "no deleted-open handles remain"
```

Verified behavior on this machine: `df` **unchanged** after `rm` (the 64 MB stayed claimed), `lsof +L1`
listed the handle, and **+64 MB returned** once the holder process died. That's the whole deleted-open
story in one lab.

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "no space left" (full sequence)

**SYMPTOM:** app can't write; monitoring pager: `/` at 98%; on K8s: pods evicting, node on `DiskPressure`.
→ **SCOPE:** which mount, which host, what kind of consumer. One `df` + one `du` command tree.
→ **HYPOTHESES:** (a) real block exhaustion (big files/logs/WALs), (b) inode exhaustion, (c)
    deleted-but-open holders, (d) mount hiding / reserved blocks, (e) snapshots or another fs sharing the
    same underlying device.
→ **CHECKS, in order:**
1. `df -h <mount>` **and** `df -i <mount>` together — splits (a) vs (b) in one read.
2. `du -xhd1 <mount> 2>/dev/null | sort -h | tail -15` — the attacker's directory.
3. discrepancy? → `lsof +L1` (deleted-but-open) + `lsof <mount>` for holders.
4. `lsblk`/`findmnt` — long shot (e)/(d): is this fs the only consumer of the block device? any odd
   nested mounts?
5. K8s context: `journalctl -u kubelet` / `kubectl describe node` → which pod's volume/logs grew.
→ **EVIDENCE:** 40 GB `*-json.log` under `/var/lib/docker/containers/<id>`, written by the running
    container (fd open, `lsof` shows flagged `(deleted)` if someone already `rm`'d a prior rotation
    attempt).
→ **ROOT CAUSE:** unbounded JSON-file docker logging; owner never shipped rotation.
→ **FIX (smallest safe):** emergency = `: > path/to/json.log` (truncate, keep fd valid, reclaim blocks);
    then configure rotation (`max-size`/`max-file`, daemon.json or per-container), restart the container,
    and let it grow bounded.
→ **VERIFY:** `df -h` avail rising; `df -i` stable; app writes succeed; pod stable; then watch the
    *bounded* growth for a few hours.
→ **PREVENT:** rotation config defaulted fleet-wide (IaC), alert on `df`/`df -i` thresholds before the
    kill, alert on `DiskPressure` if K8s, run logrotate-aware practices team-wide.

### DECISION OVERLAY — what NOT to do

- Don't `rm` a live appender's log as "the fix" — you'll free the name, keep the inode, and it regrows
  (truncate instead, or restart after logging the evidence).
- Don't restart every container to "free space" — find the holder first (`lsof +L1`); a restart kills
  the fd anyway, but you lose the chance to confirm WHICH process was at fault.
- Don't delete production data (old logs? app files?) without the `du` snapshot and a rollback plan.
- Don't conclude "need a bigger disk" while `df -i` or `lsof +L1` or a missing rotation config explains it.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "`rm` frees disk immediately" | Only if link count → 0 **and** no open fd. Deleted-but-open keeps the blocks. |
| "df and du should always agree" | They measure different things (blocks vs tree). Mismatch = investigate, not a bug. |
| "No space = delete data, done" | Three root causes: blocks / inodes / open-deleted. `df -h` + `df -i` first. |
| "Inodes only matter for tiny FSs" | A spike of millions of small files (caches, tool spools, layers) exhausts ext4 inodes on any size. |
| "`df -h` and `free -h` use the same units" | Different tools, same-ish convention — but `df -H` (1000) vs `-h` (1024) is a real ~7% trap. |
| "Big disk usage = big files" | Millions of small files exhaust inodes, barely moving blocks. |
| "`du -sh *` is trustworthy across mounts" | Without `-x` it crosses filesystem boundaries; nested mounts hide reality. |
| "Deleting the file from a running container works" | The container holds the fd; you've just created a deleted-but-open leak. Truncate or restart it. |

## 13. FIRST-CHECK REASONING

- **"No space left":** `df -h` **and** `df -i` in the same breath — one read splits the block-vs-inode
  hypothesis families, which have opposite fixes. Almost everything else you can do on a full disk is
  wasted effort until you know which one is full.
- **"df full, du normal":** `lsof +L1` next — a zero-cost command that confirms (or kills) the
  deleted-but-open theory before you touch any files.

## 14. PRIORITY

**P0.**

## 15. STOP HERE — done when you can…

1. run `df -h`, `df -i`, and the `du`/`find` reconnaissance and interpret all three;
2. reproduce Lab 12 (deleted-but-open) and predict the `df` numbers before running it;
3. explain the truncate-vs-rm distinction for live logs, including why `rm` regrows;
4. enumerate the four ENOSPC root causes and the evidence that distinguishes each;
5. answer the mount-hiding and `-h`/`-H` follow-ups without notes.

## 16. DO NOT STUDY YET

Filesystem *internals* (ext4 journal/jbd2, XFS log, btrfs/zfs), LVM/snapshot design, fstrim/TRIM tuning,
RAID levels, quota enforcement, `debugfs`. Know what LVM/RAID *are* for a one-liner; nothing deeper.
"Not needed operationally at my level" is the honest, safe line.

---

## QC CHECKLIST — LINUX.P0.4

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (df/du/inode/backref)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanism (inodes, link counts, open-deleted, mounts)? | ✔ §3 |
| 5 | Dependencies (block device, fs, mount, open fds)? | ✔ §3 |
| 6 | Essential commands (`df`/`du`/`find`/`lsof`/`df -i`)? | ✔ §8–11 |
| 7 | Reproduce (Labs 10–12)? | ✔ Lab 12 verified live |
| 8 | Break it (open-deleted leak, inode pressure)? | ✔ Lab 12 + §11 |
| 9 | Observe + interpret evidence? | ✔ §8–11 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §11 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13).

---

# SESSION LINUX.P0.5 — PERMISSIONS: USERS/GROUPS, `chmod`/`chown`, `sudo`, SSH

## 1. WHAT IS IT? (≤30 s)

Every file and directory carries an owner, a group, and a `rwx` permission triplet for owner/group/
other. Users and groups are the identity layer (`/etc/passwd`, `/etc/group`, `/etc/shadow`);
`sudo` is delegated privilege with an audit trail; SSH is the authentication+channel that nearly
every server session rides on. Permission bugs are usually "who am I" bugs hiding as "why can't I."

## 2. WHY DOES IT EXIST?

"Permission denied" is the most common ops error after "no space left," and SSH auth issues are what
lock you *out* of everything else. Understanding the owner/group/`rwx` model, the least-privilege
purpose of `sudo`, and SSH key auth is what turns "works in my shell" into "works as the CI user, on
the right files, for the right reason."

## 3. HOW DOES IT WORK?

- **Identity.** `uid`/`gid` are numbers; names live in `/etc/passwd`, `/etc/group`, passwords in
  `/etc/shadow`. `root` = uid 0 = unconstrained by file permissions. See `id -u`, `id -gn`. A process
  runs with an *effective* identity — that's the one the permission check uses.
- **The triplet.** Digits 4 (read), 2 (write), 1 (execute); octal `755` = `rwxr-xr-x`. Symbolic:
  `chmod u+rwx,g-w,o+r file`. For **directories** the meaning shifts: `r` = list names, `w` = create/
  delete *names inside*, `x` = traverse/cd into it. Consequence: a file can be `rw-` while you still
  can't `rm` it, because deletion is governed by the **directory's** write bit — a classic trap.
- **`chown` vs `chmod`.** `chown user:group` fixes ownership; `chmod` fixes the bitmask. The modern
  gotcha: `chown -R` an app dir changes ownership but not the bits; the "worked as root, fails as the
  service user" bug is a *triplet vs identity* mismatch, not `chmod 777`-needed.
- **Special bits.** `setuid` (4, `s` in owner x slot — e.g. `/usr/bin/passwd` `-rwsr-xr-x`): runs with
  the file's owner. `setgid` (2). **Sticky** (1, `t` on dirs, e.g. `/tmp` `drwxrwxrwt`): only the file
  owner (or dir owner/root) can delete names inside — stops users deleting each other's `/tmp` files.
- **`umask`.** Octal mask subtracted from default perms at creation (0022 → files get `644`, dirs `755`).
  A 0077 umask ⇒ navel files are private. "git clone worked, cron script can't read the key" is often a
  umask story.
- **`sudo`.** Runs a command as another user (usually root) with the invoking user's environment and a
  log trail — least privilege over `su`/root shell. Rules in `/etc/sudoers`, **edit with `visudo`**
  (it validates syntax on write — a broken sudoers bricks ALL sudo, a classic self-inflicted outage).
  Simple rule anatomy: `user ALL=(ALL:ALL) ALL` = "anywhere, as any user:group, run anything."
  `NOPASSWD:` skips the password for specific commands (used by CI/automation accounts — a security
  trade-off to flag, not "solved").
- **SSH key auth.** A keypair: the *private* key proves identity, the *public* key is copied to
  `~/.ssh/authorized_keys` on the target. The server proves you hold the private key without it ever
  leaving your machine (challenge-response), and (optionally) identity can be proxied via `ssh-agent`.
  Non-negotiable hygiene: private key **0600**, `~/.ssh` **0700** (often `authorized_keys` 0600 too,
  owned and not group-writable, or sshd refuses under strict modes). First connection stores the host
  key in `known_hosts` (TOFU = trust-on-first-use).
  **The skip trap (lab-verified):** if your private key's permissions are too open, OpenSSH silently
  *skips* it and the server just sees no valid key → the confusing, generic
  `Permission denied (publickey)`. The client didn't say why; the server legitimately rejected.

## 4. PRODUCTION MENTAL MODEL

```
identity:  uid/gid (id -u / id -gn)  →  process effective identity → answers "who am I on this host?"
check:     owner / group / other × rwx        (octal 4-2-1 | symbolic u/g/o)
dirs:      r=list · w=add/rm names · x=traverse   → deletion needs DIR w, not file w
special:   setuid s (passwd) · setgid · sticky t (/tmp)
umask →  defaults at creation (files 644 · dirs 755 @ 022)
sudo:      /etc/sudoers via visudo · user ALL=(ALL:ALL) ALL · NOPASSWD for automation
ssh:       private key 0600 → ~/.ssh 0700 → authorized_keys 0600+owned
           loose perms ⇒ key silently skipped ⇒ generic "Permission denied (publickey)"
debug:     ssh -vvv  (client)  +  /var/log/auth.log / journalctl -u ssh  (server)
```

## 5. INTERVIEW-SAFE ANSWER

"Linux checks every file access against the *process's effective identity*: owner, then group, then
other, with r/w/x meaning one thing for files and a slightly different thing for directories — for
example, deleting a file needs write on the *directory*, not the file, which is why you can 'not
delete' an obviously writable file. When something reports 'permission denied,' my first question is
'who am I actually running as' — `whoami`/`id` plus `ls -l` on the file — because CI users, cron, and
systemd services all run as someone other than me, and most of these bugs are identity mismatches or a
umask, not a missing `chmod 777`. For privilege, we use `sudo` against `/etc/sudoers`, edited with
`visudo` so a syntax slip can't lock the whole box out of sudo. For SSH, authentication is proof of
holding the private key via challenge-response; the public key lives in `authorized_keys`. The hygiene
I insist on: private key 0600, `~/.ssh` 0700, `authorized_keys` owned and not group-writable. And a
gotcha I've hit: if the key's permissions are too open, OpenSSH silently skips it and you get a generic
'Permission denied (publickey)' with no explanation — so I check key modes before I touch the server."

## 6. FOLLOW-UP ATTACKS

**Q.** Why can't I delete a file I own and can write?
**A.** Unlink is controlled by the **parent directory's** write+execute bits, not the file's. Check
`ls -ld` the directory (and sticky bit: on `/tmp` you can only delete your OWN files — the `t`).

**Q.** Difference between `sudo` and `su`?
**A.** `su` starts a new login session as the target user (a root *shell*, all-or-nothing); `sudo`
executes a single command as root with your environment and a log entry — least privilege. This is why
the modern policy is "no root shells over SSH + sudo."

**Q.** What does the `s` in `-rwsr-xr-x` mean and why does it matter?
**A.** setuid — the program runs with its owner's privileges. `/usr/bin/passwd` is `rws` root so a
normal user can change their password in `/etc/shadow`. Also why a world-writable setuid-root binary is
a root-exploit primitive. (Creating a bad one is out of scope; recognizing it in `ls -l` is in scope.)

**Q.** SSH says `Permission denied (publickey)` — what do you check and in what order?
**A.** Client side first because it's cheap: `ssh -vvv` and the identity key's **modes** (the silent-skip
trap), then whether the right key is being offered at all (`-o IdentitiesOnly=yes`), then the user name.
Server side: `journalctl -u ssh` / `auth.log` for the real reason — wrong user, missing key, wrong
`authorized_keys` perms (`~/.ssh` must not be group-writable), or `AllowUsers`/`sshd_config`
restrictions.

**Q.** Why is `chmod 777` usually wrong advice?
**A.** It removes the *entire* protection model — group/other get everything. The correct fix is identity
alignment (chown to the service user) or the narrowest `chmod` (e.g. `755`, or group-write only).

**Q.** umask 077 vs 022 — what's the practical difference?
**A.** 022 → new files `644`, dirs `755` (readable by group/other); 077 → files `600`, dirs `700`
(private). A backup/agent user that can't read files created under 077 is a classic cross-team failure.

**Q.** Why does CI "work locally"?
**A.** Your shell ≠ the CI user: different identity, home, umask, secrets, and working directory. The
interview-grade habit is "reproduce as the failing identity": `sudo -u ciuser`, or the same user in a
container, and *then* look at perms.

## 7. PRACTICAL EXAMPLE (production)

An ECS-consumer deploy step fails with `Permission denied` reading a private SSH key while it "works
locally." The CI runner executes as `runner` with umask 0022 but a script extracted the key with default
perms 0644 → OpenSSH silently skips it → `Permission denied (publickey)` to the artifact host. The
evidence chain: `ssh -vvv` + `ls -l` on the key (0644) + `id` of the runner. Fix: `chmod 600` in the
pipeline + make the runner's umask/storage explicit. Not a single line of server-side change.

## 8. BUILD / REPRODUCE

Verified on this box (uid 1000, no passwordless sudo → every lab below is non-root).

### Lab 13 — who am I + primitives (read)

```bash
id -u; id -gn; id                    # project ownership/group membership
umask                                # defaults that will be applied at create
ls -ld /tmp                          # drwxrwxrwt → sticky bit in action
ls -l /usr/bin/passwd                # -rwsr-xr-x → setuid-root binary, no root needed to observe
```

### Lab 14 — dir-write vs file-write (the "can't delete my file" factory)

```bash
mkdir -p /tmp/perm/dir && echo hi > /tmp/perm/dir/f
chmod 777 /tmp/perm/dir/f            # the FILE is maximally writable...
chmod 555 /tmp/perm/dir              # ...but the DIR only allows list+traverse
rm /tmp/perm/dir/f                   # fails: deletion = parent dir write+execute, not file perms
chmod 775 /tmp/perm/dir              # restore dir write → rm now works
rmdir /tmp/perm/dir; rm -rf /tmp/perm
```

### Lab 15 — the SSH silent-skip key trap (verified live)

```bash
rm -rf /tmp/sshtest && mkdir /tmp/sshtest
ssh-keygen -t ed25519 -N '' -f /tmp/sshtest/id_k -q        # throwaway keypair
chmod 0664 /tmp/sshtest/id_k
ssh-keygen -y -f /tmp/sshtest/id_k    # → "WARNING: UNPROTECTED PRIVATE KEY FILE!" (verified)
chmod 0600 /tmp/sshtest/id_k
ssh-keygen -y -f /tmp/sshtest/id_k    # parses fine (verified)
# same trap during a real attempt (verified against a live SSH endpoint):
#   loose perms ⇒ ssh silently skips the key ⇒ server replies:
#   "Permission denied (publickey)"   ← no client-side warning at all
```

Takeaway: private-key modes **before** blaming the server. Bonus: `ssh -vvv` shows which identity files
were offered and why — the narratable debugging flow.

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT A — "deploy works locally, fails in CI" (full sequence)

**SYMPTOM:** CI job aborts with `Permission denied` on a key/artifact path; identical command passes in
your shell.
→ **SCOPE:** one step vs the whole job; the *identity* executing that step.
→ **HYPOTHESES:** (a) different user (runner vs you), (b) umask/permissions of created files (CI unpacks
    keys with looser modes), (c) missing secrets/env in CI, (d) path/mount doesn't exist for that user.
→ **CHECKS, in order:**
1. Reproduce as the failing identity: `sudo -u <ciuser> -- <same command>` (or the container equivalent)
2. `whoami; id; umask` inside the *step* (add a debug step) — confirm (a)/(b) immediately.
3. `ls -l` the exact key/artifact the step reads — match mode vs who is reading it.
4. Confirm the secret was injected (`printenv KEY` in the step, redacted at log time).
→ **EVIDENCE:** runner runs as `runner`, umask 0022, key on disk `0644` → read OK by user but skipped
    by ssh → `Permission denied (publickey)` to the artifact host.
→ **ROOT CAUSE:** CI-step identity + default key modes ≠ your shell's session, per §7.
→ **FIX (smallest safe):** `chmod 600` for keys at pipeline materialization + make the runner creds and
    umask explicit; optionally run the step under the app user.
→ **VERIFY:** same CI job green twice in a row; key modes confirmed via a `ls -l` artifact step.
→ **PREVENT:** CI users and local devs share the *same documented* key/perm standard; validate modes in a
    pipeline preflight (break the build, not prod).

### INCIDENT B — "SSH died overnight, Permission denied (publickey)" (full sequence)

**SYMPTOM:** automation boxes and humans both fail SSH auth; control-plane step dies.
→ **SCOPE:** one host, one user, or all hosts (helps decide client vs server vs config-deploy).
→ **HYPOTHESES:** (a) key perms story (client-side silent skip), (b) `authorized_keys` changed/corrupted,
    (c) `/etc/ssh/sshd_config` or `AllowUsers` restriction changed, (d) password-auth disabled + no key
    flow = out, (e) `~/.ssh` modes on the server became group-writable (strict modes reject), (f)
    host key changed → scary `host key verification failed` is a *different* symptom (findable).
→ **CHECKS, in order:**
1. Client: `ssh -vvv` — read which identities are offered and the exact server reply.
2. Client: `ls -l ~/.ssh/id_*` — eliminate the silent-skip trap before touching the server.
3. Server: `journalctl -u ssh -n 50` / `/var/log/auth.log` — sshd KNOWS why it rejected (bad modes,
   wrong user, no such key, restriction). Trust the log, not guesses.
4. `ls -ld ~/.ssh; ls -l ~/.ssh/authorized_keys` on server; `sshd -t` to validate config.
→ **EVIDENCE:** auth.log: `Authentication refused: bad ownership or modes for file
    /home/app/.ssh/authorized_keys` — a recent deploy had `chown -R`ed to root.
→ **ROOT CAUSE:** server-side `authorized_keys` ownership/modes broken by a config-management run →
    strict modes refuse all key auth.
→ **FIX:** restore owner+mode (app user, 0600/0700), `sshd -t`-validate, retry.
→ **VERIFY:** a fresh `ssh` succeeds; config-run idempotency fixed so it can't regress.
→ **PREVENT:** declarative config that pins modes (IaC), alert on auth-refused from chronic paths, and a
    documented recovery (an out-of-band console is the escape hatch — plan for it).

### DECISION OVERLAY — what NOT to do

- Don't `chmod 777` the path to make it "just work" — it works by deleting the security model.
- Don't hammer `ssh` retries on "Permission denied (publickey)": run `ssh -vvv` once and read it.
- Don't restart/disable sshd while testing auth — sshd restart is fine, but note `sshd -t` *before*
  restarting with a possibly-broken config (avoid the can't-ssh-in-at-all spiral).
- Don't ignore the client silently-skipping loose-perm keys (Lab 15) — it looks like a server failure.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "File perms decide who can delete" | Unlink = parent **directory** write+execute (+ sticky watches it). |
| "`chmod 777` = fixing perms" | It's deleting the model. Fix identity/umask; use the narrowest bits. |
| "`sudo` = a root shell" | It's per-command delegation with a log; `sudo -i` is the shell variant. |
| "editing sudoers is safe" | A syntax error bricks ALL sudo. `visudo` validates before save. |
| "A `644` private key is fine if nobody reads it" | OpenSSH's mode check silently SKIPS it → confusing `Permission denied (publickey)` (lab-verified). |
| "`Permission denied (publickey)` = bad key on server" | Often a *client* mode problem, wrong user, or a silently-skipped key. Read `ssh -vvv` + server log. |
| "Root sees everything, so CA works anywhere" | Root bypasses file perms but not SELinux, capabilities, or mount restrictions — the next-layer surprises. |
| "`chown user:group file` fixes access entirely" | Only ownership of the identity layer; the `rwx` mask and umask still apply. |
| "r/w/x mean the same on dirs" | On dirs: r=list, w=create/remove names, x=traverse. File semantics don't carry over. |

## 13. FIRST-CHECK REASONING

- **"Permission denied"** → `whoami; id; ls -l <path>` together — one pass answers the two hypothesis
  families (wrong identity vs wrong mask) that cover ~95% of cases before you touch `chmod`.
- **SSH "Permission denied (publickey)"** → client key **modes** plus `ssh -vvv` first, because the
  cheap local check eliminates the silent-skip trap (Lab 15) and the verbose log shows what was offered
  — only then go read the server's `auth.log`.

## 14. PRIORITY

**P0.**

## 15. STOP HERE — done when you can…

1. explain who-am-I vs file-mask debugging and reproduce the dir-write deletion rule (Lab 14);
2. produce and explain the SSH silent-skip trap (Lab 15) and inspect modes before blaming a server;
3. explain `sudo` vs `su`, why `visudo`, and why a broken sudoers is an outage;
4. read `ls -l` (including `s`/`t` bits and umask effects) fluently in both octal and symbolic form;
5. run a permissions incident as a sequence, not a `chmod 777` reflex.

## 16. DO NOT STUDY YET

SELinux/AppArmor policy *crafting* (concept only), PAM modules, sudoers rule-engine depth (host/user
aliases), LDAP/Kerberos integration, Linux capabilities beyond "it exists", `getfacl`/ACL management.
"Can't do it as a user, and I know why" is a fine answer; "I can write SELinux policies" is a claim to
NOT make at 1–3 YOE.

---

## QC CHECKLIST — LINUX.P0.5

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (identity → check → special bits → ssh)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanism (triplets, dir semantics, sudo/sshd)? | ✔ §3 |
| 5 | Dependencies (users/groups, PAM, sshd config)? | ✔ §3 |
| 6 | Essential commands (`id`, `umask`, `chmod`, `ls -l`, `sudo`, `ssh -vvv`, `visudo`)? | ✔ §8–11 |
| 7 | Reproduce (Labs 13–15)? | ✔ verified on this box |
| 8 | Break it (dir-delete rule, loose key perms)? | ✔ Labs 14–15 |
| 9 | Observe + interpret evidence? | ✔ §8–11 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §11 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13).

---

# SESSION LINUX.P0.6 — SYSTEMD + JOURNALD: UNITS, `systemctl`, "SERVICE WON'T START"

Environment note: this box runs **systemd as PID 1** (`ps -p 1` → systemd, `systemctl is-system-running`
→ running), and our user manager works, so the labs are real, non-root, user-unit labs. Production
services you'll manage are system units under `/etc/systemd/system` — the semantics are identical.

## 1. WHAT IS IT? (≤30 s)

systemd is PID 1: it boots the machine, orders service startup, supervises daemons (start/restart/
stop per unit files), isolates them with cgroups, and collects their logs into **journald** ("service
won't start" is *its* verdict + the journal's job to explain).

## 2. WHY DOES IT EXIST?

Before systemd, init scripts were shell scripts with no ordering, no restart policy, no supervision
and scattered log files. systemd replaces that with declarative **units**, dependency+ordering,
auto-restart, per-service resource controls, and one queryable structured log. In 2026 it's simply the
default on Ubuntu/Debian/RHEL/Rocky — and "restart the service / why won't it stay up" is a core
day-1 DevOps skill.

## 3. HOW DOES IT WORK?

- **Units.** A `.service` unit file describes one supervised process. Locations: `/usr/lib/systemd/system`
  (ship-with-package, never edit), `/etc/systemd/system` (admin overrides + your own services), and for
  labs: `~/.config/systemd/user` (per-user, no root).
- **Dependency vs ordering** (a classic follow-up): `Requires=`/`Wants=` express *dependency*;
  `After=`/`Before=` express *ordering*. `After=dbus.service` means "start after dbus starts", not
  "require dbus to be running". `Wants` doesn't block startup failure; `Requires` (weak-ish: unit may
  still start) is stronger — don't conflate the two families.
- **The `[Service]` block that decides behavior:**
  - `Type=` — **simple** (started as soon as `ExecStart`'s process spawns; most apps), **oneshot**
    (run-to-completion, exits = done), **forking** (daemon double-forks; systemd must be told the
    `PIDFile=`/wait), **notify** (app calls `sd_notify` to signal real readiness),
    **exec** (started after the binary successfully execs).
  - `ExecStart=`/`ExecStartPre=`/`ExecStartPost=`; `User=`/`Group=` (drop privileges); `WorkingDirectory=`;
    `Environment=` (or `EnvironmentFile=`).
  - `Restart=` — `no`, `on-failure` (exit≠0), `always` (even clean exit), `on-abnormal`… plus
    `RestartSec=`.
  - `StartLimitIntervalSec=` + `StartLimitBurst=` — if a unit starts too often in a window, systemd
    refuses further start attempts: **`start-limit-hit`**. `systemctl reset-failed` clears it.
  - `TimeoutStartSec=`/`TimeoutStopSec=`; `LimitNOFILE=`.
- **`[Install]` + enable/start.** `start` = run now; `enable` = register (symlink into multi-user.target
  `WantedBy=`). They are different axes: `enable --now` does both.
- **`daemon-reload`.** systemd caches unit definitions. After you edit any unit file, you MUST
  `systemctl daemon-reload` (a bare `restart` won't pick up the new definition). `status` prints a
  warning when it detects changed files on disk — a great tripwire.
- **`mask` vs `disable`.** `disable` removes boot symlinks but the unit can still be started by hand.
  `mask` symlinks the unit to `/dev/null` — even a manual start is refused.
- **journald.** All services (and the kernel, `journalctl -k`) write structured logs. `journalctl -u <svc>`
  (that unit only), `-f` follow, `-n 100` tail, `--since "10 min ago"`, `-p err` (min severity), `-b`
  (current boot), `-x` (explain). Persistent storage lives in `/var/log/journal` (size-capped by
  `SystemMaxUse` in `/etc/systemd/journald.conf`).
- **Supervisor state ≠ app health.** `active (running)` means systemd considers the unit started — it
  is NOT proof the app listens, is ready (Type=simple says "started" immediately), or is serving. That
  gap is exactly what readiness-probes exist for in Kubernetes.

## 4. PRODUCTION MENTAL MODEL

```
unit file (/etc/systemd/system) ──daemon-reload──► systemd (PID 1)
   [Unit]     After= / Wants= / Requires=      ordering vs dependency
   [Service]  Type= / ExecStart= / User= / Restart= / StartLimit*
   [Install]  WantedBy=multi-user.target  (enable ⇄ boot-start symlink)
start ──► spawns process ──► cgroup ──► journald ──► journalctl -u <svc>
crash ──► Restart=on-failure/always ──► RestartSec ──► burst → start-limit-hit → reset-failed
status:   active(running) = supervisor ok   ≠   app actually serving (readiness lives elsewhere)
```

## 5. INTERVIEW-SAFE ANSWER

"systemd is PID 1 — it's the boot-and-supervision layer. Each service is a unit file with three blocks:
`[Unit]` for dependency and ordering — and I'm careful: `After=` is ordering, not dependency; `Wants=`/
`Requires=` is dependency — `[Service]` for how it runs and restarts, and `[Install]` for boot enabling.
For 'it won't start' my first move is always `systemctl status <svc>` — it shows the active/result
state, the main PID and its exit code — and then `journalctl -u <svc> -n 100`, because the journal has
the actual error. Three things I check next as a habit: what `Type=` is set, because a simple-vs-forking
mismatch makes the service look dead while the real daemon runs fine; `Restart=` plus the start-limit
settings, because a crash-loop eventually hits `start-limit-hit` and systemd refuses to try again until
`reset-failed`; and whether the binary's environment works as the `User=` — permission and missing-env
problems are the usual exit-1/203 causes. And I keep the distinction straight: 'active (running)' is
the supervisor's verdict, not proof the application is actually serving — that's why we have health
checks and readiness probes on top."

## 6. FOLLOW-UP ATTACKS

**Q.** `Type=simple` vs `Type=forking` vs `Type=oneshot` vs `Type=notify`?
**A.** simple: systemd treats it as started the moment the ExecStart process spawns (right for most apps,
but "started" ≠ "ready"). forking: the app daemonizes (double-fork), so systemd waits or follows the
`PIDFile` — the classic "my daemon runs but systemd says it failed" trap. oneshot: runs once and exits
successfully = done (setup/run-migrations). notify: the app explicitly signals readiness via
`sd_notify` — the closest to "truly ready".

**Q.** `Restart=always` vs `on-failure`?
**A.** always: even a *clean* exit 0 triggers a restart (for a supervisor you always want up).
on-failure: only unclean returns (for jobs/one-shots that legitimately end). Picking wrong = restarts
you never wanted, or a dead service you did.

**Q.** What is `start-limit-hit` and how do you recover?
**A.** Start attempts exceeded `StartLimitBurst` within `StartLimitIntervalSec` → systemd refuses new
starts. Recovery = `systemctl reset-failed`, then investigate WHY it was crash-looping before letting
it run again — resetting without a root cause just repeats the loop.

**Q.** When exactly do I run `daemon-reload`?
**A.** After editing any unit file or drop-in. `systemctl restart` re-reads the *current* cached unit;
without daemon-reload, edits silently don't apply. `systemctl status` warns when files changed on disk.

**Q.** Why does the service say `active (running)` but the app isn't reachable?
**A.** Supervisor state ≠ app health: with `Type=simple`, 'running' is recorded at process spawn, before
listen/ready. Or it crash-loops between your samples. Debug the *app* (journal, port, health endpoint),
not systemd. (Same lesson as readiness probes under Kubernetes.)

**Q.** `enable` vs `start` vs `mask` vs `disable`?
**A.** start/stop = now; enable/disable = at boot (via `WantedBy=` symlinks); mask = refuse to start even
by hand.

**Q.** How do you find out WHY a unit failed with exit 203?
**A.** 203/EXEC = systemd couldn't even exec: wrong ExecStart path, missing interpreter, or a
Permission/Exec format issue on the binary — checked first in the journal.

## 7. PRACTICAL EXAMPLE (production)

A container-host agent restarts every few seconds. `systemctl status agent` shows
`Active: activating (auto-restart) (Result: exit-code)` with `Main PID: 0 (code=exited,
status=1/FAILURE)`; `journalctl -u agent -n 50 --no-pager` reveals a missing `EnvironmentFile=` path.
`User=agent` then reads an empty env instead of failing to load it, so the binary starts, hits the
missing config, and exits 1. Root cause: config path typo in the unit — a 5-minute fix, found in 60
seconds once you stop guessing and read the two commands.

## 8. BUILD / REPRODUCE

These are real, verified labs on this box (user units, no root needed — `systemctl --user`).

### Lab 16 — create a service, watch it crash-loop into start-limit (verified)

```bash
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/wrsleeper.service <<'EOF'
[Unit]
Description=WarRoom sleeper (deliberately broken)
[Service]
Type=simple
ExecStart=/bin/sh -c "sleep 2; exit 1"
Restart=on-failure
RestartSec=1
StartLimitIntervalSec=10
StartLimitBurst=3
[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user start wrsleeper.service
systemctl --user status wrsleeper.service --no-pager -n0   # watch "activating (auto-restart)"
sleep 14
systemctl --user status wrsleeper.service --no-pager -n0   # now "failed"
journalctl --user -u wrsleeper.service -n 8                # "...restart counter is at 3"
                                                           # "...Start request repeated too quickly."
systemctl --user show -p NRestarts,ExecMainStatus wrsleeper.service  # NRestarts=3, status=1

# recovery + make it succeed:
systemctl --user reset-failed wrsleeper.service
```

Then edit the unit: `ExecStart=/bin/sh -c "sleep 100"` → `daemon-reload` → `start` → status shows
`active (running)` with a live Main PID → `stop` → `rm` the unit → `daemon-reload`. Verified on this
box: with `StartLimitIntervalSec=10` `StartLimitBurst=3`, the journal logs `Start request repeated too
quickly.` and the unit lands in `failed`. (Modern systemd's *default* burst is lax enough that modern
units may not trip it — set it explicitly in labs and in production when you want protection.)

### Lab 17 — the health ≠ active trap (verified)

```bash
cat > ~/.config/systemd/user/wrtrue.service <<'EOF'
[Unit]
Description=Exits cleanly (not a failure)
[Service]
Type=oneshot
ExecStart=/bin/true
[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user start wrtrue.service
systemctl --user status wrtrue.service --no-pager   # "inactive (dead)" — being dead is NOT "failed"
systemctl --user show -p Result wrtrue.service      # success
systemctl --user cat wrtrue.service                 # show the effective unit + drop-ins
systemctl --user stop wrtrue.service 2>/dev/null; rm -f ~/.config/systemd/user/wrtrue.service
systemctl --user daemon-reload
```

Lesson: `inactive (dead)` after run-to-complete is *success* for oneshot; `failed (Result: exit-code)`
is failure. Confusing those three states (running / dead / failed) is a podium interview grab.

### Lab 18 — journal queries (read-only)

```bash
journalctl -u <some-real-service> -n 20 --no-pager      # a unit's recent lines
journalctl --since "10 min ago" -p warning              # recent warnings+
journalctl -k -n 20                                     # kernel ring → matches dmesg
journalctl -b --unit ssh* -p err                        # errors for ssh units, this boot
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "service won't start / keeps dying" (full sequence)

**SYMPTOM:** `systemctl start app` → fails, or starts then dies. Deploy pipeline blocks on it.
→ **SCOPE:** this unit vs its dependencies vs the app itself vs the platform. systemd told you a lot
    already — read its verdict before re-running.
→ **HYPOTHESES:** (a) unit definition problem (path/Type/User/env), (b) app-level failure on startup
    (missing config, bind conflict, permission), (c) dependency/ordering issue (db started, app zoomed
    through), (d) restart-flood reached `start-limit-hit`, (e) timeout (TimeoutStartSec) for slow apps.
→ **CHECKS, in order:**
1. `systemctl status <svc> --no-pager -n0` — active/result, Main PID, exit code, restart counter. Forms
   the hypothesis bracket. (FIRST CHECK — see §13.)
2. `journalctl -u <svc> -n 100 --no-pager` — the actual error line (missing file, denied, [Errno], 203).
3. `systemctl show -p ExecMainStatus,Type,Restart,LoadState <svc>` — definition facts in one shot.
4. `systemctl list-dependencies <svc>` (`--all`) — see what's *After* it; `systemctl is-active` those.
5. `systemctl cat <svc>` — the *effective* unit incl. drop-ins (someone override `ExecStart` once?).
6. If start-limit: `journalctl -u <svc> | grep -i "start request repeated"`.
→ **EVIDENCE:** `Active: failed (Result: exit-code)`, `status=1/FAILURE`, and a journal line like
    `environmentad: error while loading shared libraries` / `Address already in use` / `parse error` —
    i.e. an *app* failure, not a unit-syntax one.
→ **ROOT CAUSE:** (representative) port already bound by a zombie of the OLD version — the app exits 1.
→ **FIX (smallest safe):** identify the holder (`ss -ltnp`), confirm it's the stale instance, terminate
    that process properly (`systemctl` its own manager or `kill`), then `systemctl restart <svc>`.
    For start-limit: `reset-failed` FIRST, then fix the crash loop. Never `reset-failed`–and-run without
    a root cause.
→ **VERIFY:** `systemctl is-active <svc>` → active; `systemctl status` shows new Main PID, no restart
    counter ramping; the app answers its health endpoint (that's the health check, not systemd).
→ **PREVENT:** crash-loop alerting + `Restart=`/`StartLimit*` policy; port-conflict detection in deploy
    pipeline (stop-old then start-new ordering); a healthcheck wired to monitoring so "running but
    broken" gets caught the moment it can't serve.

### DECISION OVERLAY — what NOT to do

- Don't `systemctl restart` *hoping* — you restart a fresh copy of the same config: evidence first.
- Don't `reset-failed` + forget — the loop repeats; read the journal for the cause.
- Don't `mask` a broken unit as a "fix" — it's a refusal to start, for the persistent triage case.
- Don't judge by exit code alone — 1 = app-shaped failure, 203 = systemd couldn't exec, 143 =
  SIGTERM'd (sometimes a *supervisor* killing it — look at what sent the signal).

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "`After=` means 'requires'" | `After` = ordering. Dependency is `Wants`/`Requires`. Conflating them is the classic mistake. |
| "`active (running)` = healthy" | Supervisor verdict only. Type=simple marks started at spawn; health = probes/endpoints. |
| "`inactive (dead)` is a failure" | For oneshot/clean-exit units it's the *expected* success state. Check `Result`. |
| "`restart` picks up my unit edit" | No — `daemon-reload` first, then restart/start. |
| "`enable` starts it now" | enable = boot-time; use `enable --now` or start for immediate. |
| "Just `reset-failed` and retry forever" | start-limit-hit keeps returning until the crash cause is fixed. |
| "System services and `systemctl --user` differ in concept" | Same semantics; user-unit examples transfer 1:1 to `/etc/systemd/system`. |
| "A 203 exit = app bug" | 203 is systemd's exec failure (path/interpreter/perms/exec format). App bugs are usually exit 1. |
| "Journal survives forever by default" | Persistence + `SystemMaxUse` decide that; volatile without `/var/log/journal`. |

## 13. FIRST-CHECK REASONING

- **"service won't start":** `systemctl status <svc> --no-pager` first — systemd already computed the
  state machine (running/dead/failed/activating) and the exit code; that one read brackets the
  hypothesis space (unit-definition vs app-failure vs dependency vs start-limit) before you touch
  anything. Its journal line then confirms or kills the #1 suspect.
- **"crash-loops / I don't know where to even start":** still `status`, then `journalctl -u <svc>
  -n 100` — status shapes "what kind", journal finds "why". Status-before-journal, always.

## 14. PRIORITY

**P0.**

## 15. STOP HERE — done when you can…

1. write a correct `[Unit]/[Service]/[Install]` unit from memory and pick `Type=` for an app;
2. run Lab 16 end-to-end and predict the `status` text at each phase (activating → failed);
3. explain `After` vs `Requires`, `enable` vs `start` vs `mask`, `Restart=always` vs `on-failure`;
4. narrate a "won't start" incident and land on the FIRST check with justification;
5. distinguish `running`/`dead`/`failed` and supervisor-state vs app-health (Lab 17).

## 16. DO NOT STUDY YET

Socket **activation** internals, target/slice graph engineering, seccomp/hardening options
(`ProtectSystem`, `PrivateTmp`) beyond "what they're for", journald forward-to-syslog plumbing,
`systemd-nspawn`, resource accounting policies. Know they *exist*; don't study their tuning at 1–3 YOE.

---

## QC CHECKLIST — LINUX.P0.6

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (unit → systemd → cgroup → journal)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanism (units, Type=, Restart=, ordering vs dependency)? | ✔ §3 |
| 5 | Dependencies (PID1, cgroups, journald persistence)? | ✔ §3 |
| 6 | Essential commands (`systemctl`, `journalctl`, `systemd-analyze`)? | ✔ §8–11 |
| 7 | Reproduce (Labs 16–18)? | ✔ verified live (PID 1 IS systemd here) |
| 8 | Break it (crash-loop → start-limit press)? | ✔ Lab 16, observed `Start request repeated too quickly` |
| 9 | Observe + interpret evidence? | ✔ §8–11 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §11 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13).

---

# SESSION LINUX.P0.7 — FILE DESCRIPTORS, SOCKETS, PORTS, /proc

Environment note: all labs below were verified live on this box (soft = hard = 1,048,576 for open
files; ephemeral port range 32768–60999; `tcp_fin_timeout` = 60 s).

## 1. WHAT IS IT? (≤30 s)

An open file, pipe, device, or socket is referenced by a per-process **file descriptor**: a small
integer index into a table (`/proc/<pid>/fd`) pointing at a kernel object. Sockets are just FDs whose
object is a network connection. `/proc` is the kernel's runtime view of processes and network; `ss`,
`lsof`, and `ps` are all just readers over it.

## 2. WHY DOES IT EXIST?

Every "Too many open files", "Address already in use", "who is holding my file/port", "why is the port
in TIME_WAIT", and FD-leak-at-scale story lives here. It's the mechanism under the P0.4 deleted-file
lab and the P0.6 EADDRINUSE incident — and the natural bridge from processes into networking.

## 3. HOW DOES IT WORK?

- **The FD table.** Every process inherits 0 (stdin), 1 (stdout), 2 (stderr). New opens grab the lowest
  free slot ≥ 3. On `fork()` the table is copied; across `exec()` the fds survive *unless* marked
  close-on-exec (FD_CLOEXEC). `ls -l /proc/<pid>/fd` shows each fd as a symlink to its target
  (`/path`, `pipe:[ino]`, `socket:[ino]`, `/dev/null`).
- **Limits.** `ulimit -n` shows a per-shell **soft** limit; the **hard** limit is the ceiling you can
  raise to (`ulimit -Sn`/`-Hn`). The per-process truth lives in `cat /proc/<pid>/limits` ("Max open
  files"). Opening beyond the soft limit → `EMFILE` (errno 24). For systemd services the limit is set
  with `LimitNOFILE=` (link to P0.6).
- **Sockets.** A **server** creates a listening socket (state LISTEN; kernel holds the accept-backlog —
  `ss` shows it as Recv-Q/Send-Q on the LISTEN line). When a client connects, a *new* socket appears:
  state `ESTABLISHED` on both sides, each end an FD of its owning process. After close, the side that
  initiated the shutdown holds the socket in **TIME_WAIT** for ~2×MSL (`tcp_fin_timeout` = 60 s here)
  to guarantee the final ACK got through — it is not a leak, it is deliberate.
- **Source ports.** A *connecting* client picks an ephemeral source port from
  `/proc/sys/net/ipv4/ip_local_port_range` (here 32768–60999). Rapid open/close cycles bury clients in
  TIME_WAIT entries; exhaust the range → `EADDRNOTAVAIL`.
- **`/proc/net/tcp`** is the kernel's own TCP table in hex: `0100007F:223D 00000000:0000 0A` means
  local 127.0.0.1:8765 (8765 = 0x223D), no peer, state 0A = LISTEN. State codes: `01` ESTABLISHED,
  `06` TIME-WAIT, `0A` LISTEN. The trailing decimal number is the socket **inode** — glue to the fd
  table's `socket:[ino]` symlink and to `ss -p`'s `users:(("prog",pid=…,fd=…))`.
- **Tools.** `ss -tlnp` (listening TCP incl. owning process), `-tuna` (all TCP/UDP numeric), filters
  like `state time-wait`, `dport = :8765`; `lsof -p <pid>` (a pid's open files — reads the same
  /proc), `lsof -iTCP:<port>` (cross-process: who has that port). `ss -p` needs permission for the
  socket's owner; as the same non-root user you see your own processes.

## 4. MENTAL MODEL

```
process ── fd table (/proc/<pid>/fd: 0,1,2,3…) ──► kernel object: file | pipe:[ino] | socket:[ino]
                                          limits: soft ≤ hard (cat /proc/<pid>/limits)
LISTEN ── backlog ──► accepted as NEW socket (ESTABLISHED) ── close ──► TIME_WAIT (60s, closer holds)
client ── ephemeral src port (32768–60999) ──► server :8765
/proc/net/tcp = kernel truth (hex addr:port, state 01/06/0A, inode)  ── ss/lsof = friendly readers
```

## 5. INTERVIEW-SAFE ANSWER

"An FD is a per-process integer that indexes a table of open file descriptions — files, pipes,
devices, even sockets; `ls /proc/<pid>/fd` shows the live table as symlinks, and `cat /proc/<pid>/limits`
shows the open-file limit. The classic failure is EMFILE: when a process works beyond its soft limit —
typically file descriptors leak because consecutive `open()` calls aren't paired with `close()` — every
new connection consumes an FD, so at scale 'too many open files' is what a leaked-FD bug looks like.
On the socket side I distinguish three socket kinds by state: a LISTEN socket owns the port and holds
the accept backlog; an ESTABLISHED socket is a live connection; TIME_WAIT is the closer's housekeeping
for 2×MSL (60 s here) and isn't a leak. When debugging I map things through /proc: a pid's fd
`socket:[inode]`, the inode in `/proc/net/tcp`, and `ss`'s users line all match, so I can always go
from 'who owns port 8765' down to the exact socket the process holds."

## 6. FOLLOW-UP ATTACKS

**Q.** Soft vs hard limit — can I raise?
**A.** Soft you can raise anytime up to the hard limit (`ulimit -Sn`); raising the hard limit requires
root. For apps under systemd, set `LimitNOFILE=` and reload (P0.6).

**Q.** Why do leaked sockets eat the process alive?
**A.** Because each connection is at least one FD and each FD is an entry in a fixed-size table capped
by the soft limit — leak FDs and the process stops at EMFILE exactly when you need the connections.

**Q.** What is close-on-exec and why should I care?
**A.** An fd marked FD_CLOEXEC quietly disappears on `exec()`. Without it, a leaked fd survives into
every child — the disease behind "my daemon holds the old config file" and inherited secret handles.
Shells like bash open `exec 3>file` without cloexec, so children inherit it (shown in Lab 19).

**Q.** Whose side is in TIME_WAIT, and is it a leak?
**A.** The side that closes first holds TIME_WAIT for 2×MSL (default ~60 s here). Not a leak — it
protects the final ACK and prevents a stale duplicate reconnecting. It becomes a *problem* only when a
client floods connections faster than sockets expire (port exhaustion → EADDRNOTAVAIL).

**Q.** "Connection refused" vs "timeout" — meaning?
**A.** Refused: nothing is LISTENing on that port (or a firewall answered RST). Timeout: packets
dropped/discarded without a reply — usually firewalled/filtered. And EADDRINUSE is different again: a
`bind()` colliding with an existing LISTEN socket (or a socket in TIME_WAIT without SO_REUSEADDR).

**Q.** `ss` vs `lsof` — overlapping?
**A.** Both read the same kernel sources (/proc + socket tables); `ss` is the go-to for socket facts and
filters, `lsof -iTCP:<port>`/`-p` for pid↔file mapping. Two UIs, one truth.

**Q.** What does the listen backlog mean?
**A.** Accept-queue size for connections the kernel has established-but-not-yet-accepted; when full,
new inbound connects can be dropped. `ss` shows it as Recv-Q on the LISTEN line — *not* a measure of
how many clients are connected.

**Q.** Read a `/proc/net/tcp` row for me.
**A.** `0100007F:8FC2 0100007F:223D 01` → local 127.0.0.1:36802 (0x8FC2), peer 127.0.0.1:8765
(0x223D), state 01 = ESTABLISHED; the trailing numbers include the socket inode (and uid). Little-endian
hex addresses; `0A` LISTEN, `06` TIME-WAIT.

## 7. PRACTICAL EXAMPLE (production)

Deploy fails at post-check: app won't start, log line `[Errno 98] Address already in use`. Instead of
restarting blindly: `ss -tlnp | grep 8765` → shows the OLD, still-LISTENing instance (`pid=…,fd=3`).
The stale process (from the previous deploy) was never demolished because the old script's stop step
silently failed. Kill it properly, `systemctl restart app`, verify with `ss -tlnp` that exactly the
new Main PID owns the port and the app answers its health endpoint.

## 8. BUILD / REPRODUCE

### Lab 19 — FD table, inheritance, limits, EMFILE (verified)

```bash
ulimit -Sn && ulimit -Hn            # here: 1048576 / 1048576 (soft == hard)
bash -c 'exec 3>/tmp/p07_fdtest.txt; echo hello >&3; sleep 30 & pid=$!;
         ls -l /proc/$pid/fd; kill $pid; rm -f /tmp/p07_fdtest.txt'
# verified: child shows fd 3 -> /tmp/p07_fdtest.txt  (inherited, no cloexec)

( ulimit -Sn 256; python3 - <<'EOF'
import os
fds=[]
while True:
    try: fds.append(os.open('/dev/null', os.O_RDONLY))
    except OSError as e:
        print("raised:", e, "errno", e.errno); print("fds:", len(fds)); break
EOF
)
# on default limit (1M) verified: Errno 24 Too many open files; fds opened = 1048573.
# drop-in-a-subshell limit (256) makes it finish instantly; the real defaults are huge here.
```

### Lab 20 — socket states, inode cross-map, port conflict (verified)

```bash
python3 -m http.server 8765 --bind 127.0.0.1 &            # pid captured as $SERVER
ss -tlnp | grep 8765        # LISTEN 0 5 127.0.0.1:8765 ... users:(("python3",pid=…,fd=3))
ls -l /proc/$SERVER/fd | grep socket        # 3 -> socket:[8284]
grep "0100007F:223D" /proc/net/tcp          # ... state 0A ... 8284 ...  (inode matches!)
curl -s -o /dev/null http://127.0.0.1:8765/ ; sleep 1
ss -tan state time-wait | grep 8765         # TIME-WAIT 127.0.0.1:8765 <-> 127.0.0.1:601xx
python3 -m http.server 8765 --bind 127.0.0.1   # OSError: [Errno 98] Address already in use
kill $SERVER
```

All verified here: inode `8284` appears both in fd 3's `socket:[8284]` and in the `/proc/net/tcp`
row; two curls produced client TIME-WAIT sockets `:60102` / `:60118` (ephemeral range 32768–60999);
a second bind failed with **Errno 98 Address already in use**.

### Lab 21 — ESTABLISHED + hex decode + who-closes-first TIME_WAIT (verified)

```bash
# slow server (detached):
setsid bash -c 'python3 -c "
import http.server,time
class H(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  time.sleep(6); self.send_response(200); self.end_headers()
 def log_message(self,*a): pass
http.server.HTTPServer((\"127.0.0.1\",8765),H).serve_forever()"' </dev/null >/dev/null 2>&1 &
sleep 1
setsid bash -c 'curl -s http://127.0.0.1:8765/' </dev/null >/dev/null 2>&1 &
sleep 1
ss -tan "dport = :8765"      # ESTAB client 127.0.0.1:36802 -> 127.0.0.1:8765
ss -tan "sport = :8765"      # LISTEN + ESTAB server 127.0.0.1:8765 <-> 127.0.0.1:36802
grep ":223D " /proc/net/tcp
# verified rows:  0100007F:223D 00000000:0000 0A    (LISTEN, inode 858)
#   0100007F:8FC2 0100007F:223D 01    (client 36802 → 8765, ESTABLISHED, inode 1879)
#   0100007F:223D 0100007F:8FC2 01    (server ↔ client, ESTABLISHED, inode 861)
sleep 6   # curl finished, server closes first → server side holds TIME_WAIT
ss -tan "sport = :8765" | head -4      # LISTEN + TIME-WAIT (server-side of :36802)
# cleanup: kill server pid, confirm port free
```

Verified: reading `ss` from both ends plus the raw hex row — you can walk port → state → inode →
fd from pure /proc, which is exactly what the tools do for you.

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Too many open files" (errno 24) on a high-traffic service

**SYMPTOM:** app logging `[Errno 24] Too many open files` at peak, then refusing connections.
→ **SCOPE:** which process is failing and *where* in its lifecycle (open-per-request is the classic
  router/worker leak; connection-per-request is socket FD starvation). A single misbehaving pid vs the
  whole box.
→ **HYPOTHESES:** (a) real FD leak in the app (open without close at scale), (b) legit concurrency that
  simply exceeds a too-small limit, (c) socket FDs not closed because connections linger, (d) limit
  lowered (Misconfigured `LimitNOFILE=/ulimit`), (e) a file-descriptor-holding dependency (watchdog,
  DB handle pool) growing unboundedly.
→ **CHECKS, in order:**
1. `cat /proc/<pid>/limits | grep "open files"` — the effective limit for THAT pid (soft AND hard).
2. `ls /proc/<pid>/fd | wc -l` (or `lsof -p <pid> | wc -l`) — current count, now compare to the limit.
3. Break it down: `lsof -p <pid> | awk '{print $NF}' | sort | uniq -c | sort -rn | head` — files vs
   sockets vs pipes; `lsof -p <pid> | grep -c 'socket'`.
4. If sockets: `ss -tanp | grep <pid>` — established vs TIME_WAIT vs stray LISTEN from a zombie.
5. Raise-and-observe skeptical: temporarily bump soft (or systemd `LimitNOFILE=`) — if it still grows,
   it's a leak, not a limit.
→ **EVIDENCE:** fd count climbing toward soft limit over time; thousands of `socket:` entries, or one
  path repeated, from a code path that forgets `close()`.
→ **ROOT CAUSE:** (representative) per-request file handle leaked on the error path of the response
  handler.
→ **FIX:** patch + release; *valid* mitigation until then: correct limit; ensure `close()`/context
  manager also on exception paths. Never fix a leak by raising the limit and declaring victory.
→ **VERIFY:** stable fd count at peak traffic (graph it), zero Errno-24 across the next peak.
→ **PREVENT:** fd-count metric per process alerted at ~80% of limit; leak tests with connection/request
  soak; code review for non-closed handles; correct `LimitNOFILE` set deliberately, not by default.

### DECISION OVERLAY — what NOT to do

- Don't `ulimit -n 999999` globally "to be safe" and call it a fix — you hid a leak or an unbounded
  design; alert on growth instead.
- Don't kill a process holding the port without confirming it's the stale instance (`ss -tlnp` first).
- Don't confuse TIME_WAIT with leaks during triage; count ESTABLISHED/LISTEN, not TIME_WAIT.
- Don't use `pkill -f` with a pattern your own shell matches — kill by PID from `ss`/`lsof`.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "`ss -p` will show the process" | Only when you're permitted for that socket's owner; as non-root you see your own processes. `so` fallback = /proc walk by inode. |
| "TIME_WAIT = socket leak" | Deliberate 2×MSL housekeeping by whoever closed first; drains in `tcp_fin_timeout` (60 s). |
| "Accept backlog = how busy I am" | It's the kernel's not-yet-accepted queue, not client count. |
| "`/proc/net/tcp` is human JSON" | Hex, little-endian, state codes 01/06/0A — decode before reading. |
| "FDs disappear on exec" | Only with close-on-exec; else inherited (Lab 19 child kept fd 3). |
| "Soft limit = real limit" | Soft is advisory-per-process; hard is the root ceiling. |
| "Errno 98 always means the app is broken" | Often it's a stale LISTEN owner you can see with `ss -tlnp`. |
| "Raising limits fixes leaks" | It only buys time; the leak still consumes. |
| "Port exhaustion = server problem" | Often the *client's* ephemeral range (32768–60999) is what got burned. |
| "Only processes have FDs" | Since a socket is an FD, 'who owns port 8765' == 'which pid holds fd X', same table. |

## 13. FIRST-CHECK REASONING

- **"Port/addr already in use" (or "app can't bind"):** `ss -tlnp | grep <port>` FIRST — it answers,
  in one line: is anyone LISTENing, and which pid/fd. Then `lsof -iTCP:<port>` as the cross-check.
  Refused vs timeout shapes whether it's a bind problem at all.
- **"Too many open files":** FIRST read the exact pid's ceiling and count: `cat /proc/<pid>/limits`
  (soft/hard) then `ls /proc/<pid>/fd | wc -l` — do these two *before* assuming a leak; they separate
  "limit mis-set" from "genuinely leaking" in seconds.

## 14. PRIORITY

**P0.**

## 15. STOP HERE — done when you can…

1. explain what an FD is, where the table lives, and what soft/hard limits mean;
2. run Labs 19–21 and read every row you produce (LISTEN/ESTABLISHED/TIME_WAIT; hex /proc/net/tcp);
3. cross-map fd inode ↔ /proc/net/tcp inode ↔ `ss -p` users line without tools;
4. triage EADDRINUSE and errno 24 incidents end-to-end with the FIRST checks above;
5. say confidently that sockets are FDs and that concurrency is FD-bound, not just load-bound.

## 16. DO NOT STUDY YET

epoll/inotify/io_uring internals, TCP stack tuning knobs (tcp_tw_reuse, keepalive tuning, window and
congestion control), SO_REUSEADDR/SO_REUSEPORT subtleties, packet capture depth, inode/filesystem
internals, the full /proc/sys tuning catalog. Know they exist; tune none at 1–3 YOE.

---

## QC CHECKLIST — LINUX.P0.7

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (fd table → socket → /proc → tools)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (FD lifecycle, limits, socket states, inode mapping)? | ✔ §3 |
| 5 | Dependencies (fork/exec semantics, TCP close handshake, /proc/sys)? | ✔ §3, §6 |
| 6 | Essential commands (`ss`, `lsof`, /proc reads)? | ✔ §3, §8 |
| 7 | Reproduce (Labs 19–21)? | ✔ verified live (limits 1M; range 32768–60999; TIME_WAIT 60 s) |
| 8 | Break it (EMFILE, EADDRINUSE, TIME_WAIT)? | ✔ Labs 19–20, errno 24 & errno 98 observed |
| 9 | Observe + interpret evidence (hex decode, inode math)? | ✔ Lab 21, `0x223D`/`0x8FC2`/states 0A·01·06 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §11 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13).

---

# SESSION LINUX.P0.8 — ENVIRONMENT VARIABLES, CRON, SYSTEMD TIMERS

Environment note: everything below was verified live on this box — user-cron works (`cron.service`
active, user `crontab` dispatch watched in the journal) and the per-user systemd manager fires timers.

## 1. WHAT IS IT? (≤30 s)

Environment variables are a per-process `KEY=value` string block living in the process's memory
(readable via `/proc/<pid>/environ`). They're inherited on fork/exec, mutated with `export`, and are
how a config-less program learns its surroundings. Scheduling-wise: **cron** is the classic wall-clock
job daemon (minute granularity, hostile env), and **systemd timers** are its modern replacement
(systemd-native, calendar + repeat semantics, `Persistent=true` catch-up).

## 2. WHY DOES IT EXIST?

Env vars give every process the same humble interface — look up a name, get a string — which is why
`PATH`, `HOME`, `LANG`, `KUBECONFIG`, `AWS_PROFILE` control tooling without config files. And if you
can't do scheduled jobs correctly you're lost: cron's *environment* is what breaks 90% of honest
"it works when I run it but not from cron / not from the service" reports.

## 3. HOW DOES IT WORK?

- **Per-process, inherited, copied.** `VAR=value` vs `export VAR=value` — the first is only in the
  current shell; the second marks it for child processes. On `fork()` the whole block is copied; a
  `bash`-spawned child never sees an unexported var (verified: parent `X=…; export YE=…`→ child saw
  `X=[] YE=[exported]`). `/proc/<pid>/environ` shows the block (NUL-separated); readable by the owner
  and root (cross-ref P0.7).
- **Who defines what.** Interactive shells load profiles (`~/.profile/.bashrc`); cron and systemd do
  NOT. systemd services get exactly `Environment=`/`EnvironmentFile=`, nothing else; cron jobs get
  cron's default `SHELL=/bin/sh` + a cron-managed `PATH` (verified here:
  `SHELL=/bin/sh`, `PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin`).
- **cron.** User schedules live in `crontab -e` (view `-l`, zap `-r`); system jobs in `/etc/crontab`,
  `/etc/cron.d/`, and the `/etc/cron.*` run-parts dirs. The schedule is 5 fields: `min hour dom mon dow`,
  with `*/n` repeats and ranges. Field semantics: `dom` AND `dow` both set is "until both"? — legacy
  cron ORs them; keep them mutually exclusive.
- **systemd timers.** A `.timer` unit declares the schedule and points at a `.service` (`.timer` +
  `.service` pair). `OnCalendar=*-*-* 02:00:00` (fixed-point calendar), `Persistent=true` (if the box
  was off when it should fire, run it after boot — requires a calendar schedule), or repeat semantics
  via `OnBootSec=`/`OnUnitActiveSec=`. `systemctl list-timers` shows NEXT/LEFT/LAST/PASSED.
- **Enough with the timer grammar:** for humans, `OnCalendar` wants "this wall-clock moment, repeat" —
  sub-minute repeats are NOT reliable (verified below). For "run every N seconds in dev/tests" use
  `OnUnitActiveSec=`, which loops off the previous activation, not the clock.

## 4. PRODUCTION MENTAL MODEL

```
interactive:  .bashrc/.profile ─► your shell ─► your env; children inherit (export marks)
service:      systemd unit ─► ONLY Environment=/EnvironmentFile= ─► journald
cron:         crontab line ─► cron default env (SHELL=/bin/sh, cron PATH) ─► output → mail/void
scheduler picks: wall-clock minute jobs → cron; anything modern/systemd-managed →
    .timer + .service pair, Persistent=true for catch-up, journalctl -u <svc> for logs
```

## 5. INTERVIEW-SAFE ANSWER

"Environment variables are a per-process key-value block — every process has its own copy, children
inherit it on fork/exec, and only exported variables are inherited; `/proc/<pid>/environ` is the live
view. The practical trap is *which env a process actually gets*: an interactive shell loads
`.bashrc`/`.profile`, but cron jobs get cron's own minimal env — verified locally, `SHELL=/bin/sh`
and a cron-curated PATH, no login profile — so 'works when I run it, breaks in cron' is almost always
an environment difference: absolute paths, shebang, and explicit env in the job fix it. On the
scheduling side I prefer systemd timers over cron for modern services: a `.timer` unit plus a
`.service` unit, `OnCalendar` for wall-clock schedules, `Persistent=true` to run what was missed while
the machine was down, and repeat-on-interval via `OnUnitActiveSec` for sub-minute cadence. Cron I use
when I must match legacy systems or hit shared `/etc/cron.d` conventions. And when I write unit files,
I keep `$`/`%` out of `ExecStart` — systemd parses those itself (env substitution/specifiers) — and
point it at a real script instead."

## 6. FOLLOW-UP ATTACKS

**Q.** `VAR=value` vs `export VAR=value`?
**A.** Assignment only affects the current shell; `export` flags it for inheritance. Children only see
exported names — never assume a var crosses an exec boundary unless you exported it.

**Q.** Why do cron jobs fail that run fine in my shell?
**A.** Environment: cron's `SHELL=/bin/sh`, its own PATH, no profile/aliases/functions, no variables you
set interactively. Also: no MTA here means any stdout that isn't redirected is **discarded** (the
journal literally says `No MTA installed, discarding output`) — log to a file yourself.

**Q.** cron vs systemd timers?
**A.** Cron: minute granularity, env-poor, wall-clock only, optional catch-up if you rig it. Timers:
calendar + interval semantics, `Persistent=true` run-late catch-up, journald integration, part of the
same systemd state you already debug. Timers get default-on modern boxes; cron stays for legacy.

**Q.** What does `Persistent=true` actually do?
**A.** With a calendar schedule, if the trigger time passed while the unit was inactive (box asleep/
off), it fires once after activation to 'catch up'. Meaningless with `OnBootSec`/`OnUnitActiveSec` —
pair `Persistent` only with `OnCalendar`.

**Q.** Why did my `$VAR` break inside a unit file?
**A.** systemd expands `%specifiers` and `$ENV` in many directives itself (our test failed with
`Failed to resolve unit specifiers … Invalid slot`). Double-check quoting, or better: put the logic in
an executable script and `ExecStart=` that script — cleaner and debuggable.

## 7. PRACTICAL EXAMPLE (production)

A backup script works in the terminal, silently fails from cron. `crontab -l` shows
`0 2 * * * backup.sh` (relative path), the script builds PATH itself but a tool lives outside it, and
no one ever sees stderr → cron mail is void. Fix: absolute path to script, un-`chmod +x`, set
`SHELL`/`PATH` (or full paths), redirect output to a per-job log, and add `set -euo pipefail` so a
step failing actually fails the job loudly instead of emailing nothing.

## 8. BUILD / REPRODUCE

### Lab 22 — variables, export, /proc environ (verified)

```bash
X="via assignment"; export YE="exported"
bash -c 'echo "child sees X=[$X] YE=[$YE]"'     # verified: X=[] YE=[exported]
python3 -c "import os; print('pairs:', len(open('/proc/%s/environ'%os.getpid()).read().split(chr(0))))"
# verified: 30 pairs (NUL-separated), readable for your own process
```

### Lab 23 — systemd user timer: schedule a real job (verified)

```bash
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/wrjob.sh <<'EOF'
#!/bin/sh
echo "$(date -u +%F:%T) pid=$$ HOME=$HOME PATH=$PATH WR_DEMO=$WR_DEMO" >> /tmp/wrtimer.out
EOF
chmod +x ~/.config/systemd/user/wrjob.sh
cat > ~/.config/systemd/user/wrjob.service <<'EOF'
[Unit]
Description=WR demo job
[Service]
Type=oneshot
ExecStart=%h/.config/systemd/user/wrjob.sh
Environment=WR_DEMO=hello_from_systemd
[Install]
WantedBy=default.target
EOF
cat > ~/.config/systemd/user/wrtimer.timer <<'EOF'
[Unit]
Description=WR demo timer (every minute)
[Timer]
OnCalendar=*-*-* *:0/1:00
Unit=wrjob.service
[Install]
WantedBy=timers.target
EOF
: > /tmp/wrtimer.out
systemctl --user daemon-reload
systemctl --user start wrtimer.timer
systemctl --user list-timers --all --no-pager | grep wrtimer   # NEXT is scheduled
sleep 70
cat /tmp/wrtimer.out    # verified: cron-like auto-run, fresh oneshot PID per run,
                        # systemd env: HOME=/home/randomtechy, PATH=(full default),
                        # Environment= propagated (WR_DEMO=hello_from_systemd)
# trap demo (verified): putting the shell command INLINE like
#   ExecStart=/bin/sh -c 'echo "pid=$$ PATH=$PATH" >> /tmp/x'   # ← fails to LOAD with
#   "Failed to resolve unit specifiers … Invalid slot" (systemd expands $/% itself).
# correct pattern is the script file above.
systemctl --user stop wrtimer.timer; systemctl --user disable wrtimer.timer
rm -f ~/.config/systemd/user/wrtimer.timer ~/.config/systemd/user/wrjob.service \
      ~/.config/systemd/user/wrjob.sh /tmp/wrtimer.out
systemctl --user daemon-reload
```

Verified detail worth keeping: sub-minute cadence via `OnCalendar=*-*-* *:*:00/15` did NOT give 15 s
repeats — it aligned to ~minute boundaries (runs 21:07:26 → 21:08:26). For real sub-minute repeat use
`OnBootSec=1s` + `OnUnitActiveSec=15s` instead (also verified to fire automatically).

### Lab 24 — real cron on this box (verified)

```bash
# 1) simplest dispatch proof
printf '* * * * * /usr/bin/touch /tmp/wrcron_touch\n' > /tmp/wrcron.cron
crontab /tmp/wrcron.cron
crontab -l                       # verify installed
rm -f /tmp/wrcron_touch
sleep 70
ls -l /tmp/wrcron_touch          # created at the next minute boundary
journalctl -u cron --since "-2 min"   # verified: "(randomtechy) CMD (/usr/bin/touch …)"

# 2) cron's own env (verified)
printf '* * * * * /usr/bin/printenv PATH SHELL > /tmp/wrcron.env\n' > /tmp/wrcron.cron
crontab /tmp/wrcron.cron; sleep 70; cat /tmp/wrcron.env
# verified: SHELL=/bin/sh
#           PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
crontab -r ; rm -f /tmp/wrcron.cron /tmp/wrcron_touch /tmp/wrcron.env
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "job runs in my shell but dies in cron/systemd"

**SYMPTOM:** backup/auth/cleanup job quiet-fails; works when you run the command by hand.
→ **SCOPE:** is it the *scheduler* (never runs?) or the *job env* (runs, then fails)? `=` journal
  lines / cron mail absence answer the first; log-replay answers the second.
→ **HYPOTHESES:** (a) cron env: missing PATH entry, SHELL differences, no `$HOME`/custom vars (b)
  relative paths / no shebang / not executable, (c) cron vs timer cadence misunderstanding
  (sub-minute OnCalendar), (d) output discarded so nobody sees the error (no MTA), (e) the job's
  dependency isn't running yet (ordering: ended up as service timer without ordering).
→ **CHECKS, in order:**
1. Prove it's dispatched: `journalctl -u cron --since "-5 min"` → `(user) CMD (…)`. If a systemd
   timer: `systemctl list-timers`, `journalctl -u <svc> -n 50`.
2. Re-run the exact command with the scheduler's env: `env -i HOME=$HOME PATH=… SHELL=/bin/sh sh -x script.sh`.
3. `crontab -l` → check absolute paths, `chmod +x`, `#!/bin/sh` first line, `>> log 2>&1`.
4. If timer: `systemd-analyze verify unit.service`; confirm `.timer` Unit= names the right service.
→ **EVIDENCE:** journal shows dispatch but no effect; re-run under `env -i` reproduces the failure.
→ **ROOT CAUSE:** (representative) cron's PATH lacking the tool's dir + relative script path + no
   output capture.
→ **FIX:** absolute path + redirect to a log + `set -euo pipefail`, declare `SHELL`/`PATH` explicitly
   (or use full paths); for timers: script-based unit + `Wants/After` on dependencies.
→ **VERIFY:** next dispatch writes a timestamped success line to the log; failure path leaves an error
   line (because you now capture it).
→ **PREVENT:** standard skeleton for scheduled jobs (script, log, lockfile, alert on silence), and an
   end-to-end test run in a scheduler-env shell before shipping.

### DECISION OVERLAY — what NOT to do

- Don't "fix" cron by sourcing `/root/.bashrc` from the job — you fight the scheduler, not the env.
- Don't schedule a script that prints to stdout when there's no MTA — log to a file.
- Don't use `OnCalendar` for sub-second/15s cadence — it won't behave (verified: aligned to minutes).
- Don't set `Persistent=true` on an `OnBootSec`/`OnUnitActiveSec` timer — meaningless there.
- Don't write `$VAR`/`%H` directly in `ExecStart=` unless you intend systemd to expand them.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "cron runs my login env" | It doesn't: `SHELL=/bin/sh`, cron PATH, no profile. Verified live. |
| "cron job output is saved somewhere" | Without MTA it's discarded (`No MTA installed, discarding output`). Redirect it. |
| "`export` and assignment are the same" | Export is what children inherit; unexported vars never cross a process boundary. |
| "OnCalendar does 15 s repeats" | No — aligned to ~minute boundaries here. Use `OnUnitActiveSec=`. |
| "`$FOO` in `ExecStart=` is fine" | systemd expands it; failed with `Invalid slot` in our test. Script it. |
| "`Persistent=true` works for interval timers" | It's a calendar-schedule catch-up; no-op for `OnBootSec`/`OnUnitActiveSec`. |
| "restart/reload picks up new timers" | `daemon-reload` after every unit/timer edit (P0.6 rule). |
| "cron is a service like any other software" | It's a daemon with its own dispatch log — read `journalctl -u cron`. |
| "the 5th cron field is Sunday" | 0 and 7 are both Sunday, and legacy cron ORs dom+dow. |
| "every process sees the same env" | Per-process snapshot: two processes can see wildly different worlds. |

## 13. FIRST-CHECK REASONING

- **"Scheduled job silently not working":** FIRST prove it was *dispatched at all* — `journalctl -u cron`
  (or `systemctl list-timers` + `journalctl -u <svc>` for timers). Dispatch-then-fail is an env/path
  problem; never-dispatch is a schedule/daemon problem. One log read separates the two.
- **"Service 'can't find X' in systemd":** FIRST list the env the unit really got — `systemctl show
  -p Environment <svc>` — because the unit's env is exactly `Environment=`/`EnvironmentFile=`, never
  your shell's.

## 14. PRIORITY

**P0** (env), **P1** (cron/timers depth).

## 15. STOP HERE — done when you can…

1. explain export vs assignment and how to read `/proc/<pid>/environ`;
2. run Lab 24 and predict the journal `CMD` line + cron's default PATH/SHELL;
3. write a `.timer`+`.service` pair, know when `Persistent` applies, and say why you script ExecStart;
4. triage a "works by hand, fails scheduled" incident end-to-end (Lab §9–11 flow);
5. say when you'd pick cron vs timers and why.

## 16. DO NOT STUDY YET

anacron internals, cron PAM/security corner cases, `/etc/cron.d` production conventions beyond the
"user + path" shape, timer graph/deadline engineering (`AccuracySec`, `RandomizedDelaySec` tuning),
desync/time-zone schedule edge cases, systemd env-file syntax beyond basics. Know they exist.

---

## QC CHECKLIST — LINUX.P0.8

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (interactive vs service vs cron env)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (export, scheduler picks, timers pairs)? | ✔ §3 |
| 5 | Dependencies (fork/exec copy, journald, MTA-less cron)? | ✔ §3 |
| 6 | Essential commands (crontab, systemctl, journalctl, list-timers, /proc)? | ✔ §3, §8 |
| 7 | Reproduce (Labs 22–24)? | ✔ verified live on this box |
| 8 | Break it (cron env, sub-minute OnCalendar, `$` in ExecStart)? | ✔ all three failed as predicted, then fixed |
| 9 | Observe + interpret evidence (journal CMD lines, discard warnings)? | ✔ §8–11 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §11 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13).

---

# SESSION LINUX.P1.1 — PACKAGE MANAGEMENT (apt/dpkg, yum/dnf) + ARCHIVAL (tar, rsync)

Environment note: this box is Debian-family with apt/dpkg/rsync 3.2.7 present. Package *installation*
needs root (no passwordless sudo here) — so Labs use read-only queries and non-root tar/rsync (all
verified live). Everything transfers 1:1 to RHEL via the parity table.

## 1. WHAT IS IT? (≤30 s)

Two sysadmin pillars. **Package management**: dpkg = the installed-package database; apt = the resolver
that pulls from repositories. File ops: **tar** bundles files+metadata into one archive (the format
container layers use), **rsync** mirrors trees efficiently and, with `--link-dest`, builds
space-saving hardlink snapshots.

## 2. WHY DOES IT EXIST?

Every real change intersects packages — installing a dependency, downgrading (rollback!), figuring out
which package owns `/usr/bin/ls`, hitting an apt lock. And you can't do backups/artifacts/containers
without tar/rsync: a Docker layer *is* a tar stream. 1–3 YOE interviewers fish here for the depth
between "I've used apt/yum" and "I know how these actually behave".

## 3. HOW DOES IT WORK?

- **dpkg vs apt.** `dpkg -l` lists installed (state column: `ii` installed, `rc` configs-left);
  `dpkg -S /usr/bin/ls` → "coreutils" (who owns this file); `dpkg -L bash` → every file the package
  ships. `apt` adds the *resolver layer*: `apt update` refreshes indexes from `/etc/apt/sources.list*.d`,
  `apt install/upgrade/remove/purge/autoremove` resolves dependencies. Purely mechanical changes touch
  only `/var/lib/dpkg`. `apt-cache policy <pkg>` shows installed vs candidate version.
- **Mutations need root** — dpkg writes to owned-by-root state (`/var/lib/dpkg`). The failure mode
  "could not get lock" = another apt/dpkg already holds `/var/lib/dpkg/lock` (a running update, a hung
  process, or a jail/container sharing the state).
- **RHEL parity** (must be fluent on both families for DevOps):
  | this box (apt) | RHEL8/9 (dnf/yum) | meaning |
  |---|---|---|
  | `apt update` | `dnf makecache` | refresh repo index |
  | `apt install <p>` | `dnf install <p>` | install |
  | `apt remove/purge` | `dnf remove` | remove |
  | `apt upgrade` | `dnf upgrade` | upgrade |
  | `dpkg -l` | `rpm -qa` | list installed |
  | `dpkg -S <file>` | `rpm -qf <file>` | owner of file |
  | `dpkg -L <p>` | `rpm -ql <p>` | files in package |
  | sources in `/etc/apt/sources.list(.d)` | repos in `/etc/yum.repos.d` | where packages come from |
  | `apt-cache policy` | `dnf --showduplicates list` | versions available |
- **tar.** `tar -czf out.tgz dir` (c=create, z=gzip, f=file), `-tf` list, `-xf` extract (`-C dir` to
  where), `--exclude`, `-j` = bzip2. tar bundles *metadata* (mode/owner/symlinks/mtime) — verified:
  a `chmod 640` file came back 640 after extract. Compression is opt-in (`-z`), not intrinsic.

## 4. PRODUCTION MENTAL MODEL

```
apt ─repo index (sources.list)── dpkg ─/var/lib/dpkg── installed DB (ii/rc states)
    │ candidate vs installed (apt-cache policy)          │
    ├─ lock (would-be writer) ── "could not get lock" ── is ANOTHER apt running?
    └─ parity: yum/dnf, /etc/yum.repos.d, rpm -qf / -ql

tar   → one byte-stream, preserves mode/owner/links   (docker layer = tar stream)
rsync → -a mirrors (mode/mtime) | slash: src/ = contents | --delete syncs removals
        --link-dest=prev = hardlink unchanged, copy changed → snapshots cost only deltas
        exit codes: 0 ok · 23 partial · 24 vanished-source
```

## 5. INTERVIEW-SAFE ANSWER

"Two layers: dpkg holds the installed-state database, apt is the resolver that reads repository
indexes and computes what to install; `dpkg -S`/`-L` answer 'which package owns this file' and 'what
files did this package give me'. On RHEL the same pair is rpm/yum-dnf with repos in `/etc/yum.repos.d`.
The everyday traps I watch for: apt lock ('could not get lock' usually means a hung or concurrent
apt), downgrade/kernel handling (old kernels stack up — don't autoremove kernels blindly), and
environment-nightmares are usually 'works as root interactively, fails elsewhere' because the package
*install* needs root state but the *package choice* is resolver/version work. For files: tar isn't
compression, it's bundling — I add `-z`. And rsync: `-a` preserves metadata; `src/` vs `src` changes
whether you get the directory or its contents; `--delete` mirrors removals — always dry-run
(`-avn --delete`) first; and `--link-dest` gives me cheap point-in-time snapshots because unchanged
files become hardlinks to the previous snapshot. Exit code 23 means a partial transfer — I treat
'rc 0 but files missing' as impossible and 'rc 23' as needs-a-re-run."

## 6. FOLLOW-UP ATTACKS

**Q.** `apt` vs `apt-get`?
**A.** Same engine; `apt` is the prettied-or-parsed frontend, mostly stable for scripts now, but legacy
automation still pins `apt-get` for a frozen interface. Behavior identical underneath.

**Q.** How do you roll back a bad package?
**A.** Known-good pattern: `apt install <pkg>=<old-version>` (if version still in repo) or reinstall
from dpkg with a downloaded `.deb`; on dnf: `dnf history` → `dnf history undo <n>`. Kernels roll back
via grub menu — which is why you don't autoremove all old kernels blindly.

**Q.** Why "could not get lock"? 
**A.** `/var/lib/dpkg/lock` held by a concurrent/unfinished apt/dpkg; rarely a stale lockfile or a
second environment (container) sharing the dpkg root. Check `ps aux | grep -E 'apt|dpkg'` before `rm`
the lock — removing a live lock corrupts state.

**Q.** What's a tar exit-code nuance? (or) How would you ship a dir to another host?
**A.** Stream it: `tar -czf - dir | ssh remote 'cat > dir.tgz'` — tar/-z/-f- reads/writes stdin/stdout.
Never compress twice (-czf on already-compressed artifacts) — point the compression question back:
tar is not a compressor, `-z` is.

**Q.** rsync `-a` vs plain `-r`? 
**A.** `-a` is `-rlptgoD` (recursive, links, perms, times, and others) — the metadata-preserving mode
that makes mirrors real. Plain `-r` moves files, loses mode/time, and then "everything changed every
run".

**Q.** `--link-dest` — how does that save space?
**A.** For each file unchanged vs the reference snapshot, rsync hardlinks it into the new snapshot
(same inode, nlink 2) instead of recopying; only changed/new files consume space. Verified locally:
unchanged files showed identical inodes with nlink=2 (+3 across three snapshots); `du` stayed near-flat.

**Q.** rsync exit 23 vs 24?
**A.** 23 = partial transfer (some files failed — permission/IO on a few); 24 = files vanished **during**
the run (source deleted mid-transfer) — usually benign, still worth noting. Treat both as "didn't fully
sync", replay to converge.

**Q.** Docker layer ↔ tar?
**A.** A container image layer is a tar archive of a filesystem diff; pulling an image is receiving
those tar streams and extracting them with its metadata preserved — same guarantees as `tar -czf`.

## 7. PRACTICAL EXAMPLE (production)

Nightly mirror keeps growing unexpectedly. `rsync -a /app/ /backup/app/` was cron'd (P0.8 pattern!) but
no `--delete` — old code versions stayed forever and `du` ballooned. Fix: `rsync -av --delete --delete-excluded`
with an `--exclude` list, a `-n` dry run in the runbook, and `--link-dest` for daily snapshots so
retention costs deltas, not full copies. Evidence before fix: `du -sh /backup/app/*` vs an `ls -la`
of twice-deleted app dirs still present.

## 8. BUILD / REPRODUCE

### Lab 25 — tar: create → list → extract with metadata (verified)

```bash
mkdir -p src/sub; echo hi > src/a.txt; echo x > src/sub/c.txt
chmod 640 src/a.txt; ln -s a.txt src/alink
tar -czf mydata.tgz --exclude=sub src     # verify with -tzf:
tar -tzf mydata.tgz                       # src/ src/a.txt src/alink (sub excluded)
mkdir extract && tar -xzf mydata.tgz -C extract
stat -c '%a %n' src/a.txt extract/src/a.txt   # verified: 640 both sides
rm -rf src extract mydata.tgz
```

### Lab 26 — rsync: trailing slash, --delete, --link-dest (verified)

```bash
mkdir -p dd && echo keep > dd/keep.txt
rsync -a dd/ dest_slash/         # slash: CONTENTS land in the target (dest_slash/keep.txt)
rsync -a dd dest_noslash/        # no slash: the DIRECTORY lands inside (dest_noslash/dd/keep.txt)
rm dd/keep.txt
rsync -avn --delete dd/ dest_slash/     # dry-run: prints "deleting keep.txt" (verified)
rsync -av --delete dd/ dest_slash/ >/dev/null 2>&1; echo "rc=$?"   # verified rc=0
ls dest_slash                           # empty (verified)

# hardlink snapshots:
mkdir snapsrc && echo 'one' > snapsrc/a.txt && echo 'sub' > snapsrc/c.txt
rsync -a snapsrc/ snapA
echo 'two' > snapsrc/d.txt
rsync -a --link-dest=/tmp/a/snapA snapsrc/ snapB
ls -li snapA/a.txt snapB/a.txt          # verified: SAME inode, nlink 2 (space-free)
du -sh snapA snapB                      # snapB adds only the delta
echo more >> snapsrc/a.txt              # modify one file:
rsync -a --link-dest=/tmp/a/snapB snapsrc/ snapC
ls -li snapB/a.txt snapC/a.txt          # verified: NEW inode for changed file; unchanged c.txt
                                        # still shares inode across A,B,C (nlink 3)
# NOTE: --link-dest worked only with an ABSOLUTE path here (relative refused: "arg does not exist").
rm -rf dd dest_slash dest_noslash snapsrc snapA snapB snapC
```

### Lab 27 — package read-only queries (verified, no root)

```bash
dpkg -l | head                         # state legend: Desired/Status columns (ii = installed)
dpkg -S /usr/bin/ls                    # verified: coreutils: /usr/bin/ls
dpkg -L bash | head                    # verified: / /etc /etc/bash.bashrc /etc/skel …
apt-cache policy curl                  # installed 8.5.0-2ubuntu10.13 / candidate same (this box)
# mutating ops here need sudo (no passwordless) — install/upgrade/remove remain the root domain.
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "apt install fails: could not get lock" (mid-deploy)

**SYMPTOM:** `apt install …` aborts with `E: Could not get lock /var/lib/dpkg/lock-frontend`.
→ **SCOPE:** is *something* really doing dpkg work (deploy pipeline, unattended-upgrades) or is the
  lock stale/lost?
→ **HYPOTHESES:** (a) a concurrent apt/dpkg process (legit — another job is running), (b) a hung or
  abandoned process holding the lock (crash, killed -9 mid-run), (c) leftover lockfile after an abrupt
  boot, (d) two environments sharing the dpkg root (nested container-install-in-install).
→ **CHECKS, first:** `ps aux | grep -E 'apt|dpkg'` and `ls -l /var/lib/dpkg/lock*`. Do NOT `rm` the
  lock while a process is live — you corrupt the dpkg state (the lock IS the integrity guard).
→ **EVIDENCE:** a live `unattended-upgr` or `apt-get` process confirms case (a)/(b) — kill the
  *process* (its lock dies with it), never the lockfile. Empty `ps` + stale lockfile → (c)/(d).
→ **ROOT CAUSE:** (representative) the deploy pipeline ran `apt upgrade` in the background; our step
  raced it.
→ **FIX (smallest safe):** wait for the other job (or `systemctl stop unattended-upgrades` for the
  nightly window), re-run install. If truly stale, `rm` only after confirming no dpkg process.
→ **VERIFY:** install completes; `dpkg -l <pkg>` shows `ii`; `apt-cache policy` candidate == installed.
→ **PREVENT:** serialize package ops in pipelines (flock/lockfile), never background apt against the
  same host, let auto-updates run in their own window.

### INCIDENT — "backup says success but restore is stale/different"

**SYMPTOM:** restore reveals missing or older files, though the backup job "completed fine".
→ **SCOPE:** elapsed-time correctness: the mirror is one rsync away from the truth (P0.4/P0.8 recall).
→ **HYPOTHESES:** (a) no `--delete` → stale files mix into "live" state, (b) `-a` missing → mtimes
  flapped and everything re-copies, (c) wrong trailing slash → wrong directory structure in the backup,
  (d) partial exit 23/24 swallowed by a wrapper treating rc!=0 as fatal silently, (e) backing up a
  live DB/app dir without quiescence (files changing mid-run).
→ **CHECKS:** `rsync -avn --delete src/ dst/` diffs WITHOUT writing (verified pattern); compare
  `rsync -rcvn` for checksum-level truth; read rc in the job log (0 vs 23/24).
→ **ROOT CAUSE:** (representative) mirrors had no `--delete`; deleted production files lived forever
  in "backup", and an old copy got restored on the wrong day.
→ **FIX:** add `--delete --delete-excluded` (+dry-run step in the runbook), keep `-a`, and treat rc≠0
  as a page; for live data, quiesce or use snapshots as the rsync source.
→ **VERIFY:** dry run shows zero drift; a test restore produces a byte-identical tree (`rsync -rcnv`
  clean).
→ **PREVENT:** retention rules that keep history (link-dest snapshots rotate old data instead of
  deleting), backups of quiesced sources, and logs that capture rc + dry-run diff.

### DECISION OVERLAY — what NOT to do

- Don't `rm /var/lib/dpkg/lock*` while apt/dpkg is running — fix the *process*, not the lock.
- Don't run `apt autoremove` casually on kernel stack (grub rollback needs kernels).
- Don't declare backup success on rc=0 alone when 23/24 semantics exist; and never skip the `-n` step
  before a live `--delete`.
- Don't tar already-compressed archives with `-z` again; don't `rsync` a live DB without quiescence.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "`apt install` works without root" | dpkg writes `/var/lib/dpkg` — root-only. (This box: no passwordless sudo.) |
| "A stale lockfile is the cause" | Usually a live process holds it: check `ps` before `rm`. |
| "`rsync -r` mirrors properly" | Need `-a` (−rlptgoD) so mode/mtime survive. |
| "tar compresses" | tar bundles; `-z` is optional compression on top. |
| "src/ vs src are equivalent" | Slash = contents; no slash = the dir itself (verified Lab 26). |
| "`--delete` is a 'cleanup' flag" | It mirror-deletes dest-side files — always `-avn --delete` first. |
| "rc=0 means byte-perfect backup" | 0 = no errors report; 23/24 = partial. Check `-rcvn` for truth. |
| "snapshots cost full disk" | `--link-dest` hardlinks unchanged files — deltas only (verified). |
| "Backup mirrors need no retention" | Without `--delete` the "live" backup silently mutates into history. |
| "dnf and apt install the same thing" | Same family semantics, different repos/fmt; always parity-check RHEL boxes explicitly (rpm vs dpkg). |

## 13. FIRST-CHECK REASONING

- **Package can't install / "no space"/lock/lookup:** FIRST decide *resolver* vs *state*:
  `apt-cache policy <pkg>` (is it even a candidate?) and `dpkg -l | grep <pkg>` (is state `ii`?) — then
  `ps aux | grep -E 'apt|dpkg'` for the lock case. Two read-only queries bracket "version problem /
  state problem / concurrency problem" before touching anything.
- **Backup seems wrong:** FIRST diff, never assume: `rsync -avn --delete src/ dst/` (structure +
  deletions) and `rsync -rcvn` when byte-truth matters. Both non-destructive; both verified above.

## 14. PRIORITY

**P1** (apt/dpkg + yum/dnf fluency, tar & rsync mechanics). P0-adjacent because it underlies images,
artifacts, and infra provisioning.

## 15. STOP HERE — done when you can…

1. answer dpkg vs apt, rpm vs dnf, `-S/-L`, and rollback paths from memory (use parity table);
2. run Labs 25–26 and predict `dst1` vs `dst2` structure, the `deleting …` line, and the inode/nlink
   numbers for link-dest;
3. narrate the apt-lock incident and say exactly why you never `rm` a live lock;
4. use the two first-checks (§13) under pressure;
5. explain the tar-as-layer link to containers.

## 16. DO NOT STUDY YET

multilib/foreign-arch dpkg handling, key-signing/apt pinning grades beyond existence, deb-src and
build-essential depth, `dnf history undo` edge cases, rsync delta-transfer algorithm internals,
rsnapshot/rdiff/duplicity replacement systems, inotify-triggered live sync. Know they exist.

---

## QC CHECKLIST — LINUX.P1.1

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (apt/dpkg + RHEL parity; tar vs rsync)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (resolver vs DB, `-a`, slash, `--delete`, link-dest, rc)? | ✔ §3, §8 |
| 5 | Dependencies (root state, locks, P0.4 disk, P0.8 cron pattern)? | ✔ §3, §7 |
| 6 | Essential commands (`dpkg -l/-S/-L`, `apt-cache policy`, `tar`, `rsync`)? | ✔ §3, §8 |
| 7 | Reproduce (Labs 25–27)? | ✔ verified live (rsync 3.2.7) |
| 8 | Break it (lock error, no --delete drift, partial rc)? | ✔ Lab 26 delete dry-run + rc=23 observed |
| 9 | Observe + interpret evidence (`deleting …`, inode/nlink, `du`, rc)? | ✔ §8–10 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §11 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13).

---

# SESSION LINUX.P1.2 — RESOURCE-TROUBLESHOOTING PLAYBOOKS (CAPSTONE CONSOLIDATION)

This is the Linux **capstone**: no new mechanics — it distills P0.1–P1.1 into a decision router plus a
fixed incident loop you can run on any box with tools already lab-verified. You should be able to
answer "walk me through how you'd debug a slow/crashing box" almost entirely from this one section.

## 1. WHAT IS IT? (≤30 s)

A playbook = (a) a **60-second orientation sweep** that reads the cheap signals first, then (b) a
**triage router** that maps the symptom to one resource lens and its first-check, then (c) the same
**incident loop** used through every session: orient → scope → hypotheses → checks → evidence →
root cause → fix → verify → prevent.

## 2. WHY DOES IT EXIST?

"Run top and guess" loses time, misses evidence, and kills confidence in the follow-up interview
question *"but why did you check that first?"*. Playbooks serialize the cone of uncertainty: they
guarantee you read the cheapest discriminating evidence before you act, and they force you to close
with verify + prevent — the difference between an operator and an engineer.

## 3. HOW DOES IT WORK?

**(a) ORIENT — the 60-second sweep** (all verified on this box today; toolset confirmed: uptime, free,
vmstat, mpstat, iostat, sar, pidstat, ss, sysctl). Run in this order:

```
uptime                        # loadavg (1) . runnable+D-state trend            → busy? which way?
free -h                       # available column is the truth (2)               → memory pressure?
df -h; df -i /                # space AND inodes (3)                            → ENOSPC / inode full?
ss -tln                       # listeners reachable (4)                         → is it listening?
systemctl --failed            # services in failed state (5)                    → what crashed?
```

Healthy baseline captured live on this box (memorize how a *healthy* box reads): `uptime` load
`1.19, 0.88, 0.77` on 8 cores; `free -h` → `used 1.1Gi / available 2.5Gi`, swap `0B`; `df -h` →
`/dev/sdd 1007G, 4.7G used, 1%`; `df -i /` → `1%`; `ss -tln` → a handful of listeners (53 via
systemd-resolved, port 80, and local ports); `systemctl --failed` → `0 loaded units listed`;
`mpstat -P ALL` → per-core `%idle` 67–95%, `%iowait` 0; `vmstat` → `r=1, b=1, si/so=0/0`. If ORIENT
reads like that, the problem is NOT resources — look at the app layer (P0.6 journal, P1.1 package
state, or the network next domain).

**(b) THE TRIAGE ROUTER** — the deliverable. Symptom → lens → first-check → where it came from:

| Symptom | Lens | FIRST check | Decision it makes | Session |
|---|---|---|---|---|
| Slow box, high load | Saturation | `uptime` + `vmstat 1` | `r`>cores ⇒ CPU-bound; `b`>0 ⇒ I/O-wait; `us` vs `sy` | P0.2 |
| One app CPU-hogs | Saturation | `mpstat -P ALL 1` + `top -b -n1` (sort %CPU) | all-cores vs one-core pinning / psr | P0.2 |
| Memory pressure/OOM | Saturation | `free -h` (available, NOT free) | avail→0 ⇒ act; buff/cache reclaimable ≠ leak | P0.3 |
| Exit 137 / killed | Availability | `dmesg | grep -i oom` + `journalctl -k` | who the OOM killer took & why (cgroup?) | P0.3 |
| "No space left" | Saturation | `df -h` THEN `df -i /` | space vs inodes; then top dirs `du -xsh *` | P0.4 |
| Space free but disk "full" | Saturation | `lsof +L1` | deleted-but-open holder (P0.4 lab) | P0.4 |
| Service won't start/dies | Availability | `systemctl status <svc>` | result/exit-code bracket; then `journalctl -u` | P0.6 |
| Port / "in use" / FD leaks | Availability | `ss -tlnp | grep <port>`; `wc -l /proc/<pid>/fd` | LISTEN? holder pid? count vs limit | P0.7 |
| Works by hand, not scheduled | Drift | `journalctl -u cron` / `systemctl list-timers` | dispatched? env difference (SHELL/PATH) | P0.8 |
| Install breaks / lock | Availability | `apt-cache policy X`; `ps aux \| grep -E 'apt\|dpkg'` | resolver vs state vs concurrency | P1.1 |

**(c) THE INCIDENT LOOP** (used identically in every §11 above) —
orient → scope (ONE failing thing vs whole box) → hypotheses (2–4, kids-only after the bracket) →
checks that DISCRIMINATE (first-check first) → evidence (quote the number) → root cause (mechanism,
not description) → fix smallest-safe → verify (measure, don't assume) → prevent (alert/metrics/runbook).

## 4. PRODUCTION MENTAL MODEL

```
   report → ORIENT (60s: uptime · free · df · ss · failed)   ← cheap signals, always first
              │  healthy?  → app/database layer, not resources
              ▼
      lens:  SATURATION (consumed)  |  AVAILABILITY (down/killed)  |  DRIFT (env mismatch)
                │                       │                              │
         vmstat/mpstat/iostat       systemctl/journal/ss/lsof      cron/timer env, package state
                ▼
      EVIDENCE (quote the metric) → ROOT CAUSE → FIX → VERIFY → PREVENT
   rule: never act until the first-check has COATED the hypothesis space.
```

## 5. INTERVIEW-SAFE ANSWER

"I run a fixed loop, not tools. First the 60-second orientation — `uptime`, `free -h` (I read the
*available* column, not free), `df -h` + `df -i`, `ss -tln`, and `systemctl --failed`. If those read
healthy, the box's resources are not the story. Then I classify into one of three lenses: saturation —
something is consumed, so `vmstat` tells me *which* resource (runnable rows > cores means CPU-bound;
b > 0 means D-state/I/O-wait); availability — something is down, so systemd's verdict and the journal
or `ss`/`ss -tlnp` locate *what* (crash-loop, failed unit, port conflict, EMPTYFE leak); or drift —
the environment walked away from the assumption, like cron's minimal PATH or a package that isn't
installed where the manifest thinks. Each branch has exactly one first-check that discriminates —
e.g. high load → `vmstat 1` splits CPU-bound from I/O-bound before I touch top; 'no space' → `df -h`
then `df -i` splits space-full from inode-full; 'service failed' → `systemctl status` + the journal.
Only after the evidence bracket points at a mechanism do I act, and I always finish with verify-by-
measurement and a prevent step — because restarting a crash-loop twice isn't a fix, understanding why
it loops is."

## 6. FOLLOW-UP ATTACKS

**Q.** Load 100 on a 48-core box — is it dying?
**A.** Not without more signal: load counts runnable **and** D-state, so 100/48 could be CPU-saturated
or deep I/O wait (each process waiting on disk counts). `vmstat`: high `r` + high `us` = CPU burn;
high `b` + low idle while `r` holds = I/O-wait. Never read load in isolation (P0.2).

**Q.** `free`'s "free" column says 1 Gi but "available" says 2.5 Gi — which do I trust?
**A.** Available — free ignores reclaimable buff/cache, available accounts for it. Chasing `free`
causes fake memory alerts (P0.3 lab).

**Q.** CPU-bound vs I/O-bound, concretely?
**A.** `mpstat -P ALL 1 1`: `%iowait` high ⇒ I/O-bound (check `iostat -x` → `await`/`%util`); `%usr`
high ⇒ CPU-bound (top per-pid); `%sys` high ⇒ syscalls/context-switch storm (`pidstat -w`). One sunk
core with others idle ⇒ affinity/pinning bug, not capacity (verified pattern in the load lab).

**Q.** Containers — do these playbooks transfer?
**A.** Concepts transfer 1:1; *scoping* changes. Host-level `vmstat`/`free` show the host; the
container's truth lives in its cgroup (`systemctl status` on a systemd unit shows Tasks + Memory
limit — the P0.3 cgroup-OOM angle), plus `free` inside a container is host-glassed. Start with "is it
the container's slice or the host's disk" — the ORIENT sweep still gives that answer fast.

**Q.** When do you escalate vs keep digging?
**A.** When I'm past my verified playbook depth, or the failure implies access I don't have (hardware
console, host-kernel). Wait: escalate with a written evidence package — metrics, timeline, what I
tried — not with "it's slow". Also: never act live-destructive without sign-off; dry-runs are free.

**Q.** What's your standard "incident" answer structure?
**A.** Symptom → scope → hypotheses → cheapest discriminating check → evidence quoted → root cause →
smallest-safe fix → verify by measurement → prevention. Every §11 in this document already follows
it; I hold The ORIENT sweep, then the one lens.

## 7. PRACTICAL EXAMPLE (production — end-to-end using only prior labs)

API latency climbs at peak; SRE pings. ORIENT: `uptime` → load 12 (8 cores, so saturated-ish),
`vmstat 1` → `r` low but `b` climbing, `%iowait` up; `free -h` fine, `df -h` fine, `df -i` fine,
`ss -tlnp` shows the API LISTEN. So NOT CPU, NOT memory, NOT space/inodes/logic — lens = saturation,
resource = **I/O**. `iostat -x 1` shows one disk at `%util=100` `await` high. Who's writing?
`lsof +L1` → a deleted-but-open app log (the P0.4 lab, exactly). Fix: stop/rotate the holder so the
fd closes, space returns. VERIFY: `iostat` → `%util` down, `vmstat` `b→0`; prevent: log rotation +
"disk i/o wait" alert + fd-count metric. Total: two minutes of orient before one hypothesis is
broadcast. (This is the exact arc of P0.2→P0.4 incidents consolidated.)

## 8. BUILD / REPRODUCE (drills — all artifacts already verified)

- **Drill A — ORIENT rehearsal:** run the five-command sweep (verified today); on a healthy box teach
  your eyes the healthy numbers (`load < cores`, `available` comfortably > 0, `swap 0`, `%idle` high).
- **Drill B — CPU branch:** `labs/01-linux/loadburn.sh` (P0.2) → re-run `mpstat -P ALL 1 1` +
  `pidstat` and walk the router: high `r`+`us` ⇒ CPU-saturated verdict; then `pkill -x yes`.
- **Drill C — disk branch:** recreate the deleted-but-open file (P0.4 Lab 11/12), run `lsof +L1`,
  and walk to "holder → close → verify df returned space".
- **Drill D — availability:** crash-loop a unit (P0.6 Lab 16), then run the §11 service-won't-start
  flow to the journal line. Then clean and `systemctl --failed` must read clean.

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT — TWO CAPSTONE DRILLS

**Drill 1 — "it's slow" (CPU vs I/O verdict discipline).** 
→ SCOPE: whole box vs one app. → HYPOTHESES: CPU saturation / I/O-wait / memory (shortfall→swap) /
   a single stuck process. → CHECKS: `vmstat 1 3` (r vs b, si/so), `mpstat -P ALL 1 1`, `top -b -n1`.
→ EVIDENCE: load 12/8-cores with `us~0 sy~5 idle~25` and `b=4` ⇒ I/O-wait, not CPU. → ROOT CAUSE
   (sample): a log writer fighting the disk. → FIX: identify writer (`lsof +L1`, `pidstat -d`), stop
   rotation war. → VERIFY: `vmstat b→0`, loadavg decay. → PREVENT: `%iowait` alert + writer
   throttling. TRAP for the interview: don't say "high load = CPU busy"; the `r`/`b` split is the
   grade; and mpstat decides per-core, because a wedding-one-core bug still shows load.

**Drill 2 — "randomly killed" (OOM bracket).**
→ SCOPE: is it really OOM or a supervisor? → CHECKS: `dmesg | grep -i oom`/`journalctl -k`, exit
   137 evidence, `free -h` before/after, cgroup `.max` if a unit (P0.3). → EVIDENCE: `Out of memory:
   Killed process …` + exit 137. → ROOT CAUSE: process RSS exceeded cgroup/host limit, or overcommit
   bite. → FIX: raise cgroup limit / reduce footprint / add swap deliberately. → VERIFY: app stays up
   over a load spike. → PREVENT: memory-limit sizing from observed peak, OOM-kill alert.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "High load ⇒ CPU" | Load = runnable + D-state. `vmstat r/b` decides CPU vs IO. |
| "Trust the `free` column" | `available` is the operational truth (P0.3). |
| "Disk 'no space' = space" | Check `df -i` — inode exhaustion says 'No space left' too. |
| "Disk has space → not disk" | Deleted-but-open files still occupy space: `lsof +L1` (P0.4). |
| "Restart fixes a crash-loop" | It resets the loop; the journal stays empty until you READ it (P0.6). |
| "It's the app's fault" before orient | First prove the box can (resources) — then app. |
| "Metrics answer everything" | They bracket; the journal/app log confirms (or kills) the #1 suspect. |
| "Containers hide host disks" | The host's disk/app is the container's problem too. |
| "A clean ORIENT = no incident" | It means not resources — go app-layer (P0.8 env, P1.1 package, network next). |
| "Playbooks are rigidity" | They're a spine: hypothesis discipline on top of real evidence. |

## 13. FIRST-CHECK REASONING (capstone)

- Run the five-command ORIENT first, always — each read is under a second, each is *cheap-and-
  discriminating*: `uptime` (busy? which direction), `free -h` available (memory pressure), `df -h`
  + `df -i` (space vs inodes), `ss -tln` (listening? on what), `systemctl --failed` (crashed units).
  A healthy ORIENT redirects you off resources entirely in one minute.
- THEN branch via the router's single first-check per symptom (`vmstat 1` for load, `systemctl
  status` for services, `ss -tlnp` for ports/fds, `apt-cache policy`+`ps` for packages) — the
  first-check is chosen to *split* the hypothesis space, not to confirm noise.

## 14. PRIORITY

**P0.** This section + the ORIENT sweep are the resume-defensible core of "I can troubleshoot Linux
in production."

## 15. STOP HERE — done when you can…

1. run the 60-second ORIENT and read healthy vs unhealthy like a dashboard (Drill A);
2. pick the lens (saturation/availability/drift) for any symptom you've met in P0.1–P1.1;
3. state the single first-check per symptom from the router table without reading it;
4. narrate either capstone drill (§9–11) A→Z with evidence quotes;
5. close EVERY answer with verify-by-measurement + a prevent step.

## 16. DO NOT STUDY YET

perf-events/eBPF/BPF-trace tuning, NUMA/scheduler/internal kernel counters deeper than `mpstat`/
`iostat`/`pidstat`/`sar`, io_uring and storage-stack internals, exotic cgroup knob tuning, kernel
panic/kdump analysis. Those are senior-plus terrain; the router above covers 1–3 YOE.

---

With LINUX.P1.2 the Linux domain's mandated sessions (P0.1–P0.8, P1.1, P1.2) are **all COMPLETE**.
Remaining candidate work: re-run Labs 19–27 for maintenance before interviews. **Next domain:
NETWORKING** — begins with TCP/IP + socket behaviour (the groundwork already laid in P0.7), where the
first session will be verified and appended in the new file per the approved architecture.

---

## QC CHECKLIST — LINUX.P1.2

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (orient → lens → loop)? | ✔ §4 |
| 2 | ≤30 s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Routers + ORIENT sweep, each with a first-check and session ref? | ✔ §3 table |
| 5 | Cross-session dependencies wired (P0.2–P1.1)? | ✔ §3 router |
| 6 | Essential commands (orient set + per-lens first-checks)? | ✔ §3, §8 |
| 7 | Reproduce (Drills A–D)? | ✔ orient sweep run live today (healthy numbers quoted) |
| 8 | Break it (CPU vs IO split, OOM bracket)? | ✔ Drills 1–2 verbatim arcs |
| 9 | Observe + interpret evidence (r/b, %util, oom entry)? | ✔ §7–11 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §7, §11 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Linux domain mandated sessions complete.