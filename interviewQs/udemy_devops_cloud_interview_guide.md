# Ultimate DevOps and Cloud Interview Guide — All Questions in Course Order

| | |
|---|---|
| Course | [Ultimate Devops And Cloud Interview Guide](https://www.udemy.com/course/ultimate-devops-and-cloud-interview-guide/) |
| Instructor | Abhishek Veeramalla |
| Curriculum | 13 sections • 182 lectures • 15:26:53 |
| Target Month | October 2026 Interview Blitz |

---

## Strategic October Filtering (Priority Buckets)

* **Tier 1 (Hardcore Daily Focus - 75% of Time):**
  * Section 10: AWS (25 items • 1:49:38)
  * Section 8: Kubernetes (35 items • 3:19:39)
  * Section 6: Terraform (11 items • 59:01)
  * Section 12: Python Automation (3 items • 25:01)
* **Tier 2 (Rapid Review / Verification - 25% of Time):**
  * Section 3: Linux (17 items • 1:51:28)
  * Section 4: Networking (9 items • 33:41)
  * Section 7: Docker (12 items • 54:01)
  * Section 9: Observability (11 items • 57:14)
  * Section 13: SDLC & Experience Delivery (5 items • 22:11)
* **Tier 3 (Skip for Now / Non-Core):**
  * Section 11: Azure (15 items • 1:07:30) — Focus is 100% on AWS.
  * Section 2: Git (Skim only for rebase/merge and secret revocation).

---

## 1. Introduction (3 items • 5:23)
* 1.1 Introduction
* 1.2 Special Instructions for the learners
* 1.3 GitHub repository link for the course

---

## 2. Git (21 items • 1:51:19)
* 2.1 Git Fork vs Git Clone
* 2.2 Scenario where you used Git Fork instead of Git Clone
* 2.3 Git Fork in action with example
* 2.4 Create a fork and pull request
* 2.5 Git Fetch vs Git Pull
* 2.6 Realtime Git Fetch and Pull
* 2.7 Git Fetch vs Git Pull: which and why
* 2.8 Practice Git Fetch vs Git Pull
* 2.9 Git Rebase vs Git Merge Detailed
* 2.10 Practical difference between Rebase and Merge
* 2.11 How to explain Git Merge vs Git Rebase in Interviews
* 2.12 Practice Git Merge vs Git Rebase
* 2.13 Git Branching Strategy in production
* 2.14 3 challenges faced with Git
* 2.15 Recent challenge faced with Git
* 2.16 How do you handle Merge conflicts
* 2.17 Git Merge Strategies: Ours and Theirs
* 2.18 Create and address merge conflict locally
* 2.19 Purpose and usage of Git tags
* 2.20 Combining multiple commits into a single commit (squash)
* 2.21 10 Git commands used day-to-day
* 2.22 Ignoring pushing changes to a file
* 2.23 Purpose of .git folder
* 2.24 Restoring a deleted .git folder
* 2.25 Accidentally committed a Kubernetes Secret to Git (BFG, rotation)

---

## 3. Linux (17 items • 1:51:28)
* 3.1 10 Linux commands used day-to-day
* 3.2 Restoring lost PEM file / alternative instance access
* 3.3 /var is 90% full: next steps and triage
* 3.4 Server slow due to High CPU utilization
* 3.5 Nginx returns Connection Refused: triage
* 3.6 SSH stopped working: troubleshooting steps
* 3.7 Find and list logs older than 7 days
* 3.8 Find and remove logs older than 30 days
* 3.9 Cronjob + Shell script for advanced log rotation
* 3.10 Bulk user creation via CSV file script
* 3.11 Service health monitor script in Bash
* 3.12 Find and delete files over 100MB
* 3.13 Extract users logged in today using last, awk, uniq
* 3.14 Website doesn't load: investigation workflow
* 3.15 sed: remove first and last line of a file
* 3.16 Types of variables in Linux (local, environment, special)
* 3.17 kill vs kill -9 mechanics and signals

---

## 4. Networking (9 items • 33:41)
* 4.1 Explain DNS in simple words
* 4.2 Complete client-to-server request flow (OSI model)
* 4.3 Forward Proxy vs Reverse Proxy
* 4.4 User reports slowness in app: networking approach
* 4.5 Curl works with IP, fails with Domain: DNS resolution
* 4.6 Website returns 502 Bad Gateway: triage
* 4.7 Difference between 0.0.0.0 and 127.0.0.1
* 4.8 Public vs Private Subnets
* 4.9 Accidentally created private subnet instead of public: fix

---

## 5. CI/CD (15 items • 1:10:47)
* 5.1 Jenkins shared libraries
* 5.2 5 Maven build targets used day-to-day
* 5.3 Artifact repository selection
* 5.4 Configuring Artifactory in Maven
* 5.5 Build passed locally but fails in CI
* 5.6 CI succeeds but application is broken in Prod
* 5.7 Pipeline slows down over time: caching & optimization
* 5.8 Feature branch push doesn't trigger pipeline
* 5.9 Build fails downloading dependency from artifact repo
* 5.10 Python build fails on CI but works locally
* 5.11 Python application build process in detail
* 5.12 Static code analysis: problems identified
* 5.13 Static analysis slows down CI: optimization
* 5.14 App in OutOfSync state in Argo CD without Git changes
* 5.15 Sending email alerts on Jenkins build failure

---

## 6. Terraform (11 items • 59:01)
* 6.1 for_each vs for in Terraform
* 6.2 Modules in Terraform and why to use them
* 6.3 Role of statefile in Terraform
* 6.4 Storing statefile in Git vs S3 / Remote backend
* 6.5 Terraform statefile management and drift
* 6.6 Two engineers apply statefile at once: state locking
* 6.7 Storing statefile on-premise without cloud accounts
* 6.8 Terraform Community vs Terraform Enterprise
* 6.9 OpenTofu vs Terraform comparison
* 6.10 Write Terraform code to create AWS resources
* 6.11 Resource vs Data source in Terraform

---

## 7. Docker (12 items • 54:01)
* 7.1 Container exits immediately: troubleshooting
* 7.2 Purpose of EXPOSE in Dockerfile (documentation vs publish)
* 7.3 Port not accessible on localhost after port mapping
* 7.4 Data lost when container stops: volume persistence
* 7.5 Code changes not reflected after rebuild: build cache
* 7.6 Permission Denied inside container vs localhost
* 7.7 Docker host running out of disk space: docker system prune
* 7.8 Debugging a live running container
* 7.9 Container registry selection
* 7.10 CMD vs ENTRYPOINT in Dockerfile
* 7.11 Day-to-day Docker commands
* 7.12 Forcefully removing containers and when to do it

---

## 8. Kubernetes (35 items • 3:19:39)
* 8.1 Kubernetes Cluster Architecture (Control Plane & Worker)
* 8.2 Component interaction during `kubectl apply -f pod.yaml`
* 8.3 Purpose of Services in Kubernetes
* 8.4 Why hardcoding Pod IP communication is an anti-pattern
* 8.5 Types of Services (ClusterIP, NodePort, LoadBalancer, Headless)
* 8.6 Labels and Selectors in Kubernetes
* 8.7 NodePort vs LoadBalancer service types
* 8.8 Kubernetes Services and Kube-Proxy relationship (iptables/IPVS)
* 8.9 Disadvantages of LoadBalancer service type
* 8.10 Headless Service and StatefulSet use-cases
* 8.11 Cross-namespace service access (FQDN)
* 8.12 Restricting database Pod access via NetworkPolicies
* 8.13 Production deployment strategies
* 8.14 Rollback strategies in Kubernetes
* 8.15 Designing deployment pipelines to avoid rollbacks
* 8.16 Blue-Green vs Canary deployments
* 8.17 Role of CoreDNS in cluster name resolution
* 8.18 Taints (NoSchedule) and Pod Tolerations
* 8.19 Pod stuck in CrashLoopBackOff: triage workflow
* 8.20 Liveness vs Readiness vs Startup probes
* 8.21 Ingress vs LoadBalancer service type
* 8.22 App works with ClusterIP but fails with Ingress
* 8.23 Why an Ingress Controller is mandatory
* 8.24 Using Ingress with in-house hardware load balancers
* 8.25 Replicas: 3, but only 1 running: scheduler triage
* 8.26 Mounted ConfigMap changes not reflected in Pod
* 8.27 Node Affinity (required vs preferred)
* 8.28 Node Affinity vs Node Label Selector
* 8.29 Container runtimes (containerd, CRI-O)
* 8.30 Kubernetes QoS classes (Guaranteed, Burstable, BestEffort)
* 8.31 Resource Requests vs Limits and OOM scores
* 8.32 3 major production challenges on Kubernetes
* 8.33 Scheduling Pods on Master/Control-plane nodes
* 8.34 Horizontal (HPA) vs Vertical (VPA) Pod Autoscaling
* 8.35 Types of Secrets in Kubernetes

---

## 9. Observability (11 items • 57:14)
* 9.1 Monitoring vs Observability
* 9.2 Emitting custom application metrics and logs
* 9.3 Scraped metrics in Prometheus
* 9.4 Real-world observability implementation
* 9.5 Logs vs Metrics vs Traces (The 3 Pillars)
* 9.6 Push vs Pull monitoring architecture
* 9.7 Observability tooling stack
* 9.8 App slowness with healthy CPU and no error logs: distributed tracing
* 9.9 Tracing requests across microservices in Kubernetes
* 9.10 Pod crashes randomly with OOMKilled: diagnosis and limits
* 9.11 Reducing false alert fatigue at 2 AM

---

## 10. AWS (25 items • 1:49:38)
* 10.1 Designing a highly available multi-tier architecture
* 10.2 AWS NAT Gateway mechanics and use cases
* 10.3 Enabling internet access for private subnet workloads
* 10.4 Inter-subnet communication within a VPC
* 10.5 NACL (stateless) vs Security Group (stateful)
* 10.6 EC2 instance terminated unexpectedly: CloudTrail triage
* 10.7 Lambda function fails intermittently: timeout / memory
* 10.8 RDS storage full: storage autoscaling and vacuum
* 10.9 Accidental deletion of S3/RDS/EC2: disaster recovery
* 10.10 Real-world AWS cost optimization activity
* 10.11 Recent challenge faced with AWS and resolution
* 10.12 Auto Scaling Group not launching EC2 instances
* 10.13 Day-to-day AWS services
* 10.14 AWS EFS performance and bursting credits
* 10.15 Real-time selection: EFS vs EBS
* 10.16 Disabling AWS console access for IAM users
* 10.17 Cross-account Lambda to S3 access
* 10.18 AWS STS mechanics and temporary credentials
* 10.19 IAM Trust Policies vs Permissions Policies
* 10.20 Cross-account Lambda (Account A) to DynamoDB (Account B)
* 10.21 Disadvantages of EBS volumes in multi-zone Kubernetes
* 10.22 AWS Secrets Manager vs SSM Parameter Store
* 10.23 Day-to-day database operational tasks
* 10.24 Production Lambda usage and architectures
* 10.25 IAM User vs IAM Role

---

## 11. Azure (15 items • 1:07:30)
*(Deprioritized for October Sprint - Focus is 100% AWS)*

---

## 12. Python (3 items • 25:01)
* 12.1 Common Python packages for DevOps (boto3, requests, os, sys)
* 12.2 Production task automated with Python
* 12.3 Script to parse and extract patterns from huge log files

---

## 13. Project Management and SDLC (5 items • 22:11)
* 13.1 Walking through a typical workday
* 13.2 Pitching your DevOps & Platform experience
* 13.3 Team contributions for senior roles
* 13.4 Team contributions for early-career roles
* 13.5 Explaining current company architecture and business value
