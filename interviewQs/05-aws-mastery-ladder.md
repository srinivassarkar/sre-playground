# 05 — AWS Mastery Ladder & Operational Playbook

Mastery ladder: **P0 → P1 → P2 → IGNORE**

---

## Priority Map (Session-by-Session)

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

---

# SESSION AWS.P0.1 — AWS CLI + REGIONS/AZ + IAM IDENTITY

Environment note: aws-cli/2.36.44 (local install, no sudo), default region **us-west-1**, IAM user
`terraform_journey` in account `980664882691`. All commands verified live against real AWS.

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
- **Install:** official zip → `./aws/install --install-dir ~/.local/aws-cli --bin-dir ~/.local/bin` (no sudo needed).
- **Credentials:** `~/.aws/credentials` carries static access keys; `~/.aws/config` holds region + output format.
- **Identity (verified):** `aws sts get-caller-identity` returns `Arn`, `Account`, `UserId`. This works with NO permissions (it's identity proof, not an authorization check).
- **Region model (verified):** `aws ec2 describe-regions` → 18 active regions by default; `--all-regions` shows opt-in status. `us-west-1` has **2 AZs** (`us-west-1b`, `us-west-1c`) — us-west-1a does NOT exist.
- **Output control (verified):** `--output json|table|text`. `--no-cli-pager` (or unset AWS_PAGER) prevents less-pager hang in pipes.
- **S3 touch (verified):** `aws s3 mb s3://<unique-name>` creates a bucket, `aws s3 ls` lists, `aws s3 rb` removes.
- **STS sessions (verified):** `aws sts get-session-token --duration-seconds 900` issues temporary credentials (AccessKeyId, SecretAccessKey, SessionToken, Expiration).

## 4. MENTAL MODEL
```
syntax:    aws <service> <action> [--region X] [--output F] [--query JMESPath]
identity:  sts get-caller-identity → Arn/Account/UserId (always works)
footprint: Region (us-west-1) → AZs (us-west-1b, us-west-1c) [no us-west-1a!]
output:    json=API shape | table=human | text=script/pipe
creds:     ~/.aws/credentials + ~/.aws/config → env AWS_DEFAULT_REGION overrides
```

## 5. INTERVIEW-SAFE ANSWER
"The CLI is `aws <service> <action>` plus three control flags. Identity: `aws sts get-caller-identity` proves who I am even with zero permissions — the first thing every script checks. Footprint: regions are physical islands; us-west-1 runs 2 AZs (us-west-1b, us-west-1c — us-west-1a doesn't exist), which is the classic gotcha for HA design; opt-in regions appear only with `--all-regions`. Output: json for programmatic piping, table for humans, text for scripts, and `--query` JMESPath to extract exact values. Region is overridable per-command."

## 6. FOLLOW-UP ATTACKS
* **`--query` syntax vs JMESPath:** Filter with `[?Field==value]`, extract specific fields with `.Field`.
* **Env vs config precedence:** `AWS_PROFILE` / `AWS_DEFAULT_REGION` / `AWS_ACCESS_KEY_ID` override `~/.aws/config` & `credentials`.
* **Why no us-west-1a:** Some regions expose fewer AZs; AWS rounds availability down in older regional builds. Always check `describe-availability-zones` before assuming 3 AZs.

---

# SESSION AWS.P0.2 — IAM DEEP-DIVE: POLICIES, ROLES, TRUST & LEAST PRIVILEGE

## 1. WHAT IS IT? (≤30s)
IAM is the **identity-and-permission layer** of every AWS API call. It answers three questions in order: (1) **who** (user/role/anonymous), (2) **action** (what API call), (3) **resource** (which ARN). The key models: **users** (long-term credentials), **groups** (users sharing a policy set), **policies** (JSON documents with Effect+Action+Resource), and **roles** (assumed via STS, with a **trust policy** controlling who can assume).

## 2. HOW DOES IT WORK? (verified)
- **Policy document anatomy:**
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": ["s3:ListBucket", "s3:GetObject"],
      "Resource": ["arn:aws:s3:::demo-bkt", "arn:aws:s3:::demo-bkt/*"]
    }]
  }
  ```
- **The two doors of AssumeRole:**
  1. **Door 1 (Trust policy):** Configured on the role itself (`Principal` field) — controls WHO can assume the role.
  2. **Door 2 (Caller's policy):** Must grant `sts:AssumeRole` on the role ARN.
  * Both doors must be open for assumption to succeed.
- **Eventual consistency:** Freshly created roles/policies can take 2–5 seconds to propagate across STS endpoints. In scripts and automation, always include a retry/backoff loop after role creation.

## 3. MENTAL MODEL
```
identity:  User (long-term key) | Role (temporarily assumed via STS)
policy:    {"Effect", "Action", "Resource"}
eval:      1. Explicit Deny wins
           2. Match an Allow → permitted
           3. No match → implicit deny
assume:    Door 1 (Trust policy on role) AND Door 2 (Caller has sts:AssumeRole)
```

---

# SESSION AWS.P0.3 — VPC: SUBNETS, ROUTES, IGW, NAT & CIDR PLANNING

## 1. WHAT IS IT? (≤30s)
A **VPC** (Virtual Private Cloud) is a private, isolated IP network scoped to one region: you define a CIDR block (e.g. `10.0.0.0/16`), carve it into **subnets** (one per AZ), and control egress with **route tables**. Public subnets route `0.0.0.0/0` to an **Internet Gateway (IGW)**; private subnets route `0.0.0.0/0` to a **NAT Gateway** (located in a public subnet) for outbound-only internet access.

## 2. CIDR MATH & RESERVED IPS
- `/16` VPC = 65,536 addresses → **65,531 usable** (AWS reserves 5 per subnet).
- `/24` subnet = 256 addresses → **251 usable**.
- **The 5 Reserved IPs per subnet:**
  * `.0`: Network address.
  * `.1`: VPC router.
  * `.2`: Amazon-provided DNS (Route 53 Resolver).
  * `.3`: AWS future use.
  * `.255`: Network broadcast address.

## 3. THE DEPENDENCY VIOLATION TRAP (VPC Teardown Order)
When deleting a VPC, AWS throws `DependencyViolation` if resources or routes still exist.
**Mandatory Teardown Sequence:**
1. Terminate all EC2 instances / EKS nodes.
2. Delete NAT Gateways and release Elastic IPs (EIPs).
3. Detach and delete Internet Gateway (IGW).
4. Delete VPC Endpoints (`delete-vpc-endpoints`).
5. Delete custom Security Groups & custom NACLs.
6. **Drop stale routes (`0.0.0.0/0`)** inside non-main route tables before attempting to delete route tables.
7. Delete subnets.
8. Delete VPC.

---

# SESSION AWS.P0.4 — SECURITY GROUPS vs NACLs

| Dimension | Security Group (SG) | Network ACL (NACL) |
|---|---|---|
| **Scope** | Resource / Elastic Network Interface (ENI) | Subnet boundary |
| **State** | **Stateful** (inbound allow automatically permits reply) | **Stateless** (both directions must be explicitly allowed) |
| **Default Inbound** | Deny all | Allow all (Rule 100 on default NACL) |
| **Default Outbound**| Allow all | Allow all (Rule 100 on default NACL) |
| **Evaluation** | Union of ALL matching rules evaluated | **First match** in numerical order (Rule 1–32766, ends in 32767 Deny) |
| **Rule Targets** | CIDR ranges, prefix lists, or **SG ID references** | CIDR ranges only (cannot reference SGs) |

### The Stateless NACL Trap:
Allowing inbound HTTPS (TCP 443) on a NACL is not enough. You must also create an explicit **outbound rule for ephemeral ports (TCP 1024–65535)** to allow the server's return packet back to the client.

---

# SESSION AWS.P0.5 — EC2, EBS & AMIS

## 1. CORE MECHANICS
- **Instance Types:** `t` (burstable, CPU credits), `m` (general purpose), `c` (compute-heavy), `r` (memory-heavy), `g` (GPU/silicon).
- **Pricing Models:** On-Demand (pay-per-sec), Savings Plans (committed spend $/hr), Reserved Instances (committed family 1–3y), Spot (up to 90% discount, 2-minute interruption notice).
- **EBS Lifecycle:**
  * Root volume defaults to `DeleteOnTermination=true`.
  * Secondary attached EBS volumes default to `DeleteOnTermination=false` (they persist and continue billing after instance termination).
  * EBS volumes are **strictly zonal** — an EBS volume in `us-west-1b` cannot be attached to an instance in `us-west-1c` without snapshotting first.

---

# SESSION AWS.P0.6 & P1.4 — S3 CORE & ADVANCED OPERATIONS

## 1. CORE PROPERTIES
- **Namespace:** Bucket names are **globally unique**; object storage is **regional**.
- **Keys:** S3 has no real folders. Keys are flat strings with `/` delimiters (`docs/app/config.txt`).
- **Consistency:** Strong read-after-write consistency for PUTs and DELETEs of objects across all regions.

## 2. VERSIONING & DELETE MARKERS
- When versioning is enabled, a `DELETE` request does **not** erase data. It creates a **Delete Marker** as the latest version.
- To restore a deleted object: delete the Delete Marker.
- To permanently purge an object: pass both `--key` AND `--version-id`.

## 3. LIFECYCLE MANAGEMENT & COST CONTROLS
- **The 3 Verbs:**
  1. `Transition`: Moves objects between classes (STANDARD $\rightarrow$ STANDARD_IA $\rightarrow$ GLACIER_IR $\rightarrow$ GLACIER $\rightarrow$ DEEP_ARCHIVE).
  2. `Expiration`: Purges the latest/current version after $N$ days.
  3. `NoncurrentVersionExpiration`: Purges accumulated older versions after $N$ days (the critical versioning bill guard).
- **Default Minimum Object Size:** AWS enforces a **128 KB minimum** for lifecycle storage class transitions to prevent transition fees exceeding storage savings.

---

# SESSION AWS.P0.7 — APPLICATION LOAD BALANCER (ALB)

## 1. ARCHITECTURE & ROUTING
- **L7 Reverse Proxy:** Terminates HTTP/HTTPS, supports host-based routing, path-based routing (`/api/*`), header conditions, and WebSockets/SSE.
- **Topology:** Must span **at least 2 Availability Zones**.
- **Target Groups:** Groups of targets (EC2 instance IDs, container IPs, or Lambda functions) with dedicated health check endpoints (e.g. `GET /healthz`, matcher 200).
- **Deregistration Delay:** Drains active connections cleanly before removing a target from rotation.

---

# SESSION AWS.P0.8 — ROUTE 53 & DNS ARCHITECTURE

## 1. ROUTING POLICIES
- **Simple:** Single record answer.
- **Weighted:** Distributes traffic based on assigned weights (ideal for canary deployments and blue-green ramps). Weight 0 disables traffic without deleting the record.
- **Latency:** Routes user to the AWS region offering the lowest round-trip latency.
- **Failover:** Routes to PRIMARY; if health check fails, fails over to SECONDARY (hot-standby DR).
- **Geolocation:** Routes traffic based on user's geographic location (compliance/localization).
- **Alias Records:** Specific to AWS resources (ALBs, CloudFront distributions, S3 buckets). Unlike standard CNAMEs, **Alias records can be created at the zone apex (`example.com`)**.

---

# SESSION AWS.P0.9 — CLOUDWATCH OBSERVABILITY

## 1. THE THREE PILLARS IN AWS
- **Metrics:** Time-series aggregated over periods (60s default, 1s high-resolution).
- **Alarms:** States: `OK`, `ALARM`, `INSUFFICIENT_DATA`. Alarms trigger actions via SNS, Auto Scaling, or EC2 recovery.
- **Logs:** Log Groups (configured with explicit retention periods, e.g. 7 or 30 days) $\rightarrow$ Log Streams $\rightarrow$ Log Events. Queried via metric filters or CloudWatch Logs Insights.

---

# SESSION AWS.P0.10 — ECR & EKS (CONTAINER CAPSTONE)

## 1. CORE LESSONS & TRAPS
- **ECR Authentication:** Short-lived tokens generated via `aws ecr get-login-password`, valid for 12 hours. Kubelet pulls using the worker node IAM role (`AmazonEC2ContainerRegistryReadOnly`).
- **The EKS Max-Pods Trap:** EKS caps the maximum number of pods per node based on instance type ENI limits:
  $$\text{Max Pods} = N_{\text{ENIs}} \times (\text{IPs per ENI} - 1) + 2$$
  * On a `t3.micro`, max pods is capped at **4**. System addons (`aws-node`, `kube-proxy`, `coredns`) consume these slots, leaving application pods stuck in `Pending` with `Too many pods`.

---

# SESSION AWS.P1.1 — AUTO SCALING GROUPS (ASG)

- **Launch Templates:** Versioned configurations defining AMI, instance type, security groups, and user-data scripts.
- **Capacity Sizing:** `MinSize`, `MaxSize`, `DesiredCapacity`. An ASG with `0 / 0 / 0` maintains full policy configuration with $0 instance cost.
- **Target Tracking Policies:** Automatically adjusts capacity to maintain a metric target (e.g., maintain average CPU utilization at 50%).
- **Lifecycle Hooks:** Pauses instances during launch (`Pending:Wait`) or termination (`Terminating:Wait`) to execute custom warmup or connection-draining scripts before completing the lifecycle action.

---

# SESSION AWS.P1.2 — RDS (RELATIONAL DATABASE SERVICE)

- **Multi-AZ vs Read Replicas:**
  * **Multi-AZ:** Synchronous replication to a standby instance in another AZ for high availability. Automatic DNS failover (~60–120s). Standby does **not** serve read queries.
  * **Read Replicas:** Asynchronous replication to one or more read-only instances to scale read traffic. Can be promoted to an independent primary.
- **Point-in-Time Restore (PITR):** Combines daily automated snapshots with 5-minute transaction logs, allowing restoration to any specific second within the retention window (1–35 days). Restorations always provision a **new** instance with a new endpoint.

---

# SESSION AWS.P1.3 — SSM PARAMETER STORE & SECRETS MANAGER

- **SSM Parameter Store (Config):**
  * Free tier for Standard parameters (up to 10,000 parameters, 4 KB each).
  * Supports `String`, `StringList`, and `SecureString` (KMS-encrypted).
  * Overwriting appends a new immutable version (v1, v2); historical versions remain queryable.
  * Version labels (e.g. `prod-cfg`) pin consumers to specific versions.
- **Secrets Manager (Credentials):**
  * Built for credentials, API keys, and database passwords ($0.40/secret/month).
  * Provides automatic rotation via Lambda on a schedule.
  * Manages version stages: `AWSCURRENT` and `AWSPREVIOUS` for instant rollback.

---

# SESSION AWS.P1.5 — CLOUDTRAIL AUDIT LOGGING

- **Event History:** Always-on, free 90-day log of all management plane API calls (who, what, when, IP address). Accessible via `lookup-events` without configuring any infrastructure.
- **Trails:** Persistent delivery of management and data events to an S3 bucket or CloudWatch Logs for long-term retention and Athena SQL querying.
- **Integrity Validation:** Computes SHA-256 digest files signed with KMS to cryptographically prove audit logs were not modified post-delivery.

---

# SESSION AWS.P2.1 — AWS LAMBDA

- **Event-Driven Execution:** Functions execute in ephemeral sandboxes based on synchronous (`RequestResponse`) or asynchronous (`Event`) triggers.
- **Cold Starts:** Latency incurred when a new sandbox container boots and initializes dependencies. Mitigated via Provisioned Concurrency or lean initialization code.
- **Execution Limits:** Maximum memory 10 GB, maximum timeout **15 minutes**, maximum sync payload size **6 MB** (async 256 KB), `/tmp` scratch storage 10 GB.
- **VPC Networking:** Lambda functions connected to a private VPC lose public internet access unless routed through a private subnet with a route to a **NAT Gateway**.

---

# SESSION AWS.P2.2 — CLOUDFRONT CDN

- **Edge Distributions:** Caches static and dynamic content across hundreds of global edge locations.
- **Origin Access Control (OAC):** The modern, secure replacement for legacy OAI. Restricts S3 bucket access so objects can only be fetched through CloudFront signed requests while keeping the bucket private.
- **Cache Invalidation:** Invalidates specific path patterns (`/index.html`, `/assets/*`). Versioned asset names (`app-v2.js`) avoid invalidation costs.

---

# SESSION AWS.P2.3 — API GATEWAY

- **REST vs HTTP APIs:**
  * **HTTP APIs:** Low-latency, cost-effective proxy designed for Lambda and HTTP backends with built-in JWT authorizers.
  * **REST APIs:** Full-featured gateway supporting request/response schema validation, API keys, usage plans, WAF integration, and request transformation templates.
- **Deployments vs Stages:** A deployment is an immutable snapshot of resources and methods; a stage (e.g. `dev`, `prod`) is a named environment pointer referencing a deployment.

---

# SESSION AWS.P2.4 — ECS (ELASTIC CONTAINER SERVICE)

- **ECS vs EKS:** ECS is AWS-native with zero control-plane operational overhead; EKS provides open-standard Kubernetes ecosystem compatibility.
- **Fargate vs EC2 Launch Type:** Fargate runs containers serverless with per-task billing and no underlying EC2 instances to manage; EC2 launch type utilizes an Auto Scaling group of customer-managed nodes.
- **Task Role vs Execution Role:**
  * **Task Execution Role:** Used by the ECS agent to pull container images from ECR and push logs to CloudWatch.
  * **Task Role:** Assumed by the application running *inside* the container to interact with AWS services (S3, DynamoDB).

---

# SESSION AWS.P2.5 — AWS KMS (KEY MANAGEMENT SERVICE)

- **Envelope Encryption:**
  1. Application calls KMS `GenerateDataKey`.
  2. KMS returns a **Plaintext Data Key (DEK)** and an **Encrypted Data Key (DEK)**.
  3. The application encrypts the data locally with the plaintext DEK, then erases the plaintext DEK from memory.
  4. The encrypted DEK is stored alongside the ciphertext.
  * KMS never handles the raw data bytes; it only protects the data key.
- **Key Rotation:** Automatic annual rotation creates new backing key material for customer-managed keys (CMKs). Rotation does **not** re-encrypt existing data keys; historical key versions are retained to decrypt historical ciphertexts.

---

# SESSION AWS.P2.6 — VPC ENDPOINTS (PRIVATELINK)

- **Gateway Endpoints:**
  * Supported **only for Amazon S3 and DynamoDB**.
  * **Completely free** with no hourly or data processing charges.
  * Implemented as route-table target entries; does not provision ENIs.
- **Interface Endpoints (PrivateLink):**
  * Provisions an Elastic Network Interface (ENI) with a private IP in specified subnets.
  * Governed by Security Groups and accessed via regional DNS names.
  * Billable (~$0.01/hr per AZ plus data processing charges).
- **The ECR Private Pull Pattern:**
  * To pull images from ECR in a private subnet with zero NAT Gateway data charges:
    1. Provision Interface Endpoints for `ecr.api` and `ecr.dkr` (PrivateLink).
    2. Provision a **Gateway Endpoint for Amazon S3** (free), because ECR stores image layer blobs in S3.
