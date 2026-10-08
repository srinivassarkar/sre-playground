# AWS Solutions Architect Prep: 25 Production Questions & Model Answers

A complete, first-principles interview guide covering cloud architecture, networking, security, reliability, cost optimization, and live incident post-mortems.

---

## Table of Contents
1. [10.1 Highly Available Multi-Tier Architecture](#101-highly-available-multi-tier-architecture)
2. [10.2 NAT Gateway Mechanics and Use Cases](#102-nat-gateway-mechanics-and-use-cases)
3. [10.3 Internet Access for Private Subnet Workloads](#103-internet-access-for-private-subnet-workloads)
4. [10.4 Inter-Subnet Communication Within a VPC](#104-inter-subnet-communication-within-a-vpc)
5. [10.5 NACL (Stateless) vs Security Group (Stateful)](#105-nacl-stateless-vs-security-group-stateful)
6. [10.6 EC2 Terminated Unexpectedly: CloudTrail Triage](#106-ec2-terminated-unexpectedly-cloudtrail-triage)
7. [10.7 Lambda Fails Intermittently: Timeout vs Memory](#107-lambda-fails-intermittently-timeout-vs-memory)
8. [10.8 RDS Storage Full: Autoscaling and Vacuum](#108-rds-storage-full-autoscaling-and-vacuum)
9. [10.9 Accidental Deletion of S3 / RDS / EC2: Disaster Recovery](#109-accidental-deletion-of-s3--rds--ec2-disaster-recovery)
10. [10.10 Real-World Cost Optimization (STAR Method)](#1010-real-world-cost-optimization-star-method)
11. [10.11 Production Incident & Root Cause Analysis (STAR Method)](#1011-production-incident--root-cause-analysis-star-method)
12. [10.12 Auto Scaling Group Not Launching Instances](#1012-auto-scaling-group-not-launching-instances)
13. [10.13 Day-to-Day AWS Operational Services](#1013-day-to-day-aws-operational-services)
14. [10.14 EFS Performance and Bursting Credit Traps](#1014-efs-performance-and-bursting-credit-traps)
15. [10.15 EFS vs EBS: Workload Selection Decision Matrix](#1015-efs-vs-ebs-workload-selection-decision-matrix)
16. [10.16 Disabling Console Access for IAM Users](#1016-disabling-console-access-for-iam-users)
17. [10.17 Cross-Account Lambda (Account A) to S3 (Account B)](#1017-cross-account-lambda-account-a-to-s3-account-b)
18. [10.18 AWS STS and Temporary Credentials Architecture](#1018-aws-sts-and-temporary-credentials-architecture)
19. [10.19 IAM Trust Policy vs Permissions Policy](#1019-iam-trust-policy-vs-permissions-policy)
20. [10.20 Cross-Account Lambda (Account A) to DynamoDB (Account B)](#1020-cross-account-lambda-account-a-to-dynamodb-account-b)
21. [10.21 Disadvantages of EBS in Multi-AZ Kubernetes](#1021-disadvantages-of-ebs-in-multi-az-kubernetes)
22. [10.22 AWS Secrets Manager vs SSM Parameter Store](#1022-aws-secrets-manager-vs-ssm-parameter-store)
23. [10.23 Production Database Operational Tasks & Maintenance](#1023-production-database-operational-tasks--maintenance)
24. [10.24 Production Lambda Architectural Patterns & Hardening](#1024-production-lambda-architectural-patterns--hardening)
25. [10.25 IAM User vs IAM Role: Security Posture](#1025-iam-user-vs-iam-role-security-posture)

---

## 10.1 Highly Available Multi-Tier Architecture

### 30-Second Interview Answer
Spread every architectural tier across at least 2—ideally 3—Availability Zones (AZs), ensuring zero single points of failure across ingress, compute, caching, and persistence layers.

```
Route 53 (DNS / Latency / Failover Routing)
     │
     ▼
CloudFront (+ AWS WAF) ──▶ Edge Caching & Layer 7 DDoS Mitigation
     │
     ▼
Application Load Balancer (Public Subnets across 3 AZs)
     │
     ▼
Application Tier: Auto Scaling Group across 3 AZs (Private Subnets)
     │
     ├──────────────────────────┐
     ▼                          ▼
ElastiCache Redis (Multi-AZ)  Aurora Multi-AZ / DynamoDB (Isolated DB Subnets)
(Session & Ephemeral Cache)   (Active-Reader / Synchronous Replicas)

* Egress: One NAT Gateway per AZ in Public Subnets
* Storage: S3 for static assets via S3 Gateway VPC Endpoint
```

### The Systems Rationale & Follow-Up Defense
1. **Three-Tier Subnet Isolation:** Public subnets host only ALBs and NAT Gateways. Application servers run in private subnets with no public IPs. Databases reside in isolated database subnets with zero internet routing.
2. **Security Group Chaining by Reference:** Avoid hardcoded CIDRs. 
   * ALB Security Group allows inbound port 443 from `0.0.0.0/0`.
   * App Security Group allows inbound port 3000/8080 **only from the ALB Security Group ID**.
   * Database Security Group allows inbound port 5432/27017 **only from the App Security Group ID**.
3. **Stateless Compute Tier:** Store session state in ElastiCache or DynamoDB, and offload file uploads to S3. This allows the Auto Scaling Group (ASG) to dynamically scale instances in and out based on CPU or request count without terminating active user sessions.
4. **NAT Gateway per AZ:** NAT Gateways are AZ-scoped. Placing a single NAT Gateway in AZ-a creates an architectural Single Point of Failure (SPOF) for private workloads in AZ-b and AZ-c, while adding unnecessary cross-AZ data transfer fees ($0.01/GB).
5. **State & Database Replication:** Multi-AZ RDS uses synchronous physical block-level replication with automated failover in 60–120 seconds. Aurora Multi-AZ uses a shared storage layer across 3 AZs (6 copies of data), achieving failover in under 30 seconds and supporting up to 15 auto-scaling read replicas.

---

## 10.2 NAT Gateway Mechanics and Use Cases

### 30-Second Interview Answer
An AWS managed network service that enables instances in private subnets to initiate outbound IPv4 connections to the internet (for patching, OS updates, third-party APIs) while preventing unsolicited inbound traffic from the internet.

### How It Physically Works
1. Deployed into a **public subnet** and bound to an **Elastic IP (EIP)**.
2. Private route tables route internet-bound traffic via the NAT Gateway: `0.0.0.0/0 -> nat-xxxx`.
3. The NAT Gateway performs Source Network Address Translation (SNAT / PAT), substituting the private EC2 IP (`10.0.x.x`) with its public EIP, then forwards the packet to the Internet Gateway (IGW).
4. It maintains a stateful connection tracking table in memory. When the external server responds, it translates the destination IP back to the original private EC2 instance.

### Key Architectural Facts
* **AZ-Scoped:** Highly available within its assigned AZ, but does not span AZs. If that AZ fails, the NAT Gateway fails.
* **Throughput:** Auto-scales from 5 Gbps up to 100 Gbps burst automatically.
* **Protocol Support:** Supports TCP, UDP, and ICMP. Security Groups cannot be attached to a NAT Gateway (firewalling must be enforced at the subnet level via NACLs).
* **Private NAT Gateway:** Operates without an Elastic IP to translate overlapping private CIDRs across AWS Transit Gateway or on-premises networks.

### The Production Cost Trap
You pay an hourly instance rate plus **$0.045 per GB of data processed**. 
* **The Production Disaster:** EC2 instances in private subnets backing up terabytes of application data to S3 or pulling large container images through a NAT Gateway incur massive unnecessary bills.
* **The Fix:** Deploy an **S3 Gateway VPC Endpoint** (free of charge) and an **ECR Interface Endpoint (PrivateLink)** to keep traffic on the private AWS network backbone.

---

## 10.3 Internet Access for Private Subnet Workloads

### 30-Second Interview Answer
Associate the private subnet with a route table that directs default outbound traffic (`0.0.0.0/0`) to an active NAT Gateway located in a public subnet with an attached Internet Gateway.

### Configuration Checklist
1. Attach an Internet Gateway (IGW) to the VPC.
2. Configure the public subnet route table: `0.0.0.0/0 -> igw-xxxx`.
3. Allocate an Elastic IP and create the NAT Gateway in that public subnet.
4. Configure the private subnet route table: `0.0.0.0/0 -> nat-xxxx`.
5. Associate the private route table explicitly with the private subnet.

### Production Debugging Checklist (When Outbound Fails)
1. **Public Subnet Check:** Is the NAT Gateway actually residing in a subnet whose route table has `0.0.0.0/0 -> igw-xxxx`? (Placing a NAT Gateway in a private subnet creates an unroutable black hole).
2. **Subnet Route Association:** Is the private subnet explicitly associated with the private route table, rather than falling back to the VPC main route table?
3. **NACL Ephemeral Ports:** Do the subnet NACLs allow outbound traffic on ports 80/443 AND inbound return traffic on **ephemeral ports (1024-65535)**?
4. **Security Group Egress:** Does the instance Security Group permit outbound traffic? (Default is allow all outbound).
5. **DNS Resolution:** Are `enableDnsHostnames` and `enableDnsSupport` enabled on the VPC?

### Senior Follow-Up Alternatives
* **VPC Endpoints:** Use Gateway Endpoints for S3/DynamoDB and Interface Endpoints (PrivateLink) for other AWS services to eliminate internet routing completely.
* **Egress-Only Internet Gateway:** Use an Egress-Only IGW for IPv6 traffic instead of NAT.
* **Forward Proxy / AWS Network Firewall:** Deploy Squid or AWS Network Firewall when egress filtering requires domain whitelisting (FQDN) rather than plain IP routing.

---

## 10.4 Inter-Subnet Communication Within a VPC

### 30-Second Interview Answer
Inter-subnet communication within a VPC works **by default without any gateway or NAT**, routed automatically by the VPC's implicit **local route**.

### The Mechanics
Every route table inside a VPC contains an immutable default entry:
```
Target: VPC-CIDR (e.g., 10.0.0.0/16)  ──▶ Target: local
```
This route cannot be deleted, modified, or overridden. Consequently, any packet addressed to an IP within the VPC CIDR is routed directly across the AWS software-defined network (Nitro hypervisor / VPC mapping service) to any other subnet in any AZ.

### What Actually Enforces Traffic Boundaries
Route tables dictate **path**, not **authorization**. If packets between Subnet A and Subnet B fail to arrive, the issue is almost never the route table:
1. **Security Groups:** The destination instance must allow inbound traffic from the source. (Best practice: reference the source Security Group ID).
2. **Network Access Control Lists (NACLs):** If custom NACLs are applied, rules must explicitly allow traffic in **both directions** (stateless).
3. **Host-Level OS Firewalls:** Linux `iptables`, `nftables`, or `ufw` blocking incoming ports.

### The SRE Observability Tool
Use **AWS VPC Reachability Analyzer** to perform hop-by-hop static path analysis between two ENIs to immediately pinpoint whether a Security Group, NACL, or route table is dropping packets.

---

## 10.5 NACL (Stateless) vs Security Group (Stateful)

### Comparison Matrix

| Dimension | Security Group | Network Access Control List (NACL) |
| :--- | :--- | :--- |
| **Enforcement Layer** | Elastic Network Interface (ENI) / Instance | Subnet Boundary |
| **Connection State** | **Stateful:** Return traffic is automatically tracked and allowed | **Stateless:** Outbound return traffic must be explicitly allowed |
| **Rule Capabilities** | **Allow rules only** | **Allow and Deny rules** |
| **Evaluation Order** | All rules evaluated simultaneously | Evaluated in strict numerical order; first match wins |
| **Default Configuration** | Deny all inbound; allow all outbound | Default NACL allows all inbound and outbound |
| **Referencing** | Can reference other Security Group IDs | IP CIDRs only (cannot reference Security Groups) |

### Why Stateless Matters in Production
When a client initiates an inbound HTTPS connection on port 443:
* **Security Group:** Automatically tracks the TCP connection and permits the response to exit on whatever client port was used.
* **NACL:** Requires an inbound allow rule on port 443 **AND** an outbound allow rule on ephemeral ports **1024–65535**. If the outbound ephemeral port rule is missing, the TCP SYN-ACK cannot leave the subnet, and the client connection times out.

### When to Use Which
* **Security Groups:** 95% of operational access control. Fine-grained, least-privilege microsegmentation between application tiers.
* **NACLs:** Broad defensive backstop. Used specifically for **explicit IP blocking** (e.g., blacklisting a compromised CIDR or malicious crawler) and compliance-mandated subnet isolation.

---

## 10.6 EC2 Terminated Unexpectedly: CloudTrail Triage

### Step 1: Query AWS CloudTrail Event History
Navigate to CloudTrail Event History (covering the last 90 days) and filter by:
* `EventName = TerminateInstances`
* `ResourceName = i-0a1b2c3d4e5f6g7h8`

Inspect the JSON event payload:
* **`userIdentity`:** Identifies who initiated the termination:
  * An IAM User or assumed role (developer, deployment pipeline).
  * An AWS service principal (e.g., `autoscaling.amazonaws.com`).
* **`sourceIPAddress`:** IP of the caller (office VPN, CI/CD runner, external).
* **`userAgent`:** Identifies the tool used (AWS Console, Terraform, AWS CLI, SDK).

### Step 2: If CloudTrail Shows Zero API Calls
If no `TerminateInstances` API call exists, the termination was triggered by an automated or underlying infrastructure event:
1. **Auto Scaling Group Activity:** Check the ASG Activity History tab:
   * Scale-in event due to decreased traffic.
   * Failed ELB / EC2 health check replacement.
   * Availability Zone rebalancing.
2. **Spot Instance Interruption:** Check EC2 Console State Transition Reason. A Spot eviction displays `Server.SpotInstanceTermination` (2-minute warning notification).
3. **OS-Initiated Shutdown:** A Linux `shutdown -h now` or kernel panic where the EC2 instance setting `InstanceInitiatedShutdownBehavior` is configured to `terminate` displays `Client.InstanceInitiatedShutdown`.
4. **EBS Volume Quotas:** Failure to attach root volumes displays `Client.VolumeLimitExceeded`.
5. **Terraform Drift:** A Terraform run where resource parameters (like changing user-data or AMI without lifecycle rules) forced an in-place destroy and recreate.

### Step 3: Prevention & Guardrails
* Enable **EC2 Termination Protection** (`DisableApiTermination = true`).
* Attach an IAM boundary or Service Control Policy (SCP) explicitly denying `ec2:TerminateInstances` without an MFA token or specific tag condition.
* Configure an **Amazon EventBridge Rule** matching EC2 state transitions to dispatch immediate alerts to Slack / PagerDuty.
* Set `DeleteOnTermination = false` on attached persistent EBS volumes.

---

## 10.7 Lambda Fails Intermittently: Timeout vs Memory

### Step 1: Diagnose via CloudWatch Logs Insights
Never guess. Look at the CloudWatch `REPORT` log line emitted after each Lambda execution:
```
REPORT RequestId: c3b1d... Duration: 2999.8 ms Billed Duration: 3000 ms Memory Size: 128 MB Max Memory Used: 127 MB
```

* **Timeout Signature:** `Task timed out after X.XX seconds`. (Duration reaches or exceeds configured timeout).
* **Out-of-Memory (OOM) Signature:** `Runtime exited with error: signal: killed`. `Max Memory Used` is within 1–2 MB of `Memory Size`.
* **Throttling (429):** Check the `Throttles` and `ConcurrentExecutions` metrics against the regional or reserved concurrency limit.

### Why Failures Are Intermittent
1. **Cold Starts:** First execution on a new container takes 1–3 seconds longer (pulling container, initializing runtimes, establishing DB connections), pushing duration past the timeout threshold.
2. **Downstream Database Saturation:** Relational databases (RDS/PostgreSQL) run out of available connection pool slots under concurrency, causing connection attempts to stall until timeout.
3. **Network Latency / Variable Payload Size:** Variable external API latencies or processing large base64 image payloads.

### Production Engineering Fixes
* **Memory & CPU Coupling:** In Lambda, **CPU and network bandwidth scale proportionally with configured memory**. Bumping memory from 128 MB to 512 MB or 1024 MB allocates a full dedicated vCPU, often reducing execution time by 5x and lowering overall cost. (Use **AWS Lambda Power Tuning**).
* **Downstream Client Timeouts:** Configure HTTP client and database connection timeouts *below* the Lambda timeout (e.g., 5-second client timeout inside a 10-second Lambda) so errors fail gracefully with actionable logs instead of hard runtime timeouts.
* **Connection Pooling outside Handler:** Initialize database clients, HTTP connection pools, and AWS SDK clients in global scope outside the `exports.handler` function to reuse connections across warm invocations.
* **Use RDS Proxy:** Manages thousands of concurrent Lambda connections through a managed database connection pool.

---

## 10.8 RDS Storage Full: Autoscaling and Vacuum

### Immediate Firefighting Action
When an RDS instance enters `storage-full` state, all database writes are halted immediately.
* **Immediate Fix:** Go to the RDS console, modify the instance, allocate additional disk space (e.g. bump from 100 GiB to 200 GiB), and select **Apply Immediately**. Storage modifications apply online with zero downtime for modern engines.
* **Critical Rule:** **RDS storage can only be scaled up, never down.**

### Prevention: RDS Storage Autoscaling
Enable **Storage Autoscaling** and define a **Maximum Storage Threshold**.
* Autoscaling triggers when free storage drops below 10% (or 10 GiB) for at least 5 minutes, AND at least 6 hours have elapsed since the last modification.
* *Trap:* Because of the 6-hour cooldown, Storage Autoscaling will not rescue a database from rapid, runaway data ingestion. Always configure a CloudWatch alarm on `FreeStorageSpace < 20%`.

### Root Cause Investigation (PostgreSQL & MySQL Bloat)
1. **PostgreSQL MVCC Dead Tuples:** In Postgres, `UPDATE` and `DELETE` operations do not overwrite records in-place; they write new row versions and leave behind dead tuples.
   * Standard `VACUUM` marks space for reuse by future inserts, but **does not return physical disk space to the OS**.
   * `VACUUM FULL` rewrites tables to reclaim disk space, but acquires an **exclusive table lock**, blocking all application reads and writes.
   * **Production Solution:** Use **`pg_repack`**, an extension that reorganizes tables online without exclusive locks.
2. **Abandoned Replication Slots:** An orphaned or broken logical replication slot (e.g. from an old DMS migration or dead read replica) forces PostgreSQL to retain Write-Ahead Logs (WAL) on disk indefinitely, rapidly consuming hundreds of gigabytes.
   * Query: `SELECT * FROM pg_replication_slots WHERE active = false;` and drop unused slots.
3. **Runaway Logs:** Check for runaway PostgreSQL slow query logs, general query logs, or temporary tables created by unindexed hash joins spilling to disk.

---

## 10.9 Accidental Deletion of S3 / RDS / EC2: Disaster Recovery

### S3 Prevention & Recovery
* **Prevention:**
  * **S3 Versioning:** Deleting an object only inserts a *Delete Marker*. The original object remains intact.
  * **MFA Delete:** Requires hardware MFA tokens to permanently delete versioned objects.
  * **S3 Object Lock (Compliance Mode):** Makes objects completely immutable and undeletable, even by the AWS root account.
  * **Bucket Policy Deny:** Explicit deny on `s3:DeleteObject` and `s3:DeleteBucket`.
* **Recovery:** Remove the Delete Marker or restore the previous version ID. Use **Cross-Region Replication (CRR)** with a separate AWS account destination for disaster recovery.

### RDS Prevention & Recovery
* **Prevention:** Enable **Deletion Protection** on the RDS instance. Apply an IAM explicit deny on `rds:DeleteDBInstance`.
* **Recovery:** 
  * **Point-In-Time-Recovery (PITR):** Restores database state to any specific second within the backup retention window (up to 35 days) by replaying automated snapshots and transaction logs into a new instance.
  * *Trap:* Automated RDS backups are deleted when the DB instance is deleted unless you select "Retain automated backups" or create a **Final DB Snapshot**.
  * **AWS Backup:** Use centralized AWS Backup with a **Locked Backup Vault** and cross-account copy rules so compromised credentials cannot wipe backups.

### EC2 Prevention & Recovery
* **Prevention:** Enable **Termination Protection**. Maintain all server definitions in **Infrastructure as Code (Terraform)**.
* **Recovery:** Re-run Terraform pipelines to launch instances from pre-baked AMIs. Restore stateful data from automated EBS Snapshots managed via **Amazon Data Lifecycle Manager (DLM)**.

---

## 10.10 Real-World Cost Optimization (STAR Method)

### Situation
Our monthly AWS cloud expenditure had increased by approximately 35% over two quarters with no corresponding spike in customer traffic. The engineering team was instructed to audit the infrastructure and bring cloud spending under control.

### Task
I was tasked with identifying wasteful resource allocations, eliminating non-essential network transfer fees, and rightsizing our compute and storage fleet across all staging and production accounts.

### Action
I used **AWS Cost Explorer and Cost & Usage Reports (CUR) in Athena** grouped by service and resource tags, implementing four targeted levers:

1. **Eliminated NAT Gateway S3 Data Processing Fees:**
   * Found that EC2 instances were downloading hundreds of gigabytes of datasets and container layers from S3 through our NAT Gateways, incurring $0.045/GB in data processing charges.
   * Deployed an **S3 Gateway VPC Endpoint** in our route tables (which is completely free). All S3 traffic shifted off the NAT Gateway onto private AWS network routes, saving over **$450/month immediately**.
2. **Rightsizing Over-Provisioned Compute & Architecture Offloading:**
   * Used AWS Compute Optimizer to identify idle instances running at <12% average CPU utilization. Scaled down over-provisioned `t3.xlarge` instances to `c6i.large` / `m6i.large`.
   * Shifted heavy offline AI model inference and fine-tuning workloads off expensive cloud GPU instances onto our on-premises Apple Silicon hardware lab, cutting thousands in monthly on-demand GPU spend.
3. **Storage Tier Modernization (gp2 to gp3):**
   * Migrated all EBS volumes from legacy `gp2` to `gp3`. `gp3` provides a baseline 3,000 IOPS and 125 MB/s throughput independently of volume size, cutting storage baseline costs by **20%** across our EBS footprint.
   * Cleaned up orphaned, unattached EBS volumes and implemented S3 Lifecycle policies moving assets to **S3 Intelligent-Tiering**.
4. **Non-Production Automation:**
   * Configured **AWS Instance Scheduler** via Lambda to shut down development and staging instances overnight and on weekends, reducing non-prod compute run-time by **~65%**.

### Result
Achieved a **28% overall reduction in monthly AWS infrastructure costs** within 45 days, with zero disruption to service availability or deployment velocity.

---

## 10.11 Production Incident & Root Cause Analysis (STAR Method)

### Situation
Our production API Gateway and downstream microservices experienced intermittent cascading failures, resulting in sudden 502 Bad Gateway and 503 Service Unavailable errors for mobile and web clients during business hours.

### Task
As the platform engineer, I had to triage the running system, identify the root cause of the microservice crashes, restore uptime, and implement safeguards to prevent cascading failures.

### Action
I initiated live triage across our Linux instances, PM2 process logs, and network traffic:

1. **Isolating the OOM Memory Crash:**
   * Inspected PM2 error logs and identified that our financial ledger service crashed with:
     `FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory`.
   * Correlated timestamps with API logs and discovered a client query requesting `GET /creditsmanager?pageSize=10000`. Instantiating 10,000 full Mongoose documents in memory simultaneously breached V8's default 1.4 GB heap ceiling, triggering an unhandled garbage collection crash.
2. **Isolating the Gateway Timeout Race Condition:**
   * Discovered that our API Gateway was crashing with `Error [ERR_HTTP_HEADERS_SENT]: Cannot write headers after they are sent to the client`.
   * An upstream vision AI inference endpoint (`/api/blueye/seed/predict`) took 154 seconds to process a large image, breaching the Gateway's hardcoded 120-second timeout middleware.
   * The timeout middleware sent an HTTP 503 to the client and closed the socket. When the slow AI prediction finally finished 6 seconds later, the gateway forwarder attempted to write a 200 OK header to the closed stream, triggering an uncaught exception that crashed the Gateway.

3. **Engineering Resolutions:**
   * **Application Guardrails:** Enforced strict pagination boundaries in the controller (`pageSize = Math.min(requestedPageSize, 100)`) and applied `.lean()` to all read queries to return lightweight JSON objects, slashing memory consumption by 80%.
   * **Runtime Sizing:** Configured `node_args: '--max-old-space-size=3072'` in PM2 to provide heap headroom for bursty workloads.
   * **Stream Protection:** Added `if (response.headersSent) return;` guards in the Gateway forward proxy before dispatching responses, preventing stream collision crashes.

### Result
Resolved all crashing services within the maintenance window. API Gateway and microservice uptime returned to 99.99%, average memory per worker stabilized below 500 MB, and cascading restart loops were completely eliminated.

---

## 10.12 Auto Scaling Group Not Launching Instances

### Diagnosis Flow: Check the ASG Activity Tab
Do not start by debugging application code or SSHing. Navigate directly to **EC2 -> Auto Scaling Groups -> Selected ASG -> Activity tab**. 99% of launch failures are explicitly logged here.

### The Top 10 Root Causes & Fixes
1. **vCPU Quota Exceeded:** Activity log shows `VcpuLimitExceeded`. Request an AWS Service Quota increase for the instance family.
2. **AZ Capacity Depleted:** Activity log shows `InsufficientInstanceCapacity`. The requested instance type is temporarily unavailable in that specific AZ. Configure the ASG with a **Mixed Instances Policy** specifying multiple instance types (e.g. `c6i.large`, `c5.large`, `m6i.large`) across multiple AZs.
3. **Launch Template / AMI Missing:** The underlying AMI was deregistered, or the security group/key pair was deleted.
4. **KMS Key Permission Failure (The Classic Trap):** If the AMI or EBS volume is encrypted with a Customer Managed Key (CMK), the **AWSServiceRoleForAutoScaling** service-linked role must have explicit `kms:CreateGrant`, `kms:Decrypt`, and `kms:GenerateDataKey` permissions in the KMS key policy.
5. **Subnet IP Exhaustion:** The subnet CIDR is full (0 available private IPs). Expand the VPC CIDR or add secondary subnets.
6. **Missing IAM Instance Profile:** The launch template references an IAM role that lacks the required `iam:PassRole` permissions.
7. **Launch-Terminate Thrashing Loop:** Instances launch successfully, but fail the ELB health check within the `HealthCheckGracePeriod` (because the application takes longer to boot than the configured grace period). The ASG marks them unhealthy and terminates them, looping infinitely. Increase `HealthCheckGracePeriod` (e.g., from 30s to 300s).

---

## 10.13 Day-to-Day AWS Operational Services

### Functional Categorization
Organize daily services by infrastructure domain to demonstrate structured engineering discipline:

1. **Compute & Orchestration:**
   * **EC2:** Microservice hosting, instance lifecycle management, rightsizing.
   * **Auto Scaling Groups (ASG):** Dynamic capacity management, target tracking scaling policies.
   * **AWS Lambda:** Serverless webhook processing, operational cron jobs, automated remediation.
2. **Networking & Ingress:**
   * **VPC:** Multi-tier subnetting, route table rules, NAT Gateways, Internet Gateways.
   * **Application Load Balancer (ALB):** SSL termination, path-based routing, target group health monitoring.
   * **Route 53:** Public and private DNS zones, latency routing, health checks.
   * **VPC Endpoints:** S3 Gateway Endpoints and PrivateLink interface endpoints.
3. **Storage & Databases:**
   * **S3:** Asset storage, dataset repositories, lifecycle tiering, bucket policy enforcement.
   * **EBS (`gp3`):** Root and data volume lifecycle, automated DLM snapshots.
   * **RDS / MongoDB Atlas:** Automated backups, PITR validation, connection pooling, slow query analysis.
4. **Security, Identity & Secrets:**
   * **IAM:** Least-privilege IAM roles, trust policies, service-linked roles.
   * **AWS Secrets Manager & SSM Parameter Store:** Runtime credential injection, automated rotation.
   * **Security Groups:** Stateful microsegmentation, security group chaining.
5. **Observability & Infrastructure as Code:**
   * **Amazon CloudWatch:** Custom metrics, Log Groups, Metric Alarms, Dashboard triage.
   * **AWS CloudTrail:** API audit logging, incident forensics.
   * **Terraform:** Provisioning and maintaining all VPC, IAM, EC2, and networking resources under version control.

---

## 10.14 EFS Performance and Bursting Credit Traps

### EFS Throughput Modes
* **Elastic (Modern Standard):** Scales throughput automatically based on active read/write demand. Pay strictly per GB transferred. Ideal for unpredictable or spiky workloads.
* **Provisioned:** Allows decoupling throughput from stored size (e.g., provisioning 100 MB/s on a 10 GB file system).
* **Bursting:** Throughput scales linearly with **stored data volume**. Baseline is ~50 KiB/s per GiB stored (~50 MiB/s per TiB).

### The Bursting Credit Trap
* Small file systems (e.g., 20 GiB of application config or code) have a baseline throughput of only ~1 MB/s.
* When created, AWS grants a starting credit balance of ~2.1 TiB. The system runs fast during initial testing.
* **The Failure:** Under sustained read/write operations, a small file system consumes bursting credits faster than they regenerate. Once the `BurstCreditBalance` drops to zero, throughput collapses abruptly from 100 MB/s down to baseline (1 MB/s).
* The application appears to experience a mysterious, sudden I/O stall.

### Diagnosis & Fix
* **CloudWatch Metrics:** Monitor `BurstCreditBalance` (trending to zero), `PermittedThroughput`, and `PercentIOLimit`.
* **Fix:** Switch the throughput mode to **Elastic** in the EFS console (takes effect immediately without unmounting).

---

## 10.15 EFS vs EBS: Workload Selection Decision Matrix

| Dimension | Amazon EBS | Amazon EFS |
| :--- | :--- | :--- |
| **Storage Type** | Raw Block Storage | Managed Shared File System (NFSv4) |
| **Availability Scope** | **Single Availability Zone (Single-AZ)** | **Multi-AZ by default** (resilient across AZs) |
| **Access Model** | ReadWriteOnce (RWO): Bound to 1 instance | **ReadWriteMany (RWX):** Mounted by thousands of instances/pods concurrently |
| **Latency** | Sub-millisecond (Direct bus attach) | Low single-digit milliseconds (Network filesystem) |
| **Operating System** | Linux and Windows | **Linux only** (standard POSIX filesystem) |
| **Base Cost** | ~$0.08 / GB-month (`gp3`) | ~$0.30 / GB-month (Standard) |

### Decision Rules
* **Select EBS:** High-performance, latency-critical, single-writer workloads: relational database data files (PostgreSQL, MySQL, MongoDB), OS boot volumes, Kafka broker logs.
* **Select EFS:** Multi-instance shared access: web content management uploads (WordPress, Drupal), shared ML training datasets, persistent shared storage across multi-AZ Kubernetes Pods, Lambda function shared file access.

---

## 10.16 Disabling Console Access for IAM Users

### Cleanest & Fastest Method
Delete the IAM user's **Login Profile** (which removes the password entirely):
```bash
aws iam delete-login-profile --user-name alice
```
Or via Console: **IAM -> Users -> Alice -> Security Credentials -> Console Access -> Disable**.

### Critical Production Caveats (Interview Traps)
1. **Programmatic Access Remains Active:** Deleting the login profile **does NOT revoke API access keys**. The user can still execute CLI, SDK, and Terraform commands. You must explicitly deactivate or delete their Access Keys:
   ```bash
   aws iam update-access-key --user-name alice --access-key-id AKIA... --status Inactive
   ```
2. **Active Sessions Persist:** Existing active console sessions remain valid until their session cookies expire (up to 12 hours). To terminate immediately, attach an inline Deny policy with an `aws:TokenIssueTime` condition:
   ```json
   {
     "Effect": "Deny",
     "Action": "*",
     "Resource": "*",
     "Condition": { "DateLessThan": { "aws:TokenIssueTime": "2026-10-08T00:00:00Z" } }
   }
   ```
3. **Enterprise Standard:** Eliminate long-lived IAM Users entirely. Migrate all human access to **AWS IAM Identity Center (SSO)** backed by Okta or Google Workspace, where deactivating a user in the central IdP revokes all multi-account access instantly.

---

## 10.17 Cross-Account Lambda (Account A) to S3 (Account B)

### The Core Architectural Rule
For cross-account access, **both sides must explicitly allow the action**:
1. Account A must grant its Lambda execution role permission to access the resource.
2. Account B must grant the Lambda role permission on the resource itself.

### Implementation: Bucket Policy Method (Most Common)

```
Account A (Lambda Execution Role)                 Account B (S3 Bucket Policy)
  │                                                    │
  ├── IAM Identity Policy:                             └── S3 Bucket Policy:
      Action: s3:GetObject, s3:PutObject                   Principal: arn:aws:iam::A:role/lambda-role
      Resource: arn:aws:s3:::bucket-b/*                    Action: s3:GetObject, s3:PutObject
                                                           Resource: arn:aws:s3:::bucket-b/*
```

### Production Gotchas to Mention
1. **KMS Key Policy (The #1 Failure):** If Bucket B uses SSE-KMS with a Customer Managed Key (CMK), the KMS Key Policy in Account B must explicitly permit Account A's role (`kms:Decrypt`, `kms:GenerateDataKey`). Bucket policies alone will fail with `Access Denied`.
2. **Object Ownership:** When Account A writes an object into Account B's bucket, Account A owns the object by default unless the bucket has **Bucket Owner Enforced** enabled (disabling legacy S3 ACLs).
3. **Principle of Least Privilege:** Never specify Account A's root ARN (`arn:aws:iam::AccountA:root`) as the principal in the bucket policy; specify the exact Lambda execution role ARN.

---

## 10.18 AWS STS and Temporary Credentials Architecture

### What It Is
**AWS Security Token Service (STS)** is the web service that issues short-lived, auto-expiring temporary security credentials to authenticate AWS API requests, eliminating hardcoded long-lived access keys.

### What STS Returns
* `AccessKeyId` (starts with prefix `ASIA...`)
* `SecretAccessKey`
* `SessionToken` (Mandatory security header included in every signed request)
* `Expiration` (ISO 8601 timestamp)

### Primary STS API Calls
* **`AssumeRole`:** Used for cross-account access, role assumption, and service-to-service privilege escalation.
* **`AssumeRoleWithWebIdentity`:** OIDC federation used by GitHub Actions CI/CD workflows and Kubernetes EKS (IAM Roles for Service Accounts - IRSA).
* **`AssumeRoleWithSAML`:** Enterprise identity federation (Okta, Azure AD, Ping).
* **`GetSessionToken`:** Generates temporary credentials with MFA authentication for IAM users.

### Architectural Limits
* Duration ranges from **15 minutes up to 12 hours** (default: 1 hour).
* **Role Chaining Limit:** If Role A assumes Role B, which then assumes Role C, the maximum session duration is hard-capped at **1 hour**.
* **Confused Deputy Protection:** When allowing third-party SaaS vendors to assume roles into your account, always require an **`ExternalId`** condition in the trust policy.

---

## 10.19 IAM Trust Policy vs Permissions Policy

### The Fundamental Distinction
Every IAM Role consists of two distinct JSON policies answering two distinct security questions:

```
                      [ IAM Role ]
                           │
      ┌────────────────────┴────────────────────┐
      ▼                                         ▼
[ Trust Policy ]                      [ Permissions Policy ]
"WHO can assume this role?"           "WHAT can this role do once assumed?"
Resource-based policy on the role     Identity-based policy attached to the role
Contains "Principal" + sts:AssumeRole Contains "Action" + "Resource"
```

### Examples

#### Trust Policy (The Door bouncer):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "lambda.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

#### Permissions Policy (The House rules):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [ "s3:GetObject", "s3:PutObject" ],
      "Resource": "arn:aws:s3:::my-production-bucket/*"
    }
  ]
}
```

### Triage Rule for Interviews
* If the caller gets `AccessDenied` on `sts:AssumeRole`: Check the **Trust Policy** (and the caller's permission to call `AssumeRole`).
* If the caller successfully assumes the role but gets `AccessDenied` reading S3 or querying DynamoDB: Check the **Permissions Policy**, SCPs, or resource policies.

---

## 10.20 Cross-Account Lambda (Account A) to DynamoDB (Account B)

### Option 1: Assume a Role in Account B (Universal Pattern)
1. **Account B:** Create an IAM role (`DDBAccessRole`).
   * *Trust Policy:* Allows Account A's Lambda execution role to call `sts:AssumeRole`.
   * *Permissions Policy:* Grants `dynamodb:GetItem`, `dynamodb:PutItem`, `dynamodb:Query` on the target table ARN.
2. **Account A:** Lambda execution role has permission to call `sts:AssumeRole` targeting the Account B role ARN.
3. **Lambda Code:**
   * Lambda calls `sts.assumeRole({ RoleArn: 'arn:aws:iam::B:role/DDBAccessRole', RoleSessionName: 'LambdaDDB' })`.
   * Uses the returned temporary credentials (`ASIA...`) to instantiate the DynamoDB client.
   * *Performance Rule:* **Cache the STS credentials in global memory** until near expiration; never call `AssumeRole` on every single invocation.

### Option 2: DynamoDB Resource-Based Policy (Modern & Clean)
DynamoDB supports resource-based policies directly on tables:
1. **Account B:** Attach a resource policy directly to the DynamoDB table granting permissions to Account A's Lambda role ARN.
2. **Account A:** Lambda role has identity permissions to call DynamoDB actions.
3. **Lambda Code:** Queries the table directly using the **full table ARN** (`arn:aws:dynamodb:region:B:table/TableName`) as the `TableName` parameter. No STS role-hopping required.

---

## 10.21 Disadvantages of EBS in Multi-AZ Kubernetes

### The Root Conflict
**EBS volumes are physical block devices locked to a single Availability Zone.**

### The 5 Architectural Failures in Kubernetes
1. **Pod Rescheduling Stalls (`volume node affinity conflict`):** A StatefulSet Pod bound to an EBS volume in `us-east-1a` can only ever be scheduled on a node in `us-east-1a`. If `us-east-1a` experiences a node failure, capacity shortage, or outage, Kubernetes cannot reschedule the Pod onto healthy nodes in `us-east-1b` or `us-east-1c`. The Pod remains permanently stuck in `Pending`.
2. **AZ Failure Data Blackout:** If an entire AWS Availability Zone experiences an outage, data residing on EBS volumes in that AZ is completely inaccessible until the AZ recovers.
3. **Slow Failover Detach/Attach Latency:** When a Kubernetes node dies ungracefully, the AWS control plane must wait for timeout periods before forcing the EBS volume detach. Reattaching to a new node takes several minutes, inflating service Recovery Time Objective (RTO).
4. **ReadWriteOnce (RWO) Limitation:** Standard EBS volumes cannot be mounted simultaneously by multiple Pods across different nodes.
5. **Immediate Volume Binding Mistake:** If a StorageClass uses `volumeBindingMode: Immediate`, the EBS volume is provisioned in a random AZ *before* the Pod is assigned to a node, frequently causing scheduling mismatches.

### Production Mitigations
* Set `volumeBindingMode: WaitForFirstConsumer` so the PVC is provisioned in the exact AZ where the scheduler assigns the Pod.
* Use **Amazon EFS** (via the AWS EFS CSI Driver) for ReadWriteMany (RWX) shared storage across AZs.
* For distributed databases (Kafka, Cassandra, PostgreSQL operators), replicate data at the **application layer** across independent single-AZ EBS volumes using Kubernetes Topology Spread Constraints.

---

## 10.22 AWS Secrets Manager vs SSM Parameter Store

### Architectural Comparison

| Dimension | AWS Secrets Manager | SSM Parameter Store |
| :--- | :--- | :--- |
| **Primary Purpose** | Sensitive credentials requiring automatic rotation | Configuration parameters and static secrets |
| **Automated Rotation** | **Native integration** with RDS, Redshift, DocumentDB via Lambda | No built-in rotation (requires custom Lambda/EventBridge) |
| **Pricing** | **$0.40 per secret per month** + $0.05 per 10k API calls | **Standard tier is FREE**; Advanced tier is $0.05 per secret |
| **Maximum Size** | Up to 64 KB | 4 KB (Standard) / 8 KB (Advanced) |
| **Cross-Region Replication** | Built-in native multi-region secret replication | Manual replication required |
| **Encryption** | Always encrypted via KMS | Optional (String, StringList, or encrypted `SecureString`) |

### Production Selection Rule
* **Use SSM Parameter Store:** For application configuration, feature flags, API base URLs, environment variables, and non-rotating secrets where the free tier saves thousands in cost.
* **Use Secrets Manager:** For database master credentials, third-party API tokens with compliance-mandated rotation policies, and secrets requiring cross-account or multi-region replication.
* **Application Caching:** Always cache secrets in application memory using client SDKs or the AWS Parameters and Secrets Lambda Extension. Never call `GetSecretValue` on every incoming HTTP request.

---

## 10.23 Production Database Operational Tasks & Maintenance

### The Platform Engineer's Positioning (Not a DBA)
"I do not write application schemas or business queries—that is the product developers' domain. My job is **Database Reliability & Platform Hygiene**: protecting the database from bad application traffic, protecting application runtimes from database stalls, and guaranteeing disaster recovery."

### The 5 Operational Pillars (Detailed Implementation Breakdown)

#### 1. Automated Backups & Monthly PITR Restore Drills
* **The SRE Principle:** A backup you have never restored is not a backup.
* **Continuous Backups:** AWS RDS and MongoDB Atlas continuous automated snapshots with a 30-day retention window.
* **The Monthly Drill:**
  1. Trigger automated snapshot restore to a point-in-time (e.g. 2 hours prior) into a temporary isolated instance (`staging-dr-test`).
  2. Run automated validation queries checking record counts and the latest transaction timestamp against audit logs to benchmark **RPO (< 5 minutes)**.
  3. Measure elapsed clock time from restore trigger to database `available` status to benchmark **RTO (~22 minutes)**.
  4. Automatically teardown test instance via Terraform to eliminate cloud waste.

#### 2. Slow Query Profiling to Eliminate `COLLSCAN` / Table Scans
* **Detection Threshold:** Configured MongoDB Profiler (`slowms: 100`) and PostgreSQL `log_min_duration_statement = 200ms`.
* **The Forensic Metric:** High `docsExamined` vs `nReturned` ratio (e.g. examining 60,000 documents to return 3 results). Signature of an unindexed `COLLSCAN` (collection scan) pinning database CPU at 90%+.
* **Platform Triage:** Generate execution plan via `.explain("executionStats")`, isolate the query fingerprint, and flag in a Jira ticket with the recommended compound index covering filter fields (e.g. `{ status: 1, created_at: -1 }`). Dropped query latency from 850ms to 4ms and CPU from 85% to 20%.

#### 3. Application-Level Query Guardrails (`pageSize <= 100`, `.lean()`)
* **Why Platform Cares:** Unbounded queries trigger fatal **runtime memory crashes**.
* **The Root Cause:** In our Node.js/Mongoose microservices, requesting `pageSize=10000` instantiated 10,000 heavy Mongoose document instances (with change tracking and getters/setters), consuming >1 GB heap and triggering a fatal V8 garbage collection OOM panic.
* **The Safeguards:**
  1. Clamped query bounds in the controller: `const pageSize = Math.min(Math.max(Number(req.query.pageSize) || 20, 1), 100);`.
  2. Enforced `.lean()` on read-only queries. Returns plain JavaScript objects rather than full Mongoose instances, slashing memory allocation by ~80% and eliminating GC pauses.

#### 4. Client Connection Pool Sizing to Prevent Socket Exhaustion
* **The Common Outage:** Default connection pool settings (e.g. 50-100 per service). 4 EC2 instances running 4 PM2 workers = 16 Node processes. 16 * 50 = 800 connections. Database `max_connections` (typically 300-400) exhausts, dropping all new requests with `too many connections`.
* **The Platform Sizing Formula:**
  $$\text{Pool Size Per Worker} = \frac{\text{DB Max Connections} \times 0.7}{\text{Total Node Processes}}$$
* **Implementation:** Capped `maxPoolSize = 10` per worker (16 * 10 = 160 connections, leaving 30% headroom for migrations and admin access) or fronted with RDS Proxy / PgBouncer.

#### 5. Zero-Downtime Database Credential Rotation via AWS Secrets Manager
* **Architecture:** AWS Secrets Manager with native rotation Lambda using the **Two-User / Alternating Strategy**:
  1. Database maintains two users: `app_user_a` and `app_user_b` with identical permissions. Active secret points to `app_user_a`.
  2. Rotation triggers every 90 days: Lambda generates a new password for inactive user `app_user_b`, runs `ALTER USER`, updates Secret, and marks it current.
  3. Microservices catch authentication error on reconnect, fetch updated secret from Secrets Manager, and seamlessly reconnect with `app_user_b`.
  4. Queries on `app_user_a` drain gracefully. Zero downtime, zero service restarts.

---

## 10.24 Production Lambda Architectural Patterns & Hardening

### Core Production Architectures
1. **Asynchronous Webhook Ingestion:** API Gateway -> SQS Queue -> Lambda Worker. Buffers bursty inbound traffic, completely decoupling incoming request rate from database concurrency limits.
2. **S3 Event-Driven Processing:** S3 Object Upload (`s3:ObjectCreated:*`) -> Event Notification -> Lambda Function (validates metadata, generates image thumbnails, updates database).
3. **SQS Batch Processing with Partial Failure:** SQS -> Lambda consumer with `ReportBatchItemFailures` enabled. If 2 out of 10 batch items fail, only the 2 failed items return to the queue for retry; the 8 successful messages are deleted.
4. **Scheduled Infrastructure Automation:** Amazon EventBridge Scheduler -> Lambda (audits unattached EBS volumes, identifies open security group rules, purges expired test environments).

### Production Hardening Guidelines
* **Idempotency:** Because AWS Lambda executes with *at-least-once delivery*, functions processing payments or ledger updates must be strictly idempotent. Use an idempotency key stored in DynamoDB with a TTL.
* **Dead Letter Queues (DLQ):** Always attach an SQS DLQ to asynchronous Lambda functions and event sources to capture poison-pill payloads after maximum retry attempts.
* **Reserved Concurrency:** Set reserved concurrency on functions touching relational databases to prevent a serverless traffic surge from exhausting database connection pools.
* **Structured Logging & Tracing:** Use **AWS Lambda Powertools** to output structured JSON logs with correlation IDs (`request_id`) and enable AWS X-Ray tracing for distributed latency visibility.

---

## 10.25 IAM User vs IAM Role: Security Posture

### Architectural Comparison

| Dimension | IAM User | IAM Role |
| :--- | :--- | :--- |
| **Identity Type** | Represents a specific human or system | An assumable identity with no permanent credentials |
| **Credential Nature** | **Long-lived credentials** (static password, access key ID + secret key) | **Short-lived, temporary credentials** issued by AWS STS (auto-expire) |
| **Typical Use Case** | Legacy systems, emergency break-glass account | AWS services (EC2, Lambda, ECS), cross-account access, SSO |
| **Security Risk** | High: Access keys are frequently committed to git or leaked in logs | **Near zero:** Credentials expire within 15m–1h; nothing static to leak |

### The Production Security Standard
* **Humans:** Never create individual IAM Users. Federate all human access through **AWS IAM Identity Center (SSO)** using centralized corporate identity providers (Google Workspace, Okta, Azure AD).
* **Workloads:** Workloads running on AWS must assume **IAM Roles**:
  * EC2 instances use **Instance Profiles**.
  * Containers on ECS use **ECS Task Roles**.
  * Pods on Kubernetes EKS use **IAM Roles for Service Accounts (IRSA)**.
  * Lambda functions use **Lambda Execution Roles**.
* **CI/CD Pipelines:** Modern pipelines (GitHub Actions, GitLab CI) use **OIDC Federation** to assume an IAM role dynamically via `sts:AssumeRoleWithWebIdentity`, eliminating static AWS keys in repository secrets.
* **The Golden Rule:** *"IAM Users are who you are; IAM Roles are what you temporarily become."*
