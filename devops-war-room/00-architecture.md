# 00 — ARCHITECTURE (approved blueprint)

Status: **APPROVED** (target: 1–3 YOE DevOps/Cloud/Platform/SRE/DevSecOps)

---

# 1. EXECUTIVE STRATEGY

The problem: at 1–3 YOE, interviews are won by **fundamentals depth + structured troubleshooting
reasoning + honest navigation of follow-ups**, increasingly in a live/narrated exercise. The War
Room is built around one loop, applied everywhere:

```
BUILD → VERIFY → BREAK → OBSERVE → HYPOTHESIZE → ISOLATE → FIX → VERIFY → PREVENT → EXPLAIN → DEFEND
```

Operating rules:

1. **P0 > P1 > P2.** Every topic carries a priority label. P0 gets full 16-part treatment; P1
   condensed; P2 a few lines. Nothing is "complete" until it passes QC.
2. **Time-protected.** Every major topic ends with `STOP HERE` and `DO NOT STUDY YET`.
3. **Failure-first.** Each topic teaches the mechanism AND the failure. No passive reading.
4. **Honesty enforced.** No fabricated experience, ever. Five claim levels: `USED / UNDERSTOOD /
   PRACTICED / OPERATED / DESIGNED` (mapped to L0–L4 in §16).
5. **One mental model, not 12 subjects.** The end-to-end spine
   (Git → CI → Docker → Registry → EKS → Ingress → ALB → Route 53) is reused across domains.

Timeline map (all hands-on):

| Time available | Coverage | Effort |
|---|---|---|
| 1–2 weeks | P0 answers + write-without-Google + 20 core drills + 1 mock | ~25–30h |
| 3–4 weeks | P0 + P1 core + attack chains + question bank + 3 mocks | ~40–50h |
| 5–8 weeks | Full system incl. labs, 30 incidents, 6 mocks, revision | ~90–120h |

---

# 2. TABLE OF CONTENTS

```
devops-war-room/
  README.md                       # navigation, learning order, how to use
  00-architecture.md              # this blueprint
  01-linux.md                    02-networking.md    03-git.md    04-bash.md
  05-aws.md                      06-docker.md        07-kubernetes.md  08-terraform.md
  09-cicd.md                     10-observability.md 11-security.md
  12-troubleshooting-playbook.md  # 30 cross-layer incidents
  13-write-without-google.md      # active-recall workbook (answers hidden)
  14-attack-chains.md             # drilling chains
  15-question-bank.md             # ~200 questions, ~60 full treatment
  16-resume-defense.md            # DEFEND WHAT YOU CLAIM
  17-mock-interviews.md           # 6 rounds + scoring
  18-revision.md                  # 7d / 14d / 30d / 1h / 15min
  labs/                           # runnable lab scaffolds per domain
```

Each domain file `01`–`11` follows the same skeleton:

```
1. What/why/mental model (drawable diagram)
2. P0 topics — full 16-part template
3. P1 topics — condensed 8-part treatment
4. P2 topics — definition + purpose + when encountered
5. Required troubleshooting scenarios (SYMPTOM→SCOPE→HYPOTHESES→CHECKS→EVIDENCE→
   ROOT CAUSE→FIX→VERIFY→PREVENT) with First-Check reasoning per incident
6. STOP HERE / DO NOT STUDY YET
7. QC result
```

---

# 3. PRIORITY MAP (research-validated, 2026)

See §7 for evidence. Strategic view:

| Domain | P0 | P1 | P2/borderline | Deliberately ignore |
|---|---|---|---|---|
| Linux | processes/states/signals, load, memory/swap/OOM, disk/inodes, perms/sudo, SSH, systemd/journald, env vars, FDs, sockets, /proc, resource troubleshooting | vmstat/iostat/dmesg, tar/rsync, umask, mounts, shell rc | LVM, swap tuning, cgroups-v2, NFS, ACLs | perf, SELinux/AppArmor crafting, kernel tuning, NUMA, init.d |
| Networking | OSI/TCP-IP model, CIDR, DNS+records+failures, TCP/UDP/ports/handshake, TLS basics, HTTP+status codes, NAT, SGs/firewalls, LB+reverse proxy, refused-vs-timeout-vs-TLS-vs-4xx/5xx, curl/nc/ss/dig | tcpdump, ARP, traceroute, MTU, keepalive, HTTP/2 | TLS handshake internals, mTLS, VXLAN/CNI | BGP/OSPF, advanced routing, QUIC |
| Git | full core model, merge-vs-rebase, reset-vs-revert, fetch-vs-pull, conflicts, reflog recovery | bisect, worktrees, signed commits, submodules (what) | packfiles, filter-repo, hooks | LFS nuances, subtree debates |
| Bash | vars/args/cond/loops/functions, exit codes, pipes/redirection, set -euo pipefail, jq, curl patterns, health-check/log-parse | awk/sed field parsing, process substitution, trap, arrays, find/xargs | bash internals, param expansion | sed-as-language, awk beyond extraction |
| AWS | VPC/subnets/routes/IGW/NAT, SG vs NACL, IAM (roles/policies/trust/STS/least-priv), EC2+EBS+AMI+lifecycle, S3 core, ALB+target groups+health, Route53, CloudWatch, ECR, EKS fundamentals, regions/AZ/HA, CLI | ASG, RDS basics, SSM/Secrets Mgr, S3 versioning/lifecycle, CloudTrail | Lambda, CloudFront, API GW, ECS, KMS, VPC endpoints | multi-account orgs, Control Tower, 200 services, IAM eval-chain minutiae |
| Docker | images/containers/layers, entire Dockerfile, build context, .dockerignore, volumes vs bind, networks, port mapping, registries, Compose, multi-stage, non-root, limits, logs + write-from-memory | caching order, optimization, HEALTHCHECK, network drivers, scanning | BuildKit advanced, containerd | Swarm, --squash, dev-containers |
| K8s/EKS | control-plane, Pod/RS/Deployment, Service+endpoints, Ingress, CM/Secret, labels/namespaces, probes, requests/limits, rollouts/rollback, kubectl, RBAC/SA, networking model + full failure set | PV/PVC/SC, taints/tolerations, affinity, HPA, NetPol, Helm basics, Job/CronJob, DaemonSet, EKS node groups + IRSA | StatefulSet, PDB, priority classes, VPA | operators/CRDs, webhooks, service-mesh internals, autoscaler tuning |
| Terraform | providers/resources/data/vars/locals/outputs, plan/apply, state (why/remote/locking/import), deps, count-vs-for_each, modules, secrets, env separation, drift, partial-apply + failure set | dynamic blocks, conditionals, lifecycle, workspaces, terraform_remote_state, version constraints | JSON syntax, moved, terragrunt, policy-as-code, plan-in-CI | provider authoring, CDKTF, custom functions |
| CI/CD | CI vs CD, pipeline anatomy, triggers, caching, artifacts, GitHub Actions (events/jobs/steps/env/secrets/cache/OIDC), Docker→ECR→K8s, gating, rollback, deployment strategies, pipeline failures | Jenkins declarative basics, GitOps, ArgoCD (app-of-apps/sync/health), quality gates | reusable workflows, matrix, Argo Rollouts | Bamboo/TeamCity/Travis, Jenkins shared-libraries |
| Observability | three pillars, Prometheus (model/scrape/PromQL basics), Grafana basics, CloudWatch, alert hygiene, evidence-per-symptom, metric→log→trace | Loki, OTel basics, SLO/SLI, Alertmanager routing, histograms | exporters, advanced PromQL, tracing deep | Mimir/Thanos, APM products, cost-observability |
| Security | authN vs authZ vs net-access vs identity vs secrets, IAM least-priv, roles+trust+STS, OIDC (Actions→AWS), IRSA, RBAC, SGs, secrets (k8s/AWS/CI), TLS/HTTPS, non-root, Linux perms, secret-in-git cleanup, scanning | NetPol, pod security, SBOM, supply-chain, dependency scanning | Vault, cosign, Kyverno/OPA usage | zero-trust platforms, pentest tooling, CVE programs, OAuth deep |
| Prod. Troubleshooting | methodology + first-check reasoning + blast radius + evidence + 30 incidents | — | chaos tooling | SLO burn-alert design, on-call process design |

**Role-specific flags** (promote to P1 only if a target JD demands): Ansible/Chef config-management,
Azure/`az`, GitLab CI / Bitbucket Pipelines, Windows/PowerShell (market-discounted), Terraform
Cloud/OpenTofu, GitHub Actions reusables.

---

# 4. DEPENDENCY MAP

```
Layer 1 Foundation      Linux ◄──► Bash        Networking ◄──► Git
                           \                      /
                            ▼                    ▼
Layer 2 Cloud+Packaging   AWS core ◄──► Terraform │ Docker
                          (VPC/IAM/EC2/S3/ALB)    (packaging)
                                  │          │
                                  ▼          ▼
Layer 3 Orchestration+Delivery   K8s / EKS ◄──► CI/CD ──► GitOps (ArgoCD)
                                  │
                                  ▼
Layer 4 Operate                  Observability (metrics → logs → traces)
                                  ▲
                    ┌─────────────┴─────────────┐
                    │  Security = overlay on EVERY layer │
                    └─────────────┬─────────────┘
                                  ▼
Layer 5 Synthesize            Production Troubleshooting playbook
```

---

# 5. LEARNING ORDER

```
Phase 0  Foundation     Linux → Networking → Git + Bash        (interleaved)
Phase 1  Cloud          AWS core AND Terraform interlaced      [WARN] deviates from baseline
Phase 2  Containers     Docker (write from memory) → Kubernetes / EKS core
Phase 3  Delivery       CI/CD (GitHub Actions) → GitOps/ArgoCD → deployment strategies
Phase 4  Operate        Observability → Security hardening → 30-incident playbook
Phase 5  Defend         Attack chains → Question bank → Write-without-Google → Resume defense →
                        6 mocks → Revision
```

Why it deviates from the original baseline:
1. **Terraform pulled into the AWS phase** — its educational value (state/plan/apply/backend) is
   only concrete when provisioning real AWS resources.
2. **Delivery spine kept together**: Docker → K8s → CI/CD → GitOps are one story.
3. **Security is taught from lab #1** (IAM least-privilege + SGs inside AWS), not at the end.
4. **Observability concepts appear in Phase 0** as evidence-collection; consolidated in Phase 4.
5. **Troubleshooting is a daily drill**, never a final add-on.

---

# 6. WHAT TO DELIBERATELY IGNORE

| Topic | Why cut | Promotion rule |
|---|---|---|
| BGP/OSPF/advanced routing | neteng territory, never asked at 1–3 YOE | JD says network-heavy → one-page concept only |
| Service-mesh internals (Istio/Linkerd) | junior gets "what is it" at most | Know 2-sentence answer only |
| Operators/CRD authoring/admission webhooks | custom-controller scope, 4+ YOE | Skip |
| eBPF / Cilium internals | problem you don't have yet | Skip |
| Multi-account AWS orgs, Control Tower | senior platform scope | Never claim (see §16) |
| Terraform provider authoring, CDKTF | niche | Skip |
| Policy-as-code authoring (OPA/Kyverno/Sentinel) | guardrail scope; name it once, no labs | Name it in a security answer |
| Obscure CI platforms (Bamboo/TeamCity/Travis) | declining | Only if JD names them |
| Jenkins Groovy/shared-libraries | legacy depth; Jenkins stays P1 declarative | Only if target shop is Jenkins-heavy |
| Advanced PromQL / Mimir / Thanos / APM | exceeds level | Skip |
| Windows/PowerShell stack | salary data = bottom of market | Only if role is Windows-flavored |
| Deep distributed-systems theory | senior design territory | Know "etcd runs on Raft" — enough |
| Python/DSA curriculum | support language only, not a curriculum | Basic automation + boto3 at P2 |

---

# 7. RESEARCH METHODOLOGY

**Source hierarchy:** official docs → technical behavior/config/security; job postings + aggregated
JD frequency → relevance/expected depth; engineering blogs + postmortems → failure patterns;
community opinion → never presented as fact.

**Cross-check rule:** when sources disagree → name the disagreement and context, prefer authoritative
technical sources for behavior, state the difference, avoid false certainty. JD frequency is weighted
`frequency × technical importance × interview frequency × role relevance`.

**Initial research findings (2026, incorporated):**
- Table stakes at 1–3 YOE across JDs: Linux (critical), Git/PR (critical), CI/CD troubleshooting
  (critical), Bash (important), cloud fundamentals IAM/networking/compute/storage/LB (important),
  IaC fundamentals (important), Docker (important), monitoring/logging basics (important), secrets
  hygiene (important), basic networking troubleshooting (important). Kubernetes = "important in
  containerized orgs" = most orgs → P0 at fundamentals depth.
- JD frequency: CI/CD 67%, automation 58%, Kubernetes 56%, AWS 54%, Python 53%, Terraform ~50%.
  Highest tool-pair lift: Docker × Kubernetes (1.54). GitHub Actions overtook Jenkins.
- What separates candidates: (a) every claimed tool gets probed two levels deeper; (b) live/narrated
  troubleshooting rounds are normal — failing = going silent, not failing to solve; (c) GitOps
  (push vs pull, ArgoCD sync) is a 2026 filter question → P1; (d) Terraform *state* is what's tested.
- Market warning: 0–2 YOE postings ≈ 8% of DevOps market. Differentiator = fundamentals depth +
  evidenced troubleshooting + narration under a live test.

---

# 8. SIZE & ENVIRONMENT

- Target ~80–100k words across the file set, ~55–65 incremental generation sessions (one sub-topic
  per session, per §41 of the original brief).
- Local env (probed): docker (Docker Desktop/WSL), git, jq, helm, python3, node present. RAM 3.7 GB,
  8 cores. Missing: kubectl, kind/minikube, terraform, aws CLI (installed in later phases).
  K8s labs on a small kind cluster if RAM allows, else budgeted EKS drills on the AWS account
  (config present in `~/.aws`).

---

# 9. QUALITY-CONTROL METHODOLOGY

- **Per-sub-topic gate (13 checks):** draw the model / ≤30 s definition / why / mechanism /
  dependencies / essential commands / reproduce / break / observe+interpret / symptom→root-cause /
  first-check-with-why / follow-ups / honest resume defense. **Any NO = topic stays incomplete.**
- Every generated section ends with a printed QC checklist + pass/fail + REVISE note if needed.
- Mock scoring: 7 axes ×/10 (technical, reasoning, communication, depth, follow-up defense, production
  judgment, uncertainty handling) → compact `MUST FIX / SHOULD FIX / NICE TO HAVE`.
- Self-test rule: "can I write this config from memory 48h after the session?" is the real gate.

---

# 10. ARCHITECTURE DECISIONS & CORRECTIONS

1. **GitHub Actions is the P0 CI tool, not Jenkins** (2026 adoption data). Jenkins = P1, legacy shops.
2. **Terraform pulled forward into the AWS phase** — state/backend concepts need real AWS resources.
3. **Question bank ~200 questions, ~60 with full treatment** — rest derive from attack chains.
4. **30 incidents grouped into 4 archetypes** (reachability / identity-authorization /
   orchestration-state / delivery) to train pattern recognition, not memorized fixes.
5. **Python = P2 support skill only**, not a curriculum.
6. **Config-management tools (Ansible/Chef) flagged role-specific** — absent from the 12 domains.
7. **Write-without-Google is a separate workbook** with hidden answers, for active recall only.
8. **Claim-depth targets per domain** (L0–L4 = USED/UNDERSTOOD/PRACTICED/OPERATED/DESIGNED).
   Example: Terraform target OPERATED; Kubernetes DESIGNED is capped to senior. If unprovable →
   reduce the claim, learn it, or remove it.
9. **Mocks simulate live/narrated debugging** — narration + method scored, not just solving.
10. **Full 16-part template only for P0**; P1 condensed; P2 one-liners (authorized by the brief §36).
11. **Every generated section reports its QC verdict** before being marked complete.
12. **The market reality is encoded in the design:** depth + evidence + narration are the
    differentiator at 1–3 YOE.

---

*Approval recorded: user approved architecture + directory storage, then chose "Approve — start with
Linux". Generation now proceeds one sub-topic at a time.*