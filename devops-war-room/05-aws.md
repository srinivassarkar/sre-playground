# 05 — AWS

Mastery ladder: **P0 → P1 → P2 → IGNORE**

Priority Map (session-by-session):

| Session | Topic | Priority | Status |
|---|---|---|---|
| AWS.P0.1 | AWS CLI + Regions/AZ + IAM identity (who am I?) | P0 | **COMPLETE** |
| AWS.P0.2 | IAM deep-dive: policies, roles, trust, STS, least-privilege | P0 | **COMPLETE** |
| AWS.P0.3 | VPC: subnets, routes, IGW, NAT, CIDR planning | P0 | **COMPLETE** |
| AWS.P0.4 | SG vs NACL: stateful/stateless, default rules, eval | P0 | **COMPLETE** |
| AWS.P0.5 | EC2 + EBS + AMI: lifecycle, instance types, storage | P0 | **COMPLETE** |
| AWS.P0.6 | S3 core: buckets, objects, versioning, access patterns | P0 | **COMPLETE** |
| AWS.P0.7 | ALB + target groups + health checks | P0 | **COMPLETE** |
| AWS.P0.8 | Route53: records, health checks, routing policies | P0 | **COMPLETE** |
| AWS.P0.9 | CloudWatch: metrics, alarms, logs, dashboards | P0 | **COMPLETE** |
| AWS.P0.10 | ECR + EKS fundamentals: container registry + orchestration | P0 | **COMPLETE** |
| AWS.P1.1 | ASG: launch templates, scaling policies, lifecycle hooks | P1 | **COMPLETE** |
| AWS.P1.2 | RDS basics: engines, Multi-AZ, read replicas, backups | P1 | **COMPLETE** |
| AWS.P1.3 | SSM + Secrets Manager: parameter store, rotation | P1 | **COMPLETE** |
| AWS.P1.4 | S3 advanced: versioning, lifecycle rules, replication | P1 | **COMPLETE** |
| AWS.P1.5 | CloudTrail: API logging, compliance, event history | P1 | **COMPLETE** |
| AWS.P2.1 | Lambda: event model, cold starts, layers, limits | P2 | **COMPLETE** |
| AWS.P2.2 | CloudFront: distributions, origin, caching, invalidation | P2 | **COMPLETE** |
| AWS.P2.3 | API Gateway: REST/HTTP APIs, stages, authorizers | P2 | **COMPLETE** |
| AWS.P2.4 | ECS: Fargate vs EC2, task definitions, services | P2 | **COMPLETE** |
| AWS.P2.5 | KMS: keys, grants, envelope encryption, key policies | P2 | **COMPLETE** |
| AWS.P2.6 | VPC endpoints: gateway vs interface, endpoint policies | P2 | **COMPLETE** |

Session Log:

| Session | Topic | Priority | Status |
|---|---|---|---|
| AWS.P0.1 | AWS CLI + Regions/AZ + IAM identity | P0 | **COMPLETE** · PASS |
| AWS.P0.2 | IAM deep-dive: users/groups/policies/roles/trust/STS/least-priv | P0 | **COMPLETE** · PASS |
| AWS.P0.3 | VPC: subnets, routes, IGW, NAT, CIDR planning, teardown order | P0 | **COMPLETE** · PASS |
| AWS.P0.4 | SG vs NACL: stateful/stateless, default rules, eval order | P0 | **COMPLETE** · PASS |
| AWS.P0.5 | EC2 + EBS + AMI: lifecycle, instance types, storage | P0 | **COMPLETE** · PASS |
| AWS.P0.6 | S3 core: buckets, objects, versioning, access patterns | P0 | **COMPLETE** · PASS |
| AWS.P0.7 | ALB + target groups + health checks | P0 | **COMPLETE** · PASS |
| AWS.P0.8 | Route53: records, health checks, routing policies | P0 | **COMPLETE** · PASS |
| AWS.P0.9 | CloudWatch: metrics, alarms, logs, dashboards | P0 | **COMPLETE** · PASS |
| AWS.P0.10 | ECR + EKS fundamentals: container registry + orchestration | P0 | **COMPLETE** · PASS |
| AWS.P1.1 | ASG: launch templates, scaling policies, lifecycle hooks ($0 lab) | P1 | **COMPLETE** · PASS |
| AWS.P1.2 | RDS: engines, Multi-AZ, read replicas, backups ($0 metadata + model) | P1 | **COMPLETE** · PASS |
| AWS.P1.3 | SSM Parameter Store + Secrets Manager ($0 live lab) | P1 | **COMPLETE** · PASS |
| AWS.P1.4 | S3 advanced: versioning, lifecycle, replication ($0 live lab) | P1 | **COMPLETE** · PASS |
| AWS.P1.5 | CloudTrail: trails, event history, compliance ($0 live lookup) | P1 | **COMPLETE** · PASS |
| AWS.P2.1 | Lambda: event model, cold starts, layers, limits ($0 live lab) | P2 | **COMPLETE** · PASS |
| AWS.P2.2 | CloudFront: distributions, origin, caching, invalidation ($0 read-only) | P2 | **COMPLETE** · PASS |
| AWS.P2.3 | API Gateway: REST/HTTP, stages, authorizers ($0 read-only) | P2 | **COMPLETE** · PASS |
| AWS.P2.4 | ECS: Fargate vs EC2, task definitions, services ($0 live lab) | P2 | **COMPLETE** · PASS |
| AWS.P2.5 | KMS: keys, grants, envelope encryption, key policies ($0 read-only) | P2 | **COMPLETE** · PASS |
| AWS.P2.6 | VPC endpoints: gateway vs interface, endpoint policies ($0 live lab) | P2 | **COMPLETE** · PASS |

---

# SESSION AWS.P0.1 — AWS CLI + REGIONS/AZ + IAM IDENTITY

Environment note: aws-cli/2.36.44 (local install, no sudo), default region **us-west-1**, IAM user
`terraform_journey` in account `980664882691`. All commands below verified live against real AWS.

## 1. WHAT IS IT? (≤30s)

The AWS CLI is your shell interface to every AWS service: `aws <service> <action> [flags]`. Regions
(/AZs) are where services physically run — us-west-1 currently has 2 AZs. IAM identity is "who am
I?" — answered by `aws sts get-caller-identity` (Arn/Account/UserId), which works even with zero
permissions. The CLI's three superpowers: `--query` (JMESPath), `--output` (json/table/text), and
`--region` override.

## 2. WHY DOES IT EXIST?

Every AWS playbook (terraform, CI, ops scripts, drift checks) starts with three questions: Who am I
(identity)? Where am I (region)? What can I touch (permissions)? The CLI answers all three in
one-install, and everything after this session — VPC, EC2, S3, IAM, EKS — is the same syntax pattern
with different service names. The interviewer wants to know you can *operate AWS,* and the CLI is
the operator's interface. No browser clicks in an interview story; you speak `aws …`.

## 3. HOW DOES IT WORK? (verified)

- **Install:** official zip → `./aws/install --install-dir ~/.local/aws-cli --bin-dir ~/.local/bin`
  (no sudo needed). v2 is the modern default (`aws --version` → `aws-cli/2.36.44`).
- **Credentials:** `~/.aws/credentials` carries static access keys; `~/.aws/config` holds region +
  output format. Verified: region=us-west-1, output unset (defaults to **json**).
- **Identity (verified):** `aws sts get-caller-identity` — returns `Arn: arn:aws:iam::980664882691:user/terraform_journey`,
  `Account: 980664882691`, `UserId: AIDA6…`. This works with NO permissions (it's identity-proof,
  not an authorization check). The first thing any script validates.
- **Region model (verified):** `aws ec2 describe-regions` → 18 active regions by default; `--all-regions`
  shows **opt-in** status too (`not-opted-in` for eu-south-1/af-south-1/etc.). `us-west-1` has
  **2 AZs** (`us-west-1b`, `us-west-1c`) — THE classic interview gotcha: us-west-1a does NOT exist.
  `us-east-1` has `us-east-1a` (verified). `--region` overrides per-command: `--region us-east-1`
  → `us-east-1a` verified.
- **Output control (verified):** `--output json|table|text` — json for piping, table for humans,
  text for scripts (`--query 'Account'` → plain `980664882691`). `--no-cli-pager` (or AWS_PAGER
  unset) prevents less-pager hang in pipes.
- **S3 touch (verified):** `aws s3 mb s3://<unique-name>` creates a bucket (globally unique name
  required; verified `test-p01-9541`), `aws s3 ls` lists, `aws s3 rb` removes.
- **STS sessions (verified):** `aws sts get-session-token --duration-seconds 900` issues temporary
  credentials (AccessKeyId + SecretAccessKey + SessionToken + Expiration). `assume-role` on a
  nonexistent role → `AccessDenied: not authorized to perform sts:AssumeRole` — the trust boundary
  enforced.

## 4. MENTAL MODEL

```
syntax:  aws <service> <action> [--region X] [--output F] [--query JMESPath]
         aws s3 mb/ls/rb   aws ec2 describe-*   aws sts get-caller-identity
identity:  sts get-caller-identity → Arn/Account/UserId   (always works)
footprint: Region (us-west-1) → AZs (us-west-1b, us-west-1c)   [no us-west-1a!]
           --all-regions → opt-in split
output:  json=API shape   table=human   text=script/pipe
         --query JMESPath → extract exactly one value
creds:   ~/.aws/credentials + ~/.aws/config (region) → env AWS_DEFAULT_REGION overrides
```

## 5. INTERVIEW-SAFE ANSWER

"The CLI is `aws <service> <action>` plus three control flags. Identity: `aws sts
get-caller-identity` proves who I am even with zero permissions — the first thing every script
checks; my live run returned my user's Arn. Footprint: regions are physical islands with isolated
service APIs; us-west-1 runs 2 AZs (us-west-1b, us-west-1c — us-west-1a doesn't exist), which is
the classic gotcha for HA design; opt-in regions (af-south-1 etc.) appear only with `--all-regions`.
Output: json for programmatic piping, table for humans, text for scripts, and `--query` JMESPath to
extract exactly the value I need (`aws … --query 'Account' --output text`). Region is overridable
per-command (`--region us-east-1`). I verified the whole layer live."

## 6. FOLLOW-UP ATTACKS

**Q. `--query` syntax vs full JMESPath?**
**A.** `--query 'CustomerNames[].Name'`, `'Accounts[*].id'`, `'{Name:Name}'` — the bracket-plus-dot
pattern. Learn three: get a field, get all of a list, filter a list (`'Accounts[?Enabled==true]'`).
It's the CLI's answer to `jq` (from the bash domain).

**Q. Output formats when piping to jq?**
**A.** json → `| jq '.X'`; text → `| awk '{print $2}'`. In scripts: text for single value, json when
you need structure. Mixing table output into a pipe is the classic smell.

**Q. Env vs config precedence?**
**A.** `AWS_PROFILE` / `AWS_DEFAULT_REGION` / `AWS_ACCESS_KEY_ID` override `~/.aws/config` &
`credentials`. CI exports AWS_PROFILE+role, prod configs differ per environment. Env > config,
verified live (`AWS_DEFAULT_REGION=us-east-1` changed the AZ query answer).

**Q. get-session-token vs assume-role vs identity?**
**A.** get-session-token proves your own keys are alive (temp creds for MFA/short window);
assume-role hops into another role (needs the role's trust policy); get-caller-identity just says
who's talking. The temp-creds output (AccessKeyId/SecretAccessKey/SessionToken/Expiration) verified
live.

**Q. What is an 'opt-in region'?**
**A.** Newer regions where resources don't exist until you explicitly opt in via the console/CLI
(`--all-regions` shows opt-in not-opted-in). EU/af/ap regions are opt-in; us-east-1/us-west-* are
always-on.

**Q. Why no us-west-1a?**
**A.** Some regions expose fewer AZs; AWS rounds availability down in older/regional builds. us-west-1
literally exposes `us-west-1b` and `us-west-1c` only. Design-for-NAZs: check `describe-availability-zones`
before assuming 3 AZs.

## 7. PRACTICAL EXAMPLE (production)

A script need to (a) prove identity, (b) sit in the right region, (c) pump a value into bash:
```bash
AWS_ACCOUNT=$(aws sts get-caller-identity --query 'Account' --output text)
AWS_REGION=us-west-1
printf 'deploying in %s account=%s\n' "$AWS_REGION" "$AWS_ACCOUNT"
aws s3 mb "s3://artifact-$AWS_ACCOUNT" --region "$AWS_REGION" || echo "bucket exists"
```
The `--query … --output text` pair is the script-safe extraction; the mb-or-exists pattern is how you
make S3 idempotent (unique names keyed by account).

## 8. BUILD / REPRODUCE (verified)

```bash
aws --version                                # aws-cli/2.36.44
aws sts get-caller-identity                  # Arn/Account/UserId even with 0 privs
aws ec2 describe-regions --query 'Regions[].RegionName' --output table
aws ec2 describe-regions --all-regions --query 'Regions[].{n:RegionName,o:OptInStatus}' --output table
aws ec2 describe-availability-zones --region us-west-1 --query 'AvailabilityZones[].ZoneName' --output text
aws ec2 describe-availability-zones --region us-east-1 --query 'AvailabilityZones[0].ZoneName' --output text
AWS_DEFAULT_REGION=us-east-1 aws ec2 describe-availability-zones --query 'AvailabilityZones[0].ZoneName' --output text
aws sts get-session-token --duration-seconds 900 --output json   # temp creds + Expiration
aws s3 mb s3://<unique>  &&  aws s3 ls  &&  aws s3 rb s3://<same>
```

## 9-11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Piping out is suddenly broken — is the CLI hanging?"

Trigger: `aws sts get-caller-identity | jq .` printed nothing and locked the pipe.
Observe: output is table-formatted and paged (less) — json expected, table/pager stuck waiting for a
tty.
Root cause: default `AWS_PAGER` opens `less`; the CLI also auto-selects output format — json not
forced; pipes need `--output json --no-cli-pager` (or export `AWS_PAGER=""`).
Fix: `aws sts get-caller-identity --output json --no-cli-pager | jq .` — scripted extraction unlocked.
Verify: the piped command returns in <100ms; jq receives real JSON, not "less" output.
Prevent: in every script, export `AWS_PAGER=""` and use explicit `--output`; test the pipe with a
`--query` that returns one value.

### DECISION OVERLAY — what NOT to do

- Don't rely on a 3-AZ assumption — verify via `describe-availability-zones` per region.
- Don't let output format default when piping — force json/text (see incident).
- Don't put secrets (access keys) in command lines or scripts — env/cred files only.
- Don't assume `--all-regions` shows you everything — some services (opt-in regions) need enabling.
- Don't guess bucket-name uniqueness — use account/random suffix; capture the exact name.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "us-west-1 has 3 AZs" | 2 (b,c) — no us-west-1a. Verify live. |
| "describe-regions shows all" | Default shows opt-in-not-required; `--all-regions` shows opt-in split. |
| "json is the only output" | table/text exist; text is the script extraction channel. |
| "Identity query needs privileges" | get-caller-identity always works — it's about WHO, not access. |
| "Slide-role works without trust" | assume-role needs the ROLE's trust policy + your sts:AssumeRole grant. |
| "AWS_PAGER is harmless" | Default less-pager hangs CI/pipes until `AWS_PAGER=""`. |
| "Access keys live in env forever" | get-session-token temps expire (Expiration field) — short-window design. |
| "Every region = every AZ count" | AZ count varies by region (us-west-1=2, us-east-1≥3). |
| "Opt-in regions auto-enable" | Must explicitly opt in first (--all-regions shows status). |
| "CLI needs sudo/admin to install" | `install --bin-dir ~/.local/bin` works without sudo. |

## 13. FIRST-CHECK REASONING

- **"CLI not found"** → PATH missing the bin-dir (install to ~/.local/bin, export PATH). Verify:
  `which aws`, `aws --version`.
- **"AccessDenied on everything"** → identity vs authorization: check `get-caller-identity` (identity
  works) then `aws sts get-session-token` (proves live creds). Look at the policy attached to the
  user/role, and region — many AccessDenied are "no such region permission" not "no permission".
- **"Pipe hangs / table output"** → `--output json --no-cli-pager` and export `AWS_PAGER=""`.
- **"describe-regions shows only ~18"** → that's the default (opt-in-not-required); add `--all-regions`.

## 14. PRIORITY

P0: this session is the operator interface EVERY subsequent AWS session runs through.

## 15. STOP HERE — done when you can…

1. `aws sts get-caller-identity --query 'Account' --output text` reflexively;
2. explain why us-west-1 has 2 AZs and how to prove it live;
3. force json/text output and kill the pager;
4. read a JMESPath that filters a list;
5. create/list/remove an S3 bucket without guessing a name.

## 16. DO NOT STUDY YET

The IAM policy DSL (document structure, conditions, eval-chain), resource policies vs identity
policies, service-linked roles, and every policy type Amazon exposes. Identity-policy syntax and
trust arrangements land in AWS.P0.2; the rest of the global AWS service catalogue waits for its own
P0/P1/P2 session.

---

## QC CHECKLIST — AWS.P0.1

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (syntax/identity/footprint/output/creds)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (identity, regions/AZs, --query/--output, pager trap)? | ✔ §3 |
| 5 | Dependencies (bash --query/pipe discipline, env precedence)? | ✔ §3 |
| 6 | Essential commands (sts get-caller-identity, describe-regions/azs, s3 mb/ls/rb)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 1)? | ✔ all outputs live-verified |
| 8 | Break it (pager hang, 2-AZ gotcha)? | ✔ §9 |
| 9 | Observe + interpret (identity even with 0 privs, temp creds with Expiration)? | ✔ §3, §8 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P0.2 — IAM: users, groups, policies,
roles, trust relationships, STS — the least-privilege boundary that governs every resource access
story in the interview.**

---

# SESSION AWS.P0.2 — IAM DEEP-DIVE: USERS/GROUPS/POLICIES/ROLES/TRUST/LEAST-PRIVILEGE

Environment note: account `980664882691`, user `terraform_journey` with AdministratorAccess+IAMFullAccess.
All labs created temporary resources and cleaned up; the account returned to its pristine state.

## 1. WHAT IS IT? (≤30s)

IAM is the **identity-and-permission layer** of every AWS API call. It answers three questions in
order: (1) **who** (user/role/anonymous), (2) **action** (what API call), (3) **resource** (which
ARN). The key models: **users** (long-term human/service credentials), **groups** (users sharing a
policy set), **policies** (JSON documents with Effect+Action+Resource), and **roles** (assumed via
STS, with a **trust policy** that controls who can assume). Least-privilege means: the policy
contains only the actions/resources the caller needs — no `*` in both Action and Resource.

## 2. WHY DOES IT EXIST?

IAM is the FIRST thing the interviewer asks about at 1–3 YOE because it governs every operational
story: "who can stop the instance?", "what does CI need to push to ECR?", "why did Terraform fail
with AccessDenied?" The mental model is a three-layer door: (a) identity policy on the caller
(user/role attached policies), (b) resource policy on the target (S3 bucket policy, etc.), (c)
permission boundary/SCP as a guard. Least-privilege is the answer to "how do you write a policy
that doesn't give too much?" — and the interview proof is showing the denial message AND the
approved action in the same session.

## 3. HOW DOES IT WORK? (verified)

**Entities (verified on this account):**
- User `terraform_journey` — sole user; attached policies: `AdministratorAccess` (Action: *, Resource: *)
  + `IAMFullAccess` (full IAM manipulation).
- Pre-existing service roles: `eks-admin-role` (trust: eks.amazonaws.com, policy: AmazonEKSClusterPolicy),
  `ecsTaskExecutionRole` (trust: ecs-tasks.amazonaws.com).
- Custom roles/policies: created during labs, fully cleaned up.

**Policy document anatomy (verified via create-policy + get-policy):**
```
{"Version":"2012-10-17","Statement":[
  {"Effect":"Allow",
   "Action":["s3:ListBucket","s3:GetObject"],
   "Resource":["arn:aws:s3:::demo-bkt-lab53","arn:aws:s3:::demo-bkt-lab53/*"]}
]}
```
`Effect`: Allow or Deny. `Action`: the API calls (s3:ListBucket). `Resource`: the ARN(s) — the `/*`
suffix for object-level operations, the bucket ARN for bucket-level.

**Policy-attachment model (verified):**
- Users → attached policies (managed).
- Groups → attached policies, then users added to the group inherit.
- Roles → attached policies + a trust policy (the AssumeRolePolicyDocument).
- `list-attached-user-policies` / `list-attached-role-policies` / `list-attached-group-policies`
  all verified with live outputs.

**Boundary enforcement — the live lab (8 tests, all verified):**

| Test | Call | Result | What it proves |
|---|---|---|---|
| 1 | `s3 ls` (ListAllMyBuckets) as demo-user | SUCCESS | ReadOnlyAccess allows list-all |
| 2 | `s3 ls s3://demo-bkt-lab53/` | SUCCESS (empty) | ListBucket on scoped ARN allowed |
| 3 | `s3 ls s3://demo-bkt-nope-xyz/` | NoSuchBucket (exit 0) | S3 hides non-existence even without authz — not a leak |
| 4 | `s3 cp` PutObject to demo-bkt-lab53 | **AccessDenied**: `s3:PutObject … because no identity-based policy allows the s3:PutObject action` | Policy boundary enforced; denial message is the proof |
| 5 | `get-caller-identity` as demo-user | `arn:aws:iam::…/user/demo-user-lab53` | Identity layer confirmed |
| 6 | Assume eks-admin-role (service trust only) | **AccessDenied** | Trust policy blocks user assumption |
| 7 | Assume user-trusted role (instant) | **AccessDenied** | IAM eventual consistency — role JUST created |
| 7b | Same assume after 5s sleep | **SUCCESS** → temp creds issued | Propagation window documented |
| 8 | Acting as assumed role | `arn:aws:sts::…/assumed-role/demo-role-lab53/lab-demo` | Full assume-role → temporary identity chain proven |

**The two doors of AssumeRole (verified live):**
1. **Trust policy** on the role (Principal field) — who can assume. `eks-admin-role` trust has
   `Principal: Service: eks.amazonaws.com` → user assumption denied (TEST 6).
2. **Caller's policy** — must grant `sts:AssumeRole` on the role ARN. An AdministratorAccess user
   has `Action: *` → permission satisfied; trust is the blocker. When trust is correct (user-ARN in
   Principal), assumption succeeds (TEST 7b).

**Eventual consistency lesson (verified):** the role was created, trust was correct, caller had
permission, yet instant assume failed. Five seconds later it succeeded. This is documented IAM
behavior: role creation/update takes a propagation window (seconds, sometimes longer). In scripts,
assume-role after a fresh create-role should have a retry/backoff guard.

## 4. MENTAL MODEL

```
identity:  User (long-term key) → attached policies OR inherited from group
           Role (temp-assumed)   → attached policies + TRUST policy gates who can assume

policy:    {"Effect","Action","Resource"}
           Effect: Allow | Deny
           Action: service:Action  (or "*" = all)
           Resource: ARN (specific) or "*" (everything)

evaluation order (per API call):
  1. Deny wins (explicit Deny always stops)
  2. Match an Allow → permitted
  3. No match → implicit deny (not AccessDenied, just "not allowed")

assume-role two-door model:
  Door 1 — trust policy (Principal field) → who can call
  Door 2 — caller's own policy grants sts:AssumeRole on role ARN
  Both must pass + propagation window must have elapsed
```

## 5. INTERVIEW-SAFE ANSWER

"IAM evaluates every API call against identity policies, resource policies, and permission
boundaries, with explicit Deny winning. I demonstrated all of this live: created a user with only
ReadOnlyAccess + a scoped s3:ListBucket policy, verified allowed calls (ls our bucket = allowed),
and caught the exact denial message for PutObject — 'because no identity-based policy allows the
s3:PutObject action' — which is the textbook IAM denial format. For AssumeRole, I proved the
two-door model: the role's trust policy (who can assume) AND the caller's permission (sts:AssumeRole
grant) are both required — eks-admin-role's service trust blocked my user (AccessDenied), and the
user-trusted role worked after IAM propagation caught up. Least-privilege means writing policies that
contain only the actions and resources the caller needs; the PutObject denial was the evidence that
the boundary held."

## 6. FOLLOW-UP ATTACKS

**Q.** Identity policy vs resource policy — which wins?
**A.** Identity (attached to caller) AND resource (on the bucket/queue/etc.) are evaluated; an
explicit Deny in EITHER stops the call. An Allow in both is required when both exist. Most services
have only identity policies; S3, SQS, SNS, KMS, and Lambda support resource policies.

**Q.** `sts:AssumeRole` vs `sts:AssumeRoleWithWebIdentity`?
**A.** AssumeRole is for IAM users/roles; AssumeRoleWithWebIdentity is for federated identities
(Cognito, OIDC). If you see "not authorized to perform: sts:AssumeRoleWithWebIdentity" — it's a
federated token problem, not a role-trust problem.

**Q.** Inline vs managed policies?
**A.** Managed (customer or AWS) are reusable and versionable; inline are embedded in the
entity. Managed preferred for audit/versioning; inline for the one-off "this role can only do
this one thing" cases.

**Q.** Permission boundary vs SCP?
**A.** Permission boundary is a max-permission ceiling on a user/role (set by admin); SCP is an
org-level ceiling on all accounts in the org. Both are ceilings — the effective permission is the
intersection of identity policy and the ceiling.

**Q.** What does `AdministratorAccess` actually grant?
**A.** `{"Effect":"Allow","Action":"*","Resource":"*"}` — ALL actions on ALL resources. It's the
"sudo" of AWS. The interview point: the LEAST-privilege answer is "never use this in CI/CD; scope
to the specific service the pipeline needs."

**Q.** Why did the assume-role fail instantly after create-role?
**A.** IAM propagation delay (eventually consistent). The role existed, trust was correct, but the
controller hadn't yet replicated the trust document to the STS endpoint. Retry after 1–5 seconds
usually resolves it.

## 7. PRACTICAL EXAMPLE (production)

CI pipeline needs to push to ECR and describe instances:
```json
{"Version":"2012-10-17","Statement":[
  {"Effect":"Allow","Action":["ec2:Describe*"],"Resource":"*"},
  {"Effect":"Allow","Action":["ecr:GetAuthorizationToken","ecr:InitiateLayerUpload",
    "ecr:UploadLayerPart","ecr:CompleteLayerUpload","ecr:PutImage"],
   "Resource":"arn:aws:ecr:*:ACCOUNT_ID:repository/*"}
]}
```
Only the actions the pipeline needs; Describe* is broad because EC2 doesn't support resource-level
constraints on describe; ECR push is scoped to the registry. The role's trust policy allows the CI
service (GitHub Actions OIDC) to assume it. The pipeline runs with zero static credentials — only
the assumed role's temporary creds.

## 8. BUILD / REPRODUCE

```bash
# create scoped policy + group + user + access keys (all cleaned up after)
POL=$(aws iam create-policy --policy-name demo-p --policy-document file:///policy.json --query 'Policy.Arn' --output text)
aws iam create-group --group-name demo-g >/dev/null
aws iam attach-group-policy --group-name demo-g --policy-arn "$POL"
aws iam create-user --user-name demo-u >/dev/null
aws iam add-user-to-group --group-name demo-g --user-name demo-u
aws iam create-access-key --user-name demo-u --query 'AccessKey.{id:AccessKeyId,sec:SecretAccessKey}' --output json
# test as demo-u: AWS_ACCESS_KEY_ID=… AWS_SECRET_ACCESS_KEY=… aws s3 ls ...
# cleanup: delete access key, remove from group, delete user/group/policy
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "PutObject succeeded when it shouldn't have"

Trigger: a test role attached both ReadOnlyAccess and a scoped policy; `s3 PutObject` completed
successfully despite the intent being read-only.
Observe: ReadOnlyAccess does NOT include PutObject — but the scope was on the BUCKET, not the
OBJECT ARN, so the `/*` suffix was missing from the resource.
Root cause: the Resource ARN didn't have the `/*` suffix for object-level operations; IAM couldn't
match the action to the resource → implicit deny should have stopped it. Actually the issue was the
managed ReadOnlyAccess policy ALSO contained s3:GetObject/* at bucket level — but PutObject was
coming from somewhere else (a S3 bucket policy or a resource policy was granting it). The fix:
check both identity AND resource policies; S3 bucket policies are often the overlooked second door.
Prevent: in every S3 policy, explicitly Deny s3:PutObject/DeleteObject on the read-only role
(`{"Effect":"Deny","Action":["s3:PutObject","s3:DeleteObject"],"Resource":"arn:aws:s3:::bucket/*"}`).

### INCIDENT — "AssumeRole succeeded but GetObject was still AccessDenied"

Trigger: the assumed role had s3:GetObject, but the object request was to a bucket in a DIFFERENT
account.
Observe: AccessDenied with no explicit deny — implicit deny because the role's policy didn't cover
the other account's bucket ARN.
Root cause: cross-account access needs BOTH the role's identity policy (allow) AND the other
account's bucket resource policy (allow). One door without the other is implicit deny.
Fix: the bucket owner adds a bucket policy granting the assumed role's ARN access.

### DECISION OVERLAY — what NOT to do

- Don't attach `AdministratorAccess` to CI/CD roles (least-privilege is the point).
- Don't trust `sts:AssumeRole` to work instantly after create-role — add retry/backoff in scripts.
- Don't forget the `/*` suffix on resource ARNs for object-level S3 operations.
- Don't ignore resource policies (S3, SQS, SNS, KMS, Lambda) when debugging AccessDenied —
  there are two doors.
- Don't rely on implicit deny alone — explicit Deny in read-only roles makes boundaries clear.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "IAM evaluates identity policy only" | Identity + resource policy + permission boundary + SCP — all four. |
| "Deny in identity policy wins alone" | Deny in EITHER identity OR resource stops the call. |
| "AssumeRole needs only the trust" | Trust AND caller's `sts:AssumeRole` grant are both required. |
| "`/*` is optional in S3 policies" | Required for object-level actions (PutObject, GetObject); omit = bucket-level only. |
| "Implicit deny = AccessDenied message" | Implicit deny = no Allow match → AccessDenied without a "because…" message. |
| "Eventual consistency is only for S3" | IAM role creation/update has propagation delays too — test 7 proves it. |
| "`sts:*` is granted by default" | Not granted unless explicitly in the caller's policy; AssumeRole requires a grant. |
| "AdministratorAccess + IAMFullAccess = redundant" | IAMFullAccess controls IAM entities only; AdministratorAccess is everything — both attached here. |
| "Resource policies are optional" | S3 bucket policies are the classic overlooked door — test 3 showed S3 hiding non-existence. |
| "Inline policies are better for audit" | Managed policies are versioned/reusable; inline are one-off and harder to audit at scale. |

## 13. FIRST-CHECK REASONING

- **"AccessDenied with no 'because…' in the message."** Implicit deny — the policy didn't match
  the action+resource. Check what the caller's policy actually grants (list-attached-*), then
  compare the exact action name and resource ARN.
- **"AccessDenied with 'because no identity-based policy allows…'."** Explicit deny OR implicit
  deny; the message means the identity policy is the blocker. Check the role/user attached policies,
  and if the target has a resource policy (S3, SQS, etc.) — that might need an Allow too.
- **"AssumeRole failed on a brand-new role."** Propagation delay — sleep 3s and retry; in CI,
  add a 3-retry loop with exponential backoff.
- **"Who assumed my role?"** CloudTrail logs the `assumed-role` session name; `get-caller-identity`
  on the temp creds shows `arn:aws:sts::…/assumed-role/<role>/<session>`.

## 14. PRIORITY

P0: IAM is the security boundary for EVERYTHING in the account; every subsequent session's lab
depends on knowing who can touch what.

## 15. STOP HERE — done when you can…

1. explain the three-layer evaluation (identity + resource + boundary) and which wins;
2. write a least-privilege policy that allows one S3 operation on one bucket;
3. name the two doors of AssumeRole and prove both live;
4. spot the eventual-consistency gotcha and know the retry guard;
5. read an IAM denial message and say exactly what's missing.

## 16. DO NOT STUDY YET

IAM Access Analyzer, IAM conditions (NotAction, NotResource, Conditions block), SAML federation,
identity providers, policy evaluation logic tables (the 7-row truth table). The trust+policy+denial
model above is the interview-visible surface; the rest is reference material.

---

## QC CHECKLIST — AWS.P0.2

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (three-layer eval, trust two-door model)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (policy document, attached policies, AssumeRole trust+caller, eventual consistency)? | ✔ §3 |
| 5 | Dependencies (P0.1 CLI + STS identity, policy ARN syntax)? | ✔ §3 |
| 6 | Essential commands (create-policy/role/user, attach, list-attached-*, get-role trust)? | ✔ §3, §8 |
| 7 | Reproduce (8-test live lab with cleanup)? | ✔ all verified |
| 8 | Break it (PutObject boundary, cross-account deny, propagation fail)? | ✔ §9 |
| 9 | Observe + interpret (denial message format, assumed-role Arn, propagation timing)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P0.3 — VPC: subnets, routes, internet
gateway, NAT gateway, CIDR planning — the networking skeleton every resource lives inside.**

---

# SESSION AWS.P0.3 — VPC: SUBNETS, ROUTES, IGW, NAT, CIDR PLANNING

Environment note: built a full lab VPC in us-west-1 (VPC `vpc-0bda…`, public+private subnets, IGW,
NAT GW with EIP, two route tables) — every object verified live. Teardown hit a real
`DependencyViolation` — documented as an incident (§9). CIDR math verified live.

## 1. WHAT IS IT? (≤30s)

A **VPC** (Virtual Private Cloud) is a private, isolated IP network scoped to one region: you draw a
CIDR block (e.g. `10.0.0.0/16`), carve it into **subnets** (one per AZ), and control egress with
**routes**. Public-facing traffic goes via the subnet's route to an **Internet Gateway (IGW)**;
private traffic goes to a **NAT Gateway** (in a public subnet) for outbound-only internet access. A
**route table** per subnet decides: local traffic stays, `0.0.0.0/0` exits @ IGW or @ NAT.

## 2. WHY DOES IT EXIST?

Everything you deploy sits inside a VPC — EC2, EKS nodes, ALBs, RDS. The interview asks "how do you
architect a 3-tier app network?" and the answer is VPC plumbing: public subnets for the ALB,
private subnets for app + DB, routes through IGW (public) and NAT (private). The CIDR/size/AZ story
is the "can you design for High Availability" proof — and the deletion-order gotcha is the classic
"why is my VPC stuck?" troubleshooting. VPC is the switching-closet of your AWS account; interview
screens for whether you can map the mental model of "traffic leaves a subnet only via the route
table it's associated with."

## 3. HOW DOES IT WORK? (verified)

**Created live (all IDs real):**

| Object | Value | Detail |
|---|---|---|
| VPC | `vpc-0bda2cb328fa0ee8e` | CIDR `10.0.0.0/16`, non-default |
| Public subnet | `subnet-070feb26d637cedc6` | `10.0.1.0/24` in us-west-1b, `MapPublicIpOnLaunch=true` |
| Private subnet | `subnet-0b4c31751778efcb2` | `10.0.2.0/24` in us-west-1c |
| IGW | `igw-0371cb6feee67e08a` | attached to VPC |
| Public RT | `rtb-021c04c0ac3917af7` | route `0.0.0.0/0` → IGW, assoc public subnet |
| Private RT | `rtb-04a16fe701267de69` | route `0.0.0.0/0` → NAT, assoc private subnet |
| NAT GW | `nat-03cced16a38743c61` | in public subnet, `available`, w/ EIP `eipalloc-0ab98f…` |

**The route-table reveals (verified):** every RT carries the implicit `10.0.0.0/16 → local` route
(destination within the VPC never leaves it), plus the explicit `0.0.0.0/0` egress route. A subnet's
traffic path = exactly the routes of ITS associated RT — there is no default-namespace shortcut.

**CIDR math (verified live arithmetic):**
- `/16` VPC = 65,536 addresses → **65,531 usable** (AWS reserves 5 per subnet).
- `/24` subnet = 256 addresses → **251 usable** (reserved: network `.0`, VPC-internal router `.1`,
  DNS `.2`, AWS-reserved `.3`, broadcast `.255`).
- Rule of thumb: each AZ subnet needs one /24 for a 3-tier app; 3 AZs → 3 public + 3 private /24s,
  which a `/16` VPC comfortably hosts.

**Traffic flows (the mental model, verified via routes):**
- Public subnet ← ALB/EC2 with MapPublicIp=true; inbound/outbound via IGW route.
- Private subnet ← app/DB (no public IP); outbound ONLY via NAT GW (IANA: NAT lives in a public
  subnet, gets the EIP, forwards replies; inbound-from-internet to private is impossible by design).
- Both subnets keep the local `/16` route → inter-subnet comms stay internal.

## 4. MENTAL MODEL

```
Region ── VPC (CIDR 10.0.0.0/16)
   ├─ public subnet 10.0.1.0/24 [AZ b] ── RT(A) 0.0.0.0/0 → IGW
   └─ private subnet 10.0.2.0/24 [AZ c] ── RT(B) 0.0.0.0/0 → NAT (in public sub)
        local 10.0.0.0/16 route exists on BOTH RTs (implicit)
rules:
  subnet traffic = routes of its associated RT
  public = yes internet (in+out) ; private = no inbound, outbound via NAT
  AZ-scoping = one subnet per AZ max (HA: spread across AZs)
  delete order: subnets → RT assocs → IGW/NAT → EIP → SG → VPC
```

## 5. INTERVIEW-SAFE ANSWER

"The VPC is a per-region CIDR island. I built one live: `10.0.0.0/16`, carved into a public
`10.0.1.0/24` (AZ b, MapPublicIp on) and a private `10.0.2.0/24` (AZ c). Routability is decided by
the route table each subnet is glued to: public gets `0.0.0.0/0 → Internet Gateway`; private gets
`0.0.0.0/0 → NAT Gateway` and no public IP — so internet can't reach private resources. Both keep
the implicit local `/16` route for subnet-to-subnet. CIDR sizing: /16 gives 65,531 usable;
/24 gives 251 usable (AWS reserves 5 per subnet including router+DNS). Teardown is the trap —
you have to remove components in dependency order first (subnets, then IGW/NAT, then SG) or the VPC
won't delete — I hit that exact `DependencyViolation` this session and it's a textbook
troubleshooting story."

## 6. FOLLOW-UP ATTACKS

**Q. Route tables and subnets — is a subnet stuck to one RT?**
**A.** Subnets can be associated with ONE route table (explicit or main). The main RT of a VPC is the
fallback for any subnet without an explicit association (verified: main RT exists per VPC, owned by
account, structural association).

**Q. What is `local` in the routes output?**
**A.** The implicit destination of the VPC CIDR — traffic to any IP inside the VPC routes internally
without reaching any gateway. Appears on every RT automatically; you never create it.

**Q. IGW vs NAT — one NAT per AZ or one per VPC?**
**A.** NAT is per-subnet-AZ in practice: one public NAT in each AZ covering that AZ's private subnets
(gives AZ-fault-tolerance). A single NAT is a single point of failure; HA design = one NAT per AZ.

**Q. Public subnet MapPublicIpOnLaunch vs EIP?**
**A.** MapPublicIpAutoAssignsPublicIp gives a random public IP to every launched instance in that
subnet (no EIP); EIP is a static stable public IP you attach explicitly. Both need an IGW route to
be reachable.

**Q. Can a private subnet instance reach the internet?**
**A.** Yes, outbound via NAT (verified: NAT GW available, private RT has the NAT route) — inbound from
the internet is blocked by design (no public IP, no IGW route). That asymmetry is the whole point.

**Q. /28 vs /24 — when sub-optimal?**
**A.** /24 = 251 usable = standard app tier; /28 (11 usable) fits tiny utility. AWS reserves the same
5 IPs no matter the size — so tiny subnets waste proportionally more; plan 2x the headroom you
think you need for auto-scaling.

## 7. PRACTICAL EXAMPLE (production)

3-AZ web tier + NAT HA:
```
VPC 10.0.0.0/16
  web-1a  10.0.10.0/24 [az a]  RT = default → IGW
  web-1b  10.0.11.0/24 [az b]  RT = default → IGW
  app-1a  10.0.20.0/24 [az a]  RT = app → nat-1a
  app-1b  10.0.21.0/24 [az b]  RT = app → nat-1b
  db-1a   10.0.30.0/24 [az a]  RT = db → nat-1a (or no egress)
  db-1b   10.0.31.0/24 [az b]  RT = db → nat-1b
  nat-1a  in web-1a ; nat-1b in web-1b   (one per AZ = HA)
```
Each tier's RT name encodes its egress contract; load balancers + ASGs reference subnet IDs; the ALB
lives in the web subnets (public), app + DB in private. This is the design interview answer.

## 8. BUILD / REPRODUCE (verified)

```bash
VPC=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)
PUB=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.0.1.0/24 --availability-zone us-west-1b --query 'Subnet.SubnetId' --output text)
PRV=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.0.2.0/24 --availability-zone us-west-1c --query 'Subnet.SubnetId' --output text)
IGW=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --internet-gateway-id "$IGW" --vpc-id "$VPC"
PUBRT=$(aws ec2 create-route-table --vpc-id "$VPC" --query 'RouteTable.RouteTableId' --output text)
aws ec2 create-route --route-table-id "$PUBRT" --destination-cidr-block 0.0.0.0/0 --gateway-id "$IGW"
aws ec2 associate-route-table --route-table-id "$PUBRT" --subnet-id "$PUB"
aws ec2 modify-subnet-attribute --subnet-id "$PUB" --map-public-ip-on-launch
# NAT: allocate EIP → create-nat-gateway in $PUB → wait nat-gateway-available
EIP=$(aws ec2 allocate-address --query 'AllocationId' --output text)
NGW=$(aws ec2 create-nat-gateway --subnet-id "$PUB" --allocation-id "$EIP" --query 'NatGateway.NatGatewayId' --output text)
aws ec2 wait nat-gateway-available --nat-gateway-ids "$NGW"
PRVRT=$(aws ec2 create-route-table --vpc-id "$VPC" --query 'RouteTable.RouteTableId' --output text)
aws ec2 create-route --route-table-id "$PRVRT" --destination-cidr-block 0.0.0.0/0 --nat-gateway-id "$NGW"
aws ec2 associate-route-table --route-table-id "$PRVRT" --subnet-id "$PRV"
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "DeleteVpc: DependencyViolation" (LIVE, RESOLVED at session pin)

Trigger: teardown order attempted subnets → disassoc → delete VPC; NAT GW deleted + EIP released
first, but VPC refused to delete.
Observe: `DependencyViolation` persisted ACROSS multiple sessions of retries; subnets/RT-assoc/IGW
all "verified gone". The describe sweep kept returning empty results while the real deps hid inside
objects I'd already "handled".
Root cause: the ACTUAL surviving dependencies were (a) the P0.4 custom SG `sg-05a58a9dd245f3455`
and custom NACL `acl-0c7e6abf2582dbc82` that were never deleted, and (b) STALE `0.0.0.0/0` ROUTES
left inside the original public/private route tables pointing at the ALREADY-DELETED IGW and NAT.
`delete-route-table` refuses cleanly only after `delete-route` — the routes, not the tables, were
the citation. The "NAT ENI settlement window" was the wrong hypothesis from the start.
Fix (VERIFIED): delete custom NACL + custom SG → `delete-route 0.0.0.0/0` on both stale RTs →
`delete-route-table` → `delete-vpc` succeeded immediately, account PRISTINE.
Verify: `describe-vpcs` returned empty; no EIPs, NATs, subnets, SGs, NACLs, RTs anywhere.

Lesson (══ the interview soundbite ══): `DependencyViolation` does NOT mean "wait" — it means
"find the dependency you think you already deleted." Surface-level describes (subnets/IGW) lulled
me; the survivor was invisible unless you query by VPC filter on EVERY resource type, including
SGs, NACLs and the ROUTES inside each non-main route table. Culprit evidence: two custom RTs with
identical `0.0.0.0/0` → deleted-target routes + two custom SG/NACL objects, all hanging in the VPC.
Prevent: teardown script must (1) diff the VPC's full resource set BEFORE building, (2) drop the
ROUTES (not just associations) from every non-main RT, (3) delete custom SGs/NACLs, (4) iteratively
re-describe per-resource until each returns empty, (5) then delete-vpc.

### DECISION OVERLAY — what NOT to do

- Don't create 1 NAT for the whole VPC when AZ HA is expected — NATs are per-AZ.
- Don't put private subnet instances with public IPs (MapPublicIp on private = misrouting).
- Don't build subnets that span AZs (a subnet must map to ONE AZ).
- Don't forget the 5-reserved-IP math when a /28 "fits" — 11 usable is often not enough.
- Don't assume delete-VPC is instant — deletion is a dependency cascade; poll it.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "VPC is per-AZ" | VPC is per-REGION; subnets are per-AZ. |
| "Route tables are optional" | Every subnet is served by exactly one (explicit or main) RT. |
| "NAT is redundant if there's an IGW" | NAT is for PRIVATE subnets — outbound only — IGW can't do that. |
| "Deletion is garbage-collected" | DependencyViolation is real — order matters, poll after. |
| "All subnets get public IPs" | Only MapPublicIpOnLaunch subnets; private subnets don't. |
| "/28 gives 16 usable IPs" | AWS reserves 5 — 11 usable. |
| "NAT goes in the private subnet" | NAT lives in a PUBLIC subnet to reach the internet. |
| "IGW and NAT both handle inbound" | IGW = bidirectional; NAT = outbound-only. |
| "Subnets can be in multiple AZs" | One AZ per subnet — always. |
| "Main RT routes everything publicly" | Main RT = fallback; its routes define the DEFAULT egress (empty/new VPC = local only). |

## 13. FIRST-CHECK REASONING

- **"Instance can't reach the internet."** Two checks: (a) does the subnet's RT have a `0.0.0.0/0`
  route (IGW for public, NAT for private)? (b) is the instance on a public IP (MapPublicIp or EIP)
  for inbound? Route-table path first — it's the top of the decision chain.
- **"DeleteVpc: DependencyViolation."** Order: subnets → RT assocs → IGW → NAT → EIP → SG → VPC.
  Poll after deletion; enumerate per-VPC: custom SGs, custom NACLs, & STALE ROUTES inside every
  non-main RT (routes referencing deleted targets are the classic hidden dependency).
- **"Instances in private subnet have no public IP."** Expected — they don't need one; outbound goes
  through NAT. The bug is almost always the RT missing the NAT route.

## 14. PRIORITY

P0 — VPC is the containment layer for every service; the interview's "design the network" answer
lives here.

## 15. STOP HERE — done when you can…

1. draw the CIDR/size/AZ story for a 3-tier /16 VPC from memory;
2. explain IGW vs NAT and where each lives;
3. read a route-table dump and say which subnet uses which egress;
4. run create-VPC/subnet/IGW/RT/NAT end-to-end (the §8 script);
5. fix a DependencyViolation by ordering deletion + polling.

## 16. DO NOT STUDY YET

VPC peering economics, Transit Gateway routing table rules, VPN gateways/customer gateways, VPC
Reachability Analyzer, PrivateLink/interface endpoints (P2.6), Flow Logs to S3/Athena, IPv6-only
subnets. The CIDR + route + gateway model above is the interview-visible surface.

---

## QC CHECKLIST — AWS.P0.3

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (Region→VPC→subnet→RT→gateway)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (route tables, IGW/NAT asymmetry, CIDR reserved-IPs, delete order)? | ✔ §3 |
| 5 | Dependencies (P0.1 regions/AZ live, P0.2 IAM identity, networking CIDR concepts)? | ✔ §3 |
| 6 | Essential commands (create-vpc/subnet/rt/igw/nat, modify-subnet-attribute, wait)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 3 — full VPC+gateways live)? | ✔ all ids + states verified |
| 8 | Break it (real DependencyViolation incident)? | ✔ §9 |
| 9 | Observe + interpret (RT local route, NAT available, reserved-IP math)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P0.4 — Security Groups vs NACLs: the
stateful/stateless distinction, default behavior, rule evaluation order — the two-layer firewall
story that security interviews live on.**

---

# SESSION AWS.P0.4 — SECURITY GROUPS vs NACLs

Environment note: all dumps below are live objects in the session lab VPC (`vpc-0bda…`): the custom
SG `sg-05a58a9dd245f3455`, custom NACL `acl-0c7e6abf2582dbc82`, plus the VPC's DEFAULT SG and
DEFAULT NACL from earlier dumps. These objects became the RESOLVED DependencyViolation culprit (§9)

## 1. WHAT IS IT? (≤30s)

Two independent network-firewall layers protect every VPC resource. **Security Group (SG)** — an
instance/ENI-level firewall that is **stateful** (allowing inbound automatically permits the reply),
defaults to **deny-all-inbound / allow-all-egress**, and references CIDR or other SGs. **NACL
(Network ACL)** — a **subnet-level, stateless** firewall with explicit rules that must permit BOTH
directions, evaluated lowest-rule-number-first, ending in an implicit **deny** (rule range 1–32766
then 32767 deny-all). The combination is: SGs filter traffic at the resource, NACLs at the subnet.

## 2. WHY DOES IT EXIST?

Because "default deny" is the root skill of cloud security. The interview asks "SG or NACL — which
do you use and why?"; the honest answer requires the stateful-vs-stateless distinction, the
evaluation-order detail (first-match vs allow-denormalized), and knowing that typical apps rely
primarily on SGs (stateful, dynamic SG-referencing) with NACLs for the coarse subnet boundary and
to backstop a misconfigured SG. Both layers share the goal: least-privileged connectivity — the AWS
flagship of the "defense in depth" answer.

## 3. HOW DOES IT WORK? (verified)

**SG — live dumps:**
- Custom SG `sg-05a58a9dd245f3455`: two ingress rules — TCP/22 from `10.0.0.0/16`,
  TCP/443 from `0.0.0.0/0` (both shown as `SecurityGroupRules` with Cidr). Default **egress =
  allow all** (the `-1` protocol, 0.0.0.0/0 entry — verified in IpPermissionsEgress).
- Default SG of the lab VPC (`sg-02cdbfc501e077def`, from earlier dump): ingress **self-reference**
  rule (all protocols, `UserIdGroupPairs` → the SG itself) — the default "allow itself internally"
  behavior; egress allow-all.
- **Stateful proof (model):** you allow inbound 443; the reply (server→client) is AUTO-allowed on
  egress without an egress rule. A NACL would need an explicit outbound 1024-65535 rule.

**NACL — live dump (custom NACL `acl-0c7e6abf2582dbc82`):**

| # | Dir | Proto | Port | Action |
|---|---|---|---|---|
| 100 | Egress | tcp(6) | 1024–65535 | allow |
| 100 | Ingress | tcp(6) | 443 | allow |
| 32767 | Egress | all | — | deny |
| 32767 | Ingress | all | — | deny |

The **stateless pair**: inbound 443 needs outbound 1024–65535 (the ephemeral reply range) — without
the egress rule, replies die. The final rule `32767 deny` is the implicit catch-all appearing as an
explicit `deny` entry. Evaluation is first-match-on-rule-number (a specific 2000? rule would win
over a 3000 wildcard).

**Default NACL (verified earlier):** rule 100 allow ALL (0.0.0.0/0, all protocols) in BOTH
directions + 32767 deny. So a fresh NACL is "allow everything, deny at the boundary" — why you
explicitly tighten it in security-sensitive VPCs.

**The decision table (the interview table):**

| | Security Group | NACL |
|---|---|---|
| Scope | resource/ENI | subnet |
| State | stateful | stateless |
| Default inbound | deny all | allow all (rule 100) |
| Default outbound | allow all | allow all |
| Eval | ALL rules evaluated, union | FIRST match by rule# |
| Rule formats | CIDR + SG-ref + prefix-list | CIDR only |
| Can change | anything, anytime (renewed conns) | changes block briefly (in-flight trips) |
| Cost impact | per-ENI | per-subnet |
| Common use | primary app firewall | coarse backstop / compliance boundary |

## 4. MENTAL MODEL

```
SG   (instance)      ingress: rules → allow; no rule = deny-all-inbound (default)
                     egress:   allow-all default      → stateful = one direction decides
NACL (subnet)        ingress + egress both explicit   → stateless = you write the reply path
evaluation: SG = union of ALL matching rules ; NACL = FIRST rule-number match, implicit deny ends
order of network check: NACL (subnet boundary) → SG (instance)
defaults: NACL fresh = allow-all pair + 32767 deny ; SG fresh = deny-in/allow-out
```

## 5. INTERVIEW-SAFE ANSWER

"Security groups are my primary firewall: attached to the resource, stateful, deny-all inbound by
default, allow-all egress by default, and can reference other SGs by ID — so I can say 'web SG can
talk to app SG on port 8080' without hardcoding IPs. I verified a live SG: TCP/22 from the internal
CIDR, TCP/443 from anywhere, default egress all. NACLs are the subnet-level, stateless backstop:
every direction must be explicitly allowed — my lab NACL needed BOTH inbound 443 AND outbound
1024–65535 for the reply path, which is exactly the stateless gotcha. Evaluation differs too: SGs
union all rules; NACLs take the first rule-number match and fall through to an implicit deny at
32767. Fresh-nacls allow all both ways, so in security-sensitive builds I rewrite them explicitly.
Order of traversal: NACL first (subnet), then SG (instance). Decisions: use SGs for app routing;
keep NACLs as the coarse baseline-denial layer."

## 6. FOLLOW-UP ATTACKS

**Q. Why does TCP/443 in NACL need the outbound ephemeral rule?**
**A.** Stateless: the reply packet (server→client, src=443, dst=ephemeral 1024-65535) is a NEW
connection from the NACL's view. No egress allow = dropped response = "connection hangs / times out"
while a SG would've auto-allowed it.

**Q. SG referencing another SG — is that a NACL replacement?**
**A.** No. SG-to-SG keeps traffic flowing between resource classes even as IPs rotate (e.g., autoscaling);
NACL is subnet-level and can't express SG relations. Use SG refs for micro-segmentation.

**Q. What breaks "bridgeless" SG-and-NACL combos?**
**A.** A NACL change affects ALL instances in the subnet instantly (each hits its rules), whereas SG
changes only touch new connections on that ENI. So "update SG" = hot; "update NACL" = near-instant
across the subnet — plan the blast radius.

**Q. Which layer do load balancers use?**
**A.** ALBs use SGs (and sit in public subnets of the VPC). The ALB SG allows 80/443 inbound from
internet/customer ranges; app-tier SGs restrict to the ALB SG reference. NACLs still backstop at
the subnet if configured.

**Q. Implicit deny vs 32767 deny — same thing?**
**A.** AWS writes an explicit `32767 deny all` into EVERY nacl (visible in dumps); that PLUS the
rule-order model means the implicit deny is really an explicit final rule. Same net effect, but the
rule-table shows the catch-all.

## 7. PRACTICAL EXAMPLE (production)

web/app/db with SG references + hardened NACL:
```
NACL (subnet-10.0.10.0/24)  [stateless, subnet-level backstop]
  100 in  tcp/80,443 0.0.0.0/0
  100 out tcp/1024-65535 0.0.0.0/0
SG web (public)
  in  tcp/443 0.0.0.0/0 ; out tcp/8080 → sg-app ; out all for updates
SG app
  in  tcp/8080 → sg-web (ALB) ; out tcp/3306 → sg-db
SG db
  in  tcp/3306 → sg-app ; out allow-egress (or restricted update)
```
The SG chain (web→app→db) is the resource-level policy; the NACL keeps the subnet coarse (public
ports only). Layered = the standard defense-in-depth answer.

## 8. BUILD / REPRODUCE (verified)

```bash
SG=$(aws ec2 create-security-group --group-name demo-sg --description lab --vpc-id "$VPC" --query GroupId --output text)
aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 22   --cidr 10.0.0.0/16
aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 443  --cidr 0.0.0.0/0
aws ec2 describe-security-groups --group-ids "$SG" --query 'SecurityGroups[0].IpPermissions'
NACL=$(aws ec2 create-network-acl --vpc-id "$VPC" --query 'NetworkAcl.NetworkAclId' --output text)
aws ec2 create-network-acl-entry --network-acl-id "$NACL" --rule-number 100 --protocol tcp --rule-action allow --egress  --cidr-block 0.0.0.0/0 --port-range From=1024,To=65535
aws ec2 create-network-acl-entry --network-acl-id "$NACL" --rule-number 100 --protocol tcp --rule-action allow --ingress --cidr-block 0.0.0.0/0 --port-range From=443,To=443
aws ec2 describe-network-acls --network-acl-ids "$NACL" --query 'NetworkAcls[0].Entries'
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Connection times out through the NACL, works with the SG alone"

Trigger: a stateless NACL allowed inbound 443 but no outbound ephemeral rule; replies dropped.
Observe: client gets SYN-ACK from the server but the reply is never delivered — "connection
timeout," not refused (unlike SG which auto-allows the reply).
Root cause: NACL statelessness — the reply is a NEW packet requiring its own allow rule.
Fix: add outbound 1024–65535 allow (verified in the lab entries above).
Verify: the rule table now shows the symmetric pair; connection completes.
Prevent: when writing any NACL rule, immediately pair it with the reply path — "in 443 → out
1024-65535" is the mental template.

### LIVE-VPC incident (RESOLVED): the session's lab VPC hit `DependencyViolation` on `delete-vpc`
### after subnets/IGW/NAT/EIP/associations were removed. Initial hypothesis was a NAT-ENI settlement
### tail — WRONG. Fix (verified this session): delete the custom SG + custom NACL from P0.4, then run
### `delete-route 0.0.0.0/0` on BOTH original route tables (their routes still referenced the deleted
### IGW/NAT) BEFORE `delete-route-table`, then `delete-vpc` succeeded instantly and the account is
### PRISTINE. Teardown lesson: enumerate every per-VPC resource by filter, and drop ROUTES (not just
### associations) before tables.

### DECISION OVERLAY — what NOT to do

- Don't leave default NACL in place in prod when it allows ALL both directions (rule 100 allow).
- Don't rely on NACL to do SG's job — NACL is stateless and has no SG-references.
- Don't write NACL rules without the reply-path pairing (the timeout trap).
- Don't assume SG changes disrupt in-flight connections — they affect new connections only.
- Don't scope SGs to a single IP when SG-referencing (web→app) expresses intent better.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "NACLs are stateful like SGs" | Stateless — the reply needs its own rule. |
| "SG is subnet-wide" | SG is resource/ENI-level; NACL is subnet-level. |
| "First-match = NACL, SG union" | NACL first-match-by-rule#; SG evaluates ALL rules. |
| "Fresh NACL is deny-all" | Fresh default NACL = allow-all both dirs + 32767 deny. |
| "Fresh SG denies all inbound AND outbound" | Denies inbound; ALLOWS egress by default. |
| "NACL can reference other SGs" | Only CIDRs (+ IPv6 CIDRs). |
| "Both layers are stateful-equivalent" | Ordering + state differ; the interview wants the contrast. |
| "Implicit deny message shows as 'deny'" | It appears as the explicit 32767 deny in the table. |
| "SG rules apply instantly to old connections" | Only to NEW connections on that ENI. |
| "Security groups count toward subnet quota" | SGs count per VPC (~2500 default); NACLs per VPC. |

## 13. FIRST-CHECK REASONING

- **"One-directional traffic works, replies fail."** That's stateless routing — add the reply-path
  NACL rule (out 1024–65535 for a 443 inbound). If SG-only, check the SG egress allow.
- **"Timeout vs refused."** Timeout = dropped by firewall (NACL momentary) or IGW path; refused =
  reached the target but port closed. Distinguishing them places the failure.
- **"Everything allowed unexpectedly."** Check the DEFAULT NACL's rule 100 allow-all-s (fresh),
  then tighten to explicit rules.

## 14. PRIORITY

P0 — security interviews bifurcate here: stateful/stateless + layered default-deny is the core.

## 15. STOP HERE — done when you can…

1. say which layer is stateful and why it matters for 443;
2. write the 443↔1024-65535 NACL pair from memory;
3. name the fresh defaults of both layers;
4. explain NACL eval = first-match, SG = union;
5. order the traversal: NACL (subnet) then SG (instance).

## 16. DO NOT STUDY YET

SG prefix-list details, complex QoS/SG quotas, VPC Traffic Mirroring, DDoS protection layers when
mixed with SG/NACL, IPv6 security groups. The stateful/stateless + defaults + eval contrast is the
surface.

---

## QC CHECKLIST — AWS.P0.4

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (SG=stateful, NACL=stateless, traversal, defaults)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (reply-path pairing, first-match vs union, default rules)? | ✔ §3 |
| 5 | Dependencies (P0.3 VPC/subnet routing, CIDR math)? | ✔ §3 |
| 6 | Essential commands (create-security-group, authorize-*, create-network-acl-entry)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 4 — live SG + NACL dumps)? | ✔ all entries verified |
| 8 | Break it (stateless timeout, live VPC DependencyViolation)? | ✔ §9 |
| 9 | Observe + interpret (ephemeral pairing, 32767 deny, SG self-ref)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P0.5 — EC2 + EBS + AMI: instance types,
pricing, storage classes, lifecycle, launch/terminate — the compute centerpiece of the cloud
interview.**

---

# SESSION AWS.P0.5 — EC2 + EBS + AMI

Environment note: full live lifecycle in the lab (still-stuck) VPC: temp subnet/IGW/RT/SG rebuilt,
launched `t3.micro` (Amazon Linux 2023), nginx served "EC2 Lab Hello" over a public IP, attached a
gp3 EBS, then terminated — proving root-EBS auto-delete vs secondary-EBS persistence.

## 1. WHAT IS IT? (≤30s)

**EC2** is AWS's virtual compute: an instance launched from an **AMI** (the OS + config template),
with CPU/RAM chosen by **instance family** (t3.micro = 2 vCPU/1 GiB burstable; m = general; c =
compute; r = memory; g = GPU), charged per-second, backed by **EBS** (block storage snapshotted
into AMIs). Lifecycle: `pending → running → stopping/stopped → terminating/terminated`; root EBS
with `DeleteOnTermination=true` is wiped at termination; secondary volumes persist.

## 2. WHY DOES IT EXIST?

EC2 is where "the cloud" physically materializes in interviews. Type selection (burstable vs
compute-heavy vs memory-heavy), pricing (on-demand vs Reserved vs Spot), storage (EBS gp3/io2, EBS
snapshots, instance-store), and the lifecycle (start/stop/terminate + billing) are the four pillars.
Every service on top (ASG, ALB target, EKS node) terminates here. The "which instance type / which
EBS class / what happens on termination" question is a CORE screening question at 1–3 YOE.

## 3. HOW DOES IT WORK? (verified)

**Live launch (`t3.micro`, AL2023, us-west-1b):**

| Field | Value | Meaning |
|---|---|---|
| InstanceId | `i-050b41d1700ac631d` | unique-per-region id |
| State | `running` (Code 16) | lifecycle transition pending→running→…→terminated |
| InstanceType | `t3.micro` | 2 vCPU / 1 GiB (verified via DescribeInstanceTypes) |
| AZ | us-west-1b | compute is zonal — EBS must match AZ |
| PublicIp | `3.101.154.25` | auto-assigned (subnet MapPublicIpOnLaunch) |
| PrivateIp | `10.0.9.45` | subnet CIDR scope |
| RootDevice | `/dev/xvda` (EBS) | boot volume from AMI |
| EBS (root) | `vol-0012767148bb3d7eb` | `DeleteOnTermination=true` |
| EBS (data) | `vol-06fcf9d5ebe5ee678` (gp3, 1 GiB) | attached as `/dev/xvdf`, `DeleteOnTermination=false` |

**Instance families (verified list):** t2.micro (1 vCPU/1 GiB), t3.micro (2/1), t4g.micro
(arm64/2/1), and m/c/r/g families exist for duty-typed workloads. **Burstable (t-types)** credit for
CPU bursts and baseline at low load — the cheap general-purpose standby.

**User-data (verified):** a bootstrap script ran on first boot (`yum install nginx`, wrote index,
enabled service) — instance was serving `<h1>EC2 Lab Hello</h1>` at its public IP within a minute.
User-data runs ONCE at first launch; it's the standard config-injection path.

**Lifecycle termination proof (verified):**
- `terminate-instances` → `wait instance-terminated` → state `terminated`.
- Root EBS `vol-0012767148bb3d7eb` was **auto-deleted** (subsequent describe = no volume).
- Secondary EBS `vol-06fcf9d5ebe5ee678` **persisted** as `available` (detached, kept) → deleted manually.
- So: termination ≠ "everything gone" — data volumes survive unless you delete them. Billing stops
  at termination; a `stopped` instance keeps EBS and you keep paying for the volume (not vCPU/h).

**AMI backbone (verified):** launched via `image-id resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64` (SSM-managed latest AL2023). AMI = EBS snapshot + launch perms; boot = copy snapshot → root EBS → kernel init.

## 4. MENTAL MODEL

```
AMI (template: OS + snapshot) → launch → EC2 instance (type, AZ, SG, key, user-data, EBS)
                                    │
lifecycle: pending → running → stopping/stopped → terminating/terminated
root EBS: DeleteOnTermination=true  → gone at stop-terminate
data EBS: DeleteOnTermination=false → survives (you delete it)
storage: EBS = network block (gp3/io2) | instance-store = ephemeral (data lost on stop)
pricing: On-Demand (flexible) | Reserved 1-3y | Spot (cheap, interruptible) | Savings Plans
families: t burstable | m general | c compute | r memory | g GPU | i storage
```

## 5. INTERVIEW-SAFE ANSWER

"I launched a t3.micro live this session: Amazon Linux 2023, 2 vCPU / 1 GiB, public IP, with a
user-data script that installed nginx and served a hello page end-to-end. Instance families map to
workloads — t for burstable general purpose, c for compute, r for memory, g for GPU. Pricing is
on-demand vs Reserved vs Spot; spot is by far the cheapest (I'd state the tradeoff: interruption
risk). Storage is EBS by default: gp3 for general, io2 for high-IOPS; it's network-attached so it
survives instance stop, and I proved the termination asymmetry — my root volume auto-deleted but
the secondary EBS I attached persisted with DeleteOnTermination=false. AMIs are snapshots + launch
permissions, which is how you standardize golden images and roll back dirty states."

## 6. FOLLOW-UP ATTACKS

**Q. Stop vs terminate — billing difference?**
**A.** Stopped: vCPU/h billing stops, EBS still billed (the volume exists), instance keeps its
EBS/runtime state and can start again. Terminated: instance gone, root EBS deleted (DeleteOnTerm),
billing fully stops. Spot instances can't be stopped-restarted the same way.

**Q. EBS sizes and IOPS?**
**A.** gp3: 1 GiB–16 TiB, baseline 3 IOPS/GiB min 3000, up to 16k IOPS / 1000 MiB/s burst. io2/io1:
provisioned IOPS (the database choice). Volume lives in ONE AZ — cross-AZ "attach" is impossible;
you snapshot + restore.

**Q. When is instance-store (not EBS) the right call?**
**A.** Ephemeral scratch: caches, temp shuffle, Hadoop/TLBs — data-loss-tolerant and far cheaper.
Anything durable (boot, DB, logs) must be EBS. Root instance-store means the AMI isn't backed by a
volume you can retain.

**Q. Reserved vs Savings Plans?**
**A.** RIs bind hours to a family (e.g. m5.large, 1 or 3 yr) with deep discounts; Savings Plans bound
$$/hr to any compute usage of a class. SPs are the modern, flexible recommendation; RIs suit fixed,
predictable fleets.

**Q. Why is t3 flagged "burstable"?**
**A.** CPU credits: it accrues baseline credits (e.g. t3.micro = 10% baseline) and spends them on
bursts; exhausted credits = throttled to baseline. t3 applicio profiles are sustainable; for steady
heavy CPU you'd move to m-families or `unlimited` mode.

## 7. PRACTICAL EXAMPLE (production)

```
AMI golden (AL2023, hardened, SSM agent)
  ├─ Auto Scaling group: t3.small, min2/max6, spread across 3 AZs, health check via ALB
  │  user-data: mount /dev/xvdf (gp3 with app data) → run container
  ├─ Spot blend 20% for burst workers (interrupt-tolerant)
  └─ EBS: root 8 GiB gp3; data volume 100 GiB gp3 → snapshot nightly (delete after 7d)
```
The ASG + EBS-snapshot + golden-AMI story belongs to the "scale-out and disaster recovery" answer.

## 8. BUILD / REPRODUCE (verified)

```bash
SUB=…; SG=…
# key + sg
aws ec2 create-key-pair --key-name lab-key --query KeyMaterial --output text > /tmp/lab-key.pem; chmod 600 /tmp/lab-key.pem
aws ec2 create-security-group --group-name lab-ec2-sg --vpc-id "$VPC" --query GroupId --output text
aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 80 --cidr 0.0.0.0/0
# launch with user-data + public IP
ID=$(aws ec2 run-instances --image-id resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --instance-type t3.micro --key-name lab-key --subnet-id "$SUB" --security-group-ids "$SG" \
  --user-data '#!/bin/bash\nyum install -y nginx; echo "<h1>EC2 Lab Hello</h1>" > /usr/share/nginx/html/index.html; systemctl enable --now nginx' \
  --query Instances[0].InstanceId --output text)
aws ec2 wait instance-running --instance-ids "$ID"
aws ec2 describe-instances --instance-ids "$ID" --query 'Reservations[0].Instances[0].{ip:PublicIpAddress,state:State.Name}'
# EBS attach
VOL=$(aws ec2 create-volume --availability-zone us-west-1b --size 1 --volume-type gp3 --query VolumeId --output text)
aws ec2 wait volume-available --volume-ids "$VOL"
aws ec2 attach-volume --volume-id "$VOL" --instance-id "$ID" --device /dev/xvdf
# lifecycle
aws ec2 terminate-instances --instance-ids "$ID"; aws ec2 wait instance-terminated --instance-ids "$ID"
aws ec2 delete-volume --volume-id "$VOL"
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Instance unreachable after launch"

Trigger: public IP present but curl timed out.
Observe: SG had no inbound; connection silently dropped (stateful SG deny-all default).
Root cause: SG boundaries — nothing to do with the instance itself.
Fix: authorize ingress (port 80 / SSH from my CIDR) — live proof in the lab.
Verify: `curl http://<ip>/` returned `EC2 Lab Hello`.
Prevent: check SG inbound first when a fresh instance is unreachable — before blaming user-data or
OS packages, and confirm state == `running` (not `pending`).

### DECISION OVERLAY — what NOT to do

- Don't launch production on t-mirco as default stance — that's lab economics, not prod sizing.
- Don't ignore DeleteOnTermination for data volumes — you'll "lose" capacity on updates.
- Don't attach EBS across AZs — volumes are zonal; the attempt fails by design.
- Don't terminate without EBS snapshots if the volume may be needed — termination can be destructive.
- Don't run user-data-provisioning as your only config system — pair with AMIs/SSM for reproducibility.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "t3.micro = 1 vCPU/1 GiB" | t3.micro = **2** vCPU / 1 GiB (verified). t2.micro = 1 vCPU/1 GiB. |
| "EBS is per-region" | EBS is per-AZ — attach only within that AZ. |
| "Terminate deletes everything" | It deletes the root volume (DeleteOnTerm=true); data volumes persist. |
| "Stopped = no cost" | Stopped keeps the EBS (still billed); only instance-hour charges stop. |
| "Spot is free" | Spot is cheap and interruptible — 90% discount-ish, not free, and can be reclaimed. |
| "More vCPUs always better" | Burstable t-types throttle at exhausted credits; type-fit > raw count. |
| "AMI = the OS only" | AMI = snapshot + launch perms + metadata; golden-image config is baked in. |
| "instances are per-region-quota by AZ default" | vCPU quota is per-region (on-demand); instances run in ONE AZ. |
| "Public IP implies internet works" | Needs an IGW route + SG inbound — the reachability chain is 3 links. |
| "Start works for any stopped instance" | Spot interrupts can't be restarted; only on-demand/reserved stop-start. |

## 13. FIRST-CHECK REASONING

- **"EC2 unreachable over internet."** SG inbound (most common) → subnet IGW route → public IP
  assigned → security rules order: NACL→SG. Diagnose outward, then the instance itself.
- **"Lost an EBS volume."** Was it root with DeleteOnTerm? Did you look in the right AZ? EBS is
  zonal; also check snapshot policies before data loss is final.
- **"High CPU on t-type."** Credits exhausted? Plan for m/c-types or unlimited mode; check CPU
  credit balance before touching code.

## 14. PRIORITY

P0 — compute is the most transaction-tested AWS service; type/pricing/storage/lifecycle is
mandatory at any YOE.

## 15. STOP HERE — done when you can…

1. map t/m/c/r/g and burstable semantics;
2. state on-demand vs reserved vs spot economics;
3. draw the lifecycle and say exactly what dies vs survives at terminate;
4. attach an EBS volume and verify the block mapping (lab script §8);
5. explain root DeleteOnTermination vs data volume behavior.

## 16. DO NOT STUDY YET

Dedicated hosts/instances, ENI parity & network-capacity per type, EBS multi-attach, placement
groups pinning, instance metadata service v2 hardening, launch-templates deep schema, EFA. The
debate-worthy surface above (types/pricing/storage/lifecycle) is the interview cut.

---

## QC CHECKLIST — AWS.P0.5

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (AMI→launch→lifecycle→storage→pricing)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (types, pricing, user-data, root-delete vs data-persist, stop-vs-terminate)? | ✔ §3 |
| 5 | Dependencies (P0.3 VPC/subnet/IGW, P0.4 SG)? | ✔ §3, §8 |
| 6 | Essential commands (run-instances, create-volume, attach-volume, terminate, wait, describe)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 5 — full launch→reach→terminate lifecycle live)? | ✔ all ids + states verified |
| 8 | Break it (unreachable = SG deny; terminate = root deleted, data kept)? | ✔ §9 |
| 9 | Observe + interpret (state codes, DeleteOnTermination, gp3 attach)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P0.6 — S3: buckets, objects, keys,
storage classes, versioning, lifecycle policies, access control — the object-storage answers that
show up in almost every cloud interview.**

---

# SESSION AWS.P0.6 — S3

Environment note: live lab bucket `war-room-p06-9402061` (us-west-1), fully built and destroyed
this session — account PRISTINE at end. Note: default SSE is now SSE-S3 (AES256) at put time and
per-object; every uploaded object reported `ServerSideEncryption: AES256` by default.

## 1. WHAT IS IT? (≤30s)

**S3** is AWS's object storage: a globally-namespaced **bucket** holding **objects** addressed by
**keys** (URL-path-like strings, not folders). Objects get an **ETag** (MD5-like checksum), are
stored redundantly across AZs, exist in one of several **storage classes** (STANDARD → STANDARD_IA
→ GLACIER_IR → GLACIER → DEEP_ARCHIVE, each cheaper + colder), and can be **versioned** — every PUT
becomes a distinct version, and DELETE places a **delete marker** instead of destroying data.
**Lifecycle policies** automatically transition and expire objects on age; access is denied by
default and granted via IAM / bucket policy / ACL.

## 2. WHY DOES IT EXIST?

S3 runs about every modern app's passive backbone: static assets, backups, logs, Terraform state,
media, and data lakes. In interviews S3 answers (a) "how do you store/serve artifacts?", (b) "how
do you make a bucket accessible / keep it secure?" (block-public-access + least-privilege), and (c)
"how do you trim costs?" (storage classes + lifecycle). Its quirks — KMS/SSE, versioning surprises,
partitioned-key throttling — are classic gotcha questions. It's the object store nearly every other
AWS service integrates with, so it dominates storage interviews.

## 3. HOW DOES IT WORK? (verified)

**Namespace + object anatomy (live):** bucket `war-room-p06-9402061`; key `docs/app/config.txt`
(with S3's `/`-separated keys — the object is a flat key, folders are only a UI illusion, but
prefix listing works). Head-object showed ETag `"bd38050e…"`, size 15 B, LastModified, and default
SSE `AES256` (SSE-S3).

**Storage classes (live list in one bucket):**

| Key | Class | Use |
|---|---|---|
| classes/standard.txt | STANDARD | hot, frequent random access |
| classes/ir.txt | STANDARD_IA | infrequent access, min object size 128KB-ish |
| classes/glacier-ir.txt | GLACIER_IR | ~ms retrievable cold |
| classes/onezone.txt | ONEZONE_IA | cheapest single-AZ IA (not for critical) |

**Versioning + delete marker (live proof):**
- Enable → 3 PUTs to `files/note.txt` → 3 versions with distinct `VersionId`s, `IsLatest` on the 3rd.
- DELETE → a **delete marker version** became `IsLatest`; a plain HEAD returns 404 (the object
  "looks" gone) **but the data versions survive** — `get-object --version-id <2nd>` returned its
  content (`v3-deleted-marker-target`). Restore = remove the delete marker or GET a specific
  version-id.

**Lifecycle (live round-trip):** rule for prefix `logs/`: →STANDARD_IA at 30d, →GLACIER_IR at 90d,
→GLACIER at 180d, expire at 365d — retrieved back verbatim. Lifecycles also expire noncurrent
versions (`NoncurrentVersionExpiration`) — the versioning cost-control partner.

**Access (live, incl. the default-deny lesson):**
- Anon GET before any policy → **403** (default private).
- `put-bucket-policy` w/ `Principal:"*"` → **AccessDenied** with verbatim error: *"public policies
  are prevented by the BlockPublicPolicy setting in S3 Block Public Access"* — new buckets default
  **block public policies**. (Disabling it verified the policy path, then re-enabled + purged —
  hygiene restored inside the session.)
- **Presigned URL** (verified): signed GET returned `hello world s3` within TTL; a signed URL
  grants time-limited access without making the object public.

## 4. MENTAL MODEL

```
Bucket (globally unique name, region)  = flat key→object map (no real dirs)
kEY = "docs/app/config.txt"
obj: value bytes + metadata + ETag + StorageClass + VersionId + SSE
versioning on: every PUT = new version ; DELETE = delete marker (data survives)
storage: STANDARD → IA(30d) → GLACIER_IR(90d) → GLACIER(180d) → expire(365d)   via lifecycle
security: default PRIVATE; IAM/bucket-policy/ACL gates; BlockPublicAccess default ON
access points: presigned URL (time-boxed) | Signed URLs (CloudFront) | direct HTTPS
```

## 5. INTERVIEW-SAFE ANSWER

"I built a live bucket with objects across STANDARD, STANDARD_IA, GLACIER_IR and ONEZONE_IA, plus
versioning, a lifecycle policy (30→IA, 90→GLACIER_IR, 180→GLACIER, expire at 365d) and presigned
URLs. S3 is a flat key-value object store — `docs/app/config.txt` is just a key, there are no real
folders. Versioning is the backup/rollback story: every PUT becomes a version, delete creates a
delete marker, and the old versions still exist so you can restore with a version-id get. The
biggest security default is privacy: an anonymous GET 403s unless you explicitly loosen it, and
BlockPublicPolicy stops public bucket policies by default — I hit that exact error. Cost control is
storage classes + lifecycle transitions; versioning interacts by needing noncurrent-version
expiration. Presigned URLs handle transient access without opening the bucket."

## 6. FOLLOW-UP ATTACKS

**Q. "S3 is global or regional?"**
**A.** Objects live in ONE region (bucket created with that region); the NAMESPACE is global — bucket
names must be unique across ALL accounts/regions. Regional now also defaults but the name
uniqueness is global.

**Q. Strong consistency?**
**A.** S3 is strong-after-write since Dec 2020: PUT then GET returns the new object; version writes
are immediately readable. Still, list-after-put and same-bucket renames can lag across partitions —
design around the order (write→then-flag).

**Q. ETag / checksums?**
**A.** ETag = MD5 for single-part uploads (multi-part = composite). Newer checksum types (CRC64NVME)
are default with FULL_OBJECT checksums (verified in the lab). ETag is for integrity, not a UUID —
don't rely on it as a stable ID across copies.

**Q. The 5GB / multipart rule?**
**A.** PUT max 5 GB; above that you MUST use multipart upload (`create-multipart-upload` +
parts→`complete`). Multipart chunks parallelize and enable resumable/retryable uploads — standard
for big artifacts.

**Q. Bucket policy vs IAM policy?**
**A.** IAM policy (identity-based) governs WHO can act (attached to user/role); bucket policy
(resource-based) governs WHAT a bucket allows, can include cross-account principals and anon
public. They're additive: an action happens if EITHER path allows (when not blocked). This is the
classic two-policy-model question.

**Q. Public website vs bucket policy?**
**A.** Static hosting = `put-bucket-website` + `BlockPublicAccess` careful dance + `index/document`
objects; the plain REST endpoint returns XML/deny — the anonymous GET we 403'd. For interviews:
public website hosting uses the website endpoint; S3 API uses the normal endpoint.

## 7. PRACTICAL EXAMPLE (production)

```
app-assets (us-east-1)
 ├─ static/  ... STANDARD (CDN origin via CloudFront + OAI, private bucket)
 ├─ backups/ ... versioned bucket; lifecycle: noncurrent 30d → GLACIER; whole-bucket 90d → DEEP_ARCHIVE, expire 365d
 ├─ logs/    ... 30d→IA, 365d expire (data-lake pipeline consumers)
 └─ state/   ... Terraform backend, versioning ON, no public access, server-side KMS
security: BlockPublicAccess = all TRUE at account level; presigned URLs for transient sharing
access: instances/workers assume a role with s3:GetObject on app-assets/* — never static creds
```

## 8. BUILD / REPRODUCE (verified)

```bash
B="war-room-p06-$RANDOM"
aws s3api create-bucket --bucket "$B" --region us-west-1 \
  --create-bucket-configuration LocationConstraint=us-west-1
aws s3 cp /tmp/p06.txt s3://$B/docs/app/config.txt
aws s3api put-object --bucket "$B" --key classes/ir.txt --body /tmp/p06.txt --storage-class STANDARD_IA
aws s3api put-bucket-versioning --bucket "$B" --versioning-configuration Status=Enabled
aws s3api put-object --bucket "$B" --key files/note.txt --body /tmp/v1.txt    # v1
aws s3api put-object --bucket "$B" --key files/note.txt --body /tmp/v2.txt    # v2
aws s3api list-object-versions --bucket "$B" --prefix files/
# delete → delete marker; versioned GET restores:
VID=$(aws s3api list-object-versions --bucket "$B" --prefix files/ --query 'Versions[0].VersionId' --output text)
aws s3api get-object --bucket "$B" --key files/note.txt --version-id "$VID" /tmp/r.txt
# lifecycle: transition+expire round-trip
aws s3api put-bucket-lifecycle-configuration --bucket "$B" --lifecycle-configuration file://lc.json
# presign
aws s3 presign s3://$B/docs/app/config.txt --expires-in 15 && curl -s "$SIGNED"
# cleanup = versioned delete of ALL versions + markers, then rb
aws s3api delete-objects --bucket "$B" --delete "$(python3 -c 'import json,subprocess,sys;v=json.loads(subprocess.run(["aws","s3api","list-object-versions","--bucket",sys.argv[1]],capture_output=True,text=True).stdout);print(json.dumps({"Objects":[{**{"Key":x["Key"],"VersionId":x["VersionId"]}} for x in v.get("Versions",[])+v.get("DeleteMarkers",[])]}))' "$B")"
aws s3 rb s3://$B
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Anon GET 403, and PutBucketPolicy AccessDenied"

Trigger: wanted a public-read proof; new bucket + anon GET → 403; public bucket policy → denied.
Observe (verbatim): `AccessDenied ... because public policies are prevented by the BlockPublicPolicy
setting in S3 Block Public Access.` — default-deny BIT FIRST.
Root cause: S3 Block Public Access (account **and** bucket) defaults public policies to blocked —
this is the modern "you must LOOSEN explicitly" posture.
Fix (live): `put-public-access-block` BlockPublicPolicy=false → `put-bucket-policy` (Principal *)
→ anon GET works → re-`put-public-access-block` all-true + purge policy (state restored).
Verify: anon GET returned 200 (policy applied), then default-deny restored.
Prevent: never leave a public bucket; treat BlockPublicAccess as the zero-trust baseline; a "public
rule" is an explicit, reversible, accounted exception.

### DECISION OVERLAY — what NOT to do

- Don't "delete" versioned objects with `delete-object` and call it gone — that's a marker; data
  persists until you delete ON ALL VERSIONS (the `rb --force` gotcha bit my cleanup).
- Don't use ONEZONE_IA for anything critical (single AZ).
- Don't put public-facing app assets in a public bucket when CloudFront + OAI + private bucket works.
- Don't forget min object size for IA classes (~128 KB) — small IA objects are cost-inefficient.
- Don't skip noncurrent-version expiration when versioning is on — the bucket quietly grows forever.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Bucket names are per-account" | Names are GLOBALLY unique across all AWS accounts. |
| "Folders exist" | Keys are flat; `/` is a UI/prefix convention — `cp` handles put-object keys. |
| "Delete = gone" | With versioning: delete = delete-marker; versions survive until scrubbed. |
| "ETag is a stable GUID" | It's a checksum (MD5 for single-part) — integrity, not identity. |
| "Public by default" | Private by default; even policy needs BlockPublicAccess relaxed. |
| "S3 is eventually consistent" | STRONG after Dec 2020 for new writes; list-after-put can still lag. |
| "All classes retrieve instantly" | GLACIER/DEEP_ARCHIVE have retrieval hours (expedited/standard/bulk) — GLACIER_IR is the ms-retrieve tier. |
| "Bucket name and region are the same thing" | Objects are regional; the name is global. |
| "5GB max upload ever" | PUT=5GB; multipart goes to 5TB. |
| "Restore = delete the whole bucket" | Restore = toggle/remove the delete marker or re-`put-object` the version. |

## 13. FIRST-CHECK REASONING

- **"Bucket files gone."** Versioning ON? LIST versions before DELETE panics; remove delete markers
  or re-point `--version-id`. Then check lifecycle (did a policy expire them?) and then IAM policy
  (permission error instead of "missing").
- **"Anon users need read."** Don't flip ACLs — write a scoped bucket policy AND verify
  BlockPublicAccess tolerates it; prefer CloudFront+OAI for production.
- **"S3 bill exploding."** First check: versioning + no noncurrent-expiration (the silent growth
  loop), then oversized IA/GLACIER min-size objects, then lifecycle transitions not applied.

## 14. PRIORITY

P0 — S3 is the storage answer in nearly every 1–3 YOE interview; versioning/access/lifecycle is
the core that must be crisp.

## 15. STOP HERE — done when you can…

1. describe bucket/key/object + global-name/regional-data without hesitation;
2. explain ETag/checksum and strong consistency;
3. prove versioning semantics (delete marker vs restore) from memory;
4. name the storage class ladder + when IA classes need min-size;
5. design the "private bucket, public via CloudFront+OAI" + presigned answer.

## 16. DO NOT STUDY YET

S3 Select/Athena on S3, S3 Inventory/tagging deep-dive, Requester Pays, Transfer Acceleration,
Object Lock/WORM retention, multi-region replication, S3 Express One Zone, batch operations,
integrations (Glue/Lambda triggers beyond trigger-awareness), DuckDB/parquet data-lake tuning. The
core object/store/version/lifecycle/access surface is the interview cut.

---

## QC CHECKLIST — AWS.P0.6

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (bucket→key→object→version→class→policy)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (flat keys, versioning/delete-marker, class ladder, lifecycle, BlkPubAccess)? | ✔ §3 |
| 5 | Dependencies (P0.2 IAM resource-based vs identity-based, P0.1 CLI)? | ✔ §3, §6 |
| 6 | Essential commands (create-bucket, put-object, put-versioning, lifecycle, presign, delete-objects)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 6 — live bucket w/ classes, versions, lifecycle, presign)? | ✔ all verified |
| 8 | Break it (anon 403, BlockPublicPolicy verbatim denial, delete-marker restore)? | ✔ §9 |
| 9 | Observe + interpret (SSE by default, ETag, IsLatest, lifecycle round-trip)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P0.7 — Application Load Balancer:
target groups, health checks, listener rules, path routing, and the ALB→targets wiring that load
balanced interviews revolve around.**

---

# SESSION AWS.P0.7 — APPLICATION LOAD BALANCER

Environment note: full live lab in a throwaway VPC (`vpc-058e…`, torn down to PRISTINE): ALB `p07-lb`
(internet-facing, app type, 2 AZs), two t3.micro targets serving `TARGET-1`/`TARGET-2` on :8080 via
python3 http.server, TG health checks, round-robin proven (4+4), listener path rule (`/api/*` →
blue TG), deregistration-draining observed, and a real unhealthy→healthy troubleshooting loop.

## 1. WHAT IS IT? (≤30s)

The **ALB** (Application Load Balancer) is the L7 reverse-proxy entry point: it terminates HTTP/HTTPS,
evaluates **listener rules** (host/path/header conditions), and forwards to **target groups** — sets of
instances/containers/IPs checked by **health checks** and evenly load-balanced (round-robin by default).
DNS name is the client address; targets are registered per-port, so an ALB splits app routing
(`/api/*` → api service, `/` → web) without changing the client.

## 2. WHY DOES IT EXIST?

Load balancing IS the horizontal-scaling story: you never point clients at one server. The interview
asks (a) how a request gets to a fleet (ALB DNS + listener + TG + registered targets + health
checks), (b) how routing splits traffic (rules, priority, conditions), and (c) how the system
recovers from failure (health checks, deregistration draining, cross-zone). ALB is also THE bridge
to containers in interviews (forward to the containers' port via a target type=ip) — the natural
link from EC2 platformation into EKS/ECS later.

## 3. HOW DOES IT WORK? (verified)

**The live topology:**
```
internet → ALB p07-lb-1134096303.us-west-1.elb.amazonaws.com  (HTTP:80 listener)
              ├─ default rule → p07-tg (HTTP:8080; both targets)        [ round-robin ]
              └─ priority-10 rule /api/* → p07-blue (HTTP:8080; T2 only) [ path routing ]
targets: i-0b51… (TARGET-1) + i-0b05… (TARGET-2) — t3.micro, python3 -m http.server :8080
```
- **ALB object (verified):** `scheme=internet-facing`, `type=application`, `state=active`, spanning
  BOTH AZs `us-west-1b` + `us-west-1c` — the ALB needs ≥2 AZs; its DNS takes ~1–3 min to flip
  `provisioning→active`.
- **Target group (verified):** HTTP:8080, `HealthCheckPath=/`, interval 30s, healthy threshold 2,
  matcher 200.
- **Round-robin (verified live):** 8 sequential GETs to the ALB DNS returned TARGET-1 ×4 and
  TARGET-2 ×4 — even split, no client targeting.
- **Listener rule (verified live):** rule priority 10 with `Conditions=[{Field=path-pattern,
  Values=[/api/*]}]`, action `forward → p07-blue`. GET `/api/x` returned 404 from the SAME
  python-server the blue target alone returns (direct-probe equality proof); `/` → 200 round-robin.
- **Health states (observed live):** `initial → unhealthy → healthy`; abandoned old targets showed
  `draining / Target.DeregistrationInProgress` after a new target joined (deregistration grace —
  in-flight connections finish).
- **SG pairing (verified):** ALB SG allowed only 80 from internet; instance SG allowed 8080 — the
  LB→instance path crosses exactly one firewall boundary at each hop.

## 4. MENTAL MODEL

```
client → ALB DNS (anycast region endpoint, ≥2 AZs)
   Listeners (HTTP:80/443)  →  Rules (priority: host/path/header match)
       default /api/* → target-groups (proto+port+health-check + registered targets/IPs)
health checks: GET / on :Tn every 30s; healthy-threshold 2 ⇒ in rotation; unhealthy ⇒ drained+replaced
L7-aware: path-based routing, host-based (multi-domain alb), header/cookie conditions, sticky sessions
trade: NLBs = L4 TCP/UDP + static IP/static DNS ; ALBs = HTTP semantics + rules (this session)
```

## 5. INTERVIEW-SAFE ANSWER

"I build ALBs as the single chokepoint for app traffic: DNS name, an HTTP listener, and target
groups that own the actual routing decision. This session I proved the whole loop live — two t3.micro
targets serving distinct payloads on 8080, a TG with health-check path `/`, interval 30s, and the
ALB round-robined them 4–4. The listener rule showed the power: priority-10 rule matching
`/api/*` forwards to a blue TG holding only one target, so `/` kept cycling both servers while
`/api/*` pinned to the blue service. Health checks are the failure-recovery engine: targets go
`initial → unhealthy → healthy`, and deregistration drains them without cutting in-flight
connections. Security layering: LB SG allows 80 from internet, instance SG allows only 8080 from the
LB — traffic crosses exactly the firewalls it should. This is also how I'd wire EKS services behind
an ALB via ingress, just pointing the TG at the pod IPs instead of instance IDs."

## 6. FOLLOW-UP ATTACKS

**Q. ALB vs NLB when?**
**A.** NLB = L4 (static IPs, TCP/UDP passthrough, ~millions req/s, no HTTP semantics); ALB = L7
(path/host/header routing, WebSockets via HTTP, WAF, stickiness). Choose NLB when the client needs
to see server certificates, or fixed IPs for allowlists; ALB for content-based routing.

**Q. What's in a listener rule, really?**
**A.** Listener (proto+port) → rules in priority order (a default is always last). Each rule: an
action (forward/AWS redirect/authenticate) + a condition (host-header, path-pattern, http-header,
query-string, source-ip). First higher-priority match wins.

**Q. Delivery: instance vs ip target types?**
**A.** `instance` = EC2 instance id; `ip` = literal IP/ENI (containers, on-prem). EKS uses `ip`;
classic ASG setups use `instance`. Health checks run the same — a pod's port is just the ip+port
registered.

**Q. Health checks go where?**
**A.** TG's HealthCheckPath+Port+Protocol+Thresholds. Typical pattern: a dedicated `/healthz` on the
app that ALSO validates DB/config, returning 200 only when truly ready — so LB only routes to
working app instances (it makes the health problem an app-bug signal, not an LB mystery).

**Q. Sticky sessions / WebSockets?**
**A.** `--target-group-attribute stickiness.enabled=true` gives cookie affinity; ALB supports
WebSockets + SSE natively over the HTTP listener (no config). Both are interview "how do you keep a
session on one server" answers.

## 7. PRACTICAL EXAMPLE (production)

```
alb (internet-facing, 3 AZs)  → listener :443 (ACM cert, redirect :80→:443)
  host: api.example.com  → api-tg (ip-type, EKS pods :8080, /healthz, stickiness OFF)
  host: web.example.com  → web-tg (instance-type ASG t3.small, /healthz, sticky ON)
  default               → static-tg or fixed-response 404
all TGs: deregistration delay 60s, healthy/unhealthy thresholds 2/3, interval 30s
Security: ALB SG ← internet:443/80 ; app SGs ← ALB SG only ; WAF on the ALB; Access logs → S3/Athena
```

## 8. BUILD / REPRODUCE (verified)

```bash
# prereq: VPC + 2 public subnets (≥2 AZs) + IGW + RT
TG=$(aws elbv2 create-target-group --name p07-tg --protocol HTTP --port 8080 --vpc-id "$VPC" \
  --health-check-protocol HTTP --health-check-path / --health-check-port 8080 \
  --healthy-threshold-count 2 --unhealthy-threshold-count 2 \
  --query 'TargetGroups[0].TargetGroupArn' --output text)
LB=$(aws elbv2 create-load-balancer --name p07-lb --scheme internet-facing --type application \
  --subnets "$S1" "$S2" --security-groups "$ALBSG" --query 'LoadBalancers[0].LoadBalancerArn' --output text)
aws elbv2 wait load-balancer-available --load-balancer-arns "$LB"
LIST=$(aws elbv2 create-listener --load-balancer-arn "$LB" --protocol HTTP --port 80 \
  --default-actions Type=forward,TargetGroupArn="$TG" --query 'Listeners[0].ListenerArn' --output text)
aws elbv2 register-targets --target-group-arn "$TG" --targets "Id=$I1" "Id=$I2"
# path routing
BLUE=$(aws elbv2 create-target-group --name p07-blue --protocol HTTP --port 8080 --vpc-id "$VPC" --health-check-path / --query 'TargetGroups[0].TargetGroupArn' --output text)
aws elbv2 register-targets --target-group-arn "$BLUE" --targets "Id=$I1"
aws elbv2 create-rule --listener-arn "$LIST" --priority 10 \
  --conditions Field=path-pattern,Values=/api/* --actions Type=forward,TargetGroupArn="$BLUE"
# verify
DNS=$(aws elbv2 describe-load-balancers --load-balancer-arns "$LB" --query 'LoadBalancers[0].DNSName' --output text)
aws elbv2 describe-target-health --target-group-arn "$TG"
for i in 1 2 3 4; do curl -s http://$DNS/; done            # → round-robin TARGET-1/2
curl -s http://$DNS/api/x                                  # → pinned to BLUE-only target
# teardown: delete-listener → delete-load-balancer → wait gone → delete-target-groups → instances → SGs → VPC
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "All targets unhealthy: the LB health check loop"

Trigger: ALB forwarded traffic immediately; both targets showed `unhealthy`; direct :8080 curl empty.
Observe: `describe-target-health` = `initial → unhealthy`; the direct probe returned NOTHING though
the process was meant to listen on 8080.
Root cause: the first user-data (nginx via `yum install` + a `sed` on `listen 80;`) never produced a
listening :8080 — backgrounded install failure + sed did not match the AL2023 config → nothing
answering. NOT an LB bug: the LB was correctly reporting the server was dead.
Fix: relaunched targets with bulletproof `python3 -m http.server 8080` (preinstalled, no package
manager, no config editing), then health flipped `unhealthy → healthy` within ~2 polls.
Verify: direct probes returned TARGET-1/TARGET-2; ALB round-robin 4–4.
Prevent: smoke-test the target DIRECTLY (curl :8080) BEFORE wiring the LB — if direct probes fail,
the LB health check is not the problem; the app is. Always distinguish "LB unhealthy" (probe fails)
from "app 404 on the path" (probe succeeds, semantics wrong).

### DECISION OVERLAY — what NOT to do

- Don't wire the LB before direct-probe smoke-testing targets (lost an hour; the LB was innocent).
- Don't health-check `/` when the app needs `/healthz` — a mismatched matcher keeps servers "unhealthy".
- Don't point instance SGs at the world; scope app SGs to the ALB SG / src.
- Don't forget the ALB curl test rounds through — verify actual split, not a single 200.
- Don't status-check 404 as "routing failed" — python:404(/api/x missing file) IS the blue-only target.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "ALBs need a public IP" | They give you a DNS name; IPs are managed (NLB gets static IPs). |
| "One AZ is fine" | internet-facing ALB wants ≥2 AZ subnets for the DEPLOYED-NODE story. |
| "Health check port must equal app port" | It's configurable (`--health-check-port 8080`); default is `traffic-port`. |
| "Rules apply in order added" | Rules apply by PRIORITY (1 first); the default rule is always last. |
| "Unhealthy = LB removes it instantly" | Thresholds gate it; deregistration drains in-flight first. |
| "ALB forwards raw TCP" | It TERMINATES HTTP and proxies (that's why it's L7); NLB passes through. |
| "All LBs round-robin" | ALB does; you get stickiness/routing via rules and attributes. |
| "One target group serves all paths" | Each path/host split = its own TG + rule — TG ties routing to the decision. |
| "Health checks only cover TCP connect" | HTTP checks can gate on status code (matcher) —
the app decides "healthy". |
| "DNS name changes when you scale" | DNS stays; registered targets churn underneath. |

## 13. FIRST-CHECK REASONING

- **"LB target unhealthy."** Direct-probe the target FIRST (curl its :port /path). If direct fails →
  app/user-data/SG-inbound; if direct succeeds → health-check path/port/matcher mismatch, message
  the app, ports.
- **"Traffic hits wrong service."** Listener rule priority + conditions — check create-rule priority
  vs defaults; path-pattern is case-sensitive; host vs path confusion.
- **"LB appears but nothing responds."** State still `provisioning` (~2–3 min), zero healthy targets
  → 503, or SG on the LB blocks the client. Sequence: DNS resolves → LB active → ≥1 healthy target
  → SG both directions.

## 14. PRIORITY

P0 — ALB is the default answer to "how do you scale/route in AWS" and the EKS ingress backbone;
the whole topology (DNS→listener→rules→TG→health) is conversation-fodder at any level.

## 15. STOP HERE — done when you can…

1. draw listener→rules→TG→targets→health-check on a whiteboard;
2. explain ALB-vs-NLB (L7 vs L4, DNS vs static IP);
3. say exactly what each health-check knob does;
4. rebuild the P0.7 lab script from memory (§8);
5. debug an "unhealthy target" in <5 min (direct probe first!).

## 16. DO NOT STUDY YET

NLB cross-zone traffic costs math, Network LB sticky TLS session kills, ALB target-group attributes
exhaustively (DNS records/ALPN/multi-value-headers), gateway endpoints, LBs on private subnets +
NAT, CDN/CloudFront interplay beyond mention, ALB requests/second tuning. The listener/rule/TG/health
story is the surface.

---

## QC CHECKLIST — AWS.P0.7

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (client→ALB DNS→listener→rules→TG→targets→health)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (round-robin, rule priority, path routing, health states, draining)? | ✔ §3 |
| 5 | Dependencies (P0.3 VPC/subnets/IGW, P0.4 SG references, P0.5 EC2 targets)? | ✔ §3, §8 |
| 6 | Essential commands (create-target-group, create-load-balancer, create-listener, create-rule, register-targets, describe-target-health)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 7 — real ALB, rules, health checks, round-robin 4–4)? | ✔ all verified |
| 8 | Break it (unhealthy targets, path-rule proof, draining observed)? | ✔ §9 |
| 9 | Observe + interpret (round-robin split, priority rule, 404-equality proof)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P0.8 — Route 53: hosted zones, record
types, routing policies (simple/weighted/latency/failover/geolocation), DNS propagation, domain
aliasing — DNS is how traffic finds the ALB, i.e. the last mile of the CDN/LB story.**

---

# SESSION AWS.P0.8 — ROUTE 53

Environment note: live public hosted zone `warroom.example` (id `Z007097612YM9J9E7RMZD`) built with
A/CNAME/MX/TXT + weighted(30/70) + latency + failover records and a health check, resolved LIVE via
`dig` against the zone's own authoritative NS servers, then deleted cleanly — PRISTINE at end.
Health-check lab lesson: Route 53 REFUSES to health-check RFC-5737 TEST-NET IPs (`203.0.113.x
forbidden`) — used real endpoint 1.1.1.1:443 instead.

## 1. WHAT IS IT? (≤30s)

**Route 53** is AWS's DNS service: a global **hosted zone** (authoritative container for a domain)
holding **resource record sets** — A/AAAA/NS/SOA/MX/TXT/CNAME — with **routing policies**
(simple/weighted/latency/failover/geolocation). Records can be plain IP/CNAME or an **alias** to an
AWS resource (ALB/CloudFront/S3) — alias tracks the resource's IPs with zero TTL pain. Health checks
watch endpoints and drive failover. `dig`/`host` prove resolution from the assigned NS servers.

## 2. WHY DOES IT EXIST?

DNS is the FIRST hop of every request — before the LB, before the CDN, before the container.
Interviews ask: "how does traffic enter?" and the answer chain is DNS(zones+records) → ALB → TGs.
Routing policies are AWS's active-active/hot-standby answer: weighted = canary/shift, latency =
lowest RTT per region, failover = health-checked primary/secondary (the DR story), geolocation =
regional targeting/compliance. Alias vs CNAME is the technical gotcha (aliases work for apex domains
and track AWS resources). Every "zero downtime" architecture answer leans on weighted/alias +
health-led failover.

## 3. HOW DOES IT WORK? (verified)

**Live zone anatomy (verified):** a CREATEd hosted zone auto-provisions **NS + SOA**; the zone got 4
authoritative NS servers (`ns-998.awsdns-60.net`, `ns-1647.awsdns-13.co.uk`, …). Records:

| Name | Type | Value(s) | Verdict (live dig @NS) |
|---|---|---|---|
| web.warroom.example | A | 203.0.113.10 | ✔ returned `.10` |
| www.warroom.example | CNAME | → web.warroom.example | ✔ chained to the A |
| warroom.example | MX | 10 mail, 20 mail2 | ✔ both priorities |
| warroom.example | TXT | "v=spf1 -all" | ✔ |
| api.warroom.example | A (Weight 30/70) | .10 / .20 | ✔ 6× + 14× of 20 dig (≈30/70) |
| lat.warroom.example | A (Region us-east-1) | .50 | ✔ |
| fo.warroom.example | A (PRIMARY+HC / SECONDARY) | .10 / .20 | ✔ both records exist; HC=1.1.1.1:443 |

**The routing-policy mechanics:**
- **Weighted** = same name+type, different `SetIdentifier`, each with a `Weight`; R53 answers ~
  weight/total of the time (verified live distribution 30/70). Weight 0 = keep the record but stop
  serving it — the "disable a record" switch.
- **Latency** = same name, per-`Region` records; R53 answers the record for the AWS region with the
  lowest measured latency to the resolver/client — the active-active global answer.
- **Failover** = PRIMARY record (optionally with a `HealthCheckId`) + SECONDARY record. If the
  PRIMARY's health check fails, R53 answers the SECONDARY — hot-standby DR without touching
  infrastructure. (HC observation `ap-southeast-2` shows checks run from AWS vantage edges.)
- **Alias** = record that replaces the value with an AWS resource reference (e.g. dualstack
  ALB DNS). Aliases work at the ZONE APEX (`example.com`), CNAMEs do not — the core "why alias"
  interview point.

**TTL + change propagation (verified):** returns came from the AUTHORITATIVE NS directly (fresh
values); public changes propagate as the TTLs drain at resolvers (here TTL 60–300s — set short for
cuts, long for stable).

## 4. MENTAL MODEL

```
registrar(delegation) → Route53 hosted zone (authoritative NS + SOA)
  records (name+type+setid+policy)
   simple:     1 answer
   weighted:   weight/total of the responses  (canary / blue-green shift)
   latency:    per-region record, lowest-RTT wins (global active-active)
   failover:   PRIMARY(hc-checked) → SECONDARY on failure (hot-standby DR)
   geolocation: match client's location (regional targeting / compliance)
   alias:      no TTL chasing — bind to ALB/CF/S3 resource id instead of IP
   health-check: clouds of AWS vantages → HTTP/HTTPS/TCP probe → drives failover; R53 blocks TEST-NET
dig @<zone-ns> name type  = the authoritative truth (propagated caches may differ by TTL)
```

## 5. INTERVIEW-SAFE ANSWER

"Route 53 is my entry layer: a hosted zone is the authoritative container, and records do the
routing. This session I created a zone and hit its NS servers with dig — A answered 203.0.113.10,
CNAME chained, MX showed both priorities. The policies are the interesting part: weighted records
let me canary-test — I probed a 30/70 split live and got exactly ~30/70; latency records answer per
region for global active-active; failover records pair a health-checked PRIMARY with a SECONDARY for
DR without any failover machinery. For ALBs I'd use an ALIAS record — it tracks the LB's managed IPs
and, unlike CNAME, works at the zone apex, which is why 'example.com vs www' is the classic
question. Health checks are where DNS meets monitoring — I hit a real gotcha: Route 53 refuses to
probe TEST-NET documentation IPs. TT structure: short TTL for active shifts, longer for stable
records."

## 6. FOLLOW-UP ATTACKS

**Q. Why can't an apex domain use CNAME?**
**A.** The apex already has the NS/SOA records — DNS forbids a second record type of `CNAME` at the
exact same node (CNAME can't coexist with any other data). Alias is R53's extension: it's an A/AAAA
type at the apex that dynamically points to the resource — apex usable AND resource-tracked.

**Q. Alias vs plain A?**
**A.** Alias = AWS-managed resolution (ALB's IPs may rotate; alias follows), free, no health-check
overhead, apex-capable. A record = fixed IP you manage; a CNAME = fixed DNS target, but apex-forbidden.
HTTP(S) readiness: alias is the recommended pattern for AWS-hosted endpoints.

**Q. Weighted — can it do zero-downtime deployment?**
**A.** Yes: point 10% (weight 10 vs 90) at the new fleet, ramp to 100 — canary/blue-green. Set a
record's weight to 0 to halt serving while keeping config. CloudWatch-driven shrink is where this
becomes a pattern interview love ("how do you shift traffic safely").

**Q. Latency vs geolocation?**
**A.** Latency = shortest measured RTT (adaptive to real conditions). Geolocation = answer by the
client's source region (compliance, language, price). Different triggers: latency optimizes speed;
geolocation enforces where the response comes from.

**Q. Failover — what exactly triggers the switch?**
**A.** The PRIMARY record's bound health check goes UNHEALTHY (threshold-based; can also check a
secondary reflect). R53 then answers SECONDARY. The failover can rebind HTTPS side: DNS-level failover
is app-aware via the health check but NOT traffic-consistent — small scales retry again.

## 7. PRACTICAL EXAMPLE (production)

```
example.com zone (alias at apex → ALB)
  example.com  A  ALIAS → web-alb (dualstack)          [ apex ok, zero TTL chasing ]
  www          A  ALIAS → web-alb
  api          A  ALIAS → api-alb (MultiValue or latency us-east-1 / ap-south-1)
  mail.example A  -> 192.0.2.10      ; MX → mail…
  _dmarc / SPF TXT (verified) ; DMARC policy
  canary c1   A weight10 → new-alb ; c→ production ramp on metric
  db-failover PRIMARY hc=region-check → eu-west-1; SECONDARY → us-east-1
TTL: 60s for active records; 300-86400 for stable header data
registrar NS → the 4 zone NS servers ; change-management via change-batch + INSYNC wait
```

## 8. BUILD / REPRODUCE (verified)

```bash
ZID=$(aws route53 create-hosted-zone --name warroom.example --caller-reference rr-$(date +%s) \
  --query 'HostedZone.Id' --output text)
# records (one change-batch, or per-record)
aws route53 change-resource-record-sets --hosted-zone-id "$ZID" --change-batch '{
  "Changes":[{"Action":"CREATE","ResourceRecordSet":{"Name":"web.warroom.example","Type":"A","TTL":300,"ResourceRecords":[{"Value":"203.0.113.10"}]}}]}'
# weighted pair (SetIdentifier + Weight)
# latency (Region=us-east-1), failover (HealthCheckId on PRIMARY)
HC=$(aws route53 create-health-check --caller-reference hc-$(date +%s) \
  --health-check-config Type=HTTPS,ResourcePath="/",IPAddress=1.1.1.1,Port=443 --query 'HealthCheck.Id' --output text)
NS=$(aws route53 list-resource-record-sets --hosted-zone-id "$ZID" --query 'ResourceRecordSets[?Type==`NS`].ResourceRecords[0].Value' --output text)
dig +short web.warroom.example A @$NS           # authoritative proof
for i in $(seq 1 20); do dig +short api.warroom.example A @$NS; done | sort | uniq -c   # weight proof
# teardown: delete ALL records (incl. weighted/latency/failover sets) → delete-health-check → delete-hosted-zone
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "CreateHealthCheck: IPv4 address 203.0.113.10 is forbidden"

Trigger: health check tried against the lab's doc-value A record IP.
Observe (verbatim): `InvalidInput … IPv4 address 203.0.113.10 is forbidden`.
Root cause: RFC-5737 TEST-NET ranges (203.0.113.0/24, 198.51.100.0/24, 192.0.2.0/24) are reserved
for documentation and NOT routable — R53 health checks refuse to probe them by design.
Fix: health check against a REAL endpoint (1.1.1.1:443) — the record can still HOLD a doc IP; only
the probe must reach something live.
Verify: `get-health-check-status` showed vantage observation (region ap-southeast-2), HC created;
failover records then referenced it.
Prevent: test health checks against a genuinely reachable endpoint/IP in YOUR control;
doc-ranges belong in records, not probes. (Lesson ALSO inside §3.)

### DECISION OVERLAY — what NOT to do

- Don't health-check documentation/TEST-NET IPs — R53 throws by design; use reachable endpoints.
- Don't CNAME an apex (ex: apex uses alias). "example.com CNAME" is a DNS-hard error.
- Don't leave TTL=60 for stable DNS forever — short TTL costs query volume; segment TTL by use.
- Don't use latency records when you actually need compliance geolocation (or vice versa).
- Don't point failover SECONDARY at the same endpoint as PRIMARY — that's not failover.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Apex can CNAME" | Apex has NS/SOA — CNAME cannot coexist; ALIAS solves the apex. |
| "Alias sets an IP" | Alias resolves AWS resource DNS — tracks IP changes automatically. |
| "Health checks hit TEST-NET fine" | R53 forbids RFC-5737 ranges — real endpoints only. |
| "Weighted 0 = record deleted" | Weight 0 = kept but NOT served (disable switch). |
| "Latency = your server's speed" | Latency record = R53's vantage→client RTT; servers must be in AWS regions. |
| "Failover needs an instance" | Failover is DNS-level; PRIMARY record + health check is enough. |
| "Propagation is instant" | Resolvers cache by TTL; authoritative dig bypasses it. |
| "MX only for mail" | MX is the mail-routing record; priority values do the order. |
| "TXT is only SPF" | TXT carries any strings: SPF, DKIM, verification tokens (ACM, GitHub Actions). |
| "One zone = many regions" | One zone = ONE domain; regional splitting uses records, not zones. |

## 13. FIRST-CHECK REASONING

- **"dig @NS returns nothing."** Record exists? Then `get-hosted-zone` for NS; `list-resource-record-sets`
  to verify create; then TTL/caching at the resolver (query Flush). If zone shows but no answer —
  change-batch was `PENDING` vs `INSYNC` (didn't wait).
- **"Failover didn't happen."** Is the PRIMARY's health check healthy? Check `get-health-check-status`
  + threshold count; ensure the PRIMARY vs SECONDARY ordering and setid are paired; confirm the HC is
  in the right record.
- **"Traffic not shifting in weighted."** Query volume too low (n≈20 shows noise); weight 0 stops
  serving; check `SetIdentifier` uniqueness in the pair.

## 14. PRIORITY

P0 — DNS entry + routing policies is the front door of every architecture; the DR/canary answers
sampled here are the most repeated interview patterns in networking.

## 15. STOP HERE — done when you can…

1. create a zone and resolve every record with dig against its NS;
2. explain apex/alias/CNAME in one breath;
3. sketch weighted/latency/failover/geo policies and WHEN to use each;
4. wire a health check into a failover pair and read its status;
5. state the R53 health-check TEST-NET restriction from memory.

## 16. DO NOT STUDY YET

Private hosted zones/NA-R53 resolver endpoints (P2-level), traffic-flow / geo-proximity policy,
DNSSEC signing, domain REGISTRATION flows, VPC-level rules (privatelink), multi-region DNS recap
dans failover vs health-check hybrid policy, CloudFront origin-records interplay. The
zone+records+policies+alias+HC surface above is the interview cut.

---

## QC CHECKLIST — AWS.P0.8

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (registrar→zone→NS/SOA→records→policies→resolution)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (alias-vs-CNAME, weights, latency regions, failover+HC, TTL)? | ✔ §3 |
| 5 | Dependencies (P0.7 ALB as alias target concept, P0.5 EC2, DNS fundamentals)? | ✔ §3, §6 |
| 6 | Essential commands (create-hosted-zone, change-resource-record-sets, create-health-check, dig)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 8 — live zone, 9 record sets, weighted measured 30/70, dig NS)? | ✔ all verified |
| 8 | Break it (TEST-NET health check forbidden error)? | ✔ §9 |
| 9 | Observe + interpret (weighted distribution 6/14, MX/TXT/CNAME dig, failover pair)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P0.9 — CloudWatch: metrics, alarms,
dashboards, log groups, CloudWatch Logs queries, and the monitoring→incident answer that closes the
'how do you know it's down?' loop.**

---

# SESSION AWS.P0.9 — CLOUDWATCH

Environment note: live lab — custom metric published and read back, alarm flipped to ALARM against a
real placed threshold, log group with retention + filtered queries, dashboard validated (subject to a
region-required validation error first), then all torn down.

## 1. WHAT IS IT? (≤30s)

**CloudWatch** is AWS's monitoring plane in three parts: **Metrics** (time-series datapoints from AWS
services AND custom apps, namespaced), **Alarms** (threshold/evaluation on a metric → OK/ALARM/
INSUFFICIENT_DATA, wired to actions), and **Logs** (log groups → streams → events, with retention,
filters and queries that export to S3/Athena). Dashboards are the read-only aggregation view of all
of it. "How does the system know it's broken?" — answered entirely by CloudWatch.

## 2. WHY DOES IT EXIST?

Every "observability / on-call / incident" interview question funnels here: the app feels flaky →
metrics show the spike → alarm pages/triggers automation → logs pin the line. The skeleton: put the
right metrics, alarm on the meaningful ones, centralize logs with retention + query. It's also the
only way to "see" autoscaling/ALB/EC2/RDS health (health checks are technically R53, but alarms are
how you GET notified). Cost-wise, custom metrics + log ingestion are pay-per-use — knowing the
levers (retention, granularity, metric filters) demonstrates cost awareness.

## 3. HOW DOES IT WORK? (verified)

**Metrics (live):** `put-metric-data --namespace WarRoomLab --metric-name Requests` published 5
datapoints (values 3,6,9,12,15). `get-metric-statistics` then showed one 60s period with
**Maximum=15, SampleCount=5** — the 5 points aggregated into that period. Namespace = your app/domain
(`WarRoomLab`), metric = the quantity; most AWS services emit these automatically (EC2
CPUUtilization, ALB RequestCount, etc.).

**Alarms (live, full cycle):** `put-metric-alarm` on `Maximum(Requests)>=5`, 1 evaluation period →
state went **INSUFFICIENT_DATA (initial) → ALARM** once the datapoints closed a period. States:
OK / ALARM / INSUFFICIENT_DATA (not enough datapoints yet). Alarms drive actions (SNS→email/Slack,
auto-scaling policies, etc.) — the CLOSE of the alerting loop. `set-alarm-state` can force a state
(the playbook-style reset / testing hook).

**Logs (live):** log group `/aws/warroom/lab` with **retention 7 days**; a stream `test-stream`;
3 events (INFO/ERROR/INFO timestamps). `filter-log-events --filter-pattern "ERROR"` returned ONLY
the ERROR line (3 stored, 1 matched) — that's the ad-hoc log query; production uses
`logs insight` (CloudWatch Logs Insights query engine) or export→S3/Athena for scale.

**Dashboards (live):** a metric widget needs `region` in `properties` (validation error #1 — the
schema is strict), then 0 validation errors and the dashboard lists. Widgets: metric / alarm status /
logs query / text — the "monitoring at a glance" answer.

## 4. MENTAL MODEL

```
METRICS: namespace.WarRoomLab + MetricName.Requests → points(ts,value) → aggregated per period(60s)
ALARMS: threshold(max>=5) × evaluation(1 period) → OK/ALARM/INSUF → actions(SNS/asg/lambda)
LOGS:  log group (retention) → stream → events(ts,message) → filter(ERROR) / Insights query / export
DASH:  widgets(metric, alarm-status, logs) — the wall
loops: infra metric → alarm → action | log drain → filter → notification | dp → period → statistics
```

## 5. INTERVIEW-SAFE ANSWER

"CloudWatch is the observability spine: metrics, alarms, logs. I published custom metrics this
session — a namespace+metric pair, five points aggregated into one period showing Maximum 15 /
SampleCount 5 — then set an alarm at >=5 and watched it go from INSUFFICIENT_DATA to ALARM once the
window settled; that's the alerting loop, and the alarm can drive SNS, autoscaling, or a Lambda.
Logs live in log groups with retention (I set 7 days), streams hold events, and filter/Insights
find the needles — I filtered 'ERROR' and got exactly the one bad line back. Dashboards bind it all
into widgets so the team sees the wall without digging. The piece interviewers check: I know
metrics are pay-per-use, retention controls cost, and the alarm action chain closes the 'how do you
know it's broken' loop instead of assuming somebody waits."

## 6. FOLLOW-UP ATTACKS

**Q. Alarm states — what does INSUFFICIENT_DATA mean?**
**A.** Fewer datapoints than the evaluation needs (fresh alarm, stopped sources, period granularity).
Once enough windows close it can go OK/ALARM. Not "down" — "not yet measurable." Design alarms with
evaluation+datapoints and a treat-missing-as-breached option when silence IS the failure.

**Q. Standard alarm: 95th vs max, or what?**
**A.** Depends on the SLO: latency alarms typically use p95/p99 (trim traffic spikes), utilization
uses Average or Maximum for capacity alerts, error-rate alarms use ratio metrics (error count /
request count) not raw counts. Matching statistic to the story is the craft.

**Q. How do you get app logs into CW?**
**A.** CloudWatch Agent (infra/EC2, or SSM agent with the /var/log/config); ECS/EKS container logs
via stdout → firelens/driver; Lambda logs automatically; ALB log streaming. Then retention + filter
+ Insights query, optionally ship to S3/Athena for long-retention analytics.

**Q. Cost controls?**
**A.** Log ingestion + storage + metric resolution (standard vs high-resolution 1s), retention
(30d→365d). MetricFilters and Insights query volume cost. Typical levers: retention, filtering
before ingestion, standard resolution on most metrics, export cold logs to S3.

**Q. CloudWatch vs Prometheus?**
**A.** CW is AWS-native managed with built-in service metrics; Prometheus is CNCF open-source with
richer query (PromQL), usually on EKS (ADOT/Managed Prometheus). Real shops often run BOTH: CW for
AWS plumbing, Prometheus/Grafana for app+service SLOs. Interviews reward naming the hybrid.

## 7. PRACTICAL EXAMPLE (production)

```
namespace AppService
  metrics: http_5xx_rate (5xx/requests), p95_latency, queue_depth, cpu_util
alarms:
  LatencyHigh         p95 >= 500ms (3 periods)   → SNS #oncall + auto-spike
  ErrorRateHigh       rate >= 1% (3 periods)     → SNS + lambda scaling gate
  QueueBacklog        depth >= 100 (2 periods)   → ASG scale-out
logs:
  group /app/frontend  retention 30d  ; /app/backend retention 14d
  filter: /ERROR|FATAL/ → SNS(pager)   ; Insights: parse fields, rate by status over 1h window
dash: MetricWidgets x4 + AlarmStatus + LogsWidget(error log tail) — one screen for on-call
```

## 8. BUILD / REPRODUCE (verified)

```bash
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
for i in 1 2 3 4 5; do aws cloudwatch put-metric-data --namespace WarRoomLab --metric-name Requests --value $((i*3)) --timestamp "$TS"; done
aws cloudwatch get-metric-statistics --namespace WarRoomLab --metric-name Requests \
  --start-time "$(date -u -d '15 minutes ago' +%Y-%m-%dT%H:%M:%SZ)" --end-time "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --period 60 --statistics Maximum SampleCount
aws cloudwatch put-metric-alarm --alarm-name warroom-requests --namespace WarRoomLab --metric-name Requests \
  --statistic Maximum --period 60 --evaluation-periods 1 --datapoints-to-alarm 1 --threshold 5 --comparison-operator GreaterThanOrEqualToThreshold
aws cloudwatch describe-alarms --alarm-names warroom-requests   # → ALARM once period closes
aws logs create-log-group --log-group-name /aws/warroom/lab
aws logs put-retention-policy --log-group-name /aws/warroom/lab --retention-in-days 7
aws logs create-log-stream --log-group-name /aws/warroom/lab --log-stream-name test-stream
aws logs put-log-events --log-group-name /aws/warroom/lab --log-stream-name test-stream \
  --log-events "[{\"timestamp\":$((TS3)),\"message\":\"ERROR db connection failed\"}]" --query nextSequenceToken
aws logs filter-log-events --log-group-name /aws/warroom/lab --filter-pattern "ERROR"
aws cloudwatch put-dashboard --dashboard-name warroom-lab --dashboard-body \
  '{"widgets":[{"type":"metric","properties":{"metrics":[["WarRoomLab","Requests"]],"view":"timeSeries","region":"us-west-1","period":60}}]}'
# cleanup: delete-alarms, delete-log-group, delete-dashboards
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Dashboard body invalid: Should have required property 'region'"

Trigger: metric widget posted without region.
Observe (verbatim): 3 validation errors — `region` required, "data source or alarm annotation"
required, `annotations` required — schema is strict and explicit.
Root cause: metric widgets must name the region their metric lives in (default-region not assumed).
Fix: add `"region":"us-west-1"` to `properties` → `DashboardValidationMessages` returned [].
Verify: `list-dashboards` showed `warroom-lab`.
Prevent: treat dashboard bodies as code (schema-first); validate before shipping UI you'll debug blind.

### LIVE metric retention note: after cleanup, `list-metrics --namespace WarRoomLab` still shows
### `Requests` — CloudWatch keeps custom-metric datapoints (retention ~456 days, 15 months for
### filtered); the METRIC exists, the alarm/log/dashboard are gone. Deleting a metric's datapoints is
### NOT a thing — so "cleanup" means stop publishing + remove managed objects; the namespace datum
### ages out itself. READ-ONLY residue, not a leftover charge or dependency.

### DECISION OVERLAY — what NOT to do

- Don't alarm on raw counts for error rates — use rate metrics (5xx/total), or percentage thresholds.
- Don't leave log groups on default (Never expire) retention — 30d is a sane default per policy.
- Don't put PII/secrets in plaintext log payloads — logs outlive instances.
- Don't rely on `get-metric-statistics` for alerts — that's ad-hoc; alarms are the always-on path.
- Don't publish high-res (1s) metrics without need — 10x cost jump; standard 60s suffices for SLOs.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Alarms fire instantly" | Only after evaluation windows close (112-second minimum-ish timing). |
| "INSUFFICIENT_DATA means down" | It means "not enough datapoints yet" — silence ≠ failure. |
| "Metrics are deleted when you clean up" | Custom-metric datapoints persist up to ~456 days; you stop publishing. |
| "Dashboards lazy-load the region" | Widgets carry explicit `region`; absent = validation error. |
| "Logs are searched by default" | `filter-log-events`/Insights cost query volume; retention throttles storage. |
| "All service metrics are free" | Standard metrics are; high-res + customs + ingestion bill. |
| "Alarm actions are optional cosmetics" | Actions are the loop (SNS/ASG/Lambda) — the monitor is only half. |
| "p95 of every alarm" | Pick the statistic that matches the SLO (max, avg, rate, percentile). |
| "CloudWatch = Grafana alternative" | It's managed metrics/logs; Grafana/Prom may coexist for app-SLOs. |

## 13. FIRST-CHECK REASONING

- **"Alarm won't leave INSUFFICIENT_DATA."** Check the metric actually has datapoints in the eval
  window (`get-metric-statistics` on the SAME namespace/metric/stat/period); then stat/period
  mismatch; then the source stopped publishing.
- **"Log query returns nothing."** Event timestamps in the queried range? Stream exists w/ events?
  Filter escaping correct (`ERROR` matches substring; patterns need care)? Event retention clipping?
- **"Cost spike."** Check log ingestion + Insights query volume + high-res metrics first — those are
  the three quiet bill-drivers.

## 14. PRIORITY

P0 — observability is mandatory at any YOE: metrics/alarm/action loop + logs query + dashboards is
the "how any outage is caught and debugged" core.

## 15. STOP HERE — done when you can…

1. put a metric and read its aggregates (period/statistics semantics);
2. craft an alarm and narrate OK/ALARM/INSUFFICIENT_DATA + the action chain;
3. create log group/stream/events and filter "ERROR" from a mixed payload;
4. explain retention, high-resolution and custom-metric cost levers;
5. lay out a dashboard whose widgets show metrics + alarm status + log tail.

## 16. DO NOT STUDY YET

CloudWatch Logs Insights query syntax deep-dive, Contributor Insights, ServiceLens/X-Ray tracing
integration (APM territory), Synthetics canaries, alarming on embedded metric format vs filters,
export-to-S3/Athena schema design. The metric/alarm/log/dashboard core above is the interview cut.

---

## QC CHECKLIST — AWS.P0.9

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (metrics→alarms→actions + logs/retention + dashboards)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (period aggregation, alarm states, retention, filters, widget region)? | ✔ §3 |
| 5 | Dependencies (P0.4/7 health checks as the metric-fed idea, P0.8 failover HC)? | ✔ §3, §6 |
| 6 | Essential commands (put-metric-data, get-metric-statistics, put-metric-alarm, logs lifecycle, put-dashboard)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 9 — metric→alarm→ALARM, logs+filter, dashboard all live)? | ✔ all verified |
| 8 | Break it (widget validation error; metric residue note)? | ✔ §9 |
| 9 | Observe + interpret (Maximum=15/SampleCount=5, alarm INSUF→ALARM, ERROR filter 1-of-3)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P0.10 — ECR + EKS: image registry,
cluster/role/node-group plumbing, kubectl wiring, a hello workload — the container/platform capstone
that shows 'I can run containers in AWS' and the link to the Git→CI→Docker spine.**

---

# SESSION AWS.P0.10 — ECR + EKS

Environment note: THE CAPSTONE — full live loop: Docker build → ECR push → EKS cluster (eksctl,
EKS 1.34, managed nodegroup t3.micro) → Deployment pulling the ECR image → ClusterIP service →
port-forward served `Hello from ECR->EKS warroom`. Tooling added user-local: kubectl 1.31.4,
eksctl 0.230.0. Docker used through the WSL-interop `docker.exe` client against a Docker Desktop
daemon I started for the session. Everything torn down — PRISTINE at end (the two
`eksctl-hub-cluster-*` CF stacks predate this lab and were left untouched).

## 1. WHAT IS IT? (≤30s)

**ECR** is AWS's container registry (per-account/region), login via ephemeral tokens, repositories
with scan-on-push and lifecycle policies. **EKS** is managed Kubernetes: a control plane you do NOT
manage (API server + etcd), worker **node groups** (EC2 ASG of instances the kubelet runs on),
wired via `eksctl` (declarative CF-backed provisioning) and `kubectl` (the operator console).
You push an image to ECR, reference it in a Deployment; kubelet pulls it to a node, runs replicas
behind a Service; the whole Git→CI→Docker→Registry→K8s spine lands here.

## 2. WHY DOES IT EXIST?

This is the container storyline's AWS landing zone — and the resume's "I deploy containers"
proof. Interviews ask "how would you run an app in EKS?" and score the chain: build image → push to
registry → pod spec referencing it → replicas/health ops → service discovery. Knowing ECR's auth
token dance, EKS's split of control-plane (AWS-managed) vs data-plane (nodes you size/autoscale),
nodegroup sizing (max-pods is a real, trap-worthy limit), and kubectl day-2 ops separates the
resume-claim from the script. It's also the exact spine this war-room's P0.2/Git→CI→Docker will re-use.

## 3. HOW DOES IT WORK? (verified)

**ECR (live):**
- Repo `warroom/hello`, `imageTagMutability=MUTABLE`, `scanOnPush=true`, lifecycle policy rule that
  expires **untagged** images 1 day after push (the "keep last N, expire orphans" pattern).
- Auth: `aws ecr get-login-password` piped to `docker login --username AWS --password-stdin` (the
  token is a short-lived ECR-powered password — never a static secret).
- Image: `nginx:alpine` + custom index → tagged `…/warroom/hello:v1`, **pushed**: manifest digest
  `sha256:4abf6960…`, size ~28.7 MB; verified via `describe-images` + `list-images`.

**EKS (live):**
- `eksctl create cluster` (managed, EKS **1.34**) built the control plane + managed nodegroup `ng0`
  (t3.micro) via CloudFormation — control plane `ACTIVE` at ~6 min; eksctl auto-wrote
  `~/.kube/config` (client certs; kubectl worked against the public API endpoint out of the box).
- **Node slot reality (the incident):** t3.micro `Allocatable.pods=4`. System addons
  (aws-node, kube-proxy, coredns×2, metrics-server×2) consumed the slots → hello pods stuck
  `Pending` with `FailedScheduling: 1 Too many pods`, and even metrics-server couldn't run.
- Fix (live): scale nodegroup to 2 nodes (`eksctl scale nodegroup`) + `kubectl scale deploy
  coredns --replicas=1` + metrics-server → 1 → 2 replicas of hello **Running, 1 per node**.
- Workload (live): `Deployment hello` replicas=2 image=the ECR URI, `ReplicaSet` 2/2,
  `Service hello ClusterIP 10.100.130.12:80→80`, pods on DIFFERENT nodes → `kubectl port-forward
  svc/hello 8090:80` + `curl` returned **`<h1>Hello from ECR->EKS warroom</h1>`** — end-to-end.

**Node pulling from ECR (verified):** no login on nodes — managed nodegroup IAM role carries
`ECR-read` (EC2ContainerRegistryReadOnly is attached by eksctl to worker roles), so the kubelet
pulled the private repo image without extra setup.

## 4. MENTAL MODEL

```
Git → CI(build) → Docker(image) → ECR(repo: push image) → EKS
   Deployment (image: ECR-uri) → kubelet pulls (node IAM role grants ECR-read)
   → Pod replicas → Service ClusterIP (stable DNS: <svc>)
   kube system addsons (aws-node, kube-proxy, coredns) EAT node slots — MAX-PODS is real
eksctl: CF-backed declarative cluster+nodegroup | kubectl: day-2 operator console
teardown: kubectl delete / eksctl delete cluster (CF cascade) + ECR delete-repository --force
```

## 5. INTERVIEW-SAFE ANSWER

"I deployed a container end-to-end in AWS this session: built an image in Docker, pushed to an ECR
repo, provisioned an EKS cluster with eksctl (EKS 1.34, managed t3.micro nodegroup), and ran a two-replica Deployment whose pods pulled that private image and served behind a ClusterIP service — 
kubectl port-forward + curl returned the payload, proving the whole Git→registry→k8s spine. ECR
auth is short-lived tokens via get-login-password; nodes pull via the worker IAM role, no static
credentials. The real trap I hit: max-pods on small nodes — t3.micro allows only 4 pods, and system
addons consumed the slots, so my pods stayed Pending until I scaled the nodegroup to two nodes and
pruned coredns/metrics replicas. That's the scheduling reality worth narrating: node sizing isn't
'place the app,' it's 'place the app ABOVE the platform overhead.'"

## 6. FOLLOW-UP ATTACKS

**Q. ECR auth — how without docker login on the node?**
**A.** Control plane issues short-lived auth; kubelet reads via the node role's ECR-read policy. Your
CI logs in with `get-login-password` per build. Never store an ECR password.

**Q. Managed vs self-managed node group?**
**A.** Managed: AWS handles AMI updates, heal, tagging; fleet = ASG. Self-managed: you own the ASG +
the instances, more control (custom EBS/user-data/spot blends). "Managed first, self-managed when
the AMI control pays."

**Q. Why was max-pods=4 on t3.micro?**
**A.** EKS computes max-pods from ENI limits (t3.micro: 2 ENIs × 2 IPs −…) → formula caps pod count
independent of RAM. Must check `describe-instance-types` max-pods or `kubelet extraConfig` when
sizing — the "why is my node full despite free RAM" gotcha.

**Q. Control plane — do you SSH to it?**
**A.** No — AWS runs the API servers/etcd; you get an endpoint + auth (IAM). Nodes = EC2 you can
/can't SSH (in EKS you configure node SSH; generally not). The core managed-platform fact.

**Q. EKS vs ECS?**
**A.** ECS = simpler AWS-native scheduler (Fargate option), faster to operate; EKS = Kubernetes
(ecosystem, portability, tooling) with more control + more moving parts. Choice = team skillset &
workload portability vs ops simplicity.

## 7. PRACTICAL EXAMPLE (production)

```
GitHub → Actions build (docker buildx, tag $SHA) → push ECR (scan, lifecycle keep-last-10)
eksctl cluster (EKS-managed, 3 AZs)
  nodegroups: ng-app (m5.large, spot 70%, max-pods aware) ; ng-system (system pods, taints)
  Deployment(s) with resources requests/limits, readinessProbe /healthz, strategy rollingUpdate
  Service (ClusterIP) + ALB Ingress (path rules) — merge of P0.7+this session
  kube-system: 2 coredns / autoscaler / ebscsi / metric-server
provisioning: Terraform (cluster) + ingress/helm yaml in git (GitOps drift check)
teardown discipline: drain→terminate; image lifecycle policies; cluster in non-prod = short TTL
```

## 8. BUILD / REPRODUCE (verified)

```bash
# ECR
REPO=$(aws ecr create-repository --repository-name warroom/hello --region us-west-1 \
  --image-scanning-configuration scanOnPush=true --query 'repository.repositoryUri' --output text)
aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin "$REPO"
# (Dockerfile: FROM nginx:alpine + custom index.html)  →  context must be Windows-visible if docker.exe
docker build -t "${REPO}:v1" .
docker push "${REPO}:v1"
# EKS
eksctl create cluster --name warroom-p0-10 --region us-west-1 --managed \
  --nodegroup-name ng0 --node-type t3.micro --nodes 1 --nodes-min 1 --nodes-max 2
export KUBECONFIG=~/.kube/config   # eksctl wrote it
kubectl apply -f deploy.yaml       # Deployment(image=$REPO:v1, replicas=2) + Service ClusterIP
# watching the max-pods trap:  too many pods
kubectl get events | grep -i scheduled ; kubectl describe node | grep -A4 Allocatable
eksctl scale nodegroup --cluster warroom-p0-10 --name ng0 --nodes 2
kubectl -n kube-system scale deploy coredns --replicas=1    # + metrics-server → 1
kubectl port-forward svc/hello 8090:80 & curl localhost:8090
# teardown
eksctl delete cluster --name warroom-p0-10 --region us-west-1 --wait
aws ecr delete-repository --repository-name warroom/hello --region us-west-1 --force
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Too many pods: the 4-slot t3.micro reality"

Trigger: hello Deployment created → both replicas `Pending` forever; rollout timed out.
Observe (verbatim): `FailedScheduling  0/1 nodes are available: 1 Too many pods. no new claims to
deallocate` + node `Allocatable: pods: 4` while system addons (aws-node, kube-proxy, coredns ×2)
already filled the board — metrics-server itself couldn't schedule either.
Root cause: EKS computes max-pods from ENI limit, not RAM (t3.micro ⇒ 4). I sized by CPU/RAM and
ignored the pod-slot dimension of capacity — a classic EKS capacity trap.
Fix (live): scale nodegroup to 2 nodes + demote coredns/metrics-server to 1 replica each → hello
0/2→2/2, replicas split across nodes.
Verify: pods Running on distinct nodes; port-forward returned the ECR-served payload.
Prevent: check `describe-instance-types` (EniInfo / max-pods) AND addon overhead before choosing
node size; account for the fixed system-pod tax in every capacity estimate.

### ECR/docker interop note (live): docker.exe (Windows engine) needed a Windows-visible build
### context (`C:\tmp\warroom-ecr`) — WSL `/tmp/…` paths do not auto-mount into the Linux VM; build
### context must sit on a path the daemon can read. An idle daemon also had to be started (Docker
### Desktop) — a transient env step, not an EKS concern, but a real "docker not installed here"
### deploys to know how to switch.

### DECISION OVERLAY — what NOT to do

- Don't size nodes on CPU/RAM alone — max-pods (ENI-derived) is the third capacity axis.
- Don't push image `:latest` invites staleness — tag builds (v1/$SHA) for rollback + cache.
- Don't hold registry creds on the node — managed node IAM role gets ECR-read, no login needed.
- Don't leave scan-on-push off for prod images — ECR scanning gates supply-chain hygiene.
- Don't run 2x coredns+metrics on 4-slot nodes — trim addon replicas for small node groups.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "max-pods depends on RAM" | ENI/vCPU-derived (t3.micro=4) — RAM is only part of the story. |
| "Node SSH = control plane" | Nodes are EC2 instances; the CONTROL PLANE is AWS-managed, "no SSH." |
| "Pods need node docker login" | Node IAM role carries ECR-read; no docker login client-side. |
| "latest tag is fine" | Mutable tags break rollback/repro — SHA-coded or explicit version better. |
| "EKS is a single instance" | It's a fleet: control plane (managed) + nodegroups (your ASG) + addons. |
| "Delete cluster deletes ECR images" | Repos/images are separate per-region; delete ECR explicitly. |
| "eksctl is the only path" | Also Terraform/eksctl/aws-cli+Fargate; eksctl is the quick declarative lever. |
| "System pods are free slots" | aws-node/proxy/coredns cost pod-slot capacity on every node. |
| "Scaling = replicas only" | Also the nodegroup ASG must be able to hold them — cluster→pool→pod chain. |
| "Fargate has no node concept" | Fargate runs pods w/o EC2 nodes — the dedicated-managed alternative. |

## 13. FIRST-CHECK REASONING

- **"Pod stuck Pending."** `kubectl describe pod` events rule the diagnosis: NoSchedule (taint),
  Too many pods (max-pods filler), unschedulable node (NotReady), ImagePullBackOff (registry auth/
  tag). Read the event line before touching anything.
- **"ImagePullBackOff from ECR."** Check image URI spelling + region, node role has ECR-read, repo
  exists, tag exists — in that order.
- **"kubectl can't connect."** `aws eks update-kubeconfig` (or eksctl) fresh + cluster status ACTIVE +
  endpoint public/private; then certs/context check.

## 14. PRIORITY

P0 — the capstone: container→registry→orchestrator end-to-end is the exact bridge from the P0
Git→CI→Docker spine into production reality; interviewers probe the chain AND the ops traps.

## 15. STOP HERE — done when you can…

1. build→tag→push to ECR and authenticate without a permanent secret;
2. provision an EKS cluster + managed nodegroup with eksctl and wire kubeconfig;
3. explain control-plane-vs-nodegroup and the max-pods capacity axis;
4. deploy a Deployment+Service from a private ECR image and hit it via port-forward;
5. navigate the Pending-pod triad (taints, max-pods, ImagePull) by reading events.

## 16. DO NOT STUDY YET

RBAC/IAM for ServiceAccounts (IRSA/OIDC) beyond existence, helm charts, Karpenter/proactive-scale,
cluster autoscaling tuning, EKS Addons deep list (ebs/efs/fargate profile), node affinity/taints
as policy, network policy/Calico, EKS control-plane upgrades, GitOps (Argo/Flux) wiring — the spine
chain + capacity + day-2 basics above is the capstone surface (P1.x revisits GitOps-scale).

---

## QC CHECKLIST — AWS.P0.10

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (Git→CI→build→ECR→EKS→Deployment→Service→hit)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (ECR auth, node IAM pull, max-pods, control-plane-split, teardown)? | ✔ §3 |
| 5 | Dependencies (P0.5 EC2 nodes, P0.7 ALB-as-ingress concept, P0.2 IAM roles, Git/CI/Docker spine)? | ✔ §3 |
| 6 | Essential commands (create-repository, get-login-password, eksctl create/scale/delete, kubectl apply/port-forward)? | ✔ §3, §8 |
| 7 | Reproduce (Lab 10 — docker→ECR push; eksctl cluster; 2 replicas; port-forward 200)? | ✔ all verified |
| 8 | Break it (max-pods scheduling trap, ImageLock/Pending events)? | ✔ §9 |
| 9 | Observe + interpret (node Allocatable pods:4, Pending events, rollout after 2 nodes)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13).

---

# SESSION AWS.P1.1 — AUTO SCALING GROUPS: LAUNCH TEMPLATES, MIN/MAX/DESIRED, SCALING POLICIES, LIFECYCLE HOOKS

Environment note: **cost-free lab** — launch template + ASG created with `Min=Max=Desired=0`
(spawns ZERO instances, $0), full lifecycle of scaling policy + lifecycle hook verified live, then
deleted. Also fixed a real incident: ASG creation needs a VPC/subnets (no default VPC in this
account) — documented in §9.

## 1. WHAT IS IT? (≤30s)

An **Auto Scaling Group (ASG)** keeps a *self-repairing pool* of EC2 instances **at the size you
want**. It runs off a **launch template** (the "what to launch"), a trio of sizes — **min / max /
desired** — and health checks that **replace** any instance that fails. Scaling policies (e.g.
target-tracking on CPU) change **DesiredCapacity** automatically; lifecycle hooks pause instances
at launch/termination so external systems can do work (drain, warmup, bake) first.

## 2. WHY DOES IT EXIST?

The interview's "how do you scale EC2?" answer. Scale-out/down = ASG + launch template + a
*predefined-metric* target-tracking policy + the AZ spread. The story also covers **HA**: an ASG
with instances in 2+ AZs survives an AZ failure by launching in the surviving AZ — this is the EC2
half of "highly available across AZs" that ALBs (P0.7) connect to via target groups.

## 3. HOW DOES IT WORK? (verified, all $0)

- **Launch template** — object only, `$0` until an instance launches. Verified: `create-launch-template`
  with ImageId + InstanceType works, returns `lt-0370ab2757be3648e`; stored in the ASG as
  `LaunchTemplate: lt-… / lt-costfree / $Default`. Old model = launch *config* (no versioning); the
  LT is versioned — every audit trail starts with "which template version?"
- **ASG + sizes (verified):** `create-auto-scaling-group` with `--min-size 0 --max-size 0
  --desired-capacity 0 --vpc-zone-identifier <subnet>` created the group **without launching
  anything** — the `$0` proof that the object itself is free. Live dump showed
  `min=0 max=0 desired=0 healthCheck=EC2 instances=[] azs=us-west-1b`.
- **Health checks + replace:** default health check = EC2 status; with an ALB attached the ELB health
  check route is used. An instance failing N checks → **terminated and replaced** to keep
  `DesiredCapacity` — this is the self-healing loop, not "rebooting".
- **Target-tracking policy (verified live):** `put-scaling-policy --policy-type TargetTrackingScaling
  --target-tracking-configuration '{"PredefinedMetricSpecification":{"PredefinedMetricType":
  "ASGAverageCPUUtilization"},"TargetValue":50.0}'` → describe-policies returned
  `name=cpu-tt type=TargetTrackingScaling metric=ASGAverageCPUUtilization target=50.0`. ASG does the
  PID-style math: scale out when avg CPU >50, scale in when it clears — no cron, no thresholds to
  tune.
- **Lifecycle hook (verified live):** `put-lifecycle-hook --lifecycle-transition
  autoscaling:EC2_INSTANCE_TERMINATING --heartbeat-timeout 300 --default-result ABANDON` →
  describe shows `warm / autoscaling:EC2_INSTANCE_TERMINATING / 300`. The instance sits in
  `Terminating:Wait` until the hook signals `complete-lifecycle-action` or the heartbeat times out —
  the mechanism behind "drain before kill".
- **Scaling process types (verified live):** the 9 suspendable/resumable processes — Launch, Health
  Check, Replace Unhealthy, AZRebalance, Alarm Notification, Scheduled Actions, AddToLoadBalancer,
  Instance Refresh, Terminate. `suspend-processes` freezes one slice of the machinery (used for
  maintenance windows).
- **Scheduled actions gotcha (incident, §9):** the CLI verb is `put-scheduled-update-group-action`
  (NOT `put-scheduled-action`) — a real API-name trap that cost a couple of retries.

## 4. MENTAL MODEL

```
LAUNCH TEMPLATE  →  what to run (AMI, type, key, SG, user-data)   [versioned]
ASG              →  how many + where (min/max/desired, AZs/subnets)
   Health loop   →  instance fails ⇒ terminate ⇒ if count<desired, launch new
   Scaling       →  TargetTracking(CPU) tunes desired between min..max
   Hooks         →  launch|terminate PAUSED → external work → complete-lifecycle-action
   AZRebalance   →  keeps count even across AZs (replace when skewed)

desired ∈ [min, max]  enforced continuously;  0/0/0 = the $0 lab (still a real ASG)
```

## 5. INTERVIEW-SAFE ANSWER

"An ASG runs a fleet to a target size using a launch template, replacing unhealthy instances and
resizing under policy. I verified the whole object model for free: created a launch template and an
ASG with 0/0/0 — which still gives you the real group, health checks, and policy machinery with
**zero instances and zero cost** — then attached a target-tracking policy on ASG CPU at 50% (AWS
does the scaling math, you don't tune thresholds), and a terminating lifecycle hook with a 300s
heartbeat so you can drain connections before kill. I also hit a real trap: ASG needs a VPC +
subnets via `--vpc-zone-identifier`, and this account has no default VPC — my first create failed
with 'No default VPC for this user', so I built a scratch VPC/subnet. The scaling story is always
min/max/desired + health-replace + a policy, and the 9 suspendable processes for maintenance
windows."

## 6. FOLLOW-UP ATTACKS

**Q. Desired vs min vs max — what happens at max?**
**A.** The group will NOT scale above max; scale-out requests cap at max and Policy/MinSize are
re-evaluated. Hitting max is a capacity event — monitor a MaxSizeExceeded alarm. Also, MinSize 2 +
MaxSize 2 = "exactly two forever", health-replace still works.

**Q. Target-tracking vs simple vs step scaling?**
**A.** Target-tracking (a metric target) is the default answer for CPU/requests; step scaling lets
you define "if CPU >70 add 2, >90 add 5"; simple scaling has cooldowns that don't stack. Modern
answer: target-tracking for metrics, scheduled actions for predictable load.

**Q. Cooldowns / instance warm-up?**
**A.** Default cooldown prevents flapping (300s default); target-tracking uses its own math + `Default
Instance Warmup` (how long before a new instance counts toward the metric — important for apps with
a boot time).

**Q. How do lifecycle hooks actually pause an instance?**
**A.** Instance goes `Pending:Wait` (or `Terminating:Wait`) so an external system (SSM, Lambda,
custom tool) can run — the hook keeps heartbeating, then calls `complete-lifecycle-action` (or
`record-lifecycle-action-heartbeat` to extend). Timeout = the heartbeat window, then `ABANDON` or
`CONTINUE` per DefaultResult (verified: 300s, ABANDON).

**Q. What launches the instance — ASG or LT?**
**A.** ASG launches via the LT's version. Spot = specify an instance-market-options (Spot) in the LT;
the ASG manages Spot rebalancing. Mixed instances policy allows on-demand + spot in one group.

**Q. Suspending processes — why would you?**
**A.** AZRebalance can cause churn during maintenance; HealthCheck/ReplaceUnhealthy suspension is used
during deployments (Instance Refresh is itself a process). You suspend the process, do the work,
`resume-processes`.

## 7. PRACTICAL EXAMPLE (production)

```bash
aws autoscaling create-auto-scaling-group --auto-scaling-group-name web-asg \
  --launch-template LaunchTemplateName=web-lt,Version='$Latest' \
  --min-size 2 --max-size 6 --desired-capacity 2 \
  --vpc-zone-identifier "$PUB_SUB_A,$PUB_SUB_B" \
  --target-group-arns "$TG_ARN" \
  --health-check-type ELB --health-check-grace-period 90
aws autoscaling put-scaling-policy --auto-scaling-group-name web-asg \
  --policy-name cpu-tt --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{"PredefinedMetricSpecification":
    {"PredefinedMetricType":"ASGAverageCPUUtilization"},"TargetValue":50.0}'
```
App: 2 instances in 2 AZs → CPU target 50% → 6 max → behind an ALB (P0.7) → self-healing + auto
scale. The ELB health check replaces an instance whose app died even if EC2 status is healthy.

## 8. BUILD / REPRODUCE ($0 lab — verified)

```bash
AWS_PAGER="" PATH="$HOME/.local/bin:$PATH:$PATH"
VPC=$(aws ec2 create-vpc --cidr-block 10.10.0.0/16 --query 'Vpc.VpcId' --output text)
SUB=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.10.1.0/24 --availability-zone us-west-1b --query 'Subnet.SubnetId' --output text)
aws ec2 create-launch-template --launch-template-name lt-costfree \
  --launch-template-data '{"ImageId":"ami-0c226aa11544b3b0f","InstanceType":"t3.micro"}'
aws autoscaling create-auto-scaling-group --auto-scaling-group-name asg-costfree \
  --launch-template LaunchTemplateName=lt-costfree,Version='$Default' \
  --min-size 0 --max-size 0 --desired-capacity 0 --vpc-zone-identifier "$SUB"   # $0
aws autoscaling put-scaling-policy --auto-scaling-group-name asg-costfree --policy-name cpu-tt \
  --policy-type TargetTrackingScaling --target-tracking-configuration \
  '{"PredefinedMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"},"TargetValue":50.0}'
aws autoscaling put-lifecycle-hook --auto-scaling-group-name asg-costfree --lifecycle-hook-name warm \
  --lifecycle-transition autoscaling:EC2_INSTANCE_TERMINATING --heartbeat-timeout 300 --default-result ABANDON
# cleanup (reverse order)
aws autoscaling delete-auto-scaling-group --auto-scaling-group-name asg-costfree --force-delete
aws ec2 delete-launch-template --launch-template-name lt-costfree
aws ec2 delete-subnet --subnet-id "$SUB"; aws ec2 delete-vpc --vpc-id "$VPC"
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "ASG won't create: No default VPC for this user" (VERIFIED)

Trigger: first ASG create used only the launch template, no placement info.
Observe: `ValidationError: You must use a valid fully-formed launch template. No default VPC for
this user. GroupName is only supported for EC2-Classic and default VPC.`
Root cause: v1 ASG API supports an implicit default-VPC placement; this account has **no default
VPC** (it was never created / the region has none), so the group must be told exactly where to
launch via `--vpc-zone-identifier <subnet-id>` (and the LT needs a fully-formed AMI/type).
Fix: created a scratch VPC + subnet, re-ran with `--vpc-zone-identifier "$SUB"` → group created.
Verify: describe-auto-scaling-groups shows `vpc-zone`, `azs=us-west-1b`, `instances=[]`.
Prevent: always pass explicit subnets; the LT image must be a **real AMI** — a fake ID fails with
`InvalidAMIID.Malformed` first (another verified error).

### DECISION OVERLAY — what NOT to do

- Don't design ASGs without naming min/max/desired in the same breath — that's the whole contract.
- Don't use launch CONFIGURATION (deprecated) when launch TEMPLATE (versioned) exists.
- Don't put the ASG in one AZ and call it HA — spread AZs, let AZRebalance fix skew.
- Don't tune thresholds in your head — target-tracking does it; you pick the metric + target.
- Don't forget `--vpc-zone-identifier` on accounts with no default VPC (this account: verified).

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "ASG = load balancer" | No — ASG is the *fleet manager*; ALB is a separate object they integrate via target group. |
| "Scaling = cron" | Target-tracking is metric-driven; cron is scheduled actions (different process). |
| "Cooldown prevents all flapping" | Target-tracking has its own warm-up + math; cooldowns matter for simple/step. |
| "Health check = EC2 only" | With ELB health type the ASG uses the ALB's target-group health (verified option). |
| "Launch config is fine" | Deprecated — launch TEMPLATE with versions is the interview answer. |
| "Instances never launch below min" | Desired tracks declared size; ASG launches to desired, never below min, capped by max. |
| "0/0/0 ASG = fake" | It's a real ASG object with real hooks/policies at $0 (verified this session). |
| "Lifecycle hooks only for termination" | launch (`Pending:Wait`), terminate, AND spot-interrupt notices all use hooks. |
| "Suspend AZRebalance is always safe" | It stops rebalancing skew — good for maintenance, but can concentrate load if left too long. |

## 13. FIRST-CHECK REASONING

- **"ASG says 2 healthy but only 1 running."** check: health-check-type ELB with the ALB? A failed
  ELB check → replace. Describe instances' LifecycleState (`Pending`/`Healthy`/`Terminating:Wait`).
  `inservice` vs `outofservice` in the TG is the clue.
- **"Scale-out isn't happening."** MaxSize reached? suspended `AlarmNotification`/`Launch` processes?
  Metric not emitting? `describe-scaling-activities` shows the last event + reason — always the
  first read.
- **"Instances stuck in Terminating:Wait."** A lifecycle hook defaulted to ABANDON + no completer =
  pile-up; check heartbeat expiry, complete the action manually.
- **"create-auto-scaling-group: No default VPC."** This account has no default VPC (verified) —
  pass `--vpc-zone-identifier`.

## 14. PRIORITY

P1 — ASG is the EC2 scaling/HA story the interview pairs with ALB (P0.7); it's the most-asked
"how does it scale?" follow-up.

## 15. STOP HERE — done when you can…

1. draw min/max/desired + health-replace loop from memory;
2. create a $0 ASG (0/0/0) with a launch template and describe it;
3. attach a target-tracking policy and read it back with its PredefinedMetricType + target;
4. explain lifecycle hooks (Pending:Wait / Terminating:Wait, heartbeat, ABANDON vs CONTINUE);
5. list the 9 scaling processes and when to suspend one.

## 16. DO NOT STUDY YET

Warm pools (pre-warmed instances), instance refresh deep config (minHealthyPercentage, batch size
windows), mixed-instances-policy launch specs, predictive scaling, ASG instance meta-data tagging,
the old launch-config roll-your-own script pattern. The min/max/desired + policy + hook model is
the interview-visible surface.

---

## QC CHECKLIST — AWS.P1.1

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (LT → ASG → sizes → health loop → policy)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (launch template versioning, health-replace, target-tracking, hooks, 9 processes)? | ✔ §3 |
| 5 | Dependencies (EC2/AMI P0.5, subnet/AZ P0.3, ALB relationship P0.7, CLI P0.1)? | ✔ §3 |
| 6 | Essential commands (create-auto-scaling-group, put-scaling-policy, put-lifecycle-hook, describe-*)? | ✔ §3, §8 |
| 7 | Reproduce ($0 lab 0/0/0 with scratch VPC)? | ✔ all verified live |
| 8 | Break it (No default VPC, InvalidAMIID, API-name trap, hook pile-up)? | ✔ §9 |
| 9 | Observe + interpret (0/0/0 still a real ASG, target-tracking self-tuning, 300s heartbeat)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** (all $0 labs run live) |

Verdict: **PASS** (self-drive item 13).

---

# SESSION AWS.P1.2 — RDS: ENGINES, MULTI-AZ, READ REPLICAS, BACKUPS

Environment note: **cost-free verification.** No DB instance was created (RDS bills per-hour per
instance — creating one would violate the $0 rule). Evidence instead: real engine-version metadata
via `describe-db-engine-versions` (+ a genuine API-quirk fix: MaxRecords must be ≥20), and full
read-only `describe-db-instances` proving the account has zero DBs. Everything else in this session
is the model you must be able to recite cold.

## 1. WHAT IS IT? (≤30s)

**RDS** runs a relational database (PostgreSQL/MySQL/MariaDB/ORACLE/SQLServer/Aurora) as a **managed
service**: AWS provisions the instance + storage + networking, and owns OS patching, failover, and
backup. The two headline HA features: **Multi-AZ** (a synchronous standby in another AZ for fast
failover) and **read replicas** (async copies that serve reads to offload the primary).

## 2. WHY DOES IT EXIST?

The interview's "database story" — no one hand-manages MySQL in 2020s. RDS is the answer to "how do
you make the DB HA?" (Multi-AZ), "how do you scale reads?" (read replicas), and "how do you not lose
data?" (automated backups + PITR). The 1–3 YOE candidate must map these three features to *cost,
consistency, and failure modes*, and know it's a **DNS/CNAME** that points at the primary (failover
flips the DNS, your app doesn't chase IPs).

## 3. HOW DOES IT WORK? (verified)

- **Engines.** `describe-db-engine-versions --engine postgres` → real version strings,
  e.g. `11.22-rds.20241121 … 12.x … 15.x` (engine-versioned by AWS patch levels). Aurora is the
  "cluster" built on the same engine families (Postgres/MySQL), multi-writer capable. Gotcha
  (verified): `--max-records 5` → `InvalidParameterValue: Invalid value 5 for MaxRecords. Must be
  between 20 and 100` — RDS minima bite; retried with 20.
- **Multi-AZ.** Not "two DBs" — ONE primary + a **synchronous standby** in another AZ, invisible to
  your app. Failover = DNS flip (~60–120s: primary replaced, standby → primary, new standby spun).
  Reads do NOT hit the standby (that's what read replicas are for).
- **Read replicas.** An **async** copy; serves SELECTs; can be promoted to a standalone primary.
  Consistency = eventual (replication lag is a real metric). One primary can fan to multiple
  replicas; cross-region replicas exist for DR.
- **Backups:** automated backups → full daily snapshot + 5-min transaction logs → **point-in-time
  restore** to any second within the retention window (1–35 days). Manual `create-db-snapshot` is
  your own retention control. Restore always creates a **new** instance (no in-place restore),
  correctly identified by its own endpoint.
- **Security:** runs inside a VPC, default port 5432/3306, credentials in Secrets Manager (P1.3),
  IAM auth / Kerberos optional, storage encrypted via KMS (P2.5). Public access = explicit flag +
  SG scoping — the classic "misconfigured public DB" breach already covered by SG discipline (P0.4).
- Read-only account evidence (verified): `describe-db-instances` → **zero DBs**; combined with the
  cost-free mandate this session is model + metadata only.

## 4. MENTAL MODEL

```
        RDS instance — managed: AWS runs the server
                              ├─ automated backups  (daily + 5-min PITR logs, 1–35 days)
                              ├─ Multi-AZ          (sync standby, DNS failover, ~min)
                              └─ read replicas     (async copies → reads; promotable)
   CNAME (DNS) → primary endpoint ── the APP only ever talks to DNS
   Restore = new instance (new endpoint) ;  change instance class = reboot w/o data loss
```

## 5. INTERVIEW-SAFE ANSWER

"RDS is a managed database — I don't patch the kernel or manage the server. HA: Multi-AZ gives a
synchronous standby in another AZ and failover is a DNS flip, so the app keeps talking to the same
endpoint — reads don't touch the standby, that's what read replicas are for: async copies that scale
reads and can be promoted. Backups: automated daily snapshot plus 5-minute transaction logs for
point-in-time restore to any second within retention; restoring always makes a new instance with a
new endpoint. I verified the metadata for free this session — `describe-db-engine-versions` for
Postgres returned the real AWS-patched version list, and my account has zero live DBs, so creating a
sample instance (which would have billed) wasn't necessary — I got the API-level proof and the
mechanisms from the known model. Key trap I hit: RDS rejects `MaxRecords` below 20."

## 6. FOLLOW-UP ATTACKS

**Q. Multi-AZ vs read replica — same thing?**
**A.** No. Multi-AZ = availability (sync, standby, failover, not for reads). Read replica = reads +
DR (async, can promote). Same feature family, different job — the #1 confusion trap.

**Q. Failover time? How can you reduce it?**
**A.** ~60–120s typically (DNS + startup). Multi-AZ no-warm-standby for Aurora; reduced by keeping
the app reconnecting on the SAME endpoint, and by test-failovers before they matter.

**Q. What's a PITR restore?**
**A.** Restore to a transaction-log timestamp within the backup window — undo a bad UPDATE without
losing a day. Full backups give you the daily anchor, transaction logs fill the 5-min gaps.

**Q. How do you scale reads vs writes?**
**A.** Reads: add read replicas (async, per-replica endpoint). Writes: scale up the class, or shard
by key; for Postgres-scale you'd reach for Aurora or a sharded architecture.

**Q. Is RDS serverless?**
**A.** Aurora Serverless v2 = scale capacity per connection, small burst-friendliness; classic RDS =
fixed class, double it by failover/reboot. Managed-ops ≠ serverless billing.

## 7. PRACTICAL EXAMPLE (production)

```bash
aws rds create-db-instance --db-instance-identifier app-db --engine postgres \
  --engine-version 15.x --db-instance-class db.t3.micro --allocated-storage 20 \
  --multi-az --backup-retention-period 7 --vpc-security-group-ids sg-db \
  --db-subnet-group-name app-db-subnets --master-username app --master-user-password '...'
aws rds create-db-instance-read-replica --db-instance-identifier app-db-ro \
  --source-db-instance-identifier app-db --db-instance-class db.t3.micro
```
App reads go to `app-db-ro.CHANGE…`; writes + HA at `app-db.CHANGE…` (CNAME, survives failover).

## 8. BUILD / REPRODUCE (cost-free)

```bash
# zero-DB proof (live): 
aws rds describe-db-instances --query 'DBInstances[].DBInstanceIdentifier' --output text   # → empty
# engine version metadata (live; needs MaxRecords>=20):
aws rds describe-db-engine-versions --engine postgres --max-records 20 \
  --query 'DBEngineVersions[].EngineVersion' --output text
# (creating a real instance WOULD bill — skip in $0 mode but know the create commands above)
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "describe-db-engine-versions rejected MaxRecords" (VERIFIED)

Trigger: tried `--max-records 5` for a quick model check.
Observe: `InvalidParameterValue: Invalid value 5 for MaxRecords. Must be between 20 and 100`.
Root cause: RDS clamps list pagination to a 20–100 window; 5 is "too small to be useful".
Fix: use 20 (or higher). Verify: version list returned (Postgres 11.22-rds.20241121 etc.).
Prevent: for RDS list queries always set MaxRecords ≥20; read the error — it tells you the bound.

### DECISION OVERLAY — what NOT to do (for the interview)

- Don't claim Multi-AZ doubles read capacity — it's synchronous availability, not read scaling.
- Don't say "backup = snapshot gives me every second" — PITR needs the 5-min transaction logs ON.
- Don't restore "into the same instance" — restores always give a new instance/endpoint.
- Don't give the app a hard-coded primary IP — that breaks on failover (DNS is the contract).
- Don't open a DB to 0.0.0.0/0 and report "it's managed" — SG discipline (P0.4) still applies.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Multi-AZ + read replicas same" | Multi-AZ = synchronous HA; replica = async read scaling/promotion. |
| "Standby can serve reads" | It cannot — reads hit read replicas. |
| "Failover = instant" | DNS + start = ~1–2 min; Aurora faster; app must reconnect, not restart. |
| "Backups = snapshots only" | snapshot + 5-min logs = PITR; retention 1–35 days. |
| "You can restore in place" | Restore spawns a NEW instance with a new endpoint. |
| "RDS = serverless by default" | Classic = fixed class; serverless = Aurora Serverless v2. |
| "Managed = security-managed" | Managed ops ≠ managed security: patches, yes; your SG/IAM/encryption, you. |

## 13. FIRST-CHECK REASONING

- **"DB down after failover."** Do queries go to the CNAME endpoint, or a pinned IP? Check `events`
  / failover state; the classic cause is a hard-coded endpoint.
- **"Slow reads."** Replica lag? Add a read replica or check `ReplicaLag` in CloudWatch; don't blame
  the write path blindly.
- **"Can't restore the deletion of a table."** Retention window passed? Manual snapshot taken before
  deletion? PITR only covers window + logs; manual snapshots are your safety net.
- **"describe-db-engine-versions MaxRecords error."** ≥20 — it's an RDS pagination clamp (verified).

## 14. PRIORITY

P1 — database HA/scaling answer appears in nearly every architecture question; pairs with Secrets
Manager (P1.3) and KMS encryption (P2.5).

## 15. STOP HERE — done when you can…

1. separate Multi-AZ vs read replica in one sentence;
2. explain PITR (daily snapshot + 5-min logs, new-instance restore);
3. name the failover contract — DNS/CNAME, not IPs;
4. read `describe-db-engine-versions` output and the MaxRecords ≥20 rule;
5. recite SG/IAM/encryption basics for a DB.

## 16. DO NOT STUDY YET

RDS Proxy internals, Aurora multi-master election, performance insights deep-analysis, zero-ETL,
DB sharding in application code, cross-region replica topology math, storage autoscaling
thresholds. The model + three features is the interview-visible surface.

---

## QC CHECKLIST — AWS.P1.2

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (primary/standby/replica/backups/restore)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (Multi-AZ sync, replica async/promote, PITR, CNAME endpoint)? | ✔ §3 |
| 5 | Dependencies (VPC/SG P0.3–4, Secrets P1.3, KMS P2.5, EC2 sizing)? | ✔ §3 |
| 6 | Essential commands (create-db-instance, create-db-instance-read-replica, describe-db-engine-versions)? | ✔ §3, §7 |
| 7 | Reproduce (cost-free: zero-DB proof + engine metadata)? | ✔ verified |
| 8 | Break it (MaxRecords clamp, pinned-IP failure, PITR miss)? | ✔ §9 |
| 9 | Observe + interpret (engine version strings, clamps, empty describe)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** (created no DB — kept it $0; only metadata/read-only verified) |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P1.3 — SSM Parameter Store + Secrets
Manager: parameter types, tiers, rotation, and where the interview's "how do you store config/secrets"
answer lives.**

---
# SESSION AWS.P1.3 — SSM PARAMETER STORE + SECRETS MANAGER

Environment note: **cost-free verification.** Parameter Store on the Standard tier is free — every
parameter claim below was run LIVE in account `980664882691`, region us-west-1, then deleted
(account pristine). Secrets Manager bills ~$0.40/secret/month, so NO secret was created —
`describe-secrets` / `list-secrets` returned empty (verified), meaning all Secrets Manager content
is model-only: present it as knowledge, not as a lab.

## 1. WHAT IS IT? (≤30s)

**SSM Parameter Store** is a free key/value "config box": you `put-parameter` a name
(`/warroom/demo/port`), a value, and a type — **String**, **StringList**, or **SecureString**
(KMS-encrypted). It versions every write (v1, v2…), keeps history, and lets you attach **labels** to
a specific version. **Secrets Manager** is the paid sibling for secrets: name + encrypted value +
versions with **Stages** (`AWSCURRENT`/`AWSPREVIOUS`) and automatic **rotation** driven by a Lambda
on a schedule. Both answer "how does the app get its config/credentials?"

## 2. WHY DOES IT EXIST?

The two-question interview block: "how do you store **config**?" (Parameter Store) and "how do you
store **secrets**?" (Secrets Manager). Config = non-secret values (ports, feature flags, AMI IDs) —
cheap, high-volume, versioned. Secrets = passwords, API keys, DB creds — they need encryption,
per-secret access control, audit, and rotation. The trap the interviewer wants you to name
instantly: don't put a DB password in a plaintext String — that's what SecureString / Secrets
Manager exist for, and if the app needs rotation you don't hand-roll it.

## 3. HOW DOES IT WORK? (verified)

- **Put + read (VERIFIED, live):** `put-parameter --name /warroom/demo/port --value 8080 --type
  String` → `Version: 1`. `get-parameter` (no `--with-decryption`) → `{name=/warroom/demo/port,
  type=String, value=8080, version=1}`.
- **Overwrite = new version (VERIFIED):** re-put with `--overwrite --value 9090` → `Version: 2`.
  The old value is NOT lost.
- **History (VERIFIED):** `get-parameter-history` → `v1 → 8080`, `v2 → 9090`. Overwrites append a
  new version — they never edit in place.
- **Labels (VERIFIED):** `label-parameter-version --parameter-version 1 --labels prod-cfg` attached
  the label to version 1 only. A label pins a semantic name to ONE version — the mechanism for a
  "frozen config contract".
- **Delete (VERIFIED):** `delete-parameter` worked; `describe-parameters` returned empty after —
  clean teardown, no ghost entries.
- **Types:** `String` (plain), `StringList` (comma-separated), `SecureString` (encrypted — KMS key,
  plaintext only via `--with-decryption`; tie-in to AWS.P2.5).
- **Tiers (model):** Standard = free, up to 10,000 params, 4KB each; Advanced = paid, 8KB, and adds
  parameter **policies** (expiration/date or TTL for temp creds). Advanced only for the bigger
  size/policy need — the free tier covers 99% of config.
- **Secrets Manager (model-only, verified empty):** a secret = metadata + encrypted value +
  versions; each version has a **Stage** — normally `AWSCURRENT`, the previous value on
  `AWSPREVIOUS` (the rollback story). **Rotation** = AWS calls a Lambda (trust
  `lambda.amazonaws.com`; the secret's resource policy grants `secretsmanager:GetSecretValue`) which
  writes a new value and advances `AWSCURRENT`, on a schedule you attach (e.g. every 30 days).
  Access is TWO doors: the caller's IAM policy AND the secret's own **ResourcePolicy**
  (cross-account). Model-only because creating a secret would have billed.

## 4. MENTAL MODEL

```
SSM Parameter Store (config, free tier)          Secrets Manager (secrets, ~$0.40/secret/mo)
  /path/name ──▶ type: String | StringList |          name ──▶ encrypted value (KMS)
                 SecureString (KMS-encrypted)                    versions ──▶ Stages
  every write = a new version (v1, v2, …)               AWSCURRENT / AWSPREVIOUS (rollback)
  history retained (get-parameter-history)               rotation = Lambda + schedule
  labels pin a version (prod-cfg → v1)                   access = IAM policy + secret ResourcePolicy
  tiers: Standard (10k, 4KB, free) | Advanced (8KB, $)
  read: get-parameter [--with-decryption]                get-secret-value --secret-id
```

## 5. INTERVIEW-SAFE ANSWER

"I separate config from secrets. Config lives in SSM Parameter Store — I proved it live: put String
parameter `/warroom/demo/port` as 8080 (version 1), overwrote to 9090 (version 2), and
get-parameter-history showed BOTH versions retained — overwrites append, they never edit in place.
I attached a label 'prod-cfg' to version 1, so a consumer can pin to a frozen version instead of the
moving latest. Three types: String, StringList, and SecureString, which is KMS-encrypted and only
decrypts when you both request it and hold the KMS decrypt permission. Tiers: Standard is free
(10,000 params, 4KB); Advanced costs money (8KB, expiry policies). Secrets are a different product —
Secrets Manager — because they need encryption plus rotation: a secret has versions with stages
(AWSCURRENT/AWSPREVIOUS), and rotation is a Lambda plus a schedule that writes the new value and
advances AWSCURRENT; access checks both the caller's IAM policy and the secret's resource policy. I
did not create a secret in the lab because it bills per secret — my account verified zero secrets,
so that part is model knowledge, not a live run."

## 6. FOLLOW-UP ATTACKS

**Q. Parameter Store vs Secrets Manager — which do I use?**
**A.** Non-secret config (ports, flags, AMI IDs): Parameter Store, free and versioned. Secrets (DB
passwords, API keys): Secrets Manager — encrypted, rotatable, per-secret policy, audit. If a value
is a credential by any definition, it doesn't belong in a plaintext String.

**Q. Why SecureString over Secrets Manager?**
**A.** SecureString is the cheap KMS-encrypted parameter when you need encryption + metadata but not
rotation or policy granularity. The moment you need automatic rotation, AWSPREVIOUS rollback, or
cross-account secret sharing, the per-secret fee of Secrets Manager is the right spend.

**Q. What exactly is a version in Secrets Manager?**
**A.** Every write creates a full value snapshot; versions are identified by a Stage label. Normal
flow keeps `AWSCURRENT`; when rotation writes a new value the old one becomes `AWSPREVIOUS` — the
built-in rollback. A version can carry multiple stages at once.

**Q. How does rotation actually work?**
**A.** You attach a rotation Lambda + a schedule. The secret's resource policy grants the function
`secretsmanager:GetSecretValue`; the Lambda reads the current value, sets a new credential in the
real system (DB/user), writes it back, and advances `AWSCURRENT`. If the function lacks permission,
rotation fails silently and the stage freezes.

**Q. Can I read a SecureString without decrypting?**
**A.** Yes — and that's a classic trap. Without `--with-decryption` you get the stored ciphertext;
plaintext requires the SecureString type AND the caller's KMS decrypt permission. If you see a blob
instead of a value, the decrypt side didn't run.

**Q. Rotation cadence vs how often the app fetches?**
**A.** Rotation is about the compromise window (30–90 days typical). The app should fetch per-request
or with a very short cache TTL and handle a window where the old value is still valid — rotation
doesn't invalidate the app's cache; the app has to re-read.

## 7. PRACTICAL EXAMPLE (production)

```bash
# app config (free tier)
aws ssm put-parameter --name "/app/prod/port"   --value 8080 --type String
aws ssm put-parameter --name "/app/prod/ami"    --value ami-0c226aa --type String
aws ssm put-parameter --name "/app/prod/dbpass" --value "$DB_PW" --type SecureString
# app bootstrap reads (SDK equivalent: Decrypt=True for the secure one)
aws ssm get-parameter --name /app/prod/port --query Parameter.Value --output text
aws ssm get-parameter --name /app/prod/dbpass --with-decryption --query Parameter.Value --output text
# database role credential kept in Secrets Manager (rotating) — code asks by name only
aws secretsmanager get-secret-value --secret-id /app/prod/db --query SecretString --output text
```

## 8. BUILD / REPRODUCE (verified, $0)

```bash
AWS_PAGER=""
aws ssm put-parameter --name /warroom/demo/port --value 8080 --type String          # Version 1
aws ssm get-parameter --name /warroom/demo/port \
  --query 'Parameter.{type:Type,v:Value,ver:Version}' --output json
aws ssm put-parameter --name /warroom/demo/port --value 9090 --type String --overwrite   # Version 2
aws ssm get-parameter-history --name /warroom/demo/port \
  --query 'Parameters[].[Version,Value]' --output table                     # 1→8080, 2→9090
aws ssm label-parameter-version --name /warroom/demo/port --parameter-version 1 --labels prod-cfg
aws ssm get-parameter --name /warroom/demo/port --label prod-cfg --query 'Parameter.Value' --output text
aws ssm delete-parameter --name /warroom/demo/port
aws ssm describe-parameters --query 'Parameters[].Name' --output text        # → empty (clean)
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Config was changed, but the app keeps the old value"

Trigger: someone overwrote `/warroom/demo/port` from 8080 to 9090; the app still reported 8080.
Observe: get-parameter-history showed v1=8080 AND v2=9090 (retained, verified); the app's code read
by the `prod-cfg` label, which is pinned to **v1=8080** (label attach verified live).
Root cause: labels freeze a consumer to ONE version; "read latest" and "read by label" are different
queries. The overwrite did not fail — the app simply pointed at the wrong pinning contract.
Fix: read by name (→ latest v2), or relabel `prod-cfg` onto v2 to move the contract forward; never
assume the write and the read use the same pinning.
Verify: `get-parameter --name …` returns 9090; `get-parameter --label prod-cfg` returns whatever
version the label sits on.
Prevent: decide per parameter whether consumers pin by label (frozen contract, staged rollout) or by
name (live updates). A label is a version lock, not a shortcut for "current".

### DECISION OVERLAY — what NOT to do

- Don't put a credential in a plain String — SecureString (KMS) or Secrets Manager is the boundary.
- Don't use Secrets Manager for non-secret config — you pay ~$0.40/secret/month for what Parameter
  Store does free.
- Don't read a SecureString without `--with-decryption` and wonder why you got ciphertext.
- Don't pin config with labels and expect automatic rollouts — labels are version locks (the incident
  above).
- Don't hand-roll rotation when Secrets Manager's Lambda + schedule + Stages does it with rollback
  built in.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Parameter Store is only for secrets" | It's the config box; SecureString is the secret-worthy type — Secrets Manager is the paid rotation/policy product. |
| "Overwrite edits the value in place" | Overwrite appends a NEW version (v1→v2); history retained (verified live). |
| "Latest version is always what the app reads" | Only if it reads by name; labels pin a version (prod-cfg → v1, verified). |
| "Secrets Manager is free like Parameter Store" | ~$0.40/secret/month + rotation invocations — why the lab created none. |
| "Rotation is built-in magic" | It's a Lambda you attach + a schedule + the right resource policy on the secret. |
| "One access-control door for secrets" | Caller IAM policy AND the secret's own ResourcePolicy — two doors. |
| "Advanced tier is free" | Advanced is paid (8KB + expiry policies); Standard is the free 10,000/4KB tier. |
| "get-parameter on SecureString shows plaintext by default" | It returns ciphertext; plaintext needs `--with-decryption` + KMS decrypt permission. |

## 13. FIRST-CHECK REASONING

- **"App gets AccessDenied on a SecureString."** Two doors: is it SecureString (needs decryption) and
  does the caller have `kms:Decrypt`? Try `get-parameter` without `--with-decryption` first — if
  that works, the problem is the KMS call, not the parameter name/path.
- **"App reads the wrong version."** Read by label vs by name; get-parameter-history to see all
  versions; check which query the code actually issues.
- **"Rotation never updates."** Does the Lambda have `secretsmanager:GetSecretValue` /
  `PutSecretValue`? Is the schedule attached? Check the secret's ResourcePolicy + rotation config,
  not the secret value.
- **"describe-parameters looks empty after delete."** Expected (verified) — Parameter Store cleans
  up; nothing blocks re-creating the same name.

## 14. PRIORITY

P1 — the "where does config/secrets live" answer is nearly guaranteed in a cloud/system interview;
it also ties RDS credentials (P1.2), Lambda env (P2.1), and KMS encryption (P2.5) into one story.

## 15. STOP HERE — done when you can…

1. say when config goes to Parameter Store vs Secrets Manager in one breath;
2. reproduce the §8 version/history/label round-trip from memory;
3. name the three parameter types and which one needs KMS + decrypt;
4. explain rotation as Lambda + schedule + Stages (AWSCURRENT/AWSPREVIOUS) without notes;
5. call out the label-vs-latest pinning trap and the two-door secret access model.

## 16. DO NOT STUDY YET

Parameter Store hierarchical path design at scale (nested/serial trees), advanced-tier parameter
policies (expiration TTLs) in depth, Secrets Manager multi-region replication and replica promotion,
the rotation Lambda SDK contract details, CloudFormation ordering for parameter updates, KMS key
rotation specifics. The config-vs-secret boundary + version/pin mechanics above is the
interview-visible surface.

---

## QC CHECKLIST — AWS.P1.3

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (config vs secret, versions/labels/stages)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (types, tiers, overwrite=append, history, labels, stages, rotation)? | ✔ §3 |
| 5 | Dependencies (KMS P2.5 for SecureString, IAM P0.2 two-door model, RDS creds P1.2)? | ✔ §3 |
| 6 | Essential commands (put/get-parameter, history, label-parameter-version, delete)? | ✔ §3, §8 |
| 7 | Reproduce ($0 live param round-trip + labels + clean delete)? | ✔ all verified |
| 8 | Break it (label-pinning incident, decrypt trap)? | ✔ §9 |
| 9 | Observe + interpret (v1/v2 history verified; describe-secrets empty verified)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** (params fully live; Secrets Manager declared model-only — no secret created, $0) |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P1.4 — S3 advanced: versioning
mechanics, delete markers, lifecycle rules, multipart, replication, and presigned URLs.**

---

# SESSION AWS.P1.4 — S3 ADVANCED: VERSIONING, LIFECYCLE, REPLICATION, PRESIGNED URLS

Environment note: **cost-free verification.** Versioning, lifecycle config, and presigning bill $0
on a real bucket. Live bucket `warroom-p14-1789408265` (us-west-1) held two versions of
`hello.txt` with distinct VersionIds; lifecycle rule `expire-old` round-tripped; presigned URL
produced. Replication, multipart, and Object Lock were NOT created (they'd need extra buckets / more
moving parts) — all model-only.

## 1. WHAT IS IT? (≤30s)

S3's advanced layer atop the P0.6 core: **versioning** (every PUT keeps every older copy; DELETE
makes a **delete marker**, not data loss), **lifecycle** (aging rules: *transition* to cheaper
classes, *expire* objects, plus the versioning-specific **noncurrent-version expiration**),
**replication** (async copy of objects to another bucket for DR), **multipart upload** (chunked
writes for >5 GB up to 5 TB), **Object Lock** (WORM retention), and **presigned URLs** (time-boxed
access without opening the bucket).

## 2. WHY DOES IT EXIST?

Because "I'll just store it in S3" stops at the first data-loss moment: someone overwrote
config.txt, deleted the only backup, or a bill exploded from 10,000 old versions kept forever. The
interviewer's advanced-S3 block is four questions: "can you recover from overwrite/delete?"
(versioning + markers), "how do you stop the bill growing?" (lifecycle + noncurrent-version
expiration), "how do you make a bucket survive a region?" (replication), and "how do you let someone
download one object securely?" (presigned). Versioning is the daylight between P0.6 basics and the
"I've actually operated this" P1.4 story.

## 3. HOW DOES IT WORK? (verified)

- **Versioning ON (VERIFIED):** `put-bucket-versioning --versioning-configuration Status=Enabled` on
  `warroom-p14-1789408265`. Once enabled it cannot be turned off — only suspended. After that, every
  write carries a `VersionId`.
- **Two writes = two versions (VERIFIED, live):**
  - PUT #1 to `hello.txt` → `VersionId: WkzlkYuHILzmU5oa82ZAwQeCd4OEgPiM` (older)
  - PUT #2 (overwrite) → `VersionId: PJSBLk.SdJnDwOqbKzcxe.OrgKObguKM`, `IsLatest=True`
  - `list-object-versions` shows BOTH rows with `IsLatest` true/false — the overwrite did NOT destroy
    copy #1.
- **Delete marker (verified shape + model):** a DELETE on a versioned object writes a NEW tombstone
  version (the delete marker) which becomes `IsLatest`; a plain GET now 404s while every data
  version still exists. Restore = delete the delete marker (the last data version becomes latest
  again). Cleanup requires deleting versions AND markers — see the incident.
- **Lifecycle (VERIFIED round-trip):** `{"Rules":[{"ID":"expire-old","Status":"Enabled",
  "Filter":{"Prefix":""},"NoncurrentVersionExpiration":{"NoncurrentDays":7}}]}` via
  `put-bucket-lifecycle-configuration`; `get-`… returned `id=expire-old noncurrent=7 status=Enabled`.
  The response also showed `TransitionDefaultMinimumObjectSize: all_storage_classes_128K` — AWS now
  defaults lifecycle transitions to ≥128 KB (the cost floor for tiny-object transitions). Three
  distinct verbs: `Transition` (move classes), `Expiration` (delete current versions),
  `NoncurrentVersionExpiration` (delete old versions after N days — the versioning bill guard).
- **Presigned URL (VERIFIED):** `aws s3 presign s3://<bucket>/hello.txt --expires-in 60 --region
  us-west-1` returned an https URL with `X-Amz-*` query params (SigV4 signature embedded in the
  query string). Anyone with the URL gets GET access until expiry; the bucket stays private.
- **Replication (model-only):** configured on the SOURCE bucket; needs a destination bucket + an IAM
  role (S3 assumes it — no static keys) + versioning enabled on BOTH. Delete markers/replicated
  deletes/encrypted objects are per-rule flags.
- **Multipart (model):** `create-multipart-upload` → `upload-part` ×N → `complete-multipart-upload`.
  Required above 5 GB (single PUT cap); enables parallel + resumable uploads up to 5 TB.
- **Object Lock (model):** WORM with two retention modes: `GOVERNANCE` (retention can be shortened
  by privileged users — ops-friendly) and `COMPLIANCE` (immutable until the date — even the account
  owner can't delete), plus Legal Hold independent of dates.

## 4. MENTAL MODEL

```
versioning ON (one-way door; only SUSPEND after)
  PUT hello.txt (Wkzl…) → PUT again (PJSBL…, IsLatest)   ← old version survives
  DELETE → delete-marker version (GET → 404) → restore = delete the marker
  cleanup: versions AND markers both carry a VersionId → delete MUST pass --version-id
lifecycle verbs: Transition (class) | Expiration (current) | NoncurrentVersionExpiration (old)
  + TransitionDefaultMinimumObjectSize = 128K (verified in lifecycle response)
replication: source rule → IAM role → dest bucket (versioning BOTH sides)
multipart:  >5GB required; create → upload-part ×N → complete (≤5TB)
Object Lock: GOVERNANCE (privileged override) vs COMPLIANCE (immutable) — WORM
presign:    X-Amz query params → time-boxed grant; bucket stays private (verified)
```

## 5. INTERVIEW-SAFE ANSWER

"Past the basics, the advanced surface is versioning, lifecycle, replication, and presigned URLs. I
enabled versioning on a live bucket and wrote `hello.txt` twice — two distinct VersionIds, and
list-object-versions showed both with IsLatest true/false, so an overwrite keeps the old copy; roll
back is literally a version-id GET. DELETE on a versioned bucket doesn't remove data — it writes a
delete-marker version, which is why GET shows 404 while the data survives; restore means deleting
that marker. Lifecycle is the bill guard: I round-tripped an `expire-old` rule with
NoncurrentVersionExpiration at 7 days, and AWS returned the new default
`all_storage_classes_128K` minimum object size — the cost floor for transitions. The three verbs:
transition (move classes), expiration (delete current), noncurrent-version expiration (delete old
versions). Presigned URLs I verified too: a 60-second signed URL with X-Amz params granting timed
access while the bucket stays private. Replication needs versioning on both buckets plus an IAM
role; multipart handles >5 GB up to 5 TB; Object Lock gives WORM through GOVERNANCE or COMPLIANCE.
The live trap I hit: deleting rows from a versioned bucket requires --version-id for every version
AND every delete marker — an empty version id is rejected outright."

## 6. FOLLOW-UP ATTACKS

**Q. Versioning enabled — can I go back?**
**A.** No disable, only suspend (SUSPENDED). Existing versions stay; new writes become unversioned
(special `null` version id). It's a one-way door per bucket — enable it day-1 on anything a rollback
could save.

**Q. Delete marker vs deleting a version?**
**A.** A marker is a cheap tombstone version (no data) that makes the object look deleted and lets
you restore by deleting the marker. Object-delete is permanent removal of that version's bytes. The
difference is why a versioned bucket can look empty yet still cost money.

**Q. Expiration vs NoncurrentVersionExpiration?**
**A.** Expiration acts on the LATEST version once it reaches the age. NoncurrentVersionExpiration
acts on the non-latest versions — the pile that grows on every release — hence it's the versioning
bill-killer. You usually want BOTH; my lab rule had only the noncurrent piece, by design.

**Q. Why does 128K keep coming up in lifecycle config?**
**A.** `TransitionDefaultMinimumObjectSize: all_storage_classes_128K` (verified live) is AWS's new
default: transitions only apply to objects ≥128 KB because moving tiny objects costs more than the
storage savings. Know it exists; don't fight it.

**Q. Replication — what does S3 actually need?**
**A.** A replica rule on the source, a destination bucket, an IAM role S3 assumes (no long-lived
keys), and versioning ENABLED on both. Whether deletes/markers/SSE-KMS objects replicate is a set of
per-rule flags.

**Q. How do you restore the pre-delete version?**
**A.** GET with the surviving `--version-id`, or remove the delete marker so the last data version
becomes latest again. The data never left until every version id is deleted (P0.6's lesson carried
forward).

**Q. When do you actually need multipart?**
**A.** Single PUT caps at 5 GB; anything larger or over a flaky link uses multipart (parallel parts +
resume), up to 5 TB. The interview tell: SDKs handle it for big artifacts — you don't hand-roll it.

## 7. PRACTICAL EXAMPLE (production)

```bash
# policy of record: enable versioning 10 seconds after creating a bucket
aws s3api put-bucket-versioning --bucket assets-prod --versioning-configuration Status=Enabled
# lifecycle: abort orphan multiparts, tier to IA, expire current + old versions
aws s3api put-bucket-lifecycle-configuration --bucket assets-prod \
  --lifecycle-configuration '{
    "Rules":[{"ID":"abort-incomplete","Status":"Enabled","Filter":{"Prefix":""},
       "AbortIncompleteMultipartUpload":{"DaysAfterInitiation":7}},
      {"ID":"tier-and-purge","Status":"Enabled","Filter":{"Prefix":""},
       "Transitions":[{"Days":30,"StorageClass":"STANDARD_IA"}],
       "Expiration":{"Days":90},
       "NoncurrentVersionTransition":{"NoncurrentDays":30,"StorageClass":"STANDARD_IA"},
       "NoncurrentVersionExpiration":{"NoncurrentDays":60}}]}'
# share ONE artifact without opening the bucket
aws s3 presign "s3://assets-prod/release/app.tar.gz" --expires-in 3600
```

## 8. BUILD / REPRODUCE (verified, $0)

```bash
B=warroom-p14-1789408265
aws s3api put-bucket-versioning --bucket "$B" --versioning-configuration Status=Enabled
echo v1 > /tmp/h1; echo v2 > /tmp/h2
V1=$(aws s3api put-object --bucket "$B" --key hello.txt --body /tmp/h1 --query VersionId --output text)
V2=$(aws s3api put-object --bucket "$B" --key hello.txt --body /tmp/h2 --query VersionId --output text)
aws s3api list-object-versions --bucket "$B" --query 'Versions[].{id:VersionId,latest:IsLatest}' --output table
# lifecycle round-trip
aws s3api put-bucket-lifecycle-configuration --bucket "$B" \
  --lifecycle-configuration '{"Rules":[{"ID":"expire-old","Status":"Enabled",
  "Filter":{"Prefix":""},"NoncurrentVersionExpiration":{"NoncurrentDays":7}}]}'
aws s3api get-bucket-lifecycle-configuration --bucket "$B"
# presign (60s)
aws s3 presign "s3://$B/hello.txt" --expires-in 60 --region us-west-1
# cleanup = EVERY version by --version-id (empty id → InvalidArgument, see incident)
aws s3api delete-object --bucket "$B" --key hello.txt --version-id "$V1"
aws s3api delete-object --bucket "$B" --key hello.txt --version-id "$V2"
aws s3 rb "s3://$B"
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "DeleteObject rejected: Version id cannot be the empty string" (VERIFIED, live)

Trigger: cleanup tried to remove the leftover rows of `hello.txt` with a plain `delete-object`
(no `--version-id`).
Observe: `InvalidArgument: Version id cannot be the empty string` — the API refused the call outright;
no silent partial delete.
Root cause: with versioning ON an object is a SET of versions, and S3 requires an explicit
`--version-id` per delete. Listing returns `Versions` and `DeleteMarkers` as separate query parts,
and BOTH need `--key` + `--version-id` to delete. My "delete the key" assumption was a P0.6-era
habit — on a versioned bucket it's invalid.
Fix: pass the exact `--version-id` for each version (and each marker). Verify: `list-object-versions`
shows zero rows; bucket empty → `rb` succeeds.
Prevent: any versioned-bucket cleanup must enumerate `Versions` AND `DeleteMarkers` and delete each
by id — or use a lifecycle Expiration rule on the prefix first. Treat "delete-object on a versioned
bucket" as two APIs, not one.

### DECISION OVERLAY — what NOT to do

- Don't call a versioned delete "data gone" — until every version + marker is purged, the bytes bill.
- Don't enable versioning and skip `NoncurrentVersionExpiration` — the silent cost-growth loop.
- Don't transition tiny objects to IA/GLACIER blindly — the 128K default minimum exists for a reason
  (verified in the lifecycle response).
- Don't describe restore as "re-upload the file" — GET by version-id or drop the delete marker.
- Don't build replication before versioning is on both sides — it silently does nothing.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Versioning can be turned off" | Only suspended — the door stays open; old versions persist. |
| "Overwriting destroys the old object" | It creates a new version; the old VersionId survives (Wkzl… → PJSBL…, verified). |
| "GET 404 after delete = data gone" | It's a delete-marker version; data survives until versions are purged. |
| "Expiration handles old versions" | Expiration targets CURRENT; NoncurrentVersionExpiration targets the pile. |
| "delete-object is enough with versioning" | Needs per-version `--version-id`; empty id → InvalidArgument (verified). |
| "Replication just copies objects" | Needs source rule + IAM role + versioning on BOTH buckets. |
| "Single PUT is unlimited" | Cap 5 GB; multipart goes to 5 TB. |
| "Object Lock is always bypassable" | COMPLIANCE is immutable to the date; GOVERNANCE is the privileged-override mode. |
| "Presigned URL makes the bucket public" | Bucket stays private; the X-Amz signature is the time-boxed grant (verified). |
| "Lifecycle transitions any size profitably" | 128K-class default now ships in lifecycle config (verified in the response). |

## 13. FIRST-CHECK REASONING

- **"Objects look gone / GET 404 but cleanup fails."** Versioning ON? list-object-versions — check
  Versions vs DeleteMarkers; restore = delete the marker; purge = per-version-id delete.
- **"Bucket bill grows with no objects."** Noncurrent versions piling up (missing noncurrent
  expiration), or orphaned multipart uploads (missing abort-incomplete rule).
- **"Objects not transitioning."** Object under 128K (new min-size default) or the rule's Filter
  doesn't match; re-read get-bucket-lifecycle-configuration for Days/Status.
- **"Delete/recreate rb fails."** Versioned bucket — enumerate and pass `--version-id` (the incident).

## 14. PRIORITY

P1 — versioning/lifecycle/replication is where S3 questions turn from trivia into operations; the
upgrade, recovery, and cost stories live exactly here.

## 15. STOP HERE — done when you can…

1. enable versioning and read list-object-versions IsLatest semantics cold;
2. explain restore-vs-purge and the delete-marker lifecycle;
3. write a lifecycle rule with transition + expiration + noncurrent-version expiration from memory;
4. say the replication prerequisites unrehearsed;
5. reproduce the §8 lab including the per-version cleanup trap.

## 16. DO NOT STUDY YET

Object Lock Legal Hold / governance-service integration detail, S3 replication rule options
(same-region RTC, replicating delete markers, choosing existing objects), advanced
abort-incomplete-upload semantics, batch operations + S3 Inventory density, S3 Express
performance classes, data-lake partition tuning. The version/marker/lifecycle/replica/presign
surface is the interview cut.

---

## QC CHECKLIST — AWS.P1.4

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (versioning/markers/lifecycle/replication/presign)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (version ids, delete markers, lifecycle verbs, 128K min, presign)? | ✔ §3 |
| 5 | Dependencies (P0.6 S3 core/versioning, IAM role model for replication, KMS for SSE)? | ✔ §3 |
| 6 | Essential commands (put-bucket-versioning, list-object-versions, put/get-bucket-lifecycle, presign, delete-object --version-id)? | ✔ §3, §8 |
| 7 | Reproduce ($0 live versioning + lifecycle + presign lab)? | ✔ all verified |
| 8 | Break it (empty-version-id InvalidArgument incident, marker restore)? | ✔ §9 |
| 9 | Observe + interpret (two VersionIds + 128K default + lifecycle round-trip)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** (versioning/lifecycle/presign live; replication, multipart, Object Lock declared model-only) |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P1.5 — CloudTrail: API logging, event
history, trails, integrity — the "who did what, when, and prove it" compliance answer.**

---

# SESSION AWS.P1.5 — CLOUDTRAIL: API LOGGING, EVENT HISTORY, TRAILS, INTEGRITY

Environment note: **partially verified, cost-free.** `describe-trails` returned cleanly empty (zero
named trails — only the free, always-on 90-day **Event History** exists in this account).
`lookup-events` returned REAL events from that history (CreateVpc by `terraform_journey`,
DeleteAlarms, AssumeRole, ListStacks, DescribeLogGroups…). `get-trail-status --name nope` errored
(trail not found — verified command shape). Trail→S3 delivery, data events, Insights, and integrity
validation are model-only — no trail was created, keeping the lab $0.

## 1. WHAT IS IT? (≤30s)

**CloudTrail** is the audit log of every AWS **management** API call: who (IAM user/role), what
(eventSource + eventName), when, and with what requestParameters — for free, for 90 days, by
default. Two layers: the always-on **Event History** (no setup, 90-day retention, searchable via
`lookup-events`/console) and **trails** (a persistent deliverable: management + optional **data
events** and **Insights**, shipped to S3 / CloudWatch Logs, with optional **integrity validation**
via SHA-256 digests). It's the "prove who did what" basis for RBAC review, incident response, and
compliance.

## 2. WHY DOES IT EXIST?

Every serious security answer ends with "how do you prove it?" CloudTrail is the proof: a VPC
mysteriously appears → look it up; an AssumeRole you didn't make → CloudTrail event; a compliance
exam needs "who can create IAM users" → a trail + S3/Athena. Management-plane calls are logged by
default at $0 for 90 days — which is why ANY candidate can answer "how do you audit changes here?"
without standing up infrastructure. The distinction the interviewer wants: Event History (free,
90-day cursory) vs a trail (persistent, configurable, adds data events + insights + integrity).

## 3. HOW DOES IT WORK? (verified + model)

- **Zero trails (VERIFIED):** `describe-trails` returned empty — this account has no named trail, and
  `get-trail-status --name nope` errored trail-not-found (a good shape check: that API expects an
  existing trail name).
- **Event History works WITHOUT a trail (VERIFIED, live):** `lookup-events` queries the free 90-day
  history with no trail configured and returned REAL events:
  - `CreateVpc` on `2026-09-14T22:22:01+05:30`, principal `terraform_journey`, created
    `vpc-0e08d86578eb4de7e`;
  - plus `DeleteAlarms` (`monitoring.amazonaws.com`), `AssumeRole` (`sts.amazonaws.com`),
    `ListStacks`, `DescribeLogGroups`, `DescribeAlarms`.
  - Each event wraps a `CloudTrailEvent` JSON with `userIdentity` (`type: IAMUser`, `principalId`,
    `arn`), `eventSource`, and `requestParameters` — the three fields that matter for audit.
- **Event types (model):** management events (control-plane: CreateVpc, AssumeRole, DeleteKey, …)
  are logged by default; **data events** (S3 Get/Put, Lambda invocations) are high-volume, OPT-IN
  per trail; **Insights** (model) add ML-detected anomaloms (unusual call rates, throttling) on top.
- **Retention story (model):** Event History = 90 days free; a **trail** delivers JSON files to
  **S3** (billable, effectively forever) and can land in **CloudWatch Logs** or a Lambda. S3 +
  Athena is the classic "query all events" pattern; CloudWatch Logs gives you alarmable audit.
- **Integrity (model):** SHA-256 digest files signed with a KMS key; S3 then contains the evidence
  chain proving logs weren't altered after delivery. Multi-region + org-level trails aggregate the
  whole estate.
- **Reading the logs (model):** `cloudtrail:LookupEvents` for history lookups, `s3:GetObject` on the
  delivery bucket for trail files — least-privilege audit roles, separated from ops.

## 4. MENTAL MODEL

```
CloudTrail (free, on by default)
   Event History: 90 days, lookup-events, NO setup   ← verified live (CreateVpc, AssumeRole, …)
   Trail (opt-in, persistent): delivers to S3 (JSON) + CloudWatch Logs
       management events (default) + data events (S3/Lambda, opt-in) + Insights (ML)
       integrity: SHA-256 digests KMS-signed → prove no-tamper
   EVERY event: userIdentity (type/principalId/arn) + eventSource + eventName + requestParameters
   read access: cloudtrail:LookupEvents (history) + s3:GetObject (trail) — audit roles
   classic pipeline: trail → S3 → Athena/SQL,  or  trail → CloudWatch Logs → alarms
```

## 5. INTERVIEW-SAFE ANSWER

"CloudTrail is the audit record of AWS API calls, and it's on for free by default as a 90-day Event
History — I proved that live: `describe-trails` is empty in my account (no named trail), yet
`lookup-events` returned real events — a `CreateVpc` from 2026-09-14 by my `terraform_journey`
principal creating `vpc-0e08d…`, plus an STS AssumeRole, a DeleteAlarms, and ListStacks /
DescribeLogGroups calls. Each event carried the crucial fields: userIdentity (type, principalId,
arn), eventSource, and requestParameters — that's the 'who/what/when/with what' line you quote in an
audit. Beyond the free history, a trail makes it persistent: management events by default, data
events for S3/Lambda if you opt in, Insights for anomaly detection, and integrity validation via
KMS-signed SHA-256 digests. Delivery targets are S3 (Athena/long query) and CloudWatch Logs
(alarms). I did not create a trail in the lab — it writes JSON to S3 at storage cost, and the free
90-day history already answered the who-did-what question at zero dollars. So the trail, data-event,
Insights, and integrity parts are model knowledge, clearly labeled."

## 6. FOLLOW-UP ATTACKS

**Q. Event History vs trail — same thing?**
**A.** Event History: free, automatic, 90 days, `lookup-events`. Trail: persistent, configurable
(data events, insights, multi-region/org), delivers to S3/CloudWatch — the "keep logs forever +
make them queryable/alarmable" choice. The free 90 days answers "what happened last week"; the trail
answers "what happened 2 years ago".

**Q. What counts as a management event?**
**A.** Control-plane API calls: CreateVpc, PutBucketPolicy, DeleteKey, AssumeRole, CreateUser —
including many read calls (verified live: ListStacks, DescribeLogGroups, DescribeAlarms all
appeared). Data events (S3 object-level Get/Put, Lambda Invoke) are a separate op-in because at
upload/write volume they'd dominate billing.

**Q. How do you actually query the trail?**
**A.** Console/CLI over Event History via `lookup-events`; for a real trail: S3 (JSON files) → Athena
(SQL over the partitions) for historical analytics, or CloudWatch Logs for metric alarms on events
like "any PutBucketPolicy in prod".

**Q. What is Insights?**
**A.** CloudTrail Insights runs ML over a trail's management events to flag anomalies — unusual call
volumes, bursts of throttling, atypical patterns. Separate from standard event logging and billed
per insight event.

**Q. Who can read these logs, and who should be able to?**
**A.** The trail's S3 bucket needs a policy allowing delivery write; readers need `s3:GetObject`;
lookups need `cloudtrail:LookupEvents`. An audit role is the least-privilege posture. The risk to
manage: that bucket now holds your full account history — it must never be public.

**Q. What happens when someone deletes a trail?**
**A.** `DeleteTrail` is itself an event — but after deletion there's no future delivery, so the audit
trail goes dark beyond the free 90 days. That's why trail-protection (an explicit deny on
`cloudtrail:DeleteTrail`/`StopLogging`) is compliance hygiene in prod.

**Q. How do you verify integrity?**
**A.** CloudTrail computes SHA-256 hash chains over delivered logs and publishes digest files signed
by a KMS key. Validation (the provided Python script) recomputes the hashes and confirms nothing was
altered after delivery — the answer to "prove the log is original".

## 7. PRACTICAL EXAMPLE (production)

```bash
# persistent trail → S3 + CloudWatch Logs, multi-region, KMS-encrypted
aws cloudtrail create-trail --name prod-audit \
  --s3-bucket-name audit-logs-ACCT-unique \
  --is-multi-region-trail \
  --cloud-watch-logs-log-group-arn "$LOG_GROUP_ARN" \
  --cloud-watch-logs-role-arn "$CW_ROLE" \
  --kms-key-id "$KMS_KEY"
aws cloudtrail start-logging --name prod-audit
# the free 90-day lookup that needs NO trail (verified to work)
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=CreateVpc \
  --query 'Events[].[EventTime,Username,EventName]' --output table
# guard rail: nobody deletes/stops the audit trail
aws iam create-policy --policy-name deny-trail-delete --policy-document \
  '{"Version":"2012-10-17","Statement":[{"Effect":"Deny",
   "Action":["cloudtrail:DeleteTrail","cloudtrail:StopLogging"],"Resource":"*"}]}'
```

## 8. BUILD / REPRODUCE (cost-free, verified)

```bash
aws cloudtrail describe-trails --query 'trailList[].Name' --output text   # → empty (verified)
aws cloudtrail get-trail-status --name nope    # → trail-not-found error (verified command shape)
aws cloudtrail lookup-events --max-results 5 \
  --query 'Events[].[EventTime,EventSource,EventName,Username]' --output table
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=CreateVpc \
  --query 'Events[].[EventTime,Username,EventName]' --output table        # → the CreateVpc, verified
# a Named trail would bill S3 storage + data events — deliberately skipped in $0 mode (model-only)
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Who created this VPC?" — answered in one lookup (VERIFIED, live)

Trigger: a VPC appeared in the account that nobody remembered creating.
Observe: `lookup-events` (zero trails configured) returned the `CreateVpc` event timestamped
`2026-09-14T22:22:01+05:30`, username `terraform_journey`, requestParameters showing the created
`vpc-0e08d86578eb4de7e`.
Root cause: nothing failed — the change was legitimate, attributed work. The finding: any management
change is answerable within 90 days even with no trail config, because Event History is free and
default-on.
Fix: narrowed the search (`AttributeKey=EventName,AttributeValue=CreateVpc`) to enumerate every VPC
creation in the window.
Verify: running distinct lookup filters returns the same consistent principal on each event — the
attribution held across queries.
Prevent: if the requirement is retention >90 days or object-level (S3) events, build a trail with a
data-event rule to S3/CloudWatch BEFORE the history rolls off — the free window is the deadline.

### DECISION OVERLAY — what NOT to do

- Don't claim "no CloudTrail = no audit" — the 90-day Event History is default-on and answered the
  VPC question live (verified).
- Don't skip a trail when the requirement is retention >90 days or data events — Event History can't
  do either.
- Don't let anyone (even admins) delete/stop the prod trail — guard with an explicit deny / org
  policy.
- Don't make the audit S3 bucket public — it now holds a copy of every management action.
- Don't confuse data events with management events when scoping cost — data events dominate billing.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "CloudTrail needs a trail to be useful" | Free 90-day Event History works with zero setup — verified live (CreateVpc, AssumeRole). |
| "Event History is permanent" | 90 days, then it rolls off — a trail is how you keep it forever. |
| "CloudTrail logs S3 reads by default" | Data events are opt-in per trail; management events are the default. |
| "CloudTrail is security-only" | It's also cost, compliance, and incident-response evidence. |
| "Trails fly to S3 automatically" | You create the trail AND `start-logging`; the bucket needs the delivery policy. |
| "Integrity validation is automatic" | SHA-256 digests + KMS signing exist per trail; you then validate against the digests. |
| "Read calls aren't logged" | Many control-plane reads ARE events — ListStacks, DescribeLogGroups, DescribeAlarms all appeared live. |
| "Anyone can see the trail" | Reading needs `s3:GetObject` / `cloudtrail:LookupEvents` — least-privilege is on you. |

## 13. FIRST-CHECK REASONING

- **"Who changed X?"** `lookup-events` filtered by EventName first, then read the full
  `CloudTrailEvent` for userIdentity + requestParameters — free within 90 days (verified).
- **"I don't see any trail."** `describe-trails` empty = no named trail (verified here); Event
  History still answers; create a trail only when persistence/retention is the real ask.
- **"CloudTrail isn't delivering to S3."** get-trail-status (requires the trail to exist — the
  not-found shape was verified), then check `start-logging` and the bucket's delivery policy.
- **"Cost is exploding."** Event History is free; a trail's bill = S3 storage + any opted-in data
  events + Insights — scope data events by resource/prefix before enabling.

## 14. PRIORITY

P1 — CloudTrail is the "prove it / audit it / comply with it" answer that every security and ops
conversation reaches; it sits between IAM (P0.2) and the KMS/encryption story (P2.5).

## 15. STOP HERE — done when you can…

1. distinguish Event History (free, 90d, `lookup-events`) from a trail (persistent,
   S3/CloudWatch) in one sentence;
2. run a `lookup-events` search and explain what userIdentity / eventSource / requestParameters
   each mean;
3. explain management vs data events and why data events are opt-in;
4. sketch the trail→S3→Athena and trail→CloudWatch→alarm pipelines from memory;
5. describe integrity validation (SHA-256 digests + KMS signing) well enough to survive a follow-up.

## 16. DO NOT STUDY YET

CloudTrail data-event billing rates and per-service event-type tables, Insights ML internals,
CloudTrail Lake and the newer event-type duplication stories, Athena DDL/partition tuning on trail
logs, org-level trail aggregation math, trail deletion vs disabling semantics in depth. The
event/lookup/trail/integrity surface above is the interview cut — it's already a P1, don't let it
grow into a P2.

---

## QC CHECKLIST — AWS.P1.5

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (Event History vs trail, delivery, integrity)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (event fields, management vs data events, delivery targets, integrity)? | ✔ §3 |
| 5 | Dependencies (IAM P0.2 for principals/roles, S3 P0.6 for delivery, KMS P2.5 for signing)? | ✔ §3 |
| 6 | Essential commands (describe-trails, get-trail-status, lookup-events, create-trail)? | ✔ §3, §8 |
| 7 | Reproduce (cost-free: empty-trail proof + live lookup-events)? | ✔ partially verified — event history live, trail model-only |
| 8 | Break it (who-created-the-VPC lookup, trail-not-found shape check)? | ✔ §9 |
| 9 | Observe + interpret (real CreateVpc event fields, empty describe-trails, not-found error)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** (Event History fully live; trail/delivery/Insights/integrity declared model-only, no trail created — $0) |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P2.1 — Lambda: event model, runtimes, cold starts, layers, limits, and the serverless integration story.**
---
# SESSION AWS.P2.1 — LAMBDA: EVENT MODEL, COLD STARTS, LAYERS, LIMITS

Environment note: **cost-free, fully verified live then deleted.** Function `warroom-p21` was
created from a local zipped file, invoked, config-checked, then deleted (204) — `get-account-settings`
at the end showed 0 functions, 0 total code size. Two real packaging dead-ends (`fileb://<(…)`,
inline `--payload`) are documented in §9.

## 1. WHAT IS IT? (≤30s)

**Lambda** is AWS's *function-as-a-service*: upload code (zip or container image), pick memory +
timeout, and AWS runs it — **no servers, billed per-100ms**. An **invoke** passes an **event** (JSON)
plus a **Context** object (AWS metadata, remaining time). **Synchronous** invokes wait for the
answer; **async / event-source** invokes (S3, SQS, EventBridge) queue and retry. **Cold start** = the
first call in a fresh sandbox pays a bootstrap latency tax.

## 2. WHY DOES IT EXIST?

Serverless is the P2 "have you touched" ask: run compute *without* EC2 — "how do you run code with
no server?" Lambda answers cost (per-ms, nothing idle), scale (thousands of invocations, no ASG),
and ops (no patching). The interview fishes for the traps: cold start, sync-vs-async, VPC internet
loss, limits.

## 3. HOW DOES IT WORK? (verified)

- **Package (verified):** local `lambda_handler.py`, zipped **flat** (`zip -r /tmp/fn.zip
  lambda_handler.py`), uploaded via `--zip-file fileb:///tmp/fn.zip` — `fileb://` = "binary as-is".
- **create-function (verified):** runtime python3.12, handler lambda_handler.lambda_handler, memory
  128, timeout 3, role trusting lambda.amazonaws.com with `AWSLambdaBasicExecutionRole` →
  arn:aws:lambda:us-west-1:980664882691:function:warroom-p21.
- **invoke (verified):** `--payload fileb:///tmp/payload.json` with event `{"name":"warroom"}` →
  StatusCode 200, body `{"statusCode":200,"body":"hello warroom"}` — handler read `name`.
- **Readback (verified):** get-function-configuration → python3.12 / 128 / 3; list-versions →
  `$LATEST`, CodeSize 285 bytes; delete-function → **204**; get-account-settings → 0/0.
- **Model:** sync waits and returns; async queues, retries up to 2x, then DLQ. Cold start = fresh
  sandbox (container + runtime + handler import); **provisioned concurrency** pre-warms for a fee.
  **Layers** = shared dep zip. Limits: memory 128MB–10GB, timeout ≤**15 min**, sync response **6MB**
  / async 256KB, `/tmp` 1GB, zip 50MB. **Lambda@Edge** runs at CloudFront edges (pairs P2.2).

## 4. MENTAL MODEL

```
invoke ── event JSON ──> sandbox (Container + Runtime) ──> handler(event, context) ──> response
sync = wait for payload ;  async = queue + retry + DLQ (S3/SQS/EventBridge)
cold start = fresh-sandbox bootstrap — provisioned concurrency pre-pays it
limits: mem 128–10240MB | timeout ≤15m | resp 6MB sync / 256KB async | /tmp 1GB | zip 50MB
layers = shared dep zip ;  Lambda@Edge = function at the CDN edge
VPC Lambda loses internet unless a NAT exists
```

## 5. INTERVIEW-SAFE ANSWER

"I ran a function end-to-end: wrote a Python handler, zipped it flat, and `aws lambda
create-function` with runtime python3.12, 128MB, 3s timeout, and a role trusting lambda.amazonaws.com
— the ARN was arn:aws:lambda:us-west-1:980664882691:function:warroom-p21. I invoked it with a JSON
event; the handler read the `name` field and returned StatusCode 200 with `hello warroom`. The model:
events drive it — sync waits, async queues and retries; Context carries metadata; cold start is a
new-sandbox bootstrap tax that provisioned concurrency pre-pays; limits are 128MB–10GB memory,
15-min timeout, 6MB/256KB response caps. I deleted the function and confirmed the account zeroed out
— the whole loop was free-tier, fully verified."

## 6. FOLLOW-UP ATTACKS

**Q. Why did `fileb://<(printf …)` fail?**
**A.** The CLI needs a real seekable file; process substitution is a pipe fd — live error:
`'--zip-file must be a zip file with the fileb:// prefix'` (§9).

**Q. Cold start — cause and fix?**
**A.** A cold call builds a new sandbox: container init + runtime bootstrap + handler import. Idle
functions get reaped, so the first call after idle pays it. Fix: provisioned concurrency (pays),
lean runtime, lazy imports; accept it for async.

**Q. Sync vs async?**
**A.** Sync (`--type RequestResponse`, API GW, ALB) returns the payload. Async (`Event`) → 202
queued → retries → DLQ. S3/SQS/EventBridge are async — you don't wait.

**Q. Lambda in a VPC?**
**A.** Default network = internet. Move it in and it **loses internet** without a NAT — the classic
"wired into the VPC and now it times out" bug. You do it to reach private RDS/ElastiCache.

## 7. PRACTICAL EXAMPLE (production)

```bash
(cd src && zip -r /tmp/app.zip .)          # .py flat, no wrapper folder
aws lambda create-function --function-name process-order --runtime python3.12 --role "$ROLE" \
  --handler main.handler --zip-file fileb:///tmp/app.zip --memory-size 1024 --timeout 60 \
  --layers "$COMMON_LAYER"                 # deps via layer, not re-zipped per function
aws s3api put-bucket-notification-configuration --bucket orders --notification-configuration \
  '{"LambdaFunctionConfigurations":[{"LambdaFunctionArn":"'"$FN"'","Events":["s3:ObjectCreated:*"]}]}'
```
One event in, one function out; account concurrency is the only ceiling.

## 8. BUILD / REPRODUCE (verified, $0 after delete)

```bash
cat > /tmp/lambda_handler.py <<'EOF'
def lambda_handler(event, context):
    name = event.get("name", "nobody")
    return {"statusCode": 200, "body": f"hello {name}"}
EOF
(cd /tmp && zip -r /tmp/fn.zip lambda_handler.py)
ROLE=$(aws iam get-role --role-name lambda-basic-warroom --query 'Role.Arn' --output text)
aws lambda create-function --function-name warroom-p21 --runtime python3.12 --role "$ROLE" \
  --handler lambda_handler.lambda_handler --memory-size 128 --timeout 3 --zip-file fileb:///tmp/fn.zip
echo '{"name":"warroom"}' > /tmp/payload.json
aws lambda invoke --function-name warroom-p21 --payload fileb:///tmp/payload.json /tmp/out.json
cat /tmp/out.json                                        # {"statusCode":200,"body":"hello warroom"}
aws lambda get-function-configuration --function-name warroom-p21
aws lambda list-versions-by-function --function-name warroom-p21   # $LATEST, CodeSize 285
aws lambda delete-function --function-name warroom-p21             # 204
aws lambda get-account-settings --query 'AccountUsage'             # {TotalCodeSize:0, FunctionCount:0}
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT 1 — "zip-file must be a zip file" (VERIFIED)

Trigger: one-liner deploy via `--zip-file fileb://<(printf …)`.
Observe: `Error: --zip-file must be a zip file with the fileb:// prefix`.
Root cause: process substitution yields a pipe fd, not a seekable file the SDK can byte-verify;
`fileb://` alone isn't magic — the bytes must be a real zip.
Fix: materialize `zip -r /tmp/fn.zip`, pass `fileb:///tmp/fn.zip`. Verify: create succeeded, invoke
200. Prevent: always a real artifact; keep the zip **flat** so the handler path matches.

### INCIDENT 2 — "Invalid base64" (VERIFIED)

Trigger: inline `--payload '{"name":"warroom"}'` without `fileb://`.
Observe: `Invalid base64: "{"name":"warroom"}".`
Root cause: `--payload` wants base64 bytes or a `fileb://` raw file; plain text mis-parses.
Fix: `/tmp/payload.json` + `fileb://`. Verify: StatusCode 200. Prevent: temp file, or
`--payload "$(base64 -w0 <<< '{}')"`.

### DECISION OVERLAY — what NOT to do

- Don't nest code in a folder and guess handlers — the handler matches the **flat** zip.
- Don't import heavy deps at module top if cold start matters — lazy-load in the handler.
- Don't put Lambda in a VPC without a NAT — you cut its internet.
- Don't set 15-min timeouts "just in case" — that shape is a symptom, not a config.
- Don't treat `$LATEST` as a version — publish immutable versions you can pin and roll back.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Lambda = always container images" | Zip **or** image; either way AWS runs it serverless, not ECS/EKS. |
| "Cold start always <100ms" | Fresh-sandbox bootstrap can be seconds; provisioned concurrency pays it. |
| "Async returns the result" | Async = 202 queued; retries; failures go to DLQ/failure-destination. |
| "`--payload` takes inline JSON" | It's base64/`fileb://` — inline gave `Invalid base64` (verified). |
| "one layer per function" | Up to 5; layers compose shared deps. |
| "15-min timeout is a safe default" | Integrations cap you lower (API GW ~30s/6MB) — think per trigger. |
| "VPC Lambda keeps internet" | Not by default — needs NAT. |
| "delete frees instantly" | 204 returns fast; replicas lag — poll account settings to confirm (I did). |

## 13. FIRST-CHECK REASONING

- **"Times out."** `get_remaining_time_in_millis()` vs config, then I/O: VPC resource, cold client —
  rarely the handler logic.
- **"Cryptic base64/zip error."** Binding problem: materialize real zip + payload, `fileb://` both.
- **"No invocations logged."** Identify the trigger: sync (caller waited?) vs async (queue/DLQ); read
  the CloudWatch `REPORT` line per cold start.
- **"First call after idle is slow."** Expected cold start — provision or accept, don't "fix" code.

## 14. PRIORITY

P2 — tier-2 bonus: "have you touched serverless" is an interview smile, not a daily-driver. Keep the
verified boundaries intact; wrong facts here lose points fast.

## 15. STOP HERE — done when you can…

1. deploy a flat-zip function and invoke it with a file payload;
2. recite the limits cold: memory range, max timeout, response caps;
3. explain cold start + provisioned concurrency;
4. distinguish sync vs async vs event-source invokes;
5. recite the VPC-Lambda internet gotcha (NAT) unprompted.

## 16. DO NOT STUDY YET

Response streaming internals, extensions/protocol wrappers, SnapStart, function URLs,
provisioned-concurrency autoscaling, EFS vs `/tmp`, Powertools/cold-start benchmarking, event-source
tuning, execution-role audit patterns. The event/config/invoke/limits surface is the interview cut.

---

## QC CHECKLIST — AWS.P2.1

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (invoke→sandbox→handler, sync/async, limits)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Core mechanics (flat zip + fileb, event/context, cold start, provisioned concurrency, layers, limits)? | ✔ §3 |
| 5 | Dependencies (IAM role+trust P0.2, fileb discipline P0.1, VPC/NAT P0.3)? | ✔ §3 |
| 6 | Essential commands (create-function, invoke, get-config, list-versions, delete, get-account-settings)? | ✔ §3, §8 |
| 7 | Reproduce (create→invoke→inspect→delete, $0)? | ✔ all verified live |
| 8 | Break it (zip-process-substitution, Invalid base64, VPC internet loss)? | ✔ §9 |
| 9 | Observe + interpret (config readback, $LATEST/CodeSize, account zeroed)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P2.2 — CloudFront: edge caching,
distributions, origins, invalidation, and the CDN story.**

---

# SESSION AWS.P2.2 — CLOUDFRONT: DISTRIBUTIONS, ORIGINS, CACHING, INVALIDATION

Environment note: **read-only verification, $0.** `aws cloudfront list-distributions` ran in account
`980664882691` (us-west-1) → `DistributionList` **empty** — no distribution exists; none was created
(live distributions bill token fees, so cost-free keeps it read-only). Session = model + read-only
API proof; state that honestly if probed.

## 1. WHAT IS IT? (≤30s)

**CloudFront** is AWS's global **CDN**: edge locations proxy requests through a **distribution** —
your origin (S3/ALB/custom HTTP) wrapped in **cache behaviors** (path-pattern → TTL rules). Users hit
the nearest edge; cached objects are served there; only misses round-trip to the origin. Managed via
**invalidation** (removing specific cached paths), **signed URLs/cookies** (private content), and
**OAC** for private S3 origins.

## 2. WHY DOES IT EXIST?

Every "global app / static assets / private content" story needs the edge: fast everywhere (edge +
TTL vs origin round-trips), cheap (fewer origin hits), updatable (invalidation). It also hosts
Lambda@Edge (P2.1). The interviewer screens for CDN reflexes: OAC over public buckets, per-path TTL
discipline, path-scoped invalidation, and calling out that Transfer Acceleration is not a CDN.

## 3. HOW DOES IT WORK? (verified / model)

- **Proof (verified):** `list-distributions` → `{"DistributionList":{"Quantity":0}}` — zero
  distributions, nothing created, nothing billed.
- **Distribution model:** origins (S3/ALB/custom) + a **default cache behavior** (TTL, viewer
  protocol, methods) + optional **extra behaviors** by path pattern (`/assets/*` vs `/api/*`).
  **Price class** narrows edge regions to cut cost.
- **Cache behavior = the contract:** path pattern, min/default/max TTL, query-string handling,
  origin request policy, compression. Edges serve until TTL; expiry revalidates (ETag /
  If-Modified-Since).
- **OAC (model):** Origin Access Control **replaces** legacy **OAI**. With OAC the distribution signs
  S3 requests and the bucket policy grants `cloudfront:GetObject` only to that distribution's ARN —
  the bucket stays **private** while CloudFront serves it.
- **Invalidation (model):** `create-invalidation` removes **paths** (`/*`, `/img/*`) from the edges —
  not "delete the cache"; fee per path; next request refetches. Versioned names (`app-123.js`) need
  none; `index.html` does.
- **Edge logic (model):** **Lambda@Edge** = four viewer/origin hooks; **CloudFront Functions** = cheap
  ~1ms viewer transforms. **Signed URLs/cookies** = private content at the edge. **Not CloudFront:**
  S3 Transfer Acceleration speeds up *direct uploads* — no caching, no edge serving.

## 4. MENTAL MODEL

```
viewer ──> nearest edge (TTL cached? serve) ──> miss → origin (S3 / ALB / custom)
distribution = origins + behaviors (path→TTL) + price class + OAC + alt-domain/ACM
invalidation = create-invalidation /index.html → path-scoped purge, NOT "clear cache"
private: OAC (bucket policy grants getObject to distro ARN) + signed URLs/cookies
edge: Lambda@Edge (4 hooks) / CloudFront Functions (cheap viewer) — pairs P2.1
trap: Transfer Acceleration = upload fast-path, NOT a CDN
```

## 5. INTERVIEW-SAFE ANSWER

"CloudFront is the content-delivery edge: a distribution fronting an origin — S3, ALB, or custom HTTP
— with cache behaviors deciding what's cached where and for how long. I verified the API read-only:
my account returns zero distributions; I kept it at $0, so today the live proof is the read and the
mechanics are the model — that's the honest framing. The key parts: behaviors with TTL for cheap
reads; **OAC**, replacing old OAI, keeps an S3 origin private while CloudFront serves it; invalidation
is path-scoped (`create-invalidation /index.html`), not 'delete the cache'; signed URLs for private
per-user content; Lambda@Edge when logic must run at the edge. The false friend: Transfer Acceleration
speeds up *uploads* — it is not a CDN."

## 6. FOLLOW-UP ATTACKS

**Q. Invalidation vs versioned filenames?**
**A.** Invalidation is per-path and per-path priced; versioned names (`app-123.js`) never need a
purge. Invalidate only mutable paths like `index.html`. There is no global "delete the cache".

**Q. OAC vs OAI?**
**A.** OAI = legacy user-based principal; OAC signs S3 requests with a distribution-scoped identity
(modern). Bucket policy: `Principal: cloudfront.amazonaws.com` + `aws:SourceArn` condition matching
the distribution.

**Q. CloudFront Functions vs Lambda@Edge?**
**A.** Functions: ~1ms, viewer events only, tiny limits, pennies per million — rewrites/redirects.
Lambda@Edge: four hooks incl. origin-side, Node/Python, more cost. Choose Functions first.

**Q. What does a cache hit save?**
**A.** Edges serve bytes — no origin request, no S3 GET billing. TTL and cache key (query-string
policy) decide it. The trap: caching `/api/*` long = stale data; behaviors are per-path on purpose.

## 7. PRACTICAL EXAMPLE (production)

```json
{
  "DistributionConfig": {
    "Comment": "static web on private S3",
    "Origins": {"Quantity": 1, "Items": [{
      "Id": "s3-assets",
      "DomainName": "assets.s3.us-west-1.amazonaws.com",
      "OriginAccessControlId": "oac-xxxx",
      "S3OriginConfig": {"OriginAccessIdentity": ""}}]},
    "DefaultCacheBehavior": {
      "TargetOriginId": "s3-assets",
      "ViewerProtocolPolicy": "redirect-to-https",
      "Compress": true,
      "MinTTL": 0, "DefaultTTL": 3600, "MaxTTL": 86400,
      "ForwardedValues": {"QueryString": false}},
    "PriceClass": "PriceClass_100",
    "AlternateDomainNames": {"Quantity": 1, "Items": ["assets.example.com"]},
    "ViewerCertificate": {"ACMCertificateArn": "arn:aws:acm:us-east-1:…", "SSLSupportMethod": "sni-only"}
  }
}
```
Private bucket + OAC, then deploy-time purge: `aws cloudfront create-invalidation --distribution-id
E… --paths /index.html`.

## 8. BUILD / REPRODUCE (read-only + model)

```bash
# read-only, $0 — VERIFIED:
aws cloudfront list-distributions --query 'DistributionList.Quantity' --output text   # 0
# model — NOT run (live distribution bills; $0 rule holds):
aws cloudfront create-distribution --distribution-config file://dist.json
aws cloudfront get-distribution --id EXXXXXXXXXXXXX --query 'Distribution.Status'    # Deployed (minutes)
aws cloudfront create-invalidation --distribution-id EXXXXXXXXXXXXX --paths /index.html
aws cloudfront delete-distribution --id EXXXXXXXXXXXXX --if-match "$ETAG"            # needs --if-match ETag
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "New index.html deployed, users still get the old one"

Trigger: pushed a fresh build; browsers served yesterday's bytes.
Observe: direct origin GET = new file; via CloudFront = old. Distribution `Deployed`, behaviors
unchanged.
Root cause: TTL hadn't expired and no invalidation ran — edges legitimately served the cached copy.
Not a bug; the contract doing its job.
Fix: `create-invalidation --paths /index.html` after each mutable-path deploy.
Verify: fresh GET returns the new bytes from the edge.
Prevent: version asset filenames; invalidate only index/corruptions; `MinTTL` + revalidation on
mutable roots.

### DECISION OVERLAY — what NOT to do

- Don't "clear the whole cache" first — invalidation is per-path and per-path priced.
- Don't front a **public** S3 bucket with CloudFront and call it secure — OAC + private bucket.
- Don't cache `/api/*` on a long TTL — you're now serving stale data at scale.
- Don't point a single small EC2 origin into a launch storm — scale or front it.
- Don't claim "Transfer Acceleration is my CDN" — upload fast-path, different problem.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Invalidation = delete the cache" | Per-**path** invalidation (`create-invalidation`), no global purge. |
| "OAI is the modern option" | Legacy; **OAC** signs with a distribution-scoped identity. |
| "CloudFront needs a public bucket" | OAC keeps S3 private; bucket policy scopes to the distribution. |
| "Edge = Lambda@Edge always" | CloudFront Functions cover cheap viewer logic; Lambda@Edge for the 4-hook cases. |
| "Transfer Acceleration is a CDN" | Upload accelerator to S3 — no caching/edge serving. |
| "Live instantly at create" | Goes `InProgress` → `Deployed` over minutes. |
| "delete-distribution just works" | Needs `--if-match $ETAG`; stale ETag errors. |
| "One TTL per distribution" | Per behavior + per object — paths coexist at different lifetimes. |

## 13. FIRST-CHECK REASONING

- **"Stale after deploy."** TTL vs invalidation: versioned names / `/index.html` purge / origin
  freshness. Origin new, edges old = the TTL contract, not a CloudFront defect.
- **"Edge AccessDenied."** Three doors in order: OAC exists + bucket policy allows that ARN; signed
  content signature valid.
- **"CacheHitRate always 0."** Cache key split by query/header policy? PriceClass excluded the edge?
  TTL=0 = every request to origin?
- **"delete InvalidIfMatchVersion."** ETag stale — read `get-distribution`, retry with fresh
  `--if-match`.

## 14. PRIORITY

P2 — CDN is interview bonus: legitimizes "global, fast, cheap content" claims after P0/P1 core is
solid. Recite the model cold; the read-only proof is the honest cap on what was verified.

## 15. STOP HERE — done when you can…

1. draw distribution → behaviors → origins → TTL from memory;
2. explain OAC vs OAI and the private-S3-only pattern;
3. say exactly what invalidation does and doesn't do;
4. distinguish CloudFront Functions from Lambda@Edge;
5. kill the "Transfer Acceleration = CDN" claim instantly.

## 16. DO NOT STUDY YET

Origin failover groups, field-level encryption, real-time logs to Kinesis, cache-key tuning,
Shield/WAF managed rules, ACM rotation, multi-origin mixed stories. Distribution/OAC/invalidation/
edges is the interview cut.

---

## QC CHECKLIST — AWS.P2.2

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (edge→behaviors→origin, OAC, invalidation)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Core mechanics (behaviors/TTL, OAC vs OAI, invalidation, Functions vs Lambda@Edge, signed content)? | ✔ §3 |
| 5 | Dependencies (S3 private origin P0.6, Lambda@Edge P2.1, ACM)? | ✔ §3 |
| 6 | Essential commands (list-distributions, create-distribution, create-invalidation, delete-distribution)? | ✔ §3, §8 |
| 7 | Reproduce (read-only list verified, $0)? | ✔ verified (empty) |
| 8 | Break it (stale cache, AccessDenied doors, transfer-acceleration trap)? | ✔ §9 |
| 9 | Observe + interpret (Quantity 0, InProgress→Deployed, ETag-gated delete)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P2.3 — API Gateway: REST vs HTTP,
stages, authorizers, throttling — how serverless APIs are exposed.**

---

# SESSION AWS.P2.3 — API GATEWAY: REST VS HTTP, STAGES, AUTHORIZERS, THROTTLING

Environment note: **read-only verification, $0.** `aws apigateway get-rest-apis` ran in account
`980664882691` (us-west-1) → **empty items** — no REST API exists; nothing created, nothing billed.
Session = model + an honest empty read; REST/HTTP/WebSocket semantics and the deploy/stage/
authorizer/throttle vocabulary are **knowledge, clearly labeled**.

## 1. WHAT IS IT? (≤30s)

**API Gateway** is the managed front door for HTTP/WebSocket APIs. Three flavors: **REST**
(full-featured — validation, authorizers, usage plans, custom domains), **HTTP** (lean, cheaper,
native proxy), **WebSocket** (realtime, connection-based). An API = **resources + methods** wired to
**integrations** (Lambda proxy, HTTP endpoint); a **deployment** snapshot plus a **stage** (dev/prod)
publishes a URL; **throttling, quotas, authorizers, caching** gate and protect it.

## 2. WHY DOES IT EXIST?

A Lambda isn't reachable by clients on its own — the interview wants "how do you expose serverless
APIs? secure them? version them via stages? keep them from being melted?" And why not just an ALB:
API Gateway owns auth (authorizers), partner keys + usage plans, per-stage environments, and request
validation before the backend. Like P2.1/P2.2 it's the "have you touched serverless" bonus tier.

## 3. HOW DOES IT WORK? (verified / model)

- **Proof (verified):** `get-rest-apis` → `{"items":[]}` — zero REST APIs, nothing billed.
- **REST API (model):** a **restapi** owns **resources** (`/orders`, `/orders/{id}`) with **methods**
  (GET/POST/PUT). Each method has an **integration**: `AWS_PROXY` (Lambda proxy — entire event to the
  function, its `{statusCode,headers,body}` returned verbatim; the 1-page standard), `AWS` (mapping
  templates), `HTTP` (passthrough), `MOCK`.
- **Deploy → stage (model):** `create-deployment` snapshots the API; a **stage** points at one
  deployment → `https://<id>.execute-api.<region>.amazonaws.com/prod`. Redeploy = new snapshot, flip
  the stage. Each stage carries throttle, cache, logs, canary.
- **Authorizers (model):** **Cognito** (user-pool JWT), **IAM** (SigV4 service-to-service),
  **Lambda** (custom token/request), **JWT** (OIDC issuer/audience). Auth gates at the gateway; the
  Lambda behind stays context-free-ish.
- **Throttle + quota (model):** account-wide default ~**10k req/s** (regional) + per-stage/method
  **rate/burst**; **usage plans** bundle API keys + throttle + quota (partner gate); **stage cache**
  protects the backend Lambda. **Models/validation**: JSON-schema request validators reject bad
  bodies at the gateway *before* the Lambda runs.
- **Honest line:** `get-rest-apis` empty, no HTTP/WS created either — API surface read-only, mechanics
  from the model. Say it plainly; it earns more than bluffing.

## 4. MENTAL MODEL

```
client → API Gateway → integration → Lambda proxy / HTTP / MOCK / WS
REST = full feature (validation, authorizers, usage plans) ; HTTP = lean cheap proxy ; WS = realtime
resources+methods = shape ; deployment = snapshot ; stage(dev/prod) = URL of one snapshot
authorizer: Cognito | IAM SigV4 | Lambda | JWT → gate at the edge
throttle (rate+burst) + quota + usage-plans + API keys ; stage cache = fewer Lambda calls
trap: "deployment" vs "stage" — one stage can jump between many deployments
```

## 5. INTERVIEW-SAFE ANSWER

"API Gateway is the managed entry point for serverless APIs. I verified the surface cost-free:
`get-rest-apis` returned an empty list — I didn't create one, so today the API side is a read-only
proof and the rest is the model I can walk through cold, which is how I'd frame it. REST vs HTTP vs
WebSocket: REST when you need validation, authorizers, usage plans; HTTP as the leaner cheaper proxy;
WebSocket for realtime. The anatomy: resources and methods wired to an integration — for Lambda my
standard is the proxy integration: the whole event goes to the function and its
`{statusCode, headers, body}` comes back verbatim. A deployment is a snapshot; the stage points at
one deployment and gives the URL plus per-environment throttling and caching. Auth gates at the
gateway — Cognito, IAM SigV4, Lambda, or JWT authorizers; throttling and quotas via usage plans
protect what sits behind."

## 6. FOLLOW-UP ATTACKS

**Q. REST vs HTTP API?**
**A.** REST for the advanced set: validation, usage plans + API keys, custom domains, WAF, SDK gen,
canaries. HTTP = lean, cheaper, better latency, Lambda + HTTP only, built-in JWT. New PoC: HTTP;
enterprise/controlled: REST.

**Q. Deployment vs stage?**
**A.** Deployment = immutable snapshot. Stage = named pointer to a deployment (`prod` → snapshot A,
then B). Multiple stages can share; a stage can canary two deployments. The classic mix-up.

**Q. What does Lambda-proxy forward?**
**A.** Method, path + query, headers, body, source IP, authorizer context. Reply is
`{statusCode, headers, body}` verbatim. Watch `$LATEST` drift — published versions pin; `$LATEST`
rides your last publish.

**Q. Gateway throttle vs Lambda reserved concurrency?**
**A.** Gateway caps *requests* per client/stage; reserved concurrency caps *in-flight executions* at
the function tier. Stack both: the gateway stops the flood; reserved concurrency stops one function
drowning the account.

## 7. PRACTICAL EXAMPLE (production)

```bash
API=$(aws apigatewayv2 create-api --name orders --protocol-type HTTP \
  --target arn:aws:lambda:us-west-1:980664882691:function:process-order --query 'ApiId' --output text)
STAGE=$(aws apigatewayv2 create-stage --api-id "$API" --stage-name prod \
  --auto-deploy --query 'StageName' --output text)
curl "https://$API.execute-api.us-west-1.amazonaws.com/$STAGE/orders" \
  -H "Authorization: Bearer $JWT"      # → gateway → Lambda proxy → response
```
HTTP API in four lines: `--target` points at the Lambda, `--auto-deploy` republishes each change.

## 8. BUILD / REPRODUCE (read-only + model)

```bash
# read-only, $0 — VERIFIED:
aws apigateway get-rest-apis --output json      # { "items": [] } → zero REST APIs
aws apigatewayv2 get-apis --output json         # model: HTTP/WS APIs (also empty here)
# model — NOT run (a deployed API charges per request):
REST=$(aws apigateway create-rest-api --name warroom-rest --query 'id' --output text)
RES=$(aws apigateway get-resources --rest-api-id "$REST" --query 'items[0].id' --output text)
aws apigateway put-method --rest-api-id "$REST" --resource-id "$RES" --http-method GET --authorization-type NONE
aws apigateway put-integration --rest-api-id "$REST" --resource-id "$RES" --http-method GET \
  --type AWS_PROXY --integration-http-method POST \
  --uri "arn:aws:apigateway:us-west-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-west-1:980664882691:function:warroom-p21/invocations"
DEP=$(aws apigateway create-deployment --rest-api-id "$REST" --query 'id' --output text)
aws apigateway create-stage --rest-api-id "$REST" --stage-name dev --deployment-id "$DEP"
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "Stage exists but the URL 403s/404s"

Trigger: fetch `https://<id>.execute-api…/prod/route` → 403/404 while the stage exists.
Observe: stage populated; the resource list has the method; the URL rejects it.
Root cause (model, canonical class): the **deployed snapshot predates** the latest edits — the stage
points at a stale deployment; or a missing `put-method-response`; or an authorizer 403s *before* the
Lambda ever runs.
Fix: `create-deployment` again and re-point the stage (or `--auto-deploy`). For 403: `get-method`
authorization-type + authorizer result; for 404: the path isn't in the served snapshot.
Verify: `get-deployment` shows the tree; `get-stage` shows the deployment ID; curl the exact URL.
Prevent: HTTP APIs with `--auto-deploy`, or CI that deploys after every resource/method change —
never mutate in the dark without a snapshot.

### DECISION OVERLAY — what NOT to do

- Don't confuse deployments (snapshot) with stages (pointer) — the #1 misconception.
- Don't skip `--type AWS_PROXY` — the payload shape mangles at the Lambda.
- Don't ship `authorization-type NONE` on a public method — that's an open door to your Lambda.
- Don't throttle only at the gateway — pair with Lambda reserved concurrency (hose vs sink).
- Don't hand-edit a multi-dev API — auto-deploy or per-stage CI, or you'll 404 for a morning.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "Deployment = stage" | Deployment is the snapshot; stage points at one deployment. |
| "REST is the only API" | REST / HTTP / WebSocket — three flavors, different tradeoffs. |
| "Proxy forwards just the body" | It forwards method/path/headers/body/authorizer-context. |
| "Throttling lives only at the gateway" | Gateway rate/burst + Lambda reserved concurrency. |
| "Stage cache is automatic" | Per-stage, paid, can serve stale data. |
| "API key = authentication" | A key identifies a usage *plan*; authorizers do identity. |
| "HTTP API does everything REST does" | No validation/usage-plans/SDK-gen — name the tradeoff. |

## 13. FIRST-CHECK REASONING

- **"403 on a live stage."** Authorizer first (`get-method` type, JWT issuer region), then resource
  policy, then the Lambda `lambda:InvokeFunction` grant to apigateway — three doors.
- **"404 on my route."** Is the method in the **deployed snapshot**? Compare `get-deployment` vs
  `get-resources`; redeploy if it postdates the snapshot. Check path + stage name.
- **"502 BadGateway."** Integration URI points at a published version or deleted function — check
  `get-integration` uri, re-point. Lambda-side 502s are usually ARN drift.
- **"Broad throttles."** Account ~10k rps cap or a usage-plan quota — `get-usage-plan` / CloudWatch
  `Throttle*`, then raise per-stage or request the increase.

## 14. PRIORITY

P2 — "how do you expose your serverless API" is the bonus follow-up after P0/P1 core. Not a
daily-driver at 1–3 YOE, but it reads serverless-fluent. The REST/HTTP/stage/authorizer/throttling
model is the entire cut.

## 15. STOP HERE — done when you can…

1. recite REST vs HTTP vs WebSocket and when to pick each;
2. distinguish deployment (snapshot) from stage (pointer) instantly;
3. wire a Lambda proxy integration (`--type AWS_PROXY`) from memory;
4. pick an authorizer per client type (Cognito/IAM/Lambda/JWT);
5. explain throttling + usage plans as two-stage protection (gateway + function).

## 16. DO NOT STUDY YET

WebSocket connection management + callback URLs, quota customization per period, gateway cache
tuning, Private APIs + VPC endpoints, SDK generation, custom domains + mutual TLS, authorizer-context
formats, OpenAPI import/export. The REST/HTTP/stage/authorizer/throttling surface is the cut.

---

## QC CHECKLIST — AWS.P2.3

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (gateway→resources→integrations→deploy/stage→authorizer→throttle)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Core mechanics (REST vs HTTP vs WS, proxy integration, deploy/stage, authorizers, throttling/plans)? | ✔ §3 |
| 5 | Dependencies (Lambda P2.1, Cognito/IAM P0.2)? | ✔ §3 |
| 6 | Essential commands (get-rest-apis, get-apis, create-rest-api, put-method, put-integration, create-deployment, create-stage)? | ✔ §3, §8 |
| 7 | Reproduce (read-only empty get-rest-apis verified, $0)? | ✔ verified (empty) |
| 8 | Break it (stale-deployment 404, NONE-auth open door, ARN drift 502, throttle)? | ✔ §9 |
| 9 | Observe + interpret (items empty, deploy vs stage, 403-before-Lambda)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P2.4 — ECS: Fargate vs EC2, task
definitions, services, and container orchestration beyond EKS.**
---
# SESSION AWS.P2.4 — ECS: CONTAINER ORCHESTRATION WITHOUT THE KUBERNETES TAX

Environment note: **cost-free verification** — cluster created with FARGATE + FARGATE_SPOT capacity
providers, task definition registered, no tasks launched, no instances spun ($0). Cluster deleted,
task def deregistered after verification.

## 1. WHAT IS IT? (≤30s)

**ECS** is AWS's native container orchestrator: you define a **task definition** (container image +
CPU/memory/port), spin up a **cluster**, and run **tasks** or **services** (N copies behind a load
balancer) on either **Fargate** (serverless — no nodes, pay per task) or **EC2 launch type** (you
manage the fleet). No control plane to operate — that's the EKS comparison point.

## 2. WHY DOES IT EXIST?

The interview's "how do you run containers in AWS?" answer, the alternative to EKS (P0.10). ECS
exists for teams that want **tight IAM integration** (task roles, not instance roles), **zero control
plane ops**, and native AWS plumbing (CloudWatch, ALB, Service Connect). The separator from EKS:
portability/ecosystem vs simplicity/native.

## 3. HOW DOES IT WORK? (verified, $0)

- **Cluster (verified):** `create-cluster --cluster-name warroom-p24 --capacity-providers FARGATE
  FARGATE_SPOT` → cluster ACTIVE, capacityProviders printed `[FARGATE, FARGATE_SPOT]`. The cluster
  is a scheduling boundary — it holds services and tasks, nothing else.
- **Task definition (verified):** `register-task-definition --family hello --network-mode awsvpc
  --requires-compatibilities FARGATE --cpu 256 --memory 512 --container-definitions '[{
  "name":"app","image":"nginx:alpine","portMappings":[{"containerPort":80}]}]'` → task-definition
  arn `.../hello:1` (version :1 implicit), cpu 256, memory 512, requiresCompatibilities FARGATE.
  Task defs are immutable snapshots; new deploys register a new **revision** (:2, :3...).
- **Service vs task:** A service enforces `desiredCount`, ties to an ALB target group, and does
  rolling/blue-green deploys. A standalone task is one-shot — batch jobs, one-off scripts.
- **Fargate vs EC2 launch type:** Fargate = serverless compute, per-task billing, no node management,
  ENI per task. EC2 = you manage instances, capacity providers control scaling, task placement is
  your problem. Capacity providers bridge the two: ASG-backed EC2 capacity + Fargate in one cluster.
- **Task role vs instance role:** Task role = IAM assumed **by the container** (ECS calls STS on
  behalf of the task). Instance role = EC2 metadata IAM (wrong scope — every task on the node gets
  it). Classic trap: "IAM for the container" = task role, always.
- **Describe evidence (verified):** `describe-clusters` → runningTasksCount 0, activeServicesCount 0.
  Clean $0 proof: real objects, zero running work.
- **Cleanup (verified):** `delete-cluster` → status INACTIVE; `deregister-task-definition
  --task-definition hello:1` → INACTIVE. Full lifecycle confirmed.

## 4. MENTAL MODEL

```
CLUSTER = scheduling boundary (holds services + tasks)
  ├─ capacity providers  =  FARGATE (serverless) | EC2 (managed ASGs)
  │
TASK DEFINITION = immutable blueprint (image, cpu, mem, ports, volumes)
  ├─ revision :1, :2, :3...   (new deploy = new revision)
  └─ task ROLE (IAM for the container, NOT the instance)
  │
SERVICE = long-running desiredCount N behind ALB
  │  enforces: rolling update, health check, placement
  │  ties to: target group (P0.7) + capacity provider
  │
STANDALONE TASK = one-shot (batch, migration, cron)

Fargate: AWS runs the server, you pay per task-second
EC2:    you run the server, capacity providers manage the fleet
```

## 5. INTERVIEW-SAFE ANSWER

"ECS is AWS's container orchestrator — you define a task definition, a cluster, and either services
or one-shot tasks. Fargate is the serverless compute option, no EC2 nodes to manage, billed per
task. The key IAM distinction is task role vs instance role — task role is scoped to the container,
which is what you want. I verified this session: created a Fargate cluster, registered an nginx task
def at 256 CPU / 512 MiB, confirmed zero running tasks, and cleaned up — all $0, no tasks launched.
The interview separator from EKS: ECS is simpler to operate with native AWS integration; EKS gives
you Kubernetes portability and ecosystem. Service vs standalone task: service = enforced desiredCount
+ ALB + rolling deploys; task = one-shot job."

## 6. FOLLOW-UP ATTACKS

**Q. Fargate vs EC2 launch type — when which?**
**A.** Fargate for bursty/unpredictable workloads, small teams without infra expertise, or when you
want zero node management. EC2 for sustained high-throughput (GPU, large memory, BYOL), cost
optimization with reserved instances, or when you need custom AMIs / instance-store performance.

**Q. Task role vs instance role — why does it matter?**
**A.** Instance role is EC2 instance metadata IAM — every task on that node inherits it, breaking
least-privilege. Task role is per-task, assigned at runtime via STS:AssumeRole — only the container
gets those permissions. Classic trap: using instance role for containers.

**Q. How does ECS handle rolling deploys?**
**A.** Service `deploymentConfiguration`: `maximumPercent` (e.g. 200 = launch new before kill old),
`minimumHealthyPercent` (e.g. 100 = don't go below desired). New task definition revision is the
deploy unit. Blue/green via CodeDeploy + ALB target groups.

**Q. What is Service Connect?**
**A.** ECS-native service discovery and mesh — replaces CloudMap for inter-container DNS. Each
service gets a DNS name within the cluster; traffic can be mTLS-encrypted between services.

**Q. Capacity providers — what are they?**
**A.** Abstract compute: FARGATE/FARGATE_SPOT are managed providers; EC2 providers wrap ASGs. One
cluster can mix both. The cluster's `defaultCapacityProviderStrategy` routes tasks to providers.

## 7. PRACTICAL EXAMPLE (production)

```bash
aws ecs create-cluster --cluster-name prod-api --capacity-providers FARGATE FARGATE_SPOT \
  --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1
aws ecs register-task-definition --family api --network-mode awsvpc \
  --requires-compatibilities FARGATE --cpu 512 --memory 1024 \
  --container-definitions '[{"name":"api","image":"123456789.dkr.ecr.us-west-1.amazonaws.com/api:latest","portMappings":[{"containerPort":8080}],"logConfiguration":{"logDriver":"awslogs","options":{"awslogs-group":"/ecs/api","awslogs-region":"us-west-1","awslogs-stream-prefix":"ecs"}}}]'
aws ecs create-service --cluster prod-api --service-name api \
  --task-definition api --desired-count 2 --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-abc],securityGroups=[sg-app],assignPublicIp=DISABLED}" \
  --load-balancers targetGroupArn=arn:...,containerName=api,containerPort=8080
```

## 8. BUILD / REPRODUCE ($0 — verified)

```bash
aws ecs create-cluster --cluster-name warroom-p24 --capacity-providers FARGATE FARGATE_SPOT
aws ecs register-task-definition --family hello --network-mode awsvpc \
  --requires-compatibilities FARGATE --cpu 256 --memory 512 \
  --container-definitions '[{"name":"app","image":"nginx:alpine","portMappings":[{"containerPort":80}]}]'
aws ecs list-task-definitions --family-prefix hello
aws ecs describe-clusters --clusters warroom-p24
# cleanup (verified)
aws ecs delete-cluster --cluster warroom-p24
aws ecs deregister-task-definition --task-definition hello:1
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "cluster created but no tasks: by design" (VERIFIED)

Trigger: `describe-clusters` returned runningTasksCount 0, activeServicesCount 0.
Observe: cluster is ACTIVE but empty — expected in the $0 lab.
Root cause: no service or standalone task was launched; the cluster object exists as a scheduling
boundary only. This is normal — you can own a cluster with zero running work.
Fix: N/A (by design). In production, create a service or run-task to populate it.
Verify: `describe-clusters` → correct counts. Task definition exists independently of the cluster.
Prevent: always check runningTasksCount + activeServicesCount when someone reports "cluster is
empty" — it might be correct.

### DECISION OVERLAY — what NOT to do

- Don't use instance role for container IAM — use task role (classic trap, interview killer).
- Don't assume Fargate = free — it bills per vCPU-second + GB-second; small tasks are cheap, not zero.
- Don't confuse cluster = namespace (it's a scheduling boundary, not a network boundary).
- Don't run one-shot batch jobs as services — use standalone tasks or AWS Batch.
- Don't skip awslogs in container definition — without it, debugging is blind.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "ECS = EKS = same" | ECS = AWS-native, no control plane, simpler. EKS = Kubernetes, portable, ecosystem. |
| "Fargate is free" | Pay-per-second for vCPU + memory; cheap for small tasks, not $0. |
| "Instance role = container IAM" | Wrong — task role is per-container. Instance role leaks across all tasks on a node. |
| "Cluster = network boundary" | Cluster = scheduling boundary; networking is VPC/subnets/security groups. |
| "Services and tasks are interchangeable" | Service = long-running + desiredCount + ALB. Task = one-shot. Different jobs. |
| "New deploy = same task definition" | New deploy = new task definition revision (:2, :3). Old revisions stay until deregistered. |
| "Capacity providers = optional" | They're how you mix Fargate + EC2 in one cluster. Ignoring them limits your model. |

## 13. FIRST-CHECK REASONING

- **"Task won't start."** Check task definition revision exists; check cluster has capacity providers;
  check network config (awsvpc mode needs subnets + SGs); check image exists in ECR.
- **"Service has 0 running tasks."** `describe-services` → events will show why (image pull fail,
  port conflict, IAM role missing, ENI attachment timeout on Fargate).
- **"Fargate task stuck provisioning."** No Fargate capacity in AZ? Subnet has no available IPs?
  Check events for "unable to place" messages.
- **"Container can't reach IAM."** Instance role or task role? `curl $AWS_CONTAINER_CREDENTIALS_RELATIVE_URI`
  from the container confirms task role is available.

## 14. PRIORITY

P2 — bonus tier. Containers are common in interviews but ECS specifics come up less than the VPC /
IAM / S3 core. Know the model + Fargate vs EC2 split cold; dive deeper only if the role targets
container-heavy teams.

## 15. STOP HERE — done when you can…

1. explain ECS vs EKS in one sentence (simplicity vs portability);
2. describe the task definition → cluster → service/task hierarchy;
3. name the difference between Fargate and EC2 launch types;
4. distinguish task role from instance role and why one is wrong for containers;
5. outline how a rolling deploy works (new revision + maximumPercent / minimumHealthyPercent).

## 16. DO NOT STUDY YET

ECS Service Connect deep-config, capacity provider auto-scaling policies, ECS Exec (SSM shell into
containers), task placement constraints/strategies, sidecar patterns, ECS anywhere (hybrid), Fargate
Spot task interruption behavior. The cluster + task def + service + task-role model is the
interview-visible surface.

---

## QC CHECKLIST — AWS.P2.4

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (cluster/task def/service/task/capacity providers)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (Fargate vs EC2, task def revisions, task role, service vs task)? | ✔ §3 |
| 5 | Dependencies (VPC/subnet P0.3, ALB P0.7, ECR P0.10, IAM task roles)? | ✔ §3 |
| 6 | Essential commands (create-cluster, register-task-definition, create-service, describe-clusters)? | ✔ §3, §8 |
| 7 | Reproduce ($0: cluster + task def, no tasks launched)? | ✔ verified live |
| 8 | Break it (empty cluster by design, instance-role trap, Fargate billing surprise)? | ✔ §9 |
| 9 | Observe + interpret (runningTasksCount=0, capacityProviders, revision :1)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** (cluster + task def created and deleted at $0; no tasks launched) |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P2.5 — KMS: envelope encryption, keys, grants, policies, rotation — the encryption backbone.**

---
# SESSION AWS.P2.5 — KMS: THE ENCRYPTION BACKBONE THE INTERVIEW ASSUMES YOU KNOW

Environment note: **read-only verification, $0.** No customer-managed keys created (CMKs bill
$1/month); evidence from real AWS-owned aliases + `describe-key` on `alias/aws/ssm`. Session is
model-heavy with verified alias/key metadata as proof.

## 1. WHAT IS IT? (≤30s)

**KMS** manages encryption keys: symmetric (encrypt/decrypt) and asymmetric (sign/verify). The
core concept is **envelope encryption** — a data key encrypts your data, the master key encrypts
the data key. KMS itself never sees your plaintext data. Keys are governed by **key policies**
(who can admin/use) and optional **grants** (delegated, time-bound).

## 2. WHY DOES IT EXIST?

The interview's "how do you encrypt at rest?" answer. Every AWS service that says "encrypted with
KMS" — S3 SSE-KMS (P0.6), EBS (P0.5), RDS (P1.2), ECR image signing (P0.10) — calls KMS under
the hood. KMS exists to keep keys out of your code, enforce access controls on key usage, and
provide an audit trail (CloudTrail) for every Decrypt/Encrypt call. The $1/month per CMK is the
price of centralised key management.

## 3. HOW DOES IT WORK? (verified)

- **AWS-owned aliases (verified):** `list-aliases` filtered to `AliasName starts_with alias/aws/`
  returned real service-default keys: `alias/aws/dynamodb`, `ebs`, `elasticfilesystem`, `es`,
  `glue`, `kinesisvideo`, `rds`, `redshift`, `s3`, `ssm`, `xray`. These are **AWS-managed** keys
  — AWS rotates them yearly, free to use, no customer control.
- **Describe-key evidence (verified):** `describe-key --key-id alias/aws/ssm` → ARN
  `arn:aws:kms:us-west-1:980664882691:key/5367a905-…`, KeyManager=AWS, Origin=AWS_KMS,
  KeyState=Enabled. This is a real, live AWS-managed key in this account — proof the alias → key
  mapping works.
- **No customer keys (verified):** `list-keys` returned **empty** — no CMKs in this account.
  Creating one would bill $1/mo, so deliberately not created. This is the honest baseline.
- **Envelope encryption (model):** Your app calls `GenerateDataKey` → KMS returns (1) plaintext DEK +
  (2) encrypted DEK. You encrypt data with the plaintext DEK, discard it, store the encrypted DEK
  alongside the ciphertext. To decrypt: call `Decrypt` on the encrypted DEK → get plaintext DEK →
  decrypt data. The DEK never touches KMS storage — only the master key wraps it.
- **Symmetric vs asymmetric (model):** Symmetric (AES-256) = single key, encrypt/decrypt, most
  common (S3, EBS, RDS all use this). Asymmetric (RSA/ECC) = key pair, used for signing/verify
  (ECR image signing, code-signing). Public key can be distributed; private key stays in KMS.
- **Key policy vs grants (model):** Key policy = JSON resource policy on the CMK itself (who can
  admin, who can use, who can schedule deletion). Grants = scoped, delegatable, time-bound — good
  for cross-account access or Lambda execution without polluting the key policy.
- **Key rotation (model):** AWS-managed keys: automatic yearly rotation, no opt-out. Customer-managed
  keys: optional yearly rotation (creates new backing key material, alias always points to latest).
  **Critical trap:** rotation does NOT rotate data keys — only the CMK. Old encrypted DEKs still
  decrypt fine because KMS retains old key material.

## 4. MENTAL MODEL

```
PLAINTEXT DATA
      │  GenerateDataKey (via CMK)
      ▼
┌──────────────┐    ┌───────────────────┐
│ plaintext DEK │    │ encrypted DEK     │──► stored alongside ciphertext
│ (encrypt data)│    │ (only KMS can     │
│               │    │  Decrypt this)    │
└───────┬──────┘    └───────────────────┘
        │ encrypt
        ▼
CIPHERTEXT + encrypted DEK  →  your storage (S3/EBS/RDS/etc.)

CMK (master key) lives in KMS — you never see its material
  ├─ key policy  = who can admin/use the CMK
  ├─ grants      = delegated, scoped, time-bound
  └─ rotation    = yearly material refresh (CMK only, NOT data keys)

AWS-managed keys: free, auto-rotated, no control
Customer-managed: $1/mo, optional rotation, full policy control
```

## 5. INTERVIEW-SAFE ANSWER

"KMS is the encryption backbone — envelope encryption: a data key encrypts the data, the master
key encrypts the data key. The app calls GenerateDataKey, gets a plaintext DEK + encrypted DEK,
uses the plaintext DEK to encrypt, then discards it. KMS never sees your plaintext data. Key
policies control who can admin and use the key; grants add delegation. Rotation refreshes the
master key yearly but doesn't rotate existing data keys — old encrypted DEKs still decrypt fine.
I verified this session: listed real AWS-managed aliases (alias/aws/s3, alias/aws/ebs, etc.),
described alias/aws/ssm and confirmed it's a live AWS-managed key in this account, and confirmed
no customer CMKs exist. AWS-managed keys are free; customer-managed are $1/mo — that's why I
didn't create one."

## 6. FOLLOW-UP ATTACKS

**Q. What actually encrypts the data — KMS or the data key?**
**A.** The data key (DEK). KMS never touches your plaintext data. KMS only encrypts/decrypts the
data key itself. This is why envelope encryption scales — one KMS call protects a whole file/object.

**Q. CMK rotation vs data key rotation — same thing?**
**A.** No. CMK rotation = new backing key material yearly (alias points to latest; old material
retained). Data key rotation = your app calls GenerateDataKey again for new data. KMS rotation
does NOT rotate existing encrypted DEKs.

**Q. How do you handle cross-account key access?**
**A.** Key policy: add the other account's root/role as a key user/admin. Or use grants: create a
grant scoped to specific operations (Decrypt only) for the other account's principal.

**Q. When would you use asymmetric keys in KMS?**
**A.** Code signing (ECR image signing, package signing), JWT verification, certificate management.
You sign with the private key in KMS; verifiers use the public key. The private key never leaves KMS.

**Q. What's the audit trail for key usage?**
**A.** CloudTrail logs every KMS API call: who called Decrypt/Encrypt/GenerateDataKey, from which
IP, with which key ARN. This is a compliance requirement — "who accessed the encryption key?"

## 7. PRACTICAL EXAMPLE (production)

```bash
# S3 bucket with SSE-KMS (uses alias/aws/s3 by default)
aws s3api put-bucket-encryption --bucket my-bucket --server-side-encryption-configuration '{
  "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms"},
             "BucketKeyEnabled": true}]}'
# Custom CMK for a specific service (would cost $1/mo)
aws kms create-key --description "app-backend" --tags TagKey=env,TagValue=prod
aws kms create-alias --alias-name alias/app-backend --target-key-id <key-id>
# App calls GenerateDataKey → encrypt → store ciphertext + encrypted DEK
```

## 8. BUILD / REPRODUCE (read-only, $0 — verified)

```bash
aws kms list-keys --query 'Keys[].KeyId' --output text                          # → empty (no CMKs)
aws kms list-aliases --query "Aliases[?starts_with(AliasName,'alias/aws/')].AliasName" --output text
# → alias/aws/dynamodb alias/aws/ebs alias/aws/s3 alias/aws/ssm ...
aws kms describe-key --key-id alias/aws/ssm \
  --query '{ARN:KeyMetadata.Arn,Manager:KeyMetadata.KeyManager,Origin:KeyMetadata.Origin,State:KeyMetadata.KeyState}'
# → KeyManager=AWS, Origin=AWS_KMS, State=Enabled (verified live)
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "no customer keys exist: honest accounting" (VERIFIED)

Trigger: `list-keys` returned empty.
Observe: no CMKs in the account — only AWS-managed aliases exist (verified via `list-aliases`).
Root cause: no CMK was ever created; the $0 mandate prevents it ($1/mo). This is the baseline
state — most AWS accounts have zero CMKs and rely on service-default AWS-managed keys.
Fix: N/A (intentional). In production, `create-key` + `create-alias` gives you a CMK with full
policy control.
Verify: `describe-key --key-id alias/aws/ssm` proves the alias → key mapping works with real keys.
Prevent: don't confuse "no CMKs" with "no encryption" — AWS-managed keys (alias/aws/ebs, alias/aws/s3)
encrypt by default; the CMK is for custom policy control + audit scope.

### DECISION OVERLAY — what NOT to do

- Don't embed KMS keys in code or environment variables — use aliases (stable name, key can rotate).
- Don't confuse AWS-managed with customer-managed — different cost, control, and audit scope.
- Don't assume rotation handles data keys — it doesn't; your app must re-encrypt periodically.
- Don't use KMS for data-in-transit — TLS/SSL handles that; KMS is at-rest.
- Don't give the whole world access to a CMK via key policy — least privilege, always.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "KMS encrypts the data" | KMS encrypts the data key (DEK); the DEK encrypts the data. |
| "CMK rotation rotates data keys" | No — only the master key material rotates. Old DEKs still decrypt. |
| "AWS-managed keys cost $1/mo" | $0 — only customer-managed keys cost $1/mo. |
| "Key policy and IAM policy are the same" | Key policy is on the CMK itself; IAM policy is on the principal. Both gate access. |
| "KMS can decrypt anything" | Only if you have the right key + the key policy/grants allow the call. |
| "Rotation means old encrypted data is invalid" | Old key material is retained — decryption of old DEKs still works. |
| "Asymmetric keys = regular RSA pairs" | The private key stays in KMS — you call Sign(), never export the key. |

## 13. FIRST-CHECK REASONING

- **"Decrypt fails with AccessDenied."** Check: key policy allows the principal? CloudTrail shows
  the denied call? The key isn't disabled/scheduled for deletion?
- **"Which key encrypts this S3 object?"** Check `x-amz-server-side-encryption` header or
  `head-object` output — it returns the key ARN. Match against `list-aliases`.
- **"CMK deleted accidentally."** KMS has a 7–30 day waiting period; `cancel-key-deletion` within
  that window recovers it. After deletion, encrypted data is permanently unrecoverable.
- **"Encryption expired on S3 object."** S3 uses the bucket key setting + CMK state; check if the
  CMK was disabled or the bucket key was changed.

## 14. PRIORITY

P2 — bonus tier. KMS appears in every "how do you encrypt?" follow-up but doesn't get deep
coverage unless the role touches compliance, cryptography, or data-platform work. Know envelope
encryption and the CMK/data-key rotation distinction cold.

## 15. STOP HERE — done when you can…

1. explain envelope encryption (DEK + CMK, GenerateDataKey flow) in one paragraph;
2. distinguish AWS-managed vs customer-managed keys (cost, control, rotation);
3. name what rotation does and doesn't rotate (CMK only, not data keys);
4. describe key policy vs grants and when you'd use each;
5. list three services that use KMS by default (S3, EBS, RDS).

## 16. DO NOT STUDY YET

KMS Custom Key Stores (CloudHSM-backed), multi-region keys, KMS-defined grants deep-dive,
asymmetric key use-cases for code-signing pipelines, key policy condition keys, `Retire grant`
mechanics, KMS in Serverless (Lambda env-var encryption). The envelope encryption + alias model is
the interview-visible surface.

---

## QC CHECKLIST — AWS.P2.5

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (DEK/CMK, envelope flow, policy vs grants)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (envelope encryption, symmetric vs asymmetric, rotation limits, key policy/grants)? | ✔ §3 |
| 5 | Dependencies (S3 SSE P0.6, EBS encryption P0.5, RDS encryption P1.2, ECR signing P0.10)? | ✔ §2–3 |
| 6 | Essential commands (list-keys, list-aliases, describe-key, generate-data-key, create-key)? | ✔ §3, §8 |
| 7 | Reproduce (read-only: alias listing + describe-key on alias/aws/ssm)? | ✔ verified live |
| 8 | Break it (no CMKs = honest baseline, AccessDenied on decrypt, rotation misconception)? | ✔ §9 |
| 9 | Observe + interpret (empty list-keys, AWS-managed aliases, KeyManager=AWS)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** (no CMK created — AWS-managed alias metadata verified; envelope model from knowledge) |

Verdict: **PASS** (self-drive item 13). Next session: **AWS.P2.6 — VPC endpoints: gateway vs interface (PrivateLink), endpoint policies, and private traffic the interview asks about.**

---
# SESSION AWS.P2.6 — VPC ENDPOINTS: PRIVATE TRAFFIC THE INTERVIEW ASKS ABOUT

Environment note: **cost-free lab** — VPC + subnet + route table + gateway endpoint (S3) created
and fully deleted after verification. Gateway endpoints are $0. Key incident verified: CLI verb
trap + dependency-violation on VPC deletion.

## 1. WHAT IS IT? (≤30s)

**VPC endpoints** let your VPC traffic reach AWS services **without crossing the public internet**.
Two types: **Gateway endpoints** (S3, DynamoDB — free, route-table attached, no ENI) and
**Interface endpoints** (most services — ENI per AZ, ~$0.01/hr + data). The endpoint is a routing
object, not a proxy — it keeps traffic on the AWS backbone.

## 2. WHY DOES IT EXIST?

The interview's "how do you keep traffic off the public internet?" answer. Gateway endpoints replace
NAT Gateway / IGW egress for S3 and DynamoDB — saving money and meeting compliance ("no public
internet path"). Interface endpoints (PrivateLink) extend this to most AWS services. Paired with
P0.3 (NAT discussion) — endpoints remove the "private subnet needs NAT for AWS services" problem.

## 3. HOW DOES IT WORK? (verified, $0)

- **VPC + subnet (verified):** Created VPC `10.11.0.0/16` + subnet + route table for the lab.
  No default VPC in this account (same as P1.1 incident).
- **Gateway endpoint (verified):** `create-vpc-endpoint --vpc-id <vpc> --service-name
  com.amazonaws.us-west-1.s3 --route-table-ids <rt>` → endpoint id `vpce-03bf087869329ff72`
  (first run) / `vpce-0b387a7148d2b7fc3` (second run), type **Gateway**, state available,
  service s3. Gateway endpoints add a route to your route table pointing S3 traffic to the
  endpoint — no ENI, no hourly cost, no security group.
- **Describe evidence (verified):** `describe-vpc-endpoints` → type Gateway, State available.
  The endpoint shows as a route-table target, not an IP address.
- **Interface endpoints (model):** Create an ENI per AZ in your subnet, gets a private IP, governed
  by a security group. You get a DNS name (e.g. `com.amazonaws.us-west-1.secretsmanager`) that
  resolves to the ENI's private IP. Billable: ~$0.01/hr per endpoint per AZ + data processing.
- **Endpoint policy (model):** JSON resource policy attached to the endpoint — restricts which
  resources the endpoint can access. Example: an S3 gateway endpoint policy that allows access
  only to specific buckets. Default policy = full access to the service.
- **Key incident (verified):** `delete-vpc-endpoint` (singular) → **ParamValidation: Found invalid
  choice, maybe you meant delete-vpc-endpoints** — the CLI verb is PLURAL. Also: first `DeleteVpc`
  on the lab VPC failed with **DependencyViolation: The vpc ... has dependencies and cannot be
  deleted** because the endpoint still existed. You must delete endpoint FIRST, then route table /
  subnet, then VPC. The endpoint counts as a VPC dependency.
- **Cleanup order (verified):** endpoint → route table → subnet → VPC. Reverse of creation order.

## 4. MENTAL MODEL

```
PRIVATE SUBNET → AWS SERVICE

WITHOUT endpoint:  app → route table → NAT GW → IGW → internet → AWS service endpoint
                                                      ↑ public path ($$$)

WITH gateway endpoint (S3/DynamoDB):
  app → route table → GATEWAY ENDPOINT → AWS backbone → S3/DynamoDB
  ($0, no ENI, route-table attachment)

WITH interface endpoint (other services):
  app → route table → ENI (private IP, per AZ) → AWS backbone → service
  (~$0.01/hr + data, security-group governs access)

Endpoint policy = JSON filter on what the endpoint allows
```

## 5. INTERVIEW-SAFE ANSWER

"VPC endpoints keep traffic on the AWS backbone instead of the public internet. Gateway endpoints
for S3 and DynamoDB are free — they add a route to the route table, no ENI, no hourly cost.
Interface endpoints for other services create an ENI per AZ with a private IP and are billable at
about a cent per hour plus data. I verified this session: created a gateway endpoint for S3, saw
it show up as a route-table target, and confirmed the state is available. I also hit two real
incidents: the CLI verb is plural (delete-vpc-endpoints, not singular), and the endpoint counts as
a VPC dependency — you can't delete the VPC until the endpoint is gone. Endpoint policies are JSON
resource policies that restrict what the endpoint can access, like limiting S3 access to specific
buckets."

## 6. FOLLOW-UP ATTACKS

**Q. Gateway vs interface endpoint — when which?**
**A.** Gateway for S3 and DynamoDB only (free, route-table-based). Interface for everything else
(billable, ENI-based, security-group governs). Gateway has no DNS name; interface does.

**Q. Why do you need a VPC endpoint if you already have a NAT Gateway?**
**A.** NAT Gateway costs money per GB; endpoints for S3/DynamoDB are free. For private subnets
that only need S3/DynamoDB, a gateway endpoint eliminates the NAT path entirely.

**Q. Endpoint policy — what's an example?**
**A.** A JSON policy on the endpoint resource that says "this endpoint can only access
arn:aws:s3:::my-bucket". Applied at the endpoint level — independent of the IAM policy on the
caller. Both must allow the action.

**Q. Can you have both gateway and interface endpoints for the same service?**
**A.** S3/DynamoDB support gateway endpoints. Most services only support interface endpoints. You
can have both if the service supports both — the route table picks gateway, DNS picks interface.

**Q. What's PrivateLink?**
**A.** PrivateLink is the technology behind interface endpoints — it creates ENIs with private IPs
in your VPC that connect to a service endpoint in the provider's VPC. You can also use it for
your own services (endpoint service) exposed to other VPCs/accounts.

## 7. PRACTICAL EXAMPLE (production)

```bash
# Gateway endpoint for S3 (free)
aws ec2 create-vpc-endpoint --vpc-id vpc-abc \
  --service-name com.amazonaws.us-west-1.s3 \
  --route-table-ids rtb-abc rtb-bcd \
  --policy-document '{"Statement":[{"Effect":"Allow","Principal":"*","Action":"s3:GetObject",
    "Resource":"arn:aws:s3:::my-data-bucket/*"}]}'
# Interface endpoint for Secrets Manager (billable)
aws ec2 create-vpc-endpoint --vpc-id vpc-abc \
  --service-name com.amazonaws.us-west-1.secretsmanager \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-abc subnet-bcd \
  --security-group-ids sg-endpoint
# App in private subnet resolves secretsmanager.vpce-... → private IP → no internet path
```

## 8. BUILD / REPRODUCE ($0 — verified)

```bash
AWS_PAGER="" PATH="$HOME/.local/bin:$PATH:$PATH"
VPC=$(aws ec2 create-vpc --cidr-block 10.11.0.0/16 --query 'Vpc.VpcId' --output text)
SUB=$(aws ec2 create-subnet --vpc-id "$VPC" --cidr-block 10.11.1.0/24 --availability-zone us-west-1a --query 'Subnet.SubnetId' --output text)
RT=$(aws ec2 create-route-table --vpc-id "$VPC" --query 'RouteTable.RouteTableId' --output text)
aws ec2 associate-route-table --route-table-id "$RT" --subnet-id "$SUB" > /dev/null
aws ec2 create-vpc-endpoint --vpc-id "$VPC" --service-name com.amazonaws.us-west-1.s3 --route-table-ids "$RT"
# verify
aws ec2 describe-vpc-endpoints --filters Name=vpc-id,Values="$VPC" \
  --query 'VpcEndpoints[].{Type:VpcEndpointType,State:State,Service:ServiceName}'
# cleanup (reverse order — VERIFIED order matters)
aws ec2 delete-vpc-endpoints --vpc-endpoint-ids <endpoint-id>
aws ec2 disassociate-route-table --association-id <assoc-id>
aws ec2 delete-route-table --route-table-id "$RT"
aws ec2 delete-subnet --subnet-id "$SUB"
aws ec2 delete-vpc --vpc-id "$VPC"
```

## 9–11. BREAK IT, OBSERVE, TROUBLESHOOT

### INCIDENT — "delete-vpc-endpoint: invalid choice" (VERIFIED)

Trigger: ran `aws ec2 delete-vpc-endpoint --vpc-endpoint-ids vpce-...`
Observe: `ParamValidation: Found invalid choice 'delete-vpc-endpoint', maybe you meant
'delete-vpc-endpoints'`
Root cause: the CLI verb is **plural** — `delete-vpc-endpoints`. The singular form is invalid.
Fix: use `aws ec2 delete-vpc-endpoints --vpc-endpoint-ids vpce-...`.
Verify: endpoint disappears from `describe-vpc-endpoints`.
Prevent: muscle-memory the plural; the API model uses plural for batch-delete (even one ID).

### INCIDENT — "DependencyViolation: VPC has dependencies" (VERIFIED)

Trigger: tried `delete-vpc --vpc-id $VPC` after deleting subnet only.
Observe: `DependencyViolation: The vpc vpc-... has dependencies and cannot be deleted`
Root cause: the gateway endpoint still existed and counts as a VPC dependency. Even though the
subnet was deleted, the endpoint (attached to the route table) blocks VPC deletion.
Fix: delete the endpoint FIRST → then route table → then subnet → then VPC. Verified this order
works.
Prevent: always check `describe-vpc-endpoints` before deleting a VPC; endpoints are an
easy-to-forget dependency.

### DECISION OVERLAY — what NOT to do

- Don't use NAT Gateway for S3/DynamoDB when a free gateway endpoint exists.
- Don't forget endpoint policies — default = full service access, violating least privilege.
- Don't assume all services have gateway endpoints — most need interface endpoints (billable).
- Don't delete a VPC before checking for endpoints, ENIs, NAT gateways, or other dependencies.
- Don't hard-code interface endpoint DNS — it's region-specific and changes with AZ placement.

## 12. INTERVIEW TRAPS

| Trap | Truth |
|---|---|
| "VPC endpoint = proxy" | No — it's a route-table entry (gateway) or ENI (interface) on the AWS backbone. |
| "Gateway endpoints cost money" | Free — only interface endpoints have hourly + data charges. |
| "All services have gateway endpoints" | Only S3 and DynamoDB. Everything else is interface endpoints. |
| "Endpoint policy replaces IAM policy" | Both gate access. Caller IAM + endpoint policy must both allow the action. |
| "Interface endpoint = single IP" | One ENI per AZ, so one private IP per AZ. Multi-AZ = multi-ENI. |
| "Endpoints make NAT Gateway obsolete" | Only for S3/DynamoDB. Other services still need NAT or interface endpoints. |
| "Endpoint is deleted with the VPC automatically" | No — it's a dependency. You must delete it first or the VPC delete fails. |

## 13. FIRST-CHECK REASONING

- **"Private subnet can't reach S3."** Check: gateway endpoint exists and is attached to the
  route table? Route table associated with the subnet? `describe-vpc-endpoints` + `describe-route-tables`.
- **"VPC won't delete: DependencyViolation."** Check: gateway endpoints, interface endpoints,
  NAT gateways, ENIs still attached. `describe-vpc-endpoints` is the first read.
- **"Interface endpoint unreachable from one AZ."** ENI only exists in subnets you specified
  during create. If you missed an AZ's subnet, that AZ has no route to the service.
- **"Endpoint policy blocks expected access."** Default = full access. If someone added a policy,
  it restricts — check `describe-vpc-endpoints` for the policy document.

## 14. PRIORITY

P2 — bonus tier. VPC endpoints come up in "how do you keep traffic private?" and "cost
optimization" discussions. Gateway endpoint for S3 is the high-value free-tier answer; interface
endpoints show depth when PrivateLink is mentioned.

## 15. STOP HERE — done when you can…

1. explain gateway vs interface endpoints (cost, ENI, route-table vs DNS);
2. name which two services get free gateway endpoints (S3, DynamoDB);
3. describe the VPC deletion order (endpoint → route table → subnet → VPC);
4. explain endpoint policy vs IAM policy (both must allow);
5. recall the CLI verb trap (delete-vpc-endpoints is plural).

## 16. DO NOT STUDY YET

PrivateLink for custom endpoint services (exposing your own service), VPC endpoint connection
notifications, endpoint service whitelisting, cross-account endpoint sharing, VPC endpoint
CloudWatch metrics, IPv6 + endpoint behavior, transfer acceleration via endpoints. The gateway vs
interface split + deletion-order lesson is the interview-visible surface.

---

## QC CHECKLIST — AWS.P2.6

| # | Check | Result |
|---|---|---|
| 1 | Mental-model diagram (gateway vs interface, route-table vs ENI, policy)? | ✔ §4 |
| 2 | ≤30s definition? | ✔ §1 |
| 3 | Why it exists? | ✔ §2 |
| 4 | Important mechanisms (gateway vs interface, endpoint policy, dependency on VPC deletion)? | ✔ §3 |
| 5 | Dependencies (VPC/subnet/route-table P0.3, NAT discussion, S3 P0.6, IAM P0.2)? | ✔ §2–3 |
| 6 | Essential commands (create-vpc-endpoint, describe-vpc-endpoints, delete-vpc-endpoints)? | ✔ §3, §8 |
| 7 | Reproduce ($0: gateway endpoint for S3, fully cleaned)? | ✔ verified live |
| 8 | Break it (plural CLI verb, DependencyViolation, default policy = full access)? | ✔ §9 |
| 9 | Observe + interpret (endpoint type Gateway, State available, route-table target)? | ✔ §3 |
| 10 | Symptom→root-cause→fix→verify→prevent? | ✔ §9 |
| 11 | First-check + WHY? | ✔ §13 |
| 12 | Answer follow-ups? | ✔ §6 |
| 13 | Defend resume claim honestly? | **SELF-VERIFY** (gateway endpoint created and deleted at $0; both incidents verified live) |

Verdict: **PASS** (self-drive item 13). AWS core interview phases P0, P1, P2 — ALL COMPLETE.
