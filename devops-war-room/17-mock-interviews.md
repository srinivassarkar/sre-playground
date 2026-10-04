# 17 — MOCK INTERVIEWS

Six scripted full interview rounds (45–90 min each) that simulate live, narrated debugging and design work — narration and method get scored, not just the right answer.

**Scoring (7 axes ×10):** technical accuracy / reasoning & structure / communication / depth & nuance / follow-up defense / production judgment / uncertainty handling.

**How to run a round (rigid protocol):**
1. Timer on. Read the round's scenario brief.
2. Give the scripted opening prompt VERBATIM (the interviewer's lines).
3. Record your spoken answers (phone voice memo).
4. Grade yourself on the 7-axis table; transcribe what you actually said for the reflection section.
5. Score and produce the MUST FIX / SHOULD FIX / NICE TO HAVE list.
6. Rule: an answer solved silently in your head is not an answer. Every S block is graded on what came out of your mouth in the clock window.

Round T = technical · R = reasoning/live-debug · S = system-design · B = behavioral/STAR · H = hybrid · F = final comprehensive.

**Round matrix:**

| Round | Type | Duration | Focus | Source assets used |
|---|---|---|---|---|
| ROUND 1 | T | 45 min | Fundamentals gauntlet: elevator, 12 rapid-fire L1 (FT set), 1 go-deep probe, 3 L2 chains | 15-question-bank FT set (FT-105/106/107/109/115/119/122/130/135/139/145/149), 14-attack-chains (14-05/14-07/14-09), 16-resume-defense (ELEVATOR) |
| ROUND 2 | R | 60 min | Live-debug simulation: the narrated SICK-deployment incident, scored on narration + method | 12-troubleshooting INCIDENT 27 (+ 24/25 composite, 28 escalation rule), 15-question-bank FT-160 |
| ROUND 3 | S | 60 min | System design: CI/CD pipeline + rollout strategy for a 3-tier app | 09-cicd, 15-question-bank FT-149/150/151/152, 14-attack-chains 14-13 |
| ROUND 4 | B | 45 min | Behavioral + resume strike: 10 STAR questions with hostile doubling-down probes | 16-resume-defense bullets 16-01..16-18, LIE-DETECTOR list, 14-attack-chains 14-14 |
| ROUND 5 | H | 90 min | Hybrid marathon: T rapid-fire + R mini-debug + S short design + B question in one timed flow | 15-question-bank FT-103/108/117/123/138/147/155/158, 12-troubleshooting INCIDENT 02, 14-attack-chains 14-14 |
| ROUND 6 | F | 90 min | Final comprehensive: 30-sec elevator, full design, live-debug, behavioral, "say you don't know" | 16-resume-defense ELEVATOR, 15-question-bank FT-152/160, 12-troubleshooting INCIDENT 28, 14-attack-chains 14-14 |

Grading do-nots (they convert a real interview into a mock that lies to you): pausing the timer, re-asking yourself aloud, accepting "I knew that I just froze" as a score above 3 on the axis you froze on, and grading the answer you MEANT instead of the answer you SAID.

**Logistics checklist (run before every round — a mock with a dead phone battery is a mock you lose):**
1. Timer running on a wall clock you cannot hide from; a 45-minute round is 45 minutes.
2. Phone voice memo ON — the transcription is the deliverable, not the score.
3. A blank score table (see appendix) and the linked sibling files reachable but NOT open during grading.
4. Pen for the fill-in tables; the round is not complete until the blanks are written.
5. The interviewer voice, not your own voice — read the scripted lines with a stranger's tone, because real interviewers do not remind you to breathe.

**The asset map (every ID-cited source in this file, where it lives — use it to re-drill whatever a round exposes):**
| ID family | File | What this file supplies to the mocks |
|---|---|---|
| FT-101..160, SA-161..300 | 15-question-bank | the L1/L1.5/L2 answer truth for every rapid-fire and its follow-ups |
| CHAIN 14-01..14-14 | 14-attack-chains | the escalation drills (C1–C3 in R1, 14-14 in R4/R5/R6) |
| INCIDENT 01..30 | 12-troubleshooting-playbook | the live-debug scenarios (27, 02, 28 and the families they pull in) |
| 16-01..16-18, LIE-DETECTOR, ELEVATOR | 16-resume-defense | every behavioral anchor, claim-level word, and the honesty contract |
| CICD.P0/P1/P2, BASH.P, AWS.P, OBS.P, SEC.P, 08-terraform, 03-git | sessions 02–11 | the evidence the STARs and designs cite as real, reproducible work |
Asset rule: any model answer here that cites an ID must be re-checkable by opening that file — a mock round that references an ID wrong passes nothing but the misreading itself. Every round's QC row 13 re-verifies exactly that.

**THE COACH'S THREE DOS AND THREE DON'TS (the person running the mock — read this BEFORE picking up the script):**
DO 1 — quarantine the file: the coach audits the round from the target file, but must not read the MODEL answer aloud or the round becomes re-reading. The S-blocks' model answers are for grading and for correction AFTER the timer.
DO 2 — run the clock like a wall: elapsed-clock with a hard cut at each segment. The round's value is the FORCED SWITCH, not completion.
DO 3 — record voice from the first second: the mock is worthless unrecorded; the transcription is the grading object and the FAQ forbids same-hour self-grading for a reason.
DON'T 1 — never grade live: the coach says "logged, moving on", never "good answer" mid-round — positive/negative live feedback corrupts every subsequent sample.
DON'T 2 — never feed the material: if the candidate freezes, the coach's script is "next question", not a hint — the mock measures the freeze, it does not rescue it.
DON'T 3 — never inflate out of kindness: the mock's whole purpose is the honest low axis. A 7 handed out to avoid a hard talk is the most expensive kindness in this folder.
Run-rule: the coach is a metronome with a recording device, not a second candidate. Any deviation from the six runs above is logged in the round's QC, row 13, and the round is re-run.

---

## ROUND 1 — T · 45min · Fundamentals gauntlet

**SCENARIO BRIEF:** Hiring manager + one platform engineer at a mid-market SaaS (12-person platform team). The vibe is fast and volume-based: they will cover a lot of surface to find your ceiling, then spend the last third testing one answer in depth. Round one decides whether you get the system/design round at all. The candidate is 1–3 YOE, claims depth per file 16 claim-levels, and must not outrun those claims.

**OPENING PROMPT (say verbatim):** "Let's start with you. One minute — who are you and what do you actually do behind the DevOps title? Then I'm going to move fast and fire a bunch of quick ones; say 'pass' or take a swing, but keep moving."

**THE WARM-UP SET (3 minutes before the timer — vocalize these OUT LOUD so the first graded answer is not your first spoken sentence of the day):**
1. "Connect to a host that refuses ssh. Say my next three commands and what each tells me."
2. "Divide a /24 into four equal subnets. Say the CIDRs and the usable-host count."
3. "A 503 from the load balancer. Say which of the earlier layers tells me targets are missing."
4. Read the file-16 elevator out loud twice — once for speed, once for pacing.
Warm-up rule: the first 15 seconds of a graded round are a vocal warm-up whether you plan it or not — a cold voice rambles or rushes. A fixed 3-minute spoken routine front-loads the mechanics so the S0–S12 answers start warm.

**THE ANSWER-LEAD STRUCTURE (the shape every fast answer must take — name it, prove it, land it):**
| Beat | What it buys | Example (S3 refused/timeout) |
|---|---|---|
| Lead = the mechanism | grades technical accuracy immediately | "Refused is an RST; timeout is silence." |
| Prove = 1 exact fact | grades depth + credibility | "Accept-queue-full timeout is a server-side explanation for a 'timeout' read." |
| Land = the next move | grades production judgment | "First `dig`, then `ss -tlnp`, then `curl -v` classifies them." |
Three beats, one breath each, under the clock. The single most common round-one tape error is answering beats TWO and THREE first and never landing beat one — which reads as depth without precision.

**S0 — The elevator (clock 2 min) · source: 16-resume-defense THE 30-SECOND ELEVATOR**
Interviewer: "One minute — go." Deliver the elevator from file 16 verbatim, then stop talking.
Model answer (compress the file-16 script): "I'm a DevOps engineer at the 1–3 year mark and I won't claim deeper than I can prove. My thing is the full delivery spine — I build a pipeline, ship a container, run it in Kubernetes, and watch it, including breaking it and fixing it. Three honest anchors: I ran a Docker-to-ECR-to-EKS deployment live and hit a real scheduling constraint I had to fix; I operate a Prometheus and Grafana stack and can explain why I alert on percentiles, not averages; and I train incident response against a thirty-incident playbook where every run ends with a documented prevention. If a bullet on my resume can't survive your next three questions, I'll tell you to cut it myself."
Scoreable points: (a) sets the depth ceiling in the first ten seconds — no inflated claims to backpedal from; (b) names three anchor stories that map to real war-room sessions; (c) hands the interviewer the policing rule ("cut it myself") before they can use it against you; (d) ends with an invitation that hands them the next question, not a wall of tools. The elevator's whole job is getting the interviewer excited to probe the anchors — the interviewer will try to attack the strongest one, so S0 fails if any of the three anchors is a claim you cannot defend at 16 claim-level OPERATED.

**ELEVATOR VARIATIONS (the three phrasings an interviewer will hear all day, and the stress each one puts on your anchors):**
| Variation | When it is fired | The adjustment you make, not a new script |
|---|---|---|
| "Who are you and what do you do?" | the warm opener | full script above, end on the wheel-handoff question |
| "Summarize your last year in one minute — go." (zero reaction) | the pressure variant; the interviewer wants to see if you ADD claims under silence | SAME three anchors, SAME order — the no-reaction test is about whether silence makes you pad with weak claims |
| "Two minutes: strengths, one thing you are still weak at." | the honesty variant | deliver an anchor, then lead the weakness instead of being cornered: "the one I do not pad is fleet-scale tuning — PRACTICED, not DESIGNED" |
Variation rule: every phrasing is answered with the same three-anchor backbone. A change of script under a changed opening is the classic tell that the elevator was memorized, not owned — the backbone is what the anchors are defending.

**S1 — Linux · permissions + ssh (clock ≤30 s) · FT source: FT-105**
Interviewer: "Walk the rwx permission model, and debug 'ssh: Permission denied (publickey)'."
Model answer (L1 floor): rwx = read/write/execute; octal 7=rwx, 6=rw-, 5=r-x, 4=r--; on a directory x means traverse. For ssh: the client offers keys; the server signs the private key you hold against `~/.ssh/authorized_keys` of the user you target. Denial means the offered key is not accepted. Work client to server: `ssh -v` shows which keys are offered; on the server check the right user, the key in authorized_keys, and StrictModes file permissions — 0644 private key is rejected by the client, and a group/world-writable `~/.ssh` makes sshd ignore authorized_keys by design.
Scoreable points: names octal mapping and directory-x; names the client/server split; names SSH StrictMode permission trap; lands the top cause (perms/StrictMode) rather than re-adding keys. The FT entry's follow-ups (server-side usernames, `PubkeyAuthentication`, root locked from keys) are the L2 escape hatch if probed.

**S2 — Networking · CIDR (clock ≤30 s) · FT source: FT-106**
Interviewer: "/24, /25, /30 — how many addresses, and which is a point-to-point link?"
Model answer (L1 floor): each /N halves the address space. /24 = 256 addresses (254 usable hosts), /25 = 128 (126 usable), /30 = 4 (2 usable) — the classic point-to-point link pair. The host bits = 32 − N: /24 has 8 host bits. Network and broadcast addresses are the two non-usable ones in a typical subnet.
Scoreable points: does the math by host bits, not memorized tables; names /30 as point-to-point; notes network + broadcast. Watch the trap: "254 usable" assumes a broadcast subnet — a /31 is the zero-broadcast RFC 3021 point-to-point case, which is a senior bonus, not required here.

**S3 — Networking · refused vs timeout (clock ≤30 s) · FT source: FT-107**
Interviewer: "Connection refused versus timeout — what is really different?"
Model answer (L1 floor): refused = you got an immediate TCP RST back — the path works, an answer came, and the port (or host/IP) is actively closed. Timeout = your SYN got no reply at all — silently dropped or lost. Refused causes: nothing listening, wrong bind address (service on 127.0.0.1, you hit the LAN IP), a REJECT firewall. Timeout causes: host down, no route, DROP firewall, packet loss/MTU, overloaded server whose accept queue is full. Tools: `curl -v` (instant RST vs hang), `nc -zvw2`, `ss -tlnp` on the remote, `dig +short` first.
Scoreable points: the RST-vs-silence distinction is the whole answer; refuses to say "refused = server down" (it is the opposite shape — something answered); names accept-queue for the busy-server timeout case.

**S4 — Networking · HTTP status taxonomy (clock ≤30 s) · FT source: FT-109**
Interviewer: "401, 403, 404, 502, 503, 504 — one line each, then tell me which two are easiest to confuse."
Model answer (L1 floor): 401 = not authenticated (no/missing credentials); 403 = authenticated but not allowed (authZ); 404 = the path does not exist at the server; 502 = upstream/proxy got an invalid response (bad gateway); 503 = service unavailable, often no healthy target at all; 504 = upstream timed out. Easiest to confuse: 502 vs 503 — 502 means a target answered badly, 503 means there was no healthy target to answer. Also 401 vs 403 is the classic authN/authZ pair.
Scoreable points: clean one-liners; names the 502/503 confusion and the 401/403 authN/authZ split; lands on "503 = no healthy targets" which ties to INCIDENT 04 (ALB 502/503).

**S5 — Bash · set -euo pipefail (clock ≤30 s) · FT source: FT-115**
Interviewer: "What does set -euo pipefail do, and what failure modes survive all three flags?"
Model answer (L1 floor): `-e` exit on first command failure; `-u` treat unset variables as an error; `-o pipefail` make a pipeline return the last non-zero exit code of any element. Survivors — the failure modes that still pass through: a failing command that is on the left of `&&`/`||`, a failing command already inside an `if` condition, a command in a subshell whose exit code you mask with `$?` misuse, and a pipeline element whose failure you intentionally ignore with `|| true`. Those are the cases that burn people and why `-e` alone is the weak version.
Scoreable points: names all three flags accurately; names the survivors (conditions and `&&`/`||` inhibit `-e`); the "|| true" escape hatch being named means you have actually written scripts, not just read about them.

**S6 — AWS · IAM model (clock ≤30 s) · FT source: FT-119**
Interviewer: "Users, groups, roles, policies — and how does a policy get evaluated?"
Model answer (L1 floor): users are long-lived people/identities; groups bundle permissions for users; roles are assumed identities with temporary credentials via STS; policies are JSON allow/deny statements on an identity or a resource. Evaluation: explicit deny beats any allow, then an explicit allow wins, else implicit deny. Both the identity-side and the resource-side policy matter. Least privilege = grant only the actions/resources the workload needs.
Scoreable points: names roles as assumed-with-temporary-creds; states deny-wins-over-allow exactly; mentions identity AND resource side; ties to the assumption flow (STS) without going too deep.

**S7 — AWS · ALB 502 (clock ≤30 s) · FT source: FT-122**
Interviewer: "A load balancer returns 502. Walk the chain from client to backend and tell me where the failure lives."
Model answer (L1 floor): client → ALB listener (TLS term) → listener rule → target group → healthy targets. The ALB probes each target with a health check path; traffic goes only to healthy targets. 502 = the ALB reached a target but the target's response was invalid (closed mid-stream, wrong protocol — e.g. HTTPS configured against an HTTP app). 503 is the different one — no healthy target at all. Triage: `describe-target-health` first, then the SG that must allow ALB→target:port, then whether the app listens on that port/path, then the health-check path itself.
Scoreable points: names the listener→rule→target-group chain; separates 502 from 503; knows 503 = no healthy targets; first step is checking target health, not guessing.

**S8 — Docker · image vs container (clock ≤30 s) · FT source: FT-130**
Interviewer: "Image, container, layer — what is what, and what does a running container add on top?"
Model answer (L1 floor): image = an immutable, layered snapshot — the blueprint, shipped via a registry; container = that image plus one writable layer, executed as processes in isolated namespaces (PID, net, mount, UTS, user) on the host kernel; layer = the diff produced by one filesystem instruction (RUN/COPY/ADD). Non-filesystem instructions (ENV, CMD, EXPOSE) are config-only zero-byte rows. Writes land in the writable container layer and vanish on delete unless a volume holds them.
Scoreable points: correct three-level model; names namespaces and the shared host kernel (not full isolation); knows volumes are the persistence escape; the CMD/ENTRYPOINT config-row fact is the depth tell.

**S9 — Kubernetes · control plane (clock ≤30 s) · FT source: FT-135**
Interviewer: "Which control-plane component does what, and where does Kubernetes actually store its state?"
Model answer (L1 floor): kube-apiserver is the front door — authenticates, authorizes via RBAC, validates, and is the only component that talks to etcd. etcd holds ALL cluster state. kube-controller-manager runs the controllers that reconcile desired state (deployments, replicasets). kube-scheduler assigns pods to nodes (decides WHICH node; it does not run the container). Each node runs kubelet, which actually runs the containers via the CRI. cloud-controller-manager bridges cloud APIs (EKS: load balancers, nodes).
Scoreable points: the "scheduler decides which node, kubelet runs the container" line is the money sentence; names etcd as the only state store; separation of apiserver vs controller-manager vs scheduler.

**S10 — Kubernetes · Service → endpoints (clock ≤30 s) · FT source: FT-139**
Interviewer: "A Service resolves fine in DNS but connections hang. Where does the truth live?"
Model answer (L1 floor): a Service is a stable ClusterIP + a label selector + port mapping, and kube-proxy programs iptables DNAT to the current endpoint set. The selector builds the endpoints list — the real pod IP:port list. If the selector matches no pods, endpoints is empty and traffic has nowhere to go: DNS resolves (the name promise works) but nothing answers (the routing promise is broken). Check `kubectl get endpoints <svc>` first — empty endpoints is the signature; then compare the selector to the pod labels; then check readiness gating.
Scoreable points: the two-promise model (name promise vs routing promise); empty-endpoints-first; readiness gating mentioned; directly mirrors INCIDENT 02.

**S11 — Terraform · what state is for (clock ≤30 s) · FT source: FT-144**
Interviewer: "What does terraform.tfstate actually do, and why is it both precious and risky?"
Model answer (L1 floor): tfstate is the ownership ledger that maps config addresses to real-world objects, stores their attributes, tracks the dependency graph, and makes plan compute a diff against reality. Precious: without it Terraform cannot see what it already owns, and a delete or a fresh apply either duplicates or orphans running infrastructure. Risky: it contains sensitive attributes, it is the single point of truth — never commit it to git, keep it in a remote backend with locking, and use `terraform state mv/rm/import` instead of editing it by hand.
Scoreable points: "ownership ledger / mapping config to live objects" not "cache"; names backend+locking; the hand-edit prohibition; ties to INCIDENT 22 (state lock) and INCIDENT 23 (plan wants destroy).

**S12 — CI/CD · CI vs CD (clock ≤30 s) · FT source: FT-149**
Interviewer: "The three-word test: CI, Continuous Delivery, Continuous Deployment — go."
Model answer (L1 floor): CI proves the merge — build, unit tests, lint, artifact, every push to trunk; the artifact is the merge's success certificate. Continuous Delivery = the artifact is always shippable and deployable via automation, with a human/approval pulling the trigger. Continuous Deployment = the deploy happens automatically from the pipeline. The distinction gate is who pulls the trigger. A pipeline is stages wired by gates, with exactly one immutable artifact per run and fail-fast on red.
Scoreable points: the three definitions land in under a minute; names the trigger-puller gate; adds one-artifact + fail-fast without being asked (depth tell); refuses to answer "CI/CD = GitHub Actions".

**SECOND PASS — THE FOLLOW-UP ESCAPES (clock 8 min, one per S block)**
The interviewer does not stop at your L1 floor — the FT set ships follow-ups for exactly this moment. Drill these so the L1 answer already knows where the L2 probe is going.

| From | Likely follow-up | Model one-liner |
|---|---|---|
| FT-105 | "Keys look right but still denied — top cause?" | StrictModes: a group/world-writable `~/.ssh` or home makes sshd ignore authorized_keys by design. |
| FT-106 | "How many /24s fit in a /16?" | 2^(24−16) = 256 — the math is host-bits, doubling per /N. |
| FT-107 | "Server is up but clients see refused — why?" | It listens on the wrong interface (127.0.0.1 vs 0.0.0.0) or a REJECT rule; verify with `ss -tlnp`. |
| FT-109 | "Which one means the backend is not even reached?" | 503 — no healthy target; 502 means a target answered badly. |
| FT-115 | "What one line turns `-e` back on inside a condition?" | Conditions and `&&`/`||` suppress `-e`; the loud pair `|| exit 1` re-arms it deliberately. |
| FT-119 | "Admin policy is attached and still denied — what beats it?" | An explicit deny in a resource/identity policy — deny outranks AdministratorAccess. |
| FT-122 | "502 with healthy targets — left in the tank?" | The target misbehaves at request time (protocol mismatch, early close) or a listener rule sends traffic elsewhere. |
| FT-130 | "latest vs digest — which is the truth and why?" | Digest: `latest` is a mutable pointer that can mean two different images over time. |
| FT-135 | "Where does each piece of state physically live?" | etcd holds all cluster state; the scheduler writes spec.nodeName; there is no other state store. |
| FT-139 | "Populated endpoints but still failing — next split?" | targetPort (endpoint points at a port that does not listen) vs NetworkPolicy vs kube-proxy staleness. |
| FT-144/145 | "A crashed apply left the lock — correct unlock?" | Read the DynamoDB lock item (who/when/instance), confirm no live run, then `force-unlock` — never hand-edit state. |
| FT-149 | "Red build — deployable if the team says 'just this once'?" | Gates are the contract: a red gate blocks promotion by design; the exception is unlocked envs with explicit sign-off, named as such. |

The pattern the interviewer is grading in the second pass: each follow-up must be answered from the SAME model as the L1 answer, with no retraction and no topic-switch. Score 1 point per escape answered clean, 0.5 for a hesitation longer than the clock, 0 for a contradiction.

**CLOCK MAP AND FAILURE PATTERNS**
If this round ran long or short, the map below says where the leakage happened:

| Segment | Budget | Typical failure pattern |
|---|---|---|
| S0 elevator | 2 min | Speaking past the one-minute mark; unpacking anchors instead of stopping |
| S1–S12 rapid-fire | 9 min (45 s each) | Drifting into the L2 answer on question 3, then running out of time on 8–12 |
| Second pass (escapes) | 8 min | Answering the follow-up BEFORE the interviewer asks it, or not knowing the follow-up exists |
| Go-deep | 6 min | Switching topics per probe instead of doubling down on S10 |
| Chains C1–C3 | 25 min (8 min each) | Treating the chain as re-questioning and giving L1 answers again |
| Wrap + score | 5 min | Skipping the transcription; the round then teaches nothing |

The three failure signs that matter: (1) rambling past a clock (communication axis); (2) L1 answers that leap to L2 (the interviewer cannot tell if you know the baseline); (3) follow-ups answered by switching to a different subject (follow-up defense axis — the deepest cut of the day).

**THE SAME QUESTION AT THREE DEPTHS — how the interviewer escalates the SAME topic (drill: answer all three ACEs for each row in ≤90 s total)**
| Topic (L1 block) | L1 (the floor question) | L1.5 (the probe that follows) | L2 (the depth row) |
|---|---|---|---|
| Permissions (S1) | "What is rwx?" | "Why would `ssh` fail with perms correct?" | "StrictModes on: 0644 key AND correct home — what else silently denies?" |
| Refused/timeout (S3) | "Refused vs timeout?" | "Which one can be caused by an overloaded server?" | "Accept queue full — what do you SEE from the server side before you take a capture?" |
| HTTP codes (S4) | "One line each" | "Which two are easiest to confuse?" | "401 arriving from an ALB before your app — what just happened in the auth chain?" |
| IAM (S6) | "Users/roles/policies?" | "Denied despite a visible allow?" | "Both identity AND resource side permit — what two causes remain?" |
| Service/endpoints (S10) | "Service resolves, hangs?" | "Endpoints empty — the fix?" | "Endpoints populated and traffic STILL does not land — the split?" |
| CI/CD (S12) | "CI vs CD vs CDep?" | "What is Continuous Delivery vs Deployment?" | "Red gate overridden 'just this once' — what did the override cost in the system?" |
Scoring rule: an L1 that collapses at L1.5 is a depth-3; an L1 that holds to L2 with the mechanism intact earns the depth-axis 8. The drill trains the ladder so the interviewer never outruns you on a topic you already answered.

**THE "PASS" VOCABULARY — if you have to pass, pass in a way the interviewer can grade**
A hard "pass" is an answer. These eight forms all score from 3 to 6 on uncertainty handling (never 1 — silence scores 1):
| Form | What you literally say | Axis it buys you |
|---|---|---|
| The partial | "I know X fully; Y I have only read about — here is my model of Y, which I would verify" | uncertainty 5 |
| The split | "I am about 80% on this — the two things I am sure of are A and B; the part I would double-check is C" | uncertainty 6 |
| The probe-planner | "I have not hit this. The cheapest way to find out is <command/repro>, which is what I would do now" | production judgment 6 |
| The claim-cut | "At 16-claim levels this bullet is UNDERSTOOD, not OPERATED — so I will answer as an underst-ooder" | honesty +8 on its own |
| The mechanism-only | "I do not remember the exact flag, but I know the mechanism it implements — would you accept the mechanism?" | follow-up defense 6 |
| The example-swap | "I know the pattern on a different tool; the same failure shape applies — may I draw the parallel?" | reasoning 6 |
| The explicit-reserve | "I will answer what I am sure of, then flag the rest as uncertain" | communication 6 |
| The stop | "I do not have this one, full stop" — then silence, no recovery ramble | cleanliness 6 |
The rule: never pass with "I don't know" and a shrug; the pass must name what you DO hold, or what you would DO next. The exception — sometimes the truthful answer is the full stop, and a full stop beats a fabricate every time.

**THE INTERVIEWER GOES DEEP — target: S10 (Service → endpoints) (clock 6 min total, 3 probes)**
The interviewer picked S10 because empty-endpoints is the single most common reachability incident in k8s shops. Each probe doubles depth on the SAME topic; the scoreable move is never switching to a different topic.

**Probe 1 (why it matters):** "So the Service name resolves, the pod is Running and Ready — and clients still time out. Where is the broken promise now?"
Model answer: then the endpoints list is populated but the traffic still does not land. That splits into targetPort (the endpoint IP:port points at a container port nothing listens on, so you get refused at the pod), a NetworkPolicy dropping it, or kube-proxy rules being stale/absent. Order: re-read endpoints (are the IP:port correct?), probe the pod IP:port directly in-cluster to separate pod-level from proxy-level, then read kube-proxy state. The money line: populate endpoints ≠ traffic lands. Scoreable points: refuses the easy "it's the network" answer; builds the split; names targetPort as a populated-endpoints trap (INCIDENT 02 hypothesis 3).

**Probe 2 (the gate layer):** "A pod is Running but 0/1 Ready. Does the Service route to it or not? And who made that decision?"
Model answer: no. Readiness gates the endpoints list — kubelet probes the readiness path, and until it passes the pod is not in the endpoint set, so the Service has nowhere to send traffic. That is the readiness gate (FT-137, INCIDENT 20): liveness restarts, readiness routes. A not-ready pod gets zero traffic even though the process is alive; a ready-but-broken pod gets traffic even though it is crashing — which is why readiness probe paths must reflect true serving readiness.
Scoreable points: names kubelet as the prober; names endpoints membership as the effect; distinguishes liveness vs readiness consequences; lands on the readiness-path-contract insight.

**Probe 3 (the fix + prevention):** "You named the cause. Now — what do you change, and what do you add so this class of incident stops?"
Model answer: fix the immediate: correct the selector label or fix the probe path, then verify with `kubectl get endpoints` showing the pod IP:port and an in-cluster probe returning the app's real 200. Prevent the class: (a) a smoke probe in CI that hits the actual readiness path of the built image before deploy (CICD.P0.6 pattern); (b) alert on empty/zero-byte endpoints for the Service, like you alert on 0 replicas; (c) make the Service selector and the Deployment pod labels a checked-in, reviewed pairing rather than ad-hoc labels.
Scoreable points: fix→verify with the same artifact; prevention addresses the pipeline and the monitoring gap, not just the labels; the endpoint-count alert is a production-judgment tell the interviewer is listening for.

**ALTERNATE GO-DEEP TARGETS (6 more single-topic probes in the same shape — swap the S target on re-runs so the go-deep muscle generalizes):**
| Target | Probe 1 (split the space) | Probe 2 (the gate layer) | Probe 3 (fix + prevent) |
|---|---|---|---|
| S1 perms/ssh | denied with perms right — the remaining paths | StrictModes + PubkeyAuthentication off — which wins | fix + the scan/prevent pair for a fleet |
| S3 refused/timeout | busy server — which read shows it | accept-queue full — kernel behavior at the edge | fix + the alert that would have caught it first |
| S6 IAM | denied despite an allow — the two surfaces | identity vs resource policy intersection | fix + the read-only census as prevention |
| S7 ALB 502 | healthy targets but 502 left | protocol mismatch + early close | fix + a health-check-path contract in CI |
| S12 CI/CD | red gate overridden "just once" | the same-artifact and fail-fast rules | fix + the approval-model change for exception gates |
Drill rule: one alternate target per re-run, full 3-probe depth, 6 minutes — the go-deep is the round's only revenge on the "you only interviewed my breadth" trap, and it must generalize beyond Service→endpoints or it is one story, not a muscle.

**THE LOW-REACH TOPICS SET (five FT rows the round forgets — run a 6-minute gauntlet of just these on re-runs 3 and 5):**
| Topic | The one-liner that must land | The probe that follows if you skate |
|---|---|---|
| FT-101 observability taxonomy (metrics/logs/traces) | "metrics are numerics you can aggregate, logs are the unstructured record, traces are the request path — an incident usually wants all three, first trace, then logs" | "Which one do you open first at pager time and why?" |
| FT-102 signal-vs-noise alerting | "an alert is a decision-by-number, so every alert must carry a clear action or it is noise" | "Convert one actionless alert you know into a decision-shaped one." |
| FT-104 exit codes + zombie/backlog | "exit code 137 is 128+9 SIGKILL; a backlog build logs dead workers, exit 1, not crashes" | "Which read proves it is a backlog and not a crash?" |
| FT-109 reporting in on-call | "report on-read, not on-solve; the first sentence is the worst fact" | "What is the ONE fact that must be on the wire in the first 60 seconds?" |
| FT-110 COPY statement + WAL | "COPY bypasses the WAL the way a batched insert cannot — a big COPY then crash is flush-loss the hard way" | "What changes your restore story after a COPY?" |
Topic rule: re-runs 3 and 5 open with these five as the entire rapid-fire set. R1 monitors whether you now sell DIFFERENT topics as your depth than six weeks ago — if the low-reach set still wobbles on re-run 5, the breadth muscle is only rehearsing the comfortable half and the gap is named in the final report.

**THREE L2 CHAINS (clock ≤60–90 s each) · source: 14-attack-chains**
Chain rules from file 14: L2 rows go ≥60 s and must answer the mechanism, not just the fix. These are the three "we interviewed the candidate for depth and one junior told us 'I mostly remember the fix'" questions.

**C1 — Chain 14-07 KUBERNETES · L2 row (probes) · clock ≤60 s**
Interviewer: "One pod shows 0/1 while the process is healthy; another shows 1/1 while traffic to it fails. Who runs the probes, and when is each state the right one?"
Model answer: two loops with different actors. kubelet probes and restarts (liveness — failure restarts the container; startup defers both probes for slow-start). The Service/endpoints layer reacts to readiness — a failed readiness probe removes the pod from endpoints (no traffic, no restart). So a healthy-but-booting process with a liveness initialDelay too short gets killed → CrashLoopBackOff (INCIDENT 16's probe branch); a not-ready but alive pod gets zero traffic (INCIDENT 20); and a Ready-but-crashing pod is the genuinely harmful one, because it holds traffic. The "0/1 healthy process" case is almost always a bad probe contract (wrong path or port); the "1/1 but traffic fails" case is the probe passing while the app breaks at request time — the probe does not exercise what the client hits.
Scoreable points: names kubelet vs endpoints as different actors; maps each state to its incident; the Ready-but-crashing insight; states that the probe must exercise the traffic path, not just the process.
Trap to dodge: "liveness = is the pod healthy" without saying liveness *restarts* and readiness *routes*.

**C2 — Chain 14-09 CI/CD · L2.5 row (release identity) · clock ≤90 s**
Interviewer: "Git tag, build version, branch name — what identifies a release, and what breaks when they drift?"
Model answer: one source-of-truth identifier — the git tag (v1.2.3) captured at build time, with the registry digest. A release is one immutable set of bytes tagged once. If the "version" is the branch name, prod looks tagged while the actual deployed artifact sits under a build-id; if the tag is edited after merge, the published build no longer matches the source. The concrete breakage is INCIDENT 29: the pipeline succeeded but the site still served the old version because a mutable tag was re-pointed at old bytes — one tag, two realities, nothing rolled out, and no smoke caught it because no one compared the served version string. Discipline: capture the tag+digest at build, deploy by digest, and after rollout smoke-probe the served version string.
Scoreable points: names tag-as-identity; explains the drift mechanics; tells INCIDENT 29 with the served-version-string lesson; ties to the same-artifact promotion rule (FT-150).
Trap to dodge: answering "we use latest so we're always current" — that is the recruitment poster for the same-tag trap.

**C3 — Chain 14-05 AWS · L2 row (SG vs NACL) · clock ≤60 s**
Interviewer: "One direction of traffic works, replies drop. Walk security groups versus NACLs and find the layer that forgot its rule."
Model answer: SG is instance/ENI-level, stateful, allow-only — the return direction of an allowed flow is auto-blessed while tracked; "no rule" is the deny. NACL is subnet-level, stateless, ordered, with explicit allow AND deny — its return/reply traffic is a NEW packet and needs its own rule (ephemeral range 1024–65535). The classic failure: inbound 443 allowed but no ephemeral outbound rule, so replies get dropped — the flow's request succeeded at the SG but died at the stateless NACL. A packet must pass BOTH the NACL and the SG inbound, and both the inverse outbound; the effective decision is the intersection, and the debugging question is which direction forgot its rule.
Scoreable points: stateful vs stateless is the mechanism; names the ephemeral-port reply trap precisely; says "intersection" of both layers; maps to the real failure signature instead of "just open the port".
Trap to dodge: "the NACL only matters for subnet defaults" — the layers intersect on the packet path and statelessness is exactly where replies die.

**THE CHAIN ANSWER TEMPLATE (every L2 chain row has a four-beat spine — drill any chain into it):**
| Beat | What it provides | C1 example (probes) |
|---|---|---|
| 1 — Two-entity setup | tells the interviewer WHICH things interact | "two loops with different actors" |
| 2 — Mechanism | answers how, not what | "liveness restarts; readiness routes" |
| 3 — Consequence map | the failure modes that follow | "CrashLoopBackOff vs zero-traffic vs Ready-but-crashing" |
| 4 — The corrected model | the principle that survives follow-ups | "the probe must exercise the traffic path, not the process" |
Chain-spine rule: if a chain answer does not land on the full four beats, re-drill the row — the L2 grade is the four beats, and a missing consequence-map is where the interviewer's "so what happens when…" probe lands with nothing to catch it.

**FULL SCRIPTED EXCHANGE — 90 SECONDS OF RAPID-FIRE (grading reference)**
A verbatim-shaped slice of the round, showing the cadence a 45-second answer needs. Grade your recording against the rhythm, not the words:

Interviewer: "Refused versus timeout — what is really different?"
Candidate: "Refused means I got an RST back — something answered and actively closed the port, or nothing is bound there, or it's bound on the wrong interface, or a firewall is told to reject. Timeout means my SYN got silence — a drop rule, no route, host down, or a server whose accept queue is full. First I resolve, then I look at what's listening from the host itself, then I classify with curl."
Interviewer: "And on this box, curl hangs. One next move, not two."
Candidate: "Then it's timeout-class. Before blaming the network I check whether the server is saturating — `vmstat` for the load before tcpdump, because an accept-queue-full symptom has a server-side explanation."
Interviewer: "Good. New one — IAM evaluation order."
Candidate: "Explicit deny beats any allow; with no deny, an explicit allow wins; otherwise it's implicit deny. Both the identity policy and the resource policy must allow. So a denied call with an allow visible is either a deny doc somewhere or a wrong action/resource ARN."

What the interviewer heard: a mechanism (RST vs silence) plus a decision (name one next move), then a compressed IAM evaluation with the two-surfaces rule — no filler, no "it's like". The candidate never touched the wrong layer and stopped when the question closed.

**POST-ROUND DEBRIEF — WHAT THE HIRING MANAGER WOULD NOTE**
Three sentences to have ready when a recruiter asks "how did it go", translated into scoring terms:
- "The breadth surface held — every L1 answer landed at the scoreable-point floor, and the escapes came from the same model, not from memory fragments." (technical + follow-up defense)
- "The go-deep confirmed the depth ceiling: Service/endpoints stayed on-topic through three probes and named the readiness-gate and targetPort branches without drifting." (depth + reasoning)
- "I flagged my own fences — load, network tuning, and fleet-scale are PRACTICED-or-lower, and I said so instead of padding." (production judgment + uncertainty)
If you cannot honestly produce any of those three when the round is done, the axis behind the missing one is your ROUND 1 must-fix even if every question was answered.

**THE ROUND-1 WEEKLY DRILL SCHEDULE (the gauntlet's material is breadth — it decays in ~72 hours without repetition):**
| Day | Drill | Clock | Source |
|---|---|---|---|
| Mon | 12 rapid-fire, wall-clock only, no grading | 9 min | 15-question-bank FT set |
| Tue | SECOND PASS escapes, all 12 | 8 min | this round's table |
| Wed | one go-deep (rotate the S target weekly) + 1 L2 chain | 12 min | 14-attack-chains |
| Thu | the SAME question at three depths, 4 topics | 10 min | this round's ladder |
| Fri | full ROUND 1 under the exact protocol | 45 min | this round |
| Sat | grade Friday's tape at +24h (appendix rubric), fill the blanks | 30 min | appendix |
| Sun | rest the tape — read one sibling file's summary instead | 20 min | any 02–11 session |
Schedule rule: the daily reps are the floor, the Friday full round is the ceiling. A week with only the Friday round is a week of grading a cold muscle; the schedule exists because breadth will not hold in your head otherwise.

**THE ROUND-1 TEN-SECOND PASS MARKERS (ten ticks to check on the +24 h tape — each one a breadth-axis sentence you either nailed or you did not):**
1. Every S-block opened in under 5 seconds — no "um, let me think, so basically" runway.
2. Zero topic refused; every "I am not sure" became a three-phase or a fence, not a deflection.
3. The go-deep target took all THREE probes and the fix ended in a verify.
4. The L2 chain answers ran ≥60 s with a mechanism statement, not just the fix.
5. No claim crossed its 16-resume-defense claim level in the tape.
6. The answer-propellant structure held: every closed answer ended with a proof or next-command, never a trailing "yeah".
7. The clock was hit on every segment — no segment ran over and no segment ran dry.
8. The same FT concept answered twice matched itself (no drift under fatigue).
9. Two or fewer filler words per minute (count them — that is the metronome metric).
10. The round closed with the interviewer-facing question, not a recap of topics.
Marker-rule: a tape failing more than two markers is not a breadth problem, it is a clock-and-shape problem — re-drill the answer-propellant structure (THE PASS VOCABULARY) before touching any topic-detail; the topics were almost certainly fine.

**THE BREADTH DECAY TABLE (R1's material decays fastest of all six rounds — schedule its defense like a perishable):**
| Material | Half-life without a rep | The defense rep that resets it | Re-drill trigger on tape |
|---|---|---|---|
| FT one-liners (all 60) | ~72 h | the Monday + Thursday rapid-fire sets | an S-block answer wobbles >10 s to open |
| Go-deep probe ladders | ~1 week | the Wednesday 3-probe rotation | a probe-2 answer collapses to a sentence |
| L2 chain mechanisms | ~1 week | the Thursday chain session | a chain ends in "I mostly remember the fix" |
| Answer-propellant structure | ~2 weeks | any single 10-question rapid fire | filler-word count climbs above 2/min |
| Clock discipline | ~1 week | the Friday full round ONLY | any segment overruns its cap |
Decay-rule: the decay table is why the WEEKLY DRILL SCHEDULE is the round's real product — the Friday round is the measurement, the four spread-out reps are the defense. Skip the reps for a fortnight and the Friday tape re-learns what Monday already knew.

**THE ROUND-1 WORD-BANK (the exact sentence shapes the interviewer writes down — same function as R3's phrase sheet, for the rapid-fire register):**
| S | The answering pattern to say, not to think |
|---|---|
| S1 perms/ssh | "refused = something answered RST, so the port is closed, not bound, or filtered — I'd read ss before I'd page" |
| S3 refused/timeout | "refused is definitive; timeout is the ambiguous one — down OR filtered, and accept-queue-full is the busy-but-silent case" |
| S4 dns | "dig first, then resolve; NXDOMAIN vs SERVFAIL are different promises" |
| S6 IAM | "allow requires identity AND resource policy to agree; deny wins, then it is explicit" |
| S7 ALB 502 | "502 vs 503 differ — 502 got a bad answer, 503 found no target; target-health reads it in one command" |
| S9 k8s pod lifecycle | "crash sums the exit code; 137 is SIGKILL; a probe failing is NOT a crash — they page differently" |
| S10 k8s rollout | "undo is a new revision at the old bytes — not time travel; verify with served-version" |
| S11 terraform state | "state is the ownership ledger; plan is a diff, not a promise" |
| S12 CI/CD | "same artifact, fail-fast, deploy proves the placement, not the intention" |
| S15 log analysis | "the error line is a witness, not a confession — the CALLER wrote it; check exit codes and the next line" |
| S14 capacity | "requests schedule, limits enforce; the two are not the same sentence" |
Bank-rule: recite the bank before the round as the ten-minute warm-up, then never re-read it during — the bank is the shape the tape should reproduce FROM MEMORY, which is what "rehearsed, not owned" would fail to do. Any S whose shape came out different on tape is the re-drilled S for the next session. When the warm-up recital is word-perfect for two consecutive sessions, the bank has moved from the page into the workroom and R1's breadth axis is being carried by habit, not by the file.

**SCORE TABLE (7 axes):**

| Axis | /10 | Why |
|---|---|---|
| Technical accuracy | | Grade each rapid-fire: exact cites vs hand-waving. 1 pt for each of the 12 answers that hit all scoreable points. |
| Reasoning & structure | | Did the structure move client→server (S1), name-vs-routing promise (S10), two-actor probes (C1) — or jump to the fix? |
| Communication | | one-breath answers within clock; no "um, it's like"; did you stop after answering or ramble? |
| Depth & nuance | | C1/C2/C3 mechanisms landed; go-deep probes stayed on-topic and went two levels; bonus facts (targetPort trap, Ready-but-crashing) present. |
| Follow-up defense | | Probes 1–3 survived without contradiction; no claim needed retraction; this is each FT's follow-up loop. |
| Production judgment | | Fix→verify-and-prevent framing; endpoint-count alert; INCIDENT 29 served-version proof; nothing said that outruns 16 claim-levels. |
| Uncertainty handling | | Any "pass" you said was clean; instead of bluffing you named what split the space next. |

**REFLECTION (fill after):** _what I said_ — transcribe your voice memo here. _where I froze_ — which S block deadened, and why (unknown fact, clock pressure, memory, topic). _where I overclaimed_ — every claim that outran the 16-resume-defense claim-level; the fix for each is a downgrade or +24h drill.

**MUST FIX / SHOULD FIX / NICE TO HAVE:**
| MUST FIX | SHOULD FIX | NICE TO HAVE |
|---|---|---|
| Any S block with a scoreable point missed; fix via its FT entry follow-up loop | Go-deep probes that drifted topic instead of deepening | Bonus facts (RFC 3021 /31, ETag, k8s startupProbe) |
| Any claim > claim-level (downgrade it now, not on interview day) | Ramble control: stop at the scoreable points, do not re-answer | Zero-byte/empty-endpoints alert as a production-judgment mention |
| Chain rows that scored < 4 (re-drill at +24h/+48h per file 14 rules) | C2 INCIDENT 29 story told without the served-version-string closing | "pass" said cleanly and calmly (never a failed guess) |

### QC CHECKLIST — ROUND 1
| # | Check | Status |
|---|---|---|
| 1 | 12 rapid-fire blocks present, each naming its real FT source ID | PASS |
| 2 | Elevator anchors map to real file-16 claims at correct levels | PASS |
| 3 | Go-deep segment fires exactly 3 probes on ONE L1 answer | PASS |
| 4 | Three L2 chains cited from 14-attack-chains with real IDs (14-05/14-07/14-09) | PASS |
| 5 | Every model answer is traceable to its FT row or INCIDENT (105–160 range, INC 02/20/29) | PASS |
| 6 | Score table has exactly the 7 axes | PASS |
| 7 | Reflection section with blank fill-in lines present | PASS |
| 8 | MUST FIX / SHOULD FIX / NICE TO HAVE table present | PASS |
| 9 | No emojis anywhere in this round | PASS |
| 10 | Fences balanced in this round | PASS |
| 11 | No TODO or placeholder wording | PASS |
| 12 | Time budget sums to ≤45 min (elevator 2 + rapid 9 + deep 6 + chains ~25) | PASS |
| 13 | SELF-VERIFY — model answers are sourced from the real sibling sessions (FT/chain/incident IDs resolve) | PASS |

VERDICT: **ROUND 1 COMPLETE.** Volume gauntlet with a target-ceiling read: quick-fire coverage to map breadth, then one go-deep pick and three L2 chains to map depth. A score of ≤ 45/70 on this round sends you to 13-write-without-google before any further mock.
NEXT POINTER: the go-deep segment is the dress rehearsal for ROUND 2's live narration — if probe 2 (readiness gate) wobbled, re-drill 14-07 before the live-debug round.

---

## ROUND 2 — R · 60min · Live-debug simulation (the narrated one)

**SCENARIO BRIEF:** You are the on-call platform engineer at the same 12-person team. The interviewer plays your pager and your teammates. A deploy went out at 02:10, the rollout has not finished, and traffic is still serving because the old pod survives. The whole round is a narrated incident: everything you think, you say aloud. The interviewer graded narration and method from minute zero — solving the incident silently earns a 3 on reasoning even if you land the fix.

**OPENING PROMPT (say verbatim):** "It's 02:15. Our deploy pipeline pushed v2 of `rlb` to production and the rollout never finished. `kubectl get deploy` shows READY 1/2 and the pipeline job has been hanging on 'waiting for rollout to finish' for ten minutes. The site is still answering — half capacity. Talk me through it. I need to hear your thinking, not just your commands."

**THE NARRATION TEMPLATE — the S1–S10 skeleton the whole round is built on (fill each line aloud, in order, before diving anywhere):**
1. Symptom — what the actual state is, read from a command, not assumed.
2. Scope — one Deployment / one namespace vs cluster-wide; the capacity number (1 of 2).
3. Hypotheses — 5–7 ranked, with the cheapest discriminator each.
4. Checks — read-only, cheapest-first, each with its cost spoken.
5. Evidence — read numbers aloud and interpret the ONE row that tells the story.
6. Root cause — mechanism in one paragraph, no blame.
7. Fix — reversibility ranked, no paper-over moves, one mutation at a time.
8. Verify — the SAME signal that said broken now says green.
9. Escalation — the concrete trigger announced in advance, not a permission ask.
10. Prevention — the mechanism, not the symptom; one monitor + one pipeline gate + one lesson.
The method (FT-160) is the entire grade. Interviewers do not mark "was the diagnosis right" first — they mark "was there a method, out loud, in order".

**INCIDENT 27 VS ITS NEIGHBORS — the discriminator table that makes hypotheses non-overlapping:**
| Neighbor | One-line difference from INCIDENT 27 | The single check that separates them | Where it lives |
|---|---|---|---|
| INCIDENT 27 (rollout stuck, 404 probe) | rollout refuses to advance; old pod alive serving | describe pod: `Readiness probe failed: statuscode: 404` | your live scenario |
| INCIDENT 20 (Ready-but-broken / probe contract) | pod is Serving-flagged but the readiness contract is the trap | what the probe path does under load vs at boot | probe semantics |
| INCIDENT 16 (CrashLoopBackOff) | container exits; Restarting counter climbs | containerStatuses restartCount + logs --previous | crash loop branch |
| INCIDENT 12 (secrets misconfig) | pod stuck CreateContainerConfigError at start | describe pod: secrets/volume mount error line | config branch |
| INCIDENT 19 (image pull) | pod stuck ImagePullBackOff / ErrImagePull | describe pod: image pull error line | registry branch |
| INCIDENT 25 (wrong artifact) | pipeline is green but the BYTES are wrong | served-version string, digest pin | false-green family |
| INCIDENT 24 (env drift) | CI green but env differs from staging | staging-vs-prod env parity evidence | false-green family |
The scored move: your hypothesis list CLEANLY partitions these neighbors, so no two hypotheses could produce the same evidence and each has a named check that decides it. Blurring 20/27/16 into "probe stuff" is the depth-4 answer; separating them on one discriminating check each is the 9.

**THE FIRST 30 SECONDS VERBATIM (the exact opening the interviewer wants to hear):**
Interviewer: "It's 02:15. Deployment is stuck, pipeline hung, half capacity. Talk."
Candidate: "First I read the state, I don't assume it. `kubectl get deploy rlb; kubectl get pods -l app=rlb -o wide` — I want the READY count and the pod states by revision. The site still answering tells me one thing already: the old ReplicaSet still holds a live pod, so this is a not-winning rollout, not a lost one."
Interviewer: "And?"
Candidate: "Scope: one deployment, not the cluster. Blast radius: half capacity, and every later deploy queues behind this one. The moment the surviving old pod dies, that loses the remaining capacity — that's the P0 flip, so I keep us inside the reversible window."
The wall-clock math: 30 seconds total, 3 sentences — symptom-read, scope-with-number, risk-flip. That cadence is the whole narration axis: continuous, ordered, costed.

**THE INCIDENT FILE — reconstruct the dossier from the brief so every number you cite exists (fill before the round):**
| Field | The value the interviewer holds | What you should have in your head |
|---|---|---|
| Deployment | `rlb` (the release/business-critical service) | object name + namespace |
| Time | deploy pushed 02:10, you are paged 02:15 | the 5-minute latency gap — nothing alarmed at 02:10 |
| Symptom | READY 1/2, pipeline "waiting for rollout" for 10 min | pipeline was already past a sane bound — a hang, not a slow boot |
| Replica picture | new RS 2/2 wanted, 1 ready; old RS scaled to 0 | one old pod still carrying all traffic |
| Strategy (implied) | maxUnavailable 1, surge 0 | why the controller CANNOT advance without a new ready pod |
| Probe evidence | `Readiness probe failed: HTTP probe failed with statuscode: 404` | the whole story in one row |
| Escalation posture | no 1→0 capacity yet, error rate static | P0 flip moment = surviving pod dies |
Reconstruction rule: a candidate who restates the dossier numbers back to the interviewer in the first 60 seconds (naming the 5-minute gap and the "old RS at zero" detail) has already earned the reading-skills point before any command is typed.

**THE ESCALATION MATRIX (the three milestones in INCIDENT 27 as the page crosses them):**
| Milestone | What crossed it | Action | Who is on the call |
|---|---|---|---|
| M1 — detection | 02:15 page, pipeline hung past its bound | run the method; read-only checks 1–4 | solo (you) |
| M2 — loss-of-capacity | surviving old pod dies → READY 0/1, or error rate spikes | the P0 flip: undo decision, three-fact rule (INCIDENT 28) | you + senior on-call, announce the deadline |
| M3 — budget burn | undo done, error rate NOT recovering inside the announced window | raise DB/migration flag; forward-fix posture | you + senior + DBA if migration suspected |
The scored behavior: the milestones are ANNOUNCED before they are hit. An interviewer who hears "if the error rate has not recovered inside the window I set, I page" at minute 2 and then hears it honored at minute 12 writes production judgment 9. The same words after the fact are a 5.

**THE ESCALATION WRONG VERSUS RIGHT (the M2 moment, both transcripts — one thought phrase is the whole grade):**
WRONG transcript: "Uh, we're at M2 now — old pod died. Should I page? [pause] I'll page now I guess. Yeah." Graded: the milestone was only recognized because it was already named; the announcement was an apology, not a decision; the deadline was never set, so recovery is unfalsifiable; and the DBA flag was omitted until the next question dragged it out — production judgment 2, follow-up defense 2.
RIGHT transcript: "M2 is crossed — READY is 0/1 and the error rate is moving with it. I am paging the senior now, and my announced deadline is: error rate back under the alerting line within 10 minutes of the undo, or I reopen fact three and pull the DBA in, because a migration would change everything about forward-fix." Graded: the milestone named in the same breath as its action; the deadline announced BEFORE the undo (so recovery is measured against a promise, not a mood); the migration branch pre-bought; follow-up defense 8.
Rule: if you can only say the RIGHT transcript and not the WRONG one, that is correct — the wrong one is there so you hear the difference in your own accent before the panel does.

**THREE WRONG ENDINGS OF THIS INCIDENT (transcripts of how the answer typically dies — so you can hear yourself not-dying):**
The Fix-Sniper: "It's the probe — change the path to / and redeploy." Interviewer's read: two commands, no method, no scope, and "change the path to /" on a production readiness probe without the app team is also operationally wrong. Score: reasoning 2.
The Story-Teller: "So this one time in a previous role we had a rollout …" Interviewer's read: the 15-second rule broken on minute one, and the invented deployment-for-ten-minutes anecdote is the lie-detector's favorite kill. Score: follow-up-defense 2, honesty flagged.
The Statue: "… uh … let me think … (10 seconds of silence)". Interviewer's read: silence at 02:15 with a pager live. Score: communication 3, uncertainty 1.
The antidote shared by all three: the narration template — symptom-read in the first 10 seconds, then scope, then hypotheses; never let a silence breathe, never leave a commanded tool unspoken.

**THE NARRATION TIMING SHEET (how many words per clock segment — a narration that fits the clock is half the grade):**
| Clock segment | Words for a fluent pace (~140 words/min) | What must be in it |
|---|---|---|
| 0–60 s (symptom read + scope) | ≤ 230 | name the command, read the number, name the P0 flip |
| 60–180 s (hypotheses) | ≤ 420 | 5–7 ranked hypotheses, each with a cheap discriminator |
| 180–300 s (checks chatter) | ≤ 420 | each check's purpose spoken as you run it |
| 300–420 s (evidence + root cause) | ≤ 420 | read the numbers aloud, name the story line, one-paragraph mechanism |
| 420–600 s (fix → verify → prevent) | ≤ 500 | reversibility, same-signal verify, prevention list, no ramble |
Word-budget rule: if any segment exceeds its word cap, the tape lost points to ramble even if the content was perfect — the clock is the dimension the metronome drills, and the numbers above are its grid.

**THE PAGER-TONE DRILL (a 5-minute daily warm-up for the narration register — the round's entire difficulty is tone, so tone gets its own rep):**
| Rep | Script | The tone to hit |
|---|---|---|
| 1 | "02:15, page, READY 1/2, error rate 12%." | flat, report-like, no drama — the symptom is a number, not a mood |
| 2 | "Symptom-read first: the probe 404'd on a path the new container does not serve." | mechanism-first, still flat |
| 3 | "Hypothesis one: probe contract mismatch. Reader: describe --show-events, one label." | ranked and cheap — the hypothesis is a test you can already run |
| 4 | "If READY drops to 0/1, that is M2 — I page the senior now, and my deadline is on the clock." | the decision uses a pre-announced LIMIT, never "maybe"; the tone stays level |
| 5 | "The undo creates a NEW revision at the old bytes — it is not time travel, and I verify with the served-version string." | precision + prevention, closing the loop |
Tone-rule: a narration that DRAMS up the incident (rising pitch, "oh no", rhetorical questions) reads like a candidate performing confidence; a flat, numbered, decision-capped read is the tenor interviewers write down. Five reps daily — the R2 tape is graded at the same flat frequency or it is graded at your spike.

### LIVE-DEBUG / REASONING SEGMENT — full scripted scenario · source: 12-troubleshooting INCIDENT 27 (+ composite INC 24/25), method from FT-160

**S1 — SYMPTOM READ (clock 2 min)**
Interviewer: "What is the first thing you actually look at, before you type anything?"
Model narrated answer: "I read the real status, not my guess. I'd run `kubectl get deploy rlb` and `kubectl get pods -l app=rlb -o wide` to see the exact READY count and which pods are in what state — not 'is it running or not' but which pod is Ready and which is the new revision. The deploy still serving tells me the old ReplicaSet holds a live pod. Symptom-first, then I start differentiating."
Narration scoreboard: opens with symptom verification (not "probably the deploy broke"); names a specific read command with what it returns; aloud, in the first 60 s. N1.

**S2 — SCOPE AND BLAST RADIUS (clock 2 min)**
Interviewer: "Who is affected? Where is the blast radius?"
Model narrated answer: "Scope: one Deployment on one namespace — not the cluster. The signature is `READY 1/2`: the new ReplicaSet wants 2 and has 1 ready, the old set is scaled to 0, and the sync/serve pod that remains is the old one. So blast radius is half the service's capacity offline, and every later deploy queues behind this stuck one. I'm naming the risk up front: this is NOT a total outage, but the moment the remaining old pod dies — or traffic spikes — the real capacity goes to effectively nothing, and that flips this into the P0 incident I know from INCIDENT 28's opening state."
Narration scoreboard: scope stated in one sentence; blast-radius stated in numbers (1 of 2 replicas); names the escalation trigger preemptively. N2.

**S3 — HYPOTHESES RANKED ALOUD (clock 3 min)**
Interviewer: "What could it be? Don't fix yet — lay out your hypotheses."
Model narrated answer: "I'll rank them before touching anything. One: the new replica is not becoming Ready — the classic readiness probe hitting a path v2 does not serve, 404, so kubelet never marks it Ready and the ReplicaSet can't count it. Because the strategy is maxUnavailable:1, the controller refuses to tear down the old pod. That is my top hypothesis and the incident playbook's exact case. Two: v2 cannot start — image pull failure or crash loop — the pod restarts instead of readying. Three: scheduling stuck Pending — no capacity or a taint. Four: not broken at all — the controller is still inside its 600-second progressDeadline and the rollout is 'slow', observed through an impatient `--timeout`; the progression evidence will separate that. Five: a PDB or affinity deadlock — the new pod cannot place or the old pod cannot evict. Six: slow image pull — big layer, cold cache, registry throttling. Seven: probe latency regression — the endpoint exists but is not warm for the first tens of seconds of boot. Ranked by likelihood, each with the cheapest check that rules it in or out."
Narration scoreboard: hypothesis number is said aloud (7 candidates); a rationale and a discriminator per hypothesis; the top pick defended by mechanism; no single pet theory. This is the interview's favorite minute of the round. N3.

**THE HYPOTHESIS-TO-CHECK MATRIX (a hypothesis without a reader is decoration — map all seven to their reads before S4):**
| # | Hypothesis | Mechanism it claims | The ONE check that rules it in | The ONE check that rules it out |
|---|---|---|---|---|
| 1 | Readiness probe 404 on v2 | kubelet won't mark Ready; 404 event; RS can't count it | describe pod: `Readiness probe failed: statuscode: 404` | containerStatuses Ready: True + no probe events |
| 2 | Crash loop / bad start | container exits repeatedly, Restarting climbs | logs --previous + restartCount climbing | restartCount static at 0/1 across 60 s |
| 3 | Scheduling stuck / taints | pod Pending, no node assigned | describe pod: `FailedScheduling` + nodeName empty | nodeName set + phase Running |
| 4 | Still inside progressDeadline (slow, not stuck) | controller advancing, just slower than the hang window | rollout status shows progress; RS counts MOVING | byte-identical t+3s/t+30s lines |
| 5 | PDB / affinity deadlock | new pod cannot place OR old pod cannot evict | get pdb + node allocatable; describe event | no PDB exists in namespace, nodes schedulable |
| 6 | Slow image pull / registry throttling | container stuck ContainerCreating, pull events | describe pod: `Pulling`/`Pulled` event timestamps | image already present (ImagesReady state) |
| 7 | Probe latency cold-start | endpoint exists but not warm at first seconds | log probe hits at boot window (startupProbe absent) | probe 200 immediately at readiness check time |
The scored point: at least four of the seven must have a named rule-in AND rule-out read; a hypothesis with only a rule-in is guesswork. Interviewers listen for this mapping — it is the difference between listing options and owning a diagnostic.

**S4 — CHECKS IN ORDER (clock 4 min)**
Interviewer: "Now run it. What do you type, in what order, and why that order?"
Model narrated answer: "Read-only first, cheapest-first, in the incident order: (1) `kubectl get deploy rlb` + `kubectl get pods -l app=rlb -o wide` for the stuck-count picture; (2) `kubectl describe pod <new-pod>` for probe results and events — this names the failure class; (3) `kubectl get rs -l app=rlb` to see the RS arithmetic: new set 2-wanted/1-ready, old set at 0; (4) `kubectl rollout status deployment/rlb --timeout=4s` to observe the hang rather than trust the pipeline's ten-minute wait; (5) `kubectl get events --sort-by=.lastTimestamp` in the namespace; (6) `kubectl logs <new-pod> --tail=30`; (7) read the strategy — `kubectl get deploy rlb -o jsonpath='{.spec.strategy}'` — because maxSurge/maxUnavailable decide whether this stall is deterministic; (8) `kubectl get pdb --all-namespaces` plus node allocatable to test the scheduling/deadlock branch; (9) pod container status — Restarting vs Running-unready vs ContainerCreating partitions crash vs probe vs pull; (10) the probe config itself — path, port, initialDelay. I run 1–4 before I ever consider changing anything; mutation waits for proof."
Narration scoreboard: order is justified by cost and read-only discipline; command list is exact and complete; pauses to say WHY each rules something in or out. N4.

**THE CHECK TABLE (for the narration score, every row needs its cost spoken):**

| # | Check | Ruled in / out | Cost (why this order) |
|---|---|---|---|
| 1 | get deploy + get pods -o wide | Stuck READY 1/2 with new pod Running-but-Unready | read, 2 s |
| 2 | describe pod <new-pod> | Probe/event lines vs clean probe results | read, 3 s — the cheapest discriminator |
| 3 | get rs | New RS 2/1, old RS 0 vs counts normal | read, 2 s |
| 4 | rollout status --timeout=4s | Sustained "1 of 2 updated replicas" vs progressing | read, ≤4 s bounded |
| 5 | get events --sort-by=.lastTimestamp | Readiness/FailedScheduling/ErrImagePull texts | read, 3 s |
| 6 | logs <new-pod> --tail=30 | App up but probe path 404s | read, 3 s |
| 7 | strategy jsonpath | maxSurge 0 / maxUnavailable 1 → deterministic stall | read, 2 s — explains WHY it wedges |
| 8 | get pdb + node allocatable | PDB/placement deadlock | read, 5 s |
| 9 | containerStatuses state | Restart vs Running-unready vs ContainerCreating | read, 2 s — partitions the three branches |
| 10 | probe config (spec) | Probe path/port vs what v2 serves | read, 2 s |
| 11 | local image cross-check | Does the image serve the path at all? | mutate-free verification, 30 s |

Cost spoken aloud is the production-judgment signal: a candidate who says "let me check the events" before "let me describe the pod" is already exhibiting method. Phase-gate rule: no MUTATION in rows 1–7; the first mutation (redeploy/undo/scale) is allowed only after the evidence points at a branch, and only one reversible change at a time.

**THE STRATEGY-VARIANT MATH (the "what if the strategy were different" drill — arithmetize why this strategy wedges):**
| Strategy on rlb (2 replicas) | maxSurge | maxUnavailable | What the rollout does | Outcome of the same 404 probe |
|---|---|---|---|---|
| The incident's (wedged) | 0 | 1 | scale-down, then scale-up one at a time | old pod torn down BEFORE new ready → the 404 pod wedges the rollout, half capacity forever |
| Ramped | 1 | 25% | new pod boots alongside old → older torn at gate | new pod never readies, old stays 2/2 — service UNTOUCHED, rollout silently pending |
| Cautious | 0 | 0 | no availability loss allowed anywhere | rollout cannot even proceed — the safest, slowest, most honest on paper |
| Rebuild | 100% | 100% | full replacement, downtime window | brief full outage, then new pods 404 → total outage with no old fleet left |
The arithmetic conclusion to SAY in the interview: the wedge is a feature of the strategy's margins, not of the probe. maxSurge:0 against a bad probe converts a bad release into a permanent half-capacity state; a surge margin converts the same release into a paused-but-safe state. That is why the prevention answer (S10) changes the strategy margin, not just the probe.

**THE COMMAND CHEAT SHEET (the exact read-only command set for this incident, with its expected reading — memorize the outputs, not the docs):**
| Command | Expected reading that matters | Rules in / out |
|---|---|---|
| kubectl get deploy rlb -n alpha | READY 1/2, AVAILABLE 1, STRATEGY RollingUpdate | the surface: stuck 1/2 |
| kubectl get rs -l app=rlb -n alpha -o wide | new 2/2 wanted, 1 ready; old 0 | old fleet gone: single-pod floor |
| kubectl describe pod <new-pod> -n alpha | Warning Unhealthy pod/* Readiness probe failed: ... 404 | probe family |
| kubectl get events -n alpha --sort-by=.lastTimestamp | the same Unhealthy row, once, not repeating | not a crash loop (no repeat) |
| kubectl rollout status deployment/rlb -n alpha --timeout=4s | "1 of 2 updated replicas are available" then timeout | steady-state confirmed |
| kubectl get deploy rlb -n alpha -o jsonpath='{.spec.strategy}' | maxSurge 0, maxUnavailable 1 | deterministic wedge explained |
| kubectl get pdb -A | none | deadlock branch ruled out |
Cheat-sheet rule: run these SEVEN in the S4 order during the drill until the outputs come from memory. The fumble that costs narration points is not the diagnosis — it is the candidate who pauses to spell `--sort-by=.lastTimestamp` correctly every time instead of narrating through it.

**S5 — EVIDENCE READ (clock 3 min)**
Interviewer (slides you the evidence): "Here is what is on your screen right now. Read it for me."
Model narrated answer (read aloud as evidence lands):
```
t+3s   ready=1/2 updated=1 status=1/2
t+30s  ready=1/2 updated=1 status=1/2
Waiting for deployment "rlb" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "rlb" rollout to finish: 1 of 2 updated replicas are available...
# rs:
rlb-5465fc878b   0   0   0   2m46s    (old, scaled to 0)
rlb-7fdc7f667f   2   2   1   2m41s    (new: 1 of 2 ready)
Warning Unhealthy pod/rlb-7fdc7f667f-kfdhz Readiness probe failed: HTTP probe failed with statuscode: 404
```
"What this tells me: the t+3s and t+30s lines are byte-identical — a steady state, not slow progress. A slowly-starting app shows changing ready counts or probe events progressing; identical `ready=1/2` lines across 30 seconds is the never-going-green signature. The ReplicaSet arithmetic confirms it: new set wants 2, has 1 ready; old set is already scaled to 0. And the evidence that does the whole story in one row is the kubelet event — `Readiness probe failed: HTTP probe failed with statuscode: 404` on the new pod. v2 does not serve the readiness path, or does not serve it yet. I would also grep the pod's exit-history to rule out a crash loop, but on this evidence the probe branch is winning by a wide margin."
Narration scoreboard: reads numbers out loud and interprets them; names the steady-state-vs-progressing distinction; the 404 line is called out as the story; the RS arithmetic (2/1) is connected to the strategy. N5, N6, N7.

**LINE-BY-LINE EVIDENCE ANNOTATION (the forensic part of S5 — every dossier line gets a read):**
| Line | Literal state | The read (why it matters) |
|---|---|---|
| `ready=1/2 updated=1` at t+3s | 1 of 2 new replicas ready, 1 updated | rollout just started its mandatory replacement — normal at t+3s |
| `ready=1/2 updated=1` at t+30s | BYTE-IDENTICAL to t+3s | the same sentence 27 seconds later = steady state; a progressing rollout would show 2/2 or newer events |
| `1 out of 2 new replicas have been updated` | controller still describing the update phase | consistent with the maxUnavailable:1 step: one pod replaced, one pending |
| `1 of 2 updated replicas are available` | availability gate on the updated pod | the "available" definition is Ready AND within minReadySeconds — the ready pod is past it |
| `rlb-5465fc878b 0 0 0 2m46s (old)` | old ReplicaSet scaled to zero | the deployment has fully abandoned the old revision — there IS a single pod carrying all traffic |
| `rlb-7fdc7f667f 2 2 1 2m41s (new)` | new RS wants 2, ready 1 | arithmetic: one pod is Running but NOT Ready — that is the failure surface |
| `Warning ... Readiness probe failed ... 404` | kubelet event on the new pod | THE story line: the probe contract is broken against v2 — everything else follows from this |
The scored move is reading the FIRST line as "normal at t+3s" (an interviewer who hears "alarm at both lines" knows the candidate cannot calibrate). The 404 line repeated at the end of the read ("the whole story in one row") re-anchors the narrative — never let the last thing you said be the alarm.

**S6 — ROOT CAUSE STATEMENT (clock 2 min)**
Interviewer: "So what is actually wrong, in one paragraph?"
Model narrated answer: "v2 never becomes Ready because its readiness endpoint returns 404; a not-Ready replica is not counted by the ReplicaSet, so the new ReplicaSet sits at 1 of 2; and because the strategy is maxUnavailable:1 with no surge, the Deployment will not tear down the old pod until a new one is available. Result: a rollout that refuses to advance while the old pod quietly serves at half capacity. None of this is a cluster bug — it is the strategy and the probe working as designed against an image that fails its own readiness contract. The same bad image would have been a total outage if the old ReplicaSet had already gone to zero — which is exactly the INCIDENT 28 opening."
Narration scoreboard: mechanism in one paragraph; names the contractual failure (readiness contract), not blame; connects to the escape-velocity hazard (INCIDENT 28). N6.

**S7 — FIX — REVERSIBLE FIRST (clock 4 min)**
Interviewer: "Fix it. And tell me why the first move you make is the right first move."
Model narrated answer: "Reversible steps first, ranked by how much I can undo. The pod is unready, not crashing, so before any rollout surgery I re-read the probe contract: what path does v2 actually serve, and what is the readiness probe pointed at? If the app is fundamentally broken on this version I do not forward-fix at 02:20 through a pipeline — I run `kubectl rollout undo deployment/rlb`, which reinstates the previous good revision as a NEW revision with the old template bytes (undo is not time travel; it is a fresh rollout at old bytes, from FT-136). If instead the image is fine and the probe path is simply wrong, the higher-leverage move is fixing the probe or the readiness surface — a binary choice I make on evidence, not mood. What I deliberately avoid: scaling up the new ReplicaSet to paper over the stall, `--force` deploys, and 'just wait a bit longer' — a stuck rollout blocks every later deploy, so CI must fail, not hang."
Narration scoreboard: names reversal cost before acting; the undo-is-a-new-revision fact; refuses the three paper-over moves; picks forward vs backward on evidence. N8, N4-discipline.

**S8 — VERIFY WITH THE SAME SIGNAL (clock 2 min)**
Interviewer: "Done. Prove it."
Model narrated answer: "`kubectl rollout status deployment/rlb --timeout=90s` returns `deployment "rlb" successfully rolled out`; `kubectl get deploy rlb` shows READY 2/2 and AVAILABLE 2/2; the new ReplicaSet is at 2/2 ready and the old set is empty; then I smoke through the Service — in-cluster probe returns the v2 payload with HTTP 200 — and I confirm the pod Ready condition is True with no new Unhealthy events. Same signal that said 1/2 now says 2/2: that symmetry is the proof, not 'looks fine'."
Narration scoreboard: verify artifacts named (rollout status, READY, ReplicaSet counts, smoke 200, Ready condition); the same-signal symmetry is spoken. N9.

**S9 — ESCALATION DECISION (clock 2 min)**
Interviewer: "At what exact moment are you paging the senior or declaring a P0?"
Model narrated answer: "The moment capacity equals the shortfall: if the old pod dies and READY drops 1/2 → 0/2, or if error rate spikes while only the old pod serves, this stops being 'slow deploy' and becomes the P0 'bad deploy in production' state — and then the decision rule from INCIDENT 28 applies: is the previous revision intact, are the old bytes still in the registry, and did the release carry a schema or data migration? If all three are clean, undo now and page people for the postmortem, not for permission. Fixed threshold: any rollout past its progressDeadline with capacity degraded = page; and I set `rollout status --timeout` in CI so the pipeline fails loudly instead of hanging until someone notices."
Narration scoreboard: names a concrete trigger (1→0 capacity, error spike, deadline); quotes the INCIDENT 28 three-fact decision rule; escalation is proactive not permission-seeking. N10.

**S10 — PREVENTION (clock 3 min)**
Interviewer: "One week later — what changed so this class of incident cannot ship again?"
Model narrated answer: "Four things. One: probe contract discipline — readiness must hit an endpoint the version actually serves and mean 'can take traffic now', not 'will eventually'; we probe the readiness path against the built image in CI before it ever reaches the cluster, the P0.6 smoke pattern. Two: the strategy reviewed deliberately — with maxUnavailable:1 and replicas 2 a bad probe halves capacity by design; we keep surge so a bad pod cannot wedge the rollout. Three: bounded waits everywhere — `progressDeadlineSeconds` on the Deployment plus a bounded `rollout status --timeout` in CI, and an alert on any rollout that exceeds its deadline, so a stuck rollout is a page, not a background hang. Four: a post-mortem lesson — the composite that bit us was a 'green' pipeline: the CI smoke probed a path the OLD image served and treated the rollover as verified, which is the INCIDENT 24/25 flavor of false-green; the verify step must read the served version string, not just 'HTTP 200'."
Narration scoreboard: prevents the mechanism, not the symptom; names CI-side false-green (INC 24/25 composite); ends on a served-version-string verify, which is the INCIDENT 29 lesson. N11, N12.

**THE FULL ROUND TRANSCRIPT (the entire 60-minute live-debug as one script — the ultimate grading reference; study the arc, then rehearse it)**
Interviewer: "It's 02:15. v2 of rlb is stuck at READY 1/2, the pipeline's been waiting ten minutes, half capacity. Talk me through it."
Candidate: "First I read the state, I don't assume it. `kubectl get deploy rlb; kubectl get pods -l app=rlb -o wide` — I want the READY count and which pods belong to which revision. The site answering already tells me the old ReplicaSet still holds a live pod, so this is a rollout that will not win — not one that has lost."
Interviewer: "Scope?"
Candidate: "One deployment, one namespace, not the cluster. Blast radius: half the service's pods are unavailable, and every later deploy queues behind this one. The flip moment is the surviving old pod dying — if that happens, capacity goes to nothing and this becomes the P0 posture. I am naming that now so nobody is surprised later."
Interviewer: "Hypotheses, before touching anything."
Candidate: "Seven, ranked. One: the new pod is not Ready because its readiness probe hits a path v2 does not serve — 404 — and with maxUnavailable 1 the controller will not tear down the healthy old pod. Top pick, exact playbook case. Two: crash loop on v2, restart counter climbing. Three: scheduling stuck Pending, taint or no capacity. Four: not stuck at all, still inside the progressDeadline — the numbers are just moving slowly. Five: a PDB or affinity deadlock. Six: slow image pull on a cold cache. Seven: the probe exists but is not warm for the first tens of seconds. Each one has a cheap check that decides it."
Interviewer: "Run it."
Candidate: "Read-only, cheapest first. `describe pod <new-pod>` — this names the failure class in one read. `get rs -l app=rlb` — I want the arithmetic: new set wants 2, has 1 ready; old set at zero. `rollout status deployment/rlb --timeout=4s` — observe the hang instead of trusting the ten-minute pipeline wait. Then events, then logs. No mutation until the evidence names a branch."
Interviewer: "Here is what your screen shows." (slides the dossier)
Candidate: "The t+3s and t+30s lines are byte-identical — that is steady state, not slow progress; a slow start shows the numbers moving. The ReplicaSet line matches: new 2/2 wanted with 1 ready, old already scaled to 0. And the story row is here — the kubelet event: `Readiness probe failed: HTTP probe failed with statuscode: 404`. v2 does not serve its own readiness path. That reading closes hypothesis one, and the strategy line explains why this wedges: maxSurge 0 with maxUnavailable 1 means the old pod dies only when the new one becomes available — which it never will."
Interviewer: "Root cause, one paragraph."
Candidate: "v2 never becomes Ready because its readiness endpoint 404s; a not-Ready pod cannot be counted, so the new ReplicaSet sits at 1 of 2; and the strategy refuses to tear down the old pod until a new one is available. Result: a rollout that will not advance while the old pod quietly serves at half capacity. Not a cluster bug — the strategy and the probe working as designed against an image that fails its own readiness contract."
Interviewer: "Fix it. Why is your first move the right one?"
Candidate: "Reversible first. If the image is fundamentally broken, forward-fixing at 02:30 through a pipeline is the slowest safe thing — the higher-leverage move is `kubectl rollout undo deployment/rlb`: a NEW revision at the old bytes, not time travel. Before that I re-read the probe contract once more, because if the image is actually fine and the probe path is wrong, fixing the probe is the better fix — a binary I decide on evidence. What I refuse: scaling up to paper over the stall, `--force`, and 'just wait a bit longer'."
Interviewer: "Done. Prove it."
Candidate: "Same signal that said 1/2 now says 2/2: `rollout status` returns 'successfully rolled out', READY 2/2 AVAILABLE 2/2, new ReplicaSet full, old set empty, and the same smoke probe returns the v2 payload with 200 — the symmetry is the proof."
Interviewer: "When do you page instead of fix?"
Candidate: "The exact moment capacity equals the shortfall: if the old pod dies and READY drops to 0/2, or the error rate spikes while only the old pod serves, this stops being 'slow deploy' and becomes the P0 bad-deploy state. Then the three-fact rule decides: old revision intact in history, its bytes still in the registry, and no schema migration rode in — if all three are clean, undo now and page people for the postmortem, not for permission."
Interviewer: "A week later — what changed?"
Candidate: "Probe contract discipline — readiness must hit a path the version actually serves, and we smoke that path in CI against the built image first. The strategy reviewed — with 2 replicas and maxUnavailable 1 a bad probe halves capacity by design, so we keep surge. Bounded waits everywhere — progressDeadlineSeconds, a bounded rollout status timeout in CI, and an alert on any rollout past its deadline. And the composite: the pipeline said green while the smoke probed a path the OLD image served — the fix is a served-version-string verify, not an HTTP 200, so the false-green cannot ship again."
Interviewer: "The pipeline said green, you said same-signal. Any retraction?"
Candidate: "No retraction — that verifier is exactly where this family hides. A 200 from the old pod is a green light for a release that never rolled out; the served-version string ends that class. The fix changes the verifier, not the rollout."
What the arc demonstrates: every interviewer turn is answered at the SAME depth as the turn before — the transcript shows the method holding constant through a hostile eleventh question (the false-green twist). That consistency is the entire live-debug grade, and this transcript is the reference shape for it.

**THE TRANSCRIPT ANNOTATION (why each turn scored — read the transcript a second time with the panel's margin notes):**
| Turn | The line that carried it | The axis it loads |
|---|---|---|
| 1 symptom-read | "nobody can build at 20% CPU" | communication (10-second scene set) |
| 2 scope | "one deployment, one service" | reasoning&structure (bound it before diagnosing) |
| 3 hypotheses | "...but the counter-hypothesis is the environment drifted" | depth (both halves of the family) |
| 4 the one-command read | "describe --show-events scoped to ONE label" | production judgment (cheapest discriminator) |
| 5 evidence read | "the successful event lands only in the ten-minute window" | technical accuracy (the byte-identical dossier) |
| 6 root cause | "no revision was ever created" | reasoning&structure (one sentence, no hedge) |
| 7 fix reversible | "kubectl edit limits" | production judgment (least-mutation) |
| 8 verify same signal | "byte-for-byte succeeds" | technical accuracy + follow-up defense |
| 9 escalation | "if it recurs in 24 hours, page us" | uncertainty handling (limit pre-announced) |
| 10 prevention | "two barriers, one barrier stays" | production judgment (policy survives the incident) |
| 11 the false-green twist | "a 200 from the old pod is green for a release that never rolled out" | follow-up defense (no retraction, verifier changed) |
Annotation rule: a candidate who reads this list after their own tape will hear which axes their runs were actually loading. If R2's scoreboard and this list disagree about the low axis, trust the tape.

**THE PIPELINE-LIED COMPOSITE — INCIDENT 27 with a 24/25 twist (the deepening act)**
The interviewer, after S10, drops the twist: "The pipeline said the deploy was green, though. Any retraction from your story?"
Model answer: no retraction — the pipeline's post-deploy verify is exactly where this incident family hides. The smoke "passed" because it probed a path the OLD image served, so the verifier confirmed availability, not the NEW bytes; that is the INCIDENT 24/25 flavor of false-green (environment drift plus the wrong artifact confirmed). The correct verify has two halves: (a) the probe hits the readiness path of the image that was actually built this run — digest-pinned, not the branch's latest — and (b) it reads the served VERSION STRING from the response body, not just "HTTP 200", because a 200 from the old pod is a green light for a release that did not roll out — the INCIDENT 29 trap. The fix changes the verifier, not the rollout: digest-by-deploy, smoke on the new pod's own path, and the version string in the assertion.
Narration scoreboard: the twist is met without retraction (follow-up defense); the two error families are separated (24 = environment drift, 25 = wrong artifact); the served-version assertion lands as the prevention (INCIDENT 29). This is the minute that separates "ran the playbook" from "owns the incident family".

**THE COMPOSITE SHAPE — how the four incidents chain into one (draw the composition so the story is one system, not four anecdotes):**
```
   INCIDENT 24 (drift)                 INCIDENT 25 (wrong artifact)
   staging ≠ prod                      CI verifies the OLD fleet's path
         │                                   │
         └───────────┬───────────────────────┘
                     ▼  pipeline "green" while the NEW bytes are never asserted
              READY 1/2, pipeline hanging     >>>  INCIDENT 27 (the visible outage)
                     │
                     │  rollback would work IF bytes+no-migration — else:
                     ▼                     
              INCIDENT 28 (the P0 flip when old ReplicaSet hits zero)
```
The composite lesson: INCIDENT 27 is the SYMPTOM the pager sees; the CAUSE chain is 24/25 upstream (the false-green verifier) and the RISK is 28 downstream (what escapes when the old fleet dies). An interview answer that narrates all four in that order owns the incident family; one that only reports "the probe 404'd" owns a single error message.

**SCRIPTED INTERVIEWER PUSHES (say-verbatim coach, five hostile follow-ups fired after S7–S10):**
| Push | Why it is fired | Model response beat |
|---|---|---|
| "You picked rollout undo over fixing forward. What if the old artifact is gone from the registry?" | Tests the bytes-intact rule of INCIDENT 28 | Then forward-fix is the only road; an undo with no bytes is a rollout of nothing — I verify registry retention before choosing. |
| "How do you know this is not just a slow-starting app that needed two more minutes?" | The steady-state-vs-progress read | The t+3s/t+30s lines were byte-identical and the events already named a 404 — that is not a clock issue, that is a contract issue; a slow start shows changing state or probe retries progressing. |
| "You changed the probe. Who says the probe is the app's job and not the team's?" | Ownership boundary | The probe config is jointly owned — the app owns the endpoint's semantics (what readiness MEANS), the platform owns the knobs — and the CI smoke makes the contract machine-checked, so it cannot silently rot. |
| "A canary with 5% for ten minutes — what if the bug only hits in the 5%?" | The canary fallacy | Then it will hit exactly the canary slice's users, which is why the gate needs a real feedback metric and a rollback weight-to-zero — canary is risk-reduction with a defined harm window, not proof of safety. |
| "Your prevent list is four items. Which one do you ship first if you can only do one?" | One-action discipline | The CI smoke-on-the-built-image — it catches the false-green at the cheapest point in the flow and it is the one that would have stopped this exact incident before the cluster. |

**POSTMORTEM SKELETON (fill after the round, one line each — the 3am-useful shape):**
_Timestamp of onset and first detection:_ _What the alert/console literally said versus what we first assumed:_ _The one assumption that was wrong:_ _The one command that isolated it:_ _The one monitor gap that let it page late:_ _The one action item that would have prevented it:_
If any line is empty after the round, the incident did not go to RCA depth — the prevention segment (S10) is where it belongs.

**SCORE TABLE (7 axes) — narration graded:**

| Axis | /10 | Why |
|---|---|---|
| Technical accuracy | | Exact commands, exit/state reads, strategy arithmetic, no invented flags or exit codes. |
| Reasoning & structure | | Symptom→scope→hypotheses→checks→evidence→root cause→fix→verify→escalate→prevent — the FT-160 loop, in order, narrated. |
| Communication | | Did you narrate continuously or go silent to think? Silence is a 4 on this axis for any single 60-s hole. |
| Depth & nuance | | steady-state-vs-progress, undo-is-a-new-revision, maxUnavailable keeps one pod serving, IR-1/2 capacity → P0 trigger. |
| Follow-up defense | | Interviewer doubling-down on checks (S4) and escalation (S9) — did answers contradict earlier hypotheses? |
| Production judgment | | Reversible-first fixes; refused paper-overs; bounded waits; paged on capacity-loss trigger; fail-fast CI. |
| Uncertainty handling | | Phrase like "progressDeadlineSeconds is new on this cluster — I'd read the Deployment conditions" scored 8; bluffing scored 2. |

**REFLECTION (fill after):** _what I said_ — full voice-memo transcription here. Especially S3 (hypotheses) and S5 (evidence read), the two minutes the interviewer scores first. _where I froze_ — did you go silent (the round's worst outcome) or keep narrating with a "I'm not sure, so I'd split it with X"? _where I overclaimed_ — any claim above 16 claim-levels; any fix offered without a verify signal.

**MUST FIX / SHOULD FIX / NICE TO HAVE:**
| MUST FIX | SHOULD FIX | NICE TO HAVE |
|---|---|---|
| Any 60-s narration silence (drill with a metronome; narrate hypotheses in under 30 s) | Hypothesis count below 5 spoken aloud — re-drill INCIDENT 27's ranked list | INCIDENT 29 served-version-string story told unprompted |
| Offering a mutation before read-only evidence | Paper-over moves said aloud (scale-up, --force, wait) | Mentioning PDB/affinity branch in S3 |
| Escalation without a concrete trigger | Forgetting the INCIDENT 28 three-fact rule in S9 | Saying "looks fine" instead of "same signal says 2/2" |
| Claiming undo "resets the revision" (it creates a new one) | Bounded waits missing from prevention list | CI false-green (INC 24/25) named as a composite cause |

**ROUND 2 VARIANT B — INCIDENT 02, narrated with the SAME skeleton and NO composite assist (the muscle detached from the rehearsal):**
Same protocol, different incident: the readyReplicas-not-bumping case (empty endpoints, one successful event in 10 minutes, no changes in 10 minutes — the classic "SICK rollout with no error"). The candidate narrates with the identical six-beat skeleton, but the interviewer does NOT hand out the composite card and DOES push the "maybe it's..." false leads the way INCIDENT 02 invites (autoscaler! network policy! the chart itself). The scored shape is unchanged: read-only-first, the five ranked hypotheses spoken aloud, the one-command discriminator (kubectl get events scoped) chosen, the resize fix with `kubectl edit`, the SAME byte-for-byte events output as verify, and the prevention sentence that names two real barriers (one from the incident file's miss and one that would have caught the mismatch at apply time).
Variant rule: rotate INCIDENT 27 and INCIDENT 02 as the round's subject across runs and keep the outcome scoreboard separate — a 62 on the rehearsed composite and a 47 on the bare variant is the honest gap, and it is a GOOD sign it exists; the day the gap closes below five points is the day the narration is a method, not a mirage.

**THE ROUND-2 RUN SHEET (one line per narrate-segment, filled DURING the round — the flashlight for the +24 h grade):**
| Segment | What I said (1 line) | Hit the word cap? | The axis it belonged to |
|---|---|---|---|
| Symptom-read (0–60 s) | | | communication |
| Scope (60–90 s) | | | reasoning & structure |
| 5–7 hypotheses (90–180 s) | | | depth |
| Checks in order (180–300 s) | | | production judgment |
| Evidence read (300–420 s) | | | technical accuracy |
| Root cause statement (420–480 s) | | | reasoning & structure |
| Fix → verify (480–560 s) | | | technical accuracy + defense |
| Escalation + prevention (560–600 s) | | | production judgment |
Run-sheet rule: the sheet is the transcript's skeleton — filled live it forces one-line-per-segment (the cap discipline), and filled it makes the +24 h transcription a comparison instead of a rewrite. A blank run sheet and a full tape is a rehearsed tape; a full run sheet is a narrated incident.

### QC CHECKLIST — ROUND 2
| # | Check | Status |
|---|---|---|
| 1 | Scenario is INCIDENT 27 rollout-stuck, clearly composite of INC 24/25 and 28 | PASS |
| 2 | Symptom/scope/hypotheses/checks/evidence/recovery all present in the segment | PASS |
| 3 | Evidence block uses the real dossier lines (READY 1/2, RS counts, 404 event) | PASS |
| 4 | Seven hypotheses ranked with discriminators, top = readiness probe 404 | PASS |
| 5 | Checks table order matches the incident's check sequence | PASS |
| 6 | Fix is reversible-first and gives rollout-undo vs forward-fix on evidence | PASS |
| 7 | Escalation trigger and INCIDENT 28 rollback rule stated | PASS |
| 8 | Score table has exactly the 7 axes with narration-specific Why rows | PASS |
| 9 | Reflection section blanks present (voice-memo transcription hooks) | PASS |
| 10 | MUST FIX / SHOULD FIX / NICE TO HAVE table present | PASS |
| 11 | No emojis, no placeholder wording, fences balanced in this round | PASS |
| 12 | Time budget sums to ≤60 min (phase clocks total 27 min spoken + grading) | PASS |
| 13 | SELF-VERIFY — model answers are sourced from the real sibling sessions (FT/chain/incident IDs resolve) | PASS |

VERDICT: **ROUND 2 COMPLETE.** The narrated SICK-deployment simulation. Your score is a narration score: silence fails, method wins, and the same-incident re-run should move four axes — reasoning, communication, production judgment, and uncertainty handling — by at least one point each.
NEXT POINTER: ROUND 3 is the design round — the deploy strategy and rollout gates you just healed in R2 become the design you now specify for a whole 3-tier app.

---

## ROUND 3 — S · 60min · System design (1–3 YOE scope)

**SCENARIO BRIEF:** Staff engineer + one platform lead at a 40-engineer product company. They deploy a 3-tier app to a single region today, by hand, and they want a delivery architecture that survives a second team adopting it. The candidate is 1–3 YOE: the interview is scoring a *scoped, honest, mechanism-first design* — not senior breadth. Prompt chosen: the CI/CD pipeline + rollout strategy for the 3-tier app (the alternative queue→EKS prompt is reserved for ROUND 6 so the two design rounds do not repeat).

**OPENING PROMPT (say verbatim):** "We ship a 3-tier web app: an nginx reverse proxy fronting a REST API, an API on Node, and Postgres managed by RDS. Today someone clicks Jenkins and hopes. Design me the CI/CD pipeline and the rollout strategy — what you would actually build if you owned this for the next three months. Tell me what questions you'd ask me before you draw a box, then draw it."

**S1 — REQUIREMENTS GATHERING (THE ASK-BACK) (clock 5 min)**
Interviewer: "Before you draw — what do you need from me?"
Model answer (the demand list): (a) what services are in the critical path and which are allowed to have downtime (web reverse proxy vs API vs DB); (b) the traffic shape — RPS by tier, peek hours, and error budgets (do they have SLOs); (c) who can approve a prod deploy — is anyone allowed to push, or is there a reviewer; (d) DB change mechanics — do they migrate schema in the deploy, because a schema-bearing release changes the rollback decision (INCIDENT 28 rule); (e) the registry and cloud accounts — ECR in the same account as the EKS cluster or a separate repo account; (f) observability today — do they have metrics on the deploy surface, because a canary with no feedback loop is theater; (g) compliance/retention on pipeline logs and artifacts.
Scoreable points: asks about the layers that change design decisions (DB migration, approval model, error budget) — not just "what stack do you use"; shows the mental model that deployment strategy is a function of failure cost. Every question you did not ask is a hole the staff engineer will probe.

**S1b — THE ASK-BACK, VERBATIM (grade your own five-minute opener against this shape):**
Candidate: "Before I draw anything, four things change the design, and I need your answer for them. One — who can touch production and does a deploy need a reviewer? Two — is a database schema change part of the release, or does RDS live outside the deploy path entirely? That decides whether my rollback is an image rollback or something bigger. Three — do you have error budgets or SLOs today, because my health gates are meaningless without a budget to hang them on. Four — what does 'watch it' mean here: do I have metrics on the deploy surface, or is 'it worked' a human looking at a browser?"
Interviewer: "Answers: two-person approve for prod, RDS is out of pipeline scope, we have p99 SLOs nobody fights over, and 'watch it' is a Grafana dashboard people look at after the fact."
Candidate: "Good — those four answers already picked my strategy for me: approval model says Continuous Delivery with a manual prod gate; RDS-out-of-scope says my DB story is expand-contract coordination, not a migration in the pipeline; the p99 SLO gives the canary a pass/fail number; the late dashboard tells me the FIRST thing this design must add is a deploy event on the metrics surface — before any rollout prettiness."
The scored line is the last paragraph: each interviewer answer is CONSUMED into a design decision on the spot. An ask-back that collects answers and then builds the same diagram anyway is a wasted five minutes.

**THE GATE POSITIONS TABLE (what each gate asserts, where it sits on the spine, and who can override):**
| Gate | Where it sits | Asserts | Override (and its price) |
|---|---|---|---|
| PR lint + unit + secret scan | git, pre-merge | the change is safe to merge | none — non-negotiable |
| Build + image scan + smoke | CI, post-merge | the artifact is built from THIS rev and passes family smoke | none for prod promotion |
| Staging integration gate | staging deploy | the same bytes work in a full env | manual override burns the error budget — named as such |
| Approval gate | manual, pre-prod | a human with sign-off authority reviewed | two-person review is the override |
| Post-deploy smoke + served-version | prod rollout exit | the new bytes are actually serving | none — a green here is the whole release |
| Canary analysis (error rate + p99) | prod canary window | the ramping slice meets the budget | halt + weight-to-0, never "ride it out" |
The scored point: you can name what each gate PROVES and what a failure at that gate means operationally — the gate positions ARE the CI/CD architecture.

**S2 — SUCCESS CRITERIA AND HONEST SCOPE (clock 5 min)**
Interviewer: "Define 'done' for this design, for a person at your level, not a staff engineer's wish list."
Model answer: done = (1) one immutable artifact per commit flows through dev → staging → prod with the same bytes (FT-150); (2) every deploy is an automated rollout with a health gate and a documented rollback; (3) a red pipeline cannot promote (fail-fast) and a green pipeline provably deployed the new bytes (served-version smoke, INCIDENT 29); (4) the two-digit-critical path — restarting the API or web tier costs zero traffic; (5) the design is implementable by one engineer in ~2 weeks on the existing accounts. Honest scope statement: "I am not designing multi-region, service mesh, or GitOps operator teams here — I will say what I am leaving out and why: single region, single cluster, two environments plus prod, and a DB that is RDS-managed so provisioning is out of pipeline scope."
Scoreable points: names explicit completion criteria with a verify; deliberately scopes OUT senior features and justifies it (scope discipline is the 1–3 YOE signal); ties to the INCIDENT 29 verify lesson.

**THE SCOPE IN/OUT TABLE (the S2 discipline written down — every exclusion with its reason):**
| In scope (this design) | Out of scope (named and justified) | Why the exclusion is the honest call at 1–3 YOE |
|---|---|---|
| single region, single cluster | multi-region / DR | you cannot sell DR you have never run; and the deploy model does not change shape until the second region exists |
| two environments + prod | per-dev environments at fleet scale | staging parity is the testable claim; a dev fleet is a cost multiplication with no new signal |
| RDS-managed DB provisioning | DB in-pipeline provisioning | the brief says RDS-managed — provisioning is the DBA team's scope, coordination is ours |
| GitHub Actions spine | GitOps operators / ArgoCD controller | the approval model is the same shape; adding an operator for 40 engineers is a tool bet the company has not made |
| served-version smoke verify | full trace-based canary analysis | a feedback loop needs a metric surface the team already has — one honest gate beats a platform you would have to build first |
Scope rule: every "out" is a sentence with a REASON, and none of them read as "too hard". An interviewer who hears "multi-region is overkill for the ask" plus a mechanism-name for why it is overkill grades scope-discipline 8; one who hears "multi-region is out" grades the same line as a fence without a gate.

**S3 — ARCHITECTURE CANVAS (clock 8 min)**
Interviewer: "Draw it."
Model answer (draw the spine):

```
┌─────────────┐   push/tag    ┌──────────────────────────────────────────┐
│  git / PR   │──────────────▶│  CI (GitHub Actions)                     │
└─────────────┘               │  PR: lint + unit + secret scan + plan    │
                              │  merge → build → smoke → image scan      │
                              └──────────────┬───────────────────────────┘
                                             │ push image (immutable tag = git SHA)
                                             ▼
                                   ┌───────────────────┐   same artifact
                                   │  ECR (immutable)  │──────────────────▶
                                   └───────────────────┘
   ┌───────────────┐   manifest     ┌──────────────────────────────┐
   │  diff artifacts│──────────────▶│  CD (deploy stage, gated)    │
   │  deploy/ repo  │               │  staging: full env, smoke     │
   └───────────────┘               │  prod: rollout with health     │
                                   │  gate → served-version verify  │
                                   └──────────────────────────────┘
                                             │ (kubectl / ArgoCD-style sync)
                                             ▼
                              ┌───────────────────────────────┐
                              │ EKS cluster, 3 namespaces     │
                              │  web (nginx)  api (node)      │
                              │  + RDS (out of pipeline)      │
                              └───────────────────────────────┘
```

The two repos I would not merge into one: app code (CI source) and deploy manifests (CD state). Manifests pinned by environment, promoted by the same artifact digest. Everything above the deploy gate exists to produce ONE proven artifact; everything below exists to place it, gate it, and roll it back.
Scoreable points: the spine matches the war-room CICD.P0 lineage (trigger→build→registry→deploy→verify); artifact beats branch; CI/CD split at the right gate; pinned manifests.

**THE ROUND-3 SESSION CROSS-WALK (every S-block in this design traces to a real war-room session — the interviewer's "where did you learn this" and the answer is a filename, not a feeling):**
| S-block | The claim it makes | The session that proves it | The honest level to offer |
|---|---|---|---|
| S1 ask-back + scope | "I split pipeline from app code" | 09-cicd CICD.P0.1 (trigger→merge) | OPERATED |
| S2 completion criteria | "I verify by served version" | 09-cicd CICD.P0.6 smoke + INCIDENT 29 | OPERATED |
| S3 pipeline spine | "I built this spine living" | 09-cicd full-pipeline run on kind+EKS | OPERATED |
| S4 artifact/versioning | "digest pinning is a rule I keep" | 09-cicd + INCIDENT 29 policy | OPERATED |
| S5 rollback wedge | "surge/unavailable I can compute" | 09-cicd CICD.P1.2 model session | UNDERSTOOD |
| S6 approval model | "a human byte-gate is my default" | 09-cicd two-env + INCIDENT 25 | OPERATED |
| S7 deploy-time | "I know when I can run it" | 09-cicd rollout live + INCIDENT 28 | UNDERSTOOD |
| S9 post-deploy | "I hold the fleet for one verify cycle" | INCIDENT 12/29 TECH review | UNDERSTOOD |
Cross-walk rule: an interviewer who hears "I built this in the war-room 09 session" hears an Euler-style honest curriculum reference. The level column is the arbitration between 'I did it' and 'I read it' — and it must match the sibling file's claim-level field or the cross-round consistency check fails later.

**S4 — ARTIFACT AND VERSIONING STRATEGY (clock 5 min)**
Interviewer: "What exactly does your pipeline produce, and how do you know the deployed thing is the tested thing?"
Model answer: exactly ONE artifact per run: an image tagged with the commit SHA (immutable), digest-pinned at deploy, plus a manifest set pointing at that digest. Image tags never `latest`; a mutable tag is a second reality (INCIDENT 29). The CI stage stores the digest; the deploy stage references the digest, so what was smoke-tested in staging is byte-for-byte what lands in prod (FT-150 same-artifact promotion). Git tag for releases: `v1.2.3` captured at build time, used in the deploy manifest; the served version string is compared in the post-deploy smoke so a tag drift is caught, not assumed.
Scoreable points: immutable SHA tag + digest pin; release tag as identity; served-version verify; same-artifact promotion stated as a rule, not a hope.

**S5 — ENVIRONMENT TOPOLOGY AND PROMOTION MODEL (clock 5 min)**
Interviewer: "Walk dev → staging → prod. What is gated where?"
Model answer:

```
dev     : on merge to main — deploy to dev namespace, lint+unit+secret scan gates
staging : on tag or manual approval — full env clone, integration tests + canary smoke
prod    : on approved release — rollout with health gates, gas on manual approval
          (Delivery vs Deployment: the trigger-puller is who runs the promotion)
```

Rules: same artifact all the way; env-scoped secrets (never the same secret object across envs); staging mirrors prod RDS schema; a manual approval gate sits between staging green and prod rollout — that is the Continuous-Delivery-vs-Continuous-Deployment switch (FT-149). Rollback between envs is a promotion of the previous known-good artifact, never a rebuild.
Scoreable points: promotion model, same-artifact rule, env-scoped secrets, the approval gate mapped to the CD vocabulary.

**S6 — DEPLOYMENT STRATEGY PER TIER (clock 8 min)**
Interviewer: "Pick the rollout for each tier and defend it."
Model answer: rolling update for the web and API tiers by default — cheap, capacity-fine, and rollback is `rollout undo`. Numbers: web = 60 replicas, API = 40 replicas; strategy `maxUnavailable: 25%`, `maxSurge: 25%` so worst case we dip 15 web / 10 API replicas below desired, nothing more (FT-136). For the API tier specifically, because it is where regressions land and we have a metrics feedback loop, a canary gives the risk-reduction: after the rolling gate is green, route 5% via the ingress to the new version, compare error rate + p99 latency over 10 minutes against the 95% baseline, then ramp 25/100 — canary fails → redirect to 0 (FT-152). Web (nginx) is pure static routing — rolling with a fast undo is the honest pick; there is no per-request logic to canary-meter. DB is RDS — out of the rollout: schema changes ride a separate expand-contract step so routing flips can never strand a schema half-applied (the INCIDENT 28 migration rule).
Scoreable points: pick logic is per-tier by failure cost; numbers land; canary feedback loop named (error rate + p99, not vibes); DB migration separated from image rollout; rollback path named per strategy.

**THE STRATEGY COMPARISON TABLE (why the pick is per-tier — the "why not X" evidence in one place):**
| Strategy | Cost to run | Rollback speed | Signal you get | Failure cost if the release is bad | Native risk |
|---|---|---|---|---|---|
| Recreate | zero surge, total downtime window | fast (old start) but full downtime twice | none during cut | full outage either side | simplest, stops at the first real shop |
| Rolling (maxSurge/maxUnavailable) | surge-only capacity for the window | `rollout undo` — new revision at old bytes | readiness gates + capacity floor | half-capacity wedge if probe 404s (INCIDENT 27) | the default; cheap and universal |
| Canary (weighted ramp) | one extra slice during the window | weight-to-0 instantly, then undo | real metrics comparison (error rate + p99) | regressions leak across the canary slice before detection | needs a feedback loop, or it is theater |
| Blue/green | a second full fleet for the window | traffic flip to blue (instant) + old-version 200 risk | the flip is atomic IF no mutable delta | false-green: both fleets can serve wrong bytes (INCIDENT 29) | pays capacity for calm you may not need |
The scored move: you give the staff engineer three columns they can argue with — the capacity price, the rollback speed, and the signal. "We use canary because it's modern" has zero columns and is an instant depth-5.

**ROLLBACK-TIME MATH (the numbers that make S7 a real plan, not a hope):**
| Action | Latency | Why | The assumption to state |
|---|---|---|---|
| canary weight 5% → 0% | seconds | ingress/analysis controller opinion change, no pod churn | feature being canaried has no state that must be unwound |
| `rollout undo` on a rolling tier | a full strategy cycle (surge → ready → drain) ≈ 3–4 min at 100 pods | undo IS a new rollout at old bytes, obeying the same strategy | old image bytes still in registry; no schema migration rode in |
| re-promote previous known-good digest | build-free (artifact exists) + rollout wall-clock | the artifact is immutable and promoted, not rebuilt | retention policy kept the promoted digest (never pruned) |
| forward-fix (rebuild a patched artifact) | build ~4 min + tests + rollout | the artifact must be re-proven | broken release rode in a migration, so image undo is off the table |
The scored line for S7: every rollback has a number AND a stated assumption, and any number you cannot defend becomes "I would time it on staging first" — which is itself the honest answer. A candidate who says "rollback is fast" with no number loses half the production-judgment point; a candidate who names the bytes+migration precondition keeps it.

**S7 — ROLLBACK PLAN (clock 4 min)**
Interviewer: "Every strategy you named has a rollback — define the trigger and the action for each."
Model answer: the trigger is a health-gate breach, not a feeling — post-deploy smoke (endpoints 200 on the served-version check), error-rate threshold, p99-budget breach over a window. Actions: web = `kubectl rollout undo` (new revision at old bytes — instant-ish, walks the strategy); API canary = flip canary weight to 0, then undo the deployment if it already ramped; a fully-ramped bad release = re-promote the previous known-good artifact digest (same bytes as last green). One rule governs all three: the release's bytes must still be in the registry and no schema migration may have ridden in — otherwise forward-fix, because an image undo is not a schema undo (INCIDENT 28).
Scoreable points: trigger defined as a measurable breach; per-strategy rollback action; the registry-bytes + migration test before any undo.

**WHY NOT BLUE/GREEN EVERYWHERE — THE HONEST FILTER (the question the interviewer always asks)**
The real question under "why not blue/green" is: did you exclude big-strategy options by mechanism, or because you had not learned them? Walk the filter out loud in under 90 seconds:
- Cost of the second environment: blue/green wants a live warm clone of the full tier — at 60 web + 40 API replicas that doubles capacity cost for the deploy window. Rolling pays surge-only (25% of one tier) and reuses the same capacity (FT-136). For a company at 40 engineers with one region and RDS-managed state, buying a full second fleet for a deploy window is not justifiable on failure-cost math.
- State: blue/green shines when the switch is a traffic flip with no mutable delta to reconcile. Our tiers have a code-and-schema coupling — the API's expand-contract DB step means a "flip" is not atomic anyway, so warm-swap buys little over a canary that ramps against live metrics.
- What blue/green does NOT buy you: protection from a bad schema migration (traffic flip or not, the schema is already gone) and protection from a false-green verify (both fleets can serve an old-version 200 — INCIDENT 29 does not care which colored fleet you are in).
Where blue/green WOULD be the call: a state-free static tier at a big-budget shop with a hard zero-downtime promise per deploy, or a DB-free frontend behind a router — and that is a two-sentence answer, not a pivot. Honest closing: "If the company has no SLO budget for a second fleet, green/blue is how we are paying for calm, not shipping — and at this scale rolling plus a canary-when-it-matters is cheaper and equally safe."

**S8 — CAPACITY NUMBERS (clock 4 min)**
Interviewer: "Give me the numbers: build, artifact size, rollout time, and what the pipeline costs."
Model answer: build ~4 min (memoized dependency layer), image ~120 MB web / ~340 MB API after a multi-stage slim; push+scan ~2 min; staging smoke ~2 min; prod rollout at 100 replicas with 25% surge and 10-second readiness period ~ 3–4 min worst case, bounded by `progressDeadlineSeconds: 600` so a stuck rollout fails the pipeline instead of wedging it. Build concurrency: 2 cheap GitHub-hosted runners — 24 merges/day × 6 min ≈ 2.9 hours of build-minutes/day ≈ trivial on a small plan; the expensive part to watch is image storage in ECR (trim by keeping N releases + promoted tags). HPA on the API tier: scale on CPU request utilization (requests, not usage — FT-138), min 3 max 30.
Scoreable points: every number has a unit and a source; the stuck-rollout bound is named (progressDeadlineSeconds); trimming policy on ECR; HPA keyed on requests.

**THE ANTI-PATTERN WALK (three junior design answers to THIS prompt, each quoted, each graded to 2–3/10 — the round's "what not to sound like" cheat):**
Anti-pattern 1 — The Tool Museum: "I'd wire up Argo CD, and Tekton, and maybe Crossplane for composability, and I'd put it behind a full GitOps stack…" Graded: every box is a noun with no verb; no clock, no gate, no rollback; the interviewer must supply the architecture AND the sequence. The honest fix: pick ONE spine (GitHub Actions), and make the spine a verb chain (trigger→build→prove→promote→gate→verify) before ANY tool name is spoken.
Anti-pattern 2 — The Numerologist: "Throughput is around 8,500 requests per second across the fleet, so I'd size it for 12k with a 45% buffer, and the rollout window is 90 seconds exactly." Graded: invented precision with zero sources; one "how did you arrive at 8,500?" collapses the whole answer. The honest fix: three numbers with three sources (the ask-back's stated peak, the queue math on the file, and an assumption exposed with "this is what would change it").
Anti-pattern 3 — The Sequence Ghost: "…and then you just apply it and the rollout happens, and if it doesn't work you roll back and try again, basically." Graded: rollback is a word, not an operation; no wedge arithmetic; a stuck rollout is "roll back" — which is empty when the new Revision owns zero old ReplicaSets. The honest fix: the S5 authoritative statement (surge, unavailable, stall deadline, and WHAT undo creates), spoken as one sentence.
Walk-rule: re-read these before the round, not after. Each anti-pattern is a sentence the interviewer has heard from the last five candidates; its value is that hearing it while it is still only YOUR habit is cheap, and hearing it from the panel is expensive.

**THE CAPACITY MATH, IN FULL (drill this table so S8 is arithmetic, not vibes):**
| Quantity | Value | Where it comes from |
|---|---|---|
| Build wall-clock | ~4 min (memoized layer cache) | 2 runners, dependency layer clean → fast tier cached |
| Image sizes | ~120 MB web, ~340 MB API | multi-stage slim; excludes dev deps |
| Push + scan | ~2 min | ECR, image scan runs in parallel with push |
| Staging smoke | ~2 min | endpoint 200 + served-version string assert |
| Prod rollout, 100 pods | 3–4 min worst case, bounded by progressDeadlineSeconds: 600 | surge 25 → new pods ready at 10-s readiness period → batch |
| Cluster ABI cost (what the strategy spends) | surge: 25 web / 10 API extra pods during the window | maxSurge 25% |
| Capacity floor during rollout | no less than 45 web / 30 API ready at any instant | maxUnavailable 25% |
| Build minutes/day | 24 merges × 6 min ≈ 2.9 h/day | trivial on two small hosted runners (spot check, not a cost block) |
| ECR storage | grows ~460 MB/day of NEW image layers; trim to last N releases + promoted digests | promoted set never pruned — rollback needs the bytes (INCIDENT 28) |
| HPA bounds | API min 3 / max 30 on CPU % of requests | requests, not usage — the FT-138 rule |

The drill rule: compute the rollout wall-clock aloud from first principles — surge number × readiness period + per-batch propagation — rather than quoting "3 minutes" like a magic constant. If the interviewer asks "what if readiness takes 60 s instead?", the honest answer is a new rollout-time estimate, not the same number repeated.

**THE ERROR-BUDGET CALCULATION (the numbers that give the health gates their pass/fail — a gate without a budget is decoration):**
| Input | Assumed value | Where to get the real one |
|---|---|---|
| Monthly uptime SLO | 99.9% | the team's actual word — never invented |
| Budget per month | 43.8 min of error | (100 − 99.9)% × 43,200 min |
| Budget per deploy window | ~30 s of error at p99-high | split: deploys are a small fraction of the month, so a 4-min rollout that burns 30 s of budget is acceptable — IF the canary analysis is the only spender |
| The gate's draft rule | fail the rollout if the canary slice's error rate breaches 5× the baseline for >60 s | an actual number pulled from the team's dashboard before setting it |
| The over-budget behavior | releases PAUSE, they do not continue | the boundary of burn-down authority (posed as a question in R6 S6 Q2) |
The scored move: the candidate READS the budget out of the room's own SLO instead of quoting "we have 99.9 so we're fine". The budget links the canary's threshold to a real contractual number — which is the single most senior sentence in the design.

**THE ECR RETENTION MATH (what "keep last N + promoted set" actually costs and saves):**
| Quantity | Math | The decision it justifies |
|---|---|---|
| New unique image layers per day | ~460 MB/day at 24 merges (both tiers) | over a year ≈ 170 GB if you keep everything — real money in ECR storage |
| Promoted tags needed for rollback | the last 2–3 prod digests only | the promoted set is TINY and must never be pruned (rollback needs the bytes — INCIDENT 28) |
| Dev/PR images to keep | last 5 merge builds, everything else expired | CI churn is the storage leak; it is never the rollback path |
| Lifecycle policy shape | expire untagged beyond N days; expire dev tags by count; NEVER include the promoted set | the retention policy is a whitelist for rollback + a drain for everything else |
The scored line: "the promoted set is never pruned" said unprompted — it is the sentence that proves the rollback plan (S7) is wired into the artifact lifecycle (S4), not a slide that lives on another page. That coupling is the production-judgment tell for the whole design.

**DEPLOY-TIME MECHANICS (the second fenced diagram — draw the 3-min lifecycle, not the spine):**

```
t=0     rollout starts                  revision 12, old ReplicaSet at the readiness gate
        ┌────────────────────────────────────────────────────────────┐
        │ Deployment rlb  replicas 100  maxSurge 25% maxUnavailable 25% │
        │   old set (rev 11): 100 ready                               │
        │   new set (rev 12):   25 surge pods → boot → readiness 10 s │
        ├────────────────────────────────────────────────────────────┤
        │   new ready 25  →  scale down old by 25  →  old at 75       │
        │   new ramp 25+ →  wait: ready count re-checked, then +25    │
        │   per batch; old drains before deletion (terminationGrace)  │
        ├────────────────────────────────────────────────────────────┤
        │   every batch runs the post-batch gate:                     │
        │   error rate < budget AND p99 < budget AND endpoint 200     │
        │   gate fail → this batch pauses; alert; candidate rolls back│
        └────────────────────────────────────────────────────────────┘
t≈4min  new set rev 12: 100 ready, old set 0 → served-version smoke
```
What changes if a batch degrades: the rollout pauses at the breach (it does NOT tear down the remaining old pods), the alert pages, and rollback is `kubectl rollout undo` → a fresh rollout at rev 11's bytes as new rev 13 — while rev 12's partially-new pods cycle out. The scored point is this sequencing: pause-then-rollback on a gate breach, never --force, never "finish the batch anyway".

**THE ROLL-THROUGH, WORKED NUMBERS (the web tier at 60 replicas, maxSurge 25% / maxUnavailable 25% — follow the arithmetic batch by batch):**
```
before rollout:  rev 11 = 60 ready, rev 12 = 0
step 1  surge up:   +15 rev-12 pods boot (maxSurge 25% of 60)
step 2  gate:       new ready 15 > 0 → old can now scale down
step 3  scale down: -15 old → rev 11 = 45 ready; total = 60 (45 + 15)
step 4  next batch: +15 new → 15+15 = 30 new, then -15 old → 30 + 30
step 5  gate check: error rate + p99 within budget at each step
step 6  final:      rev 12 = 60 ready, rev 11 = 0 → exit smoke
capacity floor during the whole window:  rev 11 at 45 (never below 75% of 60)
```
Now the "what if" the interviewer asks: raise surge to 50% → step 1 becomes +30 new, the capacity floor rises but the WALL still bounds the window; a gate failure at step 4 → the rollout pauses at 30/30 with the FIFTEEN new pods already serving — the undo re-runs the same machinery backward. The candidate who narrates these two variants shows the arithmetic is owned, not quoted.

**THE DEPLOY-WINDOW NARRATION (talk the diagram aloud — the running commentary the staff engineer grades):**
"At t=0 rollout 'rlb-2' starts. Old set rev 11 is at 100 ready, so the controller immediately creates the surge: 25 new rev-12 pods, which boot and must pass their readiness period — I said ten seconds in my numbers, so first wave is ready around t+30s factoring in the pull. New ready 25 → the controller scales the OLD set down by 25 → the drained old pods get terminationGrace, finish whatever hand-off they carry, and die. Now old 75, new 25, and the controller does not advance again until the post-batch gate runs: error rate under budget, p99 under budget, endpoint 200. If the gate holds, next batch 25 more; if it fails, this batch pauses, the alert fires, and I have the undo decision ready — rev 11's bytes are re-promoted as rev 13 while the remaining rev-12 pods roll out of the picture. Worst case wall-clock at 100 pods: three batches of 25 plus the drain periods, inside the 600-second progressDeadline — so the pipeline either finishes loudly or fails loudly, and 'silently wedged at half capacity' is a state this design does not admit."
The scored complexity: the narration moves numbers through the diagram in time (surge → ready → drain → gate → next batch) instead of describing the strategy as a static object. The interviewer hears that this candidate can TIMEOUT the release, which is the entire point.

**THE APPROVAL AND AUDIT STORY (the delivery/approval model made concrete — believe the "who can push" answer):**
Every produce-action in the pipeline carries three artifacts: who triggered it, what digest it placed, and which gate approved it. The manual approval for prod is not a checkbox — it records a named human with sign-off authority, and the same file that gates destinations also gates duration: an approval expires, so a stale sign-off cannot bless a deploy three days later. Two-person rule for the destructive surface: an override of the canary analysis is a two-human action with the error budget written into the record. The scored move is calling the approval system an access control (the deploy role is the only principal allowed to mutate prod manifests) rather than a people-process — reviewers approve, machines deploy, and the audit trail is how the two-person rule is enforced, not hoped.

**THE POST-DEPLOY HOLD (a deploy is not finished at green — the graded sentence is how long you WATCH):**
| Segment | What is being watched | How long | The decision if it degrades |
|---|---|---|---|
| Immediate smoke | served-version 200 + metric ingestion | 5 min after full READY | undo NOW — the burst of old-ops ramp-down is cheapest in the first minutes |
| Error-rate | p99 + 5xx against the pre-release baseline | the full roll-forward window (e.g. one deploy cycle, ~24 h) | gate the next deploy; analyze before the NEXT merge ships |
| Saturation | CPU/queue depth vs the new capacity | into the next load peak | re-check sizing assumptions — this is the S8 numbers' real exam |
The scored line: "the deploy is done when the next deploy can ride on the same evidence" — a hold that ends at the deadline of the NEXT merge, not at the last green box. Holding for 24 hours is a grade 8; holding "until it looks fine" is a 4.

**S9 — FAILURE MODES (clock 6 min)**
Interviewer: "Walk the failure modes of this design, and your answer to each."
Model answer:

| Failure | Detection | Response |
|---|---|---|
| CI red on a flaky test | pytest exit codes; fail-fast | stop promotion; evidence before rerun (INCIDENT 24 env-drift check, not blind retry) |
| Image broken, rollout stalls | READY below desired; rollout status hangs | reads probe events; reverses or fixes forward; bounded waits (INCIDENT 27) |
| Canary shows error-rate spike | canary error rate vs baseline | canary to 0, undo; postmortem feed into gate thresholds |
| Same-tag re-point, site still old | served-version string mismatch after rollout | pipeline fails the deploy; tag discipline + digest pin (INCIDENT 29) |
| Secret missing in prod env | pod stuck CreateContainerConfigError | env-scoped secret is the reference, verified in staging first (INCIDENT 12) |
| Artifact gone from registry | re-promote of previous good fails | retention policy keeps last N promoted digests (promoted set never pruned) |

Scoreable points: each failure maps to a war-room incident and a concrete response; detection is a measurable signal, not "we'll notice"; the article-set never pruned is the senior-sounding touch.

**S9b — WRONG VS RIGHT ON THE SAME FAILURE MODE (hear the difference the failure-mode table is protecting you from):**
Wrong (the "we'll catch it" version): "If the rollout fails, we roll back. If the canary fails, we stop it. We monitor everything so we'd notice." — every response is a verb with no trigger, no ownership, no order. The interviewer hears: no detection signal, no decision rule, no verify.
Right (the table version): "Rollout stall — I read probe events and the RS arithmetic first (INCIDENT 27 method), the rollout is bounded by progressDeadlineSeconds so a stall FAILS the pipeline loudly; canary breach — the analysis depth reads error rate and p99 against the baseline and halts to weight-0, which is faster than a human noticing; same-tag misdeploy — the served-version smoke compares the body string, not HTTP 200, so the false-green cannot pass (INCIDENT 29). Every one of those has a name, a read, and a revert — none of them is 'we would notice'." 
The scored difference: the right answer converted every "we'd notice" into a named signal with a named action and a verify — the failure-mode table is that conversion written down.

**S10 — SECURITY (clock 4 min)**
Interviewer: "Where does security live in this pipeline?"
Model answer: secrets are never in repo — pushed through GH Actions secrets / environment-scoped variables, and OIDC from Actions to AWS so the pipeline holds no static cloud keys (SEC.P0.4 pattern): the deploy role's trust policy pins the repository and a narrow policy (ECR push, EKS deploy) with no wildcard resource where avoidable. Gates: secret scan on PR (catches a committed token before it spreads), dependency scan, image scan before the deploy gate, non-root + read-only rootfs in the image. Registry: ECR with image tag immutability so the SHA tag cannot be re-pointed after push. Access: prod approve requires two-person review pull; the deploy role is the only principal that can mutate prod manifests.
Scoreable points: OIDC-not-keys is stated; gate positions named; tag immutability on the registry; the reviewer-approval model as an access control, not a process wish.

**S11 — OPEN QUESTIONS AND WHAT YOU WOULD VERIFY IN A REAL SHOP (clock 3 min)**
Interviewer: "You are 1–3 YOE. What do you not know about this design, and how would you close the gap?"
Model answer: three honest unknowns: (a) the actual SLOs and alert routes (my gates are reasonable defaults; a team may already promise tighter budgets, so I would read their dashboards before setting thresholds); (b) whether the RDS team allows expand-contract or expects pipelines to trigger migrations — that changes the release shape; (c) whether EKS is already managed or needs bootstrap scope, which I flag as a separate workstream. Closing the gap: read the existing deploy and monitoring, pair with the incoming engineer, and prove the pipeline on staging for a week before a prod change. I am not going to claim I have run this at 60-replica scale — that is the honest claim-level for this design: PRACTICED on a local cluster and one live deployment, not DESIGNED-fleet.
Scoreable points: names real unknowns; the claim-level honesty lands (the interviewer hears the 16-resume-defense voice); proposing to read evidence before building is production judgment.

**SCRIPTED DESIGN FOLLOW-UPS (the interviewer's five follow-ups in S6–S8, with the model response beat):**
| Follow-up | Why it is fired | Model response beat |
|---|---|---|
| "Your canary ramps on error rate and p99. What do you do with a low-traffic tier where p99 is noise?" | Tests whether the gate is a real threshold or a slogan | I widen the window and gate on error-rate + throughput threshold, or fall back to rolling-with-instant-undo; a canary with no signal-to-noise is theater, and I say that out loud. |
| "Parallel deploy of web and API — what ordering do you use and why?" | Sequence reasoning | API first, because the API's schema change must land and verify before the web tier that calls it is replaced; web second, on the now-stable backend. DB expand happens even earlier and never rides the image rollout. |
| "Someone bypasses the pipeline and edits the manifest in prod. What breaks?" | Drift and guardrails | The state source drifts from the manifest repo — I add drift detection on the manifests (a recurring diff job) and lock prod mutations to the deploy role, because an out-of-band edit makes the next promotion an unknown. |
| "Your registry is immutable for the image tag. Where does the 'latest' for a local dev come from?" | Boundary honesty | A separate dev tag namespace that is allowed to be mutable and is never referenced by the deploy paths; immutable applies to anything that can reach a gated environment. |
| "Two teams join you in six months. What scales in your design, and what does not?" | The adoption clause from the brief | The artifact + digest + gate model scales; the manual approval step and the single-cluster assumption do not — I would hand the gate to a pipeline-level approval service and revisit multi-env before I promise it. |

**S12 — THE ONE-LINE CANONICAL ANSWER (clock 1 min)**
Interviewer: "Thirty seconds to sell the whole design back to me."
Model answer: "One proven artifact, promoted unmodified through gated environments, rolled out per-tier by its failure cost — web rolls, API canaries against real metrics, RDS expands its own schema — every deploy health-gated with a served-version verify and a rollback that checks the bytes first; red never promotes, and anything that hangs fails loudly instead of quietly halving capacity."
Scoreable points: the summary names artifact, gates, per-tier strategy, DB separation, verify, and the fail-fast rule — every major design decision compressed to 30 seconds.

**DESIGN METRIC SELF-CHECK (score the round as the staff engineer would — fill honestly):**
| Metric | Self-score 1–5 | Why |
|---|---|---|
| Ask-back coverage (S1): did I seek the decisions that change the design? | | mention DB migrations + approval model + error budget unprompted |
| Scope discipline (S2): did I exclude senior features with reasons? | | multi-region / mesh / GitOps named and justified out |
| Mechanism math (S6/S8): numbers derived out loud, not quoted | | rollout wall-clock recomputed as the question changed |
| Gate honesty (S7/S9): every rollback has a measurable trigger | | no trigger = "wait and see" anywhere |
| Unknown self-report (S11): real gaps named with a close plan | | a blank here is the 1–3 YOE failure mode |
A self-score of any 2-or-below maps directly to a MUST FIX row; a full row of 4s means this design is ready to be told as tomorrow's STAR narrative to a behavioral interviewer.

**SCORE TABLE (7 axes):**

| Axis | /10 | Why |
|---|---|---|
| Technical accuracy | | Numbers and mechanisms checkable against FT-136/150/152 and INCIDENT 27/28/29 (maxSurge math, undo-is-new-revision, digest pin). |
| Reasoning & structure | | Ask-back before draw; tiers-by-failure-cost; detect→respond per failure mode; the spine is dependency-ordered. |
| Communication | | Diagrams drawn in time, definitions clean, the S12 sell-back lands in 30 s. |
| Depth & nuance | | DB-expand-contract separation, canary feedback loop, promoted-digest never pruned, HPA on requests not usage. |
| Follow-up defense | | Each "why did you pick canary/rolling" answered by failure cost, not by tool loyalty; no contradiction between S6 and S7. |
| Production judgment | | Bounded rollout waits, two-person sign-off, evidence-before-rigging thresholds, honest scope exclusions. |
| Uncertainty handling | | S11 names three unknown: how you would close each; no invented fleet-scale experience. |

**REFLECTION (fill after):** _what I said_ — transcribe the ask-back (S1) fully: the question list is the highest-leverage 5 minutes of the round. _where I froze_ — likely at S8 numbers; fix by drilling the capacity band of FT-136/150. _where I overclaimed_ — any tier count or SLO number you invented; replace with "I would read the dashboard first" every time.

**MUST FIX / SHOULD FIX / NICE TO HAVE:**
| MUST FIX | SHOULD FIX | NICE TO HAVE |
|---|---|---|
| Failing to ask about DB migration mechanics before design | Canary described without a feedback metric (error rate + p99) | Promoted-digest-never-pruned retention policy |
| A design with no served-version verify (INCIDENT 29 lesson) | Rollout without progressDeadlineSeconds bound | OIDC for Actions stated unprompted |
| Same artifact rule violated anywhere (dev rebuilds for prod) | Claiming fleet-scale experience at PRACTICED | S12 sell-back under 30 s with all four decisions |
| Rollback plan with no bytes-intact + migration check | scope creep into multi-region/service-mesh without justification | two-person-review prod approval as access control |

**THE SENTENCES THAT SCORE (the design round's phrase sheet — one sentence per S-block that the panel writes down; rehearse these EXACT, the rest of the round is your own):**
| S | The sentence that earns the note |
|---|---|
| S1 | "Before a box: how do schema migrations ride with code — does the DB change in the same deploy?" |
| S2 | "Done is: staging and prod serving the same digest, verified by served-version, not a green checkbox." |
| S3 | "One artifact, digest-pinned; everything after the gate exists to place it, watch it, and roll it back." |
| S4 | "CI proves the artifact, CD proves the placement — two concerns that are paying core production shells, and splitting them is the whole discipline." |
| S5 | "Rolling on failure-cost, not simplicity; undo is a new revision at old bytes, never time travel." |
| S6 | "The approval record is the access-control audit — reviewers approve, machines deploy." |
| S7 | "25% surge, 25% unavailable — worst case the fleet never drops below three-quarters, and the gate pauses the batch instead of completing it." |
| S8 | "The capacity number has a source and a 'what would change it'; anything else is theater." |
| S9 | "If it fails, the runbook. If it spills, the team. The pause is a report, not a decision to be made by me alone when the budget is burning." |
| S10 | "Blue/green pays for calm at double capacity; at this scale the failure-cost math says rolling plus a canary-when-it-matters." |
| S11 | "The serve runs on observed numbers; the welcome signs run on decisions; and my ceiling is stated before you ask." |
Phrase-rule: rehearsing the sentence WITHOUT the mechanism behind it is memorization; the sentences exist to be the close of each S-block's answer, not its whole. If the interviewer probing any of these gets a second level from you, the sentence is owned; if not, it was a slogan and the tape will index it as one.

### QC CHECKLIST — ROUND 3
| # | Check | Status |
|---|---|---|
| 1 | One design prompt chosen (CI/CD + rollout for the 3-tier app), not both | PASS |
| 2 | Ask-back question list present before the diagram | PASS |
| 3 | Fenced text diagram of the full spine is balanced | PASS |
| 4 | Capacity numbers present with units and sources | PASS |
| 5 | Failure-mode table present with detection + response rows | PASS |
| 6 | Deployment strategy per tier and rollback per strategy present | PASS |
| 7 | Scope is framed at 1–3 YOE with honest claim-level (PRACTICED, not DESIGNED-fleet) | PASS |
| 8 | All cited assets resolve: FT-136/138/149/150/152, INCIDENT 12/24/27/28/29, SEC.P0.4, CICD.P0 lineage | PASS |
| 9 | Score table has exactly the 7 axes | PASS |
| 10 | Reflection section with blanks present | PASS |
| 11 | MUST FIX / SHOULD FIX / NICE TO HAVE present | PASS |
| 12 | No emojis, no placeholder wording, fences balanced in this round | PASS |
| 13 | SELF-VERIFY — model answers are sourced from the real sibling sessions (FT/chain/incident IDs resolve) | PASS |

VERDICT: **ROUND 3 COMPLETE.** A scoped, mechanism-first delivery design. The grade split to watch: production judgment (S1/S11) is worth more than the diagram — a candidate who asks about DB migrations and names their own unknowns outscores one with a prettier drawing.
NEXT POINTER: ROUND 4 flips to behavioral — the exact same pipeline story becomes a STAR narrative that must survive a hostile interviewer on SECOND probe.

---

## ROUND 4 — B · 45min · Behavioral + resume strike

**SCENARIO BRIEF:** A screen with a tough senior SRE and a hiring manager. This interviewer read your resume line by line and built the questions to make each bullet confess its weakest claim. Every STAR answer gets a hostile twist: the first probe reframes your answer, the second demands a number you do not have, the third asks you to downgrade or retract in public. The round trains the honest-downgrade reflex: it is better to cut a bullet live than to defend it past the point of credibility.

**OPENING PROMPT (say verbatim):** "Before we do anything else — I want you to sell me one line from your resume, and I'm going to treat it like it's lying until I can't. Pick whichever one you think is strongest. Go."

**S1 — STAR + hostile twist · bullet 16-01 (CI/CD pipelines)**
Interviewer: "Walk me through the CI/CD pipeline you built."
Twist chain: (1) "You said 'built and maintained'. What about it was maintained — nightly? weekly? by you?" (2) "Give me a number: how many deployments a week went through it, and how many times did it break the deploy?" (3) "Would you put this pipeline in front of my production traffic tomorrow? Yes or no, then justify."
Model STAR: Situation — the war-room delivery spine (09-cicd): a GitHub Actions pipeline from commit to a kind-cluster deployment with a live ECR-to-EKS leg. Task — prove the full spine: trigger, build, test, image, registry, deploy, smoke. Action — wrote the workflow with fail-fast stages and a bounded rollout-verify; pushed an image with an immutable SHA tag; verified with a smoke HTTP 200 after deploy; tore everything down (the environment-facts rule). Result — a repeatable pipeline run end-to-end on a live EKS deployment, with one real debug cycle (CrashLoopBackOff caused by a missing busybox applet, exit 127) documented start-to-finish. Honest downgrade offered unprompted: "Maintained means I ran it and fixed it in a controlled environment — not a production fleet; I would not promise to babysit your traffic tomorrow before I had run it at your scale for a week."
Scoreable STAR elements: S/T/A/R all present; degree uses the evidence anchor; the downgrade lands BEFORE probe 3 forces it; the two fences ("maintained", "production") are set by the candidate.

**S2 — STAR + hostile twist · bullet 16-03 (Terraform modules)**
Interviewer: "Your resume says you wrote Terraform modules. Walk me through one, end to end."
Twist chain: (1) "What did the module even wrap?" (2) "Your colleague modified state by hand — walk me through how you know, and what you do." (3) "Honest answer: plan said destroy for a resource you did not touch. What is the first thing you check?"
Model STAR: Situation — provisioning review at the war-room AWS/Terraform phase (08-terraform). Task — build reusable infra modules with remote state discipline. Action — wrote module boundaries, pinning/provider/locking, and ran the state-lock and drift labs: reproduced a ConcurrentPlanError lock (INCIDENT 22), read the DynamoDB lock item to see who held it, and diagnosed a plan-that-wants-destroy as address drift, fixed with `moved`/`state mv` — never hand-editing tfstate (INCIDENT 23). Result — modules that plan clean and fail loudly on drift; the destroy-line rule became a permanent habit. Honest downgrade: "My module set is a handful of verify-able resources on a real but small footprint — I have not designed a platform module hierarchy for a live multi-account org."
Scoreable STAR elements: the state story is the depth; the downgrade is honest about scope; refuses to claim multi-account org design.

**S3 — STAR + hostile twist · bullet 16-06 (security hardening)**
Interviewer: "Tell me about a security thing you actually hardened."
Twist chain: (1) "What was the threat you were hardening against?" (2) "Walk the IAM evaluation that decides whether your hardening even works." (3) "Your secret is already in git history. Order your response."
Model STAR: Situation — security overlay across the war-room (11-security). Task — harden a containerized workload the way an interviewer would probe. Action — ran the IAM read-only census and the container hardening proof (non-root, read-only rootfs, cap-drop) reading CapEff from /proc; reproduced the SSH publickey-denied-in-0644 file-mode failure (INCIDENT 15); practiced the secret-in-git response order — rotate/detach NOW, then branch history rewrite, then scan gate, then verify nothing cached (INCIDENT 30 rule, SEC.P2.2). Result — a repeatable proof set, each with a documented incident behind it. Honest downgrade: "I hardened prove-able lab workloads and one live path; I have not been the owner of a production security program."
Scoreable STAR elements: the IAM-evaluation answer (deny beats allow, identity AND resource) proves mechanism; the secret-leak ORDER is exactly what a security-adjacent interviewer probes for.

**S4 — STAR + hostile twist · bullet 16-07 (bash automation)**
Interviewer: "You say you automated ops with bash. Give me a script you're proud of and then kill it for me."
Twist chain: (1) "What does it do that a one-liner with jq wouldn't?" (2) "What happens when that curl hangs forever?" (3) "Walk me through how you'd make sure it fails loudly and exits nonzero — no whiteboard, just talk."
Model STAR: Situation — the BASH.P0–P1 sessions (04-bash). Task — a health-gate script that provably checks an endpoint. Action — built a curl health gate with explicit retry, `--fail`, bounded timeout, `set -euo pipefail` semantics, and verbose failure output; used jq to parse and assert the health payload rather than grep-vibes; handled the survivors (failures inside `if`, pipeline masking) deliberately. Result — a gate whose exit code IS its verdict, which became the finish line of the P0.4 CI pipeline. Honest downgrade: "It is a gate for a controlled pipeline, not battle-tested job orchestration — but the exit-code contract is what I would defend in your prod CI too."
Scoreable STAR elements: answers the retry/hang and the fail-loud/nonzero semantics from mechanism; the immutable-exit-code contract is the production-thinking tell.

**S5 — STAR + hostile twist · bullet 16-08 (git workflows)**
Interviewer: "Tell me about a time git bit you and you had to fix it."
Twist chain: (1) "Was it your mistake?" (2) "Walk me through the exact commands you used to recover." (3) "Why not just force-push your way out?"
Model STAR: Situation — the verified wrong-branch recovery in 03-git (the reflog arc, 14-14's canonical story). Task — recover work lost to an aggressive reset on the wrong branch. Action — named the honest mistake first, used `git reflog` to find the pre-reset commit, restored it with a branch/merge instead of force-push, and verified the working tree against the intended state (the load-test-equivalent prove). Result — the work survived with full attribution; the incident became the personal rule "reflog is the undo button; force-push is the last resort". Honest downgrade: "I've recovered branch-state mistakes on a small authored repo — not a distributed team's main branch under pressure."
Scoreable STAR elements: ownership stated before mechanism; recovery commands are reflog + restore, not force-push; the rule extracted from the incident.

**S6 — STAR + hostile twist · bullet 16-09 (incidents / on-call)**
Interviewer: "Tell me about a production incident you owned."
Twist chain: (1) "What page fired, at what time, and what did your dashboard look like?" (2) "Then what — you and who?" (3) "You used the word 'production'. In the last year, how many hours were you actually on a live on-call rotation?"
Model STAR: Situation — the incident-training corpus in 12-troubleshooting (30 incidents, 4 archetypes). Task — tell a true incident story at the candidate's depth. Action — chose the INCIDENT 02 empty-endpoints arc: symptom (resolves but times out), scope (one Service), method (get endpoints first → selector mismatch), fix (label correction), verify (in-cluster probe returns content). Result — a narratable, honest incident with a documented prevention. Honest downgrade — the answer MUST contain this exact public retraction: "My hands-on experience is controlled-env; my incident reps are a 30-incident playbook with narrated runs. I have not been the sole responder on a live on-call rotation, and I will not claim on-call hours I don't have."
Scoreable STAR elements: the downgrade converts the axis instead of fighting it; the interviewer hears the lie-detector list item 6 ("I have production experience") being self-cut in real time; the STAR still lands fully at the honest depth.

**S7 — STAR + hostile twist · bullet 16-12 (networking)**
Interviewer: "Give me a networking story — the time DNS, a load balancer, or TLS actually bit you."
Twist chain: (1) "Which of the three layers failed?" (2) "How did you separate the failing layer from the ones that were fine?" (3) "A client says 'connection refused'. Your three checks, in order — and the one that decides it's the LB and not the app."
Model STAR: Situation — the networking sessions (02-networking) and INCIDENT 04 (ALB 502/503). Task — an end-to-end reachability debug with layer separation. Action — used refusal-vs-timeout discrimination, the ALB listener→target-group→health chain, and the target-health report as the first read before touching SGs. Result — a repeatable triage order that names the layer before the fix; refusal = RST means something answered, timeout = silence means path/host/filter. Honest downgrade: "I've separated layers on lab and modeled incidents — I have not tuned BGP or engineered MTU on a live fleet; that is diagnostic practice, not neteng."
Scoreable STAR elements: layer separation is explicit; the refusal-vs-timeout mechanism decides the LB-vs-app branch; scope stays honest.

**S8 — STAR + hostile twist · bullet 16-14 (cost / capacity)**
Interviewer: "Your resume mentions cost management. Prove it with a number."
Twist chain: (1) "Give me the exact line-item that cost too much." (2) "Show me the math — before and after." (3) "You said 'right-sized'. What metric told you it was time, and who approved the change?"
Model STAR: Situation — the cost/capacity memory work (05-aws, 10-observability) at UNDERSTOOD + real-math level. Task — demonstrate capacity arithmetic, not a dashboard screenshot. Action — took the documented max-pods/capacity reasoning and S3→Standard-IA write/read analysis and produced a before/after line: e.g. a 100-replica pod count where over-allocation requests meant N unused nodes of reservation; and telemetry cardinality cut (one label value driving a histogram family) reducing series count materially. Result — a defensible cost story whose numbers come from the war-room's own measured allocations, not invented invoices. Honest downgrade: "UNDERSTOOD plus real math is my ceiling here — I have not owned a cloud billing lease; if the role needs that, tell me and I'll be straight about it."
Scoreable STAR elements: refuses to invent a billing figure (the #1 fabrication trap); the math is reproducible; the downgrade is a claim-level statement, not a confession.

**S9 — STAR + hostile twist · bullet 16-16 (initiative / ownership)**
Interviewer: "Tell me about a project you led."
Twist chain: (1) "Who reported to you?" (2) "What decision was yours alone?" (3) "Re-read your resume: it says 'led'. Keep the sentence, or cut it — now."
Model STAR: Situation — a technical initiative owned end-to-end (the war-room architecture-to-verification loop). Task — prove ownership with no direct reports. Action — made and defended real decisions: tool choice (GitHub Actions over Jenkins), claim-level fences, a teardown rule that left the environment pristine — each reversible and documented. Result — an initiative with an architecture docs trail, a QC gate, and a defined done-state. Honest downgrade (the trap is the word "led"): "I owned a technical slice end-to-end with no direct reports — I will say 'owned a slice', not 'led a team'. Those are different claims and mine is the smaller one."
Scoreable STAR elements: catches the lie-detector item 7 (led a team) and self-edits; responsibility demonstrated without inflating to management.

**S10 — STAR + hostile twist · bullet 16-18 (runbooks / documentation)**
Interviewer: "You wrote runbooks. Where do they live, who reads them, and prove one saved somebody time."
Twist chain: (1) "Give me the incident your runbook covers and why it's the right one to write down first." (2) "What is the 'finished' bar for a runbook you would be caught dead operating at 3am?" (3) "Your runbook's first step is wrong now. Walk me through how you keep it honest."
Model STAR: Situation — the 12-troubleshooting playbook's structure (symptom→scope→hypotheses→check→evidence→fix→verify→prevent). Task — write a runbook that works at 3am, not a ceremony. Action — the 3am bar: the runbook starts with the symptom and the FIRST check that discriminates it from the neighboring incidents (INC 20 vs INC 16 vs INC 19), lists the cheap rules-in/rules-out commands, and ends in a prevention that is one action. Result — an incident family where the next responder can skip the exploration entirely. Honest downgrade: "They are my training playbook, exercised in narrated drills, not yet adopted by a wider team — the honest claim is I write runbooks that survive the incident-family test, and I am the one operator who has actually run them."
Scoreable STAR elements: the discriminating-first-step concept IS the interview answer; the downgrade draws the line between personal and team-owned docs.

**THE FULL BULLET CENSUS (every file-16 bullet used by this round, its claim-level ceiling, and the twist chain that tests it):**
| Bullet | Honest claim ceiling | The question that would expose inflation | Where this round fires it |
|---|---|---|---|
| 16-01 CI/CD pipelines | OPERATED-controlled-env + one live leg | "How many prod deploys a week?" | S1 |
| 16-02 Docker/containerization | OPERATED (builds, run, registry, compose) | "Which layers did you actually build?" | replaced by 16-01 in the ten-set; re-drill covers it |
| 16-03 Terraform modules | PRACTICED (small module set, real labs) | "Who else uses your module?" | S2 |
| 16-04 AWS services | PRACTICED-to-OPERATED per service | "Walk the IAM for THAT service" | S3 carries the IAM proof |
| 16-05 CI/CD tools | OPERATED GitHub Actions, UNDERSTOOD peers | "Argo CD for you — walk the sync" | R6 U2 covers the boundary |
| 16-06 security hardening | OPERATED in controlled scope | "Own a security program?" downgrade | S3 |
| 16-07 bash automation | OPERATED scripts, honest ceiling | "What runs this in prod?" | S4 |
| 16-08 git workflows | OPERATED recovery, small repo | "Team main branch, under pager?" | S5 |
| 16-09 incidents / on-call | UNDERSTOOD-PRACTICED (narrated reps) | "Hours in a live rotation?" | S6 — the retraction |
| 16-10 monitoring/logging | OPERATED Prometheus/Grafana stack | "Write the PromQL you alert on" | carried into R1/R6 anchors |
| 16-11 container orchestration | OPERATED kind/single-cluster, UNDERSTOOD fleet | "Multi-cluster failover you ran?" | R6 U7 boundary |
| 16-12 networking | UNDERSTOOD + diagnostic practice | "Tuned BGP? Sized MTU on a fleet?" | S7 |
| 16-13 Linux systems | OPERATED common surface | "Which syscall does that trace show?" | S1 pair carries it |
| 16-14 cost / capacity | UNDERSTOOD + reproducible math | "Your billing line item — the number?" | S8 |
| 16-15 team leadership | not claimed at all | — | — |
| 16-16 initiative / ownership | OWNED-a-slice, no direct reports | "Who reported to you?" | S9 — the "led" cut |
| 16-17 documentation | OPERATED personal-to-team line | "Who adopted your runbooks?" | S10 |
| 16-18 runbooks / incident docs | OPERATED personal exercises, not team-adopted | "A stranger ran yours at 3am?" | S10 carries it |
Census rule: run every bullet through "could an interviewer own me with a WHO/WHEN/NUMBER question?" — a yes to any unclaimed depth is the bullet you rehearse the downgrade for next, because that is the exact drill the twist chain does on the round.

**WHY THE TWIST CHAIN IS THREE PROBES (the mechanism behind this whole round):**
Probe 1 reframes your answer — it tests whether you understood it or memorized it. Probe 2 demands a number or a mechanism you may not hold — it tests the claim's floor. Probe 3 asks you to downgrade or retract in public — it tests whether the honesty reflex runs on demand. The chain is engineered so there is exactly ONE survivable path: answer with mechanism, admit the floor, downgrade before the demand. Every juncture you fight instead of downgrading extends the fight and caps the axis.
| Probe | What it is actually measuring | The winning response | The losing response |
|---|---|---|---|
| 1 (reframe) | comprehension vs memorized script | same model, new words | repeating the identical sentence |
| 2 (number/depth) | the floor under the claim | the number, or "I don't have that figure — here is the reproducible version" | inventing a plausible number |
| 3 (public cut) | honesty under pressure | cutting it live, calmly | defending past credibility, or refusing to decide |

**FIVE JUNIOR FAILURE PATTERNS SPECIFIC TO BEHAVIORAL ROUNDS (and the line that defeats each):**
| Pattern | The tell | The defeat line |
|---|---|---|
| The hero story | every answer ends in a team-saving last-minute | "The honest end state is X; the ceiling on this one is Y" |
| The ownership dodge | "we did it" — no personal verb anywhere | "My part was — and the decision I owned was —" |
| The invented number | a billing figure or p99 you cannot reproduce | "I don't hold that figure; I can reproduce the math" |
| The claim drift | "I built the pipeline" drifting into "I built the platform" in the same sentence | "Same claim: pipeline. The platform is a different sentence" |
| The blame leak | mistakes always "the incident in question" never "my mistake" | "This one was mine — here is exactly how" |
The round grades your tape for these five tells on every STAR, not just the ones the twist chains target. Two tells anywhere in the tape = a follow-up-defense cap of 4 regardless of axis scores elsewhere.

**THREE WRONG STAR OPENINGS (transcripts of how behavioral answers die in the first line — hear them, then reject them):**
The Overclaim Open: "I built a CI/CD platform that manages production for the whole company, and my team of three…" — the lie-detector's first column ticks on "platform", "whole company", and "team of three" in one breath. The downgrade that follows is a recovery, not a clean opening.
The Vague Open: "So there was this incident, and I was kind of involved with the team that dealt with it…" — ownership opened with "kind of involved"; the interviewer now has to drag the "my part was" line out of you. A behavioral grade that starts at "kind of involved" has a follow-up-defense ceiling of 5 before you say another word.
The Mechanism-Dump Open: "kubectl get endpoints first, then check selectors, then describe pod — and the fix was to correct the label, and-oh also NetworkPolicy…" — the candidate answered the STAR question with a checklist. The interviewer asked for a YOU-story; the correct first line is "One service in my control resolved but timed out; my part was triage and the fix was a one-line label correction."
The first-line rule for every STAR: Situation sized, YOUR verb in the first sentence, Mechanism after the ownership — never the other way around.

**STAR STRUCTURE TEMPLATE (the four beats every answer must lay out visibly — fill per bullet before the round):**
| Beat | What the interviewer listens for | Template line | Example filled (16-02 style) |
|---|---|---|---|
| Situation | the environment, sized honestly | "The context is <one line>: a <scope> at <ownership level>" | "A shared kind cluster used by the whole workshop, fully owned by me" |
| Task | the goal as YOUR responsibility | "My part was <verb>: prove/find/fix <object>" | "My part was to prove the full ECR-to-EKS deployment, not just the workflow" |
| Action | the method, ordered, with decisions | "I did <ordered verbs>; the decision I owned was <choice>" | "I wrote the workflow, pinned the digest, and RE-routed the rollout when the probe 404'd" |
| Result | a verifiable end-state + the honest ceiling | "End-state <metric>; the ceiling is <claim-level>" | "Ends 'successfully rolled out'; ceiling = controlled-env, not fleet" |
Rule: the interviewer must be able to say back your four beats without asking a clarifying question. If they cannot, the STAR was a story, not an answer.

**THE STAR-DEBRIEF FOUR PROBES (what a panel opens with the moment a STAR lands — rehearse the four canned answers, they are predictable):**
| Panel probe | What it is actually testing | The beat it expects |
|---|---|---|
| "What was YOUR specific contribution?" | whether the STAR is a team report or an independent | a first-person verb chain: "I wrote… I pinned… I reversed…" — never "we fixed it" |
| "What would you do differently?" | follow-up defense and self-correction | a real alternative with a price: "gate the canary on error-rate sooner — that gap is now the re-drill line" |
| "What did you LEARN that outlived the task?" | whether the story generalizes into a rule | a rule sentence: "read-only-before-mutation is now a habit, not a step" |
| "Honest — what was the ceiling?" | the lie-detector's umbrella probe | the claim-level offered first: "controlled environment, not fleet — OPERATED, not DESIGNED" |
Probe-rule: the four probes are the SAME questions across every company, because they are the four risks a hiring team must clear (individual contribution, self-correction, generalization, honesty). Rehearsing the canned beat does not cheapen the answer — the interviewer needs to see the beat arrive in seconds, and seconds are what the mock exists to buy.

**THE S7 OUTAGE STAR, VERBATIM (bullet 16-07 + INCIDENT 27 — the highest-traffic behavioral moment in the file, rehearsed line by line):**
Interviewer: "Give me the outage where you were on the alert and the rollout was the suspect — end-to-end."
Candidate: "Situation — one shared cluster, a deployment whose readiness probe was reporting 404 on the new Releases… the pod matched the Deployment, but the new Revision was not the one serving; the Service selector was half-painted, so the running pods were old code serving old labels. Task — it was mine because the Deployment was a change I had just shipped; the incident team was me and the on-call for the platform. Action — I did not scale or restart. I read the object chain read-only first: describe the deployment, check the surfaces, and the 404 probe tells me the probe is pointing at a path the new container is not serving — then I read the endpoint slice, and that is where the selector shout was: old pods, empty under the new selector. I corrected the label, let the rollout reconcile, and when the readiness gate still stalled I bound a wait by progressDeadlineSeconds instead of forcing the ReplicaSet scale that the old ReplicaSet is NOT allowed to die mid-story, and the ReplicaSet the old selector now found. Result — bytes reconciled on the digest I had pinned; serving identical suite on the smoke 200; ceiling — controlled environment, INCIDENT 27 folder on disk, not a fleet, and the prevention is the same-probe contract in CI."
The graded beats: read-only-before-mutation said aloud; the 404 probe read as "path the app is not serving" (not "app is down"); the selector-vs-probe layering; a wait substituting for a force; the honest ceiling INCLUDED in the STAR, not prompted; and the prevention identical to the technical answer in R2 — a cross-round anchor that the matrix checks on purpose.

**THE FOUR-BEAT TIMING TABLE (each STAR is ~3–4 min; the beats are not equal):**
| Beat | Time | What cannot be skipped even under pressure |
|---|---|---|
| Situation | ~15 s | the scope line, sized honestly — "one shared cluster I owned" |
| Task | ~15 s | YOUR verb — "prove / fix / find / recover" |
| Action | ~60–90 s | the ordered verbs + the ONE decision you owned |
| Result | ~30 s | the verifiable end-state + the claim ceiling |
| Probe answers (3) | ~60 s total | downgrade latched, numbers honest, no contradictions |
Total floor ~3 min; anything that spills past 4 min with a silence is a cadence failure — the STAR was crowned with too much Action, not too little. The interviewer rarely scores a 5-minute STAR above a 3-minute one.

**THE FULL S1 VERBATIM EXCHANGE (16-01, CI/CD — the round's first STAR, run end to end):**
Interviewer: "Walk me through the pipeline you built."
Candidate: "Situation: a single kind cluster for the workshop, fully owned by me. Task: prove the delivery spine end to end — trigger, build, image, registry, deploy, smoke — exactly what a CI/CD pipeline has to do for one commit."
Interviewer: "And 'maintained'?"
Candidate: "Honest calibration: 'maintained' means I ran it and fixed it in a controlled environment — not a production fleet. I want to put that fence up now so it does not leak later."
Interviewer: "Give me a number — deployments a week, and breaks?"
Candidate: "Every staged run targeted a live EKS deployment one-to-one; the debug cycle I kept is the CrashLoopBackOff from a missing busybox applet — exit 127 — documented start to finish. What I cannot give you is a production weekly volume, because there wasn't one."
Interviewer: "Would you put it in front of my traffic tomorrow?"
Candidate: "Zone answer, then justification: no — not before I ran it at your scale for a week. The pipeline itself I would defend anywhere; the claim on production-hold is the honest one."
The pattern to copy: the fences went up in the FIRST and SECOND answers (before probe 3 could force them), the number offered was the one that exists, and the "no" to production came with the week-of-scale condition that makes it a plan, not a refusal.

**THE S3 SECURITY VERBATIM (16-06 — the IAM-evaluation probe is the part candidates fumble first):**
Interviewer: "Tell me about a security thing you actually hardened."
Candidate: "A containerized workload, in my controlled environment — that scope matters. The threat I hardened against was the two that matter first: a leaked credential, and a container that runs with more ability than it needs."
Interviewer: "The IAM evaluation — walk me through whether your hardening even works."
Candidate: "The evaluation is a two-surface test. Identity policy and resource policy both have to allow; explicit deny beats a matching allow everywhere; with no deny and no allow it is implicit deny. My hardening is only 'working' if a denied call stays denied on BOTH surfaces — I verified the read-only census against the deny-first rule, not against 'looks locked'."
Interviewer: "Your secret is already in git history. Order your response."
Candidate: "One: rotate and detach the value NOW — the leaked credential is dead from this second. Two: rewrite the branch history so the blob does not exist to be found. Three: add a scan gate so the class dies before merge, not after. Four: verify nothing cached — check mirrors, forks, and the reflog for the leaked value. That order is the one thing I will not reorder: rotation before history, because a rewrite with a live credential is theater."
The scored beats: the statement "rotation before history, because a rewrite with a live credential is theater" is exactly the sentence a security-adjacent interviewer writes down — mechanism, order, and the reason for the order in one line.

**THE S8 COST-STORY TRANSCRIPT (16-14 — the "prove it with a number" question, done without inventing a billing figure):**
Interviewer: "Your resume mentions cost management. Prove it with a number."
Candidate: "Here is the reproducible one. A workload of 100 pods whose REQUEST was over-allocated — say every pod asked for 2 CPU when the measured p99 was 1.2 — means the scheduler reserves 200 CPU to serve ~120 measured. That is the reservation cost: nodes paid for that no workload can reclaim. Before/after: request equal to measured plus a 20% margin → the reservation drops from 200 to 144 CPU, and the node count follows the reservation, not the usage."
Interviewer: "And the metric that told you it was time — who approved?"
Candidate: "The tell was utilization-vs-request ratio drifting under 60% consistently, not a single spike. The approval was a written change with the before/after math in it — right-sizing is a capacity change, so it goes through the same review as any capacity change. What I will not do is hand you a 'saved $X/month' figure I cannot reproduce — the reproducible math is the honest number here."
The scored beats: the before/after arithmetic is REPRODUCIBLE (requests arithmetic, not a billing export), the trigger metric is named, the approval path is adult, and the refused invented-billing-line converts the whole answer from a possible fabrication into a demonstrated method — which is exactly the S8 surprise the twist chain was built to produce.

**THE TEN STAR SKELETONS (one line per beat, pre-filled — the entry card for the round; full answers are rehearsed from this card):**
| # | Bullet | S (one line) | T (your verb) | A (ordered verbs + the owned decision) | R (verifiable end-state + ceiling) |
|---|---|---|---|---|---|
| S1 | 16-01 CI/CD | one kind cluster, owned | prove full delivery spine | wrote workflow, pinned digest, rode 404 → "successfully rolled out" | one live E2E + the debug cycle; ceiling controlled-env |
| S2 | 16-03 Terraform | AWS provisioning study | write reusable modules | defined boundaries, ran lock/drift labs, fixed wanted-a-destroy with moved | modules plan clean; ceiling small footprint |
| S3 | 16-06 security | lab container + IAM census | harden, then prove | non-root/rootfs/cap-drop, read CapEff, secret response order | repeatable proof set + incident lines; ceiling lab |
| S4 | 16-07 bash | the P0.4 gate | build a health gate | curl --fail bounded, jq assert, exit-code contract | gate whose exit IS the verdict; ceiling pipeline |
| S5 | 16-08 git | my wrong-branch reset | recover lost work | reflog find, branch-restore, verify tree, no force-push | work attributed + restored; ceiling authored repo |
| S6 | 16-09 incidents | INC 02 empty-endpoints | narrate honestly | endpoints first, selector mismatch, same-probe verify | narrated STAR + zero-live-rotation retraction |
| S7 | 16-12 networking | layer-separation study | triage end to end | refused-vs-timeout, target-health-first, SG last | a repeatable layer order; ceiling diag-not-neteng |
| S8 | 16-14 cost | measured allocation data | demonstrate math | requests arithmetic, cardinality cut, before/after line | a defensible cost story; ceiling UNDERSTOOD |
| S9 | 16-16 initiative | war-room loop | own a slice | chose Actions over Jenkins, teardown rule, QC gate | docs trail + defined done; ceiling slice-not-team |
| S10 | 16-18 runbooks | INC 01–30 corpus | write 3am runbooks | symptom-first, discriminating-first-check, one-action prevention | playbook that beats the family test; ceiling personal |
Card rule: if you cannot deliver the card's four beats from memory at tempo, the card is a crib sheet — the round is scored on the spoken beats, and a filled card that does not translate to speech is the round's first MUST FIX.

**THE RECORDED-PROBES TABLE (fill during the round; the interviewer's three probes and your three answers, one row per STAR):**
| # | Bullet | Probe 1 / your answer | Probe 2 / your answer | Probe 3 / your answer | Downgrade said? |
|---|---|---|---|---|---|
| S1 | 16-01 CI/CD | maintained-nights? / ran-and-fixed-in-controlled-env | #deploys-week / one every staged run, one debug cycle | my traffic tomorrow? / not until a week at your scale | yes / no |
| S2 | 16-03 Terraform | module wraps what / VPC+IAM+pinned-provider sets | state by hand / lock item read (INCIDENT 22) | plan-says-destroy / address drift, state mv — never hand-edit (INCIDENT 23) | yes / no |
| S3 | 16-06 security | threat / secret leak + eval order | IAM eval / deny beats allow, identity AND resource | secret in git / rotate-clean-history-scan-verify order | yes / no |
| S4 | 16-07 bash | vs one-liner jq / exit-code contract | curl hangs / bounded timeout, --fail, then fail loudly | fail loudly / set -euo pipefail + explicit nonzero | yes / no |
| S5 | 16-08 git | your mistake / yes, named first | exact commands / reflog find, branch-restore, no force-push | why not force-push / attribution + team smell | yes / no |
| S6 | 16-09 incidents | what page / INC 02 empty-endpoints, timeout-class | then who / me + doc walk | live hours / retraction: controlled-env, no live rotation | yes / no |
| S7 | 16-12 networking | which layer / refused=RST, timeout=silence | separating layers / listener→target→target-health before SG | LB vs app / target-health decides; refusal means something answered | yes / no |
| S8 | 16-14 cost | exact line item / over-allocated request = unused nodes | math before/after / requests-allocation arithmetic | right-sized metric / utilization-based trigger, approved change | yes / no |
| S9 | 16-16 ownership | who reported / no direct reports stated at once | decision yours / tool choice, teardown rule | keep "led" / cut it live: "owned a slice" | yes / no |
| S10 | 16-18 runbooks | which incident first / highest-traffic + accidental-429 family | finished bar / 3am bar: symptom + first discriminant check | first step wrong / centralize + drill to keep honest | yes / no |

Scoring rule: a "no" in the last column on any row where the interviewer fired all three probes = a MUST FIX; the downgrade must arrive no later than the third probe. Two or more "no"s and the round's follow-up-defense axis caps at 5.

**ONE MORE FULL VERBATIM — S2 (Terraform, hands-in-state) — the second philosophy a behavioral interviewer loves:**
Interviewer: "Your module set — what did one of them even wrap?"
Candidate: "The smallest useful unit this time: a workload module that wraps the compute, the IAM for it, and the network bits it needs — inputs as a tight schema, outputs as connection data. It plans clean and fails loudly on drift."
Interviewer: "A colleague edited state by hand. Walk me through you knowing, and then doing."
Candidate: "Plan shows the tell: Terraform wants to destroy a resource I never touched — that is address drift. I would not panic and not hand-edit: read the lock first — if the plan is mid-city because a plugin blew up mid-apply, the DynamoDB lock item tells me who and when (that is INCIDENT 22's lesson), then I confirm no live run, then I write it down — and the fix for a genuine address drift is `moved` or `state mv`, which tells Terraform 'these are the same object', not recreate."
Interviewer: "Honest one. Plan says destroy for something you did not touch. FIRST thing you check?"
Candidate: "First thing: is the STATE file the one I think it is — the backend path and a fresh pull. A destroy-line from address drift is a state problem; a destroy-line against a healthy plan is an import problem. I check the state provenance before I check the code, because the code was fine yesterday."
The pattern to copy: the answers stay on the state layer (lock item, moved, provenance), never "let it recreate" — and every probe is answered from the SAME mental model. This is how S2 earns the depth-axis 8 with zero infrastructure theater.

**THE S2 DOWNGRADE PRESS — WRONG VERSUS RIGHT (the hostile turn between lines 1187 and 1198, both ways):**
WRONG reply: "Actually I have done on-call before, I just don't usually lead with it…" Graded: the interviewer's "honest one" was a trap-test and the reply escalated the claim under pressure — exactly the lie-detector workflow; every follow-up probe now re-tests the inflated claim, and the STAR collapses when the clock runs out.
RIGHT reply: "That phrase 'owned' — I overcarried it. The honest verb is 'narrated': method run on a real incident in a controlled environment; the pager rotation I have not owned, and I will not defend a claim past OPERATED." Graded: the downgrade lands BEFORE any contradiction is proven, converts the trap into calibration, keeps the STAR's evidence (method + family) intact, and the interviewer's remaining probes test the story — not the honesty.
Rule: when a behavioral interviewer says "honest one" or "be straight with me" it is a calibration probe, not a pep talk. The downgrade-reflex table exists for exactly this sentence — and the RIGHT reply is the reflex fired unprompted.

**THE S5 ROTATION STAR, VERBATIM (bullet 16-10 security-family — the evidence-anchored one, with FOREIGN-PROBE defense):**
Interviewer: "Your resume says you have done credential rotation. What exactly did you rotate, and what made it a rotation instead of a reset?"
Candidate: "Situation — the security phase of the war-room (11-security), a controlled share. Task — rotate a database credential end-to-end, not reset it: push a NEW secret, re-point production to it, verify, then retire the old one — rotation is a lifecycle, a reset is replacing one static value with another static value." Interviewer: "The order." Candidate: "Foreign-probe order: first the APPLICATION's new credential is rendered as the new value in the secret store; second the config re-points to it; third the app reconnects with it; fourth the OLD one is revoked — revoke-before-point is the outage, point-before-revoke is the window where two valid secrets live in parallel. I would state the order as 'new-first, retest, then old dies' and verify with the same connection we use in monitoring." Interviewer: "Who approved, and the lesson outlived?" Candidate: "The resecure was the lesson: rotation before history — a rewritten secret whose old value still lives somewhere is theatre; and the contract that outlives is 'the order is the security, before the value is'". 
Graded beats: rotation defined as ORDER (the interview-trapped answer is "I changed the password", because that was a reset); the foreign-probe "the order" was answered with a four-step sequence, not a philosophy; and the closing rule (the order IS the security) is the generalization the debrief probe wants.
STAR-rule: any security claim on 16-resume-defense must be narratable at THIS depth, because security-phrase interviews have exactly one question — "the order" — and the mock's hostile exchanges are its rehearsal.

**ONE FULL VERBATIM HOSTILITY EXCHANGE (S6, the on-call question — the hardest minute of the round):**
Interviewer: "Tell me about a production incident you owned."
Candidate: "The one I'd defend first is an empty-endpoints case. A service resolved but every client timed out — quiet timeouts, no refused connections. My scope was one service."
Interviewer: "You keep saying 'owned'. What page fired, what time, what was on your dashboard?"
Candidate: "Honest calibration: I'm going to use 'narrated' where I did not live-pager. What I own is the method and the incident family, not the rotation."
Interviewer: "So no actual on-call. Then what was 'owned'?"
Candidate: "That editing is exactly the defensible claim. Owned = I ran the full method on a real incident replic: endpoints first, selector mismatch on the headless selector, two label lines fixed, then the in-cluster probe proved traffic landed. That's a true STAR; 'owned a live page' would be a false one — and you'd catch it."
Interviewer: "Fine. What would have caught it BEFORE your endpoint read?"
Candidate: "A zero-byte-endpoints alert — the same alert I put on replicas. That is the prevention sentence I stand behind."
The method to copy: each probe was answered with a calibration sentence ("I'm going to use 'narrated'..."), not a deflection; the downgrade was offered before the demand; the final answer stayed on topic and added a prevention. That is a 9 on follow-up defense and a 9 on production judgment with ZERO live-on-call hours — the downgrade is what earns the score.

**LIE-DETECTOR SPOT-CHECK (5 phrases from the file-16 list and where this round must defuse them):**
| Phrase | Where it appears in the round | Defuse line |
|---|---|---|
| "I used X in production" | S1, S6 | "Controlled environment with a live leg — 'production' would be overclaiming; replace with 'fleet-scale' and I can't prove it." |
| "I led the team" | S9 | "'Owned a technical slice end-to-end, no direct reports' — 'led a team' is a different claim and I'm not making it." |
| "on-call experience" | S6 | "Narrated incidents on a 30-incident playbook, not a live rotation; I will not manufacture hours." |
| "Designed the architecture" | S3, S8 | "The architecture is fully documented across the war-room set; the ceiling for the infra pieces is DESIGNED for the controlled scope." |
| "saved the company money" | S8 | "I show reproducible math from measured allocations — I do not claim P&L impact I cannot verify." |
If any of the five phrases left your mouth without the defuse line, that STAR failed the axis and the row should be re-run in 24 hours.

**THE DOWNGRADE-REFLEX DRILL (rehearse the four shapes until they are reflexes):**
| Shape | Template | Used on |
|---|---|---|
| Recalibrate the verb | "Owned = ... / 'managed' would be overclaiming" | S1, S6, S9 |
| Cut the scope line | "I have not <senior activity>; the claim I'll defend is <smaller claim>" | S3, S8 |
| Refuse the invented number | "I don't have that figure — I can show you the reproducible math" | S8 |
| Convert to a prevention | "That gap is exactly why I'd add <monitor/gate> — that's the honest lesson" | S7, S10 |
Drill once a day for a week with a metronome on the word "downgrade": the reflex must fire within one second of hearing "honest answer" or "well-actually".

**ROUND 4 VARIANT B — STAR-ONLY, NO RESUME (the honest-mapping interview, 45 minutes, zero paper in front of you):**
The variation: the interviewer never references the resume at all. Every question arrives as a pure behavior stem ("Tell me about a time you had to say no in a change review" / "…you debugged something you had never seen" / "…you broke something in a shared environment"). You answer with the SAME ten STAR skeletons — but the anchors must be held in the head, not read from a card, and claim levels must be offered unprompted because there is no resume line for the interviewer to police. The scored shape: that the five cemented stories (09-cicd pipeline, 08-terraform workspace, 11-security rotation, INCIDENT 27, INCIDENT 04) survive without their prompts; that "this is the OPERATED-level one, this one is UNDERSTOOD" arrives before any probe forces it; and that the downgrade reflex fires faster, because the resume crutch is gone. A variant run is the correct test BEFORE the real interview — the real panel may indeed hold your resume, but ten minutes of it is us operating as if paper does not exist.
Variant rule: every OTHER run of ROUND 4 is the STAR-only variant. A candidate who only rehearses with a resume visible will have one intact weapon at the panel; the variant is what burns the crutch while the stakes are zero.

**SCORE TABLE (7 axes):**

| Axis | /10 | Why |
|---|---|---|
| Technical accuracy | | Every STAR's technical inside (state-lock, evaluation order, reflog, target-health first) is a real war-room mechanism. |
| Reasoning & structure | | STAR order held under twisting; downgrades arrived BEFORE the third probe most of the time. |
| Communication | | Answers compress to the anchor + the number; no drama, no blame-shifting, no rehearsed heroics. |
| Depth & nuance | | S2's state story and S8's refusal to invent a billing figure are the two depth tells. |
| Follow-up defense | | Third-probe answers did not contradict first-probe answers — the consistent-claim test. |
| Production judgment | | The on-call retraction (S6) and the "led" cut (S9) are the two production-judgment moments the interviewer grades hardest. |
| Uncertainty handling | | Every S ends on a claim-level, not a bluff; a clean "I don't have that number" scores 8+. |

**REFLECTION (fill after):** _what I said_ — transcribe S6 and S9 verbatim: those two upgrades/downgrades are the whole round. _where I froze_ — the third probes demanded a number or a cut; did you stall or produce? _where I overclaimed_ — list every bullet where you defended past 16 claim-level; the downgraded sentence you rehearse next is the one for that bullet.

**MUST FIX / SHOULD FIX / NICE TO HAVE:**
| MUST FIX | SHOULD FIX | NICE TO HAVE |
|---|---|---|
| Any STAR without a S/T/A/R structure visible to the interviewer | Downgrades arriving only after the third probe (move them earlier) | Served-version / same-artifact story reused from Round 3 to 16-01 |
| "production" / "led" / "managed" said without the file-16 rewrite ready | Invented numbers of any kind (S8 trap) | Reflog story told with exact commands ST-FULLY (S5) |
| An on-call claim without the S6 public retraction | Two answers contradicting each other across S1–S10 | The incID-family first-check runbook pitched in S10 |
| No evidence anchor per answer | Awarding yourself a 7 on follow-up defense with any retraction needed | Closing every answer with one "that is my claim-level" line |

### QC CHECKLIST — ROUND 4
| # | Check | Status |
|---|---|---|
| 1 | Exactly 10 STAR blocks, each with a hostile 3-probe twist chain | PASS |
| 2 | Every block cites a real 16-resume-defense bullet (16-01/03/06/07/08/09/12/14/16/18) | PASS |
| 3 | Every block carries an explicit honest-downgrade decision | PASS |
| 4 | STAR evidence anchors are real sessions (09-cicd, 08-terraform, 11-security, 04-bash, 03-git, 12-troubleshooting INC 02/04/15/30) | PASS |
| 5 | Lie-detector traps (led/managed/production, on-call) are triggered and defused in round | PASS |
| 6 | Score table has exactly the 7 axes | PASS |
| 7 | Reflection section with blanks present | PASS |
| 8 | MUST FIX / SHOULD FIX / NICE TO HAVE present | PASS |
| 9 | No emojis, no placeholder wording, fences balanced in this round | PASS |
| 10 | Time budget totals ≤45 min (10 answers × ~3–4 min + grading) | PASS |
| 11 | The round forces at least one public claim-level downgrade per run | PASS |
| 12 | Answers remain defensible at 16 claim-levels (no drift into fabrication) | PASS |
| 13 | SELF-VERIFY — model answers are sourced from the real sibling sessions (FT/chain/incident IDs resolve) | PASS |

VERDICT: **ROUND 4 COMPLETE.** The behavioral resume strike. The score you want to watch is follow-up defense plus production judgment: a candidate who self-cuts 'led' and 'production' before being cornered beats a candidate who never says a wrong word but never admits a fence.
NEXT POINTER: ROUND 5 is the hybrid marathon — the same material, compressed into one timed flow with a metronome, exactly like a real stacked interview loop.

---

## ROUND 5 — H · 90min · Hybrid marathon

**SCENARIO BRIEF:** The final-round loop, three interviewers rotating across 90 minutes with no breaks: a platform engineer firing broad technical questions, an on-call lead who wants a narrated debug, and a hiring manager who wants one honest behavioral story. The interviewer ring-fences each act: when the clock moves onto the next act you stop and switch topic — no carry-over, no "as I said in the last answer". The marathon trains clock-switching, which is how real loops feel.

**OPENING PROMPT (say verbatim):** "Four blocks, ninety minutes, I'm timing each one. When I say move on, you drop the topic mid-word and take the next question. First block: quick technical, keep the answers tight."

**ACT 1 — T · rapid-fire technical (clock 20 min) · FT set**

**S1 — Docker exit 137 (clock 2.5 min) · FT-103**
Interviewer: "A container died with exit 137 — host OOM or cgroup OOM, and how do you tell apart?"
Model answer: 137 = 128 + 9 = SIGKILL. Two killers with different domains. Command first: `docker inspect` .State.OOMKilled — true means the OOM machinery killed it. Then host vs cgroup: host-level line in dmesg/journald reads "Out of memory: Killed process"; the container-limit kill reads "Memory cgroup out of memory"; `free -h` before/after — if the host had available memory, the cgroup limit did it. In Kubernetes the same state shows as exit 137 with reason OOMKilled. And the trap: 137 with OOMKilled=false is a force kill — docker stop timeout or an external kill — memory was not the cause.
Scoreable points: 137 = SIGKILL; OOMKilled bool first; host-vs-cgroup split via dmesg + free; the false case named.

**S2 — DNS four classes (clock 2.5 min) · FT-108**
Interviewer: "Walk DNS resolution and name the four failure classes."
Model answer: app → stub resolver (/etc/resolv.conf) → recursive resolver → root → TLD → authoritative → cached by TTL. Four classes: NXDOMAIN (the name provably does not exist — authoritative answer); SERVFAIL (recursion failed — authority unreachable or delegation broken); timeout (no response — resolver unreachable, lossy path, firewall); and NOERROR-but-empty, NODATA (the name exists but has no record of the type you asked — asking A on an MX-only name). The distinction that kills candidates: NXDOMAIN says the name is gone, NODATA says the type is missing.
Scoreable points: the resolution flow; all four classes named; NXDOMAIN-vs-NODATA distinction spoken.

**S3 — curl health gate (clock 2.5 min) · FT-117**
Interviewer: "Write me a health gate in spoken curl: retries, fails loudly, exits nonzero."
Model answer: bounded everything: `curl --fail --silent --show-error --connect-timeout 5 --max-time 15 --retry 3 --retry-delay 2 -o /dev/null http://<host>/healthz` then assert the payload with jq if JSON, and the script's exit code is the gate: a FAILED gate exits nonzero and prints the status line — `|| { echo "health gate failed"; exit 1; }`. `--fail` makes curl return an error on HTTP >= 400 instead of silently shipping the body; `--retry-all-errors` handles connect flaps; the bounded timeouts stop a hung endpoint from hanging the pipeline.
Scoreable points: fail-on-4xx semantics; bounded timeouts; the "exit code is the verdict" contract; loud message before exit.

**S4 — S3 (clock 2.5 min) · FT-123**
Interviewer: "S3 — consistency, storage classes, versioning, presigned URLs. Thirty seconds on each."
Model answer: consistency — strongly consistent reads/writes since December 2020, so a PUT is a GET-visible object immediately. Classes — Standard for hot data, Standard-IA for infrequent access at a lower storage price with retrieval fees, Glacier/Deep for archive where latency to retrieve is the trade. Versioning — keeps prior object versions against accidental delete/overwrite; combine with lifecycle to expire. Presigned URLs — a time-boxed URL minted by any principal with the right permission, granting access without exposing credentials; used for uploads and temporary downloads.
Scoreable points: strong-consistency date called correctly; class trade-off by access pattern; versioning-as-safety; presigned = delegation with expiry.

**S5 — requests vs limits (clock 2.5 min) · FT-138**
Interviewer: "Who schedules on requests and who enforces limits — and why did my pod get OOMKilled?"
Model answer: requests are the scheduling contract — the scheduler sums requests against node allocatable and does not read your limits. Limits are the runtime ceiling, enforced by the kubelet through cgroups: CPU over limit throttles (CFS quota), memory over limit KILLS — that is your OOMKilled with exit 137. QoS classes rank eviction under node pressure: Guaranteed (requests == limits) survives the longest, BestEffort goes first. The two classic mistakes: limits without requests (a pod reserves more than it needs; the scheduler sees nothing) and no limits at all (a runaway pod eats the node).
Scoreable points: scheduler-vs-kubelet split; CPU-throttle-vs-memory-kill; QoS ordering; the two classic mistakes named.

**S6 — count vs for_each (clock 2.5 min) · FT-147**
Interviewer: "count or for_each — and what breaks when you switch?"
Model answer: for_each over a map/set of stable keys; count over a plain list whose addresses are INDEX-based. The breakage: removing an element in the middle of a count list recycles index 0, so Terraform plans DESTROY+CREATE on the shifted elements — `by_count[1]` switching from element b to c gets rebuilt while its for_each twin remains untouched. Access forms differ (`values(...)` and `{ for k, v in ... }` for for_each) and data sources refresh every plan. For renames use `moved` blocks / `state mv`, never "let it recreate".
Scoreable points: the index-stability mechanism; the destroy+create consequence; moved/state mv for rename; data-source refresh caveat.

**S7 — RED vs USE (clock 2.5 min) · FT-155**
Interviewer: "RED or USE — which one answers which outage question?"
Model answer: RED = Rate, Errors, Duration — the user-visible service view: is my service getting requests, failing, slow? USE = Utilization, Saturation, Errors — the resource view: is my CPU/disk/network busy, queued, erroring? They answer different questions: RED tells you a service is degrading; USE tells you which resource is the bottleneck underneath. An outage usually starts in the RED numbers and ends in a USE read — high USE saturation explains the RED error budget, so I always triangulate: RED first (what the user sees), then USE down the dependency.
Scoreable points: both methods decoded; the different questions each answers; the RED-then-USE triangulation as production judgment.

**S8 — Parameter Store vs Secrets Manager (clock 2.5 min) · FT-158**
Interviewer: "SSM Parameter Store or Secrets Manager — pick by rotation need."
Model answer: Parameter Store is cheap, lightweight, great for config and non-rotating values; Secrets Manager is the pick when a secret must have lifecycle and rotation — managed RDS-credential rotation, versioning of secret values, granular recovery windows. Decision rule: if the value rotates or is a real credential, Secrets Manager; if it is configuration a pipeline reads, Parameter Store. And both get encrypted where it matters — the rotation axis is the differentiator, not the price.
Scoreable points: the rotation axis named as the decision; credential-vs-config classification; no hand-waving at price.

**ACT 1 SECOND PASS — the rapid-fire follow-up one-liners (drill so the marathon's act-1 never wobbles on probe two):**
| From | Likely second question | Model one-liner |
|---|---|---|
| S1 (137) | "137 with OOMKilled=false — what is it?" | Not memory: docker stop timeout or external kill — SIGKILL from a different actor. |
| S2 (DNS) | "Flapping between results — which of the four classes?" | None exactly — that is load-balanced servers with different views, or stale cache churn; NXDOMAIN is consistent, flapping is infra. |
| S3 (curl) | "Why --fail and --retry together, not one?" | --fail converts 4xx/5xx to error exit; --retry re-attempts connect flaps — one measures the app, the other the network. |
| S4 (S3) | "Versioning + who pays the storage?" | Every version costs real storage; lifecycle expiry is the trim valve, and the cost is yours before the audit. |
| S5 (requests/limits) | "Overcommitting nodes — who can start anyway?" | The scheduler overcommits beyond allocatable when pods request less than node cap; bankers is the admission control cold path. |
| S6 (count/for_each) | "Renames — count or for_each?" | Neither: `moved` / `state mv` tells Terraform the same object; recreating a database is not a rename. |
| S7 (RED/USE) | "Which first at 3am — I have one screen?" | RED first (what users see), then USE down the dependency for the WHY — one screen starts with the error-rate panel. |
| S8 (SSM) | "Encryption everywhere, or only for Secrets Manager?" | All of it: a config value is still a credential if it holds a host/port/token; KMS-backed SSM on the sensitive keys. |
Scoring rule: 0.5 pt if the one-liner lands inside the clock, full 1 pt if it also names WHY the first answer still holds (no retraction). This second pass is where the marathon separates breadth from speed.

**ACT 1 SCRAMBLE BANKS (two alternate 8-question sets so the marathon does not go stale — swap them in on re-runs):**
BANK A: (1) FT-106 CIDR hosts in a /27; (2) FT-119 IAM roles vs users temporary-creds; (3) FT-130 CMD vs ENTRYPOINT and overrides; (4) FT-136 what a Deployment does on rollout undo; (5) FT-144 why state is a single point of truth; (6) FT-149 Continuous Delivery vs Deployment trigger; (7) FT-107 connection refused mechanisms; (8) FT-155 USE saturation signal.
BANK B: (1) FT-105 octal 1754 file vs dir semantics; (2) FT-109 301 vs 302 vs 307; (3) FT-117 curl --max-time vs --connect-timeout; (4) FT-122 ALB target-health first move; (5) FT-137 liveness vs readiness consequence; (6) FT-145 S3+DynamoDB backend locking; (7) FT-150 same-artifact promotion; (8) FT-158 Parameter Store rotation decision.
Scramble rule: on every re-run, replace the ACT 1 set with a bank (or mix both banks). A marathon repeated with the exact same questions measures memory, not the muscle — the discussion that follows each run is what compounds.

**ACT 2 — R · narrated mini-debug (clock 20 min) · source: 12-troubleshooting INCIDENT 02**
Interviewer: "Service `web-svc` resolves fine in the cluster but every connection hangs or refuses. The pods are Running. Walk it aloud — I want to hear you think."
Model narrated answer (phases timed in your head): symptom read — resolve-WORKS-connect-fails is the signature of this whole class: DNS and traffic are two different systems with two different sources of truth. Scope — one Service object, everything else in the namespace healthy: that confinement is itself diagnostic, since a whole-cluster network fault cannot pick out a single Service. Hypotheses ranked: (1) empty endpoints — selector matches no pods, most common by far; (2) pods running but not Ready — readiness gate keeps the endpoint list empty (INCIDENT 20 machinery); (3) wrong targetPort — endpoints populated but pointing at a port nothing listens on, refused at the pod; (4) NetworkPolicy blocking; (5) kube-proxy rules stale — rarest, diagnosed by elimination. Checks in order: `kubectl get endpoints web-svc` (the <none> answer rules in selector/readiness); `kubectl get svc web-svc -o wide` to read the SELECTOR; `kubectl get pods --show-labels` to compare; then an in-cluster probe `kubectl exec dnsprobe -- wget -T 4 -O- http://<ClusterIP>:80`. Evidence read — the contrast pair: same probe, one variant `Connection refused`, one variant `download timed out`, and after the fix the probe returns the app's real payload. Root cause — selector `app=webtierX` vs pod labels `app=webtier`. Fix + verify with the same probe: endpoints populate (10.244.0.6:8080, ...) and the probe returns content. Escalation — this one never needed it; but if endpoints stayed empty with correct labels and healthy pods, the next hop is the readiness gate, then the data plane, each with a named discriminator.
Narration scoreable points: hypothesis count aloud (5); the object-boundary scope line; cheapest check first (endpoints); readiness-gate branch present (INC 20); verify uses the SAME probe that failed; escalation named with the next discriminator.

**ACT 2 RE-READ — SECOND PASS WITHOUT THE SCRIPT (the retell drill; the marathon's narration muscle is built by retelling, not reading):**
Run the same INCIDENT 02 triage again, but this time from the list of beats rather than the model answer — in your own words, same order: (1) resolve-WORKS-connect-fails = two systems, two truths; (2) one namespace = confinement is the evidence; (3) five hypotheses ranked with the cheapest discriminator; (4) checks: endpoints, selectors, labels, in-cluster probe; (5) contrast-pair proof — refused vs timeout variants, then content; (6) fix + the SAME probe proves it. Re-read rule: if any beat collapses on the retell, the first read was memory, not ownership — re-drill the incident file until the retell holds all five hypotheses and the contrast pair without notes.

**ACT 2 VARIANT B — the same act served with INCIDENT 04 (ALB 502/503) instead of INCIDENT 02, so the narration muscle does not rot on one family:**
Interviewer: "The ALB returns 502/503 to clients on a busy evening; the backend pods are Running. Walk it aloud."
Model narrated answer: "Symptom read — 502 vs 503 are DIFFERENT promises: 502 means the ALB reached a target and the response was invalid; 503 means there was no healthy target to reach. In one command, `describe-target-health` splits it for me, so that is the object I read first, not the SGs. Scope — one target group, one service path; if every target is unhealthy that is our side one way; if targets are healthy and 502s persist, the meaning changes completely. Hypotheses, ranked: (1) health check path or port mismatches what the app serves — the ALB treats healthy-as-dead, 503s; (2) SG blocks the ALB→target:port — targets 'healthy' only because the check is other-sourced, or targets unreachable at the real port, 502s; (3) the app listens on the wrong interface or a different port than the target group states; (4) protocol mismatch — HTTPS in the target group against an HTTP listener; (5) a registered target that never existed (stale registration). Checks in order — `describe-target-health` first (the discriminator, read-only), then the target-group port/protocol, then the SG from the ALB's security group to the target, then the app's actual listener. Evidence — if all targets show healthy but the ALB still 502s, the failure is inside the target's response behavior: reaper on keep-alive closing mid-request, protocol mismatch, or the app crashing per-request — the health check and the real client hit different code paths. Fix + verify — correct the mismatched surface, then the SAME healthy status and a real client request both go green; prevention — the health-check path must exercise the same path clients hit, the same contract as the INCIDENT 20 lesson, plus an alert on target-health-availability so a silent half-dead fleet pages instead of surfacing only at evening peak."
Narration scoreable points (same skeleton, different family): the 502-vs-503 promise split in the first sentence; target-health-first as the cheapest discriminator; the "healthy but 502" branch named; the fix verified with the same signal; the prevention reuses the probe-contract lesson across families.
Variant rule: alternate INCIDENT 02 and INCIDENT 04 across marathon re-runs — the narration skeleton is family-agnostic, and rotating families is what proves it.

**THE ACT-2 TRIAGE TEST SET (five mini-scenarios, 3 minutes each, narrated — the breadth drill for the narration muscle):**
| # | Symptom given | The branch you must open | The discriminator that names the winner |
|---|---|---|---|
| 1 | Service times out; pod Running AND Ready | endpoints targeted (targetPort) vs NetworkPolicy vs proxy | in-cluster probe to the pod IP:port directly |
| 2 | Pod CrashLoopBackOff, restartCount climbing | crash (logs --previous) vs probe-kill vs bad image | last exit reason + log tail under the first fault |
| 3 | ImagePullBackOff, ErrImagePull persists | registry auth vs digest drift vs manifest (multi-arch) | pull events detail; `skopeo inspect` on the reported tag |
| 4 | Node drains and pods reschedule elsewhere | PDB rules-in vs node-affinity vs capacity | get pdb + describe scheduling events on the new node |
| 5 | Perfect cluster, no traffic reaches a Service | Service selector vs label drift vs ingress config | get endpoints <none> vs populated, then ingress resource read |
Each mini-scenario trains one discriminator; all five fit inside a single 20-minute act-2 replacement. A runner who can narrate all five clean keeps the marathon's narration muscle sharp on days the full incident is not available.

**ACT 3 — S · short design (clock 20 min) · scoped prompt**
Interviewer: "Three replicas of your API service, 30 RPS, deploying on every merge. Pick the rollout and the health gate. Five minutes of talking."
Model answer: rollout — rolling update by default. Numbers: 3 replicas, `maxUnavailable: 1, maxSurge: 1`, worst case the service dips to 2 replicas for a moment, never 0; rollback is `rollout undo` (a new revision at the old bytes — FT-136). Health gate — the readiness probe on `/healthz` must mean "can take traffic now": the path the version actually serves, no false 200 before warm; a startupProbe buys a slow-booting process its runway without liveness killing it (FT-137). Bounded waits — `progressDeadlineSeconds: 600` and CI's `rollout status --timeout` so a probe-failing version FAILS the deploy instead of hanging the pipeline with half capacity (INCIDENT 27). Upgrade for this service: since we have a metric feedback loop, a gated canary at 10% checking error rate + p99 for 10 minutes, then ramp — canary fails → weight to 0 (FT-152). Deploy must end on a served-version smoke: the response body identifies the version, so a "green" pipeline that actually rolled stale bytes is caught (INCIDENT 29). Rollback rule locked in: bytes intact in registry and no schema migration rode in, else forward-fix (INCIDENT 28).
Scoreable points: pick-by-failure-cost; probe contract tied to traffic-readiness; bounded rollout waits; canary gate metrics; served-version verify; the rollback bytes+migration test all inside 5 minutes. Re-run rule: rotate the act-3 prompt between this and VARIANT C below so the short design generalizes past one scenario.

**ACT 3 VARIANT C — the cron-writer short design (the same 20-minute act on a scheduled workload, scored with the SAME rubric):**
Interviewer: "One hourly job writes a small report file. Never lose a run; never double-write. Pick the scheduler and the retry. Five minutes of talking."
Model answer: shape — a scheduled one-shot, so CronJob is the honest primitive and a queue is the wrong answer unless the consumers are decoupled (they are not); concurrencyPolicy Forbid is the default because the two hazards are losing a run or double-writing, and Forbid kills the collision class outright; historyLimit bounded so a noisy week does not accumulate failed pods; the file is small, so no PVC until the design proves persistence is required — and if it is, the PVC lifecycle becomes a named decision (Retain + a bucket copy), not an afterthought. Failure language — if the job fails, the cron tick alone is NOT the retry story: the alert pages, the next tick retries, and for a never-lose promise I add a backfill check that scans for the missing hour and re-writes idempotently (same hour lands one file). Retry policy — the honest default is zero CrashLoop backoff-magic: one bounded retry inside the job, then human escalation; and the typed sentence is idempotency as the senior move — "write-then-move under the same hour key", so retries are safe by construction. Ceiling — "I have OPERATED Deployments; a production CronJob fleet is UNDERSTOOD; my kind prototype ran a real daily job against a real object store."
Scoreable points: the queue-vs-scheduler elimination in the first sentence; Forbid as the collision-class kill; the failure-language split (tick vs backfill vs human); idempotency stated as a design line, not a wish; and the claim ceiling offered, exactly as the act-3 primary demanded.

**ACT 3 FOLLOW-UP PROBES (the interviewer's five design presses on the 3-replica answer, with the model beat):**
| Probe | Why fired | Model response beat |
|---|---|---|
| "3 replicas and canary at 10% — that is 0.3 of a replica; why would you ramp at all?" | tests whether canary math is real or quoted | Because the canary measures SIGNAL, not coverage — error rate against the 90% baseline at 10% is statistically honest at 30 RPS; and if the users split evenly the surprise is still contained to a tenth of traffic. |
| "maxUnavailable 1 on 3 — which replica is down during the swap?" | capacity-floor discipline | My floor is "never below 2 of 3"; the down replicas are the ones already drained, and the surge keeps headroom while the new pod readies. |
| "What if the readiness probe is warm but the app breaks on the first real request?" | probe-contract depth | Then the probe did not exercise the traffic path — the correct probe hits the same code the client hits, and the canary analysis exists precisely to catch the warm-but-broken case over 10 minutes. |
| "/healthz on the new version — who owns that contract?" | boundary honesty | Jointly: the app team owns what readiness MEANS, the platform team owns the probe mechanics — and the CI smoke makes the contract machine-checked so it cannot rot silently. |
| "progressDeadlineSeconds 600 — why not always wait?" | bounded-wait judgment | Because a "hanging" pipeline is a half-capacity state by design; the bound converts it into a loud failure that pages, and the page is cheaper than the silence. |
Every probe is answered from the SAME S6 picks — the design does not wobble because the interviewer pressed it, which is the entire grade of this act.

**ACT 4 — B · one honest behavioral (clock 10 min) · source: 14-attack-chains 14-14 (L1 arc)**
Interviewer: "Tell me about a time a system broke and you found out late."
Model answer (the 14-14 L1 shape, three beats): CALIBRATION — the wrong-branch `git reset --hard` story: I found out when the working tree did not contain the work I expected, measured as a missing commit in `git log` and a filesystem diff against my last known state. NARROWED CAUSE — the single confirming probe: `git reflog` showed the pre-reset HEAD; the reset had re-pointed the branch. RECOVERY — restored the commit onto a branch, verified the tree against the intended state file-by-file, and the rule that came out of it became a permanent habit: reflog is the undo button, force-push is a last resort, and I now snapshot the expected state before any destructive operation. Ownership stated first: this was my mistake and my repair. No number invented; the evidence has a name (reflog), a command, and a verified outcome.
Scoreable points: ownership before mechanism; one calibration metric; one layer-confirming probe; the rule extracted; no fabricated heroism.

**ACT 4 ALTERNATE ENDING (for the interviewer who presses "but what did the TEAM lose?"):**
Pressing line: "One branch, one session — who else felt it?"
Alternate: "Nobody felt it operationally — that is the honest blast radius, and I keep it small because the point is the calibration. What the team lost was a few minutes of my fix, and what it GAINED was a rule written into my playbook and a PR gate the whole repo now enforces: reflog-as-undo, force-push-last-resort, snapshot the expected state before any destructive git. That is the same shape as the mis-commit incident: the harm was small, the correction is permanent, and I report the small harm before the permanent rule." 
The scored beat: the refused-heroism — no inflated impact invented, no "the sprint was saved" filler. The interviewer hears a candidate who trusts the SMALL honest story, which is the one real teams believe.

**INTERMISSION — THE CLOCK MAP (the marathon's 90 minutes, so clock-switching has a grid):**
| Block | Clock | Topic bucket | Switch cue to listen for | Failure sign if you violate it |
|---|---|---|---|---|
| Act 1 | 0–20 | 8 rapid-fire technical (FT) | "Keep them tight" → each ends at the money line | answer spills past its 2.5-min into the next question |
| Act 2 | 20–40 | narrated mini-debug (INC 02) | "Walk it aloud; I want to hear you think" | you go silent anywhere past 60 s |
| Act 3 | 40–60 | short design (rollout + gate) | "Five minutes of talking" | you reopen Act 1 topics instead of deciding |
| Act 4 | 60–70 | one honest behavioral (14-14) | "Full arc, please" → STAR beats, no heroics | you dodge the ownership opener |
| Grading | 70–90 | act scores + full debrief | — | you skip transcription; the round then teaches nothing |

The tactical rule: when the interviewer says "move on", you stop — even mid-word — because the graded behavior is the SWITCH, and a half-finished correctness point outranks a finished wrong one.

**THE MICRO-REST ROUTINE (the marathon's act-breaks are 30 seconds — this is what those 30 seconds are FOR, not a stretch):**
| Moment | What the 30 s buys | The one action that spends it well |
|---|---|---|
| 20:00 (after act 1) | frequency reset — leave the rapid-fire register | close the eyes, breathe four counts, then name the next act's first beat aloud ("symptom-read first") |
| 40:00 (after act 2) | tone reset — leave narration register | two-word self-check: "scope held?" then the act-3 decision posture |
| 60:00 (after act 3) | honesty reset | replay the LIE-DETECTOR one-liner once, then enter act 4 in "own-beat-repair-rule" mode |
| 80:00 (after act 4) | loop reset | the elevator backbone once, silently, so the close echoes the open |
Micro-rest rule: the breaks are register-switches, not recovery — a marathon fails when act 3 is answered in act 2's cadence. Naming the next register aloud in the first two seconds of the break is the entire skill.

**THE ACT-SCORED SNAPSHOT (fill each act before the overall table; the four-muscle heatmap):**
| Act | Muscle graded | Self-score /10 | Weak-muscle signal | Where it will also show up |
|---|---|---|---|---|
| 1 (T) | breadth + exactness | | any FT scored < 4 (drill via FT follow-up loop) | ROUND 1's rapid-fire |
| 2 (R) | narrated method | | hypothesis count under 5, or 60-s silence | ROUND 2's whole round |
| 3 (S) | decision density | | missing served-version verify or bounded wait | ROUND 3 S7/S9, ROUND 6 S2 |
| 4 (B) | honest calibration | | ownership not stated first, or a number invented | ROUND 4's downgrade reflex |
Rule: a score ≤ 4 in any act is not a "bad marathon day" — it is the same muscle failing in rounds 1/3/4/6. The snapshot is how the marathon makes the pattern visible instead of mood.

**INTERVIEWER LOB FOLLOW-UPS (the hostile pushes each act gets, with the model beat):**
| Act | Lob | Why it is fired | Model response beat |
|---|---|---|---|
| 1 | "You said S3 standard access in 2026 — cite the consistency date or drop it." | Exactness under pressure | "December 2020 — S3 is strongly consistent now; I quoted the transition because the class-level trade-off is historical, not current." |
| 2 | "You chose endpoints as check one. What if endpoints looked FINE?" | Tests the branch-after-proof | Then the split moves to targetPort — pod IP:port vs what listens — via an in-cluster probe; the readiness gate (INC 20) and the data plane follow in order. One <none> rule-in answer justifies the order; a wrong-for-this-round answer is checked next. |
| 3 | "3 replicas, maxUnavailable 1 — so you're OK with 2 for a moment?" | The capacity-floor exactness | Yes and it is the honest answer: the wrong claim would be 'zero downtime'; my claim is 'never below 2 of 3', with the surge pod padding the trade. Stating the floor IS the scoring move. |
| 4 | "That reflog story — how many people were affected while it was broken?" | Heroism-vs-reality | "One engineer, one session, a fraction of a day: it was my mistake on my own branch state — the honest size of the blast radius is part of the calibration." |

**THE ANSWER SHAPE PER ACT (the skeleton every marathon answer fits; write each answer into its own shape on the run):**
| Act | Shape | Line-by-line skeleton |
|---|---|---|
| 1 (T, 2.5 min each) | ANSWER → PROOF → NEXT | name the mechanism → one exact fact/number → the one command/check the interviewer would run next |
| 2 (R, narrated) | READ → SCOPE → RANK → CHECK → EVIDENCE → FIX → VERIFY | follow the FT-160 skeleton; hypothesis count aloud |
| 3 (S, 5 min) | DECIDE → COUNTER → BOUND | pick strategy by failure cost → say why not the obvious alternative → name the wait/limit/margin |
| 4 (B, full arc) | OWN → BEAT → REPAIR → RULE | ownership first → calibration beat → recovery steps → one permanent rule |
Rule: any act-1 answer longer than three lines loses the shape; any act-3 answer without a "why not" loses the depth; any act-4 answer without the ownership opener on the first line loses the behavioral axis entirely.

**MARATHON DEBRIEF — what the three interviewers say in the hallway, and the round that produces each sentence:**
| Hallway sentence | The behavior it maps to | Which act earns it |
|---|---|---|
| "Tight loop, knew her baseline" | act-1 answers at money-line without drift | Act 1 |
| "Actually narrated — rare" | continuous out-loud method, wrong-for-this-incident branches named | Act 2 |
| "Made the call, priced it" | decisions with the cost + the why-not exposed | Act 3 |
| "Knows what a claim is" | ownership first, honest blast radius, no heroism | Act 4 |
If the debrief cannot produce all four sentences from your tape, the missing sentence names the act that becomes the MUST FIX — and re-drill it against its sibling file (15-question-bank for 1, 12-troubleshooting for 2, 09-cicd for 3, 14-14 for 4).

**ANSWER-VELOCITY DRILL (run the marathon on volume first: 90 minutes of questions with NO extended narration, to train the switch and the one-liner):**
1. Set a 90-second metronome. Every time it ticks, the interviewer fires the next question (use the FT set, any 60 rows).
2. The requirement: every answer must END before the next tick — hard cut even at the cost of a half-finished argument.
3. Count three metrics: answers finished clean (A), answers cut mid-sentence (B), answers that leaked into the next tick (C). Score = A / (A + B + C).
4. A score under 0.8 means the ramble-control axis fails before depth even gets graded — run the drill until you hit 0.9+ at steady state.
The drill is the cure for the one failure every marathon-round tape shows: 40-second answers to 15-second questions.

**THE 90-MINUTE EVENT CHECKLIST (the marathon's three interviewers expect a seamless clock — this is the thread):**
1. Before: 30-second eyes-closed recall of the four act shapes (T: answer-proof-next, R: 10-step skeleton, S: decide-counter-bound, B: own-beat-repair-rule).
2. At 20: the hard cut from act 1 — even if a question is mid-answer, the tick wins; the graded behavior is the switch.
3. At 40: act 2 must have opened with the symptom READ and the hypothesis count aloud — the first 60 seconds of the narration decide that act.
4. At 60: act 3 must close with a decision and its counter — never a menu.
5. At 70: act 4 ends on the rule extracted, not the recovery (the recovery is middle material).
6. After: the act-scored snapshot filled in the SAME session, with the weak muscle named.
Event-rule: any act that finished with its hallmark missing (no proof in act 1, no hypothesis count in act 2, no counter in act 3, no rule in act 4) is a re-drill against the sibling file — the checklist converts the marathon from "answered a lot" into "executed four graded shapes".

**THE LAST-FIVE-MINUTES PROTOCOL (a marathon is won in its final five — the graders are comparing your shape at minute 85 to minute 5):**
| Time | The interviewer's real question | What you do (and why it is the point) |
|---|---|---|
| 85:00 | "Anything you want to revisit from earlier?" | REVISIT the act you scored weakest in the act-snapshot, with the corrected beat spoken aloud — the interviewer grades the repair, not the original flap |
| 86:30 | "What would you want the team to know about you?" | the elevator backbone again, three anchors, same order — the close is the open, rehearsed, so the panel leaves with one shape |
| 87:30 | "Any questions for us?" | TWO questions only, both about the role's failure surfaces: the deploy loop's scope, and how a new hire's first incident train works — never "when do I hear back" |
| 89:00 | handshake window | the one-sentence care point that survives the round: "I expect the hardest question today to be about my ceiling — I gave it unprompted and I will take it again tomorrow." |
Protocol-rule: the marathon's last five minutes are the only un-timed material in the file, and interviewers remember them disproportionately. Saying the predictable close is the difference between "technical pass" and "person we could double down on."

**ACT 2 ESCALATION CORRECTNESS CHECK (the INCIDENT 02 ending has an escalation beat — most runs skip it; ensure it lands):**
Question that fires it: "Endpoints are populated, labels are right, probe returns content — but the SAME symptom comes back an hour later. What changed?"
Model beat: one hour later is NOT the same incident — the fix was verified, so I re-open with a changed-hypothesis bias: either the selector drifted again (a code push re-added the label), a SECOND service shares the same selector with different cases (a new app, new labels), or the "same symptom" is a different layer — this time the clock skips endpoints because the first fix did not stick at the source. The escalation rule stays: if the re-open shows breadth (two services, two namespaces), the incident is no longer one-service scope and the wider team gets paged on the object-boundary line I drew at the start.
Scored move: saying "re-open with a changed-hypothesis bias" instead of re-running the exact same checks — an interviewer hears this as the diff between following steps and owning the method.

**THE MARATHON BAND TABLE (act scores → loop verdict — read your four act/scores before the round total):**
| Pattern | Loop verdict | Action |
|---|---|---|
| All four acts ≥ 7 | the stacked loop was clean | hold; move to ROUND 6 the same pass |
| One act ≤ 4, rest ≥ 6 | the identified weak muscle | re-drill that act's sibling file; re-run only that act before R6 |
| Two acts ≤ 4 | not the day; the loop doubles what was weak | go back to single-round mocks; do not book consecutive marathons |
| Act 1 < 4 (breadth) | the FT floor is not automatic | 15-question-bank rapid-fire drills daily, no narration |
| Act 2 < 4 (narration) | the method is not owned | 12-troubleshooting narrated runs against a metronome |
| Act 3 < 4 (design density) | decisions not priced | 09-cicd read-and-decide drills, one decision per sitting |
| Act 4 < 4 (honesty) | the calibration is a costume | 16-resume-defense lie-detector re-grid + STAR re-runs |
Band rule: the act-slice is the truth; the /70 total only summarizes it. A marathon round scored 55/70 with a 3 in act 2 is a narration problem, and the fix is not "more questions".

**THE FIVE WRONG ACT ENDINGS (the last sentence that kills each act — hear it, then end differently):**
| Act | The ending that loses the act | The ending that wins it |
|---|---|---|
| 1 (T) | "…and that's basically how it works, yeah." | The last beat after the last claim: "…so the next command I would type is `ss -tlnp`." |
| 2 (R) | "…so yeah, it was the selector." | The last beat of the narration: "…and the same probe that timed out now returns the payload — the symmetry is the proof." |
| 3 (S) | "…those are the options, any preference?" | The last beat of the decision: "…so stable version with no campaign — not 'simpler', the failure cost decides, and it is zero." |
| 4 (B) | "…and everyone was really glad it worked out." | The last beat of the rule: "…and that PR gate is the permanent difference the incident left behind." |
Ending rule: an act should close on whatever the burden of proof was — a next-move, a verified signal, a decision with its WHY, or a rule that outlives the story. "That's basically it" is the shape of not knowing what you were asked to prove.

**THE CROSS-ACT FEEDBACK MATRIX (when one act fumbles, the OTHER acts usually hid the same weakness in a lighter costume — find it before the interview does):**
| Act you fumbled | Echoes you should already see elsewhere | The interview-serial version |
|---|---|---|
| Act 1 depth (one-liners drained) | R1 rapid-fire same drain; R4 STAR mechanisms thin | the first two questions of the real loop |
| Act 2 narration (order collapsed under pressure) | R2 the same; R6 S3 the same | any incident question when the clock is on |
| Act 3 design (no counter / no price) | R3 S6/S7; R6 S2 the same | "why not X?" — every design interview opens this door |
| Act 4 calibration (owned late) | R4 downgrades late; R6 S4 alternate close missing | the "say it plainly" press |
Feedback rule: the marathon is the cheap rehearsal of the real loop's day, and a weakness that surfaces in ONE act has been wearing three costumes all week. Name the underlying muscle, not the act, or the same fumble relocates to a different question in the real interview.

**SCORE TABLE (7 axes):**

| Axis | /10 | Why |
|---|---|---|
| Technical accuracy | | Act 1: 8/8 questions hit their scoreable points without a wrong claim (137, S3 classes, count-index, RED/USE). |
| Reasoning & structure | | Act 2: hypothesis-count-5 + check-order + object-boundary scope; Act 3 decisions in the fix-cost order. |
| Communication | | Clock-switching obeyed; every act ended when told, answers compressed to the money line. |
| Depth & nuance | | Act 2 readiness branch (INC 20), Act 3 served-version verify, Act 1 NXDOMAIN-vs-NODATA — the bonus facts present. |
| Follow-up defense | | Any act-1 answer that needed retracting in act 3? The same-artifact/digest story must not contradict between S-refs. |
| Production judgment | | Bounded waits, canary gate thresholds, bytes+migration rollback rule, verify with the same probe. |
| Uncertainty handling | | In act 2, on any unknown you name the next discriminator instead of going silent — that is the scoring move. |

**REFLECTION (fill after):** _what I said_ — transcribe act 2 fully (the narration is the whole point of the marathon). _where I froze_ — the clock-switch is the trap; note the act where you tried to finish a sentence after "move on". _where I overclaimed_ — any act-1 answer that needed an act-4-style downgrade.

**MUST FIX / SHOULD FIX / NICE TO HAVE:**
| MUST FIX | SHOULD FIX | NICE TO HAVE |
|---|---|---|
| Act 1 answers longer than the 2.5-min budget (drill with a wall-clock) | Act 2 narration without hypothesis-count-5 spoken aloud | RED-then-USE triangulation in S7 |
| Talking past "move on" (rehearse hard cut-offs) | Act 3 without a served-version verify | Mentioning the gateway NXDOMAIN-vs-NODATA pair |
| Any contradiction between act 1 and act 3 stories | Forgetting bounded rollout waits in act 3 | State-lock/drift crossover from Round 4 reused in S6 |
| Silence in act 2 (name the next discriminator instead) | Number invented in act 4 (calibration must be real) | INCIDENT 20 readiness branch named during act 2 |

### QC CHECKLIST — ROUND 5
| # | Check | Status |
|---|---|---|
| 1 | Four acts present in one timed flow (T / R / S / B) with clock cues | PASS |
| 2 | Eight rapid-fire items cite real FT IDs (103/108/117/123/138/147/155/158) | PASS |
| 3 | Mini-debug is INCIDENT 02 with ranked hypotheses, checks, contrast-pair evidence, and same-probe verify | PASS |
| 4 | Short design covers rollout, health gate, bounded waits, canary gate, rollback rule | PASS |
| 5 | Behavioral block follows the 14-14 L1 three-beat shape with ownership first | PASS |
| 6 | Act-scored snapshot table present so the weak muscle is visible | PASS |
| 7 | Score table has exactly the 7 axes | PASS |
| 8 | Reflection section with blanks present | PASS |
| 9 | MUST FIX / SHOULD FIX / NICE TO HAVE present | PASS |
| 10 | No emojis, no placeholder wording, fences balanced in this round | PASS |
| 11 | Total time budget ties to 90 min (20+20+20+10 + intermission/grading) | PASS |
| 12 | Clock-switch discipline is in the scoring, not just the instructions | PASS |
| 13 | SELF-VERIFY — model answers are sourced from the real sibling sessions (FT/chain/incident IDs resolve) | PASS |

VERDICT: **ROUND 5 COMPLETE.** The marathon. Scores below 45/70 here — or a must-fix bigger than one line — say the war-room stack is not yet defense-ready; re-drill the failed act against its own sibling file before ROUND 6.
NEXT POINTER: ROUND 6 is the final comprehensive — the only round that ends on the elevator and the uncertainty segment, so bring the tightest anchor stories and the honest "I don't know" phrasing.

---

## ROUND 6 — F · 90min · Final comprehensive

**SCENARIO BRIEF:** The real onsite loop, one full day simulated in 90 minutes: an opening elevator, a full design, a live-debug under narration, one behavioral, and — the segment every mock before this skipped — a stretch of questions deliberately aimed past your knowledge, scored on how you handle not knowing. A staff engineer, a product engineering lead, and a hiring manager rotate. This is the round that decides the offer letter's sentence "outside of my hands-on scope" belongs next to "hire".

**OPENING PROMPT (say verbatim):** "Welcome to the final loop. We'll do five segments. First, the floor is yours — introduce yourself, then we will push on the gaps you leave open. And every so often I am going to ask you something I would not expect a 1–3 year engineer to know. The point is to hear how you handle it."

**THE FIVE-SEGMENT SWITCH CHEAT (know at all times which muscle is being graded — the segment is the question):**
| Segment | What is actually graded | The reflex to hold the entire time |
|---|---|---|
| S1 elevator | anchors + honesty contract | never inflate an anchor; the interviewer will probe the strongest |
| S2 design | scoped mechanism + decision order | ask-back first; every decision priced; every number sourced |
| S3 live-debug | narrated method under pressure | P0 posture, three-fact rule, verify-same-signal, deadline announced |
| S4 behavioral | ownership + calibration | first line is ownership; evidence by name; no heroism |
| S5 unknowns | behavior at the knowledge boundary | three-phase shape on every answer, bluff never |
The switch cheat exists because the round's traps hide IN the switches — an answer that would score well as a design decision reads wrong as a behavioral claim, and a three-phase answer wastes its own power in S3 where action beats deliberation.

**S1 — THE 30-SECOND ELEVATOR (clock 1 min) · source: 16-resume-defense THE 30-SECOND ELEVATOR**
Interviewer: "Floor is yours."
Model answer: deliver the file-16 elevator verbatim, in one breath, then stop:
"I'm a DevOps engineer at the 1–3 year mark, and I will not claim deeper than I can prove. My thing is the full delivery spine: I build a pipeline, ship a container, run it in Kubernetes, and watch it — and I have done each step end to end, including breaking it and fixing it. Three honest anchors: I ran a Docker-to-ECR-to-EKS deployment live on AWS and hit a real scheduling constraint I had to fix; I operate a Prometheus and Grafana stack and can explain why I alert on percentiles, not averages; and I train incident response against a thirty-incident playbook where every run ends with a documented prevention. If a bullet on my resume cannot survive your next three questions, I will tell you to cut it myself. Where do you want to start?"
Scoreable points: one breath; three anchors that stand up (each traceable: EKS run AWS.P0.10, Prometheus stack OBS.P0/P2, playbook INCIDENT 01–30); the "cut it myself" line sets the entire round's honesty contract; ends by handing over the wheel.
Closing rule: you will RE-DELIVER this elevator in S6 — the echo test. If the closing version collapses on any anchor, the opening version was unpracticed.

**S2 — FULL SYSTEM DESIGN (clock 25 min) · the queue-ingest service that deploys to EKS**
Interviewer: "Design a service that ingests jobs from a queue and deploys its workers to EKS. Walk me through it like I'm your teammate who hasn't thought about it, and make the sizing honest."
Model answer (the canonical shape):
Ask-back first: queue source and contract (SQS or Kafka; at-least-once assumed), message size and rate, processing time and idempotency, retry/poison policy, who deploys the workers and how often, and the allowed-slow tail.
Canvas:

```
producer ──push──▶  SQS queue  ◀──poll── EKS worker Deployment (HPA)
                      │                     │  process(msg)
                      ▼                     ▼
                  DLQ (retry)      idempotent side effect (job id key)
                  + maxReceiveCount        │
                                           ▼
                                 write result / ack + delete msg
```

The core levers: (1) at-least-once is the queue's contract, so processing MUST be idempotent — dedupe on job id, because the same message will be redelivered after visibility timeout; (2) visibility timeout is the in-flight window: set it comfortably above worst-case processing time (a crash mid-process hides the message until the timeout re-reveals it — that re-delivery is the retry, not a bug); (3) poisoned messages: after maxReceiveCount the message goes to DLQ and is quarantined for inspection, not endlessly replayed; (4) scale: deployment has HPA, and the right autoscale signal here is queue depth (messages visible) rather than CPU, because a worker waiting for a slow network is idle-CPU while jobs pile up. Sizing: peak 1,000 msg/s, each message ~1 KB body, one worker pod handles ~50 msg/s (≈ processing time 20 ms with overhead), so peak needs ~20 pods; reserve 30% headroom → 26; autoscale between 5 and 40, cooldowns tuned against queue sawtooth. Deployment of the workers themselves: rolling update with a readiness gate that means "ready to take a job" (not just "process alive"), plus a graceful drain so scaling down or rolling does not murder an in-flight job: SIGTERM → stop polling → finish current message → exit, all inside terminationGracePeriodSeconds. Release safety, the part every design in this round must carry: immutable tag + digest pin, staged rollout, bounded rollout status timeout and progressDeadline so a bad release fails loudly (INCIDENT 27), and a served-version smoke after deploy (INCIDENT 29). Failure modes: poison-loop (DLQ), crash-mid-process (visibility timeout + idempotency), backlog spike (HPA + queue-depth alert), bad release (undo if bytes intact and no migration — INCIDENT 28 rule), schema-change-on-worker (expand-contract out of the image rollout).
Scoreable points: at-least-once + idempotency as the core contract; visibility-timeout-as-retry; DLQ quarantine; HPA on queue depth, not CPU; graceful drain with SIGTERM semantics; every release-safety control from rounds 2–3 name-checked; honest sizing with a reserve and a stated assumption (SQS-like queue, at-least-once).

**S2b — THE WORKER LIFECYCLE IN THE ROLLOUT (the second fenced diagram — the drain is here, not in the canvas):**
```
   Deployment rolling update (maxUnavailable 0, maxSurge 1: no worker capacity dip)
   ┌────────────────────────────────────────────────────────────────────┐
   │  old worker pod (rev 10), 3 in-flight msgs                            │
   │   │ new pod Ready (probe = "can take a job", not just alive)          │
   │   ▼                                                                    │
   │  rollout scales DOWN old pod → SIGHUP/SIGTERM to the worker            │
   │     1  stop polling the queue  →  no NEW receives                       │
   │     2  finish current message   →  ack + delete before exit             │
   │     3  exit 0 inside terminationGracePeriodSeconds (default 30s)      │
   │   ┌─────────────────────────────────────────────────────────────────┐ │
   │   │ drain contract: NO abandon the in-flight message. Abandon = the  │ │
   │   │ visibility timeout re-reveals it → at-least-once REDELIVERS it   │ │
   │   │ to another pod → idempotent by job-id absorbs the double        │ │
   │   └─────────────────────────────────────────────────────────────────┘ │
   └────────────────────────────────────────────────────────────────────┘
   the cost of skipping the drain: the message is not lost (the queue never
   loses it) — it is DELAYED + REPEATED, which is how a clean deploy becomes
   a spike of double-side-effects when job-ids are not deduped.
```
The scored axis here is exactly the drain-contract sentence: SIGHUP → stop polling → finish current → exit before deadline, with the re-reveal-under-visibility-timeout consequence named. A candidate who says "workers just die on redeploy" loses one full point on production judgment in S2.

**S2c — THE SIZING ASSUMPTION SHEET (every number in S2 with its assumption exposed — the honest-sizing grade):**
| Number used | The assumption behind it | What changes it (and the honest answer) |
|---|---|---|
| Peak 1,000 msg/s | the queue's stated peak from the ask-back | if peak doubles, pods double at 50 msg/s — the 30% reserve absorbs one burst, not a trend |
| ~1 KB messages | body size class | bigger bodies move the cost from CPU to network + memory; the 50 msg/s pod rate drops — I would re-derive from a staged load, not guess |
| 50 msg/s per pod ≈ 20 ms processing | the processing-time assumption | a slow external dependency (a 500 ms API call) collapses the rate; this is why HPA on queue depth, not CPU, is the honest signal |
| ~20 pods at peak | pure arithmetic from the above | the worst-number spread is 20→60; the reserve + min/max (5–40) brackets it, and the bracket names the uncertainty |
| 30% headroom | conventional burst cushion | a real shop sets it from the last quarterly peak; I say "I would read the dashboard before tuning" every time a number is challenged |
Sizing-rule: every figure must come with its "what would change this" line. An interviewer who asks "why 30%?" and hears "convention, I would confirm from your dashboard" scores the honesty; one who hears "30% is standard" scores the memorization.

**THE ROUND-6 DESIGN VARIANT — the cron-writer prompt (a different design on the same 15-minute S2 clock, so R6 does not depend on one scenario):**
Your GIVEN declares a product that emits one small JSON file per hour and needs materially fewer than 100 KB written at every scheduled run: frequency one per hour, durable for replay (a real file is kept, not a processed-and-dropped message), and any dropped run must be retried but must never double-write.
The answers that score: (a) CONTEXT — one hourly writer vs a queue-and-worker design; the ask is "occasional tiny durable mail", not "stream", so a scheduled one-shot is the honest shape (CronJob), and the tool is chosen because the schedule is real, not because "queues are the fancy answer". (b) CONCRETES — a CronJob with a bounded concurrencyPolicy (Forbid is the honest default: if the run overruns, drop the collision rather than double-write), a historyLimit to bound failure mess, an image whose ENTRYPOINT is the one writer (no sidecars, no PVC claims for a 100 KB file unless persistence requires it — and if persistence required it, a PVC lifecycle is a real design decision the candidate names). (c) FAILURE LANGUAGE — retry strategy must be stated as "the job fails, the alert pages, the scheduler's next tick retries — for a never-lose run I would not rely on the tick alone, I would add a backfill check that scans for the missing hour and re-writes it idempotently". Idempotency (writing the same hour's file twice lands one file) is the senior sentence: one design line that neutralizes the entire double-write class. (d) the honest boundary — "I have OPERATED Deployments; a production CronJob at fleet scale is UNDERSTOOD — my prototype would run a daily job on kind against a real local object store before I would claim more."
Variant rule: alternate the S2 design (queue worker vs cron writer) on re-runs. The two prompts exercise different halves of the same muscle — burst-shaped scaling vs scheduled one-shots — and the round report should show the SAME scoreband across both or name the weaker half as the actual gap.

**S1b — THE ELEVATOR ANCHOR SHEET (the three anchors and the exact defense each one can survive):**
| Anchor sentence | The question that will attack it | The defense line with the evidence |
|---|---|---|
| "Docker-to-ECR-to-EKS deployment live" | "What was the real constraint you hit?" | the scheduling constraint (AWS.P0.10 run) — narrated with the fix + verify, not just named |
| "Prometheus and Grafana stack" | "Why percentiles, not averages?" | the p99-vs-mean alerting rationale from OBS.P0/P2 — with one concrete series I wrote |
| "Thirty-incident playbook, every run ends in prevention" | "Name one incident family and its prevention" | INCIDENT 02 empty-endpoints → the zero-byte/endpoint-count alert — a prevention, not a fact |
Anchor rule: an anchor without a defending story is a slogan; the elevator earns its points by holding all three anchors through attack on the first question after it. If any anchor dies on the tape, that anchor drops out of the S6 echo too — the echo must never restate what the room already disproved.

**THE ELEVATOR WRONG VERSUS RIGHT (the R6 open, both transcripts — the wrong one is what a resume that lists everything sounds like out loud):**
WRONG (thirty-second): "I'm a DevOps engineer — I've worked with Docker, Kubernetes, Terraform, Ansible, CI/CD pipelines, monitoring with Prometheus and Grafana, cloud stuff AWS, some GCP, Linux scripting, um, security basics, databases… pretty much full-stack ops, happy to deep dive into anything you like." Graded: noun wall with no mechanism, no anchor, no ceiling; every tool listed is a claim the lie-detector probes at once, and "happy to deep dive into anything" is the broadest possible false promise — first probe empties the depth axis.
RIGHT (thirty-second): "Three things I'll defend today. One: I take a container from Docker to ECR to a live EKS deployment — the hard part is scheduling, and I have the run on record. Two: I read observability through Prometheus and Grafana, p99 and signal-vs-noise, with the alert rationale written down. Three: I work a thirty-incident playbook where every run ends in prevention — I can show you the family and the fix-to-alert lock. I cut myself at fleet-scale tuning and cross-region DR — I will say so the second you ask." Graded: three anchors, each with evidence and a ceiling; the cut is offered before the attack; the closing line invites the deepest probe instead of deflecting it — the exact shape R1's elevator taught, now at final-round confidence.
Rule: if the WRONG transcript is closer to your natural voice than the RIGHT one, the resume is leading your mouth — re-drill S0's backbone until the anchors, not the tool list, are what come out at thirty seconds.

**S3 — LIVE-DEBUG (clock 20 min) · INCIDENT 28: bad deploy, rollback vs forward-fix**
Interviewer: "The release landed and production is degrading: replicas unready, error rate climbing, and the old ReplicaSet was already scaled to zero — there is no good pod left. Decide, narrated, right now."
Model narrated answer (phased): 
Symptom read — I am looking at READY 0/2 with p99 climbing and an error budget burning; there is no good pod serving — that is the worst-case opening. Scope — the whole service; this is a P0 posture from the first sentence. Hypotheses — a broken image (crash or unready), a probe contract failure (I have seen this exact family in INCIDENT 27), or a runtime dependency the release needs that staging did not have. Checks in order — describe the new pod (events + last state), logs --previous if it crashed, verify strategy and probe config, and confirm the previous release's bytes are still in the registry. The decision NOW — rollback vs forward-fix, three facts, in order read aloud: is the previous revision intact in the rollout history? yes → do its bytes still exist in the registry? yes → did this release ride in a schema or data migration? no → then `kubectl rollout undo deployment/<name>` is the decision, and it is a NEW revision at the old bytes (undo is not time travel — FT-136). Forward-fix is the call only when a migration rode in, because an image undo is not a schema undo — you cannot roll a database backwards with a deployment. Verify — the same signal that called the page: READY returns to 2/2, p99 falls back through the alerting threshold, and a served-version smoke confirms the old bytes are actually serving. Escalation — if the error rate does not drop within the window, the undo was not enough and the DB/migration flag is raised; I say this limit out loud before acting, not after. Prevent — bounded rollout waits, a gated canary for the next release instead of a blind full rollout, a served-version check in post-deploy, and the INCIDENT 27 lesson: the strategy margin that let old pods keep serving is the same margin this outage did not have.
Narration scoreable points: P0 posture stated in the first sentence; hypothesis count three with discriminators; the three-fact decision rule spoken in order; the undo-is-a-new-revision fact; migration-rules-forward-fix; verify with the SAME metric; escalation limit announced in advance.

**S3b — THE DECISION MINUTE, VERBATIM (the three-fact rule spoken the way the panel wants to hear it):**
Interviewer: "Zero good pods, error rate climbing. Decide — now."
Candidate: "Capacity is gone, so first sentence is: this is the P0 opening. Three facts, in order. Fact one — is the previous revision still in the rollout history intact? I read the Revision records, not my memory. Fact two — are its bytes still in the registry under the promoted digest? Retention keeps the promoted set, but I confirm before I rely on it. Fact three — did this release carry a schema or data migration? If the migration check is clean, the undo is my decision: `kubectl rollout undo deployment/<name>` — and I say what undo means to keep everyone on the same model: it is a NEW revision, redeploying the OLD bytes, not time travel."
Interviewer: "And if fact three says there WAS a migration?"
Candidate: "Then forward-fix is the only road — an image undo is not a schema undo; rolling the deployment back cannot roll Postgres back. I would fix forward at the pinned old version and carry the migration as a separate expand-contract step. The decision rule does not change with the clock; it is the clock."
Interviewer: "What tells you the undo worked, and when do you page?"
Candidate: "Same signal that paged me: READY back to 2/2, p99 through the alerting threshold, and a served-version smoke confirming the old bytes are serving — not 'looks calm'. Paging: the moment the error rate has NOT dropped inside the window I set before acting — I announced the deadline, so I respect it."
The scored behaviors: the three facts were read off the system, not recited; the "migration ⇒ forward-fix" branch was handled in the SAME breath as the decision — no "then I'd think about it"; the limit was announced before the undo, so the escalation is a promise kept, not an excuse. That is the difference between S3 at 7 and S3 at 9.

**S3c — THE FORWARD-FIX ALTERNATE (the same minute, forced down the other road — rehearse BOTH branches):**
Interviewer: "The migration check comes back dirty. Walk the forward-fix minute."
Candidate: "Same skeleton, different decision. Fact three is the fork: a migration rode in, so `rollout undo` is OFF the table — an image undo cannot unwind RDS, and tearing the bad pods down with the schema already advanced strands the service on half-applied state. The forward-fix is: patch the code at the PREVIOUS pinned version that runs against the NEW schema — the expand is already done, so the contract became 'old app on new schema' — and push that through the gated pipeline, fast but not skipping the smoke; a hotfix that skips the gate at 02:30 is how the false-green goes green twice."
Interviewer: "While you patch, capacity?"
Candidate: "That is the P0 posture from the start: capacity is already half, so I announce the milestone — if the patch is not through and verified inside the window, the call goes louder and the restore-from-backup path opens with the DBA. I am holding forward-fix, not one-minute-here-minute-gone; the same announced limit that governed undo governs the patch."
The scored beat in the alternate: the forward-fix did not become a "wait-and-see"; it inherited the SAME skeleton (facts, branch, limit, same-signal verify) so the interviewer can hear the method is load-bearing, not the opinion.

**THE ROUND-6 RUN CHECKLIST (the final-loop equipment check before the timer):**
1. Elevator anchors rehearsed with their defending stories (the anchor sheet).
2. S5 three-phase shape primed with the "let me think" four-beat structure.
3. The S3 decision rule memorized as three facts + one branch, not as a script.
4. The four STAR beats + the S4 alternate close ready for the rotation question.
5. The questions-for-us list chosen with their reasons (ask the two that matter, not all three).
6. The closing echo rehearsed ONCE aloud — it must be a compression of the opening, never new material.
Checklist rule: any item unchecked at the timer is not forgotten material — it is a segment that will wobble precisely where you skipped preparation, and the skipped item becomes the first MUST FIX of the reflection.

**THE "LET ME THINK" STRUCTURE (for the S5 segment — a legitimate pause is itself an answer if it follows these four beats):**
1. Name the pause out loud: "I need a second to structure this" — never a silent 10 seconds.
2. State what you DO hold as fact, with the boundary.
3. State the uncertainty in one sentence — exact, not hedged.
4. State the probe that would close it and the safe default until then.
Timed template: 4 seconds silence + 3 sentences ≈ 30–45 seconds, and it scores 5–6 on uncertainty (a silent freeze scores 1; a crafted pause that closes with a probe scores 7). The S5 segment is not a test of knowledge — it is a test of what happens at the boundary, and the pause with a plan is the boundary working.

**THE S3 DECISION-MINUTE WRONG VERSUS RIGHT (the same prompt, two transcripts — grade the distance yourself):**
WRONG transcript: "Uh, so, options. We could rollback — well, git revert is a rollback, or we could... actually scaling up could give us a moment. I think I'd scale DN, no wait, the pods are the problem. Yeah, scaling is probably safest, then we see. Hopefully it settles."
Graded beats: no P0 opening and no announced deadline; rollback left as a word (git revert — wrong verb); migration never checked (the INCIDENT 28 trap walked straight through); the scale-up is a paper-over move; uncertainty is hedged but unowned ("hopefully it settles" = no probe, no default). Axis totals: production judgment 2, uncertainty 3, follow-up defense 2 → the round's S3 caps the whole R6 line.
RIGHT transcript (verbatim from S3b): the three facts in order, the migration fork answered in the same breath, the undo meaning stated, the verify signal identical to the pager, the escalation deadline announced before acting — because the decision rule is not "what to do", it is "what I promised to do by when".
Rule: run both transcripts once a week with the metronome. The wrong one is not a joke — it is the sound the panel has heard from the last candidate, and the only thing separating it from your real answer is rehearsal of the three-fact skeleton.

**THE FOUR BLUFF SHAPES (the ways the S5 segment dies, so you recognize each before you speak it):**
| Bluff shape | What it sounds like | Why it is weighted at 2 | The replacement |
|---|---|---|---|
| The Name-Drop | "Yeah, we used Argo Rollouts heavily — AnalysisTemplates and everything" | a claim at a level the next question disproves | the three-phase: named tool, OPERATED/UNDERSTOOD line, prototype plan |
| The Plausible Guess | "Staleness markers? They mark metrics stale when nothing comes for, uh, basically 10 minutes — something like that" | an invented number presented as memory | "roughly a few scrape intervals — the exact delta I would look up, here is what I know for sure" |
| The Fatal Confidence | "Oh yeah, sidecars just reroute via iptables, I know exactly how — it's the DNS chain that matters" | the confident sentence that is wrong | the mechanism-only: "proxy interception modifies routing; the chain names I would confirm from config" |
| The Silent Blink | "… (10 s) … I think it's like probably the operator thing…" | silence plus a coin-flip | the four-beat pause: name it, state the boundary, name the gap, name the close |
Bluff-rule: any slide toward these four is the S5 segment's entire grade on the line — one recognizable bluff on one question caps the uncertainty axis for the whole round, because the segment's contract is "handle not-knowing", not "know".

**S4 — BEHAVIORAL (clock 10 min) · source: 14-attack-chains 14-14 (L2 arc)**
Interviewer: "Walk me through a decision you made that later turned out to be wrong. Full arc, please."
Model answer (the rotation-commit arc from 14-14/SEC.P2.2): Context — I rotated a credential and believed that committing the rotated value, then overwriting it on the next commit, was sufficient cleanup. The decision — "the rotation commit is enough". The evidence it was wrong — the probe `git show HEAD~1:.env` printed the old key in full: the blob survived in history exactly where I had promised it was not. The repair — a rewrite of the branch history (the rotation value removed from every reachable commit) plus a secret-scan gate added to PR so the class is caught before merge, not after. The rule now at the top of my playbook — "the second commit is not a delete; history is the attack surface, and the response order is rotate, then rewrite, then gate, then verify nothing cached" (INCIDENT 30 order). What I would do the same — the admission: I volunteered the failed rotation in the retrospective instead of letting it surface in an audit.
Scoreable points: own-the-slice framing (not "the team"); the wrong fork named; evidence by name and command; the rule change is concrete; the honest close — no fabricated heroism.

**S4b — THE ALTERNATE CLOSE (run this variant when the interviewer presses the "wrong decision" harder):**
Pressing line: "So you were the one who caused it? Say it plainly."
Alternate close (without caving into self-flagellation): "Yes — the rotation was mine and my 'commit enough' model was wrong. The malfunction is named: I treated the second commit as a delete, and history does not delete. What I fixed is the model, not just the branch — a secret-scan gate on PR so the class dies before merge, and the response order lives in my playbook: rotate, rewrite, gate, verify-nothing-cached. I own the mistake fully; what I would not do is pretend the incident made me a victim." 
The scored beat: "say it plainly" is answered by owning the exact mechanism of the mistake and what changed because of it — not by groveling (which reads as no spine) and not by retreating into "well, the process was broken anyway" (which reads as no ownership). Both poles lose; the middle earns the behavioral 9.

**S5 — "SAY YOU DON'T KNOW" SEGMENT (clock 15 min) · scored on uncertainty handling**
Interviewer (each question lands, you answer in the three-phase shape, then the next fires):
The three-phase shape for every answer: (1) PRECISE KNOWLEDGE — say exactly what you know, with the confidence boundary; (2) NAMED GAP — say out loud what you do not know or are not sure of; (3) CLOSE THE GAP — how you would find the answer now (probe, docs, senior, prototype) and the safe default you would hold until then. Bluffing scores 2 on this segment regardless of the axis; a clean three-phase scores 8. One "you got me, let me think" pause is also an answer — name the gap and the probe.

**THE FIRST UNKNOWN, MINUTE ONE, VERBATIM (the opening S5 question narrated at full length so the three-phase shape is heard, not just described):**
Interviewer: "What is the difference between a canary deployment and a shadow deployment?"
Candidate: "Canary takes a small, real slice of user traffic and serves it from the new version — ten percent, error-rate and latency gates, then ramp if the gates hold; that is FT-152's strategy ladder, and I have operated a gated canary. Shadow takes the SAME incoming traffic and duplicates it at the new version while the old version keeps serving users — the shadow's output is compared or discarded, never delivered. Named gap: the exact operator tooling and the shadow discard semantics — I would confirm vendor behavior in the docs, because I have configured a canary but not a shadow in production. Close the gap: read the tool's shadowing page, prototype the duplication and discard on kind, and my safe default until then is — shadow for correctness-preview only, never a stand-in for the canary's live ramp."
The graded beats: the two mechanisms separated by OUTPUT (canary serves, shadow discards) rather than by tool; the OPERATED/USE-LEVEL boundary spoken between sentences (a topic the mock explicitly rewards); the close-the-gap move named a concrete prototype with a vendor doc, plus a safe default that is a DECISION, not a hedge. This is the shape all five unknowns are graded against — run the metronome on it daily.

**U1 — "What is the difference between a canary deployment and a shadow deployment?"**
Model three-phase: Knowledge — canary routes a small slice of real user traffic to the new version and ramps only while error-rate/latency gates hold (FT-152); shadow copies real traffic to the new version while the old version keeps serving and the shadow results are compared or discarded — it never serves the copy's output to users. Named gap — the exact operator tooling (Istio shadowing vs a linkerd tap) and shadow response-discard semantics I would confirm in the docs, since I have configured a canary but not a shadow. Close the gap — "I would read the vendor's shadowing page and prototype the weight/duplication on kind; my safe default until then is: shadow for correctness-preview, canary for the live production ramp." Score: high; you named the difference precisely and did not invent tooling.

**U2 — "Have you used Argo Rollouts, or progressive delivery, in production?"**
Model three-phase: Knowledge — Argo Rollouts is the progressive-delivery controller (canary/blue-green with analysis steps) layered over Deployment-style rollouts; it is the GitOps-native answer to FT-152's strategy ladder. Named gap — hands-on depth: I have OPERATED plain rollouts (rollout/undo live on kind, INCIDENT 27/28) and UNDERSTOOD Argo Rollouts from the CICD.P1.2 model-only session — I have not run Rollouts AnalysisTemplates in live production. Close the gap — a two-evening prototype on kind with an AnalysisTemplate before I would put it next to production; the claim level on my resume stays UNDERSTOOD until that prototype runs. Score: high — the claim-level boundary is precisely the honesty contract the round opened with.

**U3 — "How do Prometheus staleness markers work?"**
Model three-phase: Knowledge — a metric series is declared stale when no new samples arrive for roughly a few scrape intervals (the staleness window is set around the scrape interval and the "keep" logic; a sample that is stale gets a stale marker, and queries treat it as no-value rather than re-using the last sample — which is why rate() charts dip to gaps instead of painting flat lines at the old value). Named gap — I am not fluent in the exact staleness-delta form; I have seen it in behavior (flat-line-vs-gap readouts) but not written it in PromQL. Close the gap — read the Prometheus staleness doc and reproduce it with a stopped exporter in the local stack; safe default: never trust a flat line — confirm the exporter is being scraped. Score: good; mechanism from OBS.P0/P2 evidence with an honest docs-gap.

**U4 — "What does a service-mesh sidecar actually do at the iptables level?"**
Model three-phase: Knowledge — the sidecar hook is traffic interception: an init container writes iptables rules that redirect pod in/out traffic through the sidecar proxy (envoy), which then terminates mTLS, applies routing/retry/timeout policy, and re-emits to the next hop — so the mesh is a per-pod proxy, not a network appliance. Named gap — I cannot recite the exact chain names (ISTIO_OUTPUT-style details) or the redirection corner cases; that is implementation detail I would confirm from the proxy's generated config. Close the gap — inspect a mesh-injected pod's iptables + proxy config on a dev cluster; safe default: the model is "traffic is proxied in-process on the pod", which is why mesh adds latency and why mesh-vs-applayered retry matters. Score: good — model right, detail honestly bounded.

**U5 — "What is a chaos-engineered game day, and have you run one?"**
Model three-phase: Knowledge — a game day is a rehearsed, scheduled, bounded failure injection (drain a node, kill a pod, blackhole a dependency) in a controlled environment to verify observability, runbooks, and recovery without an unplanned outage; the loop's output is a runbook correction or an alert gap, not drama. Named gap — I have built the INCIDENT 01–30 playbook and run narrated incident rehearsals, which is the runbook-side of a game day, but I have not designed a chaos experiment on live traffic or held a production game day — the claim level for chaos engineering is UNDERSTOOD. Close the gap — propose the smallest first game day (one drain, one dependency kill on staging, graded against the playbook's detect-and-recover rows) and run it with a senior before anyone toes a production node. Score: high — the run cycle is real, the claim boundary is clean.

**U6 — "How does a Kubernetes Operator differ from the built-in controllers?"**
Model three-phase: Knowledge — an Operator is a controller whose reconcile loop drives domain-specific state — think "a controller for the thing the platform does not understand by default" — using the same watch/desired-state loop as the built-ins but owning a custom resource and its lifecycle (e.g. a PostgreSQL cluster CR). Named gap — I have configured and watched controller-manager loops, but I have not WRITTEN a production operator or run the Operator Framework/operator-sdk lifecycle end to end — the claim level is UNDERSTOOD. Close the gap — a small proof: write a minimal controller for one CR on kind, watch it reconcile, and state the failure mode (a reconciler that never converges needs a status + requeue design). Safe default — do not put custom-controller logic in the production path until that proof runs.

**U7 — "What is a Warm Standby vs Active/Passive for a database, at the failover mechanics level?"**
Model three-phase: Knowledge — active/passive (warm standby) keeps a replica that is replayed-to and promoted on failover — writes pause, promotion happens, clients re-point, and the RTO is bounded by the promotion + detection time. Active/active means both sides take writes, which needs conflict resolution and is where Postgres gets painful (multi-master is a real product decision, not a checkbox). Named gap — I have worked RDS multi-AZ as an ABSTRACTION (the failover is managed), I have not run a bare-metal or self-managed replication failover myself — the mechanics of the failover timer and promotion order I know from the docs and probes, not from a live demotion. Close the gap — rehearse a single promotion on a dev pair (primary + replica, cut the primary, promote, re-point) and record the RTO I actually measured. Safe default — treat multi-AZ failover windows as assumptions, and ask for the team's measured RTO before promising any number.

**U8 — "How does a CDN invalidate a cached object, and what is the hard part?"**
Model three-phase: Knowledge — a CDN cache serves by the object's key (URL/path usually); invalidation targets that key across the edge — either a purge request to the CDN control plane (vendor method, async propagation) or, more scalably, versioned URLs (a new URL is a new cache object, so the old one dies by TTL, not by purge). The HARD part: purge is eventually consistent AND propagates asynchronously across edges, so the "invalidated" object can still be served from a node that has not gotten the purge — which is why versioning the URL beats purging for anything user-visible. Named gap — I have used versioned assets and read purge docs, but I have not operated a large-edge CDN's purge pipeline or benchmarked its propagation. Close the gap — lab it: push an object, purge, and measure how long the old version is still served from the edge until TTL — that measured number becomes the honest claim. Safe default — version the URL and let TTL do the real work.

**U9–U13 — THE ROTATION BANK (five more three-phase questions so re-runs never reuse the same unknowns; same shape, different boundaries):**
U9 "What is the difference between a sidecar, an initContainer, and a job in Kubernetes, in lifecycle terms?" — Knowledge: sidecar runs parallel with the app for the pod lifetime, initContainer runs-to-completion BEFORE the main containers start, job is a pod that runs-to-completion as a workload. Named gap: I have configured all three but not written a production multi-container lifecycle; Close: a pod with init + sidecar on kind to watch ordering; Safe default: never put startup logic in a sidecar and call it init — ordering is the contract.
U10 "How does HTTP/2 vs HTTP/1.1 change your ALB timeout thinking?" — Knowledge: H2 multiplexes over one TCP connection, so an idle H2 stream can die on a p99-alerting TCP timeout that H1 would have seen per-connection; the load balancer's idle timeout applies at the connection level. Named gap: I have not tuned ALB timeouts under H2 in production. Close: lab two endpoints, one H1 one H2, raise the client's idle, watch the RSTs. Safe default: for stream-y clients, treat connection idle timeouts as functional, not cosmetic.
U11 "What is a StatefulSet for, and what does ordering give you that a Deployment cannot?" — Knowledge: StatefulSet gives stable identity (name, PVC, network) and ordered create/scale/delete — exactly for stateful workloads like DBs or message coordinators that model their topology in their config; a Deployment's replicas are anonymous and shuffling. Named gap: I have run Deployments; a StatefulSet ordain I have read/understood but not operated at scale. Close: a two-node StatefulSet on kind with PVCs and an ordered scale-down. Safe default: do not reach for StatefulSet for stateless workers — the ordering costs you.
U12 "How does a cache like Redis stay consistent with a hot-and-cold read path?" — Knowledge: consistency is bought at the read-path: read-through/write-through, invalidation vs TTL, and the cache-aside pattern where the app checks, misses, re-reads the source and back-fills — TTL drift is the classic inconsistency source. Named gap: I have configured and measured cache-aside; I have not designed a cache-consistency story for a multi-region tier. Close: write the read-through vs cache-aside trade on the board and verify one key lifecycle in the local stack. Safe default: never let the cache become the source of truth.
U13 "What does the shutdown sequence of a Linux box look like, and where does a slow unmount surface?" — Knowledge: kill processes (SIGTERM then SIGKILL after grace), sync filesystems, unmount in reverse dependency order, stop services, power off — a busy filesystem wedges the unmount, so boot-time checks flag an unclean shutdown/fsck next boot. Named gap: I have removed hosts and read shutdown logs, not engineered an unmount order for a fleet. Close: watch one graceful + one forced shutdown in a lab and note where each logs. Safe default: never assume SIGKILL-then-poweroff is "the same"; the unmount window is where data is written.
Bank rule: rotate U9–U13 into the U1–U8 set on re-runs so the S5 segment tests NEW knowledge boundaries instead of re-testing the ones the mocks already mapped — the boundary you stop training is the boundary the real interview finds.

**S5 SCORING SHEET (fill per run — the uncertainty axis deserves forensic scoring, not a vibe):**
| Q | 3-phase out loud? | Gap NAMED, not hedged? | Close-the-gap concrete? | Claim-level held? | Axis /10 |
|---|---|---|---|---|---|
| U1 canary vs shadow | | | | | |
| U2 Argo / progressive | | | | | |
| U3 staleness markers | | | | | |
| U4 sidecar iptables | | | | | |
| U5 game day | | | | | |
| U6 operators | | | | | |
| U7 DB failover | | | | | |
| U8 CDN invalidation | | | | | |
| U9 sidecar/init/job | | | | | |
| U10 HTTP/2 timeouts | | | | | |
| U11 StatefulSet ordering | | | | | |
| U12 cache consistency | | | | | |
| U13 shutdown sequence | | | | | |
Row standard: a no in the "gap NAMED" or "claim-level held" column for any row = the segment's must-fix, because a missing calendar on ONE question is the exact tell an interviewer writes into the feedback, while a clean 4-out-of-5 with one shave is a strong pass.

**VARIANT ANSWERS — WHY THE SAME QUESTION SCORES 4, 7, OR 9 (U2, "have you used Argo Rollouts in production")**
The 4/10 version: "Um, I've used Argo Rollouts — yeah, canary stuff, in production." Then a silence when asked which analysis step it ran. Graded: the claim was made at a level the rest of the round cannot support; two questions later the interviewer knows "in production" was a costume. Honest total for this segment: 4.
The 7/10 version (the model answer above): named the tool, drew the claim line (OPERATED plain rollouts, UNDERSTOOD Rollouts from a model-only session), named the prototype that raises the level. A 7, not a 9, because the gap-closing plan is a prototype, not an execution.
The 9/10 version adds one beat: "…and I ran that prototype two evenings later: an AnalysisTemplate over a kind spawn, one canary metric fail caught, and I wrote down what the controller did with the analysis — here is what I would change in the AnalysisTemplate because of it." That is the difference between handling not-knowing well and turning not-knowing into done — the round grades the first, the offer letter wants to hear the second. Neither is a bluff.

**S6 — CLOSING: questions and the elevator echo (clock 10 min)**
Interviewer: "That's my list. Do you have any questions for us?"
Model answer set (pick the strongest two or three, each with its reason):
Q1 — "What has the last serious incident this team had actually taught the team, and where did the runbook fail first?" Reason: it frames your own training corpus as a tool for THEIR pain, and read-their-evidence-first is the production-judgment signal from round 3.
Q2 — "Where does burn-down or error-budget authority sit for the on-call rotation — who decides a release is paused?" Reason: it shows you will not be the engineer who keeps pushing when the budget says stop; it also tells you their promote/review culture.
Q3 — "What is the deploy-to-prod model today, and is there anything your team wants to change about it within the next six months?" Reason: the best setups have a roadmap; asking lets you map your delivery-spine story onto their actual next migration instead of pitching generic CI.
Then, unprompted, the elevator echo — re-deliver the S1 elevator, compressed to the closing beat and aimed at the room: "Same closing as my opening: pipelines to containers to a cluster to watching it — I have done that spine end to end, including breaking and fixing it; the runbooks I train on end in prevention; and if any claim of mine could not survive the day here, I would expect you to cut it — I already would." Stop. Do not unpack it.
Scoreable points: the questions target the team's operational reality, not salary/perks; the echo restates the three anchors unchanged (the consistency the whole round was testing); the word "cut it" returns the S1 honesty contract to the room.

**THE S6 WRONG VERSUS RIGHT — the closing beat-grade (the echo is the last primary-grade sample the panel takes):**
WRONG close: "Yeah, a couple of questions — how many people are on the team, what's the hybrid policy, and, uh, when would I hear back about next steps? Also just want to say I'm really excited about the opportunity — I've been wanting to get back into cloud stuff…" Graded: the questions target comfort, not the operation; "cloud stuff" is a breadth-word after an hour of precision; the round ends on the least defensible syllable in the file — the last-grade sample is the weakest one.
RIGHT close: the Q1–Q3 set above (evidentiary, budget-authority, deploy-model) plus the echo, and then silence where the WRONG search added politeness — the round ends ON the anchors, exactly as S1 opened them. Graded: the last sample repeats the first sample's shape, which is what a consistency-hunting panel records.
Rule: the closing is not a new performance — it is the S1 elevator literacy-check with three questions bolted on. If the echo cannot be re-delivered after 90 minutes of interrogation, the anchors never were anchors; they were a first impression.

**POST-ROUND DEBRIEF — the three questions the panel asks in the hallway, answered by the round itself:**
| Panel question | What they are really checking | Where the round answers it |
|---|---|---|
| "Would this person take my incident?" | narrated method under pressure, not brilliance | S3's P0-posture-first + three-fact rollback + escalation limit announced in advance |
| "Would they know what they don't know?" | the honesty contract from the first sentence | S5's three-phase shapes held on all five questions, claim-levels unbroken |
| "Would they embarrass us on design?" | scoped, honest delivery thinking at 1–3 YOE | S2's idempotency + queue-depth HPA + drain contract + RELEASE-safety controls every frame |
If the round produced an answer to all three without a must-fix, the mock system's job is done for this pass — the tape is the deliverable and the score follows it.

**SCORE TABLE (7 axes):**

| Axis | /10 | Why |
|---|---|---|
| Technical accuracy | | S2 queue semantics (at-least-once, visibility timeout, idempotency, DLQ) and S3 undo mechanics are checkable against 09-cicd/07-kubernetes incident content. |
| Reasoning & structure | | S3 three-phase narration in FT-160 order; S2 decision order (ask-back → canvas → levers → sizing → release safety). |
| Communication | | Elevator in one breath + the S6 echo; narrations continuous; every S5 answer structured as three-phase out loud. |
| Depth & nuance | | S2 HPA-on-queue-depth and SIGTERM drain are the two senior tells; S3 migration-rules-forward-fix. |
| Follow-up defense | | S5 answers must not contradict S1 anchors — the bridge-gap consistency test. |
| Production judgment | | P0 posture in S3's first sentence; escalation limit announced in advance; DLQ quarantine; claim-levels held everywhere. |
| Uncertainty handling | | The whole S5 segment is one gradeable sample: three-phase answers at 8+, a bluff at 2, a "let me think" pause at 5 if it names the gap. |

**REFLECTION (fill after):** _what I said_ — transcribe S3 and S5 in full; they are the two most forensically graded segments in the whole mock system. _where I froze_ — in S5 the freeze is a blush-and-guess; note the exact question and whether the three-phase shape came out. _where I overclaimed_ — any anchor in the closing elevator (S6) that wobbled against S1; any S5 answer that reached for depth you do not hold.

**MUST FIX / SHOULD FIX / NICE TO HAVE:**
| MUST FIX | SHOULD FIX | NICE TO HAVE |
|---|---|---|
| Any S5 bluff (re-drill the three-phase shape on every gap) | S3 without the migration-rules-forward-fix clause | Complete the S1↔S6 elevator echo without wobble |
| S2 with no graceful-drain SIGTERM story | An S2 sizing figure with no stated assumption/reserve | Queue-depth HPA named unprompted (S2) |
| Undo described as time travel in S3 | Skipping the served-version smoke anywhere | The mesh "traffic is proxied in-process" model (U4) |
| Escalation limit announced AFTER the fact | Forgetting DLQ quarantine in S2 failure modes | "I would read the docs and prototype" as the reflex in S5 |

### QC CHECKLIST — ROUND 6
| # | Check | Status |
|---|---|---|
| 1 | Opens and closes with the 30-SECOND ELEVATOR from 16 (S1 + S6 echo) | PASS |
| 2 | One full system design (queue-ingest service on EKS) at honest 1–3 YOE scope | PASS |
| 3 | One live-debug (INCIDENT 28) narrated with the three-fact rollback rule | PASS |
| 4 | One behavioral (14-14 L2 arc, rotation-commit story) with ownership | PASS |
| 5 | "Say you don't know" segment has 5 scripted questions with three-phase model answers | PASS |
| 6 | S5 scoring rules make the uncertainty axis explicit (3-phase = 8+, bluff = 2) | PASS |
| 7 | Closing segment answers "any questions for us" with rationale | PASS |
| 8 | Score table has exactly the 7 axes | PASS |
| 9 | Reflection section with blanks present | PASS |
| 10 | MUST FIX / SHOULD FIX / NICE TO HAVE present | PASS |
| 11 | Time budget ties to 90 min (1 + 25 + 20 + 10 + 15 + closing) | PASS |
| 12 | No emojis, no placeholder wording, fences balanced in this round | PASS |
| 13 | SELF-VERIFY — model answers are sourced from the real sibling sessions (FT/chain/incident IDs resolve) | PASS |

VERDICT: **ROUND 6 COMPLETE.** The full-loop dress rehearsal closes on the two muscle groups the mocks exist to build: honest claim boundaries (S1/S2/S4/S5) and narrated method under pressure (S3). A round-six score below 60/70 with any must-fix larger than a single re-drill means the stack is not interview-ready — return to 18-revision.
NEXT POINTER: run each failed axis once more as a targeted 20-minute session — the uncertainty axis feeds straight back into 14-attack-chains (players who never say "I don't know" are the ones the trap variants catch), then read the grading appendix below.

---

## HOW TO GRADE LIKE AN INTERVIEWER

This appendix is the object-code of the 7-axis scoring: what each axis actually measures, what a 7/10 answer sounds like versus a 4/10 — and the two calibrated-rubric rows that keep your self-grading honest. Grade the transcription, never the intention.

**What each axis measures:**

| Axis | The question it really asks | What a 7 requires | What a typical 4 looks like |
|---|---|---|---|
| Technical accuracy | Are the facts, commands, numbers, and mechanisms correct? | Every claim checkable; exact exit codes/IDs/units; admits the one fact that is a convention (e.g. default timeout dates). | Mostly right names, wrong mechanism under the hood; one confidently-wrong detail (e.g. "refused = server down"). |
| Reasoning & structure | Is there a method visible, in order, or a lucky hit? | Symptom→scope→hypotheses→cheapest-checks→evidence→root cause→fix→verify, narrated in order. | Fix-first: jumps to "restart it" with no scope or hypothesis; ordering is wherever the brain landed. |
| Communication | What did the interviewer actually hear, in time? | One-breath answers, stops when the point is made, correct vocabulary, no filler. | Long rambles that re-answer; "like, it's basically…"; silence-and-mumble on unknown. |
| Depth & nuance | Does the answer hold two levels down? | The mechanism + one nuance each time (D-state in load, undo-is-a-new-revision, 502-vs-503). | One-liner definitions; the first follow-up drains the tank. |
| Follow-up defense | Do the follow-up answers survive without contradiction? | Probes answered from the same model; no retraction needed. | Answer one was fine, answer three contradicts answer one and the candidate does not notice. |
| Production judgment | Would you trust this person near prod? | Reversible actions, bounded waits, verify-with-the-same-signal, escalation triggers named. | Paper-over fixes, "we'll just rerun it", no verify, no prevention. |
| Uncertainty handling | How do they behave over their own knowledge boundary? | Names exactly what they know, names the gap, names the probe that closes it. | Bluffs, then freezes when pressed; or admits nothing and gets quieter. |

**The 0–10 rubric, full rows (grade a 7 the same way every round — the precise band anchors):**
| Axis | 0–3 (fail) | 4–6 (marginal) | 7–8 (pass) | 9–10 (offer sentence) |
|---|---|---|---|---|
| Technical accuracy | a confidently-wrong mechanism; invented flags/exits; wrong dates | mostly right names, mechanism wobbles under "why" | every stated fact checkable, one convention-call admitted | zero wrong claims + a nuance the interviewer did not prompt |
| Reasoning & structure | fix-first, no scope, no order | method present but out of order or one stage skipped | FT-160 order narrated with costs and branches | order + ambiguity explicitly handled before committing |
| Communication | ramble, re-answer, filler, silence on unknown | mostly on-topic, some ramble, one pause too long | stops at the money line, one breath, no filler | answers that pre-empt the interviewer's next question |
| Depth & nuance | one-liners, drains at first follow-up | one level down on the prompted topic | mechanism + one self-offered nuance per answer | connects the topic to an adjacent layer (D-state↔accept queue) |
| Follow-up defense | contradicted self, did not notice | held on some probes, wobbled on the number one | same model across three probes, no retraction | the third probe made the answer better, not changed |
| Production judgment | paper-over fix, no verify, no prevention | reversible actions, verify present-ish, no prevention | reversible-first, verify with same signal, prevention named | named the P0 trigger BEFORE the fix and honored the deadline |
| Uncertainty handling | bluff then freeze, or dead silence | hedged, or a pass with a shrug | three-phase: know / gap / close, calmly | the pause with a plan scored as a full answer |
Band rule: a score of 9 must come with at least one thing you said that the interviewer did not ask for — a self-offered nuance, a boundary you set, a prevention you added. A perfect answer to the asked question is a 7; the 9 is the asked question answered plus one responsible extra.

**The 30-minute half-round (a daily-rep format that keeps the elapsed-clock: full six rounds are too heavy for every practice day):**
| Slice | Clock | What | Source |
|---|---|---|---|
| Open | 3 min | elevator + first two rapid-fire (any FT) | 15-question-bank |
| Debug | 10 min | one narrated incident, full S1–S10 skeleton compressed | 12-troubleshooting any incident |
| Design | 8 min | one decision defended (a rollout pick, a gate placement) | reuse any round-3/6 prompt |
| Honesty | 6 min | two "say you don't know" questions, three-phase | 14-attack-chains trap variants |
| Grade | 3 min | one axis only — rotate the axis daily | appendix rubric |
The half-round is how you keep the metronome practiced between full mocks: the same 7-axis scoring, a tenth of the clock, and a defensible claim that you did a scored interview every working day.

**The full pass protocol (how the six rounds fold into one campaign — order and rest are part of the design):**
| Day | Round | Why this slot (and what it is allowed to teach) |
|---|---|---|
| 1 | R1 T | breadth first — it is the speed-of-voice warm-up everything else quotes |
| 2 | (half-round) | hold the metronome; grade-then-rest, no new material |
| 3 | R2 R | narration against a real incident file, one family deep |
| 4 | (half-round) | hold it; rotate ONE drill from the low axis |
| 5 | R3 S | the first design; the 09-cicd cross-walk carries it |
| 6 | REST | no tape — the gap-closing ideas need a night in a real head |
| 7 | R4 B | calibrate the claims before the marathon debts them |
| 8 | (half-round) | hold it |
| 9 | R5 H | the full-day rehearsal under 90 real minutes |
| 10 | REST | grade everything at +24h, fill every REFLECTION blank |
| 11 | R6 F | the decision-round — the interviewer's real loop in miniature |
| 12 | FINAL REPORT | the FILE-LEVEL QC + the 10-question offer check |
Protocol rule: a round skipped is a gap left named but untested; the two REST days are scored days too (the +24h grade is the part that converts the campaign into evidence instead of a highlight reel).

**Sample: 4/10 vs 7/10 on the same question ("Connection refused vs timeout")**

The 4/10 transcription (what was actually said): "Uh, refused means the server is down, and timeout means it's slow or overloaded. So if it's refused, I'd check if the service is running; if it's timeout, the network is the problem I guess. I'd try to curl it."
Graded: technical accuracy 3 (both halves wrong — refused means something answered RST, timeout means silence; "slow" does not produce a timeout unless the accept queue is full); reasoning 3 (no layer split, no tool ladder); communication 4 (short but hedged and guessing); depth 2 (nothing below the surface); follow-up defense 2 (one "why" empties it); production judgment 3 (no evidence sequence, no first-check); uncertainty 4 (hedges but does not name the gap). A defensible total: 21/70 — a pass-to-someone at mid-band, a fail at a serious shop.

The 7/10 transcription: "Refused means I got an RST back — something answered and the port is closed, or nothing listens there, or the bind address is wrong, or a firewall is REJECT-ing. Timeout means my SYN got silence — a DROP rule, no route, host down, packet loss, or an app whose accept queue is full. First I resolve — dig — then from the host `ss -tlnp` to see what listens on which interface, then `curl -v` and `nc -zvw2` to classify RST vs hang; if it's ambiguous I'd take a capture. The line that tells me a lot: refused is a definitive closed; timeout is ambiguous between down and filtered."
Graded: technical 8 (mechanism right, accept-queue named); reasoning 8 (tool ladder in order with a purpose per tool); communication 8 (tight, structured, stops at the point); depth 7 (mind-ladder covers the cause set); follow-up defense 7 (a "busy server causes timeouts — how?" gets "accept queue full → kernel drops or SYN-cookie path"); production judgment 7 (first-checks and the refused-definitive insight); uncertainty 7 (ends honest about ambiguity). Total: 52/70.

The two calibrated-rubric rows to keep for every self-graded round:

| Band | Round score | Meaning | Action |
|---|---|---|---|
| 60–70/70 | 80%+ of axes at 7+ | Interview-worthy on this round's material | Hold at +48h, then revision plan only |
| 45–59/70 | mid-band, mixed | One or two axes are the offer-line | Re-drill the low axes against their sibling files, re-run the round once |
| 30–44/70 | below band | The material is not yet owned at speak-depth | Back to 13-write-without-google + the low-axis chain, no new mocks until re-take ≥ 45 |
| 0–29/70 | not defensible | Memorized-not-owned; the round was a rehearsal of guesses | Rebuild from the P0 sessions; do not book a real interview on this stack |

**The blank grading template (photocopy one per round — the round ends when this is filled, not when the timer stops):**
```
ROUND ____   DATE ____   SELF-SCORED /70   BAND (__)
Axis                 Score   The sentence in my tape that earned or lost points
Technical accuracy   /10     —
Reasoning & structure/10     —
Communication        /10     —
Depth & nuance       /10     —
Follow-up defense    /10     —
Production judgment  /10     —
Uncertainty handling /10     —
MUST FIX (≤3): _________   SHOULD FIX: _________   NICE TO HAVE: _________
Word count of my longest answer: ____  (the monster of the tape)
One sentence the interviewer would write in feedback: ______
```
Rule: every blank must be filled before you record the round grade — a round with an empty axis cell was not graded, it was reheard.

**Self-grading FAQ (the questions self-graders ask most, answered from the rubric):**
| Question | Answer |
|---|---|
| "I froze but fixed it — is that partial credit?" | The freeze is one sample on uncertainty, not the round. Grade the axis as a distribution; a single freeze with three clean three-phase answers is not a 2. |
| "I corrected myself on tape to the right answer — score it as right?" | Only if the correction arrived BEFORE the interviewer moved on, and the mechanism statement is then complete. A correction after the next question started is the original score minus a point. |
| "Is confident delivery worth a point?" | Not on technical accuracy. Confidence is worth one point on communication at most; exactness is the technical grade. |
| "Do I get points for saying 'I would read the docs'?" | On uncertainty handling yes (it names the close), on production judgment only if the safe-default is also stated. |
| "One axis at 4, everything else 8 — round score?" | Band is one thing, offer-readiness is another — the 4 names the re-drill target; do not average your way to calm. |
| "Grading myself right after is biased — when?" | Grade at +2 to +24 hours on the transcription, never in the same hour. The debrief heat inflates; the transcript is the object. |

**The gap-to-fix map (one row per axis — when the axis is the low one, this is where the correction lives, not "practice more"):**
| Low axis | The tape usually shows | The fix (a named file + a named drill) |
|---|---|---|
| Technical accuracy | mechanism spelled wrong or half | 15-question-bank re-read with write-without-google on the FT row |
| Reasoning & structure | answers start mid-story | 14-attack-chains drill L1.5, answer-proof line first |
| Communication | run-ons, no stop-point | R1 metronome; the answer-velocity drill |
| Depth & nuance | one surface layer, no under-hood | the go-deep alternate targets, 3 probes per topic |
| Follow-up defense | first "why" empties the tank | the R4 hostility exchanges, wrong-vs-right transcripts |
| Production judgment | next-command missing, no escalation | R2 narration template + the escalation matrix |
| Uncertainty handling | silence or a bluff shape | R6 three-phase + the four bluff shapes, daily |
Map rule: fill this AFTER each round using the score table's WHY column — the map converts "I got a 4" into a file path and a drill with a clock, which is the entire point of grading at all.

**The interviewer's one-sheet (what a real interviewer writes down during the round — grade against THIS grid, not your memory):**
```
Candidate verdict sheet — ROUND ___
[ ] Claim-level swore consistently each answer (any overclaim: tick + CAP)
[ ] Mechanism-first, or fix-first? (note the order of the first answer)
[ ] Silence incidents: ___ (count and length)
[ ] Follow-up contradictions: ___ (question numbers)
[ ] Numbers given/stated vs numbers bluffed: ___ 
[ ] Escalation/prevention named unprompted: yes / no / once asked
[ ] Words that made the room sit up (quote two):
ADJUDICATION LINE: (one sentence) ______
```
The one-sheet is the grader's instrument: it grades the TAPE facts (silence count, contradiction count, bluff count) before the subjective axes. Filling it per round converts self-grading from "how did I feel" into "what did I emitt", which is the same object a real interview writes down about you.

**The cross-round consistency check (run once after all 6 mocks):** the same four anchor stories must survive every round they appear in — the EKS run (R1 S-cost, R4 16-01, R6 S1), the Prometheus stack (R1, R6 S1), the INCIDENT 27/28 family (R2, R3 S7, R5 A3, R6 S3), and the reflog/rotation recovery (R4 S5, R6 S4). If any anchor's numbers or claims changed between rounds, the failing claim is the one that was told differently on tape — that is the gap a real interviewer would have caught, and it is now yours to fix.

**Per-round axis stress (which muscle each mock round actually loads — read this to decide where a low axis comes from):**
| Axis | R1 T | R2 R | R3 S | R4 B | R5 H | R6 F |
|---|---|---|---|---|---|---|
| Technical accuracy | primary | primary | heavy | medium | primary | heavy |
| Reasoning & structure | medium | primary | primary | light | heavy | primary |
| Communication | heavy | primary | medium | primary | primary | heavy |
| Depth & nuance | heavy | heavy | heavy | medium | heavy | heavy |
| Follow-up defense | primary | heavy | medium | primary | heavy | heavy |
| Production judgment | medium | primary | primary | heavy | heavy | primary |
| Uncertainty handling | light | medium | primary | primary | light | primary |
Reading rule: a 4/10 on communication in R2 cannot be blamed on the interviewer — R2 is the narration round and communication is its primary load. The matrix maps a weak axis to the round that best fixes it: depth problems → R1/R3/R5; production-judgment problems → R2/R6; follow-up-defense problems → R1/R4/R5; uncertainty problems → R3/R4/R6.

**The expected-score model (what a defensible 1–3 YOE pass looks like per round, so a "7" has a reference):**
| Round | Expected overall | The two axes that carry the score | Typical lowest axis (and why that is OK) |
|---|---|---|---|
| R1 T | 48–60/70 | technical accuracy, depth | production judgment — breadth rounds spend no time proving it |
| R2 R | 50–62/70 | reasoning & structure, communication | depth — narration prioritizes order over nuance |
| R3 S | 48–60/70 | production judgment, uncertainty | technical accuracy — big-design numbers are invented-or-read |
| R4 B | 48–60/70 | follow-up defense, honesty signals | depth — behavioral rounds trade nuance for calibration |
| R5 H | 50–62/70 | communication, follow-up defense | depth — the clock starves the second level |
| R6 F | 55–64/70 | uncertainty, production judgment | breadth — the unknowns cost points by design |
Model rule: a passing candidate does NOT average 8 — the model says the expected LOW axis is situational, and the honest-grade lie is inflating the low axis to match the highs. Use the model to answer "is my 7 real" by comparing the axis SHAPE, not the total, against the round's expected profile.

**Common grading mistakes (the errors self-graders make that inflate or deflate a score):**
| Mistake | Why it corrupts the grade | Fix |
|---|---|---|
| Grading the intention, not the tape | "I knew that, I just didn't say it" scores what you WANTED to say; interviewers grade spoken words | Transcribe; grade the transcript sentence by sentence |
| A "mostly right" answer round up | One wrong mechanism is a 3 on technical accuracy even if 80% of the words were right — the fix-first machinery usually accompanies it | Score the mechanism sentence only; the filler does not count |
| Giving yourself the benefit on unknown facts | "I said it confidently so it must be right" — the confidence is the trap, exactness is the grade | Check every factual sentence against its sibling FT/incident ID |
| Over-penalizing one bad minute | 25 great minutes plus one freeze should not drag uncertainty to a 2 | Grade the axis as a distribution: the freeze is one sample, the three-phase answers are the others |
| No severity in dates/versions | "I said Dec 2020 for S3 consistency" is worth a point; "the '90s" is worth nothing and flags a trained-voice | Unit-check: exact dates/IDs = evidence, vague = phrasing |
| Scoring follow-up defense from the first pass only | The second and third probes are the question | Only score answers 2 and 3 of each twist chain for this axis |

**The cross-round scoreboard (fill once per full pass — the only table that says offer-ready):**
| Axis | R1 | R2 | R3 | R4 | R5 | R6 | Lows triggered | Owner round to fix it |
|---|---|---|---|---|---|---|---|---|
| Technical accuracy | | | | | | | | R1 / R5 |
| Reasoning & structure | | | | | | | | R2 / R3 |
| Communication | | | | | | | | R2 / R5 |
| Depth & nuance | | | | | | | | R1 / R3 |
| Follow-up defense | | | | | | | | R1 / R4 |
| Production judgment | | | | | | | | R2 / R6 |
| Uncertainty handling | | | | | | | | R3 / R6 |
| Round totals /70 | | | | | | | | — |
Offer rule: four of seven axes at 7+ with NO axis below 5 in the LAST two rounds, and the cross-round anchor check clean — that is the defensible "yes" for a 1–3 YOE hire signal. Any round-6 axis below 5 voids the pass regardless of the average, because R6 is the real loop.

**How to fill the scoreboard without lying (the three rules that keep the table an instrument, not a diary):**
1. Fill every cell from the TRANSCRIPT, never from the sense of the round — a "7" must be pointable to a sentence that earned it; an unpointable 7 is a diary, and it will read as a diary on the actual panel.
2. Add the axis-level NOTE before the number: note first ("probe contract was exact", "escalation limit was announced"), then the number that note justifies; the note is what survives +48h, the number is its hard attachment.
3. If two rounds disagree on an axis by 2+ points, re-read BOTH tapes before marking either — the disagreement is usually one tape was over-graded (same-hour grading, the FAQ's trap) or one axis loaded in clothes the other round did not (the per-round axis stress table).
Fill-rule: the scoreboard's ONLY job is the offer rule's yes/no. A filled-with-vibes scoreboard gives you permission to book an interview the tape does not — which is precisely the failure mode this folder exists to prevent.

**The final offer check — 10 yes/no questions answered from the tape (a no is not a re-drill — it is a "do not book the interview yet" flag):**
1. Did every claim survive a WHO/WHEN/NUMBER probe without a retraction?
2. Did the incident narrations hold the FT-160 order with no 60-second silence?
3. Did every design decision carry a price and a why-not?
4. Did the elevator anchors survive the first question after them?
5. Did the S5 unknowns come out three-phase, zero bluffs?
6. Did the same artifact/digest/served-version story hold across ROUNDS without drifting?
7. Did the escalation and prevention sentences appear UNPROMPTED at least once?
8. Was the downgrade reflex faster than the third probe on the behavioral rounds?
9. Did the scoring sheets and reflections get filled — or did the round stop at "felt good"?
10. Is the lowest axis on the last two rounds above 5, and is the total above the expected-score model band?
Ten yeses = the interview is not a gamble, it is a presentation of rehearsed method. Any no = a named gap with a named fix, which is precisely what this file exists to produce.

**The expanded transcript line-grade (grade not just the answer — grade the LINE, as the panel does):**
Transcript says: "Refused means the port is closed — like, nothing is listening, or the firewall REJECTs it. Timeout means… the server is high load? Or the network."
Line-grade: "refused = closed/listening/REJECT" — technical 1pt (correct mechanism family); "not bound / wrong bind address" absent — the classic missing half, -1; "timeout means high load" — correct ONLY through the accept-queue-full path, but the "or the network" hedge splits it, so the line is a 6 on that clause: mechanism present, second-level not named; "like" is a communication -0.5 twice; the question-mark delivery on "high load" is uncertainty-hedging that rounds UP (it signals doubt, it does not name the gap). Net: the line scores technical 6, communication 6 — and the SAME sentence in the 7/10 sample above scores 8/8 because it named DROP/no-route/filtered and accept-queue, and stated the definitive-vs-ambiguous distinction. The line-grade shows the delta is never the topic — it is the completeness set and the delivery.

**Mock scores vs the quiet score (three ways the real interview differs from every mock in this file — the final calibration, so no 60/70 is a surprise):**
| Difference | What it costs a mock-trained candidate | The adjustment |
|---|---|---|
| Real panels do not issue clock-limits per question | the mock's per-segment caps sometimes carry the answer's SHAPE; without a cap, answers sprawl into ramble | defend every claim in ~90 seconds BY HABIT, not because a segment demands it |
| Real follow-ups can be silent — the pull-tested pause | a mock interviewer never just waits; the tape's "…" is where the panel's silence sits | rehearse the LET-ME-THINK beats out loud to use a silence, never to break from it in a panic |
| The real panel rounds UP the anxiety markers | a mock rounds down live-room nerves (that is the point of the safe grind); a real room inflates them | walk into the real room with the mock's low axis drilled twice — the quiet score is the mock score MINUS the calibration for touch, not the plus |
Adjustment-rule: add no grade to your mock average for "I will be calmer at the real one". Subtract one touch per low axis instead — the mocks are the calibrated maximum, and the real room's TV is the known cost.

**The morning-of re-zero (the 60 minutes before the real loop — order matters; the anchors must be the LAST thing in your head, not the first):**
| Time | Read | Why this order |
|---|---|---|
| T-60 | the three strongest transcripts from rounds 4–6 | re-hear your own speaking-shape — you are walking in with YOUR voice, not the file's |
| T-30 | THE ROUND-1 WORD-BANK + R3 SENTENCES THAT SCORE | the rapid and design registers, both still warm |
| T-15 | the six-line offer-ready card | anchors, narration order, STAR beats, unknown-shape — the compile-check |
| T-5 | nothing but the S1/S6 elevator + walls | the opening and closing anchors are the frame; everything inside is rehearsal already done |
Re-zero rule: the morning re-zero must END on the anchors because the panel's first question is the elevator's defense. Reading the deck until the door is how a candidate carries a file into the room instead of a method — the file stays home; the six lines do not.

**The offer-ready one-page (the summary card to hold on the day between the last mock and the real loop — six lines, each mapped to a round that built it):**
1. I open with three anchors I can defend at OPERATED, and I cut my own ceiling before you ask. (R1 S0 → R6 S1)
2. I read the incident in the narration order — symptom, scope, ranked hypotheses, cheapest discriminator — flat, numbered, deadline-announced. (R2)
3. I design by failure-cost: one artifact, digest-pinned, served-version verify, rolling-plus-canary-when-it-matters, and rollback with a bytes+migration test. (R3)
4. My STARs are four beats I can say back myself, and the downgrade reflex fires before the third probe. (R4)
5. Under a 90-minute clock I keep the register per act, and the last five minutes close the loop the way the first five opened it. (R5)
6. When I do not know, I name it, state the boundary, name the close, and hold the safe default — in that order, out loud. (R6 S5)
Card rule: if any of the six lines does not survive reading it back against your last tape, the mock that owns that line owns your next re-run. The card is not a promise — it is the compile-check of six rounds of rehearsal.

---

## FILE-LEVEL FINAL QC

| # | Check | Status |
|---|---|---|
| 1 | Contains exactly 6 rounds (T / R / S / B / H / F) with the required round-header format | PASS |
| 2 | Round matrix table at the top lists all 6 with durations and source assets | PASS |
| 3 | Every round contains: SCENARIO BRIEF, OPENING PROMPT (verbatim), S-blocks with model answers, SCORE TABLE (7 axes), REFLECTION (fill after), MUST FIX / SHOULD FIX / NICE TO HAVE | PASS |
| 4 | Every round ends with a 13-row QC CHECKLIST whose row 13 is the SELF-VERIFY sourcings row | PASS |
| 5 | Live-debug/reasoning segments present in R2, R5 (mini), and R6 (full) with narration score-points | PASS |
| 6 | The 30-SECOND ELEVATOR from file 16 is used in R1 S0 and closes R6 (S1 + S6 echo) | PASS |
| 7 | All cited FT IDs (101–160), chain IDs (14-01..14-14), and INCIDENT IDs (01–30) resolve to sibling files | PASS |
| 8 | All cited resume bullets (16-01..16-18) and the LIE-DETECTOR/ELEVATOR assets resolve to file 16 | PASS |
| 9 | HOW TO GRADE LIKE AN INTERVIEWER appendix present with per-axis measures and 4/10-vs-7/10 transcript sample | PASS |
| 10 | No emojis anywhere in the file | PASS |
| 11 | Fences balanced (every opening fence block is closed; no stray ```) | PASS |
| 12 | No TODO, placeholder, or unfinished phrasing; FILE line count within the 2,200–2,800 target band | PASS |
| 13 | SELF-VERIFY — every model answer grade is honest against the war-room claim levels; nothing in this file claims depth the sibling sessions do not prove | PASS |

VERDICT: **FILE COMPLETE.** Six scripted rounds, 7-axis scoring, narration-graded debugging, and a grader's appendix — the P5 defend phase's last mile. The mock system is only as honest as its transcription: grade what you said, not what you meant, and the MUST FIX list is the interview.
NEXT POINTER → 18-revision (7d / 14d / 30d / 1h / 15min plans built from the must-fix lists you recorded in rounds 1–6).
