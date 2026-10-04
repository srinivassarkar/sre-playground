# DEVOPS INTERVIEW WAR ROOM — 1–3 YOE

Primary preparation system for **DevOps / Cloud / Platform / Junior SRE / DevSecOps** interviews at
1–3 years of professional experience.

Approved architecture: see `00-architecture.md` (strategy, priorities, learning order, QC rules).

## How to use this system

1. Read `00-architecture.md` first. It is the governing blueprint.
2. Work the domain files in learning-order (architecture §5): Linux → Networking → Git+Bash →
   AWS+Terraform → Docker → K8s/EKS → CI/CD → Observability → Troubleshooting, with Security as
   an overlay and Production Troubleshooting as the integrating layer.
3. Every session ends the same way: teach → break-it lab → observe → troubleshoot → interview
   answer → follow-ups → QC verdict.
4. Active recall happens in `13-write-without-google.md` and `14-attack-chains.md`. No passive reading.
5. Resume claims must clear `16-resume-defense.md`. **Never fabricate experience** — the five claim
   levels (`USED / UNDERSTOOD / PRACTICED / OPERATED / DESIGNED`) govern what you may claim.
6. Mock interviews live in `17-mock-interviews.md`; scoring rubric is in architecture §28.
7. Final revision plans are in `18-revision.md`.

## File map

| File | Purpose |
|---|---|
| `00-architecture.md` | Strategy, TOC, priority map, dependency map, learning order, QC methodology |
| `01-linux.md` | Processes, CPU/load, memory/OOM, disk/inodes, permissions, systemd, sockets, troubleshooting |
| `02-networking.md` | TCP-IP/OSI model, DNS, CIDR, HTTP/TLS, refused-vs-timeout, tools, failure triage |
| `03-git.md` | Core model, merge/rebase, reset/revert, conflict + recovery |
| `04-bash.md` | Scripting essentials, `set -euo pipefail`, jq, health checks, log parsing |
| `05-aws.md` | VPC, IAM, EC2/EBS, S3, ALB, Route53, CloudWatch, ECR, EKS fundamentals + AWS troubleshooting |
| `06-docker.md` | Images/layers, Dockerfile from memory, volumes/networks, Compose, multi-stage, troubleshooting |
| `07-kubernetes.md` | Control plane, core objects, probes, scheduling, RBAC, networking, full failure set |
| `08-terraform.md` | plan/apply/state/backends/modules/count-vs-for_each, drift, partial apply, failure set |
| `09-cicd.md` | Pipeline anatomy, GitHub Actions (P0), Jenkins (P1), GitOps/ArgoCD, deployment strategies |
| `10-observability.md` | Metrics/logs/traces, Prometheus, Grafana, CloudWatch, alerting, evidence collection |
| `11-security.md` | authN vs authZ vs net-access vs identity vs secrets, IAM/OIDC/IRSA/RBAC, container security |
| `12-troubleshooting-playbook.md` | 30 cross-layer incidents in 4 archetypes |
| `13-write-without-google.md` | Active-recall workbook (answers hidden) |
| `14-attack-chains.md` | Interviewer drilling chains |
| `15-question-bank.md` | ~200 questions, ~60 with full treatment |
| `16-resume-defense.md` | DEFEND WHAT YOU CLAIM |
| `17-mock-interviews.md` | 6 rounds + 7-axis scoring |
| `18-revision.md` | 7/14/30-day + 1h + 15-min spaced-repetition plans |
| `19-memory-aids.md` | Mnemonic deck, memory palace, compression ladder |
| `20-final-review-and-campaign.md` | 21-day taper + final-24h + day-of ritual |
| `labs/` | Runnable lab scaffolds, one subdir per domain |

## Learning order (phases)

```
P0  Foundation      Linux → Networking → Git + Bash            (interleaved)
P1  Cloud           AWS core AND Terraform interlaced          (changed from baseline, see architecture §5)
P2  Containers      Docker → Kubernetes / EKS
P3  Delivery        CI/CD (GitHub Actions) → GitOps → deployment strategies
P4  Operate         Observability → Security hardening → 30-incident playbook
P5  Defend          Attack chains → Question bank → Write-without-Google → Resume defense → 6 mocks → Revision
```

## Lab environment (probed 2026-09-13)

- **Present:** docker (Docker Desktop/WSL), git, jq, helm, python3, node · RAM 3.7 GB · 8 cores
- **To install in later phases:** kubectl, kind (or minikube), terraform, aws CLI
- Linux + Docker labs run fully local. K8s labs will use a small `kind` cluster if it fits in RAM,
  otherwise budgeted EKS drills on the AWS account (config present in `~/.aws`).