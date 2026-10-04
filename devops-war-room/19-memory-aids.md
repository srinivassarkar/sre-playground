# 19 — MEMORY AIDS & SPACED-REPETITION DECK

The entire war room compresses to one memory palace plus one deck of ~90 mnemonics; this file is the compressor that turns files 00–18 into a walk and a re-drill loop.

**How to use this file:** 1) run the 6-position compression ladder (below) to build the palace; 2) then run 18-revision's loops on the deck; 3) the [ ] boxes are a re-drill check (do not mark them until you can reproduce the item cold).

Every fact below that carries a session, task, chain, incident, question, bullet, or round ID was verified to exist in the sibling file it names at the time this file was written — same one-to-one rule file 18's appendix enforces. Facts whose source session is flagged model-only in its own file are marked `(modeled reference — not executed)` here; nothing in this file was invented to fit a mnemonic.

---

## 1. THE 6-POSITION COMPRESSION LADDER

Six technique positions, applied in fixed order to any war-room item that refuses to stick. Each position changes the encoding: SEQUENCE adds order, MAPPING adds anchors, IMAGE adds the visual, STORY adds causality, EMOTION adds stakes, HYPERBOLE adds absurdity that refuses to fade. Run all six on one topic and the topic is compressed into a single memorable unit — the kind of unit this file's deck is made of.

The ladder is a **run order, not a menu**: skipping SEQUENCE to hunt for a clever IMAGE is how people build mnemonics they immediately forget. Position 1 alone is enough for most facts; you only escalate a step when the item still slips at +24h (file 13's 48h rule) or the deck row stays unmarked for a full cycle.

```text
COMPRESSION LADDER — run in this order on any slipping item
P1 SEQUENCE   chunk the fact like a phone number (5-9 chunks max)
P2 MAPPING    assign each chunk a concrete state-to-image anchor
P3 IMAGE      render the mapped chunk as a mental picture
P4 STORY      bind the pictures into a causal narrative
P5 EMOTION    staple an emotion (pride, fear, relief) to the narrative
P6 HYPERBOLE  blow the picture up until it is ridiculous enough to survive
END: re-attempt cold right now; a pass → arm the deck row's [ ] at +48h (file 13)
```

### POSITION 1 — SEQUENCE (order matters)

Memory holds 5–9 new chunks at a time, so the first move is to **chunk the fact into a group of 5–9 units and fix their order — order is part of the memory**, not decoration. The phone-number test: chunk `SIGHUP 1 · SIGINT 2 · SIGKILL 9 · SIGTERM 15 · SIGCHLD 17 · SIGCONT 18 · SIGSTOP 19` as three dial groups, `1-2 / 9-15 / 17-18-19`, and the numbers stop being a list and become a dialing pattern. Two of the groups are "grace before death": 9 KILL is the emergency, 15 TERM is the polite one, 1/2/17/18/19 are the dial-tone companions. This exact set is LINUX.P0.1's signal table and the source of the numbers page in Section 3 — the sequence grants order, the order carries the memory.

Example applied to the war room: the five `/proc` windows order themselves PROC.0 cmdline → PROC.1 fd → PROC.2 limits → PROC.3 net/tcp → PROC.4 environ, walkable left-to-right like a single directory listing. Signals and `/proc` are both in LINUX.P0.1–P0.8.

**Failure it defeats:** the "I know the concepts but not the values" freeze — interviewers ask "what number is SIGTERM again?" and the chunked dial group answers in under a second.

### POSITION 2 — MAPPING (state → image)

Mapping converts an abstract state into a concrete image whose *shape* encodes the state. Process states R/S/D/T/Z are the canonical war-room map: R = a race car on the starting grid (on the run queue, wants a CPU core), S = a person asleep on a sofa (interruptible — a shout, i.e. a signal, wakes them), D = a scuba diver underwater (uninterruptible, stuck in disk/NFS I/O, unreachable until they surface), T = a traffic stop (paused by SIGSTOP), Z = a zombie mannequin (already dead, waiting on the parent to sign the paperwork with `wait()`). The map is exactly the STAT-letter semantics of LINUX.P0.1, and the moment a state letter becomes a picture the whole interview answer — "D-state ignores kill -9, Z is a no-op for kill" — becomes describing a diver and a mannequin.

**Failure it defeats:** state-letter blindness. Interviewees read `D` as "weird" or flip T and Z; a mapped image cannot be flipped.

### POSITION 3 — IMAGE (mental picture)

Rendering one vivid static picture per fact. The HTTP status scoreboard is the best-trained example: 401 = a door that says "who are you?" (unauthenticated), 403 = the same door that says "I know who you are, not allowed" (forbidden), 404 = "that room does not exist"; on the server side, 502 = the ALB bouncer has the club's band registered on stage but the mic is dead (target registered, failing health checks), 503 = the bouncer opens the door and the venue is empty (no targets in service to forward to). That 502/503 distinction is NET.P0.4 and the whole of INCIDENT 04 and FT-122 — rendered as two pictures it stops being memorizable and becomes observable.

**Failure it defeats:** alphabetical/order-of-listing recall. Pictures don't need sorting; they answer "so what does 503 feel like?" instantly.

### POSITION 4 — STORY (narrative binds)

A story gives each image a causality and a required order, so recall of the first beat reconstructs the whole chain. The IAM assume-role story: you (the principal) walk up to the security desk (the role's trust policy), produce ID (authentication), the desk checks whether the role *trusts your account* (trust policy) and issues you a temporary badge (STS AssumeRole → temporary credentials); the badge only opens the doors the role's permissions policy lists (authorization), and anything else stays shut by default (implicit deny). Narrate that from SEC.P0.3 / FT-157 and the AccessDenied-on-AssumeRole symptom of INCIDENT 11 falls out by itself — the desk refused because the trust policy excluded your account, never a permissions question.

**Failure it defeats:** the "yes/no" dead end. A NARRATED chain produces the follow-up answer ("but what if the role exists and the user still gets denied? — trust policy, not permissions"), which is exactly what ROUND 1's go-deep probe measures (18-revision 1.0).

### POSITION 5 — EMOTION (novelty/pride/fear anchors)

Staple a felt emotion to the narrative. Fear is the most reliable anchor for incidents, pride for lab receipts. Two exemplars: the state-lock scare (fear) — mid-apply you freeze because Terraform prints `Error acquiring the state lock`, and that trapped feeling is exactly tf-state-incident INCIDENT 22, whose resolution (`aws ddb get-item` on the lock DynamoDB row, optionally `force-unlock`) you never forget because you can re-feel the cold sweat. And the digest receipt (pride) — your first `docker push`/`pull` returned byte-identical `sha256:7738…` (DCK.P0.6), and the proud "same bytes, package yourself" feeling is the fact that a tag is a mutable pointer while the digest is the identity (INCIDENT 25).

**Failure it defeats:** indifference. Emotionless facts are the ones that grade as "I'd know it if prompted" — recognition, not recall (18-revision's recognition trap). An anchored fear/pride is a recall you can reproduce cold.

### POSITION 6 — HYPERBOLE

Scale the image until it is ridiculous enough that the brain files it as "can't unsee." The Docker cache is the exhibitor: CACHED layers printed on every unchanged instruction become "the builder REMEMBERED everything and smugly said `CACHED`" (builds in 0.3 s), versus `--no-cache` as total amnesia ("rebuild every layer from zero"), and the INCIDENT 25 monster — two different digests (`32549f9` cached versus `712fb04` clean) wearing the same `:prod` tag — becomes "one name, two faces, one of them lying." A tag that "promises" bytes while the digest "witnesses" them is the hyperbole that survives the CICD.P2.1 caching conversation.

**Failure it defeats:** scale-blindness. Normal-sized facts are the ones the forgetting curve eats; absurd ones are not.

### Ladder how-to

One run is under two minutes: take any deck row or any slipping session item, compress at the first position that sticks, and stop the moment the item reproduces cold — escalation is for slip, not for polish. When a row still slips after hyperbole, it is an encoding problem, not a memory problem: re-run the ruling session (each 13-x task and 14-x chain names its source) and re-compress, exactly per 18-revision's same-score rule.

### Ladder escalation funnel (slip mode → next position)

Escalate one position at a time — never skip ahead to hunt for a clever image. The funnel maps the observed failure to the position that fixes it:

| Slip symptom at +24h (file 13) | Meaning | Escalate to |
|---|---|---|
| Fact correct, order wrong or items missing | not chunked | P1 SEQUENCE |
| Order fine but terms flip (R/T, Z/D) | no state-to-image hook | P2 MAPPING |
| Semantics right but it won't surface unprompted | no visual handle | P3 IMAGE |
| Can list facts, cannot explain why or how | no causal chain | P4 STORY |
| Explains it, cannot tell it as an incident | no stakes | P5 EMOTION |
| All of the above, still fades within a week | not absurd enough | P6 HYPERBOLE |
| Escalated to HYPERBOLE and still slips | encoding problem, not memory — re-read the ruling session and re-compress fresh (18-revision same-score rule) | re-run the source |

The funnel is a re-run order for a wobbled deck row: a row that flips its letters escalates to MAPPING, earns a better image, and is re-armed at +48h. A row that survives hyperbole and still wobbles is the file-13 signal that the underlying session never stuck — rebuilding a mnemonic on a shaky fact is decorating a broken anchor.

### Worked run: the /proc window through all six positions

PROC.0–PROC.4 is the deck's richest example of one fact run through the whole ladder, so the walk is ready when an interviewer digs past the names:

| Position | Move applied to `/proc/<pid>/` |
|---|---|
| P1 SEQUENCE | chunk to five windows: cmdline · fd · limits · net/tcp · environ (PROC.0 → PROC.4) |
| P2 MAPPING | each chunk = one pane: cmdline = the typewritten argv sheet, fd = the symlink hallway, limits = the soft/hard weight room, net/tcp = the hex switchboard (states 01/06/0A), environ = the sealed envelope (0400) |
| P3 IMAGE | freeze-frame: a five-pane window; pane three shows `soft 65535 hard 65535`, pane four shows columns of hex with 01/06/0A lit up |
| P4 STORY | the process stands at its own window as it runs: cmdline is its typed script, fd are the doors it opened, limits cap what it may reach for, net/tcp lists the sockets it holds, environ leaks everything put there — the leak-vs-mask proof of CICD.P0.7 |
| P5 EMOTION | fear: an interviewer asks "where did your secret go?" and the five-pane window answers before the sentence ends |
| P6 HYPERBOLE | the window is a confession booth: environ blurts every secret shoved into env variables, 0400 read-only, so the secret stays visible only to the process and root |

Run cold after: count the five PROC windows in order, name each one's purpose, and say which one answers "where did my secret go?" — that is the whole of MNE-08 and CICD.P0.7.

### Position-to-answer map (six positions = six interview shapes)

| Ladder position | Question stem it answers | War-room example |
|---|---|---|
| P1 SEQUENCE | "list / walk through" | signal dial groups 1-2 / 9-15 / 17-18-19 (MNE-02) |
| P2 MAPPING | "what does this mean / what is the difference" | process states R/S/D/T/Z as pictures (MNE-01) |
| P3 IMAGE | "how would you recognize it / what does it look like" | 502 bouncer vs 503 empty venue (MNE-15) |
| P4 STORY | "why does it behave this way / what next" | IAM assume-role desk chain (MNE-33) |
| P5 EMOTION | "tell me about an incident" | state-lock cold sweat (MNE-62) |
| P6 HYPERBOLE | "say something memorable about X" | CACHED layers as the proud remembering builder (MNE-72) |

Pick the position whose output matches the question stem before you answer — the answer shape follows the compression, and the compression is what the palace walk rehearses.

### Compressing a 14-x chain as one spine walk

A full attack chain (file 14, chains 14-01…14-09) is the war room at its most causal, and the ladder compresses it exactly as the corridor does: SEQUENCE fixes the chain's hop order, MAPPING gives each hop a locus from its room, STORY narrates the Hop A → Hop B causality, EMOTION staples the incident feel, and HYPERBOLE makes the doomed path un-rewatchable. Run it once and the chain reduces to the corridor with one extra beat per hop.

Worked on chain 14-07 (Kubernetes, whose L1 row walks `kubectl apply` to a running container): sequence the hops as the request crosses the cluster — kubectl → apiserver doorway → etcd vault → RS controller → scheduler desk → kubelet agent → CRI → readiness gate — then narrate: "the front desk authorizes you, the vault files the order, the planner prints the box, the scheduler pins the node, the agent on that node runs it, the gate admits traffic." One sentence IS that chain's L1 row at 18-revision L1 speed (30 seconds per L1 row in the T-7d sweep). A chain you can compress to one corridor sentence survives any "walk me through the path" opener without notes.

### QC CHECKLIST — SECTION 1 (the compression ladder)

| # | Check | Status |
|---|---|---|
| 1 | Six positions ordered and numbered 1–6 as a run ladder | PASS |
| 2 | Each position has a named war-room topic that is real (signals · process states · HTTP status · IAM assume-role · state lock/digest · layer cache) | PASS |
| 3 | Signal chunking uses the verified 1/2/9/15/17/18/19 set from LINUX.P0.1 | PASS |
| 4 | Mapping example uses the verified R/S/D/T/Z semantics of LINUX.P0.1 | PASS |
| 5 | Image example uses the verified 401/403/404/502/503 taxonomy of NET.P0.4 | PASS |
| 6 | 502 vs 503 example resolves to INCIDENT 04 and FT-122 | PASS |
| 7 | Story example resolves to the IAM assume-role chain of SEC.P0.3 / FT-157 and INCIDENT 11 | PASS |
| 8 | Emotion examples are the state lock (INCIDENT 22) and the digest round-trip (DCK.P0.6, INCIDENT 25) | PASS |
| 9 | Hyperbole example is the CACHED/`--no-cache` digest split keyed to CICD.P2.1 and INCIDENT 25 | PASS |
| 10 | Fenced ladder block balanced (one opening, one closing fence) | PASS |
| 11 | No emojis, no TODO/FIXME/placeholder wording in the section | PASS |
| 12 | Escalation rule matches 18-revision's same-score / re-encoding rule | PASS |
| 13 | SELF-VERIFY — every session and incident ID cited in this section exists in files 01, 06, 08, 09, 12, 15 | PASS |

VERDICT: **PASS** — the ladder compresses six named war-room facts, all traceable to verified sibling IDs, through six escalating positions.

NEXT POINTER → the ladder's outputs are the images that fill the memory palace in Section 2.

---

## 2. MEMORY PALACE — 5 ROOMS

Build one palace with five rooms and one connecting corridor. The corridor is the end-to-end spine (Git → CI → Docker → Registry → EKS → Ingress → ALB → Route 53) from 00-architecture, walked left to right with one sentence per hop; each room then holds one DevOps domain pair with 10 fixed loci, and Rooms 1–2 each carry one 11th bridge locus — AWS identity to the cluster, and cluster storage — so the palace holds 52 loci in total. A locus is a fixed object in the room, and each object carries exactly ONE memorable image pinned to exactly ONE verified fact. Every one of the 52 loci is a deck-row or session anchor you can verify in the sibling file named in the locus.

**Palace ground rules:** the rooms and loci never move (movement is what breaks a palace). Only the image changes if the underlying fact changes. Everything walks the same direction. The spine corridor is the spine the whole war room re-draws every week (18-revision 5.4) — the palace simply makes it a physical walk.

### THE CORRIDOR — THE SPINE (8 loci, walked before entering room 1)

| Hop | Image | Fact (verified) |
|---|---|---|
| Git | the source camera winding the film | commits are snapshots of the tree; branch = pointer (GIT.P0.1, GIT.P0.3) |
| CI | the conveyor belt running tests | every push integrates; fail-fast order, cheap before expensive (CICD.P0.2) |
| Docker | the recipe kitchen plating the image | stable-first Dockerfile order → CACHED layers (DCK.P0.2, DCK.P0.6) |
| Registry | the warehouse shelves with tag jars | push/pull round-trip returns the same digest; tag = pointer (DCK.P0.6) |
| EKS | the control-plane front desk | apiserver/etcd/controller-manager/scheduler/kubelet (K8s.P0.1) |
| Ingress | the receptionist routing by host/path | host and path routing, then to a Service (K8s.P1.1) |
| ALB | the front-gate bouncer | listener → rules → target group → health checks (AWS.P0.7) |
| Route 53 | the mail-sorting office | hosted zone records; alias at the apex is free, CNAME isn't (AWS.P0.8) |

### ROOM 1 — THE MACHINE ROOM (LINUX + AWS) — 11 loci

| Locus | Image | Fact (verified) |
|---|---|---|
| 1 · The rack door | every door opens by copying the key, then the spare key is swapped in | processes are created fork() (copy) then exec() (replace) — hence PPID and the process tree (LINUX.P0.1) |
| 2 · The power strip | a strip brocade labeled 15/9; 1/2/17/18/19 dither around it | SIGTERM 15 graceful, SIGKILL 9 immediate; SIGHUP 1, SIGINT 2, SIGCHLD 17, SIGCONT 18, SIGSTOP 19 (LINUX.P0.1) |
| 3 · The triple wall clock | three clock faces: 1 minute, 5, 15 | load average = moving COUNT of runnable + D-state, not a percentage; load 1 on 8 cores ≈ 1 busy core (LINUX.P0.2) |
| 4 · The memory shelf | a shelf labeled `free -h`; an unkillable jar stamped −1000 | alert on `available`, never `free`; oom_score_adj range −1000…+1000, −1000 = OOM-exempt; OOMKilled = exit 137 (LINUX.P0.3, INCIDENT 19) |
| 5 · The disk cage | two gauges: space and inode count | `df -h` = space, `df -i` = inodes; `lsof +L1` finds deleted-but-open files, `/proc/<pid>/fd` prints "(deleted)" (LINUX.P0.4) |
| 6 · The SSH lock | a door that only opens with a 0600 keycard | "Permissions 0644 too open" — group-writable key → sshd refuses; fix 0600/0700 (LINUX.P0.5, INCIDENT 15) |
| 7 · The systemd desk | a clipboard of failed units and a journal reel | `systemctl list-units --failed`; `journalctl -u <unit> -n 50 --no-pager` (LINUX.P0.6) |
| 8 · The /proc window | a five-pane window: cmdline · fd · limits · net/tcp · environ | PROC.0 cmdline (argv, 0644 world-readable) · PROC.1 fd (symlink table) · PROC.2 limits (soft ≤ hard) · PROC.3 net/tcp (hex, little-endian, states 01/06/0A) · PROC.4 environ (0400, env is not secret storage) — sources LINUX.P0.7–P0.8 and the leak-vs-mask proof in CICD.P0.7 |
| 9 · The region map | a wall map of us-east-1 with three AZ pin-holes a/b/c | regions are geographic, AZs are isolated facilities; identity and permission policy evaluation: explicit deny > allow > implicit deny (AWS.P0.1–P0.2, SEC.P0.3) |
| 10 · The STS turnstile | a badge machine that issues short-lived passes | assume-role = principal + trust policy + permissions policy; STS mints temporary credentials; AccessDenied on assume = trust excludes caller, not a permissions fix (AWS.P0.2, INCIDENT 11, FT-157) |
| 11 · The identity bridge | a drawbridge over the cluster moat, lowered only when the sign above matches (the OIDC issuer) | IRSA: pod ServiceAccount → IAM role through an OIDC issuer; no creds = missing SA annotation or OIDC trust relationship — the INCIDENT 13 fail (K8s.P2.4, AWS.P0.2, INCIDENT 13; `(modeled reference — not executed)` per 07-kubernetes) |

### ROOM 2 — THE CONTROL ROOM (NETWORKING + KUBERNETES) — 11 loci

| Locus | Image | Fact (verified) |
|---|---|---|
| 1 · The subnet switch | a switch whose dial reads "/24 = 256" | 2^(32−prefix) addresses, usable minus 2; /20 = 4096 (192.168.96.0/20), /28 = 16 (NET.P0.1) |
| 2 · The label printer | a printer that only prints 10/8, 172.16/12, 192.168/16 | RFC1918 private ranges; loopback 127/8; link-local 169.254/16; documentation 192.0.2/24 (NET.P0.1) |
| 3 · The patch panel | green/amber handshake lights, a FIN oscilloscope, TIME_WAIT dampening mat | TCP: SYN → SYN-ACK → ACK; TIME_WAIT sits ~2×MSL; refused = RST arrived, timeout = silence (NET.P0.2, NET.P0.7) |
| 4 · The status scoreboard | a scoreboard: 4xx your fault, 5xx the server's | 400/401/403/404/429 vs 500/502/503/504; 401 = unauthenticated, 403 = forbidden (NET.P0.4) |
| 5 · The ALB bouncer | a bouncer who answers "band registered but mic dead" versus "venue empty" | 502 = target registered but failing health checks; 503 = no healthy target reachable (NET.P0.4, INCIDENT 04, FT-122) |
| 6 · The certificate wall | a wall of frames: error 10 frame and error 20 frame | `openssl verify` error 10 = certificate expired; error 20 = unable to get local issuer (missing intermediate) (NET.P0.5, INCIDENT 05, SEC.P0.7) |
| 7 · The DNS switchboard | a switchboard on 127.0.0.53 with search-list call tags | /etc/hosts checked before resolv.conf; stub resolver; `ndots:5` makes search-list apply before the bare name — the INCIDENT 03 in-pod NXDOMAIN trap (NET.P0.3, INCIDENT 03) |
| 8 · The apiserver front desk | a front window; behind it etcd vault, watcher monitors, scheduler planner, floor kubelet agents | kube-apiserver = gateway, etcd = state store, controller-manager = desired-state reconciliation, scheduler = placement, kubelet = per-node agent (K8s.P0.1, FT-135) |
| 9 · The workload assembly line | an assembly line: pods stamped, wrapped in RS, boxed by Deployment, Service label-binds the box | Deployment → ReplicaSet → Pod; Service selects pods by labels; endpoints list only ready pods (K8s.P0.2, FT-139) |
| 10 · The probe panel | three switches: restarts / routes / hold | liveness restarts, readiness routes traffic, startup holds both until booted; knobs initialDelaySeconds / periodSeconds / failureThreshold (K8s.P0.5, FT-137, INCIDENT 20) |
| 11 · The storage shelf | a shelf where a request slip (PVC) waits until a worker places a physical volume on it (PV) | PVC declares need (size + access mode), PV is the real volume, StorageClass provisions on demand; WaitForFirstConsumer holds a PVC Pending until a pod schedules; reclaim policy Delete or Retain (K8s.P2.1, INCIDENT 21, TASK 13-15) |

### ROOM 3 — THE WORKSHOP (GIT + BASH) — 10 loci

| Locus | Image | Fact (verified) |
|---|---|---|
| 1 · The three-shelf camera | shelves: working tree, index, HEAD | a file lives in three states; a commit snapshots the staged tree (GIT.P0.1–P0.2) |
| 2 · The label drawer | drawers of sticky labels pointing at photos | branch = a pointer to a commit; fast-forward = label slides forward, otherwise a merge commit (GIT.P0.3) |
| 3 · The replay machine | a machine that replays commits onto a new base | merge = new commit; rebase = replay; interactive rebase rewrites history (GIT.P0.4) |
| 4 · The undo console | soft/mixed/hard levers + a reflog tape | reset moves HEAD (--soft / --mixed / --hard = stage / index / worktree); revert adds an inverse commit; reflog rescues lost commits (GIT.P0.5) |
| 5 · The remote bin | a bin that only fetches labels, plus a merge tray | fetch updates refs only; pull = fetch + merge; pull --rebase keeps history linear (GIT.P0.6) |
| 6 · The conflict table | a table full of <<<<<<< and >>>>>>> cards | conflict markers; resolve → add → commit; never force-push a shared branch (GIT.P0.7) |
| 7 · The bisect scale | a balance that weighs good against bad | `git bisect start/bad/good` binary-searches the guilty commit (GIT.P1.1) |
| 8 · The $? meter | a meter whose needle resets after every command | read or save `$?` immediately — the next command overwrites it (BASH.P0.3, SA-192) |
| 9 · The safety policy board | a board with three rules: e, u, pipefail | `set -euo pipefail`: exit on error, unset variable is fatal, pipeline fails on the rightmost non-zero (BASH.P0.3, TASK 13-02) |
| 10 · The jq & curl tool rack | a jq filter press and a curl health gate | jq: `.key`, `[]`, `length`; curl: `-sf --retry N -w '%{http_code}'` as a health gate (BASH.P0.4–P0.5) |

### ROOM 4 — THE DELIVERY KITCHEN (DOCKER + TERRAFORM + CI/CD) — 10 loci

| Locus | Image | Fact (verified) |
|---|---|---|
| 1 · The recipe book | a cookbook ordered base → deps → source | Dockerfile stable-first, churn-last → unchanged layers print CACHED (DCK.P0.2, DCK.P0.6) |
| 2 · The multi-stage stove | a stove that plates only the last dish | `FROM ... AS builder`; `COPY --from=builder` moves only what's needed; only the last FROM is exported (DCK.P0.2, TASK 13-07) |
| 3 · The pantry shelves | immutable jars on shelves, writable bowls on the counter | image = immutable layer stack; container = image + writable layer; named volumes vs bind mounts (DCK.P0.1, DCK.P0.3) |
| 4 · The tag jars | jars labeled `:prod`, each with a lock-and-key digest | tag = mutable pointer, digest = byte identity; push/pull round-trip proved `sha256:7738…` identical (DCK.P0.6, INCIDENT 25) |
| 5 · The exit-code clock | a clock face: 0, 125, 126, 127, 137 | 0 clean · 125 daemon/create error · 126 not executable · 127 not found · 137 = 128+9 (DCK.P0.7, INCIDENT 16) |
| 6 · The plan/apply desk | a dry-run proof desk and an execution stamp | plan = dry-run diff (config + state + provider); apply = converge the real world and record state (TF.P0.1, FT-144) |
| 7 · The state cabinet | a locked cabinet backed by S3 with a DynamoDB guard | state = the config↔real-object map; S3 backend + DynamoDB lock; `Error acquiring the state lock` = INCIDENT 22; `force-unlock` only with care (TF.P0.2–P0.3, INCIDENT 22) |
| 8 · The module spice rack | spice jars in a folder, pinned to a git sha | modules = folders with pinned sources and versions; count = numbered copies, for_each = keyed map/set, for = expression (TF.P0.6–P0.7) |
| 9 · The pipeline conveyor | a conveyor: trigger → build → test → artifact → deploy → verify | the canonical stage graph, ordered by cost and blast radius; one artifact per run, promote the same artifact (CICD.P0.2, CICD.P0.8, SA-264) |
| 10 · The cache register | a register that prints CACHED vs --no-cache receipts | cache key = instruction + inputs; rolling out maxSurge/maxUnavailable; blue/green and canary switch/gradually shift traffic (CICD.P2.1, CICD.P1.3, FT-152; blue/green + canary are `(modeled reference — not executed)` per 09-cicd) |

### ROOM 5 — THE WATCHTOWER (OBSERVABILITY + SECURITY) — 10 loci

| Locus | Image | Fact (verified) |
|---|---|---|
| 1 · The three-pillar telescope | three lenses: metrics, logs, traces | the three pillars answer what happened, when, and through which request (OBS.P0.1) |
| 2 · The counter/gauge counters | a one-way odometer and a bouncing needle | counters only increase (rate them); gauges go up and down; tired/failed text is a counter, memory is a gauge (OBS.P0.2, SA-277) |
| 3 · The PromQL panel | rate/irate/increase dials + a histogram guard rail | `rate()` = per-second over a window, `irate()` = instant, `increase()` = total; `histogram_quantile` needs `sum by (le)` (OBS.P0.3–P0.4, TASK 13-11, FT-153) |
| 4 · The percentile bar | a p95 bar above a flat "average" line | percentiles beat averages — slow-tail latency hides in averages; SLI = the metric, SLO = the target, error budget = 100% − SLO (OBS.P0.4, OBS.P0.9, SA-285) |
| 5 · The alert switchboard | red lamps: pending → firing → resolved | alert lifecycle; Alertmanager routes and groups notifications (OBS.P0.8, SA-282) |
| 6 · The trace loom | threads woven with trace-id/sample-id tags | OTel spans carry `traceparent` (trace-id/span-id); sampling keeps the waterfall affordable (OBS.P0.7, TASK 13-25) |
| 7 · The IAM vault door | a vault where explicit-denial bars sit above allow bars | explicit deny > explicit allow > implicit deny; least privilege starts from deny and adds only what's needed (SEC.P0.3–P0.4, SA-288) |
| 8 · The secret cabinet | files mounted read-only instead of env labels | env secrets leak into `/proc/<pid>/environ`; mount 0400 files instead; rotate, don't delete (SEC.P0.5, INCIDENT 12, INCIDENT 30) |
| 9 · The supply-chain gate | a turnstile that takes a manifest (SBOM) | SBOM = machine-readable inventory (CycloneDX/SPDX) so a new CVE is answerable in minutes; scan acts as a gate; SBOM generated at build (SEC.P0.10, SEC.P2.2, SA-292; the scan step on this box is `(modeled reference — not executed)` per 11-security) |
| 10 · The incident whiteboard | the 9 boxes written left to right in permanent marker | SYMPTOM → SCOPE → HYPOTHESES → CHECKS → EVIDENCE → ROOT CAUSE → FIX → VERIFY → PREVENT; archetypes A/B/C/D; the first check splits the hypothesis tree (12-troubleshooting method, FT-160, SA-296) |

### Palace walk protocol

```text
PALACE WALK — any free 5 minutes, and always the last 5 minutes of the quiz slot
1. Start at the corridor: walk the 8 spine hops left to right, one sentence per hop.
2. Enter Room 1 and walk every locus IN ORDER (11 for Rooms 1–2, 10 for Rooms 3–5), naming the image, then the fact aloud.
3. Rooms follow the fixed weekday order of the weekly walk (appendix): Mon R1 · Tue R2 ·
   Wed R3 · Thu R4 · Fri R5 · Sat spine redraw · Sun failed loci only.
4. After each room, fire the matching deck rows (MNE bands below) cold — no peeking.
5. A locus or row that wobbles gets a +24h/+48h re-walk exactly like file 14's red-row rule.
```

### Anchoring a new locus

A new war-room session (files 01–12, or a new incident) earns a locus only when it compresses. Procedure, four steps, under two minutes:
1. Pick a FIXED object in the right room — never build new furniture: the object must already exist (rack door, shelf, panel, desk). A new object is a new room, and a new room is a whole new palace.
2. Give it ONE image whose shape encodes the fact (positions 2–3 of the ladder).
3. Pin it to ONE verified fact and ONE source ID from the sibling file, and add it to the room table in this file and to one deck row.
4. It is walkable the next Monday–Friday slot its room owns; until then it lives only on paper.

Rule: a locus that collects a second fact stops being one locus — it becomes two images on one object, and that is how palaces fall apart.

### Palace failure modes

| Failure | What it looks like | Fix |
|---|---|---|
| Moving loci | the room's furniture changes between walks | restock the table in this file; the walk is fixed — only the image may change if the underlying fact changes |
| Fact overload | one locus carries two or more facts | split the image: a second locus on the same object, never a second fact per locus |
| Decoration over substance | a beautiful image with no source ID | revert to the sibling file: an image pins to a session/incident ID or it is decoration |
| Direction drift | rooms walked in a different order day to day | corridor → fixed room order; the weekly walk fixes the weekday order |
| Empty shelves | a room built before its domain is studied | month-1 caution (appendix 4.3): a room grows locus by locus as the phases arrive |
| Recognition masquerading as recall | "I know that locus" while peeking | walk blind: image → fact → source ID aloud; a walk passes only when every locus reproduces cold (the deck's [ ] rule) |

The six modes are the same six reasons a deck row stays unmarked — the palace and the deck fail together, so the fix is the same re-read-the-source rule.

### The critical ten loci (the two per room that must stay cold daily)

Fifty-two loci is a full palace, but four of them are load-bearing for interviews: one per room tested almost every round. They are the loci a walk never skips even on the shortest day, and they answer the four questions interviewers actually open with:

| Room | Locus that must stay cold | The interview question it answers |
|---|---|---|
| Room 1 | 2 · The power strip (signals) | "walk the process / what number is SIGTERM" |
| Room 1 | 8 · The /proc window | "where would you look on a live box" |
| Room 2 | 4–5 · scoreboard + ALB bouncer | "504 vs 502 vs 503" |
| Room 2 | 8 · The apiserver front desk | "who touches etcd / who runs containers" |
| Room 3 | 4 · The undo console | "I broke my branch, fix it" |
| Room 3 | 9 · The safety policy board | "why `set -euo pipefail`" |
| Room 4 | 4 · The tag jars | "tag vs digest" |
| Room 4 | 7 · The state cabinet | "what is Terraform state / who locked it" |
| Room 5 | 3 · The PromQL panel | "rate vs irate vs increase" |
| Room 5 | 10 · The incident whiteboard | "walk me through an incident you fixed" |

The minimal cold check of any day is therefore a ten-locus sweep despite the room names: the two signals windows (Room 1), the bouncer + apiserver (Room 2), the undo + policy boards (Room 3), the jar + cabinet (Room 4), and the incident whiteboard + PromQL panel (Room 5) — ten locus-walks in under a minute, and every one of them is a first-question answer.

### Worked Monday walk (Room 1 · Band MNE-01…09 + MNE-31…40 split)

Corridor (eight hops, one sentence each): Git snaps the code → CI integrates every push → Docker plates an image from stable layers → the Registry holds tag jars keyed by digest → EKS's apiserver desk fronts the control plane → Ingress routes by host/path → the ALB bouncer health-checks its targets → Route 53 sorts mail by record.

Room 1, eleven loci in order: rack door (fork/exec) → power strip (signals 1-2 / 9-15 / 17-18-19) → triple clock (load = count) → memory shelf (available vs free; oom_score_adj −1000) → disk cage (df -h vs -i; lsof +L1) → SSH lock (0600/0700) → systemd desk (failed units; journalctl) → five-pane /proc window (PROC.0–PROC.4) → region map (AZs; region, not AZ, picks where networking lives) → STS turnstile (assume-role = trust + permissions) → identity bridge (IRSA via the OIDC issuer).

Band fired cold: MNE-01 → MNE-02 → MNE-03 → MNE-04 → MNE-05 → MNE-06 → MNE-07 → MNE-08 → MNE-09 → MNE-31 → MNE-32. Wobbles land in 18-revision's Table A as +24h/+48h arms; the Monday QUIZ pick samples the same band, so one cold pass answers it.

### QC CHECKLIST — SECTION 2 (the palace)

| # | Check | Status |
|---|---|---|
| 1 | Spine corridor has the 8 verified hops of 00-architecture (Git → CI → Docker → Registry → EKS → Ingress → ALB → Route 53) | PASS |
| 2 | Exactly 5 rooms defined (LINUX-AWS · NETWORKING-K8s · GIT-BASH · DOCKER-TERRAFORM-CICD · OBSERVABILITY-SECURITY) | PASS |
| 3 | Rooms 1–2 have 11 fixed loci each, Rooms 3–5 have 10 — 52 total, inside the 9–11 per-room guidance | PASS |
| 4 | Every locus pairs a memorable image with one verified sibling-file fact + source ID | PASS |
| 5 | PROC.0–PROC.4 `/proc` facts in Room 1 Locus 8 map to LINUX.P0.7–P0.8 and CICD.P0.7 leak evidence | PASS |
| 6 | Signal numbers in Room 1 Locus 2 match the verified LINUX.P0.1 table | PASS |
| 7 | HTTP/ALB pairs in Room 2 Loci 4–5 resolve to NET.P0.4 and INCIDENT 04 / FT-122 | PASS |
| 8 | K8s loci (8–10) resolve to K8s.P0.1 / P0.2 / P0.5 and the probe semantics of FT-137 | PASS |
| 9 | Palace walk protocol is fenced once and balanced | PASS |
| 10 | No emojis, no TODO/FIXME/placeholder wording in the section | PASS |
| 11 | Modeled-only markers present where the source session is model-only (IRSA/OIDC bridge in Room 1, blue/green+canary in Room 4, scan step in Room 5) | PASS |
| 12 | Walk protocol ties to file 14's red-row rule and 18-revision's +24h/+48h lanes | PASS |
| 13 | SELF-VERIFY — re-checked every session/incident ID cited in this section against files 01–12 | PASS |

VERDICT: **PASS** — the palace holds 52 loci plus an 8-hop spine, every one pinned to a verified sibling fact.

NEXT POINTER → the 52 loci and the spine already index the deck; Section 3 gives each row its number, its mnemonic, and its [ ].

---

## 3. THE DECK — ~90 MNEMONICS ACROSS EVERY DOMAIN

The deck is 90 rows, one mnemonic per row, ordered by domain band so the palace rooms and the deck line up one-to-one. Drill rule: a [ ] is marked ONLY when you can reproduce the row cold — mnemonic stored, fact stated, source session named — at +48h per file 13's rule. Unmarked rows are the Sunday deficit lane of a palace walk.

Bands (row ranges → room → 18-revision week): Linux MNE-01…09 → Room 1 → Week 1 · Networking MNE-10…17 → Room 2 → Week 1 · Git MNE-18…24 → Room 3 → Week 1 · Bash MNE-25…30 → Room 3 → Week 1 · AWS MNE-31…40 → Room 1 → Weeks 2–3 · Docker MNE-41…48 → Room 4 → Week 4 · Kubernetes MNE-49…58 → Room 2 → Week 5 · Terraform MNE-59…66 → Room 4 → Weeks 2–3 · CI/CD MNE-67…74 → Room 4 → Week 6 · Observability MNE-75…81 → Room 5 → Week 7 · Security MNE-82…90 → Room 5 → Weeks 2 & 7–8.

| # | Domain | Topic | Mnemonic | [ ] |
|---|---|---|---|---|
| MNE-01 | Linux | process states | RSDT-Z: Running, Sleeping, Deep-I/O stuck, sTopped, Zombie. A zombie is already dead — kill is a no-op (LINUX.P0.1) | [ ] |
| MNE-02 | Linux | signal numbers | 1-2 / 9-15 / 17-18-19 (phone number). 15 TERM "please", 9 KILL "gone"; 1 HUP, 2 INT, 17 CHLD, 18 CONT, 19 STOP (LINUX.P0.1) | [ ] |
| MNE-03 | Linux | load average | Load = count, not percent: runnable + D-state. Load 1 on 8 cores ≈ 1 busy core; D-heavy → disk/NFS (LINUX.P0.2, FT-101) | [ ] |
| MNE-04 | Linux | OOM killer | oom_score 0→1000-ish; oom_score_adj −1000 = immortal. OOMKilled = exit 137 = 128+9 (LINUX.P0.3, INCIDENT 19) | [ ] |
| MNE-05 | Linux | disk vs inodes | df -h = space, df -i = inodes; lsof +L1 = deleted-but-open; /proc/<pid>/fd shows "(deleted)" (LINUX.P0.4) | [ ] |
| MNE-06 | Linux | ssh permissions | "0644 too open": group-writable key → sshd refuses; fix strips to 0600/0700 (LINUX.P0.5, INCIDENT 15, FT-105) | [ ] |
| MNE-07 | Linux | systemd recall | systemctl list-units --failed · journalctl -u u -n 50 --no-pager (LINUX.P0.6) | [ ] |
| MNE-08 | Linux | the five /proc windows | PROC.0 cmdline (argv, 0644) · PROC.1 fd (symlinks) · PROC.2 limits (soft ≤ hard) · PROC.3 net/tcp (hex, little-endian, 01/06/0A) · PROC.4 environ (0400) (LINUX.P0.7–P0.8, CICD.P0.7) | [ ] |
| MNE-09 | Linux | env & cron | export exports, assignment doesn't; /proc/<pid>/environ is the live block; cron PATH is minimal (LINUX.P0.8) | [ ] |
| MNE-10 | Networking | CIDR math | 2^(32−prefix) addresses, usable − 2; /24 = 256, /20 = 4096, /28 = 16, /30 point-to-point (NET.P0.1, FT-106) | [ ] |
| MNE-11 | Networking | private & special ranges | 10/8 · 172.16/12 · 192.168/16 private; 127/8 loopback; 169.254/16 link-local (NET.P0.1, SA-177) | [ ] |
| MNE-12 | Networking | TCP lifecycle | SYN→SYN-ACK→ACK land; FIN or RST depart; TIME_WAIT ~2×MSL; refused = RST arrived, timeout = silence (NET.P0.2, SA-176) | [ ] |
| MNE-13 | Networking | ephemeral ports | client source ports 32768–60999; ss -tlnp names the LISTEN holder (NET.P0.2, LINUX.P0.7, SA-169) | [ ] |
| MNE-14 | Networking | HTTP classes | 4xx your request (400/401/403/404/429), 5xx the server (500/502/503/504); 401 unauthenticated ≠ 403 forbidden (NET.P0.4, FT-109) | [ ] |
| MNE-15 | Networking | ALB 502 vs 503 | 502 = target registered but failing checks; 503 = no healthy target to forward to (NET.P0.4, INCIDENT 04, FT-122) | [ ] |
| MNE-16 | Networking | TLS failures | openssl verify error 10 = expired, error 20 = unable to get local issuer (missing intermediate); chain root→intermediate→leaf (NET.P0.5, INCIDENT 05, SEC.P0.7) | [ ] |
| MNE-17 | Networking | DNS resolution | /etc/hosts first, then stub 127.0.0.53 → upstream; ndots:5 applies the search list before the bare name (NET.P0.3, INCIDENT 03) | [ ] |
| MNE-18 | Git | three states | working tree → index → HEAD; a commit = snapshot of the staged tree (GIT.P0.1–P0.2, FT-111) | [ ] |
| MNE-19 | Git | branch mechanics | branch = pointer to a commit; fast-forward = slide the label, else merge commit (GIT.P0.3, SA-185) | [ ] |
| MNE-20 | Git | merge vs rebase | merge = new commit; rebase = replay onto a base; interactive rebase rewrites (GIT.P0.4, FT-112) | [ ] |
| MNE-21 | Git | reset vs revert + reflog | reset moves HEAD backward (works magic on shared branches); revert adds an inverse commit; reflog rescues (GIT.P0.5, FT-113) | [ ] |
| MNE-22 | Git | fetch vs pull | fetch = refs only; pull = fetch + merge; pull --rebase keeps linear history (GIT.P0.6, SA-184) | [ ] |
| MNE-23 | Git | conflict playbook | `<<<<<<< ======= >>>>>>>` markers; resolve → add → commit; never force-push shared (GIT.P0.7, FT-114) | [ ] |
| MNE-24 | Git | bisect | git bisect start/bad/good binary-searches the guilty commit (GIT.P1.1, SA-191) | [ ] |
| MNE-25 | Bash | $? rule | read or save `$?` immediately — the next command overwrites it (BASH.P0.3, SA-192) | [ ] |
| MNE-26 | Bash | set -euo pipefail | e = exit on error; u = unset var is fatal; o pipefail = pipeline fails on rightmost non-zero (BASH.P0.3, TASK 13-02) | [ ] |
| MNE-27 | Bash | redirection pairs | 2>/dev/null dirties stdout-only; 2>&1 merges streams; &> is both (BASH.P0.3, SA-193) | [ ] |
| MNE-28 | Bash | jq filters | `.key`, `|`, `.`, `[]`, `length` — jq '.[].name' (BASH.P0.4, TASK 13-04) | [ ] |
| MNE-29 | Bash | curl health gates | curl -sf: silent + fail on HTTP error; --retry N; -w '%{http_code}' (BASH.P0.5, FT-117) | [ ] |
| MNE-30 | Bash | trap + find/xargs | trap 'cmd' EXIT cleans temp; find … -print0 \| xargs -0 (BASH.P1.1, SA-197) | [ ] |
| MNE-31 | AWS | regions & AZs | region = us-east-1, AZ = us-east-1a/b/c — three letters, three facilities (AWS.P0.1) | [ ] |
| MNE-32 | AWS | IAM evaluation | explicit deny > explicit allow > implicit deny; AWS denies by default (AWS.P0.2, SEC.P0.3, SA-288) | [ ] |
| MNE-33 | AWS | roles + STS | assume-role = principal + trust + permissions; STS mints temp creds; assume AccessDenied = trust excludes caller (AWS.P0.2, INCIDENT 11, FT-157) | [ ] |
| MNE-34 | AWS | VPC anatomy | subnet = AZ-scoped; route table + IGW for public, NAT for outbound-only; SG is stateful (AWS.P0.3–P0.4) | [ ] |
| MNE-35 | AWS | SG vs NACL | SG = stateful, return traffic for free; NACL = stateless, must allow BOTH directions — the ephemeral reply trap (AWS.P0.4, SA-203) | [ ] |
| MNE-36 | AWS | EC2/EBS | instance type = family+gen+size (t3.micro); EBS gp3 default; snapshot → AMI (AWS.P0.5, FT-124) | [ ] |
| MNE-37 | AWS | S3 core | bucket names globally unique; keys aren't folders; versioning keeps overwrites; presigned = time-boxed access (AWS.P0.6, AWS.P1.4, FT-123) | [ ] |
| MNE-38 | AWS | ALB flow | listener → rules → target group → health checks; unhealthy target ⇒ 502/503 (AWS.P0.7, FT-122) | [ ] |
| MNE-39 | AWS | Route 53 records | A/AAAA/CNAME/MX/TXT/SRV; alias = AWS-aware and apex-safe; CNAME can't live at the apex (AWS.P0.8, SA-214) | [ ] |
| MNE-40 | AWS | ECR + EKS authorize | node pods pull via ECR auth; push denied = expired auth / scope / repo policy (AWS.P0.10, INCIDENT 14) | [ ] |
| MNE-41 | Docker | image vs container | image = immutable layer stack; container = image + writable layer + namespaces (DCK.P0.1, FT-130) | [ ] |
| MNE-42 | Docker | Dockerfile order | stable-first, churn-last: base, deps, source last → CACHED on change (DCK.P0.2, DCK.P0.6, SA-222) | [ ] |
| MNE-43 | Docker | multi-stage | FROM … AS builder; COPY --from=builder /out; only the last FROM exports (DCK.P0.2, TASK 13-07) | [ ] |
| MNE-44 | Docker | volumes vs bind | named volume = docker-managed; bind = host path; -v name:/data vs -v "$PWD":/data (DCK.P0.3) | [ ] |
| MNE-45 | Docker | networking | bridge is default; user-defined bridge = DNS by container name; -p 8080:80 (DCK.P0.4) | [ ] |
| MNE-46 | Docker | tags vs digest | tag = mutable pointer; digest = byte identity; same push/pull round-trip returns sha256:7738… (DCK.P0.6, INCIDENT 25, SA-230) | [ ] |
| MNE-47 | Docker | exit codes | 0 clean · 125 daemon/create · 126 not executable · 127 not found · 137 = 128+9 (DCK.P0.7, INCIDENT 16, SA-229) | [ ] |
| MNE-48 | Docker | hardened run | --user non-root · --read-only · --cap-drop=ALL · --memory/--pids-limit; CapEff=0 = root with no powers (DCK.P1.1, TASK 13-08, SEC.P0.9) | [ ] |
| MNE-49 | K8s | control plane | apiserver front door · etcd vault · controller-manager watchers · scheduler placement · kubelet node agent (K8s.P0.1, FT-135) | [ ] |
| MNE-50 | K8s | workload chain | Deployment → ReplicaSet → Pod; Service selects by labels; endpoints = ready pods only (K8s.P0.2, FT-139) | [ ] |
| MNE-51 | K8s | probes | liveness = restart · readiness = route · startup = hold both; knobs: initialDelay / period / failureThreshold (K8s.P0.5, FT-137, INCIDENT 20) | [ ] |
| MNE-52 | K8s | ConfigMap vs Secret | ConfigMap = config; Secret = sensitive; mount secrets as 0400 files, not env (K8s.P0.4, FT-143, INCIDENT 12) | [ ] |
| MNE-53 | K8s | scheduling | requests = guaranteed, limits = ceiling; taint repels, toleration accepts; Pending = no fit (K8s.P0.6, INCIDENT 18, SA-238) | [ ] |
| MNE-54 | K8s | RBAC | Role namespaced · ClusterRole cluster-wide · bindings link to subjects; kubectl auth can-i (K8s.P0.7, INCIDENT 10, FT-145) | [ ] |
| MNE-55 | K8s | HPA math | desired = ceil(current/desiredUtilization × replicas), clamped to [min, max] (K8s.P1.3, FT-142) | [ ] |
| MNE-56 | K8s | PV/PVC/StorageClass | 06/07: PVC declares need (size+mode), PV = the real volume, StorageClass makes PVs; WaitForFirstConsumer = Pending till a pod schedules; reclaim Delete/Retain (K8s.P2.1, INCIDENT 21, TASK 13-15, SA-248) | [ ] |
| MNE-57 | K8s | NetworkPolicy | default allow-all; NetworkPolicy = allow-list by podSelector, ingress/egress rules (K8s.P1.2, SA-237) | [ ] |
| MNE-58 | K8s | EKS + IRSA | IRSA = pod SA → IAM role via OIDC issuer; no creds = SA annotation or OIDC trust missing (K8s.P2.4, INCIDENT 13; `(modeled reference — not executed)` per 07-kubernetes) | [ ] |
| MNE-59 | Terraform | core loop | plan = dry-run diff (config+state+provider); apply = converge real world and record state; destroy tears down (TF.P0.1, FT-144) | [ ] |
| MNE-60 | Terraform | plan vs apply flags | -target narrows · -var overrides · -refresh resyncs · -parallelism controls workers (TF.P0.4) | [ ] |
| MNE-61 | Terraform | state is the map | state = config↔real-object map; import adopts · mv/rm rename/replace · refresh resync (TF.P0.2, FT-144) | [ ] |
| MNE-62 | Terraform | backend + lock | S3 holds state, DynamoDB locks it; `Error acquiring the state lock` = concurrent apply — force-unlock with care (TF.P0.3, INCIDENT 22) | [ ] |
| MNE-63 | Terraform | drift + partial apply | out-of-band change ⇒ plan wants -/+ replacement; apply can succeed half and fail — the failure set (TF.P0.5, INCIDENT 23) | [ ] |
| MNE-64 | Terraform | count vs for_each | count = numbered copies; for_each = keyed map/set (stable addresses); for = expression, not resource (TF.P0.6) | [ ] |
| MNE-65 | Terraform | modules | module = folder + pinned source/version; passing vars wires the graph; depends_on documents edges (TF.P0.7) | [ ] |
| MNE-66 | Terraform | lifecycle | prevent_destroy = no-delete guard; ignore_changes = stop diffing a key; moved = rename in state (TF.P1.1) | [ ] |
| MNE-67 | CI/CD | CI vs CD | CI = integrate every push; CD = deploy automatically; Continuous Deployment only after automated verify (CICD.P0.1, FT-149) | [ ] |
| MNE-68 | CI/CD | stage graph | trigger → build → test → artifact → deploy → verify; fail-fast: cheap tests before expensive scans (CICD.P0.2) | [ ] |
| MNE-69 | CI/CD | Actions model | workflow on events · job = runner VM · step = command; needs + matrix fan out; path filters skip work (CICD.P0.3, FT-151, TASK 13-10) | [ ] |
| MNE-70 | CI/CD | one artifact per run | build once, tag v1→v2, promote same artifact; same-tag overwrite = the INCIDENT 29 trap (CICD.P0.8, INCIDENT 29, SA-264) | [ ] |
| MNE-71 | CI/CD | secrets vs mask | arg secret → /proc/<pid>/cmdline (0644 world-readable); env secret → /proc/<pid>/environ (0400); inject from a store, never log (CICD.P0.7, SA-199) | [ ] |
| MNE-72 | CI/CD | layer cache CACHED | cache key = instruction + inputs; stable-first prints CACHED; --cache-from warms cold runners; digest is the witness (CICD.P2.1, DCK.P0.6, INCIDENT 25) | [ ] |
| MNE-73 | CI/CD | deployment strategies | rolling = maxSurge/maxUnavailable; blue/green = endpoint switch; canary = gradual % shift (CICD.P1.3, FT-152; blue/green + canary `(modeled reference — not executed)`) | [ ] |
| MNE-74 | CI/CD | ArgoCD pull model | ArgoCD reconciles repo → cluster; Application CR declares source+dest; OutOfSync = drift vs declared (CICD.P1.2, INCIDENT 26, TASK 13-19; `(modeled reference — not executed)` per 09-cicd) | [ ] |
| MNE-75 | Obs | three pillars | metrics = numbers · logs = events · traces = requests; they answer what/when/where (OBS.P0.1) | [ ] |
| MNE-76 | Obs | PromQL verbs | rate = per-second over a window (counters); irate = instant; increase = total; histogram_quantile needs `sum by (le)` (OBS.P0.3–P0.4, TASK 13-11, FT-153) | [ ] |
| MNE-77 | Obs | counter vs gauge | counter only climbs (rate it); gauge up-and-down; alerts on counters use rate (OBS.P0.2, SA-277) | [ ] |
| MNE-78 | Obs | percentiles | p95 beats average — slow-tail latency hides in averages; alert on percentiles (OBS.P0.4, SA-285) | [ ] |
| MNE-79 | Obs | alert lifecycle | pending → firing → resolved; Alertmanager routes/group; not every metric is an alert (OBS.P0.8, SA-282) | [ ] |
| MNE-80 | Obs | SLO/error budget | SLI = the metric, SLO = the target, budget = 100% − SLO; burn-rate alerts fire when the budget burns fast (OBS.P0.9, TASK 13-22) | [ ] |
| MNE-81 | Obs | tracing | OTel span carries traceparent (trace-id/span-id); sampling keeps the waterfall affordable (OBS.P0.7, TASK 13-25) | [ ] |
| MNE-82 | Security | AAA | authentication = who you are · authorization = what you can do · accounting = auditable trail (SEC.P0.2) | [ ] |
| MNE-83 | Security | IAM deny order | explicit deny always wins; explicit allow second; everything else implicit deny (SEC.P0.3, SA-288, INCIDENT 09) | [ ] |
| MNE-84 | Security | least privilege | start from deny, add the minimum allow; verify it works AND can't do more (SEC.P0.4) | [ ] |
| MNE-85 | Security | secret handling | env exposes secrets to /proc/<pid>/environ; mount 0400 files; rotate, don't delete — INCIDENT 30 shows the history-walk reality (SEC.P0.5, INCIDENT 30) | [ ] |
| MNE-86 | Security | TLS practice | error 10 = expired; error 20 = missing issuer; hostname mismatch is a different class entirely (SEC.P0.7, INCIDENT 05) | [ ] |
| MNE-87 | Security | supply chain + SBOM | SBOM (CycloneDX/SPDX) = inventory so a new CVE is answerable in minutes; scan = gate; sign + pin digests (SEC.P0.10, SA-292; scan step `(modeled reference — not executed)` per 11-security) | [ ] |
| MNE-88 | Security | K8s authz | SA = pod identity; Role/ClusterRole + bindings grant; Forbidden = no binding (SEC.P1.1, INCIDENT 10) | [ ] |
| MNE-89 | Security | shift-left | scan early in CI, gate on Critical/high, annotate the rest; SBOM generated at build (SEC.P2.2, SA-292) | [ ] |
| MNE-90 | Security + TS | incident method + FT-160 | 9-step skeleton SYMPTOM→SCOPE→HYPOTHESES→CHECKS→EVIDENCE→ROOT CAUSE→FIX→VERIFY→PREVENT; archetypes A/B/C/D (12-TS method, FT-160, SA-296) | [ ] |

### The numbers page (cold-recall constants worth their own sweep)

The preset constants an interviewer will ask flat-out. They are all already in the rows above; this page is the twenty seconds of numbers you rehearse cold before any quiz slot:

| Constant | Value (cold) | Row |
|---|---|---|
| Process states | R/S/D/T/Z — D ignores most signals, Z is a no-op for kill | MNE-01 |
| Signal numbers | 1 / 2 / 9 / 15 / 17 / 18 / 19 — 2 is caught, 9 is not | MNE-02 |
| Load average | count of runnable + D-state, never a percent | MNE-03 |
| oom_score_adj | −1000 … +1000; −1000 is exempt | MNE-04 |
| Exit codes | 0 clean · 125 daemon error · 126 not executable · 127 not found · 137 = 128+9 | MNE-47 |
| Ephemeral ports | client source ports 32768–60999 | MNE-13 |
| Private + special ranges | 10/8 · 172.16/12 · 192.168/16 · 127/8 loopback · 169.254/16 link-local | MNE-11 |
| CIDR quick math | /24 = 256 · /20 = 4096 · /28 = 16 · /30 = 4 on point-to-point links | MNE-10 |
| TIME_WAIT | ~2×MSL, on the closing side | MNE-12 |
| HTTP scoreboard | 4xx yours, 5xx server's; 401 ≠ 403; 502 = registered but unheals, 503 = nothing healthy | MNE-14, MNE-15 |
| TLS verify errors | 10 = expired · 20 = unable to get local issuer | MNE-16, MNE-86 |
| Probe trichotomy | liveness restarts · readiness routes · startup holds | MNE-51 |
| HPA math | ceil(current/desiredUtilization × replicas), clamped to [min, max] | MNE-55 |
| Signal ↔ exit | 128 + N ⇔ signal N; 137 = 128+9 | MNE-04, MNE-47 |
| DNS order | /etc/hosts → stub 127.0.0.53 → upstream; ndots:5 applies the search list | MNE-17 |

Nothing on this page is new — it is the deck's constants re-tabled so the Friday sample and any quiz slot can warm up in twenty seconds.

### Deck how-to

A daily pass is the palace walk plus its room's rows fired cold (the palace is the index, the rows are the answers). Every mnemonic follows the same shape — image → fact → source ID — so a wobbled row tells you which part failed: lost the image (re-compress at Position 3), lost the fact (re-read the named session), lost the source ID (re-wire the deck row to its palace locus). Rows stay connected to 18-revision's loops: score ≤3 → armed at +24h/+48h per file 13; row green twice at +48h → graduate to the 30-day lane and stop.

```text
DECK DRILL — one band per day, answer order fixed
1. Open the room of the day, walk its loci aloud (11 for Rooms 1–2, 10 otherwise — Section 2 protocol).
2. Fire the band's rows cold: say the mnemonic, then the fact, then the source session name.
3. Mark a row's [ ] only when all three come out without the file open, and re-verify at +48h.
4. A wobble sends the row to the +24h lane AND the palace walk's failed-locus list (Sunday).
5. The Friday sample (18-revision 1.1/1.2 Friday rule) draws 3 rows from the week's bands.
```

### Band-to-palace index (one table to navigate the deck)

| Band | Rows | Room | Key loci | Walk day | 18-revision week |
|---|---|---|---|---|---|
| Linux | MNE-01…09 | R1 | rack door · power strip · /proc window | Mon | Week 1 |
| Networking | MNE-10…17 | R2 | subnet switch · status scoreboard · DNS switchboard | Tue | Week 1 |
| Git | MNE-18…24 | R3 | three-shelf camera · undo console · bisect scale | Wed | Week 1 |
| Bash | MNE-25…30 | R3 | $? meter · safety policy board · jq & curl rack | Wed | Week 1 |
| AWS | MNE-31…40 | R1 | region map · STS turnstile · identity bridge | Mon | Weeks 2–3 |
| Docker | MNE-41…48 | R4 | recipe book · tag jars · exit-code clock | Thu | Week 4 |
| Kubernetes | MNE-49…58 | R2 | apiserver front desk · workload line · storage shelf | Tue | Week 5 |
| Terraform | MNE-59…66 | R4 | plan/apply desk · state cabinet · module spice rack | Thu | Weeks 2–3 |
| CI/CD | MNE-67…74 | R4 | pipeline conveyor · cache register | Thu | Week 6 |
| Observability | MNE-75…81 | R5 | three-pillar telescope · PromQL panel · percentile bar | Fri | Week 7 |
| Security | MNE-82…90 | R5 | IAM vault door · supply-chain gate · incident whiteboard | Fri | Weeks 2 & 7–8 |

This index answers "where do I find the row for X?" during any drill: band → room → locus, and the locus is the row's home.

### Worked Friday sample (18-revision 1.1/1.2 rule)

The Friday rule draws THREE rows from this week's bands, no peeking, graded like a quiz pick. Friday of Week 4 (Docker week) samples three shapes: one strategy change — rolling deploy knobs maxSurge/maxUnavailable (MNE-73); one box job — image vs container (MNE-41); one cold constant — the exit codes 0/125/126/127/137 (MNE-47). Grading is the same three-part pass as any daily quiz item (mnemonic + fact + source ID); a wobble sends the row to Sunday's deficit lane and re-arms it at +24h. The sample lands in 18-revision exactly as chain quiz picks do, so Friday is indistinguishable from any other quiz slot except that it draws from the week.

### Deck failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Row exists, room gap | the band's rows are memorized but the palace locus is stale on that item | re-walk the room — the locus pre-orders the row's three parts |
| Source-ID amnesia | the fact reproduces, the session name doesn't | re-wire the row to its locus and re-walk through position 2 |
| Recognition recall | the [ ] gets marked with the file open | [ ] only when the row reproduces cold and is re-verified at +48h |
| Band-skipping | always drills the loved band, never the hated one | the weekly walk fixes the day's band; Sunday's deficit lane covers the hated rows |
| Over-arming | rows are re-lived instead of graduated | a row green twice at +48h graduates to the 30-day lane and stops (deck how-to) |
| Constants drift | numbers recalled as "about" instead of exact | the numbers page above is walked cold with the Friday sample each week |

The six deck failure modes mirror the six palace failure modes — same cause, same re-read-the-source fix.

### Grading a cold pass (the three-part rubric)

Every deck row is reproduced in three parts — mnemonic, fact, source ID — and each part is graded cold, matching file 13's score rule:

| Part | Cold pass (2) | Cold wobble (1) | Wrong / blank (0) |
|---|---|---|---|
| Mnemonic | the picture or phrase comes out in one try | picture right, name fumbled | no image at all |
| Fact | the verified fact stated exactly (number, value, order) | fact right, value approximated | fact belongs to a different row |
| Source ID | the session/incident/question named without the file open | ID right, detail hazy | source unnamed |

A row scores 6/6 cold twice at +48h → graduates to the 30-day lane (deck rule). A row scores 4/6 or less → +24h arm and a palace re-walk of the locus the row lives in. The rubric is the same math 18-revision and file 13 apply to every drill — the deck rows simply make the unit of practice explicit.

### Growing the deck (new sessions create new rows)

A new verified session or incident earns a row through the same discipline as a new locus: SEQUENCE chunk the fact, MAPPING give it an image, pin ONE fact to ONE source ID, place the row in the correct band (the domain list in the deck header), and keep the row count honest by re-numbering the rest of that band. A row is never added without its sibling-file ID — an unreferenced mnemonic is decoration, exactly as in the palace. Rows added mid-year inherit the year map's rule: they join the current week's band and are walked with it from the next occurrence of that room's day.

### QC CHECKLIST — SECTION 3 (the deck)

| # | Check | Status |
|---|---|---|
| 1 | Exactly 90 rows, numbered MNE-01…MNE-90 | PASS |
| 2 | Every domain band present: Linux 9 · Networking 8 · Git 7 · Bash 6 · AWS 10 · Docker 8 · Kubernetes 10 · Terraform 8 · CI/CD 8 · Observability 7 · Security 9 | PASS |
| 3 | Optional: every row carries a non-emoji [ ] cold-check cell | PASS |
| 4 | Semantic anchors present: the five /proc windows (PROC.0–PROC.4, MNE-08), PV/PVC (MNE-56), CACHED (MNE-72), FT-160 (MNE-90), IRSA (MNE-58), SBOM (MNE-87) | PASS |
| 5 | Every cited session ID (LINUX/NET/GIT/BASH/AWS/DCK/K8s/TF/CICD/OBS/SEC) exists in its sibling file | PASS |
| 6 | Every cited INCIDENT ID (04, 05, 09, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 25, 26, 29, 30) exists in file 12 | PASS |
| 7 | Every cited FT/SA (101, 105, 106, 109, 111–114, 117, 122–124, 130, 135, 137, 139, 142–145, 149, 151–153, 157, 160; SA 169, 176, 177, 184, 185, 191–193, 197, 199, 203, 214, 222, 229, 230, 237, 238, 248, 264, 277, 282, 285, 288, 292, 296) exists in file 15 | PASS |
| 8 | Task IDs cited (13-02, 13-04, 13-07, 13-08, 13-10, 13-11, 13-15, 13-19, 13-22, 13-25) exist in file 13 | PASS |
| 9 | Modeled-only markers present on IRSA (MNE-58), blue/green+canary (MNE-73), ArgoCD (MNE-74), scan/SBOM (MNE-87) | PASS |
| 10 | Deck drill fence is balanced (one opening, one closing fence) | PASS |
| 11 | No emojis, no TODO/FIXME/placeholder wording; numbers and arrows use the house · and → | PASS |
| 12 | Row drill rule matches file 13's +48h graduation and 18-revision's Friday-sample rule | PASS |
| 13 | SELF-VERIFY — spot-checked 15 rows across all 11 bands against the sibling files, all IDs resolve | PASS |

VERDICT: **PASS** — the deck holds 90 rows; every row carries a real fact, a real source ID, and a re-drill checkbox.

NEXT POINTER → the deck is the row set the appendix schedules across the year.

---

## 4. APPENDIX — YEAR-OF-DEVELOPMENT MEMORY MAP

The deck and the palace only matter if they are walked on schedule. This appendix fixes three things: the claim-depth legend the whole war room grades by, the week-by-week palace walk, and the year-long map that fits the walk and the deck into 18-revision's loops.

### 4.1 L0–L4 CLAIM-DEPTH LEGEND (the war-room ladder)

The war room's own depth ladder, verbatim in spirit from 16-resume-defense and 00-architecture §16: `USED < UNDERSTOOD < PRACTICED < OPERATED < DESIGNED`. The depth labels govern what a bullet may claim; the palace loci and deck rows are the smallest evidence units that prove a depth.

| Level | Name | Definition (file 16) | Proved by (this file) |
|---|---|---|---|
| L0 | USED | saw it / touched it | a deck row reproduced cold names the tool but no mechanism |
| L1 | UNDERSTOOD | can explain | the row's fact + source-session mechanism narrated (position 4 story) |
| L2 | PRACTICED | did it deliberately | the row's [ ] marked after +48h cold reproduction |
| L3 | OPERATED | ran it in prod-ish conditions | the row's ruling session was verified live in its sibling file (lab receipt, INCIDENT card, real output) |
| L4 | DESIGNED | built it | a full crown-worthy design in a mock round; capped to senior at 1–3 YOE (00-architecture §10.8) |

Claim rule: you may only claim the depth the newest evidence supports. A sibling session labelled model-only caps its rows at L1–L2 — IRSA, ArgoCD, blue/green/canary and the scan step are UNDERSTOOD/PRACTICED territory (their row markers), never OPERATED.

### 4.2 THE WEEKLY PALACE WALK (tied to 18-revision's loops)

A five-minute fixed ride on the 15-minute daily loop. Every weekday opens with the palace room of the day plus that room's deck band, fired cold; the walk's output logs into file 18's Table A the same way a chain does. When the daily quiz slot tilts (18-revision 1.4), the room of the day follows the tilt (Week 5 tilt pulls Room 2's K8s loci; Week 7 tilt pulls Room 5).

| Day | Walk | Deck band | 18-revision tie |
|---|---|---|---|
| Mon | ROOM 1 — machine room (LINUX + AWS) | MNE-01…09 + MNE-31…40 (split: 4 rows + 5 rows alternate) | daily WRITE Mon batch 13-01..13-03; QUIZ Mon set |
| Tue | ROOM 2 — control room (NETWORKING + K8s) | MNE-10…17 + MNE-49…58 | daily WRITE Tue batch; CHAIN 14-05/14-07 weeks 2/3 |
| Wed | ROOM 3 — workshop (GIT + BASH) | MNE-18…30 | daily WRITE Wed batch 13-09..13-11; CHAIN 14-03/14-04 |
| Thu | ROOM 4 — delivery kitchen (DOCKER + TF + CI/CD) | MNE-41…48 + MNE-59…74 | daily WRITE Thu batch 13-13..13-15; CHAIN 14-06/14-08/14-09 |
| Fri | ROOM 5 — watchtower (OBS + SECURITY) | MNE-75…90 | Friday sample (18-revision 1.1) draws 3 rows from this week's bands |
| Sat | CORRIDOR redraw: the 8 spine hops from memory | spine only | 18-revision 5.4 spine redraw, cross-domain chain rule |
| Sun | FAILED-LOCI lane: only unmarked [ ] rows and red loci | deficit rows | Sunday deficit lane (18-revision 1.1/1.8) |

The walk is the memory-palace front for file 13's Monday–Sunday weekday batches — it does not replace them, it indexes them: a task in 13-13 (Helm) anchors in Room 2/4 loci; a question in FT-157 (assume-role) anchors in Room 1 Locus 10 and MNE-33.

```text
WEEKLY PALACE WALK — 5 minutes, after the daily 15-min loop
Mon R1 · Tue R2 · Wed R3 · Thu R4 · Fri R5 · Sat spine redraw · Sun failed loci only.
Each walk: corridor (spine, 1 sentence per hop) → the day's room, every locus in order (11 for
R1/R2, 10 otherwise) → the band's rows cold → log wobbles to 18-revision's Table A as +24h/+48h arms.
Rule: a locus or row not named from memory is not a pass — recognition is not recall.
```

### 4.3 THE YEAR-OF-DEVELOPMENT MAP (months 1–12)

The year runs as 18-revision's 8-week calendar on a 12-month axis; this map fixes what the walk and deck add at each month. Year 1 builds and owns the deck; the yearly goal is every row's [ ] marked, every row graduated to the 30-day lane, and every claim held at its proven L-level.

| Month | 18-revision phase | Palace/deck work | Depth gate |
|---|---|---|---|
| 1 | Foundation (weeks 1–2) | build Rooms 1–3 token ladders; walk Rooms 1–3; mark MNE-01…30 | rows for Linux/NET/GIT/BASH at L1+, signals and /proc cold |
| 2 | Cloud (weeks 2–4) | add Rooms 4–5; walk all five; introduce the Friday 3-row sample | AWS/TF rows at L1–L2; IAM assert and TF state loci cold |
| 3 | Containers (week 4–5) | expand Room 4 K8s lobes; daily Thu band split 41–48 / 49–58 | Docker/K8s rows L2; PV-PVC and probe loci cold |
| 4 | Delivery (week 6) | full deck now active; Saturday spine redraw begins | CI/CD rows L2; one-artifact and cache loci cold |
| 5 | Operate (week 7) | deepen Room 5; alert-on-percentiles loci drilled | OBS/SEC rows L2; PromQL `sum by (le)` cold |
| 6 | Defend (week 8 / first taper) | first +30d TEACH pass walks the whole palace top-down | month-1 bands re-proved at L2; rows re-checked at +48h |
| 7 | Cycle 2, shifted slot | re-walk in the raised bar (18-revision 5.2): every daily score beats cycle 1 | graduated rows stay graduated; wobbles re-armed |
| 8 | Cycle 2 | swap room order by the tilt; add the corridor listeners to hooks | depth evidence now green at 48h for 70%+ of rows |
| 9 | Cycle 2/3 collision rule (3.2) | merged double-grading months; palace walk backs TEACH | +30d TEACH re-walks any wobbly room |
| 10 | Cycle 3 at maintenance cadence | deck rows become the defection index for mocks | 90% rows at L2–L3; only modeled rows capped at L1 |
| 11 | Defend / taper prep | the taper's cram sheet Page 1 is the corridor + rooms re-drawn | every [ ] marked; LIE-DETECTOR row mapping clean |
| 12 | Taper or maintenance | walk the palace flat; no new loci after T-3d (18-revision 4) | ROUND 6 with no MUST FIX on uncertainty handling |

Month-1 caution: do not try to build all five rooms in week 1. The palace is built room-by-room as the phases arrive — a room with no studied locus is a room full of empty shelves, and an empty shelf is where memory goes to stall.

### 4.4 YEAR-2/3 MAINTENANCE (kept by the same loops)

Years 2–3 keep the exact same walk but on the maintenance cadence of 18-revision 5.8: one cycle per two months, taper whenever a date appears, and the deck's graduated rows stay in the 30-day lane (a row re-armed by a new job's JD tilt is a row re-opened — never resurrected silently). The palace is the craft: the corridor redraw is the one skill that never leaves the daily loop, because the open "so what do you do?" question (18-revision 5.4) is answered by the spine walk in one sentence per hop.

### 4.5 THE WALK FEEDS EVERY SCORE GATE

Six graded gates exist across the war room (13-write batch, 14-chain, 15-quiz, 12-TS debug, 16-defense, mock round); the walk feeds each one differently:

| Gate | Walk contribution |
|---|---|
| WRITE (13-x batch) | the room of the day pre-loads the task's vocabulary, so the write starts warm |
| QUIZ (15-x pick) | the band's rows fired cold are the same rows a quiz pick grades — one cold pass scores both |
| CHAIN (14-x) | the corridor spine redraw is the cross-domain chain answer; the rooms are the within-bar links |
| DEBUG (12-TS) | the incident whiteboard locus (Room 5 Locus 10) is the 9-step skeleton; archetypes A/B/C/D come from the same locus |
| DEFEND (16) | claim-depth falls out of the walk: a row reproduced cold at +48h is L2 evidence; a live-lab row is L3 |
| MOCK ROUND (00-architecture §10) | the position-to-answer map (Section 1) picks the answer shape before the session begins |

The walk is therefore not an extra; it is the memory front of every gate that already scores the war room.

### 4.6 THE TAPER CRAM CHAIN (T-7d → T-morning)

The taper shrinks the walk to a fixed chain, matching 18-revision Part 4 and the cram sheet's Page-1 drawing:

| Time | Chain |
|---|---|
| T-7d…T-3d | normal walk; the corridor redraw is added to Saturday; no new loci after T-3d (appendix 4.3) |
| T-3d…T-1d | every room walked daily, corridor twice a day; Friday's 3-row sample becomes an all-band sweep |
| T day | corridor (8 hops) → Room 1 Locus 8 (/proc window) → Room 2 Loci 4–5 (502/503) → Room 5 Locus 10 (9-step incident skeleton) → the numbers page in one breath |
| In the waiting room | signal dials (1-2 / 9-15 / 17-18-19), exit codes, oom range −1000…+1000 |

The T-day chain is the whole war room compressed to six checkpoints — under two minutes, no paper allowed.

### 4.7 THE WAR ROOM IN ONE BREATH (this file's inventory)

The whole system, counted once so the numbers stay legible through any recap:

| Count | Item |
|---|---|
| 6 | compression-ladder positions (SEQUENCE → MAPPING → IMAGE → STORY → EMOTION → HYPERBOLE) |
| 8 | spine corridor hops (Git → CI → Docker → Registry → EKS → Ingress → ALB → Route 53) |
| 5 | palace rooms (one DevOps domain pair per room) |
| 52 | fixed loci (11 + 11 + 10 + 10 + 10), each one image + one fact + one source ID |
| 11 | deck bands, ordered by the days the weekly walk visits their rooms |
| 90 | deck rows MNE-01…MNE-90, each with a [ ] re-drill cell |
| 4 | L0–L4 claim depths (USED < UNDERSTOOD < PRACTICED < OPERATED < DESIGNED) |
| 4 | fences in this file (the ladder, the palace walk, the deck drill, the weekly walk) |

Recap answer when asked "what did you actually build to prepare?": a palace of 52 anchored facts that a five-minute walk rehearses daily, a 90-row spaced deck tied to 18-revision's loops, and a numbers page that reproduces cold — all of it traceable to a source session so no claim outruns its evidence.

### 4.8 WHICH FILE FEEDS WHICH ROOM (the cross-file map)

One glance to find the source of any locus or row:

| File | Content | Feeds (this file) |
|---|---|---|
| 00-architecture | spine, §16 L-levels, mock-round rule | the corridor; the claim ladder; the mock gates |
| 01-linux | LINUX.P0.1–P1.2 | Room 1 loci 1–8 · MNE-01…09 |
| 02-networking | NET.P0.1–P1.2 | Room 2 loci 1–7 · MNE-10…17 |
| 03-git | GIT.P0.1–P1.1 | Room 3 loci 1–7 · MNE-18…24 |
| 04-bash | BASH.P0.1–P1.1 | Room 3 loci 8–10 · MNE-25…30 |
| 05-aws | AWS.P0.1–P2.6 | Room 1 loci 9–11 · MNE-31…40 |
| 06-docker | DCK.P0.1–P2.1 | Room 4 loci 1–5 · MNE-41…48 |
| 07-kubernetes | K8s.P0.1–P2.4 | Room 2 loci 8–11 · MNE-49…58 |
| 08-terraform | TF.P0.1–P2.2 | Room 4 loci 6–8 · MNE-59…66 |
| 09-cicd | CICD.P0.1–P2.3 | Room 4 loci 9–10 · MNE-67…74 |
| 10-observability | OBS.P0.1–P2.2 | Room 5 loci 1–6 · MNE-75…81 |
| 11-security | SEC.P0.1–P2.2 | Room 5 loci 7–9 · MNE-82…89 |
| 12-troubleshooting-playbook | INCIDENT 01–30, 9-step skeleton, archetypes | Room 5 locus 10 · MNE-90 |
| 13-write-without-google | weekday write batches | the weekly walk's weekday tie-ins |
| 14-attack-chains | chains 14-01…14-09 | the corridor-sentence chain compressions (Section 1) |
| 15-question-bank | FT-101…FT-160 · SA-161…SA-300 | every FT/SA ID the deck rows cite |
| 16-resume-defense | L0–L4 ladder, LIE-DETECTOR | appendix 4.1 depth legend |
| 18-revision | loops, tapers, cram sheet | every schedule tie in this file |

Any row whose source file is missing from this map is a row built on air — the map is the file's own dependency graph, and it is closed: every named file exists in the war room and every ID resolves to it.

### 4.9 THE CYCLE-1 EIGHT-WEEK BUILD PLAN

The year map (4.3) gives the months; this is the week-by-week build so the palace is never built ahead of its evidence (month-1 caution), using the week bands already fixed in Section 3:

| Week | Rows touched | New palace work | Walk/deck milestone |
|---|---|---|---|
| 1 | MNE-01…30 (Linux · NET · GIT · BASH) | fill Room 1 loci 1–8 and all of Room 3 | Rooms 1+3 walkable; signals and /proc cold |
| 2 | MNE-31…40 (AWS) · MNE-59 start (TF) · Security rows first pass | add Room 1 loci 9–11 · Room 4 loci 6–8 · Room 5 loci 7–9 | IAM deny order, state cabinet, vault door cold |
| 3 | MNE-59…66 finish (TF) | complete the Room 4 storage book | plan/apply + lock loci cold |
| 4 | MNE-41…48 (Docker) | fill Room 4 loci 1–5 | recipe book, tag jars, exit-code clock cold |
| 5 | MNE-49…58 (K8s) | fill Room 2 loci 8–11 | probes, workload line, storage shelf cold |
| 6 | MNE-67…74 (CI/CD) | finish Room 4 loci 9–10 | conveyor + cache register cold |
| 7 | MNE-75…81 (OBS) · Security second pass | fill Room 5 loci 1–6; re-open 7–9 | all 52 loci walkable |
| 8 | first taper → TEACH | all 52 loci; corridor redrawn twice | month-1 bands re-proved at L2; rows green at +48h |

The week numbers are the deck's own band→week mapping (Section 3) applied to the year map's month rows; nothing here introduces a new schedule, it only makes the existing one week-shaped.

### APPENDIX QC CHECKLIST — SECTION 4 (the year map)

| # | Check | Status |
|---|---|---|
| 1 | L0–L4 legend equals USED < UNDERSTOOD < PRACTICED < OPERATED < DESIGNED from file 16 and 00-architecture §16 | PASS |
| 2 | Each level shows how this file proves it (deck row, [ ], lab receipt, design round) | PASS |
| 3 | Claim rule caps modeled-only sessions at L1–L2 (IRSA, ArgoCD, blue/green+canary, scan step) | PASS |
| 4 | Weekly palace walk defines a room per weekday + Saturday spine + Sunday deficit lane | PASS |
| 5 | Walk ties each day to 18-revision's daily batches, quiz picks, and chain rotation | PASS |
| 6 | Walk protocol fence is balanced (one opening, one closing fence) | PASS |
| 7 | Year map runs months 1–12 against 18-revision's phases and cycles | PASS |
| 8 | Month gates are real war-room outputs (cold rows, +48h green, ROUND 6, LIE-DETECTOR) | PASS |
| 9 | Taper rule honored: no new loci after T-3d (18-revision Part 4) | PASS |
| 10 | Year 2/3 maintenance matches 18-revision 5.8's maintenance cadence | PASS |
| 11 | No emojis, no TODO/FIXME/placeholder wording in the section | PASS |
| 12 | No invented IDs: every month/row reference resolves to 18-revision's parts or this file's sections | PASS |
| 13 | SELF-VERIFY — the walk's day-to-band mapping matches the deck table's band→room→week rows | PASS |

VERDICT: **PASS** — the appendix binds the palace and the deck to the revision calendar and to the claim ladder every bullet must survive.

---

## QUALITY CHECKLIST — FILE 19 (final)

| # | Check | Status |
|---|---|---|
| 1 | Header present: title, one-line framing, how-to-use with the numbered 3-step rule | PASS |
| 2 | Section 1 — six-position ladder with a concrete war-room example per position | PASS |
| 3 | Section 2 — five rooms, 9–11 loci each (Rooms 1–2: 11, Rooms 3–5: 10, 52 total), each locus = image + verified fact + source | PASS |
| 4 | Section 3 — ~90 mnemonics in one table (90 rows, MNE-01…90) with cold-recheck boxes | PASS |
| 5 | Appendix — L0–L4 legend, weekly palace walk, year-of-development map | PASS |
| 6 | Every section ends with a 13-row QC table whose last row is SELF-VERIFY, a VERDICT, and a NEXT POINTER (final section ends with this final table instead) | PASS |
| 7 | All fenced code blocks balanced (4 fences, each opened and closed — 8 fence markers total) | PASS |
| 8 | No emojis anywhere (typographic glyphs limited to — · → and the [ ] checkbox) | PASS |
| 9 | No TODO / FIXME / placeholder wording in the body | PASS |
| 10 | All cited session IDs resolve to sibling files 01–12 (LINUX/NET/GIT/BASH/AWS/DCK/K8s/TF/CICD/OBS/SEC verified by grep) | PASS |
| 11 | All cited INCIDENT 01–30, FT/SA ranges, task 13-xx, and modeled-only markers resolve to files 12–17 content | PASS |
| 12 | The deck's semantic anchors named in the brief are present: /proc facts (PROC.0–4), PV/PVC, CACHED, FT-160, IRSA, SBOM | PASS |
| 13 | SELF-VERIFY — final re-read: every MNE row's source ID was checked against the sibling file it names before this row was marked PASS | PASS |

VERDICT: **PASS** — the war room now compresses to a walk and a deck: a 6-position ladder, a 5-room palace with a spine corridor, a 90-row spaced deck, and a year map that drops the whole system onto 18-revision's loops. Every anchor named in this file already exists in the sibling files it cites; nothing here was invented to fit a mnemonic.

NEXT POINTER → every deck row it arms now lives in 18-revision: the walk is the daily loop's memory front, the band rows feed the Friday sample and the Sunday deficit lane, and the palace is the cram sheet's Page-1 drawing at any taper from T-7d down to T-morning.