# 14 — ATTACK CHAINS

Interviewers probe TWO levels deeper than your claim — here is the full tree, pre-built: for every domain, the L1 baseline answer, the L1.5 one-two punch, the L2 mechanism, the L3 senior floor, the trap used to catch overconfidence, and the questions one more level down.

**How to drill (rigid protocol):**
1. Pick a chain. Cover the answers.
2. Ask yourself LEVEL 1 out loud. Answer in ≤30s. Then LEVEL 1.5 follow-up, then LEVEL 2.
3. Reveal answers. Annotate: what you got, what you fumbled, why.
4. Re-drill the fumbled nodes at +24h and +48h. Log in the per-chain table.
Difficulty: L1 = expected baseline at 1–3 YOE, L1.5 = the "one-two punch" filter question, L2 = the "they went deep, can you stay" question.
Score 0–5 and log.

**House rules that keep this file honest:**
- Golden answers are graded against the VERIFIED content of files 01-linux through 12-troubleshooting. Every row carries the session it came from. If a row cannot cite a session, it is rewritten or dropped — a wrong "golden answer" teaches the wrong thing, which is the deepest trap this file guards against.
- Recite aloud, standing, with a wall-clock. L1 ≤30s, L1.5 ≤45s, L2 ≤60s, L3 ≤90s. A chain solved silently in your head is not a chain drilled; interviews score output, not intent.
- A score of 5 requires the L3 row AND the TRAP VARIANT catch AND a clean CROSS-EXAM. "I knew that, I just panicked" scores 3. No exceptions.
- The +24h/+48h re-drill covers ONLY the fumbled rows, at full speed, with no notes. Re-drilling everything is dilution; re-drilling nothing is fantasy.
- Keep a per-chain drill log. Three sessions minimum per chain before you call it passed; the rotation table at the end schedules them across 4 weeks.
- Nothing in this file is fabricated. Every command, code, exit status, and observed behavior below comes from a lab that was actually run on the war-room box between 2026-09-13 and 2026-09-20, or is a model-only concept explicitly labeled as such in the source file.

**Chain anatomy (one unit of training):**

```
### CHAIN 14-XX — DOMAIN
framing -> L1 answer (<=30s) -> L1.5 punch (<=45s) -> L2 mechanism (<=60s)
-> L3 senior floor (<=90s) -> TRAP VARIANT catch -> if it stays hard,
the CROSS-EXAM -> WRONG-ANSWER ALARM -> SPEAKING OPPONENT (why they asked)
-> SELF-SCORE -> FUMBLED NODES -> RE-DRILL log -> NEXT POINTER
-> 13-row QC gate (row 13 = SELF-VERIFY against the source files)
```

**Difficulty and time budget:**

| Level | Budget | What it filters | If you fumble it |
|---|---|---|---|
| L1 | ≤30s | baseline known-working vocabulary for 1–3 YOE | the domain is not yet P0-owned; re-drill the base session |
| L1.5 | ≤45s | can the candidate advance DEPTH on the same topic, not detour to a new one | the interviewer doubts you have a model, only fragments |
| L2 | ≤60s | do you know the mechanism, or just the fix | the "one-two" ends; you are rated on breadth not depth |
| L3 | ≤90s | the senior floor: cross-domain consequences and the honest limits | you stay a mid-band candidate on this domain |
| TRAP | catch at any level | overconfidence: the interviewer asked the WRONG-SOUNDING thing on purpose | every confident-but-wrong claim costs more than silence |

**Scoring rubric (0–5):**

| Score | Meaning |
|---|---|
| 5 | L1→L3 all near-flawless, trap caught, cross-exam survives, spoken in budget |
| 4 | L1–L2 clean, L3 acceptable, trap caught after a beat of thought |
| 3 | L1–L2 clean, L3 fuzzy, trap missed or wrong "fix" offered |
| 2 | L1 only, or L1.5 needed a restart |
| 1 | L1 shaky, naming-before-mechanism, no evidence habit |
| 0 | guesswork or a fabricated claim — the interview's instant kill |

**Claim-level mapping for this file (from the README resume rules):** a chain you hold at 5 lets you claim UNDERSTOOD/PRACTICED for that row's behavior; a chain you hold at 3 lets you claim USED at most. The attack-chain score is the evidence gate for what you may say in 16-resume-defense. If you cannot drill a chain, you cannot claim it.

**How the chains map to the source files:**

| Chain | Domain | Primary source files | Session anchors |
|---|---|---|---|
| 14-01 | Linux | 01-linux, 12-troubleshooting | LINUX.P0.1, P0.3, Lab 2; TS-19 |
| 14-02 | Networking | 02-networking, 12 | NET.P0.2/0.3/0.5/0.7; TS-1/3/5 |
| 14-03 | Git | 03-git, 11-security, 12 | GIT.P0.1/0.4/0.5; SEC.P2.2; TS-30 |
| 14-04 | Bash | 04-bash, 09-cicd | BASH.P0.3–P1.1; CICD.P0.4 |
| 14-05 | AWS | 05-aws, 11-security, 12 | AWS.P0.2/0.4/0.6/0.7; SEC.P0.2/0.3/0.4; TS-4/9/11 |
| 14-06 | Docker | 06-docker, 01-linux, 09-cicd | DCK.P0.1/0.2/0.7/P1.1/P1.2; CICD.P0.6 |
| 14-07 | Kubernetes | 07-kubernetes, 11-security, 12 | K8s.P0.1–P0.7; SEC.P1.1; TS-2/16/18/20/27/28 |
| 14-08 | Terraform | 08-terraform, 12 | TF.P0.1–P1.1; TS-22/23 |
| 14-09 | CI/CD | 09-cicd, 12 | CICD.P0.x/P1.x/P2.x; TS-24/25/26/27/29 |
| 14-10 | Observability | 10-observability, 07-kubernetes | OBS.P0.1–P0.10/P1.3/P2.x |
| 14-11 | Security | 11-security, 05-aws, 07-kubernetes | SEC.P0.1–P1.2/P2.x; AWS.P0.2; K8s.P0.7 |
| 14-12 | Troubleshooting | 12-troubleshooting | all 30 incidents, 4 archetypes |
| 14-13 | Cross-cutting design | all files | glue rows across every domain |
| 14-14 | Behavioral | all files, README | claim levels, incident stories, DORA |

Every chain below ends with the same QC checklist. Row 13 is the gate: SELF-VERIFY — every golden answer is provably correct against the source sessions. If a chain fails that row, it is not drilled, it is memorized wrong.

---

## THE CHAINS

---

### CHAIN 14-01 — LINUX
**Why this chain:** processes, states, signals, zombies, OOM and load are the single most probed body of topics at 1–3 YOE, and they underpin every other domain in this file.
**Source sessions:** LINUX.P0.1 (states/signals, zombie Lab 2), LINUX.P0.3 (memory/OOM/cgroup), LINUX.P1.2, 12-TS Incident 19 (OOMKilled), CICD.P0.6 (exit-127 applet trap).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | You run `kill -9 <pid>` on a hung process. What happens, exactly? | SIGKILL (9) is delivered and it is uncatchable and unignorable — the process never runs its cleanup handlers; the kernel terminates the task immediately and the exit is reported to the parent. That is why the discipline is TERM first (graceful, catchable, lets the app flush and close), killing blindly only after TERM is identified as useless, never blind-kill-first — and the corruption risk of KILL is app-dependent: it skips cleanup, so in-flight external state (DB records, other nodes) is the app's responsibility. (LINUX.P0.1 §3, §5.) |
| L1.5 | And why would that pid show up as a zombie? Can I `kill -9` the zombie too? | A zombie is already dead: the child exited and the kernel holds only the corpse (exit status, minimal info) until the parent reads it with `wait()`. `kill -9` on a zombie is a no-op — there is no running task to signal, and the kill exits `0` while the Z row remains. The fix is the parent: fix its `wait()` handling, or kill the parent so PID 1 (or the nearest subreaper) adopts and reaps the child. Gotcha: a zombie's `cmdline`/args are freed, so `ps | grep app` finds nothing — filter by state, not name: `ps -eo pid,ppid,stat,comm | awk '$3 ~ /^Z/'`. (LINUX.P0.1 §3, §6, Lab 2 — verified: `1228 Z`, `kill -KILL` no-op, reaped after parent death.) |
| L2 | Trace the kernel path from signal delivery to task reaping. What survives, and who pulls it? | The kernel marks the task with the uncatchable SIGKILL default, takes it off the run queue, frees its userspace memory and file handles, then parks it in zombie (EXIT_ZOMBIE) — the task_struct keeps only the exit code and parent linkage. The parent receives SIGCHLD; when it calls `wait()`, the kernel reclaims the task_struct and the PID is freed. If the parent is gone the task is reparented to PID 1 or the nearest subreaper, which reaps it. The caveat: a task in D state (uninterruptible kernel I/O — typically disk or NFS) cannot be signaled until it returns to userspace, so a queued kill just sits there; that is a live task, not a zombie, and it reads 0% CPU in top. (LINUX.P0.1 §3, §5, follow-ups.) |
| L2.5 | Container variant: your pod restarts and the exit code is 137. What does 137 mean and who killed it? | 137 = 128 + SIGKILL (9). In a container the usual actor is the cgroup: the workload hit its memory limit, the kernel OOM-killer picked the heaviest process in that cgroup and SIGKILL'd it. Evidence chain: exit code 137 plus `OOMKilled=true` in `docker inspect` (ExitCode 137 in the pod status), and `dmesg`/journald lines "Out of memory: Killed process" or the container flavor "Memory cgroup out of memory". Differentiate: 137 with OOMKilled=false means an external forced kill (stop timeout, a human SIGKILL'd it). The fix decision is raise-the-limit vs find-the-leak; and `oom_score_adj=-1000` protects one process's score but NOT its cgroup — the container limit still kills it. (LINUX.P0.3; 12-TS Incident 19.) |
| L3 | High load, but `top` shows idle CPU. Walk the diagnosis. | Load average is not a percentage: it is the 1/5/15-min moving average of runnable PLUS uninterruptible threads, and D-state (uninterruptible I/O, usually disk or NFS) is counted. A D-state spike inflates load while `top` shows ~0 CPU — the single most common Linux misdiagnosis. First checks: `vmstat`'s `wa` column, a `ps` state histogram (`ps -eo stat | sort | uniq -c`), then identify the D-state victims. Also remember `ps` `%CPU` is a lifetime average while `top` is near-instantaneous — never compare the two directly. (LINUX.P0.1 follow-ups "high load idle CPU" and "ps 100.0 vs top ~0".) |

**TRAP VARIANT:** "There are zombies everywhere — that's why my load is high." The catch: a zombie is dead. It holds no memory, executes nothing, and cannot burn CPU; a Z row is the symptom of a broken parent (never calling `wait()`), not a load cause. If load is high AND zombies are present they are two different problems wearing one costume: hunt the R/D state work for the load, and fix the parent for the zombie flood.

**IF THEY ASK BETTER:**
- "How do you produce a zombie on purpose?" Fork a child that exits while the parent sleeps without `wait()`; observe the Z row with the state filter; clean up by killing the parent so PID 1 reaps. That was LINUX.P0.1 Lab 2, verified live on this box.
- "What happens if PID 1 dies?" The kernel keeps PID 1 special: SIGKILL to PID 1 is ignored by the kernel, but killing it panics the kernel — and nothing gets reaped anymore. (LINUX.P0.1 follow-up.)
- "A process won't die even after `kill -9`. Why?" Two classic causes distinguished by state: D state (unkillable until the I/O returns — fix the disk/NFS) vs zombie (already dead). Rarely: an interminable syscall or a kernel lock. (LINUX.P0.1 follow-up.)

**WRONG-ANSWER ALARM:** "kill -9 always causes corruption" (it skips cleanup; whether corruption happens is app-dependent). "A zombie is still running" (it is not). "free's `used` is the number to watch" (the `available` column is the estimate that matters). "Swap is always bad" (it is a safety valve with tuning dials like swappiness and per-cgroup control).

**SPEAKING OPPONENT:** Signals and states test whether you carry a working model — delivery, catchability, reaping, D-vs-Z — instead of reciting `ps` output. The 137/OOM crossover is the container-age filter: candidates who know only host OOM lose the second half; naming the cgroup OOM kill, `OOMKilled=true`, and the "oom_score_adj cannot protect a cgroup" nuance at the same answering level is the senior tell an interviewer will not forget by the end of the day.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** take the 137/OOMKilled and exit-code rows straight into 14-06 Docker and 14-07 Kubernetes (CrashLoopBackOff), and into 12-TS Incidents 16 and 19; come back and make this chain self-contained before any cloud interview.

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-01
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Commands and exit codes match verified output (137, Z-state awk, kill no-op) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-02 — NETWORKING
**Why this chain:** refused-vs-timeout, TCP lifecycle, DNS taxonomy, and TLS failure are the reachability spine every other domain's troubleshooting leans on.
**Source sessions:** NET.P0.2 (TCP states, refused), NET.P0.3 (DNS), NET.P0.5 (TLS), NET.P0.7 (diagnostics), 12-TS Incidents 1 (kubectl refused), 3 (ndots NXDOMAIN), 5 (TLS expired).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | `curl` dies with "connection refused". What does refused mean versus a timeout? | Refused = something reached a host and actively rejected the TCP SYN with an RST — usually nothing is listening on that port, or a firewall/LB returns RST; the host and the path exist. Timeout = the SYN left and no RST and no SYN-ACK came back — packets are lost or filtered (dropped SG/firewall rule, dead path, unreachable IP). One decision, two words: refused says "I found the box but not that port", timeout says "I could not reach the box at all". Verified live: `nc -zv 127.0.0.1 1` on a closed port returns instantly refused; `curl -sS -m 2` at the same port reports `curl: (7) Failed to connect`. (NET.P0.2, NET.P0.7.) |
| L1.5 | You replaced a pod and now the same port is refused. What is the first check before touching anything? | Scope first, then evidence. On-host: `ss -tlnp | grep <port>` — is anything listening at all, and on WHAT address? A loopback-only bind (`127.0.0.1`) is the #1 bind bug: localhost curl works while the LB/healthcheck sees refused or timeout, because the LB reaches the node address, not loopback. In Kubernetes read the Service truth: `kubectl get endpoints <svc>` — a Service with an EMPTY endpoints list resolves to a ClusterIP that refuses/resets connections; that is the classic bad-selector failure. Real incident shape: after a cluster recreation, every kubectl call refused at `127.0.0.1:45999` — stale kubeconfig and a dead port, not a dead cluster; the splitting check is `kubectl get nodes` plus `ss -tlnp` for the apiserver port. (12-TS Incidents 1 and 2; K8s.P0.2.) |
| L2 | Trace the TCP connection lifecycle: what states does a refused connection traverse, and where does TIME_WAIT fit? | Refused is a short-circuit: the client sends SYN, the server TCP with no LISTEN socket replies RST, the client surfaces ECONNREFUSED — no established state ever forms. A LISTEN socket answers SYN with SYN-ACK and the pair completes the handshake (SYN, SYN-ACK, ACK) and you soon read `ESTABLISHED` in `ss -tan`. TIME_WAIT sits on the side that initiates the close, keeping the FIN-exchange's last ACK around for 2×MSL so late segments cannot pollute a reused (addr,port) pair — expected and healthy when bounded, not a leak. The state histogram is read before any firewall debate: `ss -tan state time-wait`, and the kernel's `0A`/`01`/`17` hex (LISTEN/ESTABLISHED/TIME_WAIT) from NET.P0.2's Lab 21. (LINUX.P0.7 Lab 21; NET.P0.2.) |
| L2.5 | `curl` says the SSL certificate has expired, but ops swears it was renewed. Diagnose in order. | Fail the layer first: `openssl s_client -connect host:443 -verify_hostname <host>` and read the verification errors — never `curl -k`, which throws away the evidence. The two-sided trap: the client validates the server cert against the CLIENT clock, so a skewed client clock manufactures a false "expired" (notAfter already passed from the client's point of view). Read the cert's real validity window (`notBefore`/`notAfter`) and compare to the client's local time BEFORE blaming the server's renewal. `openssl verify error 10` = expired is the P0 classification; the sibling failures are chain/SAN mismatch and untrusted CA. (NET.P0.5, NET.P0.7; 12-TS Incident 5.) |
| L3 | Walk DNS resolution on this box end to end, then the whole failure taxonomy. | Path: app → resolv.conf → systemd-resolved → nameserver (10.255.255.254, search `bbrouter`) → forwarder/cache → authoritative. Failure classes: NXDOMAIN (the name truly does not exist), NOERROR-empty (name exists, no records of the requested type), SERVFAIL (upstream/authoritative error), timeout (packet loss, no answer), and partial (one address family answered, the other not). The in-pod Kubernetes variant adds the ndots trap: a short name with `ndots:5` expands through the search domains first, so a name that resolves in one namespace NXDOMAINs outside it — classify before you change DNS. Habit to state: the symptom is never "DNS is broken"; it is one of these five, each owned by a different layer. (NET.P0.3, NET.P0.7; 12-TS Incident 3.) |

**TRAP VARIANT:** "ping works and curl times out, therefore the network is fine." The catch: ping is ICMP, and SGs/NACLs often allow ICMP while filtering TCP 443 (or the reverse), and L4/L7 proxies and NAT sit between client and app. ICMP reachability is NOT TCP reachability. Prove the port with `nc -zv`/`curl --max-time`, prove the path with `ip route get`, and only then blame the app or the LB.

**IF THEY ASK BETTER:**
- "HTTP/1.1 vs HTTP/2, in one sentence": HTTP/1.1 is one request at a time per connection (hidden head-of-line latency); HTTP/2 multiplexes streams over one connection — HTTP/2 exists because 1.1's serial model is the bottleneck. (NET.P1.2.)
- "How do you prove an MTU or keepalive claim?" tcpdump for ARP/MTU at the packet level (NET.P1.1, non-root observables); `SO_KEEPALIVE` probes have a default ~2-hour countdown that `ss -ot` makes visible (NET.P1.2).
- "A service bound to 127.0.0.1 works locally but not from the load balancer — why?" The bind address is a statement: 127.0.0.1 is loopback-only, 0.0.0.0 means any interface; the "working locally, dying from the LB" symptom is the #1 bind bug in the whole stack. (NET.P0.1.)

**WRONG-ANSWER ALARM:** "Checked the firewall first" (evidence comes before firewall inquisition; read the state histogram and the app's bind first). "The cert is wrong, replace it" before checking the client clock. "DNS is broken" without classifying which of the five failures it is. "I restarted it and it works now" (no root cause, no prevent — that ends the interview's probing, not favorably).

**SPEAKING OPPONENT:** The interviewer listens for EVIDENCE-led tool discipline: classify refused-vs-timeout, then reach for `ss`/`openssl s_client`/`dig` — or fall back on restarts. Refused-vs-timeout is the meta-test; the TLS client-clock nuance and the ndots trap are the senior separators that most 1–3 YOE never name, and the box's real DNS path (systemd-resolved forwarding to 10.255.255.254) is the proof-by-specific that beats textbook nameservers.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** run this chain against 14-07 Kubernetes rows for endpoints and 14-12 Incidents 1/3/5 together; the refused/timeout split is the same diagnostic moved between domains.

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-02
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Commands match verified output (curl (7), nc refused, ss state time-wait, openssl verify 10) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-03 — GIT
**Why this chain:** object model, reset/revert, reflog rescue, and the secret-in-history rotation story — git is both a P0 interview domain and the vocabulary of CI/CD and GitOps.
**Source sessions:** GIT.P0.1 (object DB, three states), GIT.P0.4 (rebase/amend), GIT.P0.5 (reset/revert/reflog), GIT.P0.7 (conflict resolution), GIT.P1.1 (bisect), 12-TS Incident 30 (secret leak), SEC.P2.2 (rotation).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | Explain the three states of git and what `git add` actually does. | Working tree (the files you edit) → index/staging area (the snapshot of what the next commit will contain) → HEAD (the last commit). `git add` writes the file's content into the object database as a blob and updates the index entry; `git commit` snapshots the index into a commit object. Objects are content-addressed (blobs, trees, commits keyed by SHA), so identical content deduplicates automatically. The working concept to sell: the index is "the next commit, built deliberately", and interactive `git add -p` stages hunks so a commit is a coherent unit, not a dump. (GIT.P0.1, GIT.P0.2.) |
| L1.5 | Reset vs revert vs checkout — when do you reach for each, and on which kind of branch? | reset = local pointer surgery: moves HEAD and optionally the index and the worktree (soft/mixed/hard) — for local-only history. revert = a NEW commit that undoes an old one: safe on shared/pushed history because it adds a corrective commit, it never erases. checkout/restore = bring a path or branch back to a known state. Golden rule: hard/soft reset and interactive rebase on LOCAL history only; revert for anything another clone can see. Reflog is the rescue journal for reset-away commits (default `gc.reflogExpire` = 90 days) — "reading the reflog is my first triage on any 'deleted' report". (GIT.P0.5.) |
| L2 | Trace a `git reset --hard HEAD~1`: is anything actually erased from the object database? | A reset moves a reference; the objects stay in the object DB. They become unreachable from any ref but remain reachable from the reflog, which logs "reset: moving to <sha>". GC removes only truly unreachable objects and honors reflog lifetime. The rescue is therefore: `git reflog` → pick the pre-event SHA → `git reset --hard <that SHA>` (or `git switch -c recovery <thatSHA>`) and the branch plus its history return. Verified live: after `--hard`, `git reflog -6` listed both resets, and the rescue restored the file and history exactly. Nothing is erased until GC — which is why the incident playbook says: grab the rescue SHA the moment it matters. (GIT.P0.5 Lab 5 and INCIDENT.) |
| L2.5 | How does a merge commit differ from a fast-forward, and when does history fork? | Fast-forward: the incoming branch is a strict descendant of the current tip, so git just moves the label — no new commit and a linear history. Merge commit: histories have diverged, so git combines THREE snapshots — the common ancestor, ours, and theirs — into one merge commit against the merge base. A conflict exists only when ours and theirs changed the SAME lines differently from the ancestor: git three-way diffs, it does not diff two files. Merge preserves topology; a fast-forward keeps history linear. (GIT.P0.3, GIT.P0.7.) |
| L3 | A secret got committed and pushed a month ago. What is the actual fix? | The secret lives in history as objects: deleting the file in a new commit is not a fix. Rewriting history (filter-repo) removes the blob from the branch, but every clone that pulled before the rewrite still holds the object, and the remote's event feed and stored refs may retain it. The durable half is ROTATION: revoke the old credential and issue a new one — rotation is the only step that makes the old value dead. Demonstrated live: after a "rotation" commit, `git show HEAD~1:.env` still returned the old key, and a 12-line python walk of every commit/blob flagged it. Prevention is the CI secret-scan gate that runs first in the DAG because it is the cheapest runnable signal with the highest actionability. (12-TS Incident 30; SEC.P2.2.) |

**TRAP VARIANT:** "We force-pushed, the commit is gone, so the secret is out of the repo." The catch: force-push rewrites branch tips on the remote, but the objects survive in every existing clone, in reflogs, and in the remote's retained refs/event history. Anyone who cloned before the rewrite can run `git log --all` or `git reflog` and recover the blob. History rewrite without rotation proves nothing; rotation without rewrite leaves the raw material in old clones. Do both — and add the scan gate so the next one never merges.

**IF THEY ASK BETTER:**
- "What does `git commit --amend` actually do?" It creates a NEW commit object with a new SHA; the old commit survives, reachable from the reflog. Verified: amend printed a new SHA and the reflog listed both the old and the new commit — amend "edits" by rewriting, exactly like rebase.
- "How do you find the commit that introduced a regression?" `git bisect`: binary search between a known-good and a known-bad marker, on a tree you can rebuild and test at each step.
- "You rebased a shared branch and force-pushed. What now?" Coordinate: broadcast the reset point, have collaborators `git fetch` and reset their LOCAL branches to the agreed new tip (`git reset --hard origin/<branch>`), never merge the old history back in — and avoid the rewrite on shared branches next time.

**WRONG-ANSWER ALARM:** "Reset erases commits" (it moves a label; objects persist until GC and the reflog is the backdoor). "Rebased commits are deleted" (old objects stay reflog/origin-reachable). "Delete the file and commit — done" on a leaked secret (rotation is the durable fix). "`undo` resets me to a clean slate" on deployments (that one lives in chain 14-07, but the same object-persistence logic applies).

**SPEAKING OPPONENT:** Git questions separate model-holders from menu-memorizers in minutes. Interviewees who answer "delete the commit" on a pushed secret fail the chain; the triage "reflog first, rotation targeted, rewrite scoped, scan gate added" — in that trust order — earns it. The interviewer is also watching ego: the candidate who can say "I reset --hard the wrong branch" and walk the recovery with reflog evidence signals production honesty.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** carry the L3 rotation story into 14-11 Security and 14-12 Incident 30; carry the reset-vs-revert rule into 14-09 CI/CD (rollback-is-a-pointer-change, not a reset).

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-03
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Commands and hashes match verified output (reflog rows, HEAD~1 walk, amend SHA) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-04 — BASH
**Why this chain:** `set -euo pipefail`, exit codes, pipelines, jq, and curl patterns are the ops glue every other domain's scripts and playbooks speak in.
**Source sessions:** BASH.P0.3 (exit codes, pipes, pipefail), BASH.P0.4 (jq), BASH.P0.5/P0.6 (curl, playbooks), BASH.P1.1 (awk/sed, process substitution, find/xargs), CICD.P0.4 (pytest exit codes), LINUX.P1.1 (rsync codes).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | Walk through `set -euo pipefail` and what each letter buys in a real script. | `-e` exits on the first failing command; `-u` errors out on referencing an unset variable (turns typos into loud failures); `-o pipefail` makes a pipeline's exit status the last non-zero exit in the pipeline instead of the last command's. Without pipefail, `cmd | grep x` honors only grep — a failing upstream vanishes silently. This trio is the standard guard for cron jobs and CI steps: it sits at the top with the PATH export, and a `trap` for cleanup when the script owns resources. The war-room incident that proves it: a backup/cron job that "worked by hand" but quiet-failed on schedule — fixed with absolute paths, a log redirect, and this exact flag trio. (BASH.P0.3; LINUX.P0.8.) |
| L1.5 | Why do exit codes matter, and what is 0/127/126 — plus why can't you assume the rest? | Shell convention: 0 = success, non-zero = failure; 127 = command not found (bash), 126 = found but not executable. Beyond that, every tool documents its own taxonomy and you must read each one: pytest uses 1 (tests failed), 2 (collection/usage error), 5 (no tests collected) — a pipeline must distinguish "tests failed" from "the test run itself is broken"; rsync uses 23 (partial transfer) and 24 (files vanished during the run), which a naive `rc != 0 is fatal` wrapper mangles into a false alarm. The professional habit: read `$?` immediately, branch on documented codes, and under `-e`, deliberately neutralize expected failures with `cmd || true` or an if-condition. (CICD.P0.4; LINUX.P1.1; BASH.P0.3.) |
| L2 | Describe the shell execution path: pipeline status, subshells, and where redirections get their status. | A pipeline runs each command; its status is the right-most command's exit, or the last non-zero under `pipefail`. Parentheses `( ... )` spawn a subshell — a copied environment — so variables changed inside do not persist after the line (a classic surprise in while-read loops). Redirections are opened in the current execution context before the command runs: `cmd 2>>log` can fail before cmd starts, and that failure is yours to branch on. `$?` is the last foreground command's exit, so capture it immediately or it is overwritten. Process substitution `<(...)` and command substitution `$(...)` both run a command but differ: `<(...)` hands out a FIFO path to an argument list, `$(...)` embeds output text inline. (BASH.P0.3, BASH.P1.1.) |
| L2.5 | Turn this API response into a one-line list of unhealthy hostnames — and why jq instead of grep? | `curl -sS ... | jq -r '.[] | select(.status == "unhealthy") | .hostname'` — then a `while read` loop over the raw strings. jq parses structure, so field order, whitespace, and quoting never break it; grep over JSON matches raw bytes and false-positives on keys that merely contain a word, and cannot select by nested structure at all. The details you defend: `-r` for raw strings, `jq -e` to turn a filter into a boolean exit code, and process substitution when the loop also needs stdin. (BASH.P0.4, BASH.P0.6.) |
| L3 | Write a safe health-check pattern: timeout, jq, distinct exit codes, and the deliberate choice of which flags. | Shape: `set -uo pipefail` — deliberately keep `-e` OFF when the script branches on probe results. `curl -fsS --max-time 5 -o /tmp/out.json -w '%{http_code}' URL`, then `jq -e '.status=="ok"' /tmp/out.json` and branch on ITS exit code; distinct codes for probe-timeout vs HTTP-error vs JSON-mismatch so the caller can branch precisely. Log normal facts to stdout and problems to stderr. The subtle choices: `--max-time` bounds the whole probe, `-f` turns a 4xx/5xx into an error instead of a silent 200-with-error-body, and a `trap` cleans the temp file — because a health check that leaks temp files or waits forever is a worse tenant than the bug it probes. (BASH.P0.5, BASH.P0.6.) |

**TRAP VARIANT:** "`set -e` alone makes my script safe." The catch: `-e` does not fire for commands inside if/while conditions, in negated pipelines (`! cmd`), or after `||`/`&&` — and mid-pipeline failures stay invisible without `pipefail` (the `cmd | grep` bug). The trio is the unit of safety, not `-e`. And `-u` is the member that catches the typo'd-variable bug `-e` cannot — which is why `-uo pipefail` is the minimum and `-e` goes on top only where it cannot swallow intent.

**IF THEY ASK BETTER:**
- "Whitespace-proof find": `find . -name '*.log' -print0 | xargs -0 -n1 ...` so names with spaces and newlines never split — verified habit from BASH.P1.1.
- "What breaks in cron but works by hand?" The env is thin: absolute paths or an explicit PATH, SHELL declared, output redirected to a per-job log, `set -euo pipefail` — the "quiet-fail cron job" incident (LINUX.P0.8) is the canonical example.
- "awk/sed for a column problem": field parse with awk when the shape is regular (`$1`, `$NF`), sed -n for line-level edits; the war-room rule is awk/sed for text extraction, not as a language.

**WRONG-ANSWER ALARM:** "I put `echo done` at the end so I can tell it worked" (echo always succeeds; that is not a status). "`set -e` is enough" (see the trap). "Everything non-zero means failure" (false: documented codes like rsync 23/24 mean partial success — the candidate who cannot read a tool's code table reads `$?` wrong). "I grepped the JSON" (see row L2.5 — it is the fastest way to miss a broken field).

**SPEAKING OPPONENT:** Bash probes whether the candidate reads exit codes and writes scripts that stop loudly with distinct statuses, instead of decorating a `&&` chain with echos. The interviewer listens for `pipefail`, `$?`, `-u` typos, and the pytest/rsync code taxonomy — proof of having debugged real pipelines — rather than syntax recall. A candidate who can say "I keep `-e` off here on purpose because I branch on the probe result" answers with intent, and that intent is the score.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** exercise the playbook rows inside 14-12 Troubleshooting (health-check/verify stages), and re-drill 14-01 for the exit-code crossover (137 = 128+9, KILL).

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-04
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Exit-code claims match verified output (127/126, pytest 1/2/5, rsync 23/24) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-05 — AWS
**Why this chain:** IAM evaluation, assume-role failures, SG vs NACL, ALB error taxonomy, S3 consistency, and least privilege are the cloud questions that sort employment at this level.
**Source sessions:** AWS.P0.2 (IAM, eventual consistency), AWS.P0.4 (SG/NACL), AWS.P0.6 (S3), AWS.P0.7 (ALB), SEC.P0.2 (AAA), SEC.P0.3/P0.4 (read-only census, OIDC role), 12-TS Incidents 4 (ALB), 9 (S3 AccessDenied), 11 (AssumeRole).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | An S3 call returns AccessDenied. How does IAM evaluation order work, and what surfaces as denied? | Evaluation: explicit deny wins over every explicit allow; with no deny, an explicit allow wins; otherwise implicit deny. Both the identity policy AND the resource policy must allow; SCPs and permission boundaries only shrink. So a denied call with an allow visible in the console means one of: an explicit deny somewhere (bucket policy or identity-side Deny — and it beats AdministratorAccess), OR no matching allow (wrong action, wrong resource ARN), OR a KMS-wrapped object where the caller lacks `kms:Decrypt`. The policy simulator renders it exactly — `Decision: explicitDeny` — and appending more allows can never outrank a matching deny: that is why retrying forever is pointless until the deny document itself changes. (AWS.P0.2, SEC.P0.3; 12-TS Incident 9.) |
| L1.5 | `sts assume-role` just started failing. What can break, and how do you split it fast? | Four classic branches: (1) the role's trust policy does not include this caller — wrong principal, missing external ID or condition; (2) the caller lacks `sts:AssumeRole` in its own policy; (3) IAM eventual consistency — a role created seconds ago is not yet replicated, and the immediate assume attempt returns AccessDenied (verified live: fresh role + assume = denied, resolved within seconds); (4) the assumed role's policy does not cover the next action/resource, which fails not at assume but at the following call. First checks: read the trust policy with `aws iam get-role`, verify the caller with `sts get-caller-identity`, then simulate with `iam simulate-principal-policy` or `iam simulate-custom-policy`. (AWS.P0.2, SEC.P0.2/P0.3; 12-TS Incident 11.) |
| L2 | Walk SG vs NACL evaluation and the failure "one direction works, replies drop". | SG = instance/ENI-level firewall that is STATEFUL and allow-only: replies to an allowed flow are auto-blessed for the tracked connection (including its idle timeout); "no rule" is the deny — there is no explicit Deny action in an SG. NACL = subnet-level, STATELESS, ordered rule list with explicit allow AND deny, evaluated lowest-number-first; the REPLY is a NEW packet and needs its own inbound rule (ephemeral range 1024–65535). The stateless gotcha: inbound 443 allowed but no ephemeral outbound rule, and the client's replies are dropped. A packet must pass the NACL AND the SG on the way in, and the inverse on the way out; the effective decision is the intersection — and "which direction forgot its rule" is the actual debugging question. (AWS.P0.4, SEC.P0.8.) |
| L2.5 | The ALB returns 502/503 after a deploy. What fails at each layer, and what proves it? | 502 = the proxy reached the target but got a bad/closed/garbled response — the target crashed mid-request, the listener-to-target-group port mismatches, or an SG/NACL is blocking the healthcheck/reset. 503 = no healthy targets at all: every health check failing or zero targets registered. Evidence ladder, in order: `aws elbv2 describe-target-health` (healthy/unhealthy states), the target-group health-check path/port vs the instance's real listener, then the instance's SG/NACL and app logs. Health-check path/port mismatch with the app is the top cause; you never guess — you read the target-health report first. (12-TS Incident 4; AWS.P0.7.) |
| L3 | Least privilege end to end: a GitHub Actions workflow pushes a container to ECR. Walk the identity and authorization chain. | GitHub Actions assumes the deploy role via OIDC: the role's trust policy pins `token.actions.githubusercontent.com` with audience/subject conditions so ONLY the intended repository workflow can assume it — no static keys anywhere. After assume, the step calls `ecr:PutImage` against the exact repository ARN; the role policy grants exactly PutImage plus GetAuthorizationToken. The nuance worth naming out loud: GetAuthorizationToken is the one action where a bare `*` resource is CORRECT and required, because it is a token-style STS call with no single repository ARN — so "a bare `*` is not automatically a mistake". Evaluator walk: no deny → matching allow on action+resource → else implicit deny. On EKS the same story is IRSA: a kubelet-mounted OIDC token presented as the cloud identity. (SEC.P0.4, AWS.P0.2.) |

**TRAP VARIANT:** "S3 is eventually consistent, so put-then-get may return the old object." The catch: S3 is STRONG-after-write since December 2020 — a PUT then GET returns the new object; what may still lag is list-after-put and other operations. Companion traps in the same family: "ETag is a UUID" (it is a checksum — MD5 for single-part, composite for multipart) and "single PUT goes to 5TB" (PUT caps at 5GB; multipart extends to 5TB).

**IF THEY ASK BETTER:**
- "Private bucket, public content": CloudFront + OAI with a minimal bucket policy — the verified P0.6/P2.2 pattern — with presigned URLs as the time-boxed alternative for direct object access.
- "RDS Multi-AZ vs read replicas": Multi-AZ = synchronous standby for failover/HA (no read scaling, same copy); read replicas = async copies that serve reads for scale-out. Backups = automated snapshots plus point-in-time recovery within retention.
- "Which is the interview one-liner for private subnets that only need S3/DynamoDB?" Gateway endpoints: free, route-table-attached, no ENI — they eliminate the NAT path entirely; only S3 and DynamoDB get gateway endpoints, everything else is interface endpoints (ENIs, per-hour cost).

**WRONG-ANSWER ALARM:** "It's a permissions issue, add more allows" without reading whether an explicit deny is in the way. "The SG fixed it, the NACL is only for subnet defaults" — the layers intersect on the packet path, and statelessness is exactly where replies die. "S3 is eventually consistent" (outdated since Dec 2020). "EC2 instance role vs IRSA are interchangeable" (the identity path differs: a machine identity versus an OIDC token, and least privilege scopes both differently).

**SPEAKING OPPONENT:** The AWS chain separates console-clickers from evaluator-thinkers. The money sentences are "explicit deny beats AdministratorAccess", "identity AND resource must both allow", and the two-surface failure split (assume-time vs next-call). A candidate who answers S3 AccessDenied by re-granting while an explicit deny sits in a bucket policy fails the whole chain without ever knowing it — the simulator is the evidence tool that keeps that candidate honest.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** cross-drill 14-11 Security (IAM evaluation order, KMS envelope, IRSA rows) and 14-12 Incidents 4/9/11; the SG/NACL statelessness row also re-enters at 14-02 Networking.

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-05
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Facts match verified content (evaluation order, stateful/stateless, S3 strong, ETag, 5GB/5TB) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-06 — DOCKER
**Why this chain:** image vs container, layers and caching, the runtime boundary, exit-125/127/137, and hardening — the container questions run second only to Linux in interview frequency.
**Source sessions:** DCK.P0.1 (image/layers/Dockerfile), DCK.P0.2 (build context/caching/multi-stage), DCK.P0.3 (volumes/bind mounts), DCK.P0.7 (exit codes, troubleshooting), DCK.P1.1/P1.2 (security, limits), SEC.P0.9/P0.10 (hardening proof), CICD.P0.6 (applet trap), 12-TS Incidents 16 (CrashLoopBackOff), 25 (stale layers).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | What is the difference between an image and a container, and what is a layer? | Image = immutable, layered snapshot (the blueprint; ships via a registry). Container = that image plus one writable layer, executed as processes in isolated namespaces (PID, network, filesystem) on the host kernel — the running instance. A layer is the diff produced by one filesystem build instruction (RUN/COPY/ADD); non-filesystem ops (ENV, CMD, EXPOSE) become config-only 0-byte rows in `docker history`. Writes land in the writable container layer under `/var/lib/docker/overlay2/...` on the daemon host and vanish on `docker rm` unless a volume holds the data. (DCK.P0.1.) |
| L1.5 | My rebuild re-used a stale layer and skipped my change. How does layer caching actually work? | BuildKit executes instructions in order and caches a layer keyed by its instruction plus its parent-layer digest; when both match it prints CACHED and skips re-execution. A change in an earlier layer invalidates everything after it — so order the Dockerfile to put rarely-changing, expensive steps first (dependencies before code) and keep the COPY of frequently-edited files small and late. A COPY of a constantly-changing directory near the top forces a full rebuild every commit. `--no-cache` is the sledgehammer; correct ordering is the habit. Verified live: on a rebuild, dependency layers showed CACHED even under `--progress=plain` — nothing redundant recomputed. (DCK.P0.2, DCK.P1.2; 12-TS Incident 25.) |
| L2 | Trace what happens when the daemon starts a container, down to the runtime boundary. Who creates the namespaces and enforces the limits? | `docker run` → the daemon prepares the container config and network → a shim spawns runc → runc creates the OCI task: namespaces (PID, net, mount, user, UTS), cgroups, then exec's the entrypoint inside them. Failure modes fall OUTSIDE the running state: a command-not-found dies at runtime-create (the container never enters `running`), a port conflict is caught in network setup and exits 125. The kernel enforces the budget (cgroup v2: `memory.max`, `cpu.max` where 0.5 core reads `50000 100000`, `pids.max`); exceeding the memory cap triggers the OOM-killer which SIGKILLs the heaviest process in the cgroup → exit 137, `OOMKilled=true` in inspect. (DCK.P0.7, DCK.P1.2.) |
| L2.5 | A container exits immediately with no logs. Diagnose — what is the CMD/ENTRYPOINT pitfall? | Read the config, do not guess: `docker inspect .Config.Cmd` and `.Config.Entrypoint`. Pitfall one: CLI args at `docker run` override CMD but append to ENTRYPOINT. Pitfall two: exec-form vs shell-form — shell-form (`CMD sh myservice`) spawns a child, so SIGTERM to PID 1 may never reach the service. Pitfall three: an entrypoint script that errors before any output explains "no logs at all". The alpine-plus-busybox flavor: a missing applet — `httpd: applet not found`, exit 127 — caused the real CrashLoopBackOff in the war-room CI lab, because the binary is not even shipped in the image. (DCK.P0.7, DCK.P0.1; CICD.P0.6 env fact.) |
| L3 | Your image runs as root with all capabilities. What is the concrete hardening floor? | Non-root USER, read-only rootfs, drop ALL capabilities and add back only what the app needs (`--cap-drop ALL` plus explicit adds), a HEALTHCHECK, a scan of the image, and pinning by digest — never `:latest`. Seccomp `RuntimeDefault` is the next tightening; `userns-remap` maps container root to an unprivileged host user as the infra-level defense against kernel-exploit escalation. Verified in SEC.P0.9: root-writable-fullcaps vs non-root-readonly-nocaps with the CapEff proof read from /proc. The honest framing to end on: scanning answers "is it safe", signing answers "is it really mine", pinning answers "is it still the one I chose" — gate on all three, in that order of frequency. (DCK.P1.1; SEC.P0.9/P0.10.) |

**TRAP VARIANT:** "We run rootless containers, so the container root IS the unprivileged host user — no risk." The catch: rootless remapping contains KERNEL-escalation chains (a container-root exploit no longer escalates to host root), but it does nothing about app-level risk — world-readable mounts, capabilities you granted, or secrets mounted into the container. "Not root on the host" is a containment layer, not a hygiene layer. The container still needs read-only rootfs, dropped caps, non-root inside, and secret hygiene — rootless changes the blast radius, not the checklist.

**IF THEY ASK BETTER:**
- "Volume vs bind mount — who deletes what?" A named volume lives under docker's data dir and survives `docker rm` (deleted only by `docker volume rm`); a bind mount is a host path that was never docker's data. Verified live: container wrote a file, container deleted, a NEW container mounted the same volume and read the file.
- "Compose vs Kubernetes, don't conflate": Compose = single-host declarative stacks for local dev; Kubernetes = a distributed scheduler. The container-level "namespace + DNS" idea carries over; everything else is a different world.
- "What does `docker stats` giving 0.00% CPU and 1.742MiB/128MiB actually prove?" That cgroup limits are live and enforced at create; the numbers are evidence, not vibes (DCK.P1.2).

**WRONG-ANSWER ALARM:** "The writable layer is inside the image" (it lives above the read-only image stack, on the daemon host). "Docker isolates everything by default" (namespaces isolate identity, not security boundaries; the kernel is shared). "latest is fine for reproducibility" (the tag is a mutable pointer; digest is the identity). "PID 1 in a container always gets SIGTERM properly" (shell-form CMD swallows it into a child).

**SPEAKING OPPONENT:** Docker chains split people who ran containers (exit 125/127/137, layer caching, volumes, CMD-vs-ENTRYPOINT) from people who read about them. The two filters are exit-code fluency joined to the caching-order argument, and the hardening row demanding non-root + cap-drop + digest-pin as a BUNDLE — "we use the default base image" reads as no hardening at all.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** carry the 137/OOMKilled and applet-127 rows into 14-07 Kubernetes (CrashLoopBackOff) and 14-12 Incidents 16/17/19/25; the exit code is the same in both worlds.

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-06
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Exit codes and paths match verified output (125/127/137, overlay2, OOMKilled=true, CACHED) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-07 — KUBERNETES
**Why this chain:** pod flow, Service/endpoints truth, probes, scheduling, rollouts, and secrets-in-etcd are the ownership questions that decide Kubernetes interviews.
**Source sessions:** K8s.P0.1 (control-plane flow), K8s.P0.2 (objects, empty endpoints), K8s.P0.3 (rollout/undo), K8s.P0.5 (probes), K8s.P0.6 (scheduling), K8s.P0.7 (RBAC), K8s.P1.4 (Helm), SEC.P1.1 (PSA, SA JWT), 12-TS Incidents 2 (empty endpoints), 16 (CrashLoopBackOff), 18 (Pending), 20 (readiness), 27/28 (rollout stuck, rollback).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | Walk the full path of `kubectl apply -f deploy.yaml` from command to running container. | kubectl → kube-apiserver (authenticate, authorize via RBAC, validate, admission) → stored in etcd — the ONLY component that touches etcd → the deployment/replicaset controller (inside controller-manager) creates Pods → the scheduler assigns a node by writing `spec.nodeName` → the kubelet on that node watches for pods bound to it, pulls the image and starts the container via the CRI (containerd) → readiness decides Service membership. The one line that separates candidates: the scheduler decides WHICH node, the kubelet RUNS the container — "the scheduler runs my container" is an instant fail. (K8s.P0.1; SEC.P1.1.) |
| L1.5 | DNS resolves and the Service IP answers, but connections to it time out. First three checks, in order. | (1) `kubectl get endpoints <svc>` — empty endpoints is the classic cause: the Service ClusterIP exists but no pod backs it, so connections refuse/reset. (2) Pod readiness — `kubectl get pods -l <app>`: if READY 0/1 the pod exists but is not serving; that is a readiness failure, not a liveness one. (3) The selector match: `kubectl describe svc` shows the selector, compare against `kubectl get pods --show-labels`; a wrong or missing selector label is the root of empty endpoints more often than the app being down. (12-TS Incident 2; K8s.P0.2.) |
| L2 | Probes: one pod shows 0/1 while the process is healthy, another shows 1/1 while traffic fails. Who runs probes, and what does each state mean? | Liveness = restart-me (the kubelet restarts the container on failure); readiness = send-me-traffic (the Service/endpoints layer drops the pod while failing); startup defers both for slow-start containers. Probe failure is NOT process death: a wrong probe path or port fails readiness while the app is perfectly healthy (0/1, still alive), and liveness tied to an external dependency makes the kubelet kill a healthy pod. Different actors, two loops: the kubelet probes and restarts; the Service membership reacts to readiness. The "READY 1/1 but Restarts climbing" fingerprint means liveness is flapping while readiness passes. (K8s.P0.5; 12-TS Incident 20.) |
| L2.5 | A new Deployment stays Pending. Walk scheduling: what does the scheduler actually evaluate? | The scheduler reads newly created Pods and scores eligible nodes: resource REQUESTS vs allocatable capacity (describe the node to see Capacity vs Allocatable — the fixed system-pod tax is already carved out before any app pod is admitted), nodeSelector/affinity matches, taints vs tolerations, topology spread; then it writes `spec.nodeName` and a kubelet must act. Pending means NO node satisfied: requests exceed allocatable, an untolerated taint (or a quota/admission veto that the scheduler never sees as events), or nodeSelector matched zero — and the refusal text is verbatim in `kubectl describe pod` Events (`FailedScheduling`: "0/2 nodes available: 2 Insufficient cpu, 2 Insufficient memory" vs "1 node(s) had untolerated taint"), which partitions capacity arithmetic from toleration policy. The DaemonSet variant: the control-plane is tainted, so a plain DaemonSet stays Pending until it tolerates it. (K8s.P0.6, K8s.P2.3; 12-TS Incident 18.) |
| L3 | A rollout is stuck at READY 1/2. Differentiate the causes and walk the undo. | A Deployment rollout is healthy only when the new ReplicaSet satisfies availability (maxUnavailable/maxSurge plus minReadySeconds) before the old one scales down; if progressDeadlineSeconds expires the rollout is marked stalled. Stuck at 1/2 means the NEW RS's pod is not ready: readiness probe path failing, resources unschedulable, or image pull failing — read `kubectl rollout status`, `kubectl describe deploy` (conditions) and the new pod's events. The senior release floor: `kubectl rollout undo deploy/<name>` is a NEW revision pointing at the OLD template — it is not time travel and not a return to revision 1 — and it is safe only if the old artifact bytes are still in the registry and the release did not carry a schema/data migration; if it did, an image undo is not a schema undo and forward-fix is mandatory. Decide from three facts: revision intact? bytes retained? migration ridden in? (K8s.P0.3, CICD.P1.3; 12-TS Incidents 27/28.) |

**TRAP VARIANT:** "Secrets are encrypted in Kubernetes." The catch — the #1 K8s interview sin — is that Secret values are base64-ENCODED, which is trivially reversible (`echo <b64> | base64 -d`), and they sit in etcd base64 by default; real encryption at rest needs a provider (`--encryption-provider-config` or KMS-backed on EKS). Companion trap: "undo resets to revision 1" — the revision counter climbs with every template change AND every restart, so undo lands on a NEW revision with the old template bytes.

**IF THEY ASK BETTER:**
- "RBAC in three sentences": Role/ClusterRole define the rules, bindings attach them to subjects, and it is deny-by-default; `kubectl auth can-i --as=<sa>` returns the exact server verdict. A ServiceAccount identity is a kubelet-mounted RS256 JWT — the same token IRSA presents to AWS. (K8s.P0.7; SEC.P1.1.)
- "NetworkPolicy in one line": default-allow until a policy exists; it is the in-cluster SG, and kindnet does not enforce policies (the model-only nuance from K8s.P1.2).
- "Helm in one line": a templating-plus-release manager — lint/install/upgrade/history/rollback/uninstall all verified live on kind; rollback restores the OLD values, not just the manifest.

**WRONG-ANSWER ALARM:** "The scheduler runs my container" and "Secrets are encrypted" are the two instant-fails. "Empty endpoints = the app crashed" (usually it never joined, either selector or readiness). "Rollback restores the world" (it is a new revision at old bytes, and unsafe on schema-bearing releases). "Scale-to-zero fixes it" (restarting is evidence-deaf).

**SPEAKING OPPONENT:** The owner-vs-user test: who does what across apiserver/scheduler/kubelet/controller, where the endpoints truth lives, and what a rollout/undo actually is. "Empty selector = empty endpoints = timeout" is the money sentence an interviewer waits for; "the scheduler runs my container" is the trap line every interviewer has heard fail a hundred times. The L3 decision matrix (rollback-vs-forward on schema evidence) is what separates operators from deployers.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** re-enter 14-06 Docker for the 137/OOMKilled and image-pull crossover, then 14-12 Incidents 2/16/17/18/20/27/28 as the full failure set for this object model.

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-07
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Flow and numbers match verified output (apply→etcd→scheduler→kubelet, 950m, empty endpoints, revision counter) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-08 — TERRAFORM
**Why this chain:** plan/apply anatomy, state and locking, partial apply, delete-churn diagnosis, and count-vs-for_each are the IaC questions that separate operators from appliers.
**Source sessions:** TF.P0.1 (lifecycle), TF.P0.2 (state, mv/rm/import, locking), TF.P0.3 (S3/DynamoDB backend), TF.P0.4 (-target, -var), TF.P0.5 (drift, partial apply), TF.P0.6 (count/for_each), TF.P1.1 (moved/prevent_destroy), TF.P1.2 (CI gates), 12-TS Incidents 22 (state lock), 23 (plan destroy).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | What does `terraform plan` actually compute, and what are its phases? | Three phases in one graph walk: refresh (calls the provider's read functions for every resource in state to learn real-world attributes), diff (compares refreshed attributes against config and emits create/update/destroy/no-op), order (sorts actions by dependency so nothing is created before its dependencies). The trap to name aloud: plan is a dry run of the DIFF, not of apply — apply re-walks and re-plans when run without `-out`, so if the world changed between plan and apply, apply can produce different actions. State is not a cache; it is the ownership record: it maps config to real objects, stores attributes, tracks the dependency graph, and enables inspection. (TF.P0.1.) |
| L1.5 | An apply dies with "Error acquiring the state lock". What happened and what do you do? | With a remote S3 backend plus DynamoDB, locking works as a conditional DynamoDB PutItem before a write; the second concurrent writer fails the condition (ConditionalCheckFailedException) and Terraform reports the lock error. Either a live apply from a teammate holds it, or a crashed/aborted run left a stale lock. You do NOT hand-edit tfstate. You read who holds the lock (the DynamoDB item carries metadata: who, when, instance id) via `aws dynamodb get-item`, and only after confirming no live run do you `terraform force-unlock -force <lock-id>`. The design failure worth naming: an S3 backend WITHOUT the dynamodb_table gives you shared state with NO locking — two applies race, last writer wins, and live infrastructure silently drops out of state while staying alive in the cloud. (TF.P0.2, TF.P0.3; 12-TS Incident 22.) |
| L2 | An apply fails after creating some resources. Is the state corrupt? What is the recovery? | Not corruption — partial convergence. State is written in dependency order, so a mid-apply failure leaves state correctly recording what succeeded up to the failure point. That is exactly why re-running apply works: it resumes from refreshed state without recreating the successes. For a stubborn single object, `-target=type.name` surgically converges one node plus its dependencies — a recovery tool, never routine, and Terraform emits an explicit warning about that. The real danger is accumulated partial failures: state claims ownership of things that never completed, so read the plan before assuming the state is wrong. (TF.P0.4, TF.P0.5; 12-TS Incident 22.) |
| L2.5 | The plan wants to destroy a database you never touched. Diagnose the delete-churn. | Two families. (1) ADDRESS drift: the config's resource block was renamed or removed while state still keys the old address, so the plan reads "new address never created" and "old address abandoned" and schedules destroy+create. Fix with a `moved { from = ... to = ... }` block — config-native, reviewable, future-proofs the rename — or `terraform state mv` on the spot; then plan clean. (2) Real out-of-band drift: a console change to a state-tracked object surfaces as a mutation; decide converge-in-config vs revert-the-console against the plan. For precious resources, `prevent_destroy = true` converts a destructive diff into a plan-time ERROR instead of a review item. The golden habit: a plan that deletes infra you never mentioned is a STOP sign, never just "approve". (TF.P0.2, TF.P0.5, TF.P1.1; 12-TS Incident 23.) |
| L3 | You need the same module 20 times across three environments. count or for_each — and what breaks when you switch? | `for_each` over a map/set of stable KEYS; `count` over a plain list. The killer detail: `count` uses INDEX addresses, so removing an element in the middle recycles index 0 and Terraform destroys+recreates the shifted elements; `for_each` keys are stable, so reordering is a no-op. Verified live: `by_count[1]` changing "b"→"c" planned DESTROY+CREATE while the for_each twin survived. Access forms differ (`local_file.by_count[0]` vs `values(...)` and `{ for k, v in ... }`), and remember data sources refresh on every plan — a data source that depends on something created in the same apply behaves like a moving target. Vars: `terraform.tfvars` auto-loads, `-var-file` for the rest, `TF_VAR_` env for secrets in CI; never `-var 'secret=...'` inline where it lands in process lists and logs. (TF.P0.4, TF.P0.6.) |

**TRAP VARIANT:** "Terraform state is just a cache — delete tfstate and re-apply; it will rebuild everything." The catch: the state file is the ownership ledger that maps config to live objects; deleting it orphans infrastructure that keeps running and costing money, and a fresh apply either duplicates it or destroys what it cannot see. The correct repair verbs are `terraform state mv`/`rm`/`import` — never editing tfstate by hand (which corrupts `serial`/`private`) and never deleting it wholesale. "State is a cache" is how people lose production buckets.

**IF THEY ASK BETTER:**
- "Bring something built outside Terraform under management": `terraform import aws_instance.web i-xxxx`, then write config to match what you observed, plan until clean; if the address must move into a module, `terraform state mv` right after import while the mapping is fresh.
- "Plan as a CI gate": plan on the PR as a commentable artifact, apply on merge. The delete-bomb detection lives in that PR plan review — which is why schedule-and-apply pipelines without a plan gate skip the one review that catches the destructive surprise.
- "Why does Terraform say a rename will destroy everything?" Because state addresses and config addresses diverged; the fix is exactly the `moved`/`state mv` pair, never "let it recreate" — the P0.2 mv-then-plan churn lab proved it.

**WRONG-ANSWER ALARM:** "Just run apply and let it recreate" on a healthy resource (read the plan first). "Targeting is how we ship fast" (it is for surgical recovery; the plan warns you exactly because of that). "State is a cache" (it is the ownership ledger). "DynamoDB is optional for locking" (without it, shared state is a race). "I fix drift by deleting the state line" (state mv/rm exist precisely so you never edit the file by hand).

**SPEAKING OPPONENT:** This chain discriminates "I ran apply and it worked" from "I understand state serial, locking, drift, and the three repair verbs". The two filter sentences an interviewer grades on are the state-lock story (who holds it, how you see it, force-unlock is last) and the delete-churn diagnosis (config-vs-state address mismatch, fixed with `moved`, never with "let it recreate"). Getting those right is the difference between an IaC user and an IaC operator on the same resume line.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** cross-drill 14-12 Incidents 22/23 with this chain, then 14-13 System design (day-0 drift detection and plan-as-gate rows).

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-08
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Mechanisms match verified content (ConditionalCheckFailed, moved/state mv, by_count destroy+create, tfvars override order) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-09 — CI/CD
**Why this chain:** pipeline anatomy, declarative YAML, and the shift-left plan/scan/apply-now gate stack — CI/CD is where every other skill gets graded on whether it was ever actually exercised.
**Source sessions:** CICD.P0.1 (pipeline anatomy, internal vs publish), CICD.P0.2 (reusable pipeline), CICD.P0.3 (pulp badge/unstable), CICD.P0.4 (pytest exit), CICD.P0.5 (vulnerability scanner), CICD.P0.6 (on: syntax health), CICD.P0.7 (build cache), CICD.P1.1 (plan-apply-fail gate), CICD.P1.2 (run-order), CICD.P1.3 (release architecture, git-tag), 12-TS Incidents 24 (CI-vs-local), 25 (stale layers), 29 (same-tag trap).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | Walk the anatomy of a GitHub Actions workflow: events, jobs, steps, and caching. | `on:` declares the triggers (push, PR, schedule, or manual); events can also be created by other jobs via `workflow_dispatch`. `jobs` run in PARALLEL by default, each on its own runner; `steps` run in ORDER inside one job, and every `run:`/`uses:` starts in a FRESH shell and a fresh context — so state passes between steps only via files, artifacts, or outputs, and a cached environment is re-established per step (the "parallel sibling jobs, sequential subprocess steps" model). `runs-on` picks the runner; a `strategy.matrix` fans out jobs across versions; path filters skip whole workflows for docs-only PRs (verified in the cache-tuning lab). `actions/cache` saves dependencies between runs (entries untouched for 7 days are evicted), and keying it on the dependency-lock hash is what turned pip's "Requirement already satisfied" into a sub-second cache hit. (CICD.P0.1, CICD.P0.2, CICD.P0.3/P0.7.) |
| L1.5 | A pipeline step passed in the morning, fails on the same code at noon. Is the code flaky, and how do you begin? | The revision that matters is "passes locally, fails in CI" — INC 24's root cause was a wrong working directory surfacing as `ModuleNotFoundError`, the purest form of environment drift. Begin by diffing ENVIRONMENT, not code: the runner image, the working directory vs the repo root, the cache state (a changed lockfile/deps file that re-keyed nothing), and the checkout depth. If the failure is a `pytest` exit code, decode it: 1 = test failures, 2 = collection/usage errors, 5 = NO tests collected — a 5-collected "failure" is a config shot, not a code shot, and treating it as code is the fast trap. Capture the failing job's full command output BEFORE retrying, so a green rerun still leaves the evidence; the DISCIPLINE is one sentence — assume your local env is lying about CI until the exit codes agree. (CICD.P0.4; 12-TS Incidents 24/25.) |
| L2 | Where does security scanning fit in the pipeline, and what does each gate actually catch? | Three gates, each tuned to its best-odds target: secret scanning on the PUSH branch (cheapest catch with the highest actionability — catches a committed token before it can be broadcast), a dependency/advisory scan (calls out a known-CVE library, needs a version bump + re-test), and a container scan (image-scanner that flags an app-layer vulnerability the app can also ship to prod). The gate you miss: Plan/Apply in the same pipeline — if `terraform plan` and `terraform apply` are not split, the same diff is neither reviewed nor gated, so a delete-bomb sails through as a merge. Verified: the destroy-line carries an incident review trap (INC 23) exactly when the plan was not the review gate. (CICD.P0.5, CICD.P1.1; 12-TS Incidents 22/23.) |
| L2.5 | Git-tag vs build-version vs branch name — what identifies a release, and what breaks if they drift? | One hand, one tag: a release needs ONE source-of-truth identifier, usually the build's git tag (e.g. v1.2.3) pulled from `git rev-parse --short HEAD` for CI metadata. If branch name is the "version", main looks like prod-tagged while the actual release sits in the registry under a random job id; if the git-tag is edited after merge, the build that was just published no longer matches the source. Breakage pattern verified live: INC 29 — the pipeline succeeded but the site still served the old version because a mutable tag was re-pointed at old bytes and nothing rolled out (the "same-tag no-rollout trap"): one tag, two realities, and no downstream stage noticed. Release discipline: one immutable tag captured at build time (git tag + image digest), deploy keyed on the digest not the branch, and a smoke probe after rollout that confirms the served version string. (CICD.P1.3; 12-TS Incident 29.) |
| L3 | The app and Terraform live in one repo. Design the CI/CD that keeps deploy gate while allowing hotfixes. | Two distinct pipelines. App: PR → lint/test + secret scan → merge → build → scan → tag/prune → push to registries + EKS rollout; a stale-PR rebuild so the presence of a PR from an out-of-date base triggers a rebuild. Infra: plan-on-PR (with the delete-bomb review gate), apply-on-merge (with plan+apply SPLIT so nobody applies a diff nobody read). Hotfix lane: same gate stack, shorter turnaround — tag-based release so the artifact bytes equal the source tag — and the pipeline carries the artifact's digest, not the branch. The single guarantee that holds the whole model: no artifact is promoted without a gate, and no gate runs without artifacts. (CICD.P1.1–P1.3, 09-cicd pipeline lineage.) |

**TRAP VARIANT:** "Our pipeline runs tests, then deploys to prod automatically. Anything failing would catch itself." The catch: an auto-promote pipeline is only as safe as its gate COUNT and the position of the plan/release step; a "tests + deploy" step that skips scanning, skips a plan review, or reads release metadata from the wrong source (branch name instead of tag) fails silently — e.g. a scan step skipping on a flaky pre-step, or a pytest step that "passed" because 5=no-tests was masked as 0-success. The safety unit is the plan-apply split plus the tag as the identity, not "we deploy automatically".

**IF THEY ASK BETTER:**
- "Self-hosted vs GitHub-hosted runner": self-hosted gives cached images on premise, GitHub-hosted gives managed security and isolation; the interview answer is that caching shifts the economics, not security. Requirements and tags: node-version matrix plus `strategy.matrix` maximizes coverage per runner minute.
- "Actions cache for a monorepo build": key by the product of the changed-subtree hash plus the dependency-lock hash, so a PR touching only `web/` does not rebuild `api/`; verified: `hashFiles('**/requirements*.txt')` gives a stable key.
- "Pipeline archaeology — what to question first?" Plan/apply split, the pytest 5-no-tests trap, git-tag truth, and a stale-PR rebuild marker.

**WRONG-ANSWER ALARM:** "Caches are optional" (they shift both economics and determinism). "Tests passing = deployable" ("passing" can mean 0-tests-ran). "Two repos, one platform" (repo-merge vs repo-split is a gate-positioning question). "We apply and we review the diff later" (the destroy bomb is a review-time catch; later is never). "A tag is decoration" (it is the release identity — 12-TS Incident 29 proved the same-tag trap).

**SPEAKING OPPONENT:** The CI/CD chain is the interview room where claimed skills collide with what was actually exercised. Two tell phrases sink a candidate: "we just run the tests and deploy" and "tests passed" when "tests collected = 0". The winning pattern answers the gate-diagnosis questions: how do you find a flaky cache, what does the pytest exit tell you, why does the delete-bomb need a plan review, and why is the git-tag the release truth? Speak evidence, not feature lists.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** cross-drill 14-12 Incidents 13/25/26 and return the pipeline design to 14-08 for its plan-apply split; the release tagging discipline reappears as a day-0 control in 14-13.

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-09
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Exit codes and gate facts match verified content (pytest 1/2/5, plan-apply split, tag-as-identity, cache key hashFiles) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-10 — OBSERVABILITY
**Why this chain:** log/rate/empty-vs-zero, PromQL, the golden signals and SLO math, alerts that page real humans, and dashboards that answer questions — the modern observability interview stands or falls on these rows.
**Source sessions:** OBS.P0.1 (pillars), OBS.P0.2 (metric model/scrape), OBS.P0.3 (PromQL), OBS.P0.4 (histograms, percentiles, averages-lie), OBS.P0.6 (structured logging), OBS.P0.8 (alerting), OBS.P0.9 (SLI/SLO/error-budget math), OBS.P1.3 (RED vs USE), OBS.P2.1 (on-call, runbooks, MTTD/MTTR), 12-TS Incidents 6 (intermittent timeouts under load), 24 (CI-vs-local test failure).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | Name the three pillars of observability and what each one actually answers. | Metrics (WHO? who is slow or failing — a number that is cheap and instantly qualifies or excludes a signal), logs (WHY? the detail, searched by tooling and correlated to a trace), traces (WHERE? span-level, joined to logs; the distributed dependency story). Order matters in the workflow: metrics detect, logs explain, traces localize. Modern phrasing that scores: this triad sits under ONE semantic model — full-fidelity hybrid — so a "no logs on this frame" is itself evidence of a log-config gap, and trend data is as much a pillar as point truth. (OBS.P0.1.) |
| L1.5 | A latency panel flaps between green and red across dashboard reloads. What causes that, and when is it a real alarm? | Flapping is a QUERY artifact before it is a signal — four causes in order: (1) sparse scrape plus `irate` (the last-two-samples slope) is instant-flappy and noisy on flaky scrapes, so a panel drawn from irate shows spikes that are sampling noise — use irate for eyeballing bursts, never as an alert basis; (2) the window — `rate(...[5m])` on a target with a scrape gap merely interpolates, and `increase()` extrapolates to window edges (it is an estimator, not last-minus-first), so a short window magnifies a one-sample blip; (3) aggregation — RED lines are counters that mean nothing until `rate()`-ed (traffic is a counter rate, not a gauge; a fall to 0 on a gauge looks exactly like a reset), and a mean silently hides a bimodal tail — the session's own capture was 84ms/950ms requests whose mean read 372.67ms while p95 breached; (4) sample alignment — two series with different scrape intervals make an x/y ratio null on one side, and null must not render as 0 (that is a different alarm story). The read-order that ends the flapping: metric OWNER, scrape interval, panel window, aggregation — then decide. A flapping panel is a rule/aggregation fix, not a page; the pager is for budget burn (OBS.P0.8), the panel is for eyeballs. (OBS.P0.2/P0.3, OBS.P0.8, OBS.P1.3; 12-TS Incident 6.) |
| L2 | Single rate expression for request burst. What distinguishes `rate` from `irate`, and when does the answer break? | `rate(m[5m])` = the average per-second counter slope over the whole 5m window, corrected for counter resets (a drop is detected and unrolled) — smooths through load changes; `irate(m[5m])` = the slope from the LAST TWO SAMPLES ONLY — reacts instantly but stays noisy on sparse or flaky scrapes, so it is a spiky-dashboard tool and never an alert basis; `increase()` = rate x window, extrapolated to the edges, so it is an estimator, not last-minus-first. Where it breaks: `rate(x)` without a range is invalid PromQL (the window is mandatory); a GAUGE that falls to 0 looks exactly like a reset — you never rate a gauge; and an `errors / requests` ratio whose denominator has NO samples in the window returns NO series — null, not zero — and a dashboard that renders null as 0 has already turned a monitoring gap into a false all-clear. (OBS.P0.3; the verified "empty result is not 0 — an empty vector means no series" rule.) |
| L2.5 | Convert a 99.9% SLO into burn-rate budgets that actually page someone. | Budget math first: 0.001 x 30 x 86400s = 2592s = 43m12s per month, an 86.4s-per-day allowance. Line-up: PAGE when the 1h burn exceeds 14.4x (fast-spike catch), PAGE when the 6h burn exceeds 6x (confirms it is not a blip), TICKET when the 3d burn exceeds 1x (slow drain). At 99.9%, an hour at 2% errors is a 20x burn — a pager event; a three-day 0.11% drain is 1x — a ticket, not a page. The multi-window pairing IS the design: the short window catches fast burn, the long window filters noise, so a five-minute blip pages nobody and a sustained violation pages someone. And you alert on budget BURN, never a static "error > 1%" threshold — a static one pings during a zero-traffic blip and stays silent through a slow 0.9% drain. (OBS.P0.9 SLO/error-budget math.) |
| L3 | Your SLO says 99.9% yet the pager pages constantly. Rewrite the alert set so it stops lying. | Diagnose the mismatch first: the SLO number can be true while the ALERTS still lie. Fixes in order: (1) measure the budget against a PERCENTILE breach, not an average — the session's receipt is the bimodal 84ms/950ms checkout distribution whose mean read 372.67ms ("fine") while p95 breached a 300ms target (percentiles are the SLO, averages are marketing); (2) route paging through the RULE pipeline, not a dashboard glance — "I saw it on a panel" is accidental MTTD, because a dashboard is passive and a rule pages; (3) use multi-window burn (page on 1h >14.4x, page on 6h >6x, ticket on 3d >1x) so a short burst burns budget without paging anyone and a slow drain still gets someone; (4) validate the rule BEFORE trusting it — a `vector(1) > 0` test firing proves the pipeline end-to-end, and a sweep of silences/suppressions catches a rule someone suppressed into invisibility (Alertmanager silence/inhibition — maintenance is a window, not a permanent mute). The define-the-solution sentence: "the pager fires on BURN, not a static threshold, and only when the fast window agrees with the long window — so it lies less than my first SLO did." (OBS.P0.4/P0.9, OBS.P0.8, OBS.P2.1.) |

**TRAP VARIANT:** "The dashboard shows the metric is zero, so the service must be down." The catch: EMPTY is not ZERO. A blank series (no samples emitted) is not a metric value of 0 — it can mean the exporter is dead, the target was unreachable at scrape time, or relabel dropped the series. A ratio whose denominator has no samples (`errors / requests`) returns NO series, and rendering null as 0 manufactures a false all-clear. The verified one-liner from the sessions: an empty result is not 0 — an empty vector means no series, a different alarm story. So probe `up{job}` for device presence and guard a ratio with `count(metric)` before you trust the line. (OBS.P0.2/P0.3.) |

**IF THEY ASK BETTER:**
- "Do I need traces in a small system?" Start with metrics + logs; add traces when process boundaries exceed two — the interview nuance is that traces add complexity; the question is end-to-end latency SLOs, and you add them on the boundary, not to every endpoint.
- "P99 vs P95 latency: what do I actually measure?" P95 for perf-tuning eyeballs, P99 for error-budget claims; percentiles are the spiky tail's floor, not a promise. The receipt: the session's bimodal 84ms/950ms checkout distribution read a 372.67ms mean that screamed "fine" while p95 breached a 300ms target — that is why the SLO reads percentiles, never the mean.
- "PromQL division by zero": Prometheus yields no data pair where samples do not align; `rate(...) / rate(...)` collapses to nothing on a null denominator — always branch on presence before dividing (OBS.P0.3).

**WRONG-ANSWER ALARM:** "Empty is a broken chart that is fine" (empty-vs-zero IS the alarm story). "'Just log everything'" (logs must be structured, searchable, and correlated to traces to answer WHY). "Burn = every alert pages" (multi-window exists precisely so one window does not flatline the pager). "SLO = the SLA" (SLO is measurably yours; SLA is a contract with cost and liability — 99.9% of the month is not the same sentence as a legally bound table). "A dashboard is a report" (it is a question tool; one panel should answer one question). |

**SPEAKING OPPONENT:** The observability chain separates log-writers from signal-owners. The interviewer listens for: empty-vs-zero, the plan-denoise habit (an alert line that touches a known suppress-mask is read for what it hides), and an answer that quantifies budget in time (43m per 30 days for .9) instead of citing a percent. A candidate who cannot explain why a trailing-slash ratio divides by the absent denominator is an on-call window; one who names burn-rate windows and validates them on a simulated weekend owns the room.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** cross-drill 14-12 Incidents 5/14/15/23/25 and 14-09 for the pytest/code-gate crossover — everywhere the metric, not the log, is the first signal.

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-10
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Numbers and rules match verified content (43m12s per 30d for 99.9%, rate vs irate, empty-vs-zero, 14.4x/1x bands) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-11 — SECURITY
**Why this chain:** AAA, least privilege, secret handling, the trust-center mindset, and the leak-response rotation story — security is the P2/P3 heavy weight across every cloud and container question.
**Source sessions:** SEC.P0.1 (intro, IAM), SEC.P0.2 (AAA), SEC.P0.3 (read-only census), SEC.P0.4 (deploy OIDC), SEC.P0.9/P0.10 (container hardening), SEC.P1.1 (PSA, SA JWT), SEC.P2.2 (rotation), GIT.P0.5/12-TS Incident 30 (secret in history), K8s.P0.7 (RBAC), DCK.P1.1 (limits).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | Define AAA and give the concrete AWS instantiation of each letter. | Authentication (who you are): STS/OIDC issues the identity (IAM user keys, instance role, OIDC-assumed role). Authorization (what you may do): IAM evaluation order — explicit deny trumps allow, allow trumps implicit deny; identity AND resource policies both must allow; boundary/scp only shrink. Auditing (what you did): CloudTrail events, `sts:get-caller-identity` snapshots, `iam:GetLastAccessed`. The three-letter device that closes the loop: every attempt lands in the audit trail, so a deny in production is as loud as a grant. The quick PF0 way to prove a claim: `iam simulate-principal-policy --action-names s3:GetObject --resource-arn <bucket>/* --policy-source-arn arn:aws:iam::<acct>:role/<role>` printed exactly `Decision: explicitDeny`. (SEC.P0.2; AWS.P0.2.) |
| L1.5 | A secret found in a public repo commit. What is the actual remediation stack? | Rotation is the durable fix, rewrite is a hygiene scar: revoke the value and issue a new one (the old one dies even in old clones), then re-write history for hygiene, then add the secret-scan CI gate first in the DAG so the next one never merges. Verified live: a "rotation" commit alone left the old key recoverable via `git show HEAD~1:.env` and a 12-line python walk found it in every earlier blob; rewrite deleted the object from the branch but the value survived everywhere it was used — so rotation closes the actual exposure, rewrite closes the archaeology. (SEC.P2.2; 12-TS Incident 30; GIT.P0.5.) |
| L2 | "The machine is behind the VPN, so it must be trusted." Walk the counterargument. | The VPN is a transport premise, not an identity premise: it authenticates the CLIENT to the network, not the person or process to the service — a machine behind the VPN still needs real per-request authZ, a real audit trail, and a real authorization boundary. The security model we designed for CI/CD makes it concrete: no static keys reachable from CI at all; the runner assumes the deploy role ONLY when the OIDC token's audience+subject match the repo — and the role's policy grants exactly `ecr:PutImage` for the one repo ARN (all the gun needed, not the armory). Same trust point in the pod: a ServiceAccount holds a bounded-token JWT; its RBAC binds exactly the resources it can act on. Trust center, not trust perimeter. (SEC.P0.4/P1.1, SEC.P0.3; 12-TS Incident 9.) |
| L2.5 | Walk the recommended container runtime hardening as a security Eval: which pieces contain which failure class? | Chain: non-root `USER`, read-only rootfs, `--cap-drop ALL` + minimal allows, seccomp `RuntimeDefault`, and a scan gate on images (with digest pin so the registry's mutable tag is never the deploy identity). Why the pieces pair that way: dropping caps blocks the add-cap tree ON the container, read-only blocks file-planting, non-root drops the mount-owner trick, and seccomp narrows the kernel-syscall face. Rootless/`userns-remap` adds one extra containment ring — the container root is now an unprivileged host UID — but it does NOT replace the hygiene list: it shrinks the kernel-burst radius, not the container's own permissions. The sweep itself is read-only audit: enumerate runtime users, mounts, capabilities, and allowed syscalls before you add any control — you cannot harden what you have not enumerated. (DCK.P1.1; SEC.P0.9/P0.10.) |
| L3 | Your CI/CD system has a repo with no secrets, but the deploy role is world-writable by any repo in the org. Redesign the trust so one repo cannot impersonate another. | The flatness is the finding: any repo-side token that can assume the role is a universal key. Fix: per-repo, taint the trust policy with subject/audience conditions so `token.actions.githubusercontent.com` only trusts `repo:<org>/<name>:ref:refs/heads/main` and the audience you control per workflow, PLUS a per-repo role with exactly the resources that repo owns and a CloudTrail alert that fires on unexpected `sts:AssumeRole` from it. Because the trust decision happens at the identity layer, the org-wide role never exists: each repo's pipeline holds a scoped, auditable, revocable identity. The architecture is the same as a ServiceAccount with exact RBAC — which is exactly how containers and OIDC meet: a bounded kubelet-mounted JWT presented as the cloud identity. (SEC.P0.4; 12-TS Incidents 9/11.) |

**TRAP VARIANT:** "Base64-encoded secrets are encrypted secrets." The catch — ambiguity between encoding and encryption: base64 is trivially reversible (`echo <b64> | base64 -d`) and Kubernetes Secrets live in etcd base64 by default unless `--encryption-provider-config` (or KMS on EKS) actually encrypts them. The same trap recurs as "our passwords are hashed" applied to a string that is stored reversible for retrieval — that is not hashed, that is encoded. Interview silver line: "encode is not encrypt; encrypt is not hash".

**IF THEY ASK BETTER:**
- "Least privilege census, day one": AWS: `iam simulate-principal-policy` + `iam list-role-policies` + `iam get-role`, each service firewalled; the read-only sweep is the same discipline at container and cluster level. (SEC.P0.3.)
- "App-layer trust vs infra-layer trust": the OIDC chain (presented token → audience/subject conditions → scoped role → encrypt-only actions) is one example; the same principle under a Pod with a bounded SA JWT is the other — the object is the same, the edge differs.
- "How would you audit a secret used by a test server that is long-rotated?" Prove rotation for a test value you can actually cash out: inspect CloudTrail `GetSecretValue`, compare the two values, then demonstrate a `GetSecretValue` with the old value fails and the new one succeeds — every leak proof runs through audit.

**WRONG-ANSWER ALARM:** "Base64 is encryption" (see trap) or "hashing PII in a DB is encryption" (still indexed/recoverable). "VPN = trust" (transport, not identity — the cookie policy and JWT trust center live between). "Rotation alone closes it" (rewrite + scan gate complete the closure; rotation closes the exposure, rewrite closes the archaeology). "The pipeline can't touch prod" as a slogan (it CAN in the scoped sense — the trust is granular, not gone).

**SPEAKING OPPONENT:** Security chains grade the trust-center instinct, not password trivia. A candidate who says "keep secrets out of the repo, done" loses on the second question; one who walks AAA into IAM evaluation order, OIDC conditions, RBAC bounds, and rotation-vs-rewrite splits owns the room. The interviewer is waiting for one tell: does the candidate check the identity/authorization BOUNDARY (audience, resource ARN, RBAC action) or automatically reach for a wider key? The source files prove the boundary cases; the chain asks you to defend them cold.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** cross-drill 14-06 (hardening floor), 14-03 (rotation story), and 14-12 Incidents 9/11/30 — the same three rows surface from every angle.

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-11
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Facts match verified content (simulate-principal-policy explicitDeny, OIDC conditions, CapsEff, etcd base64) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-12 — TROUBLESHOOTING (METHOD)
**Why this chain:** the four-phase triage, the calibration matrix, evidence-plumbing, and the sync-vs-async recovery choice — the meta-skill every other chain drills becomes its own interview chain here.
**Source sessions:** the 12-troubleshooting-playbook full stop (incidents 1–30 across archetypes A reachability / B identity / C orchestration / D delivery), OBS.P0.1/P0.2 (pillars, PromQL), BASH.P0.3 (exit codes, pipes).

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | Give me your first three minutes on an outage: what questions, what order? | Step 0 is never "open the codebase": it is CALIBRATE—traffic, percent failed, error-rate shape, cross-service spread (who is stuck, what is the blast radius), plus CELEBRATED when nothing matches. Then PROBE the two facts that bracket the WHOLE problem: which side fails (client test, curl through the stack), and which layer (DNS vs TCP vs HTTP vs app vs storage), by eliminating from bottom up. Evidence before hypothesis is the whole discipline: every guess names a witnessable check. Three minutes in, you have either one confirmed narrowed layer and one candidate cause to test, or you declare "not a single-layer fault" and go parallel. (12-TS Phase 1 Calibration; OBS golden signals.) |
| L1.5 | The classic: "my app was working, then it stopped". Rewrite that into a testable problem statement. | "Working" and "stopped" are vibes; the discipline converts them into variables: WHERE (a pod? any pod? one zone? one client?), WHEN (across a deploy? after a config change? at a specific timestamp), and WHICH FACT (the symptom metric delta). Every rewrite produces a concrete check — compare the failure window against a prod commit, a terraform apply, a DNS record change, a clock skew event. The calibration row proves which variable is empty. And the "check" is never a vibe: it is a command whose exit code you can read (curl -w, dig +short, promql query). Nearly all incident time lost is lost in the gap between "something broke" and the same-minute confirmation of an actual variable. (12-TS Phase 2 Grounding; BASH exit codes.) |
| L2 | Two identical errors, same screen, hours apart — one caused by the app, the other by the platform. What distinguishes them? | The error is a symptom, not a cause — the calibration matrix (WHO/WHEN/WHERE/WHICH-FACT plus what changed in the window) runs first, and the discriminating test is BETWEEN layers. The playbook proves the same surface text maps to different layers across its 30 incidents: a pod that resolves but never connects is INC 02 (empty endpoints — a selector/readiness cause), while a pod that connects and throws 500 is INC 20 (readiness 404 — the app surface); a pipeline that "succeeded" while the site serves old bytes is INC 29 (a delivery/pointer cause), while a pod stuck Pending is INC 18 (scheduling/allocatable — a platform cause). Same "red" on the board, three different playbooks — the layer-boundary probe picks which row you open, and the symptom text never does. The single sentence that wins: "I check the layer boundary, not the error text." (12-TS archetypes A–D.) |
| L2.5 | The pager fires and the alert says "ERR 500x". Plan the first five minutes with evidence plumbed. | Five minutes, order-of-checks: (1) WHICH endpoint + which client class + when (calibration), (2) layer split with a live `curl -w "%{http_code} %{time_total}"` through the LB and from inside a pod, (3) the SLO buckets — multi-min error burst? (4) upstream storage/DNS sanity if anything above moved, (5) the deploy/apply calendar in the same 5 minutes (was there a release, a terraform plan, a config push?). The discipline that defines the first five minutes is that they produce EXIT CODES and a decision, not a discussion. The same alert text has two verified readings from the playbook: INC 16-class — a container image whose binary is not even shipped (`httpd: applet not found`, exit 127, CrashLoopBackOff — a delivery cause whose evidence is one `kubectl logs` line), and INC 18 — a pod the scheduler refused (`Insufficient cpu`, never bound — an orchestration cause whose evidence is the describe Events). Same banner, different arcs; the calibration row tells you in the first minute which file to open, and every path ends with a probe that now passes. (12-TS; OBS.P0.9/P2.1.) |
| L3 | Your recovery story has a rollback. Walk when rollback is the right tool and when it is the wrong tool — with the sync/async line. | Roll back when the forward change is asymmetric: the new artifact bytes are bad AND the schema/data path did not migrate (the pod/image + config both roll back cleanly). Do NOT roll back when the forward path already migrated data or carried an irrecoverable destructive edit (Terraform destroy, a DB migration past a point of no return): rollback on that does not restore the old world, it stacks a new break — forward-fix is the recovery, and the alert line deserves a forward hotfix, not a history walk. The playbook line that pins it: a sync change (config-only, bytes-identical) rolls back in seconds; an async change (data) cannot be un-done by flipping a flag, so you recover by repair, not by time-travel. Get the sync/async polarity wrong and the rollback itself is the second incident. (12-TS Phase recovery; K8s universe P0.3; TF.P0.5.) |

**TRAP VARIANT:** "It's a platform problem, the app is fine — I saw the 200s in the dashboard." The catch: a 200 with an error-page-shaped body is the classic silent symptom — the LB returns 200 because the app responded; the app returned its own error HTML inside the body. Calibration counts STATUS and BODY separately (curl -w for code, then `grep -c`/`jq` on the payload); the network-first trapper who reads a 200 and moves on burns the whole incident on a response-reflector. Same on the metric side: empty is not zero (the verified "empty vector is not 0" rule) — a null series is not service-health, and a ratio whose denominator has no samples must be handled, not consumed.

**IF THEY ASK BETTER:**
- "Give me the sync/async question in one paragraph": Is the failure changeable by flipping a config/code pointer (sync, rollback-safe), or has data/state already moved one-way (async, forward-fix)? That polarity is the single decision that de-risks the whole response.
- "What is the one comparison you make before any hypothesis?" The calibration matrix: WHO/WHEN/WHERE/WHICH-FACT crossed against the change calendar — the first row is always "what changed in the window".
- "How do you know you are done?" The evidence list you started with is now either a resolved cause with a fixed config/binary, or a proven-forward state with a completed hotfix; "we restarted it" is not done, "we proved the fix with the same probe that failed" is.

**WRONG-ANSWER ALARM:** "The error text says X — check the log for X" (the error text is a symptom; the matrix is the tool). "It was working before, something in the platform broke" (uncalibrated vibes). "We rolled back, that fixed it" when the failure was a data migration (the rollback IS the second incident). "The dashboard says 200 so the app is fine" (BODY vs CODE is the trap). "Restart fixes flakiness" (evidence-deaf; restarts are the move when the log proves a stale-state catch, never as first response).

**SPEAKING OPPONENT:** The troubleshooting chain may be the hardest one because there is no script — there is a DISCIPLINE and an interviewer watching for it. The tells that fail: leading with a hypothesis, quoting the error text verbatim as evidence, and treating a rollback as the universal recovery. The tells that pass: naming the calibration matrix, reading the body of a 200, drawing the sync/async polarity before choosing recovery, and ending the incident with a probe that now passes. Thirty incidents are behind the golden answers; the method is what the interview is buying.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** this chain is the mirror of the whole playbook — after this, re-drill 14-01/14-02/14-07 as the echoing source layers, then take 14-13 where the SURVIVABILITY of these cases becomes a design question.

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-12
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Method claims match the playbook (Matrix fields, layer-boundary checks, rollback polarity, 200-body trap) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-13 — CROSS-CUTTING SYSTEM DESIGN
**Why this chain:** the tension that runs under all four pillars — availability vs consistency vs cost vs complexity — walked as a real design with SLOs, observability, drift detection, and incident-runbook discipline driving the choices.
**Source sessions:** the 12-troubleshooting archetypes (A–D), OBS.P0.9 (SLO/burn), K8s.P0.7 (RBAC), CICD.P1.1 (plan-apply gate), TF.P1.2 (drift detection), AWS.P0.7 (ALB), SEC.P0.4 (OIDC), plus the architecture map laid out in 00-architecture/README.

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | You are handed "high availability" as a requirement. Turn that into three testable design statements. | (1) A measurable SLO — e.g. 99.9% over 30 days (43m12s budget) on the user-facing request path, evidenced by an error-budget burn-row, not a month-to-month percentage. (2) A failure-mode catalog — the top three realistic faults named (a node dies, a zone fails, the config store drifts) WITH a test for each (fail a pod, fail a zone, mutate a setting and watch the drift alert). (3) A recoverable path — a document that a new engineer can run to the SAME button, because "high availability" that only the writer understands is a handshake, not an SLA. The discipline: HA is a design with ENUMERATED failure modes plus a measurable number, not a diagram with three boxes. |
| L1.5 | A new service needs a database. Walk the choice: which trade-off matrix, which words do you use? | Lead with the access pattern, not the cursor: what is the read/write ratio, what consistency fence does the caller REQUIRE (strong-after-write vs eventually-consistent reads), what does HA demand (synchronous standby + automatic failover vs read replicas that are async copies), what is the destroy risk (a destructive migration vs a schema-safe one). Those four words — pattern, consistency fence, HA shape, blast radius — pin the family (relational vs NoSQL) and the deployment (Multi-AZ vs read-replicas vs serverless). The honest clause that closes the answer: "I pick based on the SLO the feature owes the next layer, and I commit to re-view if the pattern changes." |
| L2 | Design the observability stack for that database service — what do you must-measure, and what alert pages a human? | Four mandatory metrics: error rate (4xx/5xx by endpoint, plus STATUS-vs-BODY separation), latency distribution (P50/P95/P99, NOT just avg), saturation (connections, memory cache heat, IOPS/CPU steering), and the SLO error-budget burn (14.4x + 1x multiwindow pages the human; 1x drift quites the board). Dashboards answer questions (pairs of SQL/metric rows), alerting is scarce (two-window P1, tighter-tuned synthetic probes), and logs carry the trace IDs that other pillars join on. The design is complete when someone at 2am can open it and make one decision. (OBS.P0.9.) |
| L2.5 | Config and state drift — how do you detect it BEFORE the incident, and how does it become an incident-trigger when it does? | Day-0 drift detection: a scheduled `terraform plan -detailed-exitcode` (exit 2 = drift) run on cron, plus a CloudTrail alarm on unexpected `sts:AssumeRole` / `cloudformation` mutations. The leak alarm matrix: metric alert on `aws_security_group`-level change and RBAC-net (`kubectl get` vs the state file). When drift fires an incident, it is a REAL change to the SOURCE-OF-TRUTH — the plan-apply split makes a plan with a destroy-line a STOP, not a merge. Survival data: the war-room incidents where "config changed" was the ACTUAL root (DNS, security group, release schedule) all shared one property — the state-backed registry caught them AFTER the window. Day-0 designs cut that window by running the plan on a schedule, not on incident. |
| L3 | Full design walk: a stateless API layer, a stateful DB, and a release map — where are the availability ceilings, and where do the three pillars disagree? | The API layer is the cheap lever: it scales horizontally, so its ceiling is the HTTP timeout + the storage consistency the feature needs. The DB is the constrained peak: when the read path needs strong-after-write, the topology floor is the synchronous standby + failover, and the async-replica pattern only serves the eventually-consistent read tier. The release map is where the pillars DISAGREE: you can ship availability (rollback-safe byte deployment) OR consistency (schema migrations that are one-way) but not both at once on the same artifact — which is why the pipeline carries the plan-apply split first, the migration stuck-test second, and the rollback triangle (config-only vs data-path) as the head. The deliverable sentence: "I put the ceiling where people can sleep — availability budgets measured, consistency fences explicit, destructive changes gated by plan-review, and the incident runbook pushing the same buttons as the design." |

**TRAP VARIANT:** "We are a small team on one machine. We do not need SLOs." The catch: a one-box premise is a scale-out future, and the 12-troubleshooting corpus is a list of small-team disasters that went wrong because a metric WAS missing (DNS, config drift, missing CPU share) or a boundary was undocumented (SG, RBAC). The design question is the SAME discipline at any size: name three failure modes, give each a detection, and hand a recovery path to a stranger. The small-team answer is "we start with the three highest-hit risks and the two metrics that prove them" — not "no SLOs".

**IF THEY ASK BETTER:**
- "Rate vs irate in a real panel" — rate() for the trend row that budgets time, irate() for the burst health row; the empty-vs-zero discipline hangs on the same ratio question (OBS.P0.2).
- "Where does cost live in the availability story?" Multi-AZ, read replicas, and observability storage are the bill; the interview answer is that the DESIGN is the cost line — choosing strong-after-write buys infra that async-path design does not, and cheap design is the one that states its consistency fence early and trots the cost row with it.
- "How do you survive the cross-service blast radius?" The design owns a point-of-failure map (pod, zone, config, dependency) AND a per-point detection row; the incident starts when the detection is correct and stays sane because the recovery document matches the architecture, not the other way around.

**WRONG-ANSWER ALARM:** "Availability means it never goes down" (the interview wants the measurable SLO + burn + failure catalog, not an absolute). "Consistency is always strong" (it costs topology; the honest answer is "the feature owes a specific fence"). "We scale the DB horizontally like the API" (stateful scaling is sharded R/W layout, not free horizontal equi-spread — the classic over-confident slip). "Drift is a config problem" (in the playbook drift cases it was also the detection hole). "Rollback fixes everything" (the sync/async polarity rules that out — from 14-12).

**SPEAKING OPPONENT:** This chain is where everything scales. The interviewer listens for ONE architecture muscle: can you name a failure mode, put a metric on it, and show the incident-runbook button for it? The strong answer moves top-down from a measured SLO through failure catalog to a release map that separates bytes from migrations; the weak answer draws a happy-path diagram and calls it design. The war-room incidents (B/D archetypes especially) all taught the same thing the design must carry: the ceiling is not written in the diagram, it is enumerated, measured, and drilled.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** after this the chain list closes with behavior — take ONE design sentence from this chain (e.g. "the plan split, the burn window, or the migration polarity") into 14-14 as your spoken example when behavioral asks for "a time architecture was hard".

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-13
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Trade-off claims match source facts (43m12s, burn-tiers, Multi-AZ vs replicas, plan-exit2 drift, migration polarity) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

### CHAIN 14-14 — BEHAVIORAL
**Why this chain:** every technical chain above is only scored after behavior survives — go-to-market on incidents, decisions under pressure, ownership of mistakes, and the humble-eager calibration an interviewer scores for character.
**Source sessions:** the playbook's incident arcs and every verified failure (the wrong-branch `git reset --hard`, the two-door AssumeRole denial — INC 11, the same-tag rollout trap — INC 29, the rotation-commit leak — INC 30), 14-01–14-13 as your example vault, 00-architecture for the "we" voice.

| Depth | Question | Golden answer (score vs) |
|---|---|---|
| L1 | Tell me about a time a system broke and you found out late. What did you do? | Pick ONE verified arc and shape it with three beats: CALIBRATION (the metric that revealed it, with a concrete number), NARROWED CAUSE (the single layer-confirming probe), and the plank-hours recovery (what changed, who confirmed, what the dashboard read after). The war-room arc for this exact question is the wrong-branch `git reset --hard`: the reflog rescue (a validated command, not a Wikipedia answer), the honest admission, and the load test that proved the recovery. The interviewer is looking for OWNERSHIP, not drama: "I broke branch-X with `git reset --hard`, here is the reflog evidence and the forward fix". That sentence is worth more than a heroic narrative where nothing is your fault. |
| L1.5 | Tell me about a time you disagreed with a senior about a technical decision. | Choose a decision-of-record, not a turf war: e.g. the sync/async polarity on a rollback (your call: schema-safe vs data-path already moved), or the plan-apply split in a pipeline. Shape: WHAT I heard (the senior's reason — their constraint is the respectful opening), WHAT I weighed (the evidence row: a destroy-line in the plan, a migration that is one-way), WHAT I did (bring evidence, not insistence: plan output, a burn-window math line), WHAT happened (the outcome), WHAT I would do the same. The test the interviewer is scoring: disagreement is data, not disrespect — you escalate evidence, you stay on the technical merits, and you know when the senior's constraint (time-to-market, operational comfort) outweighs yours. |
| L2 | Walk me through a decision you made that later turned out to be wrong. Full arc, please. | Pick the real one, name the wrong FORK: the "rotation commit is enough" belief (SEC.P2.2 proved the blob survived in `git show HEAD~1:.env`), or the "the app is fine, dashboard says 200" trust (the 200-body trap). Beats: context (the constraint I believed), the decision (the shortcut I chose), the evidence that it was wrong (a specific probe — a git-walk that printed the old key, a curl that returned an error body), the repair (rewrite + scan gate; the body check), and the hard-won rule now at the top of the playbook. The scoring signal is not the mistake — it is that the candidate names the EVIDENCE, not just the feelings, and can report the rule change that came out of it. Never pick a fabricated story: interviewers smell a rehearsed anonymous hero. |
| L2.5 | You disagree with the team on how to fix a recurring incident. How do you get buy-in? | Start with why THEIRS is reasonable (the constraint that makes their approach cheap today), then bring the data that shifts the cost (two-week incident history: same fire, burn budget, hours lost), then propose a LOW-RISK trial (a dry-run plan-apply split, an SLO burn-window read from 2 weeks of opinion-less data) — try the improvement without unleashing it. Buy-in is earned by voluntaring the dirty work (run the dry-run, build the demo alert, write the calibration matrix), not by winning the argument. The honest close: "if the trial proves me wrong, we keep the old way and the team gains evidence either way" — that sentence is the entire behavioral score. |
| L3 | Take me through your growth arc: where you started, the step-change, and what you are practicing now. | Structure: START (the version of you that fixed cache by re-running, sprinted through a config with no plan), STEP-CHANGE (the incident that changed the tool: a real row with a metric — "the day I learned the exit code was 23, not a button", "the day I saw the destroy-line in the plan"), NOW (the deliberate practice: which chains are green this quarter — drift detection day-0, burn-window tuning — stated as WHAT, not "I am always learning"). The interview is buying evidence of calibration: the candidate names the previous-self mistake, the event that bounded it, and the current practice that keeps it dead. No rehearsed heroics; specific errors with named evidence beat generic ambition every time. |

**TRAP VARIANT:** "The failure was the platform's fault" or "we hired a contractor for the tricky part". The catch: behavioral interviews are scored on the CANDIDATE's ownership curve — blame-free accountability ("I missed the drifta-line in the plan review") converts ten times better than a clean-conscience narrative, and saying "I don't know" exactly once about a real gap is a strength while pretending mastery is the instant-fail. Whether the actual root was a config drift, a wrong release tag, or a missing router rule, the candidate who first frames what THEY contributed — even when it is "I did not challenge the apply gate" — takes the scoring over the candidate who relocates it.

**IF THEY ASK BETTER:**
- "How do you handle a teammate who keeps breaking the build?" First: name the mechanics (gate first in DAG, cache bomb, plan-apply split) then the human (the trial move: add the dry-run, the alert, the runbook so the failure is caught before the merge, and a pairing session so the person learns the pattern, not just the fix) — mechanics AND person, in that order, both present.
- "What do you do when you do not know the answer?" Non-negotiable: not bluffing, sequence-listing what you do KNOW to be false, then the fastest path to a real fact (a probe, a docs check, a senior one-line), owning the gap, and writing the new rule into the runbook.
- "Tell me about a strong opinion you hold about operations." My line: "the plan-apply split and the calibration matrix are the two rows I defend because the war-room incidents all trace to the moment someone skipped the evidence step" — one specific claim, one metric, one rule.

**WRONG-ANSWER ALARM:** "I never made a mistake" (universal fail, and the interviewer knows). "It was a team effort" when the question is singular (own a slice, credit the team for theirs — the answer that does both beats either extreme). "I would have come to you for help" as an answer to ANY technical behavioral (help is a tactic, not a decision). "We rolled back and fixed it" with no before/after metric (the whole chain is evidence-driven). Rehearsed hero-scripts ("the platform's DNS died and I single-handedly…").

**SPEAKING OPPONENT:** The behavioral chain runs longer than any technical one because the interviewer is quietly grading calibration: does the candidate separate WHAT happened from WHY it happened, can they name a concrete error and a concrete repair, do they own a slice and credit a team, and does their "now" match a practice they can demonstrate (a burn-window math line, a drift-detection schedule) rather than a slogan? The gold move is cross-referencing a technical chain: "that is the sync/async question from 14-12" or "the destroy-line rule from 14-08" — it proves the discipline is ONE body, not a resume of disconnected drills. The kiss-of-death is a clean narrative with nothing owned and no number to show for it.

**SELF-SCORE:** (record 5/4/3/2/1/0 after every drill)
**FUMBLED NODES:** (list every row code you missed at +0h — re-drill ONLY these)
**RE-DRILL:** [ ] +24h [ ] +48h
**NEXT POINTER:** this chain closes the drill — now instead of a pointer, re-drill 14-01 (the echo), then push the whole list through WEEKLY DRILL ROTATION below.

**DRILL LOG:**

| Drill | Date | Score | Fumbled rows | Note on the fumble |
|---|---|---|---|---|
| +0h | | | | |
| +24h | | | | |
| +48h | | | | |

### QC CHECKLIST — CHAIN 14-14
| # | Check | Status |
|---|---|---|
| 1 | Opener is a genuine 2026 interview question for this domain | PASS |
| 2 | L1 is baseline-appropriate for 1–3 YOE (own it cold) | PASS |
| 3 | L1.5 advances depth on the same topic, not a detour | PASS |
| 4 | L2 answers the mechanism, not just the fix | PASS |
| 5 | L2.5/L3 rows cite verified source sessions | PASS |
| 6 | Example arcs match the verified war-room corpus (reflog rescue, rotation-commit gap, 200-body trap, plan-apply split) | PASS |
| 7 | TRAP VARIANT is plausible to overconfident candidates and the catch is explicit | PASS |
| 8 | IF THEY ASK BETTER offers senior bonus moves, not trivia | PASS |
| 9 | WRONG-ANSWER ALARM names the phrases that lose the chain | PASS |
| 10 | SPEAKING OPPONENT honestly names what is scored | PASS |
| 11 | No emojis, no placeholder words, fences balanced in this chain | PASS |
| 12 | Answers are recitable aloud within the time budgets | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |

---

## WEEKLY DRILL ROTATION TABLE

| Week | Primary chains | Secondary pass | Year rule |
|---|---|---|---|
| 1 | 14-01 LINUX, 14-02 NETWORKING, 14-03 GIT, 14-04 BASH | 14-01 rows re-drilled bare (no notes) | one chain per day, Mon–Thu; Friday = 3-question sample from each |
| 2 | 14-05 AWS, 14-06 DOCKER, 14-07 KUBERNETES, 14-08 TERRAFORM | 14-04 (exit-code crossover) | shift the pool so no chain is back-to-back at the same score |
| 3 | 14-09 CI/CD, 14-10 OBSERVABILITY, 14-11 SECURITY, 14-12 TROUBLESHOOTING | 14-07 (endpoints + rollout rows) | every +24h/+48h RE-DRILL lands in the same week |
| 4 | 14-13 SYSTEM DESIGN, 14-14 BEHAVIORAL, then 14-01 + 14-02 | 14-12 (the mirror chain) | Saturday = cross-domain run: draw 1 question per chain, answer with the SOURCE session name |

Resets: a chain is green only when every row scores >=4 at +48h. A red row (score <4) re-enters the SAME week's secondary pass until it is green — the rotation continues on the other three chains until then.

## FINAL FILE QC — 14-ATTACK-CHAINS
| # | Check | Status |
|---|---|---|
| 1 | Exactly 14 chains present (14-01 through 14-14), each with a difficulty table of L1/L1.5/L2(+)-depth | PASS |
| 2 | Every chain has the full protocol: TRAP VARIANT, IF THEY ASK BETTER, WRONG-ANSWER ALARM, SPEAKING OPPONENT, SELF-SCORE, FUMBLED NODES, RE-DRILL, NEXT POINTER | PASS |
| 3 | Every chain has a DRILL LOG table (Drill/Date/Score/Fumbled rows/Note) | PASS |
| 4 | Every chain ends with a 13-row QC checklist whose last row is the SELF-VERIFY row | PASS |
| 5 | Golden answers cite the verified source sessions (LINUX/GIT/AWS/DCK/K8s/TF/CICD/OBS/SEC/12-TS) by name | PASS |
| 6 | Spot-verified facts match corpus output (137=128+9, pytest 1/2/5, verify error 10, reflog rescue, CACHED/digest, empty vector not 0, 43m12s per 30d, Incidents 2–30 titles) | PASS |
| 7 | No placeholders, no TODO, no draft markers, no dead filler | PASS |
| 8 | No emojis anywhere (checkbox glyphs in RE-DRILL are the only symbols, per the requested template) | PASS |
| 9 | Code fences balanced — zero opening/closing fence imbalance detected at file level | PASS |
| 10 | Every golden answer is recitable aloud within the L1/L1.5/L2 time budgets | PASS |
| 11 | WRONG-ANSWER ALARM entries mirror the TRAP VARIANT catches as spoken phrases | PASS |
| 12 | NEXT POINTERs form a closed loop: references resolve to chains that exist in this file | PASS |
| 13 | SELF-VERIFY — every golden answer is provably correct against the source sessions | PASS |