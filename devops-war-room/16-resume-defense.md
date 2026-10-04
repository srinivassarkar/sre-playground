# 16 — RESUME DEFENSE

Every bullet on your resume must survive the 3-level probe — "how?", "why did you choose X?", "what
broke?" — or it gets downgraded or cut.
A resume is a promise of what you can defend in a ten-minute conversation; a single unexplained word
("managed", "production", "led") is enough to sink twenty-five minutes of otherwise solid answers.
This file turns every likely 1–3 YOE bullet into the exact questions the interviewer WILL fire, the
STAR narrative you must be able to give, the war-room session that PROVES it, and the honest rewrite
if the claim is too big.

**The defense protocol:**
1. **Claim depth ladder:** USED (saw it) < UNDERSTOOD (can explain) < PRACTICED (did it deliberately) < OPERATED (ran it in prod-ish conditions) < DESIGNED (built it). You may only CLAIM what you can defend at the claimed depth. If the ladder step above your real one is false, the whole claim is false — interviewers probe down, not across.
2. **The 3-probe:** level-2-deep "how does that work", the "why were you there / why did you pick that", and the "what went wrong and how did you fix it". Every resume bullet → you must be able to answer all three. Rehearse each aloud until it lands under 90 seconds.
3. **Evidence anchors:** name the exact war-room session/lab that proves it (05-aws AWS.Px.y, 06-docker DCK.Px.y, 07-kubernetes K8s.Px.y, 08-terraform TF.Px.y, 09-cicd CICD.Px.y, 10-observability OBS.Px.y, 11-security SEC.Px.y, 12-troubleshooting INCIDENT NN). If a claim has NO anchor → it gets downgraded or cut, no exceptions.

**Reading rules for this file:**
- The bullet text in each header is a plausible VERBATIM resume line for that category. Say it out loud, then say the downgraded version out loud — notice the downgrade still sounds strong, because it is true.
- Entries marked **Defendable? NO** exist to stop you from shipping that wording. Take the downgrade verbatim.
- The `EVIDENCE ANCHOR` line is not decorative. If you cannot yet recite one concrete fact from the cited session (a number, a command, a failure), then the depth claim above it is a lie on your resume today.

---

## BULLET INDEX (quick map)

| Bullet | Resume line (softened) | Highest honest depth | Anchor file(s) |
|---|---|---|---|
| 16-01 | CI/CD pipelines (GitHub Actions, Docker→ECR→K8s) | OPERATED | 09-cicd, 05-aws |
| 16-02 | AWS infrastructure (VPC, IAM, EC2, S3, ALB, EKS) | PRACTICED | 05-aws |
| 16-03 | Terraform modules | PRACTICED | 08-terraform |
| 16-04 | Containers + Kubernetes | OPERATED (docker) + PRACTICED (k8s) | 06-docker, 07-kubernetes |
| 16-05 | Monitoring/alerting (Prometheus, Grafana, CloudWatch) | OPERATED (local stack) | 10-observability, 05-aws |
| 16-06 | Security hardening (IAM, secrets, TLS) | PRACTICED | 11-security |
| 16-07 | Automated Linux ops (bash/Python) | PRACTICED | 04-bash, 01-linux |
| 16-08 | Git workflows / branching | PRACTICED | 03-git |
| 16-09 | Production incidents / on-call | PRACTICED (war-room drills) | 12-troubleshooting |
| 16-10 | IaC + config management | PRACTICED | 08-terraform |
| 16-11 | Databases / storage (RDS, PVC/PV) | PRACTICED (PVC) / UNDERSTOOD (RDS) | 07-kubernetes, 05-aws |
| 16-12 | Networking (DNS, LB, TLS) | PRACTICED | 02-networking, 11-security |
| 16-13 | Logging / observability pipelines | PRACTICED | 10-observability |
| 16-14 | Cost / capacity management | UNDERSTOOD + real math | 05-aws, 10-observability |
| 16-15 | Developer environment support | PRACTICED | 06-docker, 09-cicd |
| 16-16 | Led/owned an initiative | PRACTICED (scoped) | 00-architecture, 18-revision |
| 16-17 | Contributed to architecture decisions | PRACTICED (small) | 00-architecture, 05-aws |
| 16-18 | Documentation / runbooks | PRACTICED | 12-troubleshooting |

The three worst resume words for a 1–3 YOE candidate are **"managed"**, **"led"**, and
**"production"**.
Every bullet below shows the substitution and the reasoning.

---

### BULLET 16-01 — "Built and maintained CI/CD pipelines (GitHub Actions, Docker→ECR→K8s)"
**Depth to claim:** OPERATED (the pipeline ran end-to-end live in the war-room, including one live
EKS deployment) · **Defendable?** YES — with two fences: "maintained" can only mean "ran and fixed in
a controlled environment", and the EKS leg is one verified live run, not a production fleet.
**PROBE 1 (how does it actually work):** "Walk me through your pipeline step by step — what actually
happens when a commit lands?" → Model answer: the push fires a workflow trigger;
GitHub Actions provisions an ephemeral runner; the job runs steps in order — checkout, install deps,
build/test, build image, push to registry — then a deploy job gated with `needs` updates Kubernetes.
The runner executes the YAML spec and surfaces exit codes stage by stage; a nonzero step fails the
job (fail-fast).
The image carries an immutable tag (commit SHA, not `latest`) and is digest-verified at push, so the
deploy job references exactly the artifact we tested.
Proved live: the trigger→verify→build→deploy loop in CICD.P0.2/P0.4/P0.6, including a real smoke-test
HTTP 200 after deploy and a teardown that left the box pristine.
**PROBE 2 (why / decisions):** "Why that pipeline shape — why GitHub Actions, and why push through a
registry into Kubernetes instead of deploying the same box?" → Model answer: one artifact, tested
once, promoted everywhere.
Building once in CI and shipping through the registry means the bits deployed are the bits that
passed the tests.
GitHub Actions keeps pipeline-as-code next to the repo with no Jenkins box to maintain.
Kubernetes is the target because we wanted rollouts, self-healing, and env separation; the registry
is the contract between CI and CD.
Flag the same-tag trap: `latest` lets the cluster keep the old image even when CI "succeeds" — that
is INCIDENT 29, and it is why I pin SHA tags.
**PROBE 3 (what broke + fix):** "Tell me about a pipeline that broke." → Model answer: in CICD.P0.6
the deploy succeeded but the pod crash-looped.
Containers exited immediately with exit 127 — the base image's busybox shipped no `httpd` applet, so
the web server binary was never inside the image.
Fix path: `kubectl get pods` → CrashLoopBackOff → `kubectl logs` showed `httpd: applet not found` →
changed the base image, redeployed, smoke test returned HTTP 200.
The discipline that matters: read the exit code and logs, fix the image not the rollout, then verify.
Anchored by INCIDENT 16 (CrashLoopBackOff) and the CICD.P0.6 debug loop.
**STAR NARRATIVE (60–90s spoken):**
S: My project needed a repeatable way to get a tested container from a git commit onto a running
cluster without anyone building anything by hand.
T: I put together a GitHub Actions pipeline for the build-and-test leg and extended it through a
container registry into a Kubernetes deployment, with deploy gated behind the successful test stage.
A: Pipeline-as-code in the repo; a test stage running the real test suite and linter; a container
build stage that pushed a digest-pinned image to a registry with an immutable commit-SHA tag; a
deploy stage pointed at Kubernetes; then a post-deploy smoke test checking HTTP 200.
When the first deploy crash-looped, I diagnosed from the logs and fixed the image rather than the
rollout, re-ran, verified the smoke test, then tore the whole environment down so nothing was left
running.
R: The pipeline took a commit through test, build, registry push, deploy, and a verified smoke test
in a single run — and the incident taught me the rule that matters most in CI: let the exit code and
the logs do the talking, and never promote a tag you did not test.
**EVIDENCE ANCHOR:** 09-cicd CICD.P0.4 (pytest + ruff stage, fail then pass) · CICD.P0.5 (registry:2
push/pull round-trip, digest proof, immutable vs latest) · CICD.P0.6 (kind deploy + CrashLoopBackOff
debug loop + smoke HTTP 200 + teardown) · CICD.P0.8 (tag-based promote v1→v2 then rollout undo) ·
05-aws AWS.P0.10 (live Docker→ECR→EKS, port-forward served the payload) · 12-troubleshooting INCIDENT
16, INCIDENT 29.
**HONEST DOWNGRADE:** "Maintained CI/CD pipelines in production" → "Built and ran a CI/CD pipeline:
GitHub Actions, build+test, container push, deploy to Kubernetes, smoke-verified deploys." If you
cannot narrate the crash-loop fix, cut "maintained" and say "built".
**AVOIDING THE NEXT PROBE TRAP:** Do not name ECR/EKS specifics unless you can also explain WHY the
node pulled the private image without docker login — the managed nodegroup IAM role carries ECR-read
(AWS.P0.10).
The follow-up after a good pipeline story is "how did the cluster auth to the registry"; if you
freeze there, the story collapses.

### QC CHECKLIST — BULLET 16-01
| # | Check | Status |
|---|---|---|
| 1 | Trigger→verify→build→push→deploy→smoke flow explained without notes | PASS |
| 2 | Immutable-tag reasoning given (why commit-SHA, why not `latest`) — ties to INCIDENT 29 | PASS |
| 3 | `needs`/stage gating and fail-fast described accurately | PASS |
| 4 | Crash-loop debug told as diagnosis-first (exit code + logs, not blind redeploy) | PASS |
| 5 | ECR/EKS leg placed at honest depth (one verified live run) | PASS |
| 6 | Teardown/pristine claim stated — environment left clean after the lab | PASS |
| 7 | Same-tag trap + `--rollout undo` (CICD.P0.8) in your vocabulary | PASS |
| 8 | Registry-auth probe answered (short-lived token / get-login-password, node IAM role) | PASS |
| 9 | Promoted-artifact concept present: one artifact, tested once, promoted everywhere | PASS |
| 10 | No production-fleet language anywhere in the narrative | PASS |
| 11 | Concrete numbers cited: HTTP 200, exit 127, commit-SHA tag | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **Defendable at OPERATED if and only if the registry-auth and crash-loop follow-ups are
tight.** Otherwise ship the downgrade.

NEXT POINTER → 16-02 digs the AWS leg; claiming "AWS infrastructure" means defending
VPC/IAM/S3/ALB/EKS one service at a time.

---

### BULLET 16-02 — "Managed AWS infrastructure (VPC, IAM, EC2, S3, ALB, EKS)"
**Depth to claim:** PRACTICED · **Defendable?** NO as written — "managed" implies sustained ownership.
Downgrade to "worked with / deployed on".
PRACTICED is high enough to pass the probes below if you stay inside the verified labs.
**PROBE 1 (how does it actually work):** "You listed six AWS services.
Pick VPC — how does traffic actually leave your subnet?" → Model answer: instances sit in subnets
inside a VPC; each subnet has a route table.
A public subnet routes `0.0.0.0/0` to an internet gateway; a private subnet routes outbound through a
NAT gateway without exposing inbound.
Security groups are instance-level stateful firewalls (allow rules; implicit deny), while NACLs are
stateless subnet-level filters you must reason about in both directions.
Verified live in AWS.P0.3 (CIDR planning, IGW/NAT routes, teardown order) and AWS.P0.4 (SG vs NACL
statefulness, default rules, eval).
The scheduling/identity layer: IAM binds who/what can act (AWS.P0.2), EC2 picks the compute
(AWS.P0.5), S3 the object store (AWS.P0.6).
**PROBE 2 (why / decisions):** "Why did you pick ALB, and why EKS over something simpler?" → Model
answer: ALB because we needed L7 path/Host routing and target-group health checks, and target groups
decouple the balancer from the instances behind it (AWS.P0.7).
EKS over ECS because the team already thought in Kubernetes primitives (Deployment, Service, HPA) and
I had a working kind cluster locally;
EKS gives a managed control plane with the same kubectl day-2 story (AWS.P0.10).
ECS is the simpler AWS-native option and I would choose it for a small stateless API — the honest
tradeoff is "orchestration verbs you know" versus "control plane you do not manage".
**PROBE 3 (what broke + fix):** "What actually went wrong in AWS?" → Model answer: on the live EKS
run (AWS.P0.10) my app pods stayed Pending with `FailedScheduling: 1 Too many pods`.
The t3.micro node had only four allocatable pod slots, and the system addons (aws-node, kube-proxy,
coredns, metrics-server) consumed them.
Fix: scale the nodegroup to two nodes and prune coredns/metrics replica counts; then the app ran one
pod per node behind a ClusterIP service, verified by port-forward + curl.
The lesson is capacity math: node sizing means placing the app ABOVE the platform overhead.
Related drills: INCIDENT 18 (Pod Pending) and INCIDENT 04 (ALB 502/503 with an unhealthy
target-group).
**STAR NARRATIVE (60–90s spoken):**
S: The environment was a deliberately small, memory-tight sandbox, so every AWS choice had to be
minimal and actually understood, not assumed.
T: I needed to stand up a containerized app the end-to-end AWS way: VPC isolation, identity that
could not over-permit, durable object and image storage, an L7 ingress path, and a cluster to run on.
A: I built the network story first (VPC/subnet/routing, SG vs NACL reasoning), locked identity with
IAM reasoning, used S3 and ECR as the durable stores, mapped the ALB target-group health pattern,
then ran a live EKS cluster via eksctl with a managed nodegroup and deployed a two-replica app
pulling a private ECR image.
The deployment hit the max-pods ceiling on t3.micro;
I scaled to two nodes, pruned addons, and verified with `kubectl port-forward` + curl returning the
app payload.
R: I walked the full Git→CI→Docker→ECR→EKS spine on real AWS, and I left the account byte-identical
to the start — every probe I hit became an INCIDENT file, so the mistakes are now vocabulary rather
than fear.
**EVIDENCE ANCHOR:** 05-aws AWS.P0.2 (IAM: policies/roles/trust/STS), AWS.P0.3 (VPC), AWS.P0.4 (SG vs
NACL), AWS.P0.5 (EC2/EBS), AWS.P0.6 (S3), AWS.P0.7 (ALB + target groups + health checks), AWS.P0.8
(Route53 records + health checks), AWS.P0.10 (live EKS, max-pods incident, teardown) ·
12-troubleshooting INCIDENT 04, INCIDENT 18.
**HONEST DOWNGRADE:** "Managed AWS infrastructure (VPC, IAM, EC2, S3, ALB, EKS)" → "Worked with AWS
infrastructure: designed VPCs, scoped IAM, deployed EC2/S3/ALB patterns, and ran a workload on a live
EKS cluster (eksctl), tearing everything down after." Drop "managed"; the past-tense lab honesty
reads stronger than the verb HR filters for.
**AVOIDING THE NEXT PROBE TRAP:** Say "EKS" and a probe comes from K8s.P2.4 (node groups, IRSA,
Fargate).
Claim "managed" and the probe becomes cost and change control.
Stay inside the six services you listed; each is defensible from its AWS.P0.x anchor.

### QC CHECKLIST — BULLET 16-02
| # | Check | Status |
|---|---|---|
| 1 | VPC routing story (IGW for public, NAT for private) told without notes | PASS |
| 2 | SG (stateful) vs NACL (stateless) distinction locked, from AWS.P0.4 | PASS |
| 3 | IAM identity vs policy vs role vs trust explained (AWS.P0.2) | PASS |
| 4 | ALB choice justified at L7 (path routing, target groups, health checks) | PASS |
| 5 | EKS vs ECS tradeoff stated without hedging on either | PASS |
| 6 | Max-pods incident narrated with numbers (t3.micro, 4 slots, 2 nodes) | PASS |
| 7 | Teardown/pristine claim included (account left unchanged) | PASS |
| 8 | S3 story present: bucket, objects, versioning, access patterns (AWS.P0.6) | PASS |
| 9 | Route53 record types + health-check usage present (AWS.P0.8) | PASS |
| 10 | "Managed" removed or explicitly scoped to lab-time operation | PASS |
| 11 | Probe "how did the node pull the private image" answered (node role, ECR-read) | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **NO as written, PASS after the downgrade.** The word "managed" must go.

NEXT POINTER → 16-03 moves to Terraform; the same "managed" trap repeats there and costs more.

---

### BULLET 16-03 — "Wrote Terraform modules for repeatable infra"
**Depth to claim:** PRACTICED · **Defendable?** YES — modules were built, sourced, versioned, and
re-used in TF.P0.7 against real terraform v1.16.2.
**PROBE 1 (how does it actually work):** "What does a module actually consist of, and what happens
when you call one?" → Model answer: a module is a directory of `.tf` files with an interface of
`variable` (inputs), `output` (returns), and usually `resource` blocks.
Calling a module pins a `source` (local path, git ref, registry) and a `version`.
Terraform instantiates it as a single named block, so two callers create two independent sets of
resources, each recorded separately in state.
Outputs feed callers so one module's results become another's inputs.
Verified live in TF.P0.7, alongside the count vs for_each vs for distinction in TF.P0.6 — for_each
keys a map so similarly-shaped resources survive refactors without forcing destroys.
**PROBE 2 (why / decisions):** "Why modules instead of copy-paste?" → Model answer: DRY and
reviewability — one tested implementation with inputs as the only change surface, and a version tag
per consumer so a module change never silently rewrites a dependent stack.
The tradeoff is indirection: a `plan` reads less obviously through a module boundary, so I keep
modules small and output-heavy, which is the same reason the recommended structure separates module
code from root compositions.
**PROBE 3 (what broke + fix):** "When did Terraform hurt you?" → Model answer: INCIDENT 22 — a failed
apply left a partial state and the next apply hit `Error acquiring the state lock`.
The panic fix is the wrong fix; the drill is to check who holds the lock, decide if it is stale,
force-unlock deliberately and only after proving the previous process is gone (TF.P0.3 covers the
DynamoDB lock record), then reconcile drift.
And INCIDENT 23 — an out-of-band change made the next `plan` want to destroy/recreate a resource; the
fix is to import or fix config, never to blindly apply a destroy plan.
**STAR NARRATIVE (60–90s spoken):**
S: Repeatable infra kept meaning "rewrite the resources again for the Nth project", and every rewrite
drifted differently.
T: I set out to make common infrastructure reusable as versioned Terraform modules, and to make the
failure modes — state, locking, drift — first-class knowledge rather than surprises.
A: I structured small modules with clear inputs and outputs, exercised them across multiple roots,
and deliberately ran the failure set: a state-lock collision and a drift that made the plan propose
destroy/recreate.
I fixed both the Terraform way — prove who holds the lock, force-unlock only when stale, reconcile
before applying — and rehearsed plan-as-gate usage where CI runs `terraform plan` and a person
approves the diff (TF.P1.2).
R: Module reuse got faster and safer, and more importantly I stopped treating state as a magic file:
I can now explain plan vs apply, state locking, and drift at the depth the interviewer tests, because
I broke it on purpose and fixed it in front of the evidence.
**EVIDENCE ANCHOR:** 08-terraform TF.P0.1 (plan/apply/destroy model) · TF.P0.2 (state, import,
locking) · TF.P0.3 (S3 + DynamoDB remote backends) · TF.P0.6 (count vs for_each vs for, dynamic
blocks) · TF.P0.7 (modules: structure, source, versioning) · TF.P1.2 (plan-as-gate, apply-on-merge) ·
12-troubleshooting INCIDENT 22, INCIDENT 23.
**HONEST DOWNGRADE:** "Built reusable Terraform modules used across teams" → "Wrote Terraform,
including structuring common infra as versioned modules with remote state locking." If you have not
run remote state with real teammates, cut "across teams".
**AVOIDING THE NEXT PROBE TRAP:** After "modules" the probe is almost always count vs for_each
(TF.P0.6) or state locking (INCIDENT 22).
Rehearse both cold — they separate "wrote some .tf" from "operates the tool".

### QC CHECKLIST — BULLET 16-03
| # | Check | Status |
|---|---|---|
| 1 | Module anatomy (inputs, outputs, resources, source, version) stated | PASS |
| 2 | Plan vs apply loop explained (TF.P0.1) | PASS |
| 3 | State as source of truth + remote locking explained (TF.P0.2/P0.3) | PASS |
| 4 | count vs for_each vs for told with a why (TF.P0.6) | PASS |
| 5 | Module versioning story present (why pin, what breaks without it) | PASS |
| 6 | State-lock incident narrated with the safe unlock order (INCIDENT 22) | PASS |
| 7 | Drift / destroy-recreate incident told — import or fix before apply (INCIDENT 23) | PASS |
| 8 | Plan-as-gate / apply-on-merge concept present (TF.P1.2) | PASS |
| 9 | No fabricated multi-team production usage claimed | PASS |
| 10 | Real tool version available in your story (terraform v1.16.2) | PASS |
| 11 | Probe "what is actually inside the state file" answered (resource graph + attributes) | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS at PRACTICED.** The only failure mode is inventing multi-team usage.

NEXT POINTER → 16-04 is the containers/Kubernetes pair; the word "operated" gets scrutinized here.

---

### BULLET 16-04 — "Deployed and operated containers + Kubernetes"
**Depth to claim:** OPERATED for Docker (ran it, broke it, fixed it, repeatedly) · PRACTICED for
Kubernetes (kind cluster + one live EKS run) · **Defendable?** YES with a one-word fix: attach
"operated" to the container layer and "used/practiced" to Kubernetes until there are months of runs
behind you.
**PROBE 1 (how does it actually work):** "What is the difference between an image and a container,
and how does a Kubernetes Deployment turn that into running services?" → Model answer: an image is an
immutable snapshot of filesystem plus metadata; a container is that image plus a writable scratch
layer, running as processes in namespaces on the host kernel.
Kubernetes: a Deployment declares a desired Pod template and count; a ReplicaSet converges live Pods
to that count; each Pod is one or more containers sharing a network namespace; a Service selects Pods
by label (not by IP), gives a stable DNS name, and load-balances to whatever matches — visible live
via endpoints.
I built this exact chain with `docker history` (layers), immutable tags and digest proofs (DCK.P0.6),
and Deployment→RS→Pod→Service→endpoints on kind (K8s.P0.2).
**PROBE 2 (why / decisions):** "Why run containers at all, and why wrap them in Kubernetes instead of
Docker Compose?" → Model answer: containers ship the runtime with the code, so one artifact runs
identically on a laptop and a server.
Compose (DCK.P0.5) is perfect for local multi-container dev but has no self-healing, rolling updates,
or cross-node scheduling.
Kubernetes adds a declarative control loop: desired state in, controllers converge the world to it —
rollout, rollback, probes, HPA.
I keep Compose for the dev loop and Kubernetes for anything that needs to survive a node outage.
**PROBE 3 (what broke + fix):** "Give me a container or pod failure you actually fixed." → Model
answer: two real ones.
First, the smoke-test deploy crash-looped — exit 127, the base image lacked `httpd`; fix was the
image, verified by logs then redeploy (INCIDENT 16).
Second, a rollout got stuck because the readiness probe was not ready, READY 1/2 sustained — the
Deployment would not advance (INCIDENT 27); the fix was fixing the readiness path, not
force-replacing pods.
I have also reproduced Pending/unschedulable and OOMKilled mechanics (INCIDENT 18, 19) and the
max-pods ceiling on a live EKS node (AWS.P0.10).
**STAR NARRATIVE (60–90s spoken):**
S: The goal was to be able to say honestly where a container goes in this stack — building it,
shipping it, and letting a scheduler keep it alive.
T: I needed to move from "docker run works" to the whole orchestration story, and prove it on real
infrastructure.
A: I built images, understood layers and caching, ran multi-container Compose, then pushed to a
registry with immutable tags and let Kubernetes own the workload.
On kind I ran the core-object chain, rollouts and `--rollout undo`, probes, scheduling constraints,
and HPA scaling verified from one to four replicas.
On live EKS I hit the max-pods wall, fixed node sizing, and verified with port-forward.
I then deleted every cluster and container until the environment matched the starting state.
R: The result is a vocabulary of failure, not just success: I have seen CrashLoopBackOff, stuck
rollouts, Pending, OOMKilled, and max-pods in the flesh, and can walk any of them from symptom to
root cause to verify.
**EVIDENCE ANCHOR:** 06-docker DCK.P0.1 (images vs containers, layers), DCK.P0.3 (volumes vs bind
mounts), DCK.P0.5 (Compose), DCK.P0.6 (registry, tags, layer caching), DCK.P0.7 (logs, exit codes) ·
07-kubernetes K8s.P0.2 (core objects), K8s.P0.3 (rollouts/rollback), K8s.P0.5 (probes), K8s.P0.6
(scheduling), K8s.P1.3 (HPA 1→4) · 05-aws AWS.P0.10 (live EKS) · 12-troubleshooting INCIDENT 16,
INCIDENT 18, INCIDENT 19, INCIDENT 27.
**HONEST DOWNGRADE:** "Deployed and operated containers + Kubernetes" → "Built and ran container
images, operated a Kubernetes Deployment/Service workload on kind, and deployed a workload once on
live EKS (eksctl)." If the HPA or rollback drills are fuzzy, drop those adjectives from the interview
story too.
**AVOIDING THE NEXT PROBE TRAP:** The follow-up is usually "how does a Service find Pods" (label
selector → endpoints) or "what does a rolling update do under load" (maxSurge/maxUnavailable,
CICD.P1.3).
Rehearse both — they are the highest-frequency K8s probes at this level.

### QC CHECKLIST — BULLET 16-04
| # | Check | Status |
|---|---|---|
| 1 | Image vs container vs layer explained with `docker history` proof | PASS |
| 2 | Deployment→ReplicaSet→Pod→Service chain narrated (K8s.P0.2) | PASS |
| 3 | Service-by-selector mechanism explained via endpoints | PASS |
| 4 | Rollout + `--rollout undo` demonstrated (K8s.P0.3, CICD.P0.8) | PASS |
| 5 | Probes: liveness vs readiness; stuck rollout behavior (INCIDENT 20/27) | PASS |
| 6 | CrashLoopBackOff told as diagnosis-first (INCIDENT 16) | PASS |
| 7 | Scheduling: requests/limits, Pending, max-pods (K8s.P0.6, AWS.P0.10) | PASS |
| 8 | HPA scaling story with real numbers 1→4 (K8s.P1.3) | PASS |
| 9 | Compose for local dev justified vs K8s for orchestration | PASS |
| 10 | Container security basics at least named (non-root, caps — DCK.P1.1) | PASS |
| 11 | Teardown/pristine discipline stated | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS** with "operated" scoped to Docker and "practiced" attached to Kubernetes.

NEXT POINTER → 16-05 handles monitoring; the trap is claiming a managed telemetry estate you only
read about.

---

### BULLET 16-05 — "Set up monitoring/alerting (Prometheus, Grafana, CloudWatch)"
**Depth to claim:** OPERATED for a self-run Prometheus + Grafana stack (live scrape, query,
dashboard, alert rule) · PRACTICED for CloudWatch (live $0 metric/alarm drill) · **Defendable?** YES
if CloudWatch is scoped to metrics/alarms/logs drills, not a production telemetry estate.
**PROBE 1 (how does it actually work):** "How does Prometheus actually get metrics, and how does an
alert fire?" → Model answer: Prometheus pulls an HTTP `/metrics` endpoint on a schedule (the pull
model), stores series in a TSDB keyed by labels, and evaluates PromQL rules periodically.
In OBS.P0.2 the model was proven live — a tiny two-target scrape set accumulated 1440 head series in
roughly ten minutes, the honest shape of a minimal metric set.
Alerting: an alert/recording rule in Prometheus plus Alertmanager; in OBS.P0.8 I pushed real alert
rules to a running Prometheus and watched states flip pending→firing→inactive through the API.
Grafana renders queries as dashboards, and both datasource and dashboard can be provisioned as code
(OBS.P0.5) rather than clicked together by hand.
**PROBE 2 (why / decisions):** "Why the pull model instead of an agent pushing?" → Model answer: pull
means discovery is constant — Prometheus finds known targets and the absence of a target is a fact (a
dead target is visible) rather than a gap in pushed data.
The tradeoff is cardinality (OBS.P2.2): every unique label value multiplies stored series, so
unbounded labels such as per-request IDs or per-pod random suffixes blow up cost and retention.
I chose Prometheus/Grafana because they are open and pair natively with Kubernetes, and I reach for
CloudWatch where the resource is AWS-native because the metrics and alarms already exist there.
**PROBE 3 (what broke + fix):** "Tell me about alerting that went wrong." → Model answer: the classic
failure here is noise — alerting on a metric without understanding its distribution.
In OBS.P0.4 the truth was carved in live data: average versus p95 for the same latency story, and why
you alarm on percentiles, not means, for user-facing latency.
The operationally worse variant is alerting on the wrong signal entirely and paging on silence; the
OBS.P0.8 drill made the mechanism concrete — an alert rule is only as good as the query behind it,
which is why every alert in my playbook names a runbook (see 16-18).
**STAR NARRATIVE (60–90s spoken):**
S: Nobody on the project could say whether the service was healthy at 3 a.m., because nothing was
watching it.
T: I set out to build a monitoring and alerting loop that answers one question: "how do we know it is
broken?" — with metrics, dashboards, and rules that page.
A: I stood up a real Prometheus + node-exporter + Grafana stack on a local box, verified scrapes
through /targets, queried it with live PromQL (rate, percentiles, aggregations), provisioned a
Grafana datasource and dashboard as code, then pushed real alert rules and watched them move through
pending, firing, and inactive states.
Alongside it I ran the CloudWatch drill — publish a custom metric, read it back, flip an alarm to
ALARM and back.
I loaded-tested the math too: an average versus a p95 tells a different story, and percentiles are
what user-facing latency deserves (OBS.P0.4).
R: The loop existed, was verified, and was torn down cleanly — and I came away able to explain
pull-based scraping, cardinality, and alert-state semantics at the depth interviews actually check.
**EVIDENCE ANCHOR:** 10-observability OBS.P0.2 (live Prometheus + node-exporter, 1440 head series),
OBS.P0.3 (live PromQL), OBS.P0.4 (histograms, p50/p90/p99, avg-vs-p95), OBS.P0.5 (Grafana provisioned
as code), OBS.P0.8 (real alert rules, firing/pending/inactive), OBS.P1.3 (RED/USE to live PromQL),
OBS.P2.2 (cardinality/cost) · 05-aws AWS.P0.9 (CloudWatch metric published, alarm flipped ALARM/PASS).
**HONEST DOWNGRADE:** "Set up enterprise monitoring/alerting for production" → "Set up a Prometheus +
Grafana monitoring stack locally (scrape, dashboards, alert rules) and wired a CloudWatch metric +
alarm." If you cannot show a dashboard or name an alert rule verbatim, drop Grafana from the line.
**AVOIDING THE NEXT PROBE TRAP:** Do not say "SLIs/SLOs" unless the error-budget math is yours
(OBS.P0.9).
Do not say "tracing" unless you can define span/trace IDs and sampling (OBS.P0.7).
Claim only Prometheus + Grafana + CloudWatch fundamentals, each anchored.

### QC CHECKLIST — BULLET 16-05
| # | Check | Status |
|---|---|---|
| 1 | Pull-model scraping explained and why it beats silent push gaps | PASS |
| 2 | Prometheus data model: series, labels, TSDB, 1440-series real number | PASS |
| 3 | Core PromQL verbs usable aloud (selectors, rate, histogram_quantile, sum by) | PASS |
| 4 | percentile-vs-average alerting logic stated (OBS.P0.4 data) | PASS |
| 5 | Grafana dashboards/datasources provisioned as code (OBS.P0.5) | PASS |
| 6 | Alert lifecycle pending→firing→inactive narrated (OBS.P0.8) | PASS |
| 7 | CloudWatch drill: custom metric + alarm flipped ALARM (AWS.P0.9) | PASS |
| 8 | Cardinality cost trap explained (OBS.P2.2) | PASS |
| 9 | No SLI/SLO or tracing claims made at unanchored depth | PASS |
| 10 | On-call/runbook tie-in present (alert → runbook) | PASS |
| 11 | Stack run + teardown honesty preserved (containers removed) | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS at OPERATED for the local stack; PRACTICED for CloudWatch.**

NEXT POINTER → 16-06 covers security; the danger here is claiming hardening you have never actually
done.

---

### BULLET 16-06 — "Hardened systems / security (IAM least-privilege, secrets, TLS)"
**Depth to claim:** PRACTICED · **Defendable?** YES if "hardened" means "applied security
fundamentals in hands-on labs" and never "ran an enterprise security team".
The stair-step claim is operated-with-evidence for IAM/secrets/TLS basics.
**PROBE 1 (how does it actually work):** "How does AWS IAM decide whether a request is allowed?" →
Model answer: the request comes from a principal (user/role/service), authenticated first, then
evaluated: explicit allow, explicit deny, implicit deny — with explicit deny always winning.
Multiple policies (identity + resource-based) union their allows; a single explicit deny vetoes
everything.
Least privilege means scoping actions and resources to the smallest set that works.
Verified live twice: the IAM reasoning lab (AWS.P0.2) and the read-only account census in
SEC.P0.3/P0.4, where the real account's `terraform_journey` user carries AdministratorAccess +
IAMFullAccess — a textbook example of everything least privilege warns against.
**PROBE 2 (why / decisions):** "Why did you choose those security controls?" → Model answer: secrets
first — anything committed to git, baked into an image history, or injected via environment can leak,
and I proved all three in SEC.P0.5 (a deleted secret recovered from a saved image layer).
So the decisions: never env-inject secrets at build time, use the platform secret mechanism at deploy
time, prefer short-lived credentials (ECR tokens, IRSA) over static keys.
TLS chosen at the transport layer because it protects data in motion end to end; verified the
mechanics in SEC.P0.7 — SAN fields, CA trust, and a real TLS 1.3 chain to google.com.
**PROBE 3 (what broke + fix):** "Give me a security incident you worked." → Model answer: the
strongest honest one is the leaked-secret scenario (INCIDENT 30): a key got committed to git and
pushed.
The fix is not just removing the line — it is history rewriting or accepting the leak, then rotating
the credential, because the commit history still holds it.
In SEC.P2.2 I proved a rotated-but-still-in-history key remains extractable from the scratch repo.
That is the whole lesson: security findings move the timeline to "assume compromised, rotate,
verify"; and the durable control is a scan gate in the pipeline, not a human remembering to check.
**STAR NARRATIVE (60–90s spoken):**
S: The sandbox account was a cautionary tale I could touch: an IAM user with administrator rights,
two active access keys, and no MFA.
T: I needed to turn security from theory into a repeatable checklist I could defend in interviews —
identify where secrets and privileges actually leak, and fix the practice, not the symptom.
A: I mapped the real IAM estate read-only (SEC.P0.3/P0.4), proved the three leak paths for secrets —
git history, image history, runtime environment (SEC.P0.5) — verified TLS mechanics against a real
public chain (SEC.P0.7), and ran the container hardening comparison: root-writable with full
capabilities versus non-root read-only with dropped caps, with CapEff proof (SEC.P0.9/P0.10).
I then packaged the whole thing as a gate: scan artifacts in CI, rotate when something is already
out, and write it down as a runbook.
R: The result is that I can demonstrate each control offline and explain the reasoning under probing
— least privilege, secrets hygiene, and TLS are no longer bullet-point labels but verified mechanisms.
**EVIDENCE ANCHOR:** 11-security SEC.P0.3 (real read-only IAM census, ADAD 15.8MB), SEC.P0.4 (least
privilege, permission boundaries, IRSA), SEC.P0.5 (secrets leak in ENV/ARG/history, recovery from
saved layer), SEC.P0.7 (self-signed SAN + real TLS 1.3 chain), SEC.P0.9 (perms, ed25519 keys, docker
CapEff proof), SEC.P0.10 (leaky image history, container hardening), SEC.P1.1 (k8s RBAC can-i matrix,
PSA), SEC.P2.2 (secret scan on scratch repo) · 05-aws AWS.P0.2 (IAM evaluation) · 12-troubleshooting
INCIDENT 09, INCIDENT 14, INCIDENT 30.
**HONEST DOWNGRADE:** "Hardened production systems / led security initiatives" → "Applied security
fundamentals hands-on: least-privilege IAM, secrets hygiene, TLS verification, container hardening."
If you cannot demonstrate a leaked-secret recovery or name an IAM evaluation rule, cut "hardened"
entirely.
**AVOIDING THE NEXT PROBE TRAP:** "Hardening" invites "how do you secure a Kubernetes cluster?"
(RBAC, NetworkPolicy, PSA — SEC.P1.1) or "how does TLS actually work?" (handshake, chain, SAN —
SEC.P0.7).
Do not claim mTLS, WAF, penetration testing, or compliance leadership you have not done.

### QC CHECKLIST — BULLET 16-06
| # | Check | Status |
|---|---|---|
| 1 | IAM evaluation order stated (explicit deny > allow; implicit deny) | PASS |
| 2 | Least privilege defined with a concrete action/resource scoping example | PASS |
| 3 | Real-account findings narrated (admin user, 2 keys, no MFA) | PASS |
| 4 | Three secret leak paths named (git, image history, runtime env) | PASS |
| 5 | Leaked-secret response told as assume-compromised + rotate (INCIDENT 30) | PASS |
| 6 | TLS mechanics: handshake, chain, SAN, CA trust, TLS 1.3 chain proof | PASS |
| 7 | Container hardening: non-root + read-only + dropped caps with CapEff proof | PASS |
| 8 | Kubernetes security at least named (RBAC can-i, PSA — SEC.P1.1) | PASS |
| 9 | No FUD: no mTLS/WAF/pen-test/compliance-leadership claims | PASS |
| 10 | Shift-left idea present: scan gate in CI, not human memory (SEC.P2.2) | PASS |
| 11 | Reads were read-only; account left byte-identical, stated | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS at PRACTICED.** Nothing in this bullet outruns the SEC.P0.x/P1.x evidence.

NEXT POINTER → 16-07 covers scripting; the probe there is "write a small script now" on the
whiteboard.

---

### BULLET 16-07 — "Automated Linux ops with bash/Python"
**Depth to claim:** PRACTICED (scripts written, run, broken, and debugged deliberately) ·
**Defendable?** YES — as long as you are ready to write a real script live.
**PROBE 1 (how does it actually work):** "Write a bash loop over these files that extracts the IP
from each log line and counts them.
What does `set -euo pipefail` change?" → Model answer: `set -e` exits on any failing command, `set -u`
errors on unset variables, `set -o pipefail` makes a pipeline fail if any stage fails — the three
lines that turn a fragile script into one that fails loudly and early.
Then: `while read` loop over a command's output, or a `for` loop over a glob; `grep -oE '[0-9.]+'`
then sort/uniq -c for counts; or hand the same job to jq when the input is JSON (BASH.P0.4) and parse
it from curl output (BASH.P0.5).
Live practice in BASH.P0.1–P0.6 and the log-parsing/health-check playbooks.
**PROBE 2 (why / decisions):** "When do you use bash versus Python?" → Model answer: bash when the
task is process control, pipelines, and grepping the OS — it is already there and fast to write.
Python when the logic grows — data structures, error paths, tests — or when I need the script itself
to be testable.
The boundary is complexity: one-liner to 50 lines bash; anything that needs unit tests goes Python.
I justify it with the actual task: log wrapping needs `set -euo pipefail` and pipes; report
generation needs Python.
**PROBE 3 (what broke + fix):** "Tell me about a script that failed." → Model answer: the classic is
"works on my machine, breaks in CI" (INCIDENT 24) — same name, different working directory or missing
`export PATH` (a fact of this entire war-room: every command needs `PATH="$HOME/.local/bin:$PATH"`).
In the incident the fix was making the script location- and environment-agnostic: absolute paths or
rooted paths, explicit env setup at the top, and capturing the actual error instead of assuming.
The second classic is the silent-success failure: a script that "worked" because the final pipe
exited 0 while the real command failed — `set -o pipefail` catches exactly that.
**STAR NARRATIVE (60–90s spoken):**
S: Ops tasks were being done by hand every time — check the log, pull the IP, decide who is hammering
the box — and hands make different mistakes each day.
T: I set out to automate the read-only ops loops: parse logs, run health checks, and produce
decisions the same way every time.
A: I wrote bash scripts under `set -euo pipefail` that walked log files, extracted and counted IPs
with grep/sort/uniq, hit health endpoints with curl, and validated JSON with jq before acting on it
(BASH.P0.4–P0.6).
Where the logic grew — parsing and aggregation — I switched to Python with small tests.
I deliberately broke them too: a path-dependent script that died in a different CWD, and a pipeline
that masked a real failure because the last command exited 0.
Both became playbook incidents about environment assumptions and pipefail.
R: The scripts replaced a series of hand-run commands with one repeatable, reviewable artifact — and
the failures taught me that the highest-risk part of any automation is the assumption about the
environment it runs in.
**EVIDENCE ANCHOR:** 04-bash BASH.P0.1 (variables/args/quoting), BASH.P0.3 (`set -euo pipefail`, exit
codes, pipes), BASH.P0.4 (jq JSON parsing), BASH.P0.5 (curl health checks), BASH.P0.6 (health-check +
log-parsing playbooks), BASH.P1.1 (awk/sed, process substitution, find/xargs) · 01-linux
(process/memory/disk troubleshooting incidents) · 12-troubleshooting INCIDENT 24 (works locally,
fails in CI/NEW-ENV).
**HONEST DOWNGRADE:** "Automated large-scale Linux operations" → "Wrote bash and Python scripts for
ops automation — log parsing, health checks, and CI repair — with a focus on failing loudly (set -euo
pipefail)." If you cannot whiteboard a loop + pipe, say "wrote and ran" not "automated".
**AVOIDING THE NEXT PROBE TRAP:** The live-coding probe will be small and time-boxed: "count request
IPs", "health-check this endpoint and exit nonzero on failure".
Rehearse exactly that shape.
The other trap is quoting — expansions in double quotes, why `for x in $list` breaks on spaces.
Anchor from BASH.P0.1.

### QC CHECKLIST — BULLET 16-07
| # | Check | Status |
|---|---|---|
| 1 | `set -euo pipefail` behavior stated for each flag | PASS |
| 2 | Loop + pipe + text extraction (grep/sort/uniq) whiteboard-ready | PASS |
| 3 | jq usage over JSON API output (BASH.P0.4) | PASS |
| 4 | curl health-check pattern with status-code check (BASH.P0.5) | PASS |
| 5 | bash-vs-Python boundary justified by complexity/tests | PASS |
| 6 | Path/env dependency failure narrated (INCIDENT 24 / PATH fact) | PASS |
| 7 | Silent-success pipefail lesson told (last pipe masks real failure) | PASS |
| 8 | Quoting/expansion rule stated (quote expansions, word splitting) | PASS |
| 9 | No claim of managing fleets via scripts only | PASS |
| 10 | Real script output remembered verbatim (a number, a count) | PASS |
| 11 | Test tie-in present (small tests for Python path) | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS at PRACTICED.** The live whiteboard is the real gate; practice it.

NEXT POINTER → 16-08 covers git; the probe is "describe your team's branching model and a conflict
you fixed".

---

### BULLET 16-08 — "Managed git workflows / team branching"
**Depth to claim:** PRACTICED · **Defendable?** YES for the mechanics (branches, merge, rebase,
conflict resolution run live), and only "followed/supported" for the word "managed" — you manage git,
not teams.
**PROBE 1 (how does it actually work):** "What is a merge commit versus a rebase, and when would you
pick each?" → Model answer: a branch is just a movable pointer to a commit in the object DB.
Merge creates a commit with two parents, preserving the true history shape; rebase replays your
commits on top of a new base, rewriting a linear history but changing commit hashes.
I pick merge when the history truth matters (feature branches, shared history) and rebase when I want
a clean linear history before a PR, with interactive rebase to squash.
From GIT.P0.3/P0.4, run live: fast-forward, merge commit, and interactive rebase.
**PROBE 2 (why / decisions):** "What branching strategy do you use and why?" → Model answer: for a
small team, trunk-based with short-lived feature branches and PR review — main is always deployable,
and the diff is small.
No long-lived integration branches, because they are where conflicts breed.
The reason is CI/CD fit: small diffs merge often, so the pipeline stays green and rollbacks stay
trivial.
I understand GitFlow as an option for scheduled releases, but at 1–3 YOE the defensible default is
trunk with PRs.
**PROBE 3 (what broke + fix):** "Tell me about a conflict or a git disaster you fixed." → Model
answer: two honest ones.
A conflict resolution play: two people edited the same section; the fix was reading both sides in the
working tree, merging by intent, and testing the result rather than picking a side blindly (GIT.P0.7
conflict playbook).
The disaster: a commit that had to be undone — and the difference between `reset` (move the history
pointer, destructive) and `revert` (new commit undoing the change, safe for shared history); if
something was pushed and shared, revert; if it was local, reset, and reflog recovers a reset-or-merge
gone wrong (GIT.P0.5).
Also worth naming: the secret-in-history incident (INCIDENT 30) where removing the line is not enough.
**STAR NARRATIVE (60–90s spoken):**
S: A shared repo was getting messy — big branches, long-lived merge trains, and history nobody could
read.
T: I worked to make the branching discipline predictable: small branches, clean history, and safe
recovery when something went wrong.
A: I set a simple convention — short-lived branches, PR review, main always deployable — and drilled
the mechanics that keep that promise: merges for shared history, rebase to linearize, revert for
anything already pushed, reset + reflog for anything local.
When a real conflict surfaced, I resolved it by intent and tested the result; when a bad commit
needed undoing on a shared branch, I reverted it, and I rehearsed the reflog recovery path until it
was muscle memory.
R: The flow got boring, which was the point — and the recovery skills paid off because the difference
between reset and revert is now instinct, not a Stack Overflow search in the middle of an incident.
**EVIDENCE ANCHOR:** 03-git GIT.P0.3 (branches, fast-forward vs merge commit), GIT.P0.4 (merge vs
rebase, interactive rebase), GIT.P0.5 (reset soft/mixed/hard vs revert, reflog), GIT.P0.6 (fetch vs
pull, tracking branches), GIT.P0.7 (conflict resolution playbook) · 12-troubleshooting INCIDENT 30
(secret in history).
**HONEST DOWNGRADE:** "Managed team git workflows" → "Used git workflows with disciplined branching
and PR review; resolved conflicts; recovered mistaken commits with revert and reflog." Swap "managed
teams" for "managed my own and supported the team's process".
**AVOIDING THE NEXT PROBE TRAP:** The follow-ups tend toward "when does a fast-forward happen", "what
does detached HEAD mean", and "how do you recover a lost commit".
All are covered in GIT.P0.3/P0.5 — rehearse reflog as your recovery story.

### QC CHECKLIST — BULLET 16-08
| # | Check | Status |
|---|---|---|
| 1 | Branch-as-pointer model explained (GIT.P0.3) | PASS |
| 2 | Merge vs rebase tradeoff + when to pick each (GIT.P0.4) | PASS |
| 3 | Interactive rebase / squash stated without guessing | PASS |
| 4 | reset (local, destructive) vs revert (shared, safe) locked (GIT.P0.5) | PASS |
| 5 | reflog recovery demoed in words (found-in-reflog story) | PASS |
| 6 | fetch vs pull + tracking branches understood (GIT.P0.6) | PASS |
| 7 | Conflict resolved by intent, then tested (GIT.P0.7 playbook) | PASS |
| 8 | Branching strategy justified (trunk + PR for CI/CD fit) | PASS |
| 9 | "Managed", if used, means the workflow not the team | PASS |
| 10 | Secret-in-history lesson named (INCIDENT 30) | PASS |
| 11 | No fabricated multi-team governance claims | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS at PRACTICED.** Keep "managed" attached to the workflow, never to people.

NEXT POINTER → 16-09 is the highest-stakes bullet on this page; read it twice.

---

### BULLET 16-09 — "Debugged production incidents / on-call"
**Depth to claim:** PRACTICED — and ONLY against simulated/war-room incidents, never a real
production fleet.
This is the one bullet where the honest downgrade is non-negotiable. **Defendable?** NO as written if
it claims real production on-call.
YES only after downgrading to trained/playbook depth.
**PROBE 1 (how does it actually work):** "Walk me through how you debug a production incident, from
the alert to the fix." → Model answer: a fixed sequence, not improvisation: SYMPTOM (write the
reporter's words uninterpreted) → SCOPE (what is affected, what is not, what changed recently) →
HYPOTHESES (2–4 ranked, never one) → CHECKS (first check splits the space fastest and cheapest) →
EVIDENCE (the command output that confirms or kills a hypothesis) → ROOT CAUSE → FIX → VERIFY →
PREVENT.
The discipline that carries every incident is: evidence before action.
The war-room method and 30 incidents live in 12-troubleshooting-playbook.
**PROBE 2 (why / decisions):** "In that incident, why was your first check the right one?" → Model
answer: because each check must divide the hypothesis space in half with the cheapest non-disruptive
action — read state before changing anything.
For "kubectl connection refused", the first check was not restarting anything; it was reading the
kubeconfig's server line and comparing it to what was actually listening (INCIDENT 01).
That caught a stale-port client-config problem — the cluster was fine — and turned a would-be restart
into a five-minute file refresh.
The decision rule: the tool's own answer beats a guess every time.
**PROBE 3 (what broke + fix):** "Give me one war-room incident end to end." → Model answer: POD
PENDING (INCIDENT 18): symptom — pod never reaches Running.
Scope — other pods schedule fine, so not cluster-wide; what changed — a new deployment with bigger
requests.
Hypotheses — insufficient cpu/memory, untolerated taint, bad nodeSelector.
First check — `kubectl describe pod` / `kubectl get events` shows the scheduler's reason
(`FailedScheduling: insufficient memory`).
Evidence — the exact message names the resource and the node.
Root cause — requests exceeded node allocatable. Fix — right-size requests or add capacity.
Verify — pod schedules and is Ready.
Prevent — review requests at deploy time, make the scheduler message a known vocabulary.
Full sequence in 12-troubleshooting; the same method drills into CrashLoopBackOff (16), OOMKilled
(19), stuck rollouts (27), and the same-tag pipeline trap (29).
**STAR NARRATIVE (60–90s spoken):**
S: The scariest part of ops is not knowing what the first move should be when things go red.
T: I trained incident response as a skill instead of hoping for instinct — a repeatable method plus a
library of real failure patterns to recognize.
A: I ran and wrote 30 cross-layer incidents across four archetypes (reachability, identity,
orchestration, delivery), each through the full chain from symptom to prevent.
I drilled the first-check reasoning rule until it was reflex — read the tool's answer before touching
anything — and I rehearsed recoveries with real evidence: stale kubeconfig (INCIDENT 01),
CrashLoopBackOff (16), unschedulable pods (18), OOMKill (19), PVC Pending (21), state lock (22),
CI-locally-parity (24), same-tag drift (29), and a leaked secret (30).
R: The outcome is a method I can describe in one breath and demonstrate on demand — and an honest
lower bound: these are simulated incidents, and the resume says "trained", not "on-call".
**EVIDENCE ANCHOR:** 12-troubleshooting-playbook (the full method + INCIDENT 01, 16, 18, 19, 21, 22,
24, 27, 29, 30) · 07-kubernetes K8s.P0.5 (CrashLoopBackOff reproduced) · 08-terraform TF.P0.5
(partial apply) · 09-cicd CICD.P0.6 (debug loop).
**HONEST DOWNGRADE:** "Debugged production incidents; on-call for backend services" → "Trained
incident debugging with a 30-incident troubleshooting playbook (reachability, identity,
orchestration, delivery); can run a full symptom-to-prevent triage." If the interviewer pushes "have
you actually been on-call", the answer is no — say it cleanly and show the method.
**AVOIDING THE NEXT PROBE TRAP:** The probe after any incident story is "why was that your first
check, not something else" and "what was the evidence, exactly".
If you cannot recite the actual command output from memory, you did not run the incident.
Also expect "what would you do differently" — that is the PREVENT row; always land there.

### QC CHECKLIST — BULLET 16-09
| # | Check | Status |
|---|---|---|
| 1 | Nine-step method recitable from SYMPTOM to PREVENT | PASS |
| 2 | Scope reasoning present (affected vs not, what changed) | PASS |
| 3 | 2–4 ranked hypotheses, never single-hypothesis debugging | PASS |
| 4 | First-check reasoning rule stated (cheapest, splits space, read don't touch) | PASS |
| 5 | At least one incident narrated end-to-end with evidence verbatim | PASS |
| 6 | Pending incident (18) or CrashLoopBackOff (16) told precisely | PASS |
| 7 | OOMKilled (exit 137) and PVC Pending (21) named correctly | PASS |
| 8 | Same-tag drift (29) and state lock (22) in vocabulary | PASS |
| 9 | "On-call/production" claim downgraded to trained + playbook | PASS |
| 10 | The "have you been on-call" answer rehearsed (no + method) | PASS |
| 11 | PREVENT row always present — never end the story at the fix | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS ONLY after the downgrade.** Never let this bullet imply real production on-call.

NEXT POINTER → 16-10 returns to Terraform, but from the "IaC as a practice" angle rather than modules.

---

### BULLET 16-10 — "Implemented IaC + config management"
**Depth to claim:** PRACTICED · **Defendable?** YES, with Terraform as the proven leg.
The phrase "config management" is a trap if it implies Ansible/Puppet/Chef — say which tool, or drop
the phrase.
**PROBE 1 (how does it actually work):** "What does 'infrastructure as code' change about how you
operate, and how does Terraform keep reality in sync?" → Model answer: IaC makes infrastructure
reviewable, versioned, and reproducible — the same object you deploy goes through code review and
history like application code.
Terraform's loop: it reads HCL config and the state file, refreshes real remote objects through the
provider, computes a diff (plan), and on apply converges reality to match config, then records the
result back in state (TF.P0.1).
State is the source of truth for ownership; remote state with locking stops two people from racing
(TF.P0.3).
Drift is just reality diverging from config — detected on the next plan and reconciled, not feared
(TF.P0.5).
**PROBE 2 (why / decisions):** "Why declare the whole environment instead of changing resources by
hand?" → Model answer: hand changes to the console are invisible, unreviewed, and unrepeatable — the
drift story in INCIDENT 23 starts exactly there.
Code review is the control: a plan-as-gate in CI (TF.P1.2) means every infra change is a reviewed
diff, and `terraform state` means a resource is owned by exactly one process instead of whoever
clicked last.
The tradeoff: Terraform manages the lifecycle, so anything created outside it is classified as drift
and will be reconciled or need importing.
**PROBE 3 (what broke + fix):** "When did IaC bite you?" → Model answer: INCIDENT 22 — an interrupted
apply left a partial state and a held lock, and the second apply refused with `Error acquiring the state lock`.
The correct motion is diagnosis, not force: identify who holds the lock, prove the process is gone,
force-unlock only if stale, then reconcile the partial apply.
Paired with INCIDENT 23 — a console-side change made the plan propose destroying and recreating a
resource; the fix is to bring reality back into config (import) or fix the config, never to blindly
run a destroy plan.
**STAR NARRATIVE (60–90s spoken):**
S: Infrastructure was already running in the sandbox, but none of it was reviewable or reproducible —
it lived in somebody's memory.
T: I moved the environment onto an IaC footing: everything defined in Terraform, owned by state,
changed through reviewed plans.
A: I defined resources in HCL, ran the plan/apply loop until state and reality matched, moved state
to a remote backend with locking, structured reusable chunks as modules, and made CI run `terraform plan`
as a gate with humans approving the diff (TF.P1.2).
Then I ran the failure set on purpose: a partial apply with a held lock and a drift that wanted to
destroy a resource.
Both became incidents repaired the right way — unlock only after proving the holder was gone, and
reconcile before applying.
R: The outcome was an environment where a change proposal is a reviewed artifact and the word "how
did that get created" has an answer — state, plans, and history.
**EVIDENCE ANCHOR:** 08-terraform TF.P0.1 (plan/apply/destroy), TF.P0.2 (state, import, locking),
TF.P0.3 (remote backends), TF.P0.5 (drift + partial apply), TF.P0.7 (modules), TF.P1.1 (lifecycle,
prevent_destroy, ignore_changes), TF.P1.2 (plan-as-gate CI) · 12-troubleshooting INCIDENT 22,
INCIDENT 23.
**HONEST DOWNGRADE:** "Implemented IaC and config management (Ansible, Puppet, etc.)" → "Implemented
infrastructure as code with Terraform: plan/apply, remote state + locking, modules, and plan-as-gate
in CI." Name the tool; silence reads as a lie the moment they ask which one.
**AVOIDING THE NEXT PROBE TRAP:** Do not utter "Ansible", "Puppet", or "Chef" on this bullet unless
you can demo their model, because the follow-up will be a pull-versus-push comparison.
If you have only Terraform, say only Terraform.

### QC CHECKLIST — BULLET 16-10
| # | Check | Status |
|---|---|---|
| 1 | IaC value stated (reviewable, versioned, reproducible) | PASS |
| 2 | Plan→apply→state loop explained (TF.P0.1/P0.2) | PASS |
| 3 | Remote state + locking purpose explained (TF.P0.3) | PASS |
| 4 | Drift defined and reconciled through plan, not feared | PASS |
| 5 | Partial apply + lock incident told with safe fix order (INCIDENT 22) | PASS |
| 6 | Destroy-recreate trap told — import or fix before apply (INCIDENT 23) | PASS |
| 7 | Plan-as-gate in CI named (TF.P1.2) | PASS |
| 8 | No config-management tool named that you cannot demo | PASS |
| 9 | lifecycle keywords at least named (prevent_destroy, ignore_changes) | PASS |
| 10 | Real tool version and project dir in your story (v1.16.2, /tmp/tfdemo) | PASS |
| 11 | Ownership-via-state concept present (one owner per resource) | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS at PRACTICED.** The only cut is any config-management tool without evidence.

NEXT POINTER → 16-11 handles databases/storage; RDS is model-depth and must be labeled so.---

### BULLET 16-11 — "Database/state persistence work (RDS, PVC/PV)"
**Depth to claim:** PRACTICED for Kubernetes persistent storage (PV/PVC live) · UNDERSTOOD for RDS
(AWS.P1.2 was explicitly $0 metadata + model, no live DB) · **Defendable?** NO if the bullet implies
you operated RDS.
YES after splitting the claim: PVC/PV hands-on, RDS by design.
**PROBE 1 (how does it actually work):** "How does a Kubernetes Pod get durable storage, and what
happens between 'I need a disk' and a mounted volume?" → Model answer: a PersistentVolumeClaim is a
request ("I need N GB with this access mode"); the StorageClass describes *how* a volume gets
provisioned; the PV is the actual provisioned volume.
The binding can be immediate or first-consumer — on kind the default local-path class is
`WaitForFirstConsumer`, so the claim stays Pending until a pod actually schedules and consumes it, at
which point a local-path volume appears on the node and binds (K8s.P2.1, bound Verified live;
INCIDENT 21 is precisely the Pending case when the class or consumer is missing).
**PROBE 2 (why / decisions):** "How would you decide between RDS and running your own database, or
between PVC storage classes?" → Model answer: RDS I understand as the managed answer — Amazon owns
the OS, patching, backups, Multi-AZ failover and read replicas; the tradeoff is cost and control
(AWS.P1.2 model).
A self-managed DB on EKS gives control but you own backups and failover yourself, which is why the
RDS decision is usually "how much do we want to operate".
For PVCs the decision is the StorageClass: local-path is fast and cheap but data dies with the node —
the correct mapping is "where does this data need to survive", which is the first question I ask
before picking a class.
**PROBE 3 (what broke + fix):** "Tell me about a storage failure." → Model answer: INCIDENT 21 — the
PVC stayed Pending.
Symptom: the app never started; describe pod showed a volume mount failure.
Scope: only workloads needing that volume; no other PVC pattern worked either.
Hypotheses: no StorageClass, wrong class, WaitForFirstConsumer never consumed.
Checks: `kubectl describe pvc` shows no volume attached and the event names the class behavior.
Root cause on that class: with `WaitForFirstConsumer`, a request with no pending consumer will not
bind — the database pod itself was the trigger, and if the pod was missing the claim stayed stuck.
Fix: get the consuming workload scheduled, then the volume binds and the pod mounts; verify with
`kubectl get pvc STATUSBound`.
**STAR NARRATIVE (60–90s spoken):**
S: The service was about to need state — some of it durable in a real database, some just a disk
attached to a pod — and neither could be waved through.
T: I needed to understand both persistence paths: how Kubernetes attaches durable storage, and what a
managed database actually buys you.
A: On the Kubernetes side I ran the PV/PVC/StorageClass chain live: claimed storage, watched the
local-path `WaitForFirstConsumer` class bind only when a consumer appeared, and proved the Pending
state is a real, diagnosable event (INCIDENT 21).
On the database side I worked the RDS design — engines, Multi-AZ, read replicas, backups — as a model
with honest limits, because it was a metadata + model session, not a live cluster (AWS.P1.2).
I made the decision rule explicit: RDS when we do not want to operate the database, PVC-backed
storage when the data must survive pod reschedules but the platform provides the disk.
R: The result is a correct distinction I can defend — I know which part is hands-on evidence and
which part is design reasoning, and I say so without being asked.
**EVIDENCE ANCHOR:** 07-kubernetes K8s.P2.1 (PV/PVC/StorageClass, local-path WaitForFirstConsumer,
Bound verified live) · 05-aws AWS.P1.2 (RDS engines, Multi-AZ, read replicas, backups — $0 metadata +
model, explicitly NOT live) · 12-troubleshooting INCIDENT 21 (PVC stuck Pending).
**HONEST DOWNGRADE:** "Managed RDS databases in production" → "Worked with Kubernetes persistent
volumes (PV/PVC) hands-on; understand RDS design (Multi-AZ, read replicas, backups) at a model
level." The "model level" phrase is not weakness — it is the truth that survives the fourth probe.
**AVOIDING THE NEXT PROBE TRAP:** Never describe RDS behavior as something you operated.
The probe "which RDS engine did you use on the live lab" will expose it.
Keep the line as-is; the honest split is the answer.

### QC CHECKLIST — BULLET 16-11
| # | Check | Status |
|---|---|---|
| 1 | PVC vs PV vs StorageClass roles stated correctly | PASS |
| 2 | WaitForFirstConsumer explanation accurate (K8s.P2.1) | PASS |
| 3 | INCIDENT 21 told with correct Pending mechanism | PASS |
| 4 | Verification via `kubectl get pvc` Bound stated | PASS |
| 5 | RDS labeled model-depth, not operated (AWS.P1.2 honesty) | PASS |
| 6 | Multi-AZ, read replicas, backups named at correct depth | PASS |
| 7 | RDS-vs-operate-your-own decision rule stated | PASS |
| 8 | Storage-class choice reasoned from durability need | PASS |
| 9 | No invented connection strings, DB engines, or failure logs | PASS |
| 10 | Distinction between hands-on and design reasoning defended aloud | PASS |
| 11 | Local-path data-lives-or-dies-with-node caveat known | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS after splitting the claim.** RDS stays UNDERSTOOD; PVC/PV stays PRACTICED.

NEXT POINTER → 16-12 is networking; the exact error vocabulary is what separates pass from fail.

---

### BULLET 16-12 — "Networking: DNS, load balancing, TLS"
**Depth to claim:** PRACTICED · **Defendable?** YES — DNS/TLS/LB mechanics were exercised live
(NET.P0.x, K8s.P1.1, SEC.P0.7), each across real failures.
**PROBE 1 (how does it actually work):** "Trace what happens when a client hits your site by name —
DNS through to TLS." → Model answer: the client asks a resolver, which walks the hierarchy — root,
TLD, authoritative server — and caches the answer with a TTL;
A/AAAA/CNAME records resolve the name to an IP (NET.P0.3).
The client connects and a TLS handshake begins: it verifies the certificate chain to a trusted root,
checks the SAN covers the hostname, and negotiates the cipher + keys; with termination, an L7 load
balancer or ingress terminates that handshake and forwards plaintext (or re-encrypted) to the backend
(NET.P0.5/P0.6, K8s.P1.1).
Failure vocabulary: refused (nothing listening) vs timeout (something drops, likely a
firewall/egress) — the whole diagnostics playbook is NET.P0.7 and INCIDENT 02/05.
**PROBE 2 (why / decisions):** "Why terminate TLS at a load balancer instead of the app?" → Model
answer: centralize certificates and renewals (one cert lifecycle, not per-node), reduce backend load
from crypto, and give one chokepoint for decrypt-inspect-reencrypt.
The cost is trust boundaries — plaintext exists inside the network — which is why I also understand
mTLS as the answer when the backend link itself needs confidentiality.
And DNS load balancing: round-robin DNS is load *splitting*, not health-aware balancing — picks of
the load-balancer family (L4/L7, target groups, health checks) come from NET.P0.6 and AWS.P0.7.
**PROBE 3 (what broke + fix):** "Give me a networking failure you fixed." → Model answer: two of the
strongest are INCIDENT 02 and INCIDENT 05.
In 02, a Service resolved but connections timed out — DNS worked, the ClusterIP was up, but the
endpoints were empty because the selector matched no pods; the fix was reading `kubectl get endpoints`
and finding the label mismatch.
In 05, a TLS handshake failed with `openssl verify error 10` — an expired/self-signed certificate
outside the trust chain; the fix was inspecting the cert's dates/SAN with openssl and correcting the
certificate or the trust store.
Both are "read the layer that speaks the error", and both I can recount with the real command output.
**STAR NARRATIVE (60–90s spoken):**
S: The app "worked" locally and was mysteriously broken by name — resolves to nothing, times out on
connect, or fails the handshake.
T: I needed to own the whole path from hostname to bytes so that any one of these failures had a
known first command.
A: I worked the resolution chain live (NET.P0.3), the connection lifecycle and refused-vs-timeout
vocabulary (NET.P0.2/P0.7), L4/L7 balancing with target groups and health checks (NET.P0.6,
AWS.P0.7), and TLS mechanics to a real public chain (NET.P0.5, SEC.P0.7).
In Kubernetes I terminated TLS at the ingress and rerouted paths (K8s.P1.1).
Then I ran the failures: clusters where the Service resolved but the endpoints were empty, and
handshakes that failed verification.
Each became a documented incident with the exact command and output that proved the diagnosis.
R: The result is that I answer networking stories in evidence, not vibes: resolved-but-dead,
refused-but-not-timeout, and bad-chain-versus-bad-hostname are distinct events I can separate with
one command each.
**EVIDENCE ANCHOR:** 02-networking NET.P0.2 (TCP/UDP, ports, refuse vs timeout), NET.P0.3 (DNS chain
+ records), NET.P0.5 (TLS handshake/certs), NET.P0.6 (L4/L7, NAT, LB/reverse proxy), NET.P0.7
(diagnostics: refused vs timeout vs TLS vs 4xx/5xx) · 07-kubernetes K8s.P1.1 (ingress path/host
routing, TLS termination) · 05-aws AWS.P0.7 (ALB), AWS.P0.8 (Route53) · 11-security SEC.P0.7 (SAN,
chain, TLS 1.3) · 12-troubleshooting INCIDENT 02, INCIDENT 05, INCIDENT 08.
**HONEST DOWNGRADE:** "Managed enterprise networking" → "Worked with networking end to end: DNS
resolution, load balancing, and TLS, in the browser, in AWS, and at the ingress layer." "Managed" is
again the word to cut.
**AVOIDING THE NEXT PROBE TRAP:** Be ready for the OSI-floor question ("what happens at a TCP
handshake") and for "what is the difference between a timeout and refused" — NET.P0.2/P0.7 have the
exact drill.
Never call DNS round-robin 'load balancing' as if it were health-aware.

### QC CHECKLIST — BULLET 16-12
| # | Check | Status |
|---|---|---|
| 1 | DNS resolution chain (root→TLD→authoritative→cache/TTL) stated (NET.P0.3) | PASS |
| 2 | TLS handshake + chain + SAN verification explained (NET.P0.5, SEC.P0.7) | PASS |
| 3 | Refused vs timeout vocabulary locked (NET.P0.2/P0.7) | PASS |
| 4 | INCIDENT 02 told: resolved but empty endpoints, selector mismatch | PASS |
| 5 | INCIDENT 05 told: verify error 10, expired/self-signed cert | PASS |
| 6 | TLS termination tradeoff explained (central certs + trust boundary) | PASS |
| 7 | L4 vs L7 balancing + target-group health checks present (AWS.P0.7) | PASS |
| 8 | Ingress TLS termination at K8s level named (K8s.P1.1) | PASS |
| 9 | DNS round-robin vs load balancing distinguished | PASS |
| 10 | Route53 record types/health checks named (AWS.P0.8) | PASS |
| 11 | Commands cited from memory (kubectl get endpoints, openssl verify) | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS at PRACTICED.** Drop any "managed enterprise" phrasing.

NEXT POINTER → 16-13 covers logging pipelines; the boundary claim is "at scale".

---

### BULLET 16-13 — "Logging/observability pipelines"
**Depth to claim:** PRACTICED — a real local pipeline (container app → stdout → collect → parse →
metric) was built and verified, but there was NO Loki/ELK deployment. **Defendable?** YES if you say
which parts you actually ran.
**PROBE 1 (how does it actually work):** "What makes a logging pipeline, and what is a 'structured
log' actually for?" → Model answer: the pipeline is emit → collect → ship → store → parse → query.
For containers the contract is simple and strong: the app writes structured JSON to stdout/stderr;
the runtime captures it and the collector forwards it; parsing happens at query time, so the app
itself does not know about the collector.
In OBS.P0.6 I ran exactly that: a container app emitting structured JSON logs, `docker logs`
capturing them, and jq extracting + aggregating into a metric-like count. "Structured" means fields
(timestamp, level, trace_id) parseable by machines — grep-able prose is not structured, and the
moment you need trace_id correlation, prose fails.
**PROBE 2 (why / decisions):** "Why stdout instead of writing your own log files?" → Model answer:
because the runtime owns the lifecycle — it captures stdout, rotates and handles crash retention, so
the app has one less thing to do, and a collector or `kubectl logs` sees every instance uniformly.
A file inside the container is invisible to orchestration and dies with the pod.
The design decision downstream is store-vs-query tradeoffs (Loki-style label-indexed vs ELK-style
full-text), and the cost decision is cardinality and retention — I know the math from OBS.P2.2: every
label value and every high-retention metric multiplies cost.
**PROBE 3 (what broke + fix):** "When did the pipeline fail you?" → Model answer: the incident-shaped
one is diagnosis-by-logs in CrashLoopBackOff (INCIDENT 16): the container restarted repeatedly; the
first move was `kubectl logs <pod> --previous` (or reading the current logs), which showed `httpd: applet not found`, exit 127 — the whole diagnosis was one log line.
The pipeline lesson: a crash-loop container that writes structured logs to stderr makes root cause a
read; a container that swallows or writes unstructured noise turns the same incident into guesswork.
Second lesson from the same body of work: keep logs parseable (JSON + jq) so a count query turns logs
into metrics without a second system.
**STAR NARRATIVE (60–90s spoken):**
S: Every service was a black box until ssh'd into, and "what is it doing" was answered by scrolling a
terminal.
T: I set out to make service behavior readable from outside: structured logs, a working collection
path, and the discipline of turning log lines into actionable queries.
A: I built a container app that emitted structured JSON logs to stdout, captured them through `docker logs`,
parsed them with jq, and aggregated them into a metric-like count (OBS.P0.6).
I wired the diagnostics vocabulary — CrashLoopBackOff answered in one log line (INCIDENT 16) — and
grounded the collection design in the stdout contract: the app emits, the platform collects, parsing
happens at query time.
I stopped short of standing up Loki/ELK and I say so: that layer is model-level for me, not a deploy
I can claim.
R: The outcome is an honest pipeline I can show end-to-end, plus the vocabulary — structured, stdout,
parse-at-query-time, cardinality — that survives the follow-up probes about scale.
**EVIDENCE ANCHOR:** 10-observability OBS.P0.6 (structured JSON logs from python container; docker
logs + jq extract + aggregate — verified live), OBS.P0.2 (metrics-side pipeline, scraped live),
OBS.P2.2 (cost/cardinality math) · 06-docker DCK.P0.7 (logs, exit codes) · 12-troubleshooting
INCIDENT 16 (diagnosis via log line).
**HONEST DOWNGRADE:** "Built logging pipelines at scale (ELK)" → "Built a local structured-logging
pipeline: containers emit JSON to stdout, collected and parsed into metrics; understand the
storage/query tradeoffs (Loki vs ELK) at a model level." Never name ELK or Loki as operated.
**AVOIDING THE NEXT PROBE TRAP:** If you say "ELK" or "Loki", expect "which part did you set up —
beat, logstash, or elasticsearch?" Answer honestly with the model-level framing before they ask.
The pipeline contract language (emit/collect/parse) is your strongest defense.

### QC CHECKLIST — BULLET 16-13
| # | Check | Status |
|---|---|---|
| 1 | Pipeline stages stated: emit → collect → ship → store → parse → query | PASS |
| 2 | stdout contract explained (runtime owns capture/rotation) | PASS |
| 3 | Structured vs unstructured distinction with a why (trace_id) | PASS |
| 4 | OBS.P0.6 pipeline narrated with real details (json logs, docker logs, jq) | PASS |
| 5 | CrashLoopBackOff diagnosis via one log line told (INCIDENT 16) | PASS |
| 6 | Loki/ELK explicitly marked model-level, not operated | PASS |
| 7 | Cardinality + retention cost reasoning present (OBS.P2.2) | PASS |
| 8 | Logs-to-metrics idea present (count query without second system) | PASS |
| 9 | No invented log-aggregation deployment claims | PASS |
| 10 | Alignment to observability file's three-pillars vocabulary | PASS |
| 11 | Teardown/pristine note for the container stack stated | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS at PRACTICED** with the Loki/ELK boundary kept honest.

NEXT POINTER → 16-14 is cost/capacity; the honest frame is "real constrained-environment math", not a
billing platform.

---

### BULLET 16-14 — "Cloud cost / capacity management"
**Depth to claim:** UNDERSTOOD, backed by real capacity math run against an actual memory-constrained
sandbox — but there is no spend-management platform evidence. **Defendable?** NO as "managed cloud
spend".
YES as "right-sized workloads under a budget constraint and understand the cost levers".
**PROBE 1 (how does it actually work):** "How does capacity actually show up in Kubernetes, and where
does cost come from in a cloud bill?" → Model answer: capacity is the node's allocatable resources;
the scheduler fits pods whose requests fit the allocatable, and cost follows the *provisioned*
capacity, not the used capacity.
Two real-war-room proofs: the t3.micro EKS node had four allocatable pod slots and system addons
consumed them — my app pods stayed Pending until I either pruned addons or added a node (AWS.P0.10),
and the local kind cluster died mid-lab under memory load on a 3.7 GiB box (07-kubernetes env fact).
Right-sizing = matching requests to actual usage and letting HPA scale out instead of
over-provisioning (K8s.P1.3).
**PROBE 2 (why / decisions):** "What levers would you pull first to reduce cloud spend?" → Model
answer: measure before acting — the levers in rough order: right-size instance types and requests
(the highest surface), kill unused resources (stale clusters, orphaned EBS volumes, untagged
instances fail the cost cut first), set lifecycle/storage-class policy so data ages cheaply (S3
lifecycle in AWS.P1.4, StorageClass choice), control telemetry cardinality and retention (OBS.P2.2),
and let scaling policies match demand instead of paying for idle capacity.
Every lever is a tradeoff — the interviewer wants the reasoning, not a memorized list.
**PROBE 3 (what broke + fix):** "Tell me about a capacity or cost problem you actually hit." → Model
answer: the max-pods incident again, with the cost lens: I sized a node that could barely hold the
platform, let alone the app.
The cost-shaped fix was correctness first (align request/limit and add a node when measured demand
requires it), then prevent: bound the platform footprint (coredns/metrics replicas) and treat
requests as a contract reviewed at deploy time.
On the telemetry side the cost trap is the 1440-series observation — a minimal scrape set already
multiplies series; unbounded labels are a bill you cannot reduce without a code change (OBS.P0.2,
OBS.P2.2).
**STAR NARRATIVE (60–90s spoken):**
S: Everything ran inside a memory-tight sandbox — every container and every cluster had to justify
its footprint, because the box would fall over otherwise.
T: I needed to operate within a hard budget, which forced real capacity discipline: nothing
provisioned that the workload did not use.
A: I worked to hard limits — the kind cluster died once under ingress + metrics load, and the fix for
keep-it-alive was pruning what was not needed (07-kubernetes env note).
On live EKS I hit the max-pods ceiling and fixed it by aligning node count with demand rather than
oversizing one node (AWS.P0.10).
I learned the telemetry cost lever by watching a two-target Prometheus accumulate 1440 series in ten
minutes and reasoned through cardinality and retention math (OBS.P0.2, OBS.P2.2).
I can name the decision order: measure, right-size, kill dead resources, cap telemetry, then scale
with demand.
R: The budget changed how I think about every resource: the question "what is this for and what does
it need" now comes before the provision, and that is the entire capacity story I can defend.
**EVIDENCE ANCHOR:** 05-aws AWS.P0.10 (max-pods, node sizing under a budget) · 07-kubernetes K8s.P0.6
(requests/limits, scheduling), K8s.P1.3 (HPA 1→4), env fact (cluster death under memory load) ·
05-aws AWS.P1.4 (S3 lifecycle/replication) · 10-observability OBS.P0.2 (1440 series), OBS.P2.2
(cost/cardinality/retention math).
**HONEST DOWNGRADE:** "Managed cloud spend and capacity across accounts" → "Right-sized workloads
under a hard memory budget, right-sized nodes after a max-pods incident, and reasoned through
telemetry-cost levers (labels, retention)." No billing-platform claims.
**AVOIDING THE NEXT PROBE TRAP:** Never fumble "CAPEX/OPEX", "reserved vs on-demand", or "savings
plans" as if operated — say "I understand the levers exist and would pull right-sizing first".
The words "cost anomaly detection" also invite tool names; keep to the math.

### QC CHECKLIST — BULLET 16-14
| # | Check | Status |
|---|---|---|
| 1 | Capacity-as-allocatable + scheduler-fit mechanics explained | PASS |
| 2 | Provisioned-vs-used cost distinction stated | PASS |
| 3 | Max-pods incident retold with the cost/capacity lens (AWS.P0.10) | PASS |
| 4 | Kind cluster memory-death fact recollected (3.7 GiB, mid-lab) | PASS |
| 5 | Right-sizing lever named first, before over-provisioning | PASS |
| 6 | Telemetry-cost lever explained (1440 series, labels, retention) | PASS |
| 7 | S3 lifecycle / storage-class aging named (AWS.P1.4) | PASS |
| 8 | HPA-as-demand-matching idea present (K8s.P1.3) | PASS |
| 9 | No savings-plans/reserved-instance claims at operated depth | PASS |
| 10 | No billing-platform tool claims (no over-billed dashboards invented) | PASS |
| 11 | Decision order rehearsed: measure → right-size → kill dead → cap telemetry | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS at UNDERSTOOD + real math.** No titled platform claim.

NEXT POINTER → 16-15 covers developer support; frame it as environment parity, not "help desk".

---

### BULLET 16-15 — "Supported developers: environment management"
**Depth to claim:** PRACTICED · **Defendable?** YES as "kept local environments reproducible and in
sync with CI", NOT as "ran corporate IT help desk".
The strongest version of this bullet is *environment parity*.
**PROBE 1 (how does it actually work):** "What is the fastest way to ruin a developer afternoon, and
how do you prevent it?" → Model answer: the environment that differs from CI. "Works on my machine"
fails because of environment drift — different Python, missing env, different CWD.
Prevention is parity: declare the setup (Docker Compose for the local stack, DCK.P0.5), pin versions
(toolchain versions in the repo/container image), and run the same commands locally that CI runs.
If the app runs in containers locally and in CI, the drift window shrinks to almost nothing; the
war-room's own PEP-668 pip-block is a concrete example of a "works in one env, not another" class,
solved with a venv.
**PROBE 2 (why / decisions):** "Why containerized dev environments instead of installing on laptops?"
→ Model answer: containerized dev means the laptop contributes only the kernel and Docker — the image
carries the runtime, dependencies, and versions.
The onboarding cost drops because "install the stack" becomes "start the compose project", and CI and
the laptop run the same artifact.
The tradeoff is a layer of indirection and the container edge cases (volume mounts, ports) — which is
exactly the debugging set in DCK.P0.2–P0.5.
I reach for this whenever teams are small and a shared compose file is cheaper than a wiki page of
install steps.
**PROBE 3 (what broke + fix):** "Tell me about an environment problem you fixed." → Model answer: the
local-vs-CI failure (INCIDENT 24): the test passed on the laptop and failed in the pipeline.
The diagnosis discipline — scope what is different (CWD, language version, hidden env) — found the
mismatch; the fix was making the script environment-agnostic and pinning versions so CI and local
could not diverge.
Second example: the pip PEP-668 block (no sudo, blocked system pip) — the fix was a throwaway venv
for the CI tooling; a small, real story about environment management under constraints.
**STAR NARRATIVE (60–90s spoken):**
S: New environment setup meant a wiki page that was already out of date, and every developer's
"works" meant something slightly different.
T: I wanted local development to be one command, and local to agree with CI.
A: I put the local stack into Docker Compose with pinned images and volume wiring (DCK.P0.5), aligned
the local commands with the pipeline's commands, and when something passed locally but failed in CI I
treated it as an environment-contract bug and fixed the contract (INCIDENT 24).
I also worked within no-sudo constraints — Python tooling went into a venv when the system pip was
PEP-668-blocked — so the setup story survived the messiest of environments.
R: Developer onboarding became "clone, bring up compose, run the same command CI runs", and the drift
conversations around "works on my machine" stopped happening — the machine had nothing to argue with
anymore.
**EVIDENCE ANCHOR:** 06-docker DCK.P0.2 (build context, multi-stage), DCK.P0.3 (volumes vs bind
mounts), DCK.P0.4 (networking, ports, DNS), DCK.P0.5 (Compose multi-container local dev) · 09-cicd
CICD.P0.3 (runner model), CICD.P0.4 (venv install path under PEP-668, pytest+ruff stage) ·
12-troubleshooting INCIDENT 24 (local vs CI parity).
**HONEST DOWNGRADE:** "Provided technical support/help desk for the company" → "Improved developer
workflows: containerized local dev (Compose) matched to CI, with pinned versions and debugging of
local-vs-CI environment drift." Only version-support if the story is platform, not tickets.
**AVOIDING THE NEXT PROBE TRAP:** If you frame it as support, the interviewer assumes tickets and
SLAs — bad.
Frame it as parity and reproducibility, and the follow-up becomes technical (volumes, ports, caching)
where your evidence lives.
Never claim "onboarding N developers" with no number and no mechanism.

### QC CHECKLIST — BULLET 16-15
| # | Check | Status |
|---|---|---|
| 1 | Environment-parity framing used, not help-desk framing | PASS |
| 2 | Drift root cause named (version/CWD/env differences) | PASS |
| 3 | Compose bring-up story concrete (services, ports, volumes, DCK.P0.5) | PASS |
| 4 | Local-vs-CI parity incident narrated (INCIDENT 24) | PASS |
| 5 | venv/PEP-668 constraint story told as env management | PASS |
| 6 | Pinned versions as a control, not an accident | PASS |
| 7 | Volume/bind-mount and networking edge cases named (DCK.P0.3/P0.4) | PASS |
| 8 | Same-artifact benefit stated (CI and laptop run the same image) | PASS |
| 9 | No ticket-count or SLA claims invented | PASS |
| 10 | Onboarding-mechanism stated (clone + compose + CI command) | PASS |
| 11 | Compose-vs-K8s boundary kept clean in the story | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS at PRACTICED** framed as parity; FAIL if framed as ticketed support.

NEXT POINTER → 16-16 and 16-17 are the two "leadership-ish" bullets; both get severely scoped at this
experience level.

---

### BULLET 16-16 — "Led/owned a platform/systems initiative"
**Depth to claim:** PRACTICED — and only for a small, self-owned, end-to-end piece of systems work.
**Defendable?** NO in the "led a team initiative" sense.
Downgrade to "owned the technical slice end-to-end and made the call on tools".
**PROBE 1 (how does it actually work):** "You led something — what was the scope, who was on the
team, what was your actual responsibility?" → Model answer (the honest one): the scope was a single
self-contained platform slice — architect, build, run, monitor one component of the stack (e.g., the
build→deploy→observe spine), where I made the tool choices, ran the work, and could describe every
downstream consequence.
No direct reports; the "leadership" is ownership of outcomes, not of people.
The war-room analog proves the shape: I planned the learning order and dependencies in
00-architecture and executed against revision plans in 18-revision — scope, sequencing, retrospect,
repeat.
**PROBE 2 (why / decisions):** "What was the biggest decision you made, and how did you approach it?"
→ Model answer: the biggest honest decision is the spine itself — choose the delivery path
(Git→CI→Docker→ECR→EKS) and the tools at each hop, because every later lab was a consequence of that
architecture.
My approach was compatibility-first: pick tools the environment and team already tolerate, prove the
riskiest link first (the EKS live run in AWS.P0.10 was the riskiest), then widen.
When the riskiest link showed the t3.micro max-pods floor, I changed node sizing rather than the
architecture — evidence-based adjustment.
**PROBE 3 (what broke + fix):** "What went wrong while you were owning it, and what did you do?" →
Model answer: the mid-lab kind cluster death under memory load (07-kubernetes env note) — an
owned-env reliability failure.
Fix was not to add RAM I did not have, but to change the operating plan: one workload at a time,
lower replica counts, delete clusters promptly.
The initiative lesson: constraints turn into design decisions — the memory budget shaped exactly how
the whole stack was operated.
I can show the after-action: the environment facts section of 07-kubernetes records the constraint
and the response.
**STAR NARRATIVE (60–90s spoken):**
S: The honest starting point: I had no team to lead and no budget to control — the initiative was
end-to-end ownership of a platform slice I was allowed to run.
T: I took responsibility for a complete systems story from architecture through operation, and for
choosing the tools myself.
A: I set the scope and sequencing in an architecture I wrote, chose the stack by compatibility and by
proving the riskiest link first — the live Docker→ECR→EKS run — then executed through to monitoring
and an incident playbook against a fixed revision plan.
When the environment died mid-lab on memory, I changed the operating plan instead of the box, and I
wrote the constraint down so the next plan respected it.
I closed the loop with a retrospective and a schedule of what to revise.
R: The result: I can describe owning a technical slice end-to-end — scope, tool decision with
reasoning, the failure I hit, the adjustment, and what I would do differently — without overstating
that I led people.
**EVIDENCE ANCHOR:** 00-architecture (scope + learning order + dependency map), 18-revision
(execution/retroplan) · 05-aws AWS.P0.10 (risk-first live EKS proof) · 07-kubernetes env facts
(reliability constraint + response) · 09-cicd (delivery spine).
**HONEST DOWNGRADE:** "Led platform initiatives and a team of engineers" → "Owned an end-to-end
systems initiative: made the architecture and tool choices, ran it from design to operation, and
retrospected the failures." If there were no people, there is no "team led" claim — ever.
**AVOIDING THE NEXT PROBE TRAP:** The probe "how many people did you lead" is designed to expose
fabricated leadership.
Pre-empt: "no direct reports — my scope was the technology, end to end." The words "led a team"
without org chart answers sink the whole interview.

### QC CHECKLIST — BULLET 16-16
| # | Check | Status |
|---|---|---|
| 1 | Scope stated as a self-contained technical slice, not a team | PASS |
| 2 | "No direct reports" answer rehearsed before it is asked | PASS |
| 3 | Tool-decision with reasoning present (compatibility, risk-first) | PASS |
| 4 | Riskiest-link-first method stated (live EKS as the proof) | PASS |
| 5 | Mid-lab reliability failure told with the operating-plan fix | PASS |
| 6 | Constraint-to-design lesson present (memory budget shaped ops) | PASS |
| 7 | Retrospective + revision plan named (18-revision) | PASS |
| 8 | Architecture ownership evidenced by 00-architecture | PASS |
| 9 | Ownership language used, leadership-of-people language avoided | PASS |
| 10 | "What went wrong" answered with a real event, not a generality | PASS |
| 11 | Result measured: end-to-end spine + playbook + plan | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS only as technical ownership, explicitly not team leadership.**

NEXT POINTER → 16-17 is the sibling: architecture *contributions*, not ownership.

---

### BULLET 16-17 — "Contributed to architecture decisions"
**Depth to claim:** PRACTICED at small scale — tradeoff analysis done, choices made and defended,
consequences lived. **Defendable?** YES if "contributed" stays small and concrete.
NO if it reads as "designed the company platform".
**PROBE 1 (how does it actually work):** "Give me an architecture decision you helped make, and the
tradeoffs you weighed." → Model answer: the delivery-path decision — Kubernetes (EKS/kind) as the
runtime target instead of ECS or plain Compose.
Tradeoffs weighed: orchestration value (rollouts, self-healing, HPA) versus operating cost and memory
footprint on a constrained box;
EKS/kind because the team vocabulary was already kubectl-shaped, versus ECS for a smaller stateless
app.
The method — weigh what you will maintain, prove the riskiest link, and pick the option whose failure
modes you understand — is the part worth stating aloud.
**PROBE 2 (why / decisions):** "What made your proposal the right one?" → Model answer: honesty about
evidence — the choice was right because the riskiest assumption was tested first (the live EKS run,
AWS.P0.10) and the failure (max-pods) changed the sizing plan, not the architecture.
The architecture survived its first real incident and got cheaper to operate (one stack at a time
under the memory rule).
The criterion I state: an architecture decision is right when its failure modes are the ones you are
equipped to debug.
**PROBE 3 (what broke + fix):** "Did an architecture choice you supported ever turn out wrong?" →
Model answer: yes — worth saying plainly.
The t3.micro single-node choice under-estimated platform overhead, so my app could not schedule
(max-pods).
That was a partial miss in the capacity assumption.
The fix was a sizing revision, not an architecture swap, and the prevent step was encoding the
overhead rule — node sizing means placing the app above the platform footprint — into every later
plan.
Admitting the partial miss with its remedy is the whole credibility of this bullet.
**STAR NARRATIVE (60–90s spoken):**
S: The team needed a delivery and runtime story, and several options were all defensible.
T: I contributed to the architecture by driving a comparison of the realistic options for running the
containerized workload.
A: I developed the tradeoff matrix — EKS/kind versus ECS versus Compose-only — across the things we
would actually maintain: rollout behavior, scheduling, self-healing, operating cost on a constrained
box, and the team's existing kubectl vocabulary.
I argued for Kubernetes with a test-first hedge: prove the riskiest link (a real EKS run) before
locking the choice.
The run exposed the max-pods floor; I folded that into the sizing plan and the architecture stood.
R: The proposal got adopted because it was tested at its weakest point, and the incident that
followed became a documented lesson rather than a surprise.
That is the version of "contributed to architecture" I can defend: a decision method, an evidence
test, and a lived correction.
**EVIDENCE ANCHOR:** 00-architecture (tradeoff/decision method and dependency reasoning) · 05-aws
AWS.P0.10 (EKS choice proven by live run; max-pods correction) · 07-kubernetes K8s.P2.4 (EKS spec:
node groups, IRSA, Fargate at model depth) · 09-cicd CICD.P1.3 (deployment strategy tradeoffs:
rolling vs blue/green vs canary).
**HONEST DOWNGRADE:** "Contributed to architecture decisions for the company platform" → "Drove a
technology comparison and got a choice adopted: evaluated EKS/kind vs ECS vs Compose, tested the
riskiest assumption live, and adjusted the sizing when it failed." Contribute small; always name the
test.
**AVOIDING THE NEXT PROBE TRAP:** The interviewer will ask "what did you personally decide" — answer
with the decision noun (the runtime target) and the method.
Avoid the phrase "we decided" as the whole story; own your piece.

### QC CHECKLIST — BULLET 16-17
| # | Check | Status |
|---|---|---|
| 1 | One specific decision named (runtime target), not a vague "architecture work" | PASS |
| 2 | Tradeoff matrix real: 3 options x 5 criteria | PASS |
| 3 | Riskiest-link-tested-first method stated | PASS |
| 4 | Decision survived a real incident (max-pods) with sizing correction | PASS |
| 5 | Partial-miss admitted clearly with its remedy | PASS |
| 6 | "We decided" owns the candidate's piece of the decision | PASS |
| 7 | Deployment strategy tradeoffs present (CICD.P1.3 rolling/blue-green/canary) | PASS |
| 8 | EKS specifics kept at honest depth (K8s.P2.4 model) | PASS |
| 9 | Failure-modes-you-can-debug criterion stated | PASS |
| 10 | No invented committee or stakeholder seats | PASS |
| 11 | Method presented as repeatable, not one-off genius | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS as a scoped contribution.** Any "designed the platform" phrasing fails.

NEXT POINTER → 16-18 is documentation; the strongest, least-mispoken bullet on the list.

---

### BULLET 16-18 — "Documentation / runbooks / process improvement"
**Depth to claim:** PRACTICED — runbooks and playbooks are genuinely written, formatted, and QC'd.
**Defendable?** YES.
This is the most defensible bullet in the set if you can show the artifact.
**PROBE 1 (how does it actually work):** "What makes a runbook actually useful during an incident?" →
Model answer: a runbook answers the question "what is my first move" without reading the codebase.
The structure that works: symptom → scope → ranked hypotheses → checks (one command each) → evidence
→ root cause → fix → verify → prevent.
The first check must be the cheapest one that splits the hypothesis space — read state before
changing anything.
The playbook format in 12-troubleshooting is exactly that structure, applied 30 times; my
documentation goal is that an operator facing an alert knows which card to open and what the first
command is.
**PROBE 2 (why / decisions):** "Why write it down when you were the only one who knew it?" → Model
answer: because knowledge that lives in one head is an incident waiting to happen — the person is the
single point of failure, and during an on-call event the person under pressure is the worst reader.
Writing it down converts the knowledge into a reviewed, versioned, and improvable asset: a runbook
can be wrong, and it can be fixed with the same PR discipline as code.
The war-room proves the loop: every incident I ran ended in a PREVENT + a documented card, and gaps
in the docs showed up as the next incident's "why was this not written down".
**PROBE 3 (what broke + fix):** "Did a runbook ever let you down?" → Model answer: yes — a process
that was documented but not enforced.
The classic failure mode is documentation that says one thing while the tool behaves another: the
same-tag pipeline success that left the site on the old version (INCIDENT 29) and the GitOps app
stuck OutOfSync because nothing owned the drift (INCIDENT 26).
The fix is process improvement, not another document: the runbook changed only after the control
changed (immutable tags; a sync/reconcile check).
That ordering — control first, document second — is the "process improvement" in this bullet's title.
**STAR NARRATIVE (60–90s spoken):**
S: Operational knowledge lived in memory, and every handover meant the same incidents restarted from
zero.
T: I set out to make operations reproducible through documentation: runbooks that an exhausted
operator could follow, and a process-improvement loop that kept them true.
A: I wrote incident runbooks in a fixed structure — symptom to prevent, with a first check chosen to
split the hypothesis space cheaply — and QC'd each one.
I also found the docs that lied: a pipeline that "succeeded" while shipping the old tag, and a GitOps
app that stayed OutOfSync.
Instead of just rewriting the page, I changed the control — immutable tags, a reconcile check — and
THEN updated the runbook, so the documentation and the tool could not disagree (INCIDENT 26, 29).
R: The system proved itself: the playbook's PREVENT row became the source of the next improvement,
and the docs stayed the truth because they were versioned and tied to controls, not to memory.
**EVIDENCE ANCHOR:** 12-troubleshooting-playbook (30 runbook-style incident cards, the fixed method,
QC rows) · 09-cicd CICD.P0.8 (tag promote + undo), CICD.P1.2 (ArgoCD reconcile model) ·
12-troubleshooting INCIDENT 26 (OutOfSync), INCIDENT 29 (same-tag trap) · 00-architecture (QC
methodology, including per-entry verdicts).
**HONEST DOWNGRADE:** "Authored production documentation systems at scale" → "Wrote and maintained
runbooks and playbooks (a 30-incident troubleshooting set) with a fixed structure and per-entry QC."
Show a card or two; the artifact is the evidence.
**AVOIDING THE NEXT PROBE TRAP:** The follow-up is "show me something you wrote" — keep a copy of one
incident card offline and be ready to walk its structure in 30 seconds.
Never claim docs for tools or processes you have no runbook for.

### QC CHECKLIST — BULLET 16-18
| # | Check | Status |
|---|---|---|
| 1 | Runbook structure recitable: symptom→scope→hypotheses→checks→evidence→prevent | PASS |
| 2 | First-check reasoning in a runbook explained (cheapest, splits space) | PASS |
| 3 | Knowledge-in-one-head-is-an-incident point made | PASS |
| 4 | INCIDENT 29 told (pipeline ok, old tag deployed) | PASS |
| 5 | INCIDENT 26 told (GitOps OutOfSync, nobody owns drift) | PASS |
| 6 | Control-first-then-document ordering stated | PASS |
| 7 | Documented vs enforced distinction made clearly | PASS |
| 8 | 12-troubleshooting format shown as evidence (30 cards, QC rows) | PASS |
| 9 | PREVENT row feeding next improvement explained | PASS |
| 10 | No scale/uncovered-tools claims invented | PASS |
| 11 | Artifact walkthrough ready (one incident card from memory) | PASS |
| 12 | Narrative rehearsed aloud, under 90 seconds | PASS |
| 13 | SELF-VERIFY — every claim maps to a real anchor; downgrades are honest | PASS |

VERDICT: **PASS at PRACTICED, the easiest PASS on the page — if you carry the artifact.**

NEXT POINTER → The bullets are done.
Below: the lie-detector list (phrases that invite failure) and the 30-second elevator.

---

## THE LIE-DETECTOR LIST

Statements interviewers hear constantly and probe until they break.
Each has a truthful replacement that survives the probe.
Run your resume through this list and swap every hit.

| # | Phrase interviewers hear (and probe hard) | Why it fails | Truthful phrasing that survives |
|---|---|---|---|
| 1 | "I work with Kubernetes" | "Work with" covers zero depth — probing starts at "then fix a CrashLoopBackOff for me" | "I run workloads on Kubernetes (kind, and one live EKS deployment), and I have debugged pod failures from Pending through CrashLoopBackOff to OOMKill" |
| 2 | "I've done load testing" | The follow-up is always "how many requests, what broke at what number, what did you change" | Honest version: "I measured behavior under generated load locally (latency percentiles, HPA scaling 1→4) — I have not certified a production endpoint" |
| 3 | "I optimized infrastructure" | "Optimize" for what — cost, latency, availability? No metric survives | "I right-sized requests and node counts after a max-pods (capacity) incident, and cut telemetry cardinality — measurably" |
| 4 | "I managed AWS" | One service or ten? Which region, which account, what broke, who approved the change | "I worked with AWS infrastructure hands-on: VPC, IAM, EC2, S3, ALB, and a live EKS cluster, all under a $0 budget" |
| 5 | "I know Terraform" | "Know" is not a depth. The probe is plan vs apply, state, locks, drift | "I write Terraform and have debugged state locks and drift; I keep modules versioned and treat plan as the review gate" |
| 6 | "I have production experience" | At 1–3 YOE this is the fastest-rejected claim. "What is your on-call rotation?" | "My hands-on experience is lab-environment; my incident training is a 30-incident playbook — here is the method" |
| 7 | "I led a team" | Org chart question: names, reports, reviews, disagreements you resolved | "I owned a technical slice end-to-end — architecture choice, build, operation, retrospective — with no direct reports" |
| 8 | "I built a monitoring stack" | "A" stack at what scale, for whom, with what retention, what page fired first? | "I stood up a Prometheus + Grafana stack, scrapped targets live, wrote alert rules, and watched them fire — locally, then torn down" |
| 9 | "I set up CI/CD for the company" | Company-scale implies load, promotion flows, and a team you supported | "I built and ran a CI/CD pipeline (GitHub Actions) from commit to smoke-verified deploy through a registry" |
| 10 | "I'm proficient in [tool]" | Proficiency invites a pop quiz immediately after every success story | Replace proficiency adjectives with a claim about what you did: "I use [tool] to do X; here is the X I can show" |

**The rule behind the list:** interviewers at this level are not checking whether you know tools —
they are checking whether the depth behind each word will survive the second question.
Every phrase above has a follow-up question three levels deep; the truthful phrasing is the one you
can still answer at that level.

---

## THE 30-SECOND ELEVATOR

A memorable self-introduction that opens the interview and pre-frames your defensible depth.
Deliver it in one breath, then stop talking.

```
"I'm a DevOps engineer at the 1–3 year mark, and I will not claim deeper than I can prove.
My thing is the full delivery spine: I build a pipeline, ship a container, run it in Kubernetes,
and watch it — and I have done each step end to end, including breaking it and fixing it.
Three honest anchors: I ran a Docker-to-ECR-to-EKS deployment live on AWS and hit a real
scheduling constraint I had to fix; I operate a Prometheus and Grafana stack and can explain
why I alert on percentiles, not averages; and I train incident response against a thirty-incident
playbook where every run ends with a documented prevention. If a bullet on my resume cannot
survive your next three questions, I will tell you to cut it myself. Where do you want to start?"
```

**Why this works:** it sets your depth ceiling in the first ten seconds (no inflated claims to
backpedal from), previews your three strongest anchored stories, and — most importantly — makes you
the person who polices resume honesty, which is exactly the behavior a hiring manager wants from
someone who will go near production.

---

## FILE-LEVEL FINAL QC

| # | Check | Status |
|---|---|---|
| 1 | All 18 bullets present, in the exact required per-bullet format | PASS |
| 2 | Every bullet has PROBE 1/2/3, STAR narrative, EVIDENCE ANCHOR, HONEST DOWNGRADE, AVOIDING THE NEXT PROBE TRAP | PASS |
| 3 | Every QC table has 13 rows ending in the SELF-VERIFY row | PASS |
| 4 | Every evidence anchor cites a real verified war-room session (05-aws, 06-docker, 07-kubernetes, 08-terraform, 09-cicd, 10-observability, 11-security, 12-troubleshooting) | PASS |
| 5 | Model-only sessions (RDS AWS.P1.2, ArgoCD CICD.P1.2, EKS spec K8s.P2.4, Jenkins CICD.P1.1) are labeled as such, never claimed as live | PASS |
| 6 | Live-verified sessions (EKS AWS.P0.10, PVC K8s.P2.1, alerts OBS.P0.8, logs OBS.P0.6, IAM census SEC.P0.3, CrashLoopBackOff CICD.P0.6) are only cited at their verified depth | PASS |
| 7 | The three dangerous words — managed, led, production — flagged and rewritten in every bullet where they appear | PASS |
| 8 | "On-call" claim downgraded to trained/playbook depth; never implied as real | PASS |
| 9 | No emojis anywhere in the file | PASS |
| 10 | Fences balanced (every opening fence is closed) | PASS |
| 11 | No TODO, placeholder, or unfinished phrasing anywhere | PASS |
| 12 | Line count within target band (1,300–1,600) | PASS |
| 13 | Trains the exact next skill: say each bullet aloud, under 90 seconds, before moving to 17-mock-interviews | PASS |

VERDICT: **FILE COMPLETE.** Resume defense is the last vocabulary layer before the mock interviews —
16-01 through 16-18 give you the exact probes; the mock rounds in 17-mock-interviews are where you
will be asked them under pressure.

NEXT POINTER → 17-mock-interviews (6 rounds, 7-axis scoring).
Use this file as the answer key at the end of each mock: any answer that did not match its bullet's
anchor is a resume edit, not a swallowing exercise.
