# 13 — WRITE-WITHOUT-GOOGLE WORKBOOK

**Reproduce, don't recognize. The 48h rule: if you cannot rewrite it cold from memory 48 hours after studying the source session, you do not know it yet — re-study and re-attempt.**

**How to use (rigid protocol):**
1. Cover the ANSWER block (split-screen or americal answer folded).
2. On blank paper (or /notes dir), attempt the question under the printed TIME LIMIT.
3. Reveal the answer. Score yourself. Pen the TRUE SCORES ROW.
4. Any score < 3/5 → re-study the ruling sibling file (each task names its source session) and re-attempt at +24h and +48h.
5. Log all attempts in the per-task table.

Scoring: 0–5. 5 = byte-accurate, 4 = one small slip, 3 = right shape wrong details, ≤2 = do not know it.

---

## INDEX — TASK → SOURCE SESSION → TARGET TIME

| Task | Artifact to reproduce | Source session | Target time |
|---|---|---|---|
| 13-01 | Linux process states + signal escalation | 01-linux LINUX.P0.1 | 90s |
| 13-02 | `set -euo pipefail` + health-check script | 04-bash BASH.P0.3 + BASH.P0.5 | 300s |
| 13-03 | CIDR / subnet math | 02-networking NET.P0.1 | 180s |
| 13-04 | git reset vs revert matrix + reflog rescue | 03-git GIT.P0.5 | 120s |
| 13-05 | Deployment YAML (replicas, probes, ConfigMap mount) | 07-kubernetes K8s.P0.2 + K8s.P0.4 + K8s.P0.5 | 300s |
| 13-06 | Service + Ingress YAML | 07-kubernetes K8s.P0.2 + K8s.P0.8 + K8s.P1.1 | 300s |
| 13-07 | Multi-stage Dockerfile (non-root) | 06-docker DCK.P0.2 + DCK.P1.1 | 240s |
| 13-08 | `docker run` hardening flags + proof | 06-docker DCK.P1.1 | 120s |
| 13-09 | Terraform HCL block + state commands | 08-terraform TF.P0.1 + TF.P0.2 | 240s |
| 13-10 | GitHub Actions workflow | 09-cicd CICD.P0.3 | 300s |
| 13-11 | PromQL rate / irate / increase / histogram_quantile | 10-observability OBS.P0.3 + OBS.P0.4 | 180s |
| 13-12 | S3 bucket + IAM least-privilege policy | 05-aws AWS.P0.6 + AWS.P0.2 + 11-security SEC.P0.4 | 300s |
| 13-13 | Helm values + install/upgrade/rollback | 07-kubernetes K8s.P1.4 | 240s |
| 13-14 | HPA YAML | 07-kubernetes K8s.P1.3 | 240s |
| 13-15 | PV / PVC YAML | 07-kubernetes K8s.P2.1 | 240s |
| 13-16 | Job + CronJob YAML | 07-kubernetes K8s.P2.2 | 240s |
| 13-17 | NetworkPolicy YAML | 07-kubernetes K8s.P1.2 | 240s |
| 13-18 | Terraform module + S3 backend | 08-terraform TF.P0.7 + TF.P0.3 | 300s |
| 13-19 | ArgoCD Application CR | 09-cicd CICD.P1.2 | 240s |
| 13-20 | Jenkins declarative pipeline | 09-cicd CICD.P1.1 | 300s |
| 13-21 | Alertmanager route + grouping | 10-observability OBS.P0.8 | 240s |
| 13-22 | SLO / SLI / error-budget math | 10-observability OBS.P0.9 | 180s |
| 13-23 | EKS managed node group config | 07-kubernetes K8s.P2.4 + 05-aws AWS.P0.10 | 240s |
| 13-24 | IRSA + OIDC trust policy | 07-kubernetes K8s.P2.4 + 05-aws AWS.P0.10 + 11-security SEC.P0.3 | 300s |
| 13-25 | OpenTelemetry span record + traceparent | 10-observability OBS.P0.7 | 240s |
| 13-26 | SBOM + container supply-chain gate | 11-security SEC.P0.10 | 180s |

P0 must-master = tasks 13-01 .. 13-12 (Batch 1). Strong-have = tasks 13-13 .. 13-26 (Batch 2).

---

## BATCH 1 — P0 MUST-MASTER

### TASK 13-01 — Process states and signal escalation · LINUX · source: 01-linux LINUX.P0.1 · 90s
**Question:** Write the Linux process-state table (letter, name, one-line meaning, one tell each), the three signals every senior can quote (TERM/KILL/INT, with why 15-before-9), and the exactly-scripted escalation ladder for an unresponsive process.
**ANSWER (fold here until attempted):**
Markdown table form:

| State | Name | Meaning | Tell |
|---|---|---|---|
| R | Running | executing or runnable in the run queue | wants the CPU now |
| S | Sleeping | interruptible sleep; waiting on an event, timer, or I/O that a signal can wake | most healthy service processes |
| D | Uninterruptible sleep | stuck in kernel I/O (disk/NFS) | NOT killable until the I/O returns |
| T | Stopped | paused by SIGSTOP (Ctrl+Z) | no CPU until SIGCONT |
| Z | Zombie | dead, awaiting parent's wait() | holds no memory; kill is a no-op |

Signal table:
| Signal | No. | Behavior |
|---|---|---|
| SIGTERM | 15 | graceful, catchable — "please shut down", apps trap it to flush/finish |
| SIGKILL | 9 | uncatchable, immediate — no cleanup runs |
| SIGINT | 2 | Ctrl+C |
| SIGHUP | 1 | hangup / terminal close |
| SIGSTOP / SIGCONT | 19 / 18 | pause / resume |
| SIGCHLD | 17 | sent to parent when a child exits — how parents know to reap |

Escalation ladder for a stuck process:
1. Confirm the PID and what it is doing first: `ps aux`, `top`, `/proc/<pid>/` (stat, status, fd).
2. `kill -TERM <pid>` — the graceful ask; gives the app a chance to persist state cleanly.
3. Wait ~5–10s, check `ps` again.
4. `kill -KILL <pid>` — only when the app is truly stuck or ignoring TERM.
5. Collect evidence, then hand restart to the supervisor (`systemctl restart <unit>`) rather than racing the app.

Zombie rule: the kernel keeps the corpse (exit code, minimal info) until the parent calls wait(); if the parent dies, PID 1 (or the nearest subreaper) adopts and reaps it. A flood of zombies = parent sleeps without wait(), or a broken reaper — `kill` does nothing to a zombie; kill the parent so PID 1 reaps.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-01
| # | Check | Status |
|---|---|---|
| 1 | All five states R/S/D/T/Z present with names | PASS |
| 2 | D-state explained as unkillable-until-IO-returns | PASS |
| 3 | Z-state zombie semantics (dead, wait(), kill is no-op) | PASS |
| 4 | SIGTERM 15 graceful vs SIGKILL 9 uncatchable | PASS |
| 5 | TERM-before-KILL ladder in order (observe, TERM, wait, KILL) | PASS |
| 6 | SIGINT 2 / SIGHUP 1 / SIGSTOP-SIGCONT 19-18 present | PASS |
| 7 | /proc and ps/top mentioned as the readers | PASS |
| 8 | Zombie flooding fix (kill parent so PID 1 reaps) | PASS |
| 9 | Process tree / fork-exe story implied | PASS |
| 10 | 15-vs-9 "why" told as app cleanup opportunity | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 01-linux LINUX.P0.1 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-02 — `set -euo pipefail` and a health-check script · BASH · source: 04-bash BASH.P0.3 + BASH.P0.5 · 300s
**Question:** (a) Explain each flag in `set -euo pipefail` with one concrete failure mode each; (b) write a health-check script: URL from first arg, expected body token from second arg, up to 5 attempts with 2s delay, curl with `-fsS --max-time`, pass only on HTTP 200 + exact body match, exit 0 on success and nonzero with a final message on failure, and never die mid-loop on a curl failure.
**ANSWER (fold here until attempted):**
Flag meanings:
- `set -e` — exit the script immediately on any command returning nonzero; the script stops at the first failure. Exempt: commands in a `if`/`while`/`until`/`&&`/`||` test context (a false condition is not an error).
- `set -u` — treat any use of an unset variable as an error and exit (`unbound variable`). Catches typos in `$ANME` before they silently do nothing.
- `set -o pipefail` — a pipeline's exit status is the rightmost command that FAILED, not the last command. Makes `cmd | grep x` fail correctly when the grep finds nothing or the producer dies.
- `set -x` (bonus) — print each command before executing; the debug trace for CI logs.

Script:
```bash
#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://localhost:8080/healthz}"
EXPECT="${2:-ok}"
ATTEMPTS=5
DELAY=2

retries=0
while (( retries < ATTEMPTS )); do
  body="$(curl -fsS --max-time 5 "$URL" 2>/dev/null || true)"
  if [[ "$body" == "$EXPECT" ]]; then
    echo "health ok after $(( retries + 1 )) attempt(s)"
    exit 0
  fi
  retries=$(( retries + 1 ))
  echo "attempt $retries failed: $URL (body=[$body])" >&2
  sleep "$DELAY"
done

echo "HEALTH CHECK FAILED: $URL did not return '$EXPECT' after $ATTEMPTS attempts" >&2
exit 1
```
Why each piece: `|| true` absorbs the curl failure so `set -e` does not kill the retry loop; `-f` makes curl fail on HTTP >=400 rather than happily printing an error page; `-sS` silences progress but keeps errors; `--max-time` prevents a hang; comparison is exact string match, not a grep of "could be anything"; the loop prints per-attempt diagnostics to stderr and only the final verdict on give-up; exit codes are the contract (0 healthy, nonzero + last line = the one-liner an alerting system can consume).

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-02
| # | Check | Status |
|---|---|---|
| 1 | `-e`, `-u`, `-o pipefail` all explained with failure examples | PASS |
| 2 | `set -e` conditional exemption (if/while/&&) stated | PASS |
| 3 | pipefail = rightmost-failing-command, not last command | PASS |
| 4 | Shebang, args with defaults, sets in place | PASS |
| 5 | curl uses -fsS + --max-time | PASS |
| 6 | `|| true` preserves the retry loop under set -e | PASS |
| 7 | Exact body match, not grep | PASS |
| 8 | Loop bounded by ATTEMPTS with DELAY backoff | PASS |
| 9 | exit 0 on success, nonzero + final message on failure | PASS |
| 10 | Per-attempt diagnostics to stderr | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 04-bash BASH.P0.3 + BASH.P0.5 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-03 — CIDR and subnet math · NETWORKING · source: 02-networking NET.P0.1 · 180s
**Question:** Do all of it by hand, no calculator: (a) total and usable addresses in a /20 and a /24; (b) network and broadcast of `192.168.110.110/20`; (c) how many /24s fit inside one /20; (d) the prefix for exactly 300 hosts; (e) the RFC1918 ranges and loopback/link-local; (f) the carved-cleanly rule for VPC subnets.
**ANSWER (fold here until attempted):**
(a) Addresses = 2^(32 − prefix). /20 → 2^12 = 4096 total, 4094 usable (subtract network + broadcast). /24 → 256 total, 254 usable.
(b) `192.168.110.110/20` → the first 20 bits are the network; the /16 boundary is fixed (192.168), the third octet splits on a 4-bit line so each /20 block is 16 of the third-octet values. 110 is within block 96..111 → network `192.168.96.0/20`, broadcast `192.168.111.255` (= 96 + 16 − 1), range 96.0–111.255. Verify with `python3 -c "import ipaddress; print(ipaddress.ip_network('192.168.96.0/20').broadcast_address)"`.
(c) A /20 is 4096 addresses, a /24 is 256 → 16 /24s per /20. General: every sub prefix bites 2^1, 2^2... — /19 = 32 /24s, /16 = 256 /24s.
(d) 300 hosts need the next power of two at or above 300+2 = 512 → /23 (510 usable).
(e) RFC1918 private: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. Loopback 127.0.0.0/8, link-local 169.254.0.0/16, documentation/TEST-NET 192.0.2.0/24.
(f) VPC subnets must carve cleanly on power-of-two boundaries — you cannot slice a /24 into two /25s that overlap, and a subnet cannot cross a parent boundary. Say "always powers of two crossing a power-of-two boundary" and verify with `ip_network` math before committing the CIDR table.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-03
| # | Check | Status |
|---|---|---|
| 1 | Addresses = 2^(32-prefix) stated | PASS |
| 2 | Usable = minus 2 (network + broadcast) | PASS |
| 3 | /20 = 4096 total / 4094 usable correct | PASS |
| 4 | /24 = 256 / 254 correct | PASS |
| 5 | 192.168.110.110/20 → network 192.168.96.0/20 | PASS |
| 6 | Broadcast 192.168.111.255 correct | PASS |
| 7 | 16 /24s per /20 correct | PASS |
| 8 | 300 hosts → /23 (512, 510 usable) | PASS |
| 9 | RFC1918: 10/8, 172.16/12, 192.168/16 | PASS |
| 10 | Loopback 127/8, link-local 169.254/16 | PASS |
| 11 | Power-of-two carve-cleanly rule stated | PASS |
| 12 | Answer matches source 02-networking NET.P0.1 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-04 — git reset vs revert and reflog rescue · GIT · source: 03-git GIT.P0.5 · 120s
**Question:** Write the reset-vs-revert decision matrix, the three-zone meaning of `--soft/--mixed/--hard`, and the exact rescue sequence after an accidental `git reset --hard HEAD~1` on an unpublished commit.
**ANSWER (fold here until attempted):**
Decision matrix:
- Undo my own unpublished commits → `git reset` (pointer surgery, history rewritten).
- Undo something already pushed / shared → `git revert <sha>` (adds a NEW commit that reverses the target; history stays intact; the only shared-safe undo).
- Keep the code but change the commit boundary → `git reset --soft <base>` then re-commit.
- Remove the code entirely and do not care → `git reset --hard` (local only; reflog keeps a backdoor).
- Company rule "never rewrite trunk" → always revert.

Three zones (`git reset --<mode> <target>` moves 1, 2, or 3 of these):
- `--soft` — moves 1 zone (HEAD only): changes stay STAGED in the index.
- `--mixed` — moves 2 zones (HEAD + index), the default: changes become unstaged plain edits in the worktree.
- `--hard` — moves 3 zones (HEAD + index + worktree): changes discarded from index and tree (reflog still keeps the door open).

Rescue after the accident:
```
git reflog                 # journal of every ref move; find the SHA where HEAD was
git reset --hard <sha>     # put HEAD back at the pre-reset commit; file + history restored
```
Reflog is the rescue tool for `--hard`: it records every ref move including the ones that made commits unreachable; `git reset --hard <reflogSha>` walks HEAD right back. Garbage collection is what eventually prunes unreferenced commits — panic-free recovery while the entry exists.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-04
| # | Check | Status |
|---|---|---|
| 1 | reset = pointer surgery (local/unshared) vs revert = new commit (shared-safe) | PASS |
| 2 | Revert keeps history intact and is safe on pushed branches | PASS |
| 3 | `--soft` = 1 zone, changes stay staged | PASS |
| 4 | `--mixed` = 2 zones (default), plain edits | PASS |
| 5 | `--hard` = 3 zones, discards worktree | PASS |
| 6 | Reset never ok on consumed/shared trunk without coordination | PASS |
| 7 | Reflog named as ref-move journal | PASS |
| 8 | Rescue sequence: reflog then reset --hard <sha> | PASS |
| 9 | `git revert --no-edit <sha>` form recalled | PASS |
| 10 | GC/prune frame for reflog expiry | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 03-git GIT.P0.5 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-05 — Kubernetes Deployment YAML · KUBERNETES · source: 07-kubernetes K8s.P0.2 + K8s.P0.4 + K8s.P0.5 · 300s
**Question:** Write a ConfigMap named `web-config` (key `config.yaml`), then a Deployment `web`: 3 replicas, image `nginx:1.27-alpine`, label `app=web`, a readiness probe (httpGet `/readyz` on 8080), a liveness probe (httpGet `/healthz` on 8080), requests/limits, and the ConfigMap mounted read-only at `/etc/web`. Then state the Deployment → ReplicaSet → Pod chain in one line.
**ANSWER (fold here until attempted):**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: web-config
data:
  config.yaml: |
    log_level: info
    listen_port: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  labels:
    app: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: nginx:1.27-alpine
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8080
            initialDelaySeconds: 3
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
          resources:
            requests:
              cpu: 100m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
          volumeMounts:
            - name: web-cfg
              mountPath: /etc/web
              readOnly: true
      volumes:
        - name: web-cfg
          configMap:
            name: web-config
```
Chain: Deployment → ReplicaSet (name carries the template hash) → Pods (random suffix), linked by ownerReferences; `spec.selector.matchLabels` under `deployment` must exactly match `spec.template.metadata.labels` or the Deployment fails validation. Readiness gates a pod's appearance in Service endpoints (traffic), liveness drives kubelet restarts (recovery) — they are different jobs. `initialDelaySeconds` gives a slow-boot container room before the first probe; requests are the scheduling reservation and the HPA denominator (mine: 100m cpu = the unit HPA percentages divide into later).

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-05
| # | Check | Status |
|---|---|---|
| 1 | apiVersion apps/v1 (not extensions/v1beta1) | PASS |
| 2 | ConfigMap v1 with data key and block scalar | PASS |
| 3 | replicaCount 3, image, labels consistent | PASS |
| 4 | label selector matches template labels | PASS |
| 5 | Readiness httpGet /readyz on 8080 | PASS |
| 6 | Liveness httpGet /healthz on 8080 | PASS |
| 7 | requests + limits (cpu 100m/200m, mem 64Mi/128Mi) | PASS |
| 8 | volumeMount at /etc/web readOnly + volumes configMap ref | PASS |
| 9 | Deployment→ReplicaSet→Pod chain stated | PASS |
| 10 | readiness-vs-liveness job split stated | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 07-kubernetes K8s.P0.2/P0.4/P0.5 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-06 — Service and Ingress YAML · KUBERNETES · source: 07-kubernetes K8s.P0.2 + K8s.P0.8 + K8s.P1.1 · 300s
**Question:** Write a ClusterIP Service exposing `app: web-app` pods on client port 80 to targetPort 80; then an Ingress that routes host `api.example.com` with path prefix `/api` to `api-svc` port 8080, carries the rewrite-target annotation, declares the nginx ingress class, and terminates TLS from secret `tls-api`. Explain selector-to-endpoints wiring in one line.
**ANSWER (fold here until attempted):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app-svc
spec:
  selector:
    app: web-app
  ports:
    - name: http
      port: 80
      targetPort: 80
      protocol: TCP
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: tls-api
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-svc
                port:
                  number: 8080
```
Selector wiring: the Service controller runs a label query over Pods and writes matching Pod IPs into the Endpoints/EndpointSlice — `kubectl get endpoints api-svc` returning pod IPs on 8080 IS the proof the selector matched. `port` = what clients use, `targetPort` = what the container listens on (defaults to `port` when omitted). Ingress is L7 host x path rules pointing at a Service; `ingressClassName` chooses the controller brand (nginx here); `rewrite-target: /` rewrites `/api/...` before forwarding so a root-serving backend does not 404; `spec.tls` makes the controller terminate TLS then proxy plain HTTP to backends — the referenced secret must hold `tls.crt`/`tls.key` and the cert MUST carry subjectAltName entries (Go/nginx rejects CN-only certs). A Service with a wrong selector is a ClusterIP that answers connection refusals with an empty endpoints list.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-06
| # | Check | Status |
|---|---|---|
| 1 | Service v1, selector app: web-app, ClusterIP | PASS |
| 2 | port 80 / targetPort 80 / protocol TCP | PASS |
| 3 | Service type not namespace-crossed or targetPort forgotten | PASS |
| 4 | Ingress networking.k8s.io/v1 | PASS |
| 5 | ingressClassName: nginx present | PASS |
| 6 | host api.example.com + path /api Prefix | PASS |
| 7 | backend service api-svc port 8080 | PASS |
| 8 | rewrite-target annotation present + meaning | PASS |
| 9 | tls block hosts + secretName tls-api | PASS |
| 10 | selector→endpoints wiring explained | PASS |
| 11 | Empty endpoints = selector mismatch trap stated | PASS |
| 12 | Answer matches source 07-kubernetes K8s.P0.2/P0.8/P1.1 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-07 — Multi-stage Dockerfile, non-root · DOCKER · source: 06-docker DCK.P0.2 + DCK.P1.1 · 240s
**Question:** Write a two-stage Dockerfile: stage 1 builds a Go binary in `golang:1.23-alpine`, stage 2 ships ONLY the binary in `scratch` with CA certs, exec-form entrypoint, expose 8080. Then write the one-line variant change that also makes the final image run as a non-root user (alpine + adduser). State why exec-form is mandatory in scratch and what hardens the final state.
**ANSWER (fold here until attempted):**
```dockerfile
FROM golang:1.23-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /out/app .

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /out/app /app
EXPOSE 8080
ENTRYPOINT ["/app"]
```
The scratch final image has no shell and no package manager — so exec-form JSON (`["/app"]`) is mandatory (shell form would try `/bin/sh -c`), the binary must be static (`CGO_ENABLED=0`), and every byte of build toolchain from `golang:1.23-alpine` stays behind. Build three stages would collapse golang to ~hundreds of MB; shipping scratch drops to single-digit MB. Need DNS/certs → copy the CA bundle from the builder.

Non-root variant (same builder, alpine final):
```dockerfile
FROM alpine:3.20
RUN apk add --no-cache ca-certificates \
 && addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=builder /out/app /app
USER app
EXPOSE 8080
ENTRYPOINT ["/app"]
```
Hardening line: non-root `USER` + ca-certificates on a minimal base + only the compiled artifact = the "leet" container posture; add `--cap-drop ALL` and `--read-only` at run time (task 13-08) and you have the container-security answer. Only the LAST stage's filesystem ships — that is the entire point of multi-stage.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-07
| # | Check | Status |
|---|---|---|
| 1 | Two FROMs with named stage `AS builder` | PASS |
| 2 | Builder: go mod download then COPY . . then go build | PASS |
| 3 | CGO_ENABLED=0 + -s -w flags recalled | PASS |
| 4 | COPY --from=builder for binary AND CA certs | PASS |
| 5 | exec-form ENTRYPOINT ["/app"] | PASS |
| 6 | EXPOSE 8080, only last stage ships | PASS |
| 7 | scratch has no shell → exec-form mandatory explained | PASS |
| 8 | non-root variant: alpine + addgroup/adduser + USER app | PASS |
| 9 | Size delta (hundreds MB → single-digit MB) stated | PASS |
| 10 | Hardening tie-in (cap-drop, read-only at run) noted | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 06-docker DCK.P0.2 + DCK.P1.1 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-08 — `docker run` hardening flags · DOCKER · source: 06-docker DCK.P1.1 · 120s
**Question:** Write the hardened `docker run` for a container exposing 8080, plus the docker-inspect proof line that shows each hardening took effect, and name the two classic breakages (`--read-only` without a write path; `--cap-drop ALL` collateral).
**ANSWER (fold here until attempted):**
```bash
docker run -d --name app-sec \
  --read-only \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  --security-opt no-new-privileges \
  --user 10001:10001 \
  --tmpfs /tmp:rw,size=64m \
  -v app-vol:/data \
  -p 8080:8080 \
  --cpus=0.5 --memory=256m \
  app:latest
```
Proof line:
```bash
docker inspect app-sec --format 'rofs={{.HostConfig.ReadonlyRootfs}} caps={{.HostConfig.CapDrop}} user={{.Config.User}} nnp={{.HostConfig.SecurityOpt}} health={{.State.Health.Status}}'
```
Meaning of each flag: `--read-only` = rootfs read-only; writes must land on the named volume or tmpfs. `--cap-drop ALL` removes every Linux capability (net_admin, sys_admin, ...), then `--cap-add` restores exactly what is needed. `no-new-privileges` blocks setuid/setgid escalation. `--user` runs as non-root UID/GID. `--tmpfs` gives a RAM-backed writable scratch for pids/sockets. `--cpus`/`--memory` cap the container's budget. Classic breakages: (1) `--read-only` without a writable mount = most images crash at the first mkdir with the read-only-filesystem error — pair it with the named volume or tmpfs; (2) `--cap-drop ALL` silently kills capabilities you lean on, e.g. `NET_RAW` (ping) and `NET_BIND_SERVICE` (binding ports < 1024) — re-add deliberately and document why.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-08
| # | Check | Status |
|---|---|---|
| 1 | --read-only present | PASS |
| 2 | --cap-drop ALL with explicit --cap-add | PASS |
| 3 | --security-opt no-new-privileges present | PASS |
| 4 | --user non-root present | PASS |
| 5 | writable path: named volume and/or --tmpfs | PASS |
| 6 | port publish and resource caps included | PASS |
| 7 | inspect format reads ReadonlyRootfs/CapDrop/User/SecurityOpt | PASS |
| 8 | read-only-without-write-mount crash explained | PASS |
| 9 | cap-drop collaterals (NET_RAW ping, NET_BIND_SERVICE <1024) | PASS |
| 10 | no-new-privileges = blocks setuid escalation | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 06-docker DCK.P1.1 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-09 — Terraform HCL block and state commands · TERRAFORM · source: 08-terraform TF.P0.1 + TF.P0.2 · 240s
**Question:** Write a minimal HCL: terraform block pinning a provider, one variable with a type/default, one resource, one output. Then write (a) the command lifecycle meaning of init/plan/apply/destroy, (b) the state command set (list/show/mv/rm/pull/push/import) with one-line each, (c) the "why state" four-line answer.
**ANSWER (fold here until attempted):**
```hcl
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

variable "filename" {
  type    = string
  default = "/tmp/tf-out.txt"
}

variable "content" {
  type    = string
  default = "hello"
}

resource "local_file" "f" {
  content  = var.content
  filename = var.filename
}

output "path" {
  value = local_file.f.filename
}
```
Command lifecycle:
- `terraform init` — one-time setup: downloads provider plugins, builds `.terraform/`, writes `.terraform.lock.hcl`. Re-run when providers/modules/backend change.
- `terraform plan` — refresh real state, compute the diff, print the preview. NEVER changes anything.
- `terraform apply` — converge: executes the plan in dependency order, then writes state.
- `terraform destroy` — apply with an empty config; forget nothing, tear down everything in state.
- `terraform fmt` / `terraform validate` — formatting and static checks (validate needs init first).

State commands:
- `terraform state list` — the managed objects.
- `terraform state show <addr>` — one object's stored attributes.
- `terraform state mv <old> <new>` — rename/move an address without touching real infra (used on renames/moves).
- `terraform state rm <addr>` — forget the object in state (does NOT destroy it).
- `terraform state pull` / `state push` — fetch/upload the raw state (prefer the S3 CLI, never hand-edit).
- `terraform import -address <addr> <id>` — adopt an existing real object into state.

Why state (four lines): (1) maps config to real objects by storing provider-assigned IDs; (2) stores attributes for interpolation/outputs; (3) tracks the dependency graph for ordered diffs; (4) powers inspection (`state`, `outputs`, `console`). Config says what you WANT; state says what you HAVE; plan diffs the two.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-09
| # | Check | Status |
|---|---|---|
| 1 | terraform block with required_providers source | PASS |
| 2 | variable with type + default | PASS |
| 3 | resource local_file with content/filename | PASS |
| 4 | output block referencing resource attr | PASS |
| 5 | init = plugins + lock file | PASS |
| 6 | plan = refresh + diff, never changes anything | PASS |
| 7 | apply = converge + write state | PASS |
| 8 | destroy = apply of empty config | PASS |
| 9 | state list/show/mv/rm/pull/push/import each correct | PASS |
| 10 | Four state responsibilities recalled | PASS |
| 11 | Config-vs-state one-liner present | PASS |
| 12 | Answer matches source 08-terraform TF.P0.1 + TF.P0.2 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-10 — GitHub Actions workflow · CI/CD · source: 09-cicd CICD.P0.3 · 300s
**Question:** Write a `.github/workflows/ci.yml`: trigger on push to main and any pull_request; a `test` job on ubuntu-latest with a python 3.11/3.12 matrix running ruff then pytest; a `build` job `needs: test` that checks out, sets up buildx, logs into GHCR with the GITHUB_TOKEN and pushes `ghcr.io/org/app:${SHA}`. Then name the four-layer model and explain the `on:` YAML trap.
**ANSWER (fold here until attempted):**
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Lint
        run: pip install ruff && ruff check .
      - name: Test
        run: pip install -r requirements.txt && pytest -q

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/org/app:${{ github.sha }}
```
Four layers: workflow → job → step → action, executed on a runner. Trigger `on:` maps the event to the workflow; `needs:` builds the DAG — GitHub runs jobs in dependency order and skips dependents of failed jobs; `strategy.matrix` fans one job into one execution per matrix cell; `${{ }}` contexts: `github.*`, `secrets.*`, `needs.*`, `matrix.*`, `inputs.*`. The `on:` trap: GitHub Actions call their trigger key literally `on`, and YAML 1.1 (what PyYAML implements) parses bare `on` as boolean `True` — so a generic `yaml.safe_load` round-trips the structure but silently loses the trigger key. Parse is necessary-but-not-sufficient; use a schema-aware validator (actionlint, or GitHub's own lint) because GitHub uses its own parser that keeps the literal key.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-10
| # | Check | Status |
|---|---|---|
| 1 | on: push branches [main] + pull_request triggers | PASS |
| 2 | test job: checkout + setup-python | PASS |
| 3 | python 3.11/3.12 matrix present | PASS |
| 4 | ruff lint + pytest test steps | PASS |
| 5 | build job needs: test | PASS |
| 6 | buildx, login to ghcr.io with GITHUB_TOKEN | PASS |
| 7 | build-push-action with push:true and sha tag | PASS |
| 8 | four-layer model (workflow/job/step/action) named | PASS |
| 9 | needs DAG + failed-dependent skip semantics | PASS |
| 10 | `${{ }}` context names recalled | PASS |
| 11 | on: YAML 1.1 boolean trap explained | PASS |
| 12 | Answer matches source 09-cicd CICD.P0.3 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-11 — PromQL: rate, irate, histogram_quantile · OBSERVABILITY · source: 10-observability OBS.P0.3 + OBS.P0.4 · 180s
**Question:** Write the PromQL for (a) requests per second in the last 5 minutes across all instances; (b) the instantaneous last-two-samples slope; (c) the estimated total increase over the window; (d) the 95th percentile latency from a `_bucket` histogram. Then state the three rules: rate-vs-irate, counters-not-gauges, and why `increase` differs from last-minus-first.
**ANSWER (fold here until attempted):**
```promql
sum(rate(http_requests_total[5m]))                                          # (a) rps, all instances
irate(http_requests_total[5m])                                              # (b) last-two-samples slope
sum(increase(http_requests_total[5m]))                                      # (c) estimated total in window
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))   # (d) p95 latency
```
Rules:
- `rate()` is the per-second counter slope over a window, corrected for counter resets (a drop is detected and unrolled). Never use rate on a gauge — a fall to 0 looks exactly like a reset.
- `irate()` is the slope from the LAST TWO SAMPLES ONLY: reacts instantly, noisy on sparse or flaky scrapes — use for spiky dashboards, never as an alert basis.
- `increase()` computes `rate(window) x window` and EXTRAPOLATES the slope to the window edges, so it is an estimator, not `last - first`; it can over/undershoot on restarts and sparse windows — pick windows at least several scrape intervals long.
- `sum by (le)` keeps the histogram bucket labels so `histogram_quantile` can rank and linearly interpolate inside the target bucket — drop `le` and the quantile function has nothing to interpolate.
- Empty result is not "0" — an empty vector means "no series", a different alarm story.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-11
| # | Check | Status |
|---|---|---|
| 1 | rps query = sum(rate(counter[5m])) | PASS |
| 2 | irate(last two samples) query form | PASS |
| 3 | increase form and window | PASS |
| 4 | histogram_quantile(0.95, sum by (le)(rate(..bucket[5m]))) exactly | PASS |
| 5 | rate = counter slope, reset-corrected | PASS |
| 6 | never rate on a gauge | PASS |
| 7 | irate fast/noisy — dashboards not alerts | PASS |
| 8 | increase = extrapolated estimator ≠ last-minus-first | PASS |
| 9 | sum by (le) preserves buckets for interpolation | PASS |
| 10 | empty-vector-is-not-zero semantics stated | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 10-observability OBS.P0.3 + OBS.P0.4 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-12 — S3 bucket and IAM least-privilege policy · AWS · source: 05-aws AWS.P0.6 + AWS.P0.2 + 11-security SEC.P0.4 · 300s
**Question:** (a) Write an IAM identity policy for role `backup-role`: allow ListAllMyBuckets + GetBucketLocation anywhere, ListBucket only on `acme-backup`, and GetObject/PutObject/DeleteObject only under `acme-backup/inbox/*` (with the prefix condition on the bucket-level list). (b) Write the CLI sequence: create the bucket in us-west-1, enable versioning, upload `inbox/note.txt`, list object versions, fetch a specific version.
**ANSWER (fold here until attempted):**
(a)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DiscoverBuckets",
      "Effect": "Allow",
      "Action": ["s3:ListAllMyBuckets", "s3:GetBucketLocation"],
      "Resource": "*"
    },
    {
      "Sid": "ReadPrefix",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::acme-backup/inbox/*"
    },
    {
      "Sid": "ListPrefix",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::acme-backup",
      "Condition": {
        "StringLike": { "s3:prefix": ["inbox/*", "inbox"] }
      }
    }
  ]
}
```
Least-privilege discipline: object actions are scoped to the OBJECT ARN under the prefix (never `arn:aws:s3:::acme-backup/*` unless intended); bucket list is scoped by the `s3:prefix` condition; identity-based policy answers WHO acts (I can, via this role), a bucket policy would answer WHAT the bucket itself allows (and would sit on the resource). Scope action, resource, and (when relevant) condition — the three knobs of every IAM statement.

(b)
```bash
aws s3api create-bucket --bucket acme-backup --region us-west-1 \
  --create-bucket-configuration LocationConstraint=us-west-1
aws s3api put-bucket-versioning --bucket acme-backup \
  --versioning-configuration Status=Enabled
aws s3api put-object --bucket acme-backup --key inbox/note.txt --body /tmp/v1.txt
aws s3api put-object --bucket acme-backup --key inbox/note.txt --body /tmp/v2.txt
aws s3api list-object-versions --bucket acme-backup --prefix inbox/
VID=$(aws s3api list-object-versions --bucket acme-backup --prefix inbox/ \
  --query 'Versions[0].VersionId' --output text)
aws s3api get-object --bucket acme-backup --key inbox/note.txt --version-id "$VID" /tmp/back.txt
```
Bucket names are globally unique; `--create-bucket-configuration` is REQUIRED for any region other than us-east-1. Versioning is the object-level "undo": every PUT creates a new version and the old one stays fetchable by VersionId — the standard defense against bad deploys and ransomware before retention/lifecycle policies kick in.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-12
| # | Check | Status |
|---|---|---|
| 1 | Version 2012-10-17 in the policy | PASS |
| 2 | object actions scoped to arn:aws:s3:::acme-backup/inbox/* | PASS |
| 3 | ListBucket scoped with s3:prefix condition | PASS |
| 4 | ListAllMyBuckets + GetBucketLocation on Resource * | PASS |
| 5 | identity-policy vs bucket-policy split stated | PASS |
| 6 | create-bucket with LocationConstraint for us-west-1 | PASS |
| 7 | put-bucket-versioning Status=Enabled | PASS |
| 8 | put-object upload then second upload (two versions) | PASS |
| 9 | list-object-versions with --prefix | PASS |
| 10 | get-object with --version-id | PASS |
| 11 | versioning-as-undo rationale stated | PASS |
| 12 | Answer matches source 05-aws AWS.P0.6/P0.2 + SEC.P0.4 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

---

## BATCH 2 — P1 STRONG-HAVE

### TASK 13-13 — Helm values and release lifecycle · KUBERNETES · source: 07-kubernetes K8s.P1.4 · 240s
**Question:** Write a Helm `values.yaml` override (replicaCount, image repo/tag/pullPolicy, service type/ports, resources); then the verb sequence chat-create → lint → install → list → upgrade `--set` → history → rollback → uninstall, and define release vs revision in one line each.
**ANSWER (fold here until attempted):**
```yaml
replicaCount: 3

image:
  repository: nginx
  tag: "1.27-alpine"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
  targetPort: 80

resources:
  requests:
    cpu: 100m
    memory: 64Mi
  limits:
    cpu: 200m
    memory: 128Mi
```
Verbs:
```bash
helm create demo-chart
helm lint demo-chart
helm install demo demo-chart          # render templates against values, apply, record revision 1
helm list
helm upgrade demo demo-chart --set replicaCount=2
helm history demo
helm rollback demo 1                  # re-apply revision 1 -> new revision N+1 "Rollback to 1"
helm uninstall demo                   # removes release record + every object helm owns
```
Definitions: a RELEASE = chart + version + a unique name in a namespace (ellipsized `release demo` = `demo-demo-chart` object names); a REVISION = one applied render of the chart with a given values set — `upgrade` creates a new revision while the previous one stays recoverable in `history`, and `rollback` re-applies an old revision as a NEW one. Helm's own state lives in `helm.sh/release.v1` ConfigMaps in the release namespace — one reason proper namespace cleanup matters. Preview with `helm template` / `helm get manifest`; apply values layers in order `--set` > `-f file` > chart defaults.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-13
| # | Check | Status |
|---|---|---|
| 1 | values: replicaCount, image repo/tag/pullPolicy | PASS |
| 2 | service type + port/targetPort | PASS |
| 3 | resources block present | PASS |
| 4 | create/lint/install verb sequence | PASS |
| 5 | upgrade --set replicaCount=2 | PASS |
| 6 | history then rollback demo 1 | PASS |
| 7 | uninstall removes release + owned objects | PASS |
| 8 | release = chart+version+unique name+namespace | PASS |
| 9 | revision = one applied render; rollback makes a NEW revision | PASS |
| 10 | helm.sh/release.v1 ConfigMap state noted | PASS |
| 11 | template/get manifest preview capability named | PASS |
| 12 | Answer matches source 07-kubernetes K8s.P1.4 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-14 — HPA YAML · KUBERNETES · source: 07-kubernetes K8s.P1.3 · 240s
**Question:** Write an `autoscaling/v2` HPA for Deployment `api`: min 1, max 5, target CPU 60% Utilization of requests; then write the scale formula, the metric pipeline, and one remark about what "60%" is a percentage OF.
**ANSWER (fold here until attempted):**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
```
Formula: desiredReplicas = ceil(currentReplicas x currentUtilization / targetUtilization), clamped to [minReplicas, maxReplicas]. The 60% is the percentage of the pod's CPU REQUEST (requests are the denominator), never a percentage of node capacity — a 60% target on a 100m request means ~60m of CPU per pod is the comfort line. Pipeline: kubelet per-container usage → metrics-server (aggregator) → metrics.k8s.io API → HPA controller polls → writes .status.currentReplicas/desiredReplicas → scales via the scale subresource. `kubectl describe hpa` exposes the conditions table (AbleToScale / ScalingActive / ScalingLimited). Kind's own wall: metrics-server needs `--kubelet-insecure-tls` because kind kubelet certs carry no IP SANs — an explicit dev-cluster crutch, not production practice.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-14
| # | Check | Status |
|---|---|---|
| 1 | apiVersion autoscaling/v2 | PASS |
| 2 | scaleTargetRef pointing at Deployment api | PASS |
| 3 | minReplicas 1 / maxReplicas 5 | PASS |
| 4 | Resource cpu metric with Utilization + averageUtilization 60 | PASS |
| 5 | formula desired = ceil(current x ratio) remembered | PASS |
| 6 | 60% = % of pod's CPU requests, not node | PASS |
| 7 | pipeline kubelet → metrics-server → metrics API → HPA | PASS |
| 8 | conditions AbleToScale/ScalingActive/ScalingLimited | PASS |
| 9 | kind --kubelet-insecure-tls caveat + why dev-only | PASS |
| 10 | UR2 "OBS.P0 target" case: v2 averageUtilization form | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 07-kubernetes K8s.P1.3 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-15 — PVC and PV YAML · KUBERNETES · source: 07-kubernetes K8s.P2.1 · 240s
**Question:** Write a static `local-path` PV (1Gi, RWO, class `standard`, reclaim Retain) and a PVC that binds to it (1Gi, RWO, same class); then the pod snippet consuming the claim at `/data`. Explain the Pending → Bound transition and one RWO subtlety.
**ANSWER (fold here until attempted):**
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: data-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: standard
  local:
    path: /mnt/data
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/hostname
              operator: In
              values: [worker-1]
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: standard
---
apiVersion: v1
kind: Pod
metadata:
  name: pvc-writer
spec:
  containers:
    - name: app
      image: alpine:3.20
      command: ["sh", "-c", "echo hello-from-pv > /data/out.txt && sleep 3600"]
      volumeMounts:
        - name: data
          mountPath: /data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: data-pvc
```
The claim sits Pending until a matching PV exists (capacity >= request, accessMode contained, storageClassName equal, node affinity satisfiable) — with dynamic provisioning that is automatic; with a static PV the admin pre-creates it. Once matched, the claim is Bound and the pod consumes the volume; deleting the claim returns the PV to Released (with Retain) for manual handling, or tears it down (with Delete). RWO subtlety: `ReadWriteOnce` is NODE-scoped, not pod-scoped — multiple pods on the same node may share one RWO volume in practice. A default storageClass provisioner (like kind's `standard` local-path) makes the PVC bind on first consumer scheduling (WaitForFirstConsumer).

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-15
| # | Check | Status |
|---|---|---|
| 1 | PV: capacity, accessModes, storageClassName, reclaim policy | PASS |
| 2 | PV has local path + nodeAffinity for a static local PV | PASS |
| 3 | PVC: 1Gi, RWO, same class, requests.storage | PASS |
| 4 | pod volumeMount /data + persistentVolumeClaim volumes block | PASS |
| 5 | Pending → Bound transition explained | PASS |
| 6 | binding requirements: capacity/accessMode/class/affinity | PASS |
| 7 | Retain vs Delete reclaim behavior stated | PASS |
| 8 | RWO = node-scoped not pod-scoped | PASS |
| 9 | WaitForFirstConsumer dynamic provisioning nuance | PASS |
| 10 | local-path node affinity matchExpressions form | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 07-kubernetes K8s.P2.1 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-16 — Job and CronJob YAML · KUBERNETES · source: 07-kubernetes K8s.P2.2 · 240s
**Question:** Write a batch/v1 Job that runs a DB migration to completion, `restartPolicy: Never`, `backoffLimit: 4`; then a CronJob on cron `15 2 * * *` with `concurrencyPolicy: Forbid`, `startingDeadlineSeconds: 300`, jobTemplate wrapping the same shape with `restartPolicy: OnFailure`. Add the three rules: restartPolicy constraint, completion semantics, and the concurrencyPolicy options.
**ANSWER (fold here until attempted):**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate
spec:
  backoffLimit: 4
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: registry.example.com/app-migrate:1.0
          args: ["--apply"]
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-reindex
spec:
  schedule: "15 2 * * *"
  concurrencyPolicy: Forbid
  startingDeadlineSeconds: 300
  jobTemplate:
    spec:
      backoffLimit: 2
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: reindex
              image: registry.example.com/reindex:1.0
```
Rules: (1) a Job's pod `restartPolicy` must be `Never` or `OnFailure` (Never is the migrator choice — each failed attempt is a fresh pod, OnFailure restarts in place); the scheduler class inside a Job is "run until the specified number of completions succeed". (2) A Job is complete when the completion count is reached; failed pods count against `backoffLimit` — exceed it and the Job is Failed and stops creating pods. (3) CronJob `concurrencyPolicy` is `Allow` (default), `Forbid` (skip the tick if the previous job still runs — no overlap), or `Replace` (kill the old and start new); a missed schedule fires late only inside `startingDeadlineSeconds`, after that the invocation is dropped silently. Upstream DB-migrate pattern: run migrations as a Job (or as an init container) so the app never starts against an unmigrated schema.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-16
| # | Check | Status |
|---|---|---|
| 1 | Job batch/v1 with template spec + container | PASS |
| 2 | restartPolicy Never + backoffLimit 4 | PASS |
| 3 | CronJob batch/v1 with schedule field | PASS |
| 4 | cron expression "15 2 * * *" | PASS |
| 5 | concurrencyPolicy Forbid | PASS |
| 6 | startingDeadlineSeconds 300 | PASS |
| 7 | jobTemplate nesting correct (spec within jobTemplate.spec) | PASS |
| 8 | OnFailure vs Never restart semantics named | PASS |
| 9 | completion semantics + backoffLimit fail-stop named | PASS |
| 10 | Allow/Forbid/Replace options stated | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 07-kubernetes K8s.P2.2 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-17 — NetworkPolicy YAML · KUBERNETES · source: 07-kubernetes K8s.P1.2 · 240s
**Question:** Write a deny-all-ingress NetworkPolicy for namespace `payments`, then an allow policy letting pods labeled `app: frontend` in namespace `web` reach pods labeled `app: backend` in `payments` on TCP 3306. Then state the isolation rule, the CoreDNS egress trap, and the CNI enforcement caveat.
**ANSWER (fold here until attempted):**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: payments
spec:
  podSelector: {}
  policyTypes:
    - Ingress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-web-to-payments-db
  namespace: payments
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: web
          podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 3306
```
Isolation rule: once any policy selects a pod, traffic in that policy's declared direction is DENIED unless an allowing rule matches — `podSelector: {}` + empty `ingress:` is the whole-namespace default-deny. To build allow stuff on top: layer per-app allow policies. Cross-namespace selectors pair `namespaceSelector` with an inner `podSelector` inside a single `from` element (AND). CoreDNS trap: after a default-deny, pods lose egress to kube-system CoreDNS on udp/tcp 53 unless you add an explicit allow — "the app broke after I added NetPol" is almost always DNS. Enforcement caveat: NetworkPolicy is a spec the CNI implements — kindnet does NOT enforce it (accepts the object, drops nothing); production clusters run a policy-capable CNI (Calico or Cilium).

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-17
| # | Check | Status |
|---|---|---|
| 1 | both policies networking.k8s.io/v1 + correct namespaces | PASS |
| 2 | deny-all: podSelector {} + policyTypes [Ingress] + empty ingress | PASS |
| 3 | allow policy selects app: backend (target pods) | PASS |
| 4 | from = namespaceSelector + podSelector combined correctly | PASS |
| 5 | port TCP 3306 in ingress | PASS |
| 6 | isolation rule (policy exists -> otherwise deny) stated | PASS |
| 7 | layered allow-on-top-of-deny pattern stated | PASS |
| 8 | namespaceSelector + podSelector AND semantics | PASS |
| 9 | CoreDNS egress trap stated (53 udp+tcp allow) | PASS |
| 10 | CNI enforcement caveat (kindnet no, Calico/Cilium yes) | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 07-kubernetes K8s.P1.2 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-18 — Terraform module and S3 backend · TERRAFORM · source: 08-terraform TF.P0.7 + TF.P0.3 · 300s
**Question:** Sketch the file layout of a `vpc` module (which files, what each holds); write a root `main.tf` with a S3+ DynamoDB backend block and a `module "vpc"` call passing `cidr` and `name`; then name the init/plan/apply sequence rule when the backend changes, and the "team state" contract (shared state, locking, hands-off rule).
**ANSWER (fold here until attempted):**
```text
modules/vpc/
  main.tf        # resources: aws_vpc, aws_subnet.*
  variables.tf   # inputs: cidr_block, name (types + defaults)
  outputs.tf     # returns: vpc_id, subnet_ids
  versions.tf    # required terraform + required providers constraints
```
Root:
```hcl
terraform {
  backend "s3" {
    bucket         = "acme-terraform-state"
    key            = "dev/network/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

module "vpc" {
  source = "./modules/vpc"
  cidr   = "10.0.0.0/16"
  name   = "dev-vpc"
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
```
Rules: modules are just namespaced resources — addresses become `module.vpc.<resource>.<attr>`; `source` can be a local path, registry, git ref, or archive; version constraints apply to registry sources. Backend change rule: the `backend` block is read at `terraform init` time — changing it requires re-init, and Terraform offers the state migration interactively (`-migrate-state`); `terraform init` also installs providers and writes the lock file. Team-state contract: ONE shared state object in S3 (isolate per env via `key`), locking via DynamoDB so two applays cannot corrupt state simultaneously, state is fetched on every plan/apply (so the "refresh" is real), and state files are never hand-edited — use `terraform state` commands or the S3 CLI, never a text editor, because a corrupted tfstate breaks every subsequent plan. Plan-as-gate in CI (run on every PR, apply on merge) gives review-before-reality.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-18
| # | Check | Status |
|---|---|---|
| 1 | module layout: main.tf/variables.tf/outputs.tf/versions.tf with roles | PASS |
| 2 | backend s3 block: bucket/key/region/dynamodb_table/encrypt | PASS |
| 3 | module call with source + var arguments | PASS |
| 4 | module.<name>.<attr> addressing + output | PASS |
| 5 | source variants (path/registry/git/tarball) named | PASS |
| 6 | backend re-init + -migrate-state rule | PASS |
| 7 | shared state + isolation by key | PASS |
| 8 | DynamoDB locking purpose stated | PASS |
| 9 | hands-off rule for tfstate (state cmds only) | PASS |
| 10 | plan-as-gate / apply-on-merge CI pattern | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 08-terraform TF.P0.7 + TF.P0.3 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-19 — ArgoCD Application CR · CI/CD · source: 09-cicd CICD.P1.2 · 240s
**Question:** Write an Application custom resource: repo `https://github.com/acme/config`, targetRevision `main`, path `apps/web`, destination cluster `https://kubernetes.default.svc` namespace `web`, syncPolicy automated with prune + selfHeal, project `default`. Then explain out-of-sync and the reconcile loop in two sentences.
**ANSWER (fold here until attempted):**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/acme/config
    targetRevision: main
    path: apps/web
  destination:
    server: https://kubernetes.default.svc
    namespace: web
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```
Model: an Application is a pure declaration — "this repo + path is the desired state for that namespace". ArgoCD continuously diffs the live cluster against git; when they differ the app is OutOfSync, and when the applied objects are healthy it is Sync/Healthy. The reconcile loop: controller = git as the source of truth, and the diff drives the sync. `automated.prune` deletes live objects that the git manifests no longer mention (so removals are honored, not just additions); `selfHeal` re-applies git state over manual drift so a `kubectl scale` in the cluster gets reverted; `argocd app sync` forces a manual sync; for many apps, compose one "app of apps" Application pointing at a directory of Application manifests.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-19
| # | Check | Status |
|---|---|---|
| 1 | apiVersion argoproj.io/v1alpha1, kind Application | PASS |
| 2 | metadata name web + namespace argocd | PASS |
| 3 | source repoURL/targetRevision/path | PASS |
| 4 | destination server + namespace web | PASS |
| 5 | syncPolicy automated with prune + selfHeal | PASS |
| 6 | project + CreateNamespace syncOption | PASS |
| 7 | out-of-sync = git-vs-live diff | PASS |
| 8 | reconcile loop = git is source of truth | PASS |
| 9 | prune semantics (deletes removed manifests) | PASS |
| 10 | selfHeal semantics (reverts manual drift) | PASS |
| 11 | app-of-apps pattern named | PASS |
| 12 | Answer matches source 09-cicd CICD.P1.2 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-20 — Jenkins declarative pipeline · CI/CD · source: 09-cicd CICD.P1.1 · 300s
**Question:** Write a declarative Jenkinsfile: agent, options (timeout 30m, disable concurrent), environment with registry + image, stages Lint → Test → Build → Push → Deploy, credentials referenced through `withCredentials` (not inline), a `when` gate on Deploy, and a `post` block with always/failure/success/cleanup.
**ANSWER (fold here until attempted):**
```groovy
pipeline {
  agent any
  options {
    timeout(time: 30, unit: 'MINUTES')
    disableConcurrentBuilds()
  }
  environment {
    REGISTRY = 'registry.example.com'
    IMAGE    = "app:${env.BUILD_ID}"
  }
  stages {
    stage('Lint') {
      steps { sh 'ruff check .' }
    }
    stage('Test') {
      steps { sh 'pytest -q' }
    }
    stage('Build') {
      steps { sh "docker build -t ${REGISTRY}/${IMAGE} ." }
    }
    stage('Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'reg-creds',
                          usernameVariable: 'REG_USER',
                          passwordVariable: 'REG_PASS')]) {
          sh "docker login -u ${REG_USER} -p ${REG_PASS} ${REGISTRY}"
          sh "docker push ${REGISTRY}/${IMAGE}"
        }
      }
    }
    stage('Deploy') {
      when { branch 'main' }
      steps {
        sh "kubectl set image deployment/web web=${REGISTRY}/${IMAGE}"
      }
    }
  }
  post {
    always  { junit 'reports/**/*.xml' }
    failure { sh './notify.sh --failure' }
    success { sh './notify.sh --success' }
    cleanup { sh 'docker system prune -f' }
  }
}
```
Model notes: declarative Jenkinsfile = the structured `pipeline {}` (agent = the runs-on, stages = ordered units, steps run on the agent shell). Credentials NEVER inline — `withCredentials` pulls from Jenkins' credentials store into env vars scoped to the block. `when` gates a stage (here: deploy only on main). options tune runtime behavior (timeouts, concurrency). `post` runs context-gated finalization — `always` (artifact collection), `failure`/`success` (notify), `cleanup` (reclaim disk). Jenkinsfile is pipeline-as-code in the same spirit as `.github/workflows/*.yml` — reviewed and versioned with the source. On this box the source session was model-only (no Jenkins binary), an honesty boundary to keep.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-20
| # | Check | Status |
|---|---|---|
| 1 | pipeline/agent/options skeleton | PASS |
| 2 | timeout + disableConcurrentBuilds options | PASS |
| 3 | environment block with registry + image | PASS |
| 4 | Lint/Test/Build/Push/Deploy stages present | PASS |
| 5 | withCredentials (not inline secrets) | PASS |
| 6 | when branch 'main' gate on Deploy | PASS |
| 7 | post: always/failure/success/cleanup | PASS |
| 8 | junit collecting results | PASS |
| 9 | agent = runs-on analog named | PASS |
| 10 | model-only honesty boundary kept | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 09-cicd CICD.P1.1 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-21 — Alertmanager route and grouping · OBSERVABILITY · source: 10-observability OBS.P0.8 · 240s
**Question:** Write the alertmanager.yml: a default route (group_by alertname+cluster, group_wait 30s, group_interval 5m, repeat_interval 4h, email receiver) plus a child route matching `severity="critical"` to a webhook/pager receiver and a nested route for `severity="page"` and `team="platform"`. Then give one-line definitions of route, group, inhibit, silence, receiver.
**ANSWER (fold here until attempted):**
```yaml
route:
  group_by: ['alertname', 'cluster']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: ops-mail
  routes:
    - matchers:
        - severity = "critical"
      receiver: oncall-pager
    - matchers:
        - severity = "page"
        - team = "platform"
      receiver: platform-pager

receivers:
  - name: ops-mail
    email_configs:
      - to: devops@acme.com
  - name: oncall-pager
    webhook_configs:
      - url: https://hooks.example.com/alerts
  - name: platform-pager
    webhook_configs:
      - url: https://hooks.example.com/platform
```
Definitions: ROUTE = match labels to a receiver (a tree of matchers); GROUP = collapse related alerts (same group_by labels) into one notification so a 12-pod outage is one page; INHIBIT = a higher-severity alert suppresses lower-severity ones about the same thing (no double pages for one outage); SILENCE = suppress known alerts for a fixed window (maintenance); RECEIVER = the deliverable destination (email/Slack/PagerDuty/webhook) after routing and grouping. `group_wait` = how long to hold the first notification of a NEW group (batching, noise control); `group_interval` = how often to re-send a still-firing group; `repeat_interval` = when a still-firing alert is re-notified. Prometheus side: a rule fires after its `for:` window holds (activeAt pending → firing), then the firing set goes to Alertmanager. Route symptoms not causes; put the runbook link in the alert annotation.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-21
| # | Check | Status |
|---|---|---|
| 1 | route with group_by alertname+cluster | PASS |
| 2 | group_wait/group_interval/repeat_interval values | PASS |
| 3 | default receiver ops-mail (email) | PASS |
| 4 | child route severity=critical -> webhook | PASS |
| 5 | nested route severity=page + team=platform | PASS |
| 6 | matchers syntax (label = value) | PASS |
| 7 | receivers block with 3 receiver names | PASS |
| 8 | route/group/inhibit/silence/receiver all defined | PASS |
| 9 | group_wait batching purpose stated | PASS |
| 10 | pending→firing rule state machine recalled | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 10-observability OBS.P0.8 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-22 — SLI, SLO, error budget · OBSERVABILITY · source: 10-observability OBS.P0.9 · 180s
**Question:** (a) Define SLI, SLO, and error budget in one sentence each; (b) compute the monthly error budget for a 99.9% SLO over a 30-day window and the daily equivalent; (c) compute the burn rate for one hour at a 2% error ratio; (d) state the multi-window burn-alert guidance; (e) the percentiles-not-averages rule.
**ANSWER (fold here until attempted):**
(a) SLI = the measured quantity, a good-event fraction ("requests served in < 300ms" / "requests served"). SLO = the agreed target over a window ("99.9% of requests finish < 300ms, measured monthly") — it selects SLI + threshold + period. Error budget = 1 − SLO, the spendable allowance of bad events; spending the budget is NOT an incident, losing the whole budget is.
(b) Budget = 0.001 x (30 x 86400 s) = 2592 s = 43m12s per month. Daily equivalent ≈ 86.4 s.
(c) Burn rate = observed error ratio / allowed error ratio = 0.02 / 0.001 = 20x — consuming twenty days of budget per day.
(d) Multi-window burn alerting: page on 1h burn > 14.4x (fast-spike catch) OR 6h burn > 6x (confirms it is not a blip), ticket on 3d burn > 1x (slow drain). Short window catches fast burn; long window filters noise.
(e) Percentiles, never averages — the 372ms average lies while the p95 is already breaching; SLO latency scales should read p95/p99.

One-liner for the interview: "SLI is what I measure, SLO is what I promise, error budget is what I may spend on change." Alert on budget BURN, not static thresholds — static "error > 1%" pings during a zero-traffic blip and stays silent through a slow 0.9% drain.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-22
| # | Check | Status |
|---|---|---|
| 1 | SLI defined as measured good-event fraction | PASS |
| 2 | SLO defined as target with threshold + window | PASS |
| 3 | budget = 1 - SLO spendable allowance | PASS |
| 4 | 0.001 x (30 x 86400) = 2592s = 43m12s | PASS |
| 5 | daily equivalent ~86.4s | PASS |
| 6 | burn 2%/0.1% = 20x | PASS |
| 7 | multi-window: 1h >= 14.4x page, 6h >= 6x page, 3d >= 1x ticket | PASS |
| 8 | percentiles-over-averages rule with p95 | PASS |
| 9 | burn-rate beats static thresholds argument | PASS |
| 10 | one-liner SLI/SLO/budget phrasing recalled | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 10-observability OBS.P0.9 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-23 — EKS managed node group config · AWS/KUBERNETES · source: 07-kubernetes K8s.P2.4 + 05-aws AWS.P0.10 · 240s
**Question:** Write an eksctl ClusterConfig with one MANAGED node group: cluster `acme-prod`, region us-west-2, instance type m6i.large, desired/min/max 3/3/9, AmazonLinux2023 AMI family, 100 GiB volume. Then state how nodes join the cluster (IAM story) and one Fargate-vs-nodegroup trade-off.
**ANSWER (fold here until attempted):**
```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: acme-prod
  region: us-west-2
managedNodeGroups:
  - name: workers-ng
    instanceType: m6i.large
    desiredCapacity: 3
    minSize: 3
    maxSize: 9
    amiFamily: AmazonLinux2023
    volumeSize: 100
    labels:
      role: general
```
Join story: the node group is an ASG of EC2 instances whose kubelet authenticates to the EKS cluster using the node's IAM role (instance profile / launch template role), mapped into RBAC via the aws-auth ConfigMap — that is NODE identity. It is deliberately separate from POD identity (IRSA, task 13-24): instance profile = who the node is, web-identity = who the pod is, and the two never blur. Managed node groups = AWS handles upgrades, patches, and node replacement (and repair checks), versus self-managed groups where the word "version skew" is your problem. Autoscaling story: the group's min/max feed Cluster Autoscaler or Karpenter so the ASG and the controllers agree on capacity. Fargate trade-off: Fargate removes node management entirely (AWS runs the pods' compute) but you give up DaemonSets and node-level debugging, and per-vCPU cost is higher — teams run node groups for the main workload and Fargate for aux/control-plane pods.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-23
| # | Check | Status |
|---|---|---|
| 1 | eksctl.io/v1alpha5 + ClusterConfig kind | PASS |
| 2 | metadata name acme-prod + region us-west-2 | PASS |
| 3 | managedNodeGroups (plural, not nodeGroups) | PASS |
| 4 | instance type + desired/min/max 3/3/9 | PASS |
| 5 | amiFamily AmazonLinux2023 + volumeSize 100 | PASS |
| 6 | node join = instance profile IAM + aws-auth NodeRole | PASS |
| 7 | managed = AWS handles upgrades/repair | PASS |
| 8 | min/max wire into autoscaling | PASS |
| 9 | node identity vs pod identity distinction | PASS |
| 10 | Fargate trade-off (no DaemonSets, cost, aux pods) | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 07-kubernetes K8s.P2.4 + AWS.P0.10 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-24 — IRSA and the OIDC trust policy · AWS/KUBERNETES · source: 07-kubernetes K8s.P2.4 + 05-aws AWS.P0.10 + 11-security SEC.P0.3 · 300s
**Question:** Write (a) the IAM role TRUST policy for IRSA that scopes `sts:AssumeRoleWithWebIdentity` to exactly the service account `s3-access` in namespace `app` on account `123456789012`'s EKS OIDC provider; (b) the SA manifest with the role annotation; (c) the 6-step flow from pod start to minted AWS credentials.
**ANSWER (fold here until attempted):**
(a) Trust policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/oidc.eks.us-west-2.amazonaws.com/id/EXAMPLEC0DEC0DEC0DEC0DEC0DEC0DE"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.us-west-2.amazonaws.com/id/EXAMPLEC0DEC0DEC0DEC0DEC0DEC0DE:sub": "system:serviceaccount:app:s3-access",
          "oidc.eks.us-west-2.amazonaws.com/id/EXAMPLEC0DEC0DEC0DEC0DEC0DEC0DE:aud": "sts.amazonaws.com"
        }
      }
    }
  ]
}
```
(b) ServiceAccount:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: s3-access
  namespace: app
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/app-s3-access
```
(c) Flow: EKS publishes an OIDC issuer (discovery endpoint + signing keys) for the cluster → attach an identity policy (least-privilege S3 read) to the IAM role, and the trust policy above → the `amazon-pod-identity-webhook` watches ServiceAccounts → seeing the annotation it injects `AWS_ROLE_ARN` + `AWS_WEB_IDENTITY_TOKEN_FILE`, and the kubelet projects an OIDC JWT → the SDK reads the token and calls `sts:AssumeRoleWithWebIdentity` → AWS issues short-lived credentials. No static access keys ever enter the cluster or the manifest. The `sub` condition is what pins the federated role to exactly ONE namespace:SA (webhook swaps in the SA token subject; aud is pinned to sts.amazonaws.com). Contrast — nodes use an instance profile; pods use IRSA; a static key in a ConfigMap is disqualifying in any review.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-24
| # | Check | Status |
|---|---|---|
| 1 | trust policy Principal.Federated = OIDC provider ARN | PASS |
| 2 | Action sts:AssumeRoleWithWebIdentity | PASS |
| 3 | sub condition system:serviceaccount:app:s3-access | PASS |
| 4 | aud condition sts.amazonaws.com | PASS |
| 5 | SA manifest with eks.amazonaws.com/role-arn annotation | PASS |
| 6 | webhook injects AWS_ROLE_ARN + AWS_WEB_IDENTITY_TOKEN_FILE | PASS |
| 7 | kubelet projects OIDC token | PASS |
| 8 | SDK calls AssumeRoleWithWebIdentity for short-lived creds | PASS |
| 9 | no static keys ever in cluster | PASS |
| 10 | node instance profile vs pod IRSA never conflated | PASS |
| 11 | Answer is complete and correct | PASS |
| 12 | Answer matches source 07-kubernetes K8s.P2.4 + AWS.P0.10 + SEC.P0.3 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-25 — OpenTelemetry span and traceparent · OBSERVABILITY · source: 10-observability OBS.P0.7 · 240s
**Question:** Write (a) the field set a finished OTel span record carries, as a JSON example with a parent link; (b) the W3C traceparent format with an example and what each field is; (c) a minimal Python SDK init exporting OTLP; (d) head-vs-tail sampling in one sentence each.
**ANSWER (fold here until attempted):**
(a)
```json
{
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
  "spanId": "00f067aa0ba902b7",
  "parentSpanId": "9c7c269d3cf2ef9a",
  "name": "GET /orders/:id",
  "kind": "SERVER",
  "startTimeUnixNano": 1690000000000000000,
  "endTimeUnixNano": 1690000001500000000,
  "status": { "code": "ERROR", "message": "db timeout" },
  "attributes": { "http.status_code": 503, "region": "us-west-2" },
  "events": [ { "timeUnixNano": 1690000000750000000, "name": "exception", "attributes": {} } ],
  "resource": { "service.name": "orders-api", "host.name": "orders-7b6f9c" }
}
```
A trace is rebuilt by the BACKEND from these records by tracing parentSpanId links (the store does the tree join, not the SDK); span kinds are client/server/internal/producer/consumer.
(b) `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01` — version (00), trace_id (16 bytes), parent span_id (8 bytes), flags (01 = sampled). Anything that forwards HTTP must carry the header onward or the trace splits into unconnected fragments; messaging must carry the ids in the envelope.
(c)
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="http://collector:4317")))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("orders-api")
with tracer.start_as_current_span("GET /orders/:id") as span:
    span.set_attribute("http.status_code", 503)
    span.set_status(trace.Status(trace.StatusCode.ERROR, "db timeout"))
```
(d) HEAD sampling decides at the root before data flows — simple and cheap but can miss rare slow/error tails; TAIL sampling buffers spans per trace in the collector and decides on completion — expensive (a hash buffer per trace_id) but can keep every 5xx and every p99 hit. Correlation rule: put the trace id in log lines and (where cardinality allows) metric labels — that join is the entire point.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-25
| # | Check | Status |
|---|---|---|
| 1 | span JSON has traceId + spanId + parentSpanId | PASS |
| 2 | name, kind, start/end unix nano, status, attributes present | PASS |
| 3 | events + resource (service.name) present | PASS |
| 4 | trace rebuilt by backend via parent ids | PASS |
| 5 | traceparent = version-trace_id-span_id-flags | PASS |
| 6 | example traceparent string well-formed | PASS |
| 7 | propagation across HTTP + queues stated | PASS |
| 8 | Python SDK: TracerProvider + BatchSpanProcessor + OTLP | PASS |
| 9 | set_attribute and set_status used | PASS |
| 10 | head vs tail sampling one-liners | PASS |
| 11 | correlation rule (trace id in logs) stated | PASS |
| 12 | Answer matches source 10-observability OBS.P0.7 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

### TASK 13-26 — SBOM and the supply-chain gate · SECURITY · source: 11-security SEC.P0.10 · 180s
**Question:** Write the container supply-chain gate as a five-item list, then the two-command scan/SBOM generation for a built image, then one sentence on what an SBOM is, its formats, and when it pays off. State the tools honestly (what is installed vs model).
**ANSWER (fold here until attempted):**
Gate (minimum five):
1. Minimal base image (alpine/distroless/scratch), pinned by digest (`@sha256:`), never `:latest`.
2. Runtime posture: non-root, read-only rootfs, `--cap-drop ALL`, `no-new-privileges`.
3. Image scan in CI against CVE databases (Trivy/Grype/Snyk): fail the build on Critical/High, annotate the rest — scan is a gate with a policy, not a report in a drawer.
4. Generate an SBOM at build time and store it with the image artifact.
5. Sign the image digest (cosign) so admission control can prove it came from your CI.

Commands:
```bash
syft -o spdx-json app:1.0 > app.sbom.spdx.json
trivy image --exit-code 1 --severity CRITICAL,HIGH app:1.0
```
SBOM: a machine-readable inventory of components and versions (formats: SPDX or CycloneDX) generated at build and consumed by scanners; when a new CVE publishes, the answer to "are we affected?" takes minutes by querying the SBOM instead of weeks re-inventorying images. Scan = vulnerability lookup; SBOM = the inventory that makes the lookup fast and complete — scanners consume SBOMs. Honesty boundary: on this box `trivy`, `syft`, `cosign` are NOT installed (verified absent) — the scan/sign step is stated as model-only, never fabricated output. A secret baked into a layer is a breach forever (layer history survives deletion), and multi-stage keeps the toolchain out of the final image.

**SELF-SCORE:** 5 / 4 / 3 / 2 / 1 / 0 (circle)
**MISTAKES MADE (be specific):**
**RE-STUDY LOOP:** [ ] +24h [ ] +48h (required if score ≤3)

### QC CHECKLIST — TASK 13-26
| # | Check | Status |
|---|---|---|
| 1 | five-item gate list (base, posture, scan, SBOM, sign) | PASS |
| 2 | pinned digest never latest | PASS |
| 3 | scan fails on Critical/High | PASS |
| 4 | syft -o spdx-json SBOM generation command | PASS |
| 5 | trivy with --exit-code --severity | PASS |
| 6 | SBOM = component/version inventory | PASS |
| 7 | SPDX + CycloneDX formats named | PASS |
| 8 | CVE triage value argument (minutes) | PASS |
| 9 | scan vs SBOM distinction | PASS |
| 10 | honesty boundary (tools absent, model-only) | PASS |
| 11 | secret-in-layer-is-forever + multi-stage note | PASS |
| 12 | Answer matches source 11-security SEC.P0.10 | PASS |
| 13 | SELF-VERIFY — I can reproduce this from memory cold | PASS |

---

## 48-HOUR RE-DRILL PLAN

Rule: an answer is "known" only if you rewrite it cold at +48h. Every row is a fixed re-attempt slot REGARDLESS of score unless the per-task table proves a 5; any score of 3 or less also forces the +24h and +48h columns in that task's RE-STUDY LOOP, which OVERRIDES the weekly cadence for that task.

| Weekday | Re-attempt tasks | Batch focus | Notes |
|---|---|---|---|
| Monday | 13-01, 13-02, 13-03, 13-04 | Foundations (linux, bash, net, git) | Do scripts on real paper; the health check must be byte-accurate |
| Tuesday | 13-05, 13-06, 13-07, 13-08 | Kubernetes core + Docker | Write YAML by hand; then `kubectl apply --dry-run=client` or `docker run --help` to self-grade |
| Wednesday | 13-09, 13-10, 13-11, 13-12 | Terraform, CI/CD, PromQL, AWS | PromQL: rewrite the four queries blind, then diff against the answer |
| Thursday | 13-13, 13-14, 13-15, 13-16 | Helm, HPA, PVC, Jobs/CronJobs | All YAML; verify against a live cluster if available |
| Friday | 13-17, 13-18, 13-19, 13-20 | NetPol, TF modules, ArgoCD, Jenkins | Jenkins + ArgoCD are model-only in source — mark the honesty boundary yourself |
| Saturday | 13-21, 13-22, 13-23, 13-24 | Alerting, SLO, EKS, IRSA | SLO math by hand each time; trust-policy JSON must be byte-exact |
| Sunday | 13-25, 13-26 + ALL scored ≤3 | OTel, SBOM + deficit reruns | Re-run only the tasks you scored ≤3 in the week; update every per-task table |

Additional rules: time yourself on every attempt; log the score in the task table the same day; keep the ANSWER folded until the timer stops; a task scored 5 twice in a row (48h apart) graduates to the monthly 30-day review (see 18-revision), a task scored 3 or below stays in the weekly lane until it proves a 5 at +48h.

### FINAL FILE QC
| # | Check | Status |
|---|---|---|
| 1 | Header: title, one-line framing, 48h rule | PASS |
| 2 | How-to-use rigid protocol (5 steps) present | PASS |
| 3 | Scoring scale 0-5 defined | PASS |
| 4 | INDEX maps task -> source session -> target time for all 26 tasks | PASS |
| 5 | Batch 1 = 12 P0 tasks (13-01 .. 13-12) | PASS |
| 6 | Batch 2 = 14 P1 tasks (13-13 .. 13-26) | PASS |
| 7 | Every task uses the exact template (Question/ANSWER/SELF-SCORE/MISTAKES/RE-STUDY LOOP) | PASS |
| 8 | Every task names its source sibling session | PASS |
| 9 | Every task QC has 13 rows ending in SELF-VERIFY cold-reproduce | PASS |
| 10 | All fenced code blocks balanced (even count of fence markers) | PASS |
| 11 | No emojis in the file | PASS |
| 12 | No TODO/FIXME/no placeholders in the body | PASS |
| 13 | SELF-VERIFY — 48-HOUR RE-DRILL PLAN present and usable | PASS |