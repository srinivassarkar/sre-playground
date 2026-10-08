# Kubernetes Mastery: 35 Production Questions & Model Answers

A complete, first-principles interview and operational guide covering control plane internals, networking, CNI packet flows, stateful storage, forensic incident triage, and zero-downtime deployment strategies.

---

## Table of Contents
1. [8.1 Kubernetes Cluster Architecture (Control Plane & Worker Nodes)](#81-kubernetes-cluster-architecture)
2. [8.2 Component Interaction During `kubectl apply -f pod.yaml`](#82-component-interaction-during-kubectl-apply)
3. [8.3 Purpose and Lifecycle of Kubernetes Services](#83-purpose-and-lifecycle-of-kubernetes-services)
4. [8.4 Why Hardcoding Pod IP Communication is an Anti-Pattern](#84-why-hardcoding-pod-ip-is-an-anti-pattern)
5. [8.5 Types of Services (ClusterIP, NodePort, LoadBalancer, Headless)](#85-types-of-services)
6. [8.6 Labels and Selectors: Coupling and Immutability](#86-labels-and-selectors)
7. [8.7 NodePort vs LoadBalancer Service Types](#87-nodeport-vs-loadbalancer)
8. [8.8 Services and kube-proxy: iptables vs IPVS vs eBPF](#88-services-and-kube-proxy)
9. [8.9 Architectural Disadvantages of LoadBalancer Services](#89-disadvantages-of-loadbalancer-services)
10. [8.10 Headless Service and StatefulSet Architectures](#810-headless-service-and-statefulsets)
11. [8.11 Cross-Namespace Service Access and FQDN Routing](#811-cross-namespace-service-access)
12. [8.12 Restricting Database Access via NetworkPolicies](#812-restricting-database-access-via-networkpolicies)
13. [8.13 Production Deployment Strategies](#813-production-deployment-strategies)
14. [8.14 Rollback Mechanics in Kubernetes and GitOps](#814-rollback-mechanics)
15. [8.15 Designing Pipelines to Eliminate Rollbacks](#815-designing-pipelines-to-eliminate-rollbacks)
16. [8.16 Blue-Green vs Canary Deployments](#816-blue-green-vs-canary)
17. [8.17 Role of CoreDNS in Cluster Name Resolution](#817-role-of-coredns)
18. [8.18 Taints, Tolerations, and Node Isolation](#818-taints-and-tolerations)
19. [8.19 Pod Stuck in CrashLoopBackOff: Forensic Triage](#819-pod-stuck-in-crashloopbackoff)
20. [8.20 Liveness vs Readiness vs Startup Probes](#820-liveness-vs-readiness-vs-startup-probes)
21. [8.21 Ingress vs LoadBalancer Service Type](#821-ingress-vs-loadbalancer)
22. [8.22 Service Reachable via ClusterIP but Fails with Ingress](#822-clusterip-works-ingress-fails)
23. [8.23 Why an Ingress Controller is Mandatory](#823-why-ingress-controller-is-mandatory)
24. [8.24 Integrating Ingress with On-Premises Hardware Load Balancers](#824-ingress-with-hardware-load-balancers)
25. [8.25 Replicas: 3 Desired, Only 1 Running: Scheduler Triage](#825-replicas-stuck-scheduler-triage)
26. [8.26 Mounted ConfigMap Changes Not Reflected in Pods](#826-mounted-configmap-changes-not-reflected)
27. [8.27 Node Affinity: Required vs Preferred](#827-node-affinity-required-vs-preferred)
28. [8.28 Node Affinity vs nodeSelector](#828-node-affinity-vs-nodeselector)
29. [8.29 Container Runtimes: CRI, containerd, and runc](#829-container-runtimes)
30. [8.30 Kubernetes QoS Classes: Guaranteed, Burstable, BestEffort](#830-kubernetes-qos-classes)
31. [8.31 Resource Requests, Limits, and Linux Kernel OOM Scores](#831-resource-requests-limits-and-oom)
32. [8.32 Three Production Incidents on Kubernetes (STAR Method)](#832-three-production-incidents-on-kubernetes)
33. [8.33 Scheduling Pods on Control-Plane / Master Nodes](#833-scheduling-on-control-plane-nodes)
34. [8.34 Horizontal (HPA) vs Vertical (VPA) Pod Autoscaling](#834-hpa-vs-vpa-autoscaling)
35. [8.35 Types of Secrets and Production Secret Management](#835-types-of-secrets)

---

## 8.1 Kubernetes Cluster Architecture

> **The Interview Question:**  
> "Can you walk me through the complete Kubernetes cluster architecture, explaining the distinct responsibilities of the control plane and worker nodes, and how components communicate?"

### 30-Second Interview Answer
Kubernetes is a declarative, loosely coupled distributed system built around a single source of truth: `etcd`. The **control plane** maintains the global state and runs reconciliation loops; the **worker nodes** run containers under the supervision of the local node agent (`kubelet`). Components never communicate with each other directly; every interaction happens asynchronously by watching the `kube-apiserver`.

```
[ CONTROL PLANE ]
etcd (Raft consensus) ◀──▶ kube-apiserver (HTTPS, AuthN/AuthZ, Admission)
                               ▲    ▲    ▲
            ┌──────────────────┘    │    └──────────────────┐
            ▼                       ▼                       ▼
    kube-scheduler        kube-controller-mgr     cloud-controller-mgr

[ WORKER NODE ]
kubelet ──▶ kube-apiserver (Reports Node/Pod status via gRPC CRI to containerd)
kube-proxy ──▶ Programs Linux kernel netfilter (iptables/IPVS/nftables)
CNI Plugin ──▶ Allocates network namespaces and Pod IPs
```

### Systems Rationale & Follow-Up Defense
1. **The Role of etcd:** A strongly consistent, distributed key-value store implementing the Raft consensus algorithm. It holds 100% of the cluster state. To prevent split-brain and ensure write quorum, production control planes strictly require an **odd number of nodes (3 or 5)**.
2. **Level-Triggered Reconciliation:** Controllers do not rely on edge-triggered notifications (which can drop packets). They continuously compare **Desired State** (declared in etcd) against **Actual State** (observed on nodes) and take corrective actions until convergence is reached.
3. **Managed Control Planes:** In EKS, GKE, and AKS, the cloud provider manages and autoscales the control plane across 3 availability zones behind a regional Network Load Balancer, eliminating etcd operational overhead.

---

## 8.2 Component Interaction During `kubectl apply -f pod.yaml`

> **The Interview Question:**  
> "What exact sequence of events occurs across Kubernetes control plane and worker node components when you execute `kubectl apply -f pod.yaml`?"

### Step-by-Step Execution Sequence
1. **Client Side (`kubectl`):** Validates the client-side manifest schema, builds an HTTP PATCH/POST request, and sends it to the `kube-apiserver` using TLS credentials in `~/.kube/config`.
2. **API Server Processing:**
   * **Authentication (AuthN):** Verifies client certificates, bearer tokens, or OIDC identity.
   * **Authorization (AuthZ):** Evaluates RBAC permissions (`can user create pods in namespace X?`).
   * **Mutating Admission Webhooks:** Injects default values, sidecars (e.g. Istio Envoy), or ServiceAccount tokens.
   * **Object Schema Validation:** Verifies syntax, required fields, and resource limits.
   * **Validating Admission Webhooks:** Checks Pod Security Standards or OPA/Kyverno policies.
   * **etcd Persistence:** Writes the Pod object to `etcd`. The Pod is saved with `spec.nodeName = ""` and status **`Pending`**.
3. **The Scheduler (`kube-scheduler`):**
   * Observes the unassigned Pod via an active watch stream.
   * **Filtering Phase (Predicates):** Filters out nodes that lack sufficient CPU/Memory requests, fail node selectors/affinities, or carry untolerated taints.
   * **Scoring Phase (Priorities):** Scores candidate nodes based on resource balance and topology spread.
   * **Binding:** Writes the chosen node name back to the API server (`spec.nodeName = "node-1"`).
4. **The Node Agent (`kubelet`):**
   * Kubelet on `node-1` detects the Pod assignment via its watch on the API server.
   * Invokes the **Container Runtime Interface (CRI)** (e.g. containerd) to pull the container image and create the Pod sandbox namespace.
   * Calls the **Container Network Interface (CNI)** plugin to assign a network namespace, veth pair, and Pod IP.
   * Calls the **Container Storage Interface (CSI)** driver to attach and mount required volumes.
   * Launches containers, executes `postStart` hooks, and initiates startup/readiness/liveness probes.
5. **Status Reporting:** Kubelet updates Pod status to `Running` (and `Ready` once readiness probes pass). The `EndpointSlice` controller appends the Pod IP to matching Services, and `kube-proxy` programs local kernel forwarding rules.

---

## 8.3 Purpose and Lifecycle of Kubernetes Services

> **The Interview Question:**  
> "Why are Kubernetes Services necessary, and how do they decouple ephemeral Pod lifecycles from application consumers?"

### 30-Second Interview Answer
Pods are disposable: when a Pod crashes, scales, or reschedules, its IP address is destroyed and a new IP is assigned. A **Service** provides a permanent, immutable virtual IP (ClusterIP) and a stable CoreDNS name that acts as a Layer 4 load balancer across all healthy, ready Pods matching its label selector.

### How It Works Under the Hood
1. A Service defines a **label selector** (`app: api`).
2. The **EndpointSlice Controller** continuously watches Pods. Only Pods that have passed their **Readiness Probes** have their IPs added to the `EndpointSlice` object.
3. Every worker node runs `kube-proxy`, which watches EndpointSlices and updates Linux kernel routing tables (`iptables` or `IPVS`).
4. When an internal client calls `http://api.default.svc.cluster.local:8080`, the kernel intercepts the packet and translates the virtual ClusterIP directly to one of the live Pod IPs.

---

## 8.4 Why Hardcoding Pod IP Communication is an Anti-Pattern

> **The Interview Question:**  
> "Why is it considered an architectural anti-pattern for microservices to communicate using direct Pod IP addresses?"

### The 5 Production Failure Modes
1. **Zero IP Persistence:** Pod IPs are ephemeral. Rolling deployments, node restarts, or spot evictions permanently destroy the IP.
2. **Lack of Load Balancing:** Hardcoding an IP directs 100% of traffic to a single container instance. Horizontal Pod Autoscaling (HPA) adds new pods that receive zero traffic.
3. **No Health Awareness:** If the target container deadlocks or fails its health check, traffic continues flowing to the broken IP until a connection error occurs.
4. **Subnet IP Recycling:** When a dead Pod releases its IP, the CNI can reassign that identical IP to a completely different microservice, causing catastrophic traffic misrouting.
5. **The Correct Alternative:** Always call the **Service DNS name** (`http://orders-service:8080`). For stateful quorum systems (Kafka, ZooKeeper, MongoDB), use a **StatefulSet backed by a Headless Service** (`clusterIP: None`) for deterministic DNS identities (`orders-0.orders-service`).

---

## 8.5 Types of Services

> **The Interview Question:**  
> "Can you compare the different types of Kubernetes Services—ClusterIP, NodePort, LoadBalancer, and Headless—and explain their exact use cases?"

### Comparison Matrix

| Service Type | Scope & Reachability | How It Routes | Production Use Case |
| :--- | :--- | :--- | :--- |
| **ClusterIP** (Default) | Internal cluster only | Stable virtual IP mapped by kube-proxy | Standard internal microservice-to-microservice RPC/REST |
| **NodePort** | External via `<NodeIP>:<Port>` | Opens high port (30000–32767) on every node | Dev/test, or target for on-premises hardware load balancers |
| **LoadBalancer** | External via Cloud LB | Triggers cloud provider to provision NLB/ALB pointing to NodePorts | Exposing public-facing services directly to the internet |
| **ExternalName** | Internal to external alias | Returns a DNS `CNAME` record; no proxying | Aliasing external databases (RDS/MongoDB Atlas) to internal names |
| **Headless** (`clusterIP: None`) | Internal | Returns individual Pod IPs directly via DNS A records | StatefulSets (Kafka, Cassandra, MongoDB) requiring direct peer discovery |

---

## 8.6 Labels and Selectors

> **The Interview Question:**  
> "How do labels and selectors decouple objects in Kubernetes, and what are the critical production gotchas regarding selector immutability?"

### The Architectural Role
Labels are arbitrary key-value metadata attached to objects. Selectors are queries that dynamically identify objects based on those labels.
* **Equality-Based:** `env = prod`, `tier = backend`.
* **Set-Based:** `env in (prod, staging)`, `tier notin (cache)`.

### Production Gotchas
1. **Selector Immutability:** Once a Deployment or ReplicaSet is created, its `spec.selector` is **immutable**. You cannot change the selector without deleting the deployment and recreating it.
2. **Missing Endpoints:** 95% of "Service returns 503 / connection refused" issues are caused by label selector typos. If `kubectl get endpoints <svc>` shows `<none>`, the Service selector does not match the Pod labels.
3. **Never Put Versions in Service Selectors:** Do not put `version: v2` in a standard Service selector unless executing a manual blue-green cutover.

---

## 8.7 NodePort vs LoadBalancer Service Types

> **The Interview Question:**  
> "What are the structural differences between NodePort and LoadBalancer Services, and why is LoadBalancer considered a layer on top of NodePort?"

### Structural Relationship
A `LoadBalancer` Service is a strict superset of `NodePort`, which is a superset of `ClusterIP`:
* Creating a `NodePort` automatically allocates a `ClusterIP`.
* Creating a `LoadBalancer` automatically allocates a `NodePort` on all nodes, allocates a `ClusterIP`, and instructs the cloud controller to point an external cloud load balancer at those node ports.

### Critical Comparison
* **NodePort:** Exposes ports in the restricted range `30000–32767`. Clients must track dynamic worker node IPs. If a node dies, external clients break unless fronted by an external balancer.
* **LoadBalancer:** Provides a single, static external IP or DNS name. Cloud health checks automatically route around dead or cordoned worker nodes.

---

## 8.8 Services and kube-proxy: iptables vs IPVS vs eBPF

> **The Interview Question:**  
> "How does kube-proxy implement Service routing under the hood? What are the architectural trade-offs between iptables and IPVS modes?"

### The Physical Reality
A **ClusterIP is not a physical network interface**. You cannot ping a ClusterIP with ICMP. It is a virtual IP implemented purely as packet filtering and translation rules inside the Linux kernel.

### The Modes

| Mode | Architecture | Algorithmic Complexity | Production Scaling Limit |
| :--- | :--- | :--- | :--- |
| **iptables** (Default) | Sequential packet-filtering chains; random probability matching | $O(N)$ linear rule evaluation | Degrades significantly past 5,000 Services; full rule-table reloads stall packet flow |
| **IPVS** (IP Virtual Server) | Kernel Layer 4 load balancer using in-memory hash tables | $O(1)$ constant time lookup | Scales to 50,000+ Services; supports Least-Connections and Round-Robin |
| **eBPF (Cilium)** | Bypasses netfilter; replaces kube-proxy with eBPF programs loaded into kernel sockets | $O(1)$ socket-level translation | Maximum performance; eliminates conntrack overhead and iptables latency completely |

---

## 8.9 Architectural Disadvantages of LoadBalancer Services

> **The Interview Question:**  
> "Why is it an anti-pattern to expose dozens of microservices using individual LoadBalancer type Services in production?"

### The Production Costs
1. **Massive Cloud Spend:** In AWS, each Network Load Balancer (NLB) or Classic LB costs ~$22/month base plus data processing fees. Exposing 40 microservices via `type: LoadBalancer` adds ~$900/month in useless load balancer idle costs.
2. **Layer 4 Only:** LoadBalancer Services operate at Layer 4 (TCP/UDP). They cannot perform URL path routing (`/api/users` vs `/api/orders`), HTTP header inspection, TLS termination, or SSL cert management.
3. **AWS EIP Quotas:** Every internet-facing load balancer consumes Elastic IPs, rapidly exhausting regional VPC quotas.
4. **The Standard Architecture:** Deploy **one single Ingress Controller** (or Gateway API) fronted by **one single cloud LoadBalancer**, routing hundreds of microservices via Layer 7 hostname and path rules.

---

## 8.10 Headless Service and StatefulSet Architectures

> **The Interview Question:**  
> "When would you use a Headless Service (`clusterIP: None`), and how does it integrate with StatefulSets to support distributed databases?"

### How Headless Services Function
By setting `spec.clusterIP: None`, kube-proxy ignores the service. CoreDNS stops returning a single load-balanced virtual IP; instead, DNS queries return **the individual IP addresses of every ready Pod** (multiple A records).

### The StatefulSet Contract
Stateful workloads (Kafka, PostgreSQL clusters, ZooKeeper) require persistent network identities and isolated storage:
1. **Predictable Hostnames:** Pods are named ordinally: `db-0`, `db-1`, `db-2`.
2. **Deterministic DNS:** Backed by the headless service `db`, each pod receives an immutable FQDN:
   `db-0.db.default.svc.cluster.local`
3. **Dedicated PVCs:** `volumeClaimTemplates` provisions a dedicated PersistentVolume per ordinal index (`data-db-0`) that re-attaches to `db-0` even if it reschedules onto another node.

---

## 8.11 Cross-Namespace Service Access and FQDN Routing

> **The Interview Question:**  
> "How does a Pod in Namespace A communicate with a Service in Namespace B? What is the role of search domains and the `ndots:5` latency trap?"

### FQDN Syntax
To communicate across namespaces, use the Fully Qualified Domain Name:
```
<service-name>.<namespace-name>.svc.cluster.local
```
* Short name (`curl http://orders:8080`) only resolves within the **same namespace**.
* Cross-namespace short form: `curl http://orders.backend:8080`.

### The `ndots:5` Production DNS Bug
Every Pod's `/etc/resolv.conf` defaults to `options ndots:5` and defines 3 local search domains:
1. `<namespace>.svc.cluster.local`
2. `svc.cluster.local`
3. `cluster.local`

* **The Problem:** Any hostname containing fewer than 5 dots (e.g. `api.stripe.com`, which has 2 dots) forces the Linux resolver to append all search domains first!
* Calling `api.stripe.com` generates:
  1. `api.stripe.com.default.svc.cluster.local` (NXDOMAIN)
  2. `api.stripe.com.svc.cluster.local` (NXDOMAIN)
  3. `api.stripe.com.cluster.local` (NXDOMAIN)
  4. `api.stripe.com` (SUCCESS)
* Every external HTTP call generates **4 DNS queries**, swamping CoreDNS.
* **The Production Fix:** Use trailing dots for external domains (`api.stripe.com.`), deploy **NodeLocal DNSCache**, or tune `dnsConfig: options: [{ name: ndots, value: "2" }]`.

---

## 8.12 Restricting Database Access via NetworkPolicies

> **The Interview Question:**  
> "How do you enforce network isolation between application tiers in Kubernetes, and what is required from the underlying CNI to make NetworkPolicies work?"

### The Default Security Posture
By default, Kubernetes networking is an open mesh: **all Pods can communicate with all other Pods across all namespaces**.

### The Two-Step NetworkPolicy Pattern

```yaml
# Step 1: Default-Deny all ingress in namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: prod
spec:
  podSelector: {}
  policyTypes: ["Ingress"]
---
# Step 2: Explicitly allow only API pods to reach DB on port 5432
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-to-db
  namespace: prod
spec:
  podSelector:
    matchLabels: { app: postgres }
  policyTypes: ["Ingress"]
  ingress:
    - from:
        - podSelector:
            matchLabels: { app: api }
      ports:
        - protocol: TCP
          port: 5432
```

### The CNI Enforcement Rule
**NetworkPolicies are purely declarations.** The underlying **CNI plugin must support policy enforcement** (e.g. Calico, Cilium, or AWS VPC CNI with network policy enabled). If running a basic CNI like Flannel without a policy engine, NetworkPolicy objects are accepted by the API server but completely ignored by worker nodes.

---

## 8.13 Production Deployment Strategies

> **The Interview Question:**  
> "Can you compare the trade-offs of Rolling Updates, Recreate, Blue-Green, and Canary deployments, and explain how to achieve zero-downtime rolling releases?"

### Strategy Comparison

| Strategy | Availability | Extra Compute Cost | Rollback Speed | Best Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Rolling Update** | Zero downtime | Minimal (`maxSurge: 25%`) | Moderate | Default for stateless microservices |
| **Recreate** | **Downtime** | Zero | Fast | Non-concurrent workloads (legacy DB migrations) |
| **Blue-Green** | Zero downtime | **2x (100% duplicate env)** | **Instant (DNS/Router switch)** | High-risk releases; breaking API versions |
| **Canary** | Zero downtime | Low (5–10% extra pods) | Fast (weight back to 0) | Metric-driven progressive delivery |

### Zero-Downtime Rolling Update Requirements
1. **Readiness Probes:** Prevents traffic routing until the container finishes booting.
2. **`preStop` Sleep Hook:** Add a 10-second sleep in the container lifecycle to allow kube-proxy and Ingress to remove the Pod IP from routing tables before the application process receives `SIGTERM`.
3. **`terminationGracePeriodSeconds: 60`:** Allows in-flight HTTP requests to drain cleanly.
4. **PodDisruptionBudgets (PDB):** Enforces `minAvailable: 1` during node drains and cluster upgrades.

---

## 8.14 Rollback Mechanics in Kubernetes and GitOps

> **The Interview Question:**  
> "How do rollbacks work in Kubernetes Deployments, and what are the severe database and configuration traps when rolling back?"

### Built-in Deployment Rollback
```bash
kubectl rollout history deployment/api
kubectl rollout undo deployment/api --to-revision=2
```
* **How It Works:** The Deployment controller tracks past revisions by retaining inactive **ReplicaSets** (`revisionHistoryLimit: 10`). Rolling back simply scales down the new ReplicaSet and scales up the old ReplicaSet.

### The Production Traps
1. **Deployments Only Roll Back Pod Templates:** `kubectl rollout undo` does **NOT** roll back ConfigMaps, Secrets, or external databases. If Revision 3 updated a ConfigMap, rolling back to Revision 2 leaves the Pod running old code with new configuration!
2. **Database Migrations:** If Revision 3 executed a non-backward-compatible database migration (dropping a column), rolling back the application crashes it immediately. Always use the **Expand-and-Contract (Parallel Run)** database pattern.
3. **GitOps Best Practice:** In production with Argo CD or Flux, never use `kubectl rollout undo`. Revert the Git commit; let the GitOps controller reconcile the cluster back to the audited Git state.

---

## 8.15 Designing Pipelines to Eliminate Rollbacks

> **The Interview Question:**  
> "How do you design a CI/CD pipeline to catch regressions early and minimize the need for production rollbacks?"

### The Shift-Left Pipeline Architecture
```
Commit ──▶ Unit & Contract Tests ──▶ Image Vulnerability Scan (Trivy)
       ──▶ Manifest Policy Validation (Kubeconform, Kyverno)
       ──▶ Ephemeral Staging Deployment (Helm / Kustomize)
       ──▶ Automated Smoke & Load Tests
       ──▶ Canary Promotion in Production (5% -> 25% -> 100% via Argo Rollouts)
       ──▶ Automated Prometheus Metric Analysis (Error Rate < 0.1%, P99 < 200ms)
```

### Core Principles
* **Immutable Images:** Tag images with Git commit SHA or semantic versions; strictly prohibit `:latest`.
* **Automated Canary Analysis:** Use **Argo Rollouts** with Prometheus queries. If error rate spikes above 0.5% during the 5% canary phase, Argo aborts automatically with zero human intervention.
* **Feature Flags:** Decouple code deployment from feature release using LaunchDarkly or Unleash.

---

## 8.16 Blue-Green vs Canary Deployments

> **The Interview Question:**  
> "When would you architect a Blue-Green deployment over a Canary deployment, and what are the infrastructure prerequisites for each?"

### Comparison

| Dimension | Blue-Green Deployment | Canary Deployment |
| :--- | :--- | :--- |
| **Traffic Shift** | 100% atomic cutover at a single point in time | Incremental percentage shift (5%, 25%, 50%, 100%) |
| **Infrastructure Overhead** | Requires **2x full capacity** during release | Requires only a small fractional capacity increase |
| **Blast Radius** | 100% of users hit the new version upon cutover | Only 5% of users exposed initially |
| **Rollback Complexity** | Instant: flip load balancer back to Blue | Fast: dial canary traffic weight to 0% |
| **Tooling Needed** | Service selector flip or ALB target group switch | Advanced Ingress annotations, Service Mesh, or Argo Rollouts |

---

## 8.17 Role of CoreDNS in Cluster Name Resolution

> **The Interview Question:**  
> "How does CoreDNS resolve names inside a Kubernetes cluster, and how do you diagnose DNS latency and resolution failures?"

### How CoreDNS Works Under the Hood
1. Runs as a Deployment in `kube-system`, exposed through a Service with a static ClusterIP (typically `10.96.0.10`).
2. Kubelet configures `nameserver 10.96.0.10` in every Pod's `/etc/resolv.conf`.
3. CoreDNS reads the **Corefile** configuration:
   * The `kubernetes` plugin watches the API server and resolves `*.svc.cluster.local`.
   * Unmatched queries (e.g. `github.com`) are forwarded to the upstream node/VPC resolvers.

### Diagnosis Commands
```bash
# Test resolution from an ephemeral debug pod
kubectl run -it --rm dns-test --image=registry.k8s.io/e2e-test-images/jessie-dnsutils -- nslookup kubernetes.default

# Check CoreDNS logs and latency metrics
kubectl -n kube-system logs -l k8s-app=kube-dns --tail=100
```
* **Production Optimization:** Deploy **NodeLocal DNSCache** as a DaemonSet. It runs a lightweight DNS caching agent on every worker node's link-local IP (`169.254.20.10`), eliminating cross-node CoreDNS latency and UDP conntrack race conditions.

---

## 8.18 Taints, Tolerations, and Node Isolation

> **The Interview Question:**  
> "How do Taints and Tolerations work, and why does a Toleration alone fail to guarantee that a Pod lands on a dedicated node?"

### The Mechanism
* **Taints are applied to Nodes** to *repel* Pods:
  `kubectl taint nodes gpu-node-1 dedicated=gpu:NoSchedule`
* **Tolerations are applied to Pods** to allow (tolerate) scheduling on tainted nodes:
  ```yaml
  tolerations:
    - key: "dedicated"
      operator: "Equal"
      value: "gpu"
      effect: "NoSchedule"
  ```

### The Critical Interview Gotcha
**A toleration only permits scheduling; it does NOT attract the Pod.**
* If `gpu-node-1` has the taint, and Pod A has the matching toleration, the scheduler *might* put Pod A on `gpu-node-1`, or it might put Pod A on a standard general-purpose node!
* **The Rule for Node Dedication:** To dedicate nodes (e.g. GPU instances for AI inference), you must use **both**:
  1. A **Taint** on the node (to keep non-GPU pods out).
  2. A **NodeAffinity** or `nodeSelector` on the Pod (to pull the GPU pod onto the GPU node).

---

## 8.19 Pod Stuck in CrashLoopBackOff: Forensic Triage

> **The Interview Question:**  
> "A critical production Pod is in `CrashLoopBackOff`. Walk me through your methodical triage workflow and how you interpret container exit codes."

### Step-by-Step Triage Workflow
1. **Inspect High-Level Status:** `kubectl get pod <pod-name>` (Note restart count and age).
2. **Check Last State & Exit Code:** `kubectl describe pod <pod-name>`:
   * Look at **`Last State -> Exit Code`** and **`Reason`**.
   * Look at **`Events`** at the bottom of describe output.
3. **Inspect Previous Logs:** `kubectl logs <pod-name> --previous` (Crucial: running `kubectl logs` without `--previous` displays the newly booting, empty container logs).

### The Exit Code Diagnostic Matrix

| Exit Code | Technical Meaning | Root Cause & Investigation |
| :--- | :--- | :--- |
| **Exit Code 0** | Normal Process Exit | Container finished its task; running a one-off batch command inside a long-running Deployment. |
| **Exit Code 1** | Application Error | Uncaught application exception, missing environment variable, database connection refusal. |
| **Exit Code 126 / 127** | Command Not Found | Bad entrypoint path, missing execute permissions, or missing shared C libraries in alpine image. |
| **Exit Code 137** | **SIGKILL (OOMKilled)** | Linux kernel OOM killer terminated the process because it exceeded `resources.limits.memory`. |
| **Exit Code 143** | **SIGTERM** | Container received graceful termination signal from Kubernetes and exited. |

---

## 8.20 Liveness vs Readiness vs Startup Probes

> **The Interview Question:**  
> "Can you compare Liveness, Readiness, and Startup probes, and explain the catastrophic cascading failure that occurs when you misconfigure them?"

### Probe Comparison

| Probe Type | What It Checks | Action on Failure | Typical Check |
| :--- | :--- | :--- | :--- |
| **Liveness** | Is the application process deadlocked? | **Kubelet restarts the container** | Lightweight internal `/healthz` |
| **Readiness** | Can the container receive user traffic? | **Removes Pod IP from Service EndpointSlice** | Checks internal caches and warm state |
| **Startup** | Has the slow-starting application booted? | Disables Liveness/Readiness until passed | Long timeout for legacy Java/Node cold starts |

### The Cascading Outage Trap
**Never check external dependencies (database, Redis) inside a Liveness Probe.**
* If your PostgreSQL database experiences a temporary 10-second network blip, every single backend Pod's liveness probe fails simultaneously.
* Kubelet restarts all 50 backend pods at once.
* When they reboot, all 50 pods hammer the recovering database with new connection handshakes simultaneously, causing a catastrophic, cluster-wide cascading outage.
* **Rule:** Dependency checks belong strictly in **Readiness Probes**, never Liveness Probes.

---

## 8.21 Ingress vs LoadBalancer Service Type

> **The Interview Question:**  
> "What are the architectural differences between an Ingress resource and a LoadBalancer Service, and how do they interact?"

### Comparison
* **LoadBalancer Service:** Operates at **Layer 4 (TCP/UDP)**. Provisions one dedicated cloud load balancer per Service. No path routing, no hostname routing, no URL rewriting.
* **Ingress:** Operates at **Layer 7 (HTTP/HTTPS)**. A single entrypoint routing multiple hostnames and paths (`api.domain.com/users` vs `api.domain.com/orders`) to different internal Services, terminating TLS centrally.

### How They Relate
An Ingress resource does not handle traffic directly. An **Ingress Controller** (e.g. Nginx, Traefik) runs as a Deployment inside the cluster and is exposed to the outside world via **one single `type: LoadBalancer` Service**. Ingress is the smart Layer 7 routing brain sitting behind one Layer 4 cloud balancer.

---

## 8.22 Service Reachable via ClusterIP but Fails with Ingress

> **The Interview Question:**  
> "A developer reports their service is working fine internally via ClusterIP, but external requests through Ingress return errors. How do you triage this hop-by-hop?"

### 10-Step Triage Checklist
1. **IngressClass Verification:** Verify `spec.ingressClassName` matches the installed Ingress Controller.
2. **Backend Service Mapping:** Run `kubectl describe ingress <name>`. Confirm the backend Service name and port match the actual service definition.
3. **Endpoint Verification:** Check `kubectl get endpoints <svc-name>`. If endpoints are empty, the issue is a label selector mismatch or failed readiness probe.
4. **PathType Matching:** Check `pathType: Prefix` vs `Exact`.
5. **Host Header Validation:** Test with `curl -H "Host: app.example.com" http://<lb-ip>/`. If DNS is unpropagated, requests hitting the raw IP without a Host header return 404 from the Ingress default backend.
6. **TLS Secret Existence:** Ensure the referenced TLS Secret exists in the **same namespace** as the Ingress resource.
7. **HTTP Status Code Mapping:**
   * **404:** No Ingress routing rule matched the requested host or path.
   * **502:** Ingress reached the Pod, but the container refused the connection or protocol mismatched (e.g. Ingress sent HTTP to an HTTPS backend).
   * **503:** No healthy endpoints available in the EndpointSlice.
   * **504:** Backend application timed out (increase `proxy-read-timeout` annotation).

---

## 8.23 Why an Ingress Controller is Mandatory

> **The Interview Question:**  
> "Why does creating an Ingress manifest do absolutely nothing in a default Kubernetes cluster without an Ingress Controller installed?"

### The Control Loop Reality
An Ingress resource is merely a **declarative data record in `etcd`**. The core Kubernetes control plane does not include a built-in reverse proxy.
* An **Ingress Controller** (Nginx, Traefik, Envoy, AWS Load Balancer Controller) is an independent control daemon.
* It watches the API server for `Ingress` events and translates those rules into real proxy configurations (e.g. dynamically generating `nginx.conf` and reloading worker processes, or provisioning AWS Application Load Balancers).
* Without an active Ingress Controller running, the Ingress resource sits dormant in etcd forever.

---

## 8.24 Integrating Ingress with On-Premises Hardware Load Balancers

> **The Interview Question:**  
> "How do you architect Kubernetes ingress when company policy mandates using enterprise on-premises hardware appliances like F5 BIG-IP or Citrix ADC?"

### The Architecture Patterns
1. **Hardware Appliance in Front of Ingress Controller (Standard):**
   * Expose the Ingress Controller (Nginx Ingress) via a **NodePort** Service on a dedicated pool of worker nodes.
   * The F5 BIG-IP virtual server load balances external traffic across `<Node-IP>:<NodePort>`.
   * The Ingress Controller then routes Layer 7 traffic to internal Pod IPs.
2. **Direct Appliance Integration:**
   * Deploy the **F5 Container Ingress Services (CIS)** controller inside Kubernetes.
   * CIS watches Ingress/Service objects and automatically configures F5 virtual servers, pools, and nodes directly via F5 REST APIs, bypassing NodePort hops.
3. **Client IP Preservation:** Enable PROXY protocol or `X-Forwarded-For` on the hardware appliance and configure `externalTrafficPolicy: Local` on the NodePort service.

---

## 8.25 Replicas: 3 Desired, Only 1 Running: Scheduler Triage

> **The Interview Question:**  
> "A Deployment has `replicas: 3`, but only 1 Pod is running and 2 Pods are stuck in `Pending`. Walk me through your diagnosis."

### Step 1: Run Describe on the Pending Pod
```bash
kubectl describe pod <pending-pod-name>
```
Look directly at the **Events** section at the bottom. The scheduler prints the exact rejection reason:
`0/5 nodes are available: 2 Insufficient cpu, 3 node(s) had untolerated taint`.

### The Common Causes
1. **Insufficient CPU/Memory Requests:** The sum of existing Pod requests on each node leaves no room for the new Pod's requests. Lower requests or scale out node capacity via Karpenter.
2. **Untolerated Node Taints:** Worker nodes carry taints that the Pod lacks tolerations for.
3. **Pod Anti-Affinity Rules:** The Deployment specifies hard `requiredDuringScheduling` PodAntiAffinity (e.g. only 1 replica per node), but the cluster only has 1 matching node.
4. **Volume Node Affinity Conflict:** The Pod uses an EBS PVC locked to Availability Zone `us-east-1a`, but all schedulable nodes are in `us-east-1b`.
5. **ResourceQuotas:** The namespace has exceeded its compute or Pod count quota.

---

## 8.26 Mounted ConfigMap Changes Not Reflected in Pods

> **The Interview Question:**  
> "You updated a ConfigMap in the cluster, but the running application containers still see the old values. What are the common causes and solutions?"

### The Root Causes
1. **Environment Variables (`envFrom`):** Environment variables are evaluated strictly **once at process startup**. They never update dynamically. The Pod must be restarted.
2. **`subPath` Volume Mounts:** Files mounted via `subPath` do **not** receive automatic updates when the ConfigMap changes.
3. **Application Caching:** The file on disk was updated via atomic symlink swap, but the application only read the file once at boot and cached it in memory.
4. **Kubelet Sync Delay:** Standard volume mounts can take up to 60–90 seconds to reflect updates due to Kubelet sync intervals and local cache TTLs.

### Production Solutions
* **Rolling Restart:** `kubectl rollout restart deployment/<name>`
* **ConfigMap Hash Generator (Kustomize / Helm):** Kustomize appends a content hash to the ConfigMap name (`config-a1b2c3d`). Updating the config creates a new ConfigMap, which changes the Deployment pod template, triggering an automatic rolling update.
* **Reloader Operator:** Install the open-source Stakater Reloader controller, which watches ConfigMaps and triggers rolling restarts automatically upon modification.

---

## 8.27 Node Affinity: Required vs Preferred

> **The Interview Question:**  
> "Can you explain the difference between `requiredDuringScheduling` and `preferredDuringScheduling` in Node Affinity?"

### The Rules
* **`requiredDuringSchedulingIgnoredDuringExecution` (Hard Rule):** The Pod **cannot be scheduled** unless a node satisfies the rule. If no matching nodes exist, the Pod remains `Pending`.
* **`preferredDuringSchedulingIgnoredDuringExecution` (Soft Rule):** Specifies preferences with integer weights (1–100). The scheduler attempts to place the Pod on matching nodes, but will place it on non-matching nodes if capacity is unavailable.
* **`IgnoredDuringExecution`:** If node labels change while the Pod is running, the Pod is **not evicted**.

---

## 8.28 Node Affinity vs nodeSelector

> **The Interview Question:**  
> "How does Node Affinity compare to `nodeSelector`, and when is `nodeSelector` no longer sufficient?"

### Comparison

| Dimension | `nodeSelector` | Node Affinity |
| :--- | :--- | :--- |
| **Syntax** | Flat key-value map | Expressive YAML expressions |
| **Logic Operators** | Strict exact match (AND only) | `In`, `NotIn`, `Exists`, `DoesNotExist`, `Gt`, `Lt` |
| **Soft Preferences** | No (hard requirements only) | Yes (weighted soft preferences 1–100) |
| **Composite Logic** | All labels must match | OR logic across terms; AND logic within terms |

---

## 8.29 Container Runtimes: CRI, containerd, and runc

> **The Interview Question:**  
> "What is the Container Runtime Interface (CRI), how does containerd interact with runc, and what was the impact of the dockershim removal?"

### The Container Execution Chain
```
kubelet ──▶ [ gRPC CRI ] ──▶ containerd ──▶ containerd-shim ──▶ runc ──▶ Linux Kernel (cgroups + namespaces)
```

1. **CRI (Container Runtime Interface):** A standardized gRPC API allowing Kubernetes to control any compliant container runtime without vendor-specific code.
2. **containerd:** The high-level runtime daemon managing image pulls, storage unpacks, and container lifecycle.
3. **runc:** The low-level OCI reference implementation that interacts directly with the Linux kernel to create namespaces, cgroups, and capabilities.
4. **Dockershim Removal (v1.24):** Dockershim was deprecated because Docker Engine wrapped containerd unnecessarily, adding latency and memory overhead. Docker-built OCI images still run identically on containerd.

---

## 8.30 Kubernetes QoS Classes: Guaranteed, Burstable, BestEffort

> **The Interview Question:**  
> "How are Kubernetes Quality of Service (QoS) classes determined, and how do they govern node eviction order under memory pressure?"

### QoS Determination Rules

| QoS Class | Rule | Eviction Priority |
| :--- | :--- | :--- |
| **Guaranteed** | CPU and Memory **requests equal limits** across all containers in the Pod | **Evicted Last** (Most protected) |
| **Burstable** | At least one container has requests or limits set, but not Guaranteed | **Evicted Second** |
| **BestEffort** | Zero requests and zero limits specified | **Evicted First** under any memory pressure |

### Eviction Order
When a node runs out of physical memory, the Kubelet evicts Pods in reverse QoS order: `BestEffort` first, then `Burstable` pods exceeding their requests, and finally `Guaranteed` pods.

---

## 8.31 Resource Requests, Limits, and Linux Kernel OOM Scores

> **The Interview Question:**  
> "What is the difference between CPU limits and Memory limits at the Linux kernel level? Why does exceeding memory kill a process while exceeding CPU only throttles it?"

### Compressible vs Incompressible Resources
* **CPU is Compressible:** When a container exceeds its CPU limit, the Linux kernel **Completely Fair Scheduler (CFS) throttles** the container by denying CPU time slices (`cfs_quota_us`). The process runs slower, but does **not die**.
* **Memory is Incompressible:** The kernel cannot compress physical memory. When a container exceeds its memory limit, the Linux **cgroup OOM Killer terminates the process immediately with `SIGKILL 9` (Exit Code 137)**.

### The `oom_score_adj` Setting
Kubelet sets the Linux kernel `oom_score_adj` based on QoS class:
* **Guaranteed:** `-997` (The kernel will almost never kill this process).
* **Burstable:** Scaled dynamically between `2` and `999` based on requested memory ratio.
* **BestEffort:** `1000` (The kernel kills this process first).

---

## 8.32 Three Production Incidents on Kubernetes (STAR Method)

> **The Interview Question:**  
> "Can you describe three severe production incidents you investigated on Kubernetes, detailing the symptom, your diagnostic steps, the fix, and the lasting architectural prevention?"

### Incident 1: Microservice V8 Heap OOMKilled Cascades (Exit Code 137)
* **Symptom:** Core backend Pods intermittently crashed and restarted with `CrashLoopBackOff` during peak business hours, causing cascading 502 errors.
* **Diagnosis:** Checked `kubectl describe pod` and identified `Last State: Terminated`, `Reason: OOMKilled`, `Exit Code: 137`. Correlated timestamps with API logs and discovered a client sent `pageSize=10000`, causing Mongoose to allocate 10,000 heavy document objects in memory, breaching the container's 1 GB memory limit.
* **Fix:** Enforced controller query clamps (`Math.min(pageSize, 100)`), applied `.lean()` for plain JSON serialization, and right-sized container memory limits to 2 GiB.
* **Prevention:** Implemented Prometheus alerts on `container_memory_working_set_bytes / container_spec_memory_limit_bytes > 0.85` and integrated automated load tests in the CI/CD pipeline.

### Incident 2: Ingress 504 Gateway Timeouts During Long-Running AI Inference
* **Symptom:** Clients uploading images to our vision inference API received intermittent 504 Gateway Timeout errors.
* **Diagnosis:** Inspected Nginx Ingress Controller logs. Large image prefill and vision model inference took 154 seconds, exceeding the default 60-second Nginx `proxy-read-timeout`. When Nginx timed out and severed the upstream socket, the delayed application response attempted to write headers to a closed stream, triggering fatal `ERR_HTTP_HEADERS_SENT` crashes.
* **Fix:** Added Ingress annotations `nginx.ingress.kubernetes.io/proxy-read-timeout: "300"` and `proxy-send-timeout: "300"`, and patched the application gateway with `if (response.headersSent) return;` stream guards.
* **Prevention:** Decoupled long-running AI inference onto an asynchronous queue architecture (SQS/Celery) returning 202 Accepted with polling.

### Incident 3: StatefulSet Pod Stuck in Pending After Node Eviction (Multi-AZ EBS Lock)
* **Symptom:** Following a spot node termination in AWS, a database StatefulSet Pod remained permanently stuck in `Pending`.
* **Diagnosis:** Ran `kubectl describe pod` and found: `0/6 nodes available: 1 volume node affinity conflict`. The Pod’s underlying AWS EBS volume was physically located in `us-east-1a`, but all schedulable nodes were in `us-east-1b`.
* **Fix:** Manually took an EBS snapshot, created a new volume in `us-east-1b`, and re-bound the PV to restore immediate availability.
* **Prevention:** Updated the StorageClass with `volumeBindingMode: WaitForFirstConsumer` so volumes are provisioned only after the scheduler places the Pod, and configured Karpenter with multi-AZ topology spread constraints.

---

## 8.33 Scheduling Pods on Control-Plane / Master Nodes

> **The Interview Question:**  
> "Why are ordinary Pods prevented from scheduling on control-plane nodes by default, and how can you override this behavior in development or edge clusters?"

### The Default Taint
Control-plane nodes carry the system taint:
`node-role.kubernetes.io/control-plane:NoSchedule`

### Overriding the Taint
1. **Add Toleration to Specific Pod:**
   ```yaml
   tolerations:
     - key: "node-role.kubernetes.io/control-plane"
       operator: "Exists"
       effect: "NoSchedule"
   ```
2. **Remove the Taint Entirely (For single-node dev/edge clusters):**
   ```bash
   kubectl taint nodes <node-name> node-role.kubernetes.io/control-plane:NoSchedule-
   ```

### Why Banned in Production
Worker workloads running on master nodes compete with `kube-apiserver`, `scheduler`, and `etcd` for CPU, memory, and disk I/O. A noisy neighbor container causing high disk I/O latency will starve etcd fsync operations, causing leader election drops and bringing down the entire cluster.

---

## 8.34 Horizontal (HPA) vs Vertical (VPA) Pod Autoscaling

> **The Interview Question:**  
> "How do Horizontal Pod Autoscaler (HPA) and Vertical Pod Autoscaler (VPA) differ, and why should you never combine them on the same metric?"

### Architectural Comparison

| Dimension | Horizontal Pod Autoscaler (HPA) | Vertical Pod Autoscaler (VPA) |
| :--- | :--- | :--- |
| **Scaling Mechanism** | Adds or removes **Pod replicas** | Modifies **CPU/Memory requests and limits** |
| **Disruption** | Zero downtime (dynamic scaling) | **Disruptive:** Recreates and restarts Pods to apply new limits |
| **Best For** | Stateless microservices, web apps | Stateful databases, single-replica workloads |
| **Metric Sources** | CPU, Memory, KEDA custom metrics (queue depth) | Historical container resource consumption |

### The Golden Conflict Rule
**Never run HPA and VPA simultaneously on the same metric (e.g. CPU).**
* Under high CPU load, HPA tries to scale out pods while VPA tries to increase pod CPU requests.
* VPA restarts pods while HPA is attempting to add capacity, causing violent scaling thrashing.
* **Production Best Practice:** Run **HPA for dynamic scaling**, and run **VPA in `mode: "Off"`** (recommendation mode) to continuously calculate right-sizing advice without executing restarts.

---

## 8.35 Types of Secrets and Production Secret Management

> **The Interview Question:**  
> "What types of Secrets exist in Kubernetes, what is their fundamental security flaw by default, and how do you implement enterprise secret management?"

### Secret Types

| Secret Type | Purpose |
| :--- | :--- |
| **`Opaque`** (Default) | Arbitrary user-defined key-value configuration |
| **`kubernetes.io/tls`** | TLS certificates and private keys (`tls.crt`, `tls.key`) used by Ingress |
| **`kubernetes.io/dockerconfigjson`** | Container registry credentials for `imagePullSecrets` |
| **`kubernetes.io/service-account-token`** | Legacy ServiceAccount authentication tokens |

### The Default Security Flaw
**Kubernetes Secrets are NOT encrypted by default; they are merely Base64 encoded.** Anyone with `get secret` RBAC permissions or direct access to etcd can decode them in one command:
```bash
echo "cGFzc3dvcmQ=" | base64 --decode
```

### Enterprise Production Hardening
1. **etcd Encryption at Rest:** Enable KMS envelope encryption in `kube-apiserver` using AWS KMS so secrets are encrypted on physical disk.
2. **External Secrets Operator (ESO):** Synchronize secrets directly from **AWS Secrets Manager** or HashiCorp Vault into Kubernetes memory. Never commit secrets to Git.
3. **Secrets Store CSI Driver:** Mount secrets directly as in-memory volumes into the container filesystem from AWS Secrets Manager, ensuring sensitive tokens never touch etcd.
4. **Mount as Files, Never Env Vars:** Environment variables leak into crash logs, core dumps, and child process inspections (`/proc/1/environ`). Always mount sensitive secrets as file volumes.
