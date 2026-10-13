# Terraform Mastery: 11 Production Questions & Model Answers

A complete, first-principles interview and operational guide covering Terraform HCL, state management mechanics, concurrency locking, remote backends, enterprise governance, OpenTofu divergence, and production-grade examples.

---

## Table of Contents
1. [6.1 `for_each` vs `for` in Terraform](#61-for_each-vs-for-in-terraform)
2. [6.2 Modules in Terraform and Architectural Boundaries](#62-modules-in-terraform-and-architectural-boundaries)
3. [6.3 Role and Lifecycle of the Terraform Statefile](#63-role-and-lifecycle-of-the-terraform-statefile)
4. [6.4 Storing Statefile in Git vs S3 / Remote Backend](#64-storing-statefile-in-git-vs-s3--remote-backend)
5. [6.5 Statefile Management, Refresh, and Infrastructure Drift](#65-statefile-management-refresh-and-infrastructure-drift)
6. [6.6 Concurrent Applies and Distributed State Locking](#66-concurrent-applies-and-distributed-state-locking)
7. [6.7 Storing Statefile On-Premises Without Cloud Accounts](#67-storing-statefile-on-premises-without-cloud-accounts)
8. [6.8 Terraform Community vs Terraform Enterprise (HCP Terraform)](#68-terraform-community-vs-terraform-enterprise)
9. [6.9 OpenTofu vs Terraform: The BSL Fork and Feature Divergence](#69-opentofu-vs-terraform-the-bsl-fork-and-feature-divergence)
10. [6.10 Production Terraform Code: Secure AWS Architecture](#610-production-terraform-code-secure-aws-architecture)
11. [6.11 Resource vs Data Source in Terraform](#611-resource-vs-data-source-in-terraform)

---

## 6.1 `for_each` vs `for` in Terraform

> **The Interview Question:**  
> "What is the difference between `for_each` and `for` in Terraform, and when would you choose one over the other or over `count`?"

### 30-Second Interview Answer
`for_each` is a **meta-argument** applied to `resource`, `data`, or `module` blocks to create multiple distinct, addressable infrastructure instances from a map or set of strings. 

`for` is an **expression** (a comprehension) used inside an attribute to transform or filter one data structure into another (such as filtering a list of subnets or transforming a map of tags). 

We choose `for_each` over `count` for resource creation because `count` binds resources to integer indices (`aws_subnet.public[0]`). If an item is deleted from the middle of the list, `count` causes infrastructure churn and replacement risk.

### Deep-Dive Systems Explanation

```
Input Data: Map of 3 Subnets {"us-east-1a", "us-east-1b", "us-east-1c"}

[ count ]    --> Binds to Array Indices: [0], [1], [2]
                 Removing "us-east-1b" shifts [2] to [1]
                 Result: Destroys and recreates subnet [2]!

[ for_each ] --> Binds to Stable String Keys: ["us-east-1a"], ["us-east-1b"], ["us-east-1c"]
                 Removing "us-east-1b" only destroys key ["us-east-1b"]
                 Result: Zero impact on ["us-east-1a"] and ["us-east-1c"].
```

#### Code Example: Combining `for` and `for_each`
```hcl
variable "subnets" {
  type = map(object({
    cidr_block = string
    az         = string
    public     = bool
  }))
  default = {
    "public-1"  = { cidr_block = "10.0.1.0/24", az = "us-east-1a", public = true }
    "public-2"  = { cidr_block = "10.0.2.0/24", az = "us-east-1b", public = true }
    "private-1" = { cidr_block = "10.0.10.0/24", az = "us-east-1a", public = false }
  }
}

# 'for' expression filters the map to only public subnets
# 'for_each' meta-argument creates resources for each entry in the filtered map
resource "aws_subnet" "public" {
  for_each = {
    for k, v in var.subnets : k => v if v.public
  }

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr_block
  availability_zone = each.value.az

  tags = {
    Name = each.key
  }
}
```

### Production War Story & Pitfall
* **The `count` Array Shift Outage:** A team deployed 6 EC2 instances using `count = length(var.instances)`. An engineer deleted the second instance from the variable list. Because the list indices shifted, Terraform destroyed and recreated the downstream resources attached to the later items, causing an outage and forcing a replacement of a production database node.

---

## 6.2 Modules in Terraform and Architectural Boundaries

> **The Interview Question:**  
> "What are modules in Terraform, why should an enterprise use them, and what are the major anti-patterns when designing them?"

### 30-Second Interview Answer
Modules are self-contained packages of Terraform configurations comprising `variables.tf`, `main.tf`, and `outputs.tf` that manage a specific group of related resources. 

Enterprises use modules to enforce **architectural reusability, security baselines, and blast-radius isolation**. Instead of developers directly writing raw `aws_s3_bucket` resources, they call a versioned, reviewed module that enforces networking, tagging, encryption, and lifecycle constraints.

### Deep-Dive Systems Explanation

#### Module Anatomy & Contracts
* **Inputs (`variables.tf`):** The external API of the module. Validates types, required values, and constraints.
* **Outputs (`outputs.tf`):** Exposes resource IDs and attributes for downstream consumption.
* **Encapsulation:** Internal resources inside the child module are invisible to the root module unless explicitly exported via outputs.

```
                    Root Module (Environment / Live State)
                                    │
           ┌────────────────────────┼────────────────────────┐
           ▼                        ▼                        ▼
  [ module.networking ]    [ module.security_groups ] [ module.compute ]
   - VPC                    - Ingress Rules            - AutoScaling
   - Route Tables           - Egress Rules             - Launch Templates
```

### Production Anti-Patterns & Best Practices
1. **The "God Module" Anti-Pattern:** Bundling VPC, EKS, RDS, and Redis into a single monolithic module. Planning takes 30 minutes, blast radius is catastrophic, and a syntax error in Redis halts unrelated changes.
2. **The Pass-Through Anti-Pattern:** Creating a module that merely wraps a single resource with 50 pass-through variables. A module should represent an **architectural pattern**, not a 1:1 mirror of every provider argument.
3. **Version Pinning:** Always pin modules using Git tags (`source = "git::https://github.com/org/terraform-aws-vpc.git?ref=v2.1.0"`) to prevent untested upstream changes from breaking automated pipelines.

---

## 6.3 Role and Lifecycle of the Terraform Statefile

> **The Interview Question:**  
> "What is the precise purpose of the `terraform.tfstate` file, why is it mandatory for a declarative engine, and what metadata does it store?"

### 30-Second Interview Answer
The Terraform statefile is a single source of truth that maps declarative HCL resource declarations to physical real-world cloud identifiers (such as an AWS ARN, VPC ID, or EC2 instance ID). 

It is mandatory because cloud provider APIs are **imperative**. If you delete a resource block from your HCL file, Terraform cannot know by reading the configuration alone whether that resource never existed, was intentionally removed, or was destroyed outside Terraform.

### Deep-Dive Systems Explanation

#### Why State is Required for Declarative Systems
1. **Mapping Configuration to Physical Reality:** HCL declares `resource "aws_vpc" "main" {}`. AWS returns `vpc-01a2b3c4d5e6f7g8h`. The state file records: `aws_vpc.main` ↔ `vpc-01a2b3c4d5e6f7g8h`
2. **Destruction Tracking:** If you remove `resource "aws_vpc" "main"` from code, Terraform inspects the statefile, sees that `vpc-01a2b...` exists in state but is absent in code, and emits a `Destroy` plan.
3. **Dependency Graph Resolution:** State stores pointers to ensure resources are destroyed in reverse order of creation.
4. **Performance Caching:** For large architectures (thousands of resources), querying AWS APIs for every single resource attribute on every plan would trigger cloud API rate limiting (HTTP 429).

#### Sensitive Data Risk
The statefile stores all resource attributes in **plaintext JSON**, including:
* Database master passwords (`aws_db_instance.password`).
* TLS private keys (`tls_private_key`).
* IAM access keys.

Statefiles must never be committed to Git or left unencrypted on local disks.

---

## 6.4 Storing Statefile in Git vs S3 / Remote Backend

> **The Interview Question:**  
> "Why is storing the Terraform statefile in Git an immediate failure in a production environment, and how does an S3 + DynamoDB remote backend solve this?"

### 30-Second Interview Answer
Storing statefiles in Git is a critical security vulnerability and operational hazard. First, statefiles contain plaintext secrets (passwords, tokens, private keys) which permanently pollute Git history. Second, Git has no distributed locking semantics, so concurrent applies can overwrite each other or corrupt state.

A production remote backend using **Amazon S3 and DynamoDB** isolates state: S3 provides server-side KMS encryption, versioning (for instant rollback), and strict IAM access boundaries, while DynamoDB provides atomic distributed locking to serialize applies.

### Deep-Dive Systems Explanation

| Comparison Matrix | Git Repository | Amazon S3 + DynamoDB |
| :--- | :--- | :--- |
| **Secrets Security** | High Risk: Plaintext passwords committed to Git history. | Secure: S3 SSE-KMS encryption, private bucket, bucket policy. |
| **Concurrency / Locking** | None: Merge conflicts result in corrupted JSON state. | Atomic Distributed Lock: DynamoDB conditional writes prevent dual apply. |
| **State Versioning** | Commits pollute repository; manual rollbacks risky. | Native S3 Object Versioning: Every state write creates a point-in-time recovery backup. |
| **Access Control** | Anyone with repo read access sees all infrastructure secrets. | Least Privilege IAM: Only the CI/CD pipeline role has S3 read/write permissions. |

#### Production Remote Backend Architecture
```hcl
terraform {
  required_version = ">= 1.5.0"

  backend "s3" {
    bucket         = "corp-production-terraform-state-us-east-1"
    key            = "networking/vpc/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-locks"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:us-east-1:123456789012:key/state-encryption-key"
  }
}
```

---

## 6.5 Statefile Management, Refresh, and Infrastructure Drift

> **The Interview Question:**  
> "What is infrastructure drift, how does Terraform detect and reconcile it, and how do you recover if a resource is modified manually in the AWS Console?"

### 30-Second Interview Answer
**Infrastructure drift** occurs when the actual state of live cloud infrastructure diverges from the declarative HCL configuration, typically due to manual console edits, emergency hotfixes, or automation outside Terraform.

Terraform detects drift during `terraform plan` via the **Refresh phase**. It queries cloud provider APIs using the identifiers recorded in state, updates the statefile to reflect real-world attributes, and then compares the refreshed state to the desired configuration.

### Deep-Dive Systems Explanation

```
[ Local HCL Code ] ──────────────┐
                                 ▼
[ Live Cloud Infrastructure ] ──▶ [ Refresh ] ──▶ [ Updated State ] ──▶ [ Plan Diff ]
```

#### Reconciling Drift: The Three Strategies
1. **Enforce Declarative Authority (Overwrite Drift):**
   * Run `terraform plan` and `terraform apply`. Terraform detects that a security group rule was added manually and issues a `Delete` API call to restore code compliance.
2. **Adopt the Drift into Code:**
   * If the console hotfix was legitimate, update the HCL code to match the new live configuration. Running `terraform plan` yields `No changes. Your infrastructure matches the configuration.`
3. **Ignore Known Dynamic Attributes:**
   * For attributes managed by external systems (e.g. `desired_capacity` managed by Kubernetes Cluster Autoscaler):
     ```hcl
     resource "aws_autoscaling_group" "workers" {
       # ...
       lifecycle {
         ignore_changes = [desired_capacity, tag]
       }
     }
     ```

#### Advanced State Manipulation Tools
* `terraform state rm <address>`: Drops a resource from state management without deleting it from the cloud.
* `terraform import <address> <id>`: Binds an existing live cloud resource into state management.
* `terraform state mv <source> <destination>`: Renames a resource block in HCL without destroying and recreating the live resource.

---

## 6.6 Concurrent Applies and Distributed State Locking

> **The Interview Question:**  
> "What happens when two engineers run `terraform apply` simultaneously on the same environment, and how does DynamoDB state locking prevent disaster?"

### 30-Second Interview Answer
If two engineers run `terraform apply` concurrently without state locking, a race condition occurs. Both processes read the same initial state, issue conflicting API calls to the cloud provider, and create non-deterministic drift.

DynamoDB prevents this by acting as a **distributed mutex**. Before planning or applying, Terraform acquires a lock by executing a conditional write to DynamoDB (`LockID = <state_path>`). If a second apply tries to lock the same state, it fails with a conditional write error and exits.

### Deep-Dive Systems Explanation

```
Engineer A: terraform apply                           Engineer B: terraform apply
        │                                                     │
        ▼                                                     ▼
Acquires DynamoDB Lock                                Tries to Acquire DynamoDB Lock
Status: 200 OK (Lock Acquired)                        Status: 400 ConditionalCheckFailedException
        │                                                     │
Runs Plan & API Modifications                         Terminates immediately:
        │                                             "Error: Error acquiring the state lock"
Writes Updated State to S3
        │
Releases DynamoDB Lock
```

#### Lock Item Structure in DynamoDB
When a lock is held, DynamoDB stores an item with:
* `LockID`: S3 bucket name and key path (Partition Key).
* `Info`: JSON payload containing:
  * `ID`: A unique UUID.
  * `Operation`: `OperationTypeApply` or `OperationTypePlan`.
  * `Who`: `username@hostname`.
  * `Created`: UTC timestamp.

#### Handling Stale / Dead Locks
If a CI/CD runner crashes or an engineer’s machine disconnects during an apply, the lock remains in DynamoDB:
```bash
# Verify no CI runner or peer is running the apply:
aws dynamodb get-item --table-name terraform-state-locks --key '{"LockID": {"S": "networking/vpc/terraform.tfstate"}}'

# Safely force release the lock using the specific lock ID:
terraform force-unlock 17d84f89-8b43-41a2-9d32-e3d81b4d89a1
```

---

## 6.7 Storing Statefile On-Premises Without Cloud Accounts

> **The Interview Question:**  
> "If an organization runs Terraform exclusively on bare-metal or private VMware/OpenStack infrastructure without AWS/GCP/Azure accounts, where and how do you store the statefile securely with state locking?"

### 30-Second Interview Answer
Without public cloud accounts, organizations use **self-hosted HTTP, Consul, or PostgreSQL remote backends**:

1. **GitLab Managed Terraform State (HTTP Backend):** If GitLab is hosted on-premises, its native HTTP Terraform State backend provides built-in state versioning, RBAC, and atomic state locking via backend-native semantics.
2. **HashiCorp Consul Backend:** An on-premises Consul cluster stores state in its KV store and uses native **Consul Distributed Sessions** to provide mutual exclusion locking.
3. **PostgreSQL Backend:** Stores state rows in a dedicated table using Postgres row-level locks for concurrency control.
4. **On-Premises MinIO (S3-compatible):** Running MinIO on-prem provides an S3 API interface, paired with an on-premises Postgres or Redis service for locking.

### Deep-Dive Systems Explanation

#### Implementation 1: HashiCorp Consul Backend
```hcl
terraform {
  backend "consul" {
    address = "consul.internal.corp:8500"
    scheme  = "https"
    path    = "terraform/state/datacenter-1"
    # Native distributed lock via Consul sessions:
    lock    = true
  }
}
```

#### Implementation 2: Native PostgreSQL Backend
```hcl
terraform {
  backend "pg" {
    conn_str = "postgres://tf_user:SecurePassword@pg-cluster.internal.corp:5432/tf_state?sslmode=require"
    # Creates and manages a dedicated table with native row locking:
    schema_name = "production"
  }
}
```

---

## 6.8 Terraform Community vs Terraform Enterprise (HCP Terraform)

> **The Interview Question:**  
> "What is the difference between open-source/community Terraform CLI and Terraform Enterprise / HCP Terraform, and what problems does the enterprise tier solve?"

### 30-Second Interview Answer
Terraform Community is a standalone CLI binary where all execution, state coordination, secret management, and cloud access credentials run locally on the engineer’s workstation or within custom CI runners.

Terraform Enterprise (and HCP Terraform) is a centralized platform that solves **governance, security, and fleet collaboration**:
1. **Remote Execution:** Runs occur on isolated worker agents, eliminating credentials on developer laptops.
2. **Policy as Code (Sentinel / OPA):** Hard guardrails that validate code *before* apply (e.g. blocking unencrypted S3 buckets).
3. **Private Module Registry:** Internal, versioned module catalogs with RBAC.
4. **Drift Detection & Cost Estimation:** Automated continuous drift scanning and AWS spend forecasting.

### Deep-Dive Systems Explanation

| Architectural Dimension | Community CLI | Terraform Enterprise / HCP |
| :--- | :--- | :--- |
| **Execution Plane** | Local workstation or DIY CI runner (Jenkins/GitHub Actions). | Managed, containerized execution workers with audit logging. |
| **Credential Storage** | Developer machines or CI environment variables. | Dynamic short-lived credentials via Vault or OIDC integration. |
| **Policy Enforcement** | External linters (tflint, checkov) run manually in CI. | Native Sentinel / Open Policy Agent (OPA) gates that block applies. |
| **State Storage** | Configured manually (S3, DynamoDB, GCS). | Fully managed, encrypted state store with native audit trail. |
| **Cost Estimation** | Manual integration with Infracost. | Built-in speculative plan cost estimation. |

---

## 6.9 OpenTofu vs Terraform: The BSL Fork and Feature Divergence

> **The Interview Question:**  
> "What led to the creation of OpenTofu, what is the architectural difference between OpenTofu and Terraform today, and how do you evaluate migrating between them?"

### 30-Second Interview Answer
In August 2023, HashiCorp shifted Terraform from the open-source **MPL 2.0** license to the **BSL 1.1 (Business Source License)**, which prohibits using the binary to build competing commercial hosting offerings without additional licensing.

Architecturally, OpenTofu remains a drop-in replacement for Terraform configuration syntax, but has diverged by introducing:
1. **Native Client-Side State Encryption:** Directly encrypts statefiles in HCL using AWS KMS, GCP KMS, or AES-GCM before writing to the remote backend.
2. **Decoupled Registry:** Points by default to `registry.opentofu.org`.
3. **Dynamic Provider Iteration:** Enhanced language capabilities for provider iteration.

### Deep-Dive Systems Explanation

#### Key Architectural Divergence: Native State Encryption
In standard Terraform, the backend (e.g., S3) handles encryption at rest. If someone gains read permissions to the S3 bucket or intercepts the network stream, the state file is vulnerable. OpenTofu adds client-side encryption support directly in the engine, making the state unreadable without the configured KMS keys.

```hcl
# OpenTofu Native Encryption Block (tofu >= 1.7)
terraform {
  encryption {
    key_provider "aws_kms" "production_key" {
      kms_key_id = "arn:aws:kms:us-east-1:123456789012:key/my-key"
      region     = "us-east-1"
    }

    method "aes_gcm" "state_encryption" {
      keys = key_provider.aws_kms.production_key
    }

    state {
      method = method.aes_gcm.state_encryption
      enforced = true
    }
  }
}
```

---

## 6.10 Production Terraform Code: Secure AWS Architecture

> **The Interview Question:**  
> "Write production-ready Terraform code implementing a hardened AWS VPC, private subnet, and encrypted S3 bucket following enterprise security standards."

### 30-Second Interview Answer
Production infrastructure code must adhere to four immutable standards:
1. **No Hardcoded Values:** Parameterize regions, CIDRs, and naming through strict variable typing and validation.
2. **Explicit Provider Pinning:** Constrain provider versions in `terraform {}` to prevent breaking upstream updates.
3. **Zero Plaintext Storage:** Enforce KMS encryption, block public access, and enable versioning on all storage primitives.
4. **Least-Privilege Resource Policies:** Restrict bucket policies to TLS 1.2+ enforceability.

### Production HCL Implementation

#### File 1: `versions.tf`
```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "Platform-Engineering"
    }
  }
}
```

#### File 2: `variables.tf`
```hcl
variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Target AWS deployment region."
}

variable "environment" {
  type        = string
  description = "Deployment tier (production, staging)."
  validation {
    condition     = contains(["production", "staging"], var.environment)
    error_message = "Environment must be production or staging."
  }
}

variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "Base VPC CIDR block."
}

variable "private_subnet_cidr" {
  type        = string
  default     = "10.0.10.0/24"
  description = "Isolated private subnet CIDR."
}
```

#### File 3: `main.tf`
```hcl
# 1. Hardened Base VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.environment}-vpc"
  }
}

# 2. Isolated Private Subnet (No Internet Gateway route)
resource "aws_subnet" "private" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.private_subnet_cidr
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = false

  tags = {
    Name = "${var.environment}-private-subnet-1a"
    Tier = "Private"
  }
}

# 3. Dedicated Route Table for Private Subnet
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.environment}-private-rt"
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

# 4. KMS Customer Managed Key for Storage Encryption
resource "aws_kms_key" "storage_key" {
  description             = "KMS Key for ${var.environment} S3 Bucket encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Name = "${var.environment}-s3-kms-key"
  }
}

# 5. Production Hardened S3 Bucket
resource "aws_s3_bucket" "secure_storage" {
  bucket_prefix = "${var.environment}-secure-data-"
  force_destroy = false
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.secure_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {
  bucket = aws_s3_bucket.secure_storage.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.storage_key.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

# Absolute Public Access Block
resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.secure_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enforce TLS 1.2+ In Transit
resource "aws_s3_bucket_policy" "enforce_tls" {
  bucket = aws_s3_bucket.secure_storage.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnforceTLSRequestsOnly"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.secure_storage.arn,
          "${aws_s3_bucket.secure_storage.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}
```

#### File 4: `outputs.tf`
```hcl
output "vpc_id" {
  description = "The ID of the provisioned VPC."
  value       = aws_vpc.main.id
}

output "private_subnet_id" {
  description = "The ID of the private subnet."
  value       = aws_subnet.private.id
}

output "s3_bucket_arn" {
  description = "The ARN of the secure S3 bucket."
  value       = aws_s3_bucket.secure_storage.arn
}
```

---

## 6.11 Resource vs Data Source in Terraform

> **The Interview Question:**  
> "What is the fundamental difference between a `resource` block and a `data` source block in Terraform, and how do they enable architectural decoupling?"

### 30-Second Interview Answer
A `resource` block represents a **managed mutation**: it instructs Terraform to create, update, or destroy infrastructure, binding its complete lifecycle to the Terraform state. 

A `data` source block represents an **external query**: it reads pre-existing infrastructure attributes from the cloud provider API in a read-only fashion, without managing or altering its lifecycle.

Data sources enable **architectural decoupling and blast-radius isolation**. A central networking team can manage a corporate VPC in one repository, while independent application teams read the VPC ID, route tables, and subnet IDs without creating or destroying the shared network.

### Deep-Dive Systems Explanation

```
[ Networking Team Repo ] ──▶ Creates: resource "aws_vpc" "shared" ──▶ AWS API (vpc-12345)
                                                                            │
[ Application Team Repo ] ─▶ Queries: data "aws_vpc" "selected"  ◀─────────┘
                             (Read-Only: Zero lifecycle control)
```

#### Code Example: Decoupled Architectural Lookup
```hcl
# Query the most recent hardened Amazon Linux 2023 AMI without hardcoding AMI IDs
data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Query an existing shared VPC managed by the Platform Team
data "aws_vpc" "platform_shared" {
  filter {
    name   = "tag:Environment"
    values = ["production"]
  }
}

# Create an application instance referencing read-only data sources
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.al2023.id
  instance_type = "t3.medium"
  # Referenced from read-only data source:
  subnet_id     = tolist(data.aws_subnets.private.ids)[0]

  tags = {
    Name = "app-server-prod"
  }
}
```

---
