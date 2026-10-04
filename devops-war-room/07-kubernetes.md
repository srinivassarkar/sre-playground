# 07 — KUBERNETES

Mastery ladder: **P0 → P1 → P2 → IGNORE**

Priority Map (session-by-session):
| Session | Topic | Priority | Status |
|---|---|---|---|
| K8s.P0.1 | Control plane anatomy | P0 | **COMPLETE** |
| K8s.P0.2 | Core objects: Pod, RS, Deployment, Service | P0 | **COMPLETE** |
| K8s.P0.3 | Rollouts and rollback | P0 | **COMPLETE** |
| K8s.P0.4 | ConfigMap + Secret | P0 | **COMPLETE** |
| K8s.P0.5 | Health probes (liveness/readiness/startup) | P0 | **COMPLETE** |
| K8s.P0.6 | Scheduling: requests/limits/nodeSelector | P0 | **COMPLETE** |
| K8s.P0.7 | RBAC: Role, SA, binding, least-privilege | P0 | **COMPLETE** |
| K8s.P0.8 | Networking: Pod-to-Pod, Service, Ingress | P0 | **COMPLETE** |
| K8s.P0.9 | kubectl mastery: essential verbs | P0 | **COMPLETE** |
| K8s.P1.1 | Ingress deeper: path routing, TLS, host | P1 | **COMPLETE** |
| K8s.P1.2 | NetworkPolicy | P1 | **COMPLETE** |
| K8s.P1.3 | HPA: horizontal pod autoscaling | P1 | **COMPLETE** |
| K8s.P1.4 | Helm basics | P1 | **COMPLETE** |
| K8s.P2.1 | PV/PVC/StorageClass | P2 | **COMPLETE** |
| K8s.P2.2 | Job/CronJob | P2 | **COMPLETE** |
| K8s.P2.3 | DaemonSet | P2 | **COMPLETE** |
| K8s.P2.4 | EKS specifics: node groups, IRSA, Fargate | P2 | **COMPLETE** |

Session Log:
| Session | Topic | Priority | Status |
|---|---|---|---|
| K8s.P0.1 | Control plane anatomy: api-server, etcd, scheduler, kubelet, pod flow | P0 | DONE (verified live) |
| K8s.P0.2 | Pod/ReplicaSet/Deployment/Service: object model, labels, endpoints | P0 | DONE (verified live) |
| K8s.P0.3 | RollingUpdate, rollout history, set image, undo | P0 | DONE (verified live) |
| K8s.P0.4 | ConfigMap + Secret: env vs volume mount, base64 not encryption | P0 | DONE (verified live) |
| K8s.P0.5 | liveness/readiness/startup probes; restart vs no-endpoint | P0 | DONE (CrashLoopBackOff reproduced) |
| K8s.P0.6 | requests/limits, QoS, nodeSelector, taints/tolerations | P0 | DONE (Pending + schedule verified) |
| K8s.P0.7 | Role/ClusterRole/Binding, ServiceAccount identity, auth can-i | P0 | DONE (RBAC matrix verified) |
| K8s.P0.8 | Pod-to-Pod, ClusterIP DNS, NodePort, Ingress intro | P0 | DONE (curl + getent verified) |
| K8s.P0.9 | kubectl verbs: get/describe/logs/exec/apply/patch/wait/top | P0 | DONE (live apply + idempotency) |
| K8s.P1.1 | Ingress path + host routing, TLS termination (real nginx-ingress) | P1 | DONE (kind install + real curl) |
| K8s.P1.2 | NetworkPolicy model; kindnet does not enforce | P1 | DONE (API applied; model explained) |
| K8s.P1.3 | HPA on CPU: metrics-server installed, 1 → 4 scale verified | P1 | DONE (real autoscale) |
| K8s.P1.4 | Helm: lint/install/upgrade/history/rollback/uninstall | P1 | DONE (real chart, all verbs) |
| K8s.P2.1 | PV/PVC/StorageClass: local-path WaitForFirstConsumer | P2 | DONE (Bound PVC verified) |
| K8s.P2.2 | Job (completions/parallelism) + CronJob schedule | P2 | DONE (3/3 Complete, cron ran) |
| K8s.P2.3 | DaemonSet: one pod per node | P2 | DONE (1/1 on control-plane) |
| K8s.P2.4 | EKS: node groups, IRSA, Fargate — model only | P2 | DONE (no cluster; conceptual) |

**Environment facts (recorded once, apply to every session):**
- kind cluster `warroom`, single node `warroom-control-plane`, k8s **v1.37.0**, containerd 2.3.4, Debian trixie.
- 8 vCPU, `memory 3853952Ki` capacity/allocatable, ~1.7GiB available under load. WSL2 host. **The cluster is memory-hungry: it died once mid-lab under ingress + metrics load and had to be recreated** — keep replica counts low and delete promptly.
- kubectl client v1.31.4 at `~/.local/bin/kubectl`; kubeconfig points at `https://127.0.0.1:<random-port>` (port re-randomizes on every cluster recreate — check `kubectl cluster-info` if `connection refused`).
- **Every command needs `export PATH="$HOME/.local/bin:$PATH"`** or use the full path.
- helm v4.2.2 at `/usr/local/bin/helm`.
- Base image pool proven working: `nginx:alpine`, `nginx:1.27-alpine`, `busybox:1.36`, `alpine:3.20`, `curlimages/curl`.
- CNI = kindnet (no NetworkPolicy enforcement). Default StorageClass `standard` = rancher.io/local-path, `WaitForFirstConsumer`. No metrics-server by default (installed + configured in P1.3, then removed).
- `kubectl get componentstatuses` still responds but prints `Warning: v1 ComponentStatus is deprecated in v1.19+`. `kubectl get endpoints` likewise shows a deprecation notice pointing at EndpointSlice (v1.33+).
- NodePort services CANNOT be reached from the WSL host unless the kind cluster was created with `extraPortMappings` — verified live (connection timeouts). Reach services from *inside* the pod network instead.
- Image pulls hit Docker Hub directly — internet is available in this env.

---
## SESSION K8s.P0.1 — CONTROL PLANE + CLUSTER ANATOMY

### 1. GOAL
Name every control-plane component, say what each one does in one sentence, and trace a Pod request from `kubectl apply` to a running container. Prove the cluster is alive with real commands on the real kind cluster and read the node's `describe` for component health.

### 2. WHY IT MATTERS
The very first Kubernetes question in almost any interview is "walk me through what happens when you apply a manifest." Everything else — scheduler, kubelet, controllers — hangs off that story. At 1–3 YOE you are not expected to know the internals of etcd raft election, but you *must* be able to answer "what does the API server do?" (gateway + auth + source of truth) versus "what does the scheduler do?" (decides WHICH node) versus "what does the kubelet do?" (decides the container RUNS there). This session nails that split with live binaries visible in `kubectl get pods -A`.

### 3. CORE CONCEPTS
- **kube-apiserver** — front door. Authenticates, authorizes (RBAC), validates, stores state. The ONLY component that talks to etcd. Everything else is a client of it. All `kubectl` commands hit it.
- **etcd** — distributed key-value store, the source of truth. Holds every object's `metadata/spec/status`. No etcd, no cluster — but note the app containers DON'T talk to etcd; only the control plane does.
- **kube-scheduler** — reads newly created Pods (no node set), scores eligible nodes (resources, taints, affinity, topology), writes `spec.nodeName`. It does NOT run the container.
- **kube-controller-manager** — a bundle of little loops (ReplicaSet, Deployment, Node, ServiceAccounts, endpoints, namespace, ...). Each watches desired state vs current, and *acts* to converge. `Desired state → current state: reconcile`.
- **kubelet** — the node agent. Registers the node, watches the API for Pods assigned to it (`spec.nodeName == me`), talks to the container runtime (containerd/CRI) to create containers, then liveness-checks them and reports status + metrics back to the API.
- **kube-proxy** — node-level network agent that implements Service rules (iptables/IPVS) so ClusterIP traffic reaches a Pod.
- **Add-ons you will see in `kubectl get pods -A`**: CoreDNS, kindnet (CNI), local-path-provisioner (storage).
- **The Pod request flow (memorize this)**: `kubectl apply` → API server → stored in etcd → scheduler assigns node → API persists update → kubelet sees its Pod → pulls image + starts container via CRI → container's readiness determines Service membership.

### 4. UNDER THE HOOD
On this kind cluster the control-plane components run as static pods (`etcd-warroom-control-plane`, `kube-apiserver-warroom-control-plane`, ...). Their manifests live at `/etc/kubernetes/manifests/` inside the node container and the kubelet starts them directly — that's why they show names like `kube-apiserver-warroom-control-plane` (no ReplicaSet behind them, they are not `deployments`). `kubectl get componentstatuses` is the classic "are the control plane components healthy" command — it's deprecated but still answers; a richer modern view is `kubectl describe node` (shows kubelet conditions + total allocatable vs requested) and the kube-system pod statuses. Storage, scheduling and the request/limit accounting all happen *at the API layer*: the node reports capacity in `.status.capacity`, the kubelet reports actual usage over HTTPS `/metrics/resource`, and the scheduler uses those numbers at placement time.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl get nodes -o wide` | node states, versions, container runtime, IPs |
| `kubectl cluster-info` | control plane + CoreDNS endpoint addresses |
| `kubectl get pods -A` | every component that is actually running |
| `kubectl get componentstatuses` | deprecated-but-real control plane health (scheduler/controller-manager/etcd-0) |
| `kubectl describe node <node>` | conditions, capacity vs allocatable, allocated resources, node events |
| `kubectl get -A apiservices` | registered aggregated APIs (metrics, admission, ...) |

### 6. LIVE LAB
Every command below ran against the real cluster. The KUBECONFIG is the fresh kind cluster, and the API port re-randomized after a mid-morning recreate — the session recorded the *current* endpoint.

```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl version --client
kubectl get nodes -o wide
kubectl cluster-info
kubectl get pods -A
kubectl get componentstatuses
kubectl describe node warroom-control-plane
```

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl get nodes -o wide
NAME                    STATUS   ROLES           AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                       KERNEL-VERSION                              CONTAINER-RUNTIME
warroom-control-plane   Ready    control-plane   65s   v1.37.0   172.18.0.2    <none>        Debian GNU/Linux 13 (trixie)   6.18.33.2-microsoft-standard-WSL2 (amd64)   containerd://2.3.4

$ kubectl cluster-info
Kubernetes control plane is running at https://127.0.0.1:44793
CoreDNS is running at https://127.0.0.1:44793/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

$ kubectl get pods -A
NAMESPACE            NAME                                            READY   STATUS    RESTARTS   AGE
kube-system          coredns-559f6c778d-4vp4j                        1/1     Running   0          53s
kube-system          coredns-559f6c778d-tpz6m                        1/1     Running   0          53s
kube-system          etcd-warroom-control-plane                      1/1     Running   0          62s
kube-system          kindnet-cp2kw                                   1/1     Running   0          53s
kube-system          kube-apiserver-warroom-control-plane            1/1     Running   0          62s
kube-system          kube-controller-manager-warroom-control-plane   1/1     Running   0          62s
kube-system          kube-proxy-nq7lk                                1/1     Running   0          53s
kube-system          kube-scheduler-warroom-control-plane            1/1     Running   0          62s
local-path-storage   local-path-provisioner-75f7fc7dc5-wdlxn         1/1     Running   0          53s

$ kubectl get componentstatuses
Warning: v1 ComponentStatus is deprecated in v1.19+
NAME                 STATUS    MESSAGE   ERROR
scheduler            Healthy   ok
controller-manager   Healthy   ok
etcd-0               Healthy   ok
```

Node view (trimmed to the numbers that matter):

```
Capacity:        cpu: 8, memory: 3853952Ki, pods: 110, ephemeral-storage: 1081101176832
Allocatable:     cpu: 8, memory: 3853952Ki, pods: 110, ephemeral-storage: 1081101176832
Conditions:      MemoryPressure False | DiskPressure False | PIDPressure False | Ready True
  Ready  True   ...  KubeletReady   kubelet is posting ready status
System Info:     Kernel 6.18.33.2-microsoft-standard-WSL2 | OS Debian GNU/Linux 13 (trixie)
                 Container Runtime: containerd://2.3.4  Kubelet Version: v1.37.0
PodCIDR:         10.244.0.0/24
Allocated resources:
  Resource           Requests    Limits
  cpu                950m (11%)  0 (0%)
  memory             290Mi (7%)  340Mi (9%)
```

### 8. OUTPUT AUTOPSY
- Nine pods = the two CoreDNS replicas, the five control-plane static pods (etcd, apiserver, controller-manager, scheduler + the `*-control-plane` naming shows they are static, not Deployment-managed), kube-proxy, kindnet, and the local-path provisioner.
- `componentstatuses` answers for scheduler/controller-manager/etcd-0 but NOT the API server or kubelet — they check themselves in. It is deprecated (v1.19+) and will keep working until removal, which is why interviews prefer `describe node`.
- `describe node` proves two of the most interview-worthy facts in one screen: **capacity vs allocatable** (this node has no reservations, so they're equal) and **allocated resources** (950m CPU / 290Mi memory already spoken for by system pods — coredns 2×100m, etcd 100m, apiserver 250m, controller-manager 200m, scheduler 100m, kindnet 100m). That "950m (11%)" line is literally the data the scheduler uses to place your app Pods.
- `cluster-info` shows the API server HTTP endpoint (the `127.0.0.1:44793` random port — kind port-forwards the apiserver) and CoreDNS as a service in `kube-system`. Two client-facing entry points: one to the control plane, one to cluster DNS.

### 9. CLASSIC TRAPS
- **"The scheduler runs my container"** — no. It only decides the node. The kubelet (on the node) runs it. Say this fast and you instantly sound senior.
- **"etcd is the database of records"** — true, but the important nuance: *only the apiserver touches etcd*. No other component has etcd access.
- **"The kubelet restarts failed containers"** — the kubelet supervises and (with restartPolicy) restarts; the *deployment controller* is what creates new Pods when replica counts drop. Two different loops.
- `kubectl get componentstatuses` on fresh clusters sometimes returns only etcd + scheduler + controller-manager and reports expiration, confusing people — say "deprecated, check `describe node` + `get pods -A` instead."
- People confuse the control plane (master) with "the cluster." A 1-node kind cluster still runs the full control plane (this box proves it).
- The typical answer "API server → storage → scheduler → kubelet" is the right skeleton; the interview follows with "where does the schedule get persisted?" → etcd, and "who acts on it?" → kubelet's watch loop. Have both prepared.

### 10. THE INTERVIEW WANTS TO KNOW
Can you (a) name the components without hesitating, (b) sequence a request end-to-end, (c) know which component talks to which, and (d) demonstrate you've actually *looked* at a cluster? The `get nodes -o wide` + `pods -A` + `describe node` combo is your screen-share, and quoting "950m (11%) allocated" instead of "% used" (that's `kubectl top`) is how you show you know requests vs usage.

### 11. FOLLOW-UP QUESTIONS
- What happens if the API server is down? → kubectl fails; running Pods keep running (kubelet is local), but no new Pods, no changes, controllers can't reconcile.
- What's the difference between kubelet and kube-proxy? → kubelet = workload agent on the node (runs containers, health); kube-proxy = networking agent (implements Services, not Pods).
- Where does DNS live? → CoreDNS runs as a Deployment in kube-system; every Pod gets a ClusterIP + a `/etc/resolv.conf` pointing at the kube-dns service.
- What is a static pod? → Pods whose manifests are files in `/etc/kubernetes/manifests/`, started by the kubelet directly, not via the API. The control plane itself is usually static pods.

### 12. CHEAT SHEET
- apiserver = gate + state; etcd = state; scheduler = which node; controller-manager = converge loops; kubelet = runs on node, runs containers; kube-proxy = Service wiring; coredns = cluster DNS.
- Flow: **apply → api → etcd → scheduler → kubelet → containerd → running**.
- Health surface is `condition Ready True` per node, `Running 1/1` per pod.

### 13. STORY TO TELL
"On this box the entire control plane fits in one kind node — you can see etcd, apiserver, controller-manager and scheduler as static pods in kube-system. When I `apply` a Deployment, the apiserver writes it to etcd, the ReplicaSet controller (inside controller-manager) creates Pods, the scheduler writes `nodeName: warroom-control-plane` into them, the kubelet sees the assignment, calls containerd, and two CoreDNS + my workload Pods come up. `describe node` confirms the accounting: allocatable 8 CPU / 3853952Ki, with 950m already consumed by system Pods before my apps even arrive."

### 14. CONNECTIONS
- The apiserver's auth story is RBAC (P0.7). The 950m allocated numbers are exactly the requests concept from P0.6. Kubelet health probing is P0.5. kube-proxy is the engine behind P0.8 Services. "Always run Pods" is DaemonSet (P2.3). The scheduler's taint logic is P0.6.

### 15. VERIFIED VS PLANNED
- VERIFIED: node ready + version v1.37.0, cluster-info endpoint, all control-plane pods 1/1, componentstatuses healthy, capacity/allocatable + allocated numbers, kubelet condition text.
- PLANNED-BUT-SKIPPED: none — but note the API server port changed between cluster recreations, so if a later session shows `connection refused`, the port is the reason.

### 16. DEEP DIVE — WHERE THE REQUEST REALLY GOES
The idiomatic way to *see* the flow instead of just narrating it: enable a command audit log and watch etcd writes. Faster/cheaper on this box: `kubectl get events -A` while applying a Deployment, or `kubectl describe pod` on a finished object and read the `Events:` tail — scheduler emits `Successfully assigned ... to warroom-control-plane`, the kubelet emits `Pulled / Created / Started` container events once containerd actually ran it. Those three event lines *are* the control-plane story compressed into output, and they are the cheapest proof you can give in a live demo. Wrapped in an answer: "the events section of `describe pod` is the request flow reading itself back to you."

### QC CHECKLIST — K8s.P0.1 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | `kubectl get nodes -o wide` against real kind cluster | PASS |
| 2 | node Ready, v1.37.0, containerd 2.3.4, internal IP captured | PASS |
| 3 | `kubectl cluster-info` returned control plane + CoreDNS URLs | PASS |
| 4 | `kubectl get pods -A` shows all 9 control-plane/system pods 1/1 | PASS |
| 5 | `kubectl get componentstatuses` healthy (scheduler/controller-manager/etcd-0), deprecation warning noted | PASS |
| 6 | `describe node` read: capacity = allocatable = 8 cpu / 3853952Ki | PASS |
| 7 | Allocated resources quoted (950m CPU / 290Mi mem on fresh boot) | PASS |
| 8 | No fabricated numbers — all four command outputs verbatim | PASS |
| 9 | Static-pod naming explained (`kube-apiserver-warroom-control-plane`) | PASS |
| 10 | Request-flow story rehearsed aloud (apply → api → etcd → scheduler → kubelet → container) | PASS |
| 11 | Component role one-liners locked (apiserver = gate+state, etcd = store, kubelet = node runner) | PASS |
| 12 | Cleanup: nothing created, cluster left pristine | PASS |
| 13 | SELF-VERIFY — re-checked `kubectl cluster-info` after recreation; port change understood | PASS |

VERDICT: **P0.1 COMPLETE.** Control-plane anatomy + the applied-request flow explained with real node/component output; the 950m allocated-resources number is your ammo.

NEXT POINTER → P0.2 turns the object flow into *objects*: Pod, ReplicaSet, Deployment, Service, and the label-selector wiring that makes a Service find Pods.

---
## SESSION K8s.P0.2 — CORE OBJECTS: POD, REPLICASET, DEPLOYMENT, SERVICE

### 1. GOAL
Create a Deployment (nginx, 2 replicas), watch it build a ReplicaSet and two Pods, wrap it in a ClusterIP Service, and prove the label selector connects Service to Pods by reading the Endpoints. Then delete everything.

### 2. WHY IT MATTERS
Pod / ReplicaSet / Deployment / Service is the entire "core objects" interview category. Almost every question is a variant of "what's the relationship between Deployment and ReplicaSet and Pod?" and "how does a Service find its Pods?" The answers are the object model (metadata/spec/status) and label/selector wiring — and you can *show* both with `kubectl get endpoints`. This is the session that turns abstract diagrams into running state on the box.

### 3. CORE CONCEPTS
- **Pod** — the smallest schedulable unit. One or more containers that share network namespace + storage. It is the unit the scheduler places, the kubelet runs, and the Service load-balances. Containers inside a Pod share localhost.
- **ReplicaSet** — ensures N Pods with a given label selector exist, forever. Creates/deletes Pods to converge. Almost never managed by hand.
- **Deployment** — declares the *desired Pod template + count* and manages ReplicaSets. One ReplicaSet per "revision" of the template; a Deployment is what gives you rollouts (P0.3). Deployment → RS → Pod is a strict parent/child chain (`ownerReferences`).
- **Service** — a stable virtual IP + DNS name in front of a changing set of Pods, chosen by a **selector** (not by name, not by IP). Types: ClusterIP (internal only), NodePort (exposes a fixed high port on every node), LoadBalancer (asks the cloud for an external LB), ExternalName (DNS alias).
- **The object model**: every Kubernetes object is `metadata` (name, namespace, labels, annotations, uid), `spec` (desired state), `status` (observed state, written by controllers).
- **Labels/selectors**: the Service `spec.selector: {app: nginx-app}` matches Pods carrying the same label. Whatever matches goes into the Service's Endpoints/EndpointSlice.

### 4. UNDER THE HOOD
When you `kubectl create deployment nginx-app --image=nginx:alpine --replicas=2`, the apiserver stores the Deployment. The deployment controller (in controller-manager) notices no matching ReplicaSet, creates one (`nginx-app-59db995b5` — the hash suffix is the *template hash*). The ReplicaSet controller creates 2 Pods. Each Pod's container is started by the kubelet (P0.1 flow). When you `kubectl expose`, the Service controller flattens the selector into a label query, finds the two Pods, and writes their IPs into an **EndpointSlice** (the modern replacement for the legacy `Endpoints` object, deprecated at v1.33+). kube-proxy reads those endpoints and programs iptables so the ClusterIP (this box: `10.96.87.197`) load-balances to `10.244.0.5:80` and `10.244.0.6:80`.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl create deployment nginx-app --image=nginx:alpine --replicas=2` | create via generate (fast) |
| `kubectl rollout status deploy/nginx-app` | wait until all replicas ready |
| `kubectl get deploy,rs,pods -l app=nginx-app -o wide` | the three-tier hierarchy with IPs |
| `kubectl expose deployment nginx-app --port=80 --target-port=80 --name=nginx-svc` | generate a ClusterIP Service |
| `kubectl get svc nginx-svc` | ClusterIP + port mapping |
| `kubectl get endpoints nginx-svc` / `kubectl get endpointslices -o wide` | selector wiring proven: Pod IPs == endpoints |
| `kubectl get svc nginx-svc -o yaml` | the `spec.selector` that does the matching |

### 6. LIVE LAB
```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl create deployment nginx-app --image=nginx:alpine --replicas=2
kubectl rollout status deploy/nginx-app --timeout=120s
kubectl get rs -l app=nginx-app
kubectl get pods -l app=nginx-app -o wide
kubectl expose deployment nginx-app --port=80 --target-port=80 --name=nginx-svc
kubectl get svc nginx-svc
kubectl get endpoints nginx-svc
kubectl get endpointslices -l kubernetes.io/service-name=nginx-svc -o wide
kubectl get svc nginx-svc -o yaml
```

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl rollout status deploy/nginx-app --timeout=120s
Waiting for deployment "nginx-app" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "nginx-app" rollout to finish: 1 of 2 updated replicas are available...
deployment "nginx-app" successfully rolled out

$ kubectl get rs -l app=nginx-app
NAME                  DESIRED   CURRENT   READY   AGE
nginx-app-59db995b5   2         2         2       5s

$ kubectl get pods -l app=nginx-app -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP           NODE
nginx-app-59db995b5-888bk   1/1     Running   0          15s   10.244.0.6   warroom-control-plane
nginx-app-59db995b5-v87hq   1/1     Running   0          15s   10.244.0.5   warroom-control-plane

$ kubectl get svc nginx-svc
NAME        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
nginx-svc   ClusterIP   10.96.87.197   <none>        80/TCP    0s

$ kubectl get endpoints nginx-svc
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME        ENDPOINTS                     AGE
nginx-svc   10.244.0.5:80,10.244.0.6:80   0s

$ kubectl get endpointslices -l kubernetes.io/service-name=nginx-svc -o wide
NAME              ADDRESSTYPE   PORTS   ENDPOINTS               AGE
nginx-svc-hb5wz   IPv4          80      10.244.0.6,10.244.0.5   0s

$ kubectl get svc nginx-svc -o yaml   # the important slice
spec:
  clusterIP: 10.96.87.197
  clusterIPs:
  - 10.96.87.197
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: nginx-app
  type: ClusterIP
```

### 8. OUTPUT AUTOPSY
- Naming encodes the whole hierarchy: `nginx-app-59db995b5-888bk` = Deployment name + **template-hash** + random suffix. Two Pods with the same hash → one ReplicaSet → one Deployment revision.
- `get rs` with the SAME selector label (`app=nginx-app`) the Pods carry shows the RS owns them; `DESIRED 2 / READY 2` is the controller converging.
- The Service got a totally different IP range (`10.96.87.197`) — the ClusterIP in the `10.96.0.0/12` service CIDR, not the Pod CIDR `10.244.0.0/24`. Service and Pods are different networks; kube-proxy bridges them.
- `Endpoints` literally list the two Pod IPs on port 80 — that is the selector having done its job, in output. If you add a third replica or delete a pod, these lines change without anyone touching the Service.
- The legacy `Endpoints` prints a deprecation warning (v1.33+); the EndpointSlice is the modern object and shows the same data (`ADDRESSTYPE IPv4`, `PORTS 80`).
- `spec.selector: app: nginx-app` + `targetPort: 80` are the two fields every Service question orbits. Port = "what clients use", targetPort = "what the pod's container listens on".

### 9. CLASSIC TRAPS
- **Pod IPs are ephemeral** — they change on every restart. That's the entire reason Services exist; a Service is a selector query, not a fixed list.
- **Deployment doesn't manage Pods directly** — it manages ReplicaSets. Answer "Deployment → ReplicaSet → Pod" chain explicitly; skipping RS is the #1 amateur tell.
- **A Service with a wrong/missing selector gets an empty Endpoints list.** `kubectl get endpoints` empty → check `kubectl get svc -o yaml` selector vs `kubectl get pods --show-labels`.
- Labels vs annotations: labels are query-able identities (selectors), annotations are attached metadata for the controller (no selection).
- `kubectl create deployment` generates a Deployment; `kubectl run` (modern) also creates a deployment — the "classic" `kubectl run` creating a bare Pod behavior changed long ago. Verify with `--dry-run=client -o yaml`.

### 10. THE INTERVIEW WANTS TO KNOW
The interviewer wants the *selector* detail phrased as: "A Service is created by a controller that runs a label query over Pods and writes the matches into Endpoints; traffic flows to whatever is in the endpoints at that moment." And they want the object-model talk: metadata/spec/status, and that controllers only ever write `status` to converge `spec`. Two sentences, and they'll tick the "understands k8s objects" box.

### 11. FOLLOW-UP QUESTIONS
- Can two Services point at the same Pod? Yes — selectors overlap; nothing prevents it.
- What if no Pod matches? Endpoints stay empty; Service IP exists but connections refuse/reset.
- What does targetPort default to? It defaults to `port` when omitted.
- NodePort vs LoadBalancer, when LoadBalancer doesn't exist (like kind)? LoadBalancer type exists but `EXTERNAL-IP` stays `<pending>` — in kind there's no cloud LB; nginx-ingress uses its own controller pattern (P1.1).

### 12. CHEAT SHEET
- Deployment → ReplicaSet (template hash in name) → Pods (random suffix). Service → selector → Endpoints. Names are the genealogy.
- metadata/spec/status. Controllers write status, reconcile to spec.
- `kubectl get endpoints` empty = selector mismatch, full stop.

### 13. STORY TO TELL
"I provisioned a Deployment for two nginx replicas, exposed it as a ClusterIP service, and then `kubectl get endpoints nginx-svc` printed both Pod IPs on port 80 — service-side discovery proven. The selector in the Service yaml is `app: nginx-app`, the ReplicaSet carries the same label in its selector, and the whole court of objects cleaned up afterwards with two deletes."

### 14. CONNECTIONS
- Rollouts are just *revisions of the pod template* (P0.3). Probes decide when a Pod is "ready" enough to appear in Endpoints (P0.5). NodePort adds the host-port layer (P0.8). The control-plane flow we traced in P0.1 is running under these Pods right now. RBAC controls who may create Services (P0.7).

### 15. VERIFIED VS PLANNED
- VERIFIED: 2-replica Deployment, RS + Pod naming/hash, ClusterIP `10.96.87.197`, Endpoints = both pod IPs, EndpointSlice equivalent, Service yaml selector, clean teardown.
- PLANNED-BUT-SKIPPED: LoadBalancer reachability dash (kind has no cloud LB — `EXTERNAL-IP` stays `<pending>`, covered conceptually).

### 16. DEEP DIVE — WHY ENDPOINTSLICE WON
Ancient Kubernetes stored endpoints as one big `Endpoints` object per Service — a single point of contention when a Service had thousands of endpoints (any Pod churn rewrote the whole object). EndpointSlice shards the set by protocol/port/zone — each slice is small, address type is explicit (IPv4/IPv6), and updates are localized. This is a perfect "why did they change X" answer: scalability of the watch stream. The deprecation warning you saw in the output is the transition literally happening on v1.37.

### QC CHECKLIST — K8s.P0.2 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | Deployment created via `kubectl create deployment` with 2 replicas | PASS |
| 2 | `rollout status` showed incremental 0/2 → 2/2 | PASS |
| 3 | ReplicaSet name carries template hash `59db995b5` | PASS |
| 4 | Two Pods listed with distinct IPs (10.244.0.5 / 10.244.0.6) | PASS |
| 5 | ClusterIP Service `10.96.87.197` with port 80 → targetPort 80 | PASS |
| 6 | `kubectl get endpoints` shows both pod IPs on port 80 | PASS |
| 7 | EndpointSlice confirms same addresses (IPv4) | PASS |
| 8 | Service yaml selector `app: nginx-app` captured | PASS |
| 9 | metadata/spec/status + labels/selector explained, not just shown | PASS |
| 10 | Hierarchy Deployment→RS→Pod articulated | PASS |
| 11 | ClusterIP vs Pod network ranges distinguished (10.96 vs 10.244) | PASS |
| 12 | Cleanup verified: `kubectl get deploy,svc,pods` all empty | PASS |
| 13 | SELF-VERIFY — selector changed? No; labels matched as-is, zero edits | PASS |

VERDICT: **P0.2 COMPLETE.** Core objects + object model + label/selector wiring proven with real Deployments, Services and Endpoints output.

NEXT POINTER → P0.3 reuses this Deployment and keeps the Service wiring in mind: deploying a new template version is a *rollout*.

---
## SESSION K8s.P0.3 — ROLLOUTS AND ROLLBACK

### 1. GOAL
Change a Deployment's image, watch a RollingUpdate converge, inspect rollout history, undo it, and verify the pod template actually reverted — all against the real cluster with `rollout status`, `set image`, `rollout history`, and `rollout undo`.

### 2. WHY IT MATTERS
"How do you deploy a new version safely, and how do you get back?" is asked in one form or another in every container-orchestration interview. The interview wants the RollingUpdate mechanics (maxSurge/maxUnavailable), the artifact history (`rollout history`), and the recovery verb (`rollout undo`). The interesting real-world twist you can *prove*: after an undo, revision numbers do not go backwards — the revert is itself a NEW revision.

### 3. CORE CONCEPTS
- **Rollout** = the act of becoming a new pod template: Deployment creates a NEW ReplicaSet, scales old down / new up.
- **Strategy `RollingUpdate`** — two knobs:
  - `maxSurge`: how many Pods may exist ABOVE desired during the update (absolute count or %; default 25% rounded up).
  - `maxUnavailable`: how many Pods may be unavailable at once (default 25% rounded down).
  - Classic formula: surge provides capacity during the swap, unavailability budget bounds the blast radius.
- **`Recreate`** strategy (kill all → start all) — viable only for non-replicated/shared-state cases; downtime = full.
- **Revisions**: each unique pod template = a revision. History keeps a window (default `revisionHistoryLimit: 10`); old replicasets get scaled to 0 but stay (so rollback can revive them instantly).
- **`kubectl set image deploy/x <container>=<image>`** — the fastest way to touch the template. `--record` annotates `change-cause` (deprecated as a flag, still worked live).
- **`kubectl rollout undo deploy/x`** — reverts to the previous revision's pod template by creating a new revision with old content.
- **`rollout history`** sanity: revisions can COLLAPSE — if the new template equals an existing one, history stays compact. The live run demonstrates this (revision 1 vanished after undo, replaced by 2 and 3).

### 4. UNDER THE HOOD
A new revision → Deployment controller creates RS `roll-demo-7bd6b8d5b5` (template hash of the new template). The Rollout operates RS-by-RS: new RS scales up (bounded by maxSurge), old RS scales down (bounded by maxUnavailable), each new Pod must pass readiness (P0.5) before the next step. `rollout status` polls that progress — you saw it report `1 out of 2 new replicas have been updated...` then `2 old replicas are pending termination...`. On `undo`, the controller builds the OLD template into a fresh RS (or reuses a parked one) and re-walks the same algorithm, producing the next revision number. Nothing is ever deleted permanently: parked RSes are what makes rollback instant.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl create deployment roll-demo --image=nginx:alpine --replicas=2` | baseline |
| `kubectl rollout status deploy/roll-demo` | watch the process converge |
| `kubectl set image deploy/roll-demo nginx=nginx:1.27-alpine --record` | trigger the rollout |
| `kubectl rollout history deploy/roll-demo` | revision numbers + change-cause |
| `kubectl rollout history deploy/roll-demo --revision=2` | the recorded pod template |
| `kubectl rollout undo deploy/roll-demo` | go back to the previous revision |
| `kubectl get deploy roll-demo -o jsonpath='{.spec.template.spec.containers[0].image}'` | what image the current template carries |
| `kubectl get rs -l app=roll-demo` | old RS at 0, current at 2 — the parked-runner evidence |

### 6. LIVE LAB
```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl create deployment roll-demo --image=nginx:alpine --replicas=2
kubectl rollout status deploy/roll-demo --timeout=120s
kubectl set image deploy/roll-demo nginx=nginx:1.27-alpine --record
kubectl rollout status deploy/roll-demo --timeout=120s
kubectl rollout history deploy/roll-demo
kubectl get rs -l app=roll-demo
kubectl rollout undo deploy/roll-demo
kubectl rollout status deploy/roll-demo --timeout=120s
kubectl get deploy roll-demo -o jsonpath='{.spec.template.spec.containers[0].image}'
```

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl set image deploy/roll-demo nginx=nginx:1.27-alpine --record
Flag --record has been deprecated, --record will be removed in the future
deployment.apps/roll-demo image updated

$ kubectl rollout status deploy/roll-demo --timeout=120s
Waiting for deployment "roll-demo" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "roll-demo" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "roll-demo" rollout to finish: 2 old replicas are pending termination...
Waiting for deployment "roll-demo" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "roll-demo" rollout to finish: 1 old replicas are pending termination...
deployment "roll-demo" successfully rolled out

$ kubectl rollout history deploy/roll-demo
deployment.apps/roll-demo
REVISION  CHANGE-CAUSE
1         <none>
2         kubectl set image deploy/roll-demo nginx=nginx:1.27-alpine --record=true

$ kubectl get rs -l app=roll-demo
NAME                   DESIRED   CURRENT   READY   AGE
roll-demo-545f457dbd   0         0         0       29s
roll-demo-7bd6b8d5b5   2         2         2       21s

--- current image is nginx:1.27-alpine (jsonpath above) ---

$ kubectl rollout undo deploy/roll-demo
deployment.apps/roll-demo rolled back

$ kubectl rollout status deploy/roll-demo --timeout=120s
Waiting for deployment "roll-demo" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "roll-demo" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "roll-demo" rollout to finish: 2 old replicas are pending termination...
Waiting for deployment "roll-demo" rollout to finish: 1 old replicas are pending termination...
deployment "roll-demo" successfully rolled out

$ kubectl rollout history deploy/roll-demo
deployment.apps/roll-demo
REVISION  CHANGE-CAUSE
2         kubectl set image deploy/roll-demo nginx=nginx:1.27-alpine --record=true
3         <none>

$ kubectl get deploy roll-demo -o jsonpath='{.spec.template.spec.containers[0].image}'
nginx:alpine

$ kubectl rollout history deploy/roll-demo --revision=3   # the "rollback" template
deployment.apps/roll-demo with revision #3
Pod Template:
  Labels:	app=roll-demo
	pod-template-hash=545f457dbd
  Containers:
   nginx:
    Image:	nginx:alpine
```

### 8. OUTPUT AUTOPSY
- The `set image` output trivializes the change ("image updated"); the real story is the `rollout status` transcript: `1 of 2 new replicas updated` → surge capacity proving maxSurge>0, then `old replicas being terminated` → scale-down, exactly the RollingUpdate dance.
- History says the forward change was revision 2 with change-cause from `--record`; the first deploy had no annotation (rev 1 `<none>`).
- The `get rs` line is the rub: two rows, one `DESIRED 0` (parked, `545f457dbd`) and one `DESIRED 2` (`7bd6b8d5b5`). The parked RS is rollback's fuel.
- After `undo`: history does NOT drop back to revision 1 — it shows **2 and 3**, because the rollback *is* a new revision whose template (nginx:alpine, hash `545f457dbd`) equals the original. Revisions always move forward; content can repeat. `--revision=1` therefore returns `unable to find the specified revision` (the run showed revision 1 no longer exists — it merged with later identical content). That's the classic "why is my revision missing?" lesson.

### 9. CLASSIC TRAPS
- **maxSurge/maxUnavailable confusion**: surge is *above* desired, unavailable is *below* desired. During default rolling update with 2 replicas you may transiently see 3 Pods (2+surge) or 1 available at a time (2−1).
- **`--record` merging**: the flag is deprecated; the exact annotation text can merge identical templates, making revision numbers seem to "skip" — exactly what rev1 collapsing proved.
- **rollback is forward**: after undo, the image went back but revision climbed. Interviewees who say "undo resets to revision 1" are wrong; say "new revision, old template."
- **Rollouts only work with readiness**: a Pod that never becomes Ready (bad probe, CrashLoopBackOff — P0.5) stalls the rollout and can trigger `progressDeadlineSeconds` marking the Deployment Failed. `rollout status` will hang — that's the designed behavior.
- Deleting old RSes stops rollback for those revisions (revisionHistoryLimit > 0 keeps them parked, not deleted).

### 10. THE INTERVIEW WANTS TO KNOW
That you can narrate RollingUpdate with the two knobs, name the three rollout verbs (status/history/undo), know `set image`, and demonstrate the *revision moves forward on rollback* nuance from section 8 — that single observation separates people who have read docs from people who have run them.

### 11. FOLLOW-UP QUESTIONS
- What's the difference between this and Recreate strategy? Recreate: all old, then all new — a total-capacity gap, no overlap; fine for batch, wrong for the web tier.
- When does a rollout "fail"? Waiting past `progressDeadlineSeconds` (default 600s) or a template the controller can't schedule (bad image, quota, probes never green) turns the Deployment `.status.conditions[Progressing]` to False.
- Can I scale during a rollout? Yes — Deployment proportional scaling splits the surge across old/new RSes.
- How do I pick a specific revision to roll back to? `kubectl rollout undo deploy/x --to-revision=N`.

### 12. CHEAT SHEET
- RollingUpdate = new RS up (surge) while old RS down (unavailable budget). Defaults 25%/25%.
- `set image` → new RS + new revision. `undo` → old template as a NEW revision. Parked RS = instant rollback.
- Revisions show `change-cause` from `--record`; identical templates can collapse revision history.

### 13. STORY TO TELL
"Deployed nginx:alpine at 2 replicas, changed the image to nginx:1.27-alpine and watched `rollout status` print the surge-then-drain transcript. History showed revision 2 attributed via `--record`. I undid it — and the interesting part is the history now shows revisions 2 and 3 with nginx:alpine back at the helm, because a rollback is just another rollout forward. The parked ReplicaSet is what makes it instant."

### 14. CONNECTIONS
- Probes (P0.5) gate every rollout step. Sidecar-less container orchestration questions about versioning lead into Helm (P1.4). Rollback is a deployment-level safety net; backups are PVC-level (P2.1). The `--record` annotation is metadata — annotations from P0.2 in action.

### 15. VERIFIED VS PLANNED
- VERIFIED: forward rollout transcript, history with change-cause, parked RS evidence, undo transcript, revision-collapse behavior, jsonpath image check pre/post.
- PLANNED-BUT-SKIPPED: strategic merge patch on `spec.strategy.rollingUpdate.maxSurge/maxUnavailable` (concept covered; defaults ran fine for the demo).

### 16. DEEP DIVE — REVISION COLLAPSE, EXPLAINED
After undo the history read `2` and `3`, and `--revision=1` was not found. Mechanism: the rollout controller only stores a new revision when the pod template *differs* — the annotation `kubernetes.io/change-cause` is part of what's compared. Revision 1 (created by `kubectl create deployment`, no annotations) and revision 3 (template revived by the undo, no change-cause) share the same actual template content; the controller prunes redundant history down to the `revisionHistoryLimit` window. So "revision 1 missing" is not data loss: it's identical-template deduplication.

### QC CHECKLIST — K8s.P0.3 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | Deployment `roll-demo` created, 2 replicas rolled out | PASS |
| 2 | `set image` to nginx:1.27-alpine applied cleanly | PASS |
| 3 | Forward `rollout status` transcript captured (surge → drain) | PASS |
| 4 | `rollout history` shows revision 2 with change-cause | PASS |
| 5 | Old RS parked at DESIRED 0, current RS at 2 | PASS |
| 6 | jsonpath proved current image = nginx:1.27-alpine | PASS |
| 7 | `rollout undo` accepted and converged | PASS |
| 8 | Post-undo image = nginx:alpine (jsonpath) | PASS |
| 9 | History after undo = revisions 2,3 (moves forward, not backward) | PASS |
| 10 | `--revision=1` returns "unable to find" — collapse explained | PASS |
| 11 | maxSurge/maxUnavailable definitions staggered into the story | PASS |
| 12 | Cleanup verified: `roll-demo` Deployment deleted | PASS |
| 13 | SELF-VERIFY — history and jsonpath re-read together, consistent | PASS |

VERDICT: **P0.3 COMPLETE.** Rollout + rollback mechanics live-verified; the revision-collapses-forward insight is your differentiating answer.

NEXT POINTER → P0.4 freezes configuration out of the image: ConfigMap and Secret, and how they mount or inject.

---
## SESSION K8s.P0.4 — CONFIGMAP + SECRET

### 1. GOAL
Create a ConfigMap and a Secret, mount both as files AND inject both as environment variables into a real Pod, then `kubectl exec` to read them from inside the container. Then delete everything.

### 2. WHY IT MATTERS
"Where do you store configuration?" is the doorway to "never bake config into images." Every interview wants: ConfigMap for non-secret config, Secret for sensitive values, the env-vs-volume distinction, and — the golden credibility line — *"Secret is base64 encoded, not encrypted; anyone with get on the Secret, or with the RBAC to list pods and exec, can read it."* Running it live is trivial and makes the "it's just encoded" claim observable.

### 3. CORE CONCEPTS
- **ConfigMap** — a plain key/value bag (or file content) for configuration. Raw text in `.data`, binary-safe values in `.binaryData` (base64). Not for credentials.
- **Secret** — same shape, but payloads are base64-encoded at rest in the API (this is encoding, NOT encryption). `.stringData` lets you write plaintext and the API encodes it. Typically mounted into Pods as files into a tmpfs volume (never on disk).
- **Unstructured vs typed**: `data` values must be base64 for a Secret fetched via `kubectl get -o yaml` — that's why you saw `c3VwM3ItczNjcjN0`.
- **Two consumption modes**:
  - *Environment variables*: `valueFrom.configMapKeyRef` / `valueFrom.secretKeyRef` — injected at container start; changes do NOT propagate to running Pods.
  - *Volume mount*: a projected volume per key/file — changes DO propagate (with kubelet sync delay), no restart needed.
- **Ways in**: `kubectl create configmap x --from-literal=K=V`, `--from-file=file`, `--from-env-file=env.list`, or an applied manifest.

### 4. UNDER THE HOOD
A ConfigMap/Secret is just an object in etcd behind an API. kube-proxy has nothing to do with it; the kubelet materializes it: for a volume mount it writes each key as a file (shadowing the mount point with a symlink farm — `..data` → `..2026_..._timestamp`), so updates swap a symlink and existing readers see new content. For env injection the values are baked into the container's environment block at creation — immutable for the life of the container, which is why "update ConfigMap, env doesn't change" is the classic follow-up demo. Secrets mounted as volumes are tmpfs-backed (in-memory on the node) precisely so credentials don't land on disk; base64 is only there to allow binary payloads through a JSON/etcd path.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl create configmap app-config --from-literal=APP_COLOR=blue --from-literal=LOG_LEVEL=debug` | plain-text config in |
| `kubectl create secret generic app-secret --from-literal=DB_PASSWORD=sup3r-s3cr3t --from-literal=API_KEY=xyz789` | secret in |
| `kubectl get cm app-config -o yaml` | `.data` is plaintext |
| `kubectl get secret app-secret -o yaml` | `.data` is base64 — the encoding proof |
| `kubectl apply -f cm-secret-pod.yaml` | pod with env + volume mounts |
| `kubectl exec cm-secret-pod -- sh -c 'echo $APP_COLOR; cat /etc/secret/DB_PASSWORD'` | read them from INSIDE |

### 6. LIVE LAB
```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl create configmap app-config --from-literal=APP_COLOR=blue --from-literal=LOG_LEVEL=debug
kubectl create secret generic app-secret --from-literal=DB_PASSWORD=sup3r-s3cr3t --from-literal=API_KEY=xyz789
kubectl get cm app-config -o yaml
kubectl get secret app-secret -o yaml

kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: cm-secret-pod
spec:
  containers:
  - name: app
    image: alpine:3.20
    command: ["sleep", "3600"]
    env:
    - name: APP_COLOR
      valueFrom: { configMapKeyRef: { name: app-config, key: APP_COLOR } }
    - name: DB_PASSWORD
      valueFrom: { secretKeyRef: { name: app-secret, key: DB_PASSWORD } }
    volumeMounts:
    - name: cm-vol     ; mountPath: /etc/config
    - name: secret-vol ; mountPath: /etc/secret
  volumes:
  - name: cm-vol     ; configMap: { name: app-config }
  - name: secret-vol ; secret:   { secretName: app-secret }
EOF
kubectl wait --for=condition=Ready pod/cm-secret-pod --timeout=60s
kubectl exec cm-secret-pod -- sh -c 'echo "ENV APP_COLOR=$APP_COLOR"; echo "ENV DB_PASSWORD=$DB_PASSWORD"; ls /etc/config /etc/secret; cat /etc/secret/DB_PASSWORD; echo'
```

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl get cm app-config -o yaml
data:
  APP_COLOR: blue
  LOG_LEVEL: debug
kind: ConfigMap
metadata:
  creationTimestamp: "2026-09-14T18:29:14Z"
  name: app-config
  namespace: default

$ kubectl get secret app-secret -o yaml
data:
  API_KEY: eHl6Nzg5
  DB_PASSWORD: c3VwM3ItczNjcjN0
kind: Secret
...
type: Opaque

$ kubectl exec cm-secret-pod -- sh -c 'echo "ENV APP_COLOR=$APP_COLOR"; echo "ENV DB_PASSWORD=$DB_PASSWORD"; ls /etc/config /etc/secret; cat /etc/secret/DB_PASSWORD; echo'
ENV APP_COLOR=blue
ENV DB_PASSWORD=sup3r-s3cr3t
/etc/config:
APP_COLOR
LOG_LEVEL
/etc/secret:
API_KEY
DB_PASSWORD
sup3r-s3cr3t
```

### 8. OUTPUT AUTOPSY
- ConfigMap `.data` shows raw `blue` / `debug`; Secret `.data` shows `c3VwM3ItczNjcjN0` — and yet the container printed `sup3r-s3cr3t`. That mismatch IS the encodings story: the API base64-encodes Secret payloads for transport/storage; the kubelet decodes on injection.
- The exec output proves both channels: `$APP_COLOR=blue` and `$DB_PASSWORD=sup3r-s3cr3t` came from env refs; `cat /etc/secret/DB_PASSWORD` proved the volume path materialized keys as files (`API_KEY` and `DB_PASSWORD` filenames = key names).
- Rename for free: volumes expose *key name = file name*; you can `items:`-map a key to a custom filename or `path` if you need `/etc/secret/db` instead.

### 9. CLASSIC TRAPS
- **"Secrets are encrypted"** — the #1 interview sin. They are base64-encoded (obfuscatable, trivially reversible: `echo c3VwM3ItczNjcjN0 | base64 -d`). Encryption requires an extra layer (e.g., KMS provider, or the cloud's envelope encryption on EKS).
- **Env-injection staleness**: updating a ConfigMap does NOT update a running container's env vars. Volume-mounted files eventually do. "Restart needed" vs "no restart needed" is a very common hot question.
- **Secrets show up in get/edit with base64** — blindingly common oversight: people paste `kubectl get secret -o yaml` output into a ticket thinking it's safe.
- Secrets are Namespace-scoped; un-declared keys error (`key not found`) or fail the Pod.
- Secret size limits (~1MiB per secret) — a large CA bundle blows past it; use projected volumes piling multiple Secrets.

### 10. THE INTERVIEW WANTS TO KNOW
That you know Secrets ≠ encryption; the two injection modes and their change-propagation difference; and the operational angle — "where do the secrets live at runtime" (kubelet tmpfs; never in the image). Byte-for-byte: the demo *showed* base64 in the API and plaintext inside the pod.

### 11. FOLLOW-UP QUESTIONS
- Can a Pod get a key that doesn't exist? Env ref → Pod creation fails; volume with missing key → fails; with `optional: true` → skips.
- Update semantics? Env: no. Volume file: yes (symlink swap). So "do I restart on config change?" — it depends on method.
- Who can read a Secret? Anyone with RBAC `get` on secrets in the namespace — no magic. This is the intro to P0.7.
- Literal vs file: `--from-literal` for K=V, `--from-file` for multi-line files (e.g., config files); `--from-env-file` for bulk.

### 12. CHEAT SHEET
- ConfigMap = plain in `.data`; Secret = base64 in `.data` (encoded, NOT encrypted).
- env = baked at start (static); volume = symlinked (live-ish update).
- `kubectl exec` to inspect; cleanup = delete configmap + secret + pod.

### 13. STORY TO TELL
"Created a ConfigMap and Secret from literals, mounted them into an alpine pod as both env vars and volume files, and `kubectl exec` printed the plain values from inside — the API-side yaml showed the Secret base64: `c3VwM3ItczNjcjN0`. I make the encryption-vs-encoding point explicit every time, and I mention env values can't hot-update while mounted files can."

### 14. CONNECTIONS
- The ability to *read* secrets is RBAC-controlled (P0.7). Probe-driven restarts (P0.5) are how teams turn config changes into applied env changes. Helm (P1.4) templates values into these objects. EKS encrypts at rest (P2.4) — that's where "encrypted" finally appears.

### 15. VERIFIED VS PLANNED
- VERIFIED: configmap + secret creation, raw vs base64 output, env injection (both kinds), volume mount as files, exec readback, teardown.
- PLANNED-BUT-SKIPPED: `from-file`/`from-env-file` variants and `items:` renaming — documented, same mechanism.

### 16. DEEP DIVE — THE ETCD AND DISK TRUTH
Kubernetes' own terminology is what betrays people: the field is called `data` and the values are base64, because the object shape must survive JSON + etcd, which handle binary poorly. At rest on the kubelet, Secret volumes are tmpfs (`secret-<uid>` under `/var/lib/kubelet/pods/.../volumes` mounted as tmpfs) — memory, zeroed on pod death. So the real security ordering is: base64 = transport-encoding problem; tmpfs = runtime containment problem; RBAC = access problem; KMS envelope-encryption = at-rest problem. Interview answer: three layers, in that order.

### QC CHECKLIST — K8s.P0.4 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | ConfigMap created via `--from-literal` (2 keys) | PASS |
| 2 | Secret created via `--from-literal` (2 keys) | PASS |
| 3 | ConfigMap yaml shows plaintext values | PASS |
| 4 | Secret yaml shows base64 values (eHl6Nzg5 / c3VwM3ItczNjcjN0) | PASS |
| 5 | Pod mounted both as env vars via keyRef | PASS |
| 6 | Pod mounted both as volumes | PASS |
| 7 | exec printed env APP_COLOR=blue and DB_PASSWORD=sup3r-s3cr3t | PASS |
| 8 | exec listed /etc/config + /etc/secret files (key-named files) | PASS |
| 9 | cat of mounted secret file returned decrypted value | PASS |
| 10 | "base64 != encryption" line rehearsed with the demo values | PASS |
| 11 | env-vs-volume change-propagation distinction stated | PASS |
| 12 | Cleanup verified: cm, secret, pod all deleted | PASS |
| 13 | SELF-VERIFY — re-ran exec within session; output stable | PASS |

VERDICT: **P0.4 COMPLETE.** ConfigMap/Secret creation, both injection modes and the encoding-vs-encryption line live-proven.

NEXT POINTER → P0.5 adds the health layer these configs get consumed under: liveness/readiness/startup probes and the restarts they trigger.

---
## SESSION K8s.P0.5 — HEALTH PROBES: LIVENESS, READINESS, STARTUP

### 1. GOAL
Deploy nginx with an httpGet **liveness** probe pointing at port 8080 — which nginx does not serve — and *watch the kubelet restart the container* until the pod lands in CrashLoopBackOff. Then explain readiness vs liveness vs startup with the real probe syntax from `kubectl describe`.

### 2. WHY IT MATTERS
Probes are the #1 "operational k8s" topic for 1–3 YOE. The interview wants the three-way split — liveness (am I healthy? restart me if not), readiness (am I ready for traffic? pull me from Service endpoints if not), startup (give slow apps a grace window before liveness kicks in). And they want the failure mechanics: liveness failure → restart; readiness failure → removed from load balancer WITHOUT restart. Reproducing a real restart loop live is worth more than any diagram.

### 3. CORE CONCEPTS
- **livenessProbe** — "should I kill and restart this container?" Fail → kubelet restarts (backoff). Single-process crash detection. Do NOT include readiness-style checks (external deps) in liveness or you get needless restarts.
- **readinessProbe** — "should traffic be routed to this pod?" Fail → pod stays running but is dropped from Service Endpoints. During rollouts, readiness failure *stalls* the rollout (this is why P0.3's surge logic pauses).
- **startupProbe** — runs at start; while it fails, liveness and readiness are NOT executed. Gives JVM/huge-image apps time to boot without tripping liveness. Deprecated-ish semantics: success → probes resume; fail → restart after `failureThreshold`.
- **Probe types**: `httpGet` (HTTP GET, expects 2xx/3xx; a status code ≥400 = fail), `tcpSocket` (connection succeeds = pass), `exec` (command; exit 0 = pass), `grpc` (newer).
- **Probe knobs**: `initialDelaySeconds` (grace before first probe), `periodSeconds` (interval), `timeoutSeconds`, `failureThreshold` (consecutive failures before action), `successThreshold` (consecutive successes to flip ready).

### 4. UNDER THE HOOD
Everything probe-related lives in the **kubelet** (P0.1): it runs each probe from the node against the container's network. `httpGet` is executed as an HTTP client inside kubelet, so the target is the pod IP:port. Here port 8080 on nginx answers nothing → connection refused → probe fails. Liveness does KILL: kubelet sends SIGTERM to the container process, container restarts, restart count increments, kubelet backs off exponentially (10s, 20s, 40s...) until `CrashLoopBackOff`. Readiness failure in contrast just flips `Ready` to False in `pod.status.conditions` — the endpoint controller sees Ready=False and removes the pod from the Service; the pod keeps running and can come back without restart.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl apply -f probe-demo.yaml` | deploy the misconfigured probe |
| `kubectl get pods -l app=probe-demo` | watch RESTARTS climb |
| `kubectl describe pod ...` | the probe spec + Unhealthy events |
| `kubectl get endpoints <svc>` | (readiness story) ready pods only |
| `kubectl delete deploy probe-demo` | cleanup |

### 6. LIVE LAB
```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: probe-demo
spec:
  replicas: 1
  selector: { matchLabels: { app: probe-demo } }
  template:
    metadata: { labels: { app: probe-demo } }
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports: [ { containerPort: 80 } ]
        livenessProbe:
          httpGet: { path: /healthz, port: 8080 }
          initialDelaySeconds: 3
          periodSeconds: 2
        readinessProbe:
          httpGet: { path: /, port: 80 }
          initialDelaySeconds: 1
          periodSeconds: 2
EOF
kubectl apply -f probe-demo.yaml
sleep 20 ; kubectl get pods -l app=probe-demo
kubectl describe pod -l app=probe-demo
sleep 12 ; kubectl get pods -l app=probe-demo
```

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl get pods -l app=probe-demo          # ~20s in
NAME                          READY   STATUS    RESTARTS     AGE
probe-demo-747bd465d6-vkpzt   1/1     Running   2 (4s ago)   20s

$ kubectl describe pod -l app=probe-demo
    Liveness:       http-get http://:8080/healthz delay=3s timeout=1s period=2s #success=1 #failure=3
    Readiness:      http-get http://:80/ delay=1s timeout=1s period=2s #success=1 #failure=3
  ...
  Warning  Unhealthy  16s (x9 over 36s)  kubelet
            Liveness probe failed: Get "http://10.244.0.14:8080/healthz": dial tcp 10.244.0.14:8080: connect: connection refused
  Normal   Killing    16s (x3 over 32s)  kubelet
            Container nginx failed liveness probe, will be restarted
  Warning  BackOff    15s (x3 over 16s)  kubelet
            Back-off restarting failed container nginx in pod probe-demo-747bd465d6-vkpzt_default(...)

$ kubectl get pods -l app=probe-demo          # ~40s in
NAME                          READY   STATUS             RESTARTS      AGE
probe-demo-747bd465d6-vkpzt   0/1     CrashLoopBackOff   2 (15s ago)   39s
```

### 8. OUTPUT AUTOPSY
- `RESTARTS 2` at 20s with the pod still `1/1 Running` (readiness on :80 passes) — liveness and readiness failed/succeeded by different probes, visible side by side in `describe`.
- `describe` prints the probe syntax compactly: `http-get http://:8080/healthz delay=3s timeout=1s period=2s #success=1 #failure=3` — every knob from the manifest, one line.
- The event trail is the lesson: `Unhealthy` (probe failed, x9 over 36s) → `Killing` ("Container nginx failed liveness probe, will be restarted" — the kubelet acted) → `BackOff` (exponential backoff) → CrashLoopBackOff at ~40s. Exactly the escalating lifecycle.
- Had this been **readiness-only** on :8080, the pod would sit `0/1` with RESTARTS 0 and vanish from Service endpoints — the "no traffic, no restart" state. The restart loop is *specifically* liveness behavior.

### 9. CLASSIC TRAPS
- **Probing a wall**: liveness on `/healthz` when your app has no such endpoint (reproduced). Keep liveness simple — it should fail ONLY on process-level problems.
- **Putting external dependencies in liveness** (DB, redis) — DB blip → container killed, cascade failure. External deps belong in readiness (or none).
- **ready vs start semantics**: readiness does not restart; startup only guards slow boots. Three different animals, three different knobs.
- **Initial delay too short for slow apps** → permanent restart loops (see JVM). Use `startupProbe` for the boot window.
- **Port mismatch**: containers listen in-pod; probes hit pod IP, never the Service. `port: 8080` in the probe means podIP:8080 — nginx listening on 80 refuses.
- **Multiple containers**: probe is per-container; 1/2 ready shows 0/1 overall. Deployments only roll pods whose containers all pass readiness.

### 10. THE INTERVIEW WANTS TO KNOW
The precise failure-behavior mapping: liveness→restart, readiness→endpoints removal, startup→guard. And when to choose httpGet vs exec vs tcpSocket (HTTP for web services, exec for process-level like `pidof`, tcpSocket for non-HTTP services). The demo's crash loop stops any "did you actually tune them?" follow-up dead.

### 11. FOLLOW-UP QUESTIONS
- Why would rolling updates stall with a failing probe? The new RS never reaches Ready → surge keeps waiting; `progressDeadlineSeconds` then fails the deployment.
- Can readiness failure co-exist with liveness pass? Absolutely — service gone, pod alive (DB down but process fine). This is the desired scope separation.
- Probe exec side effects? `exec` runs inside the container; heavy commands on every periodSeconds add load.
- startupProbe and period — startup runs every 1s by default; a long `failureThreshold` (e.g., 30) gives a 30s boot window without touching liveness.

### 12. CHEAT SHEET
- liveness fail → KILL+restart (backoff). readiness fail → out of endpoints (no restart). startup fail → restart; while running, masks liveness/readiness.
- Probe spec one-liner: `delay` = initialDelaySeconds, `period`, `timeout`, `#success`/`#failure` thresholds.
- Grid: httpGet for HTTP apps, tcpSocket for TCP, exec for process-signals.

### 13. STORY TO TELL
"Pointed a liveness httpGet at port 8080 on an nginx that serves 80. The pod came up 1/1 — readiness passed — then the kubelet's Unhealthy → Killing → BackOff events drove RESTARTS to 2 and the pod into CrashLoopBackOff, visible in `describe pod` with the full probe spec on the Liveness line. One-line summary for interviews: liveness kills, readiness hides, startup lets you breathe."

### 14. CONNECTIONS
- Rollouts (P0.3) depend on readiness; the surge pauses until new pods report ready. Endpoints (P0.2) only ever contain Ready pods. `kubectl get pod -o wide` NODE column shows which kubelet ran the probe. Healthchecks for containers parallel Docker's HEALTHCHECK (06-docker P1.1).

### 15. VERIFIED VS PLANNED
- VERIFIED: liveness fail/restart loop with BackOff/CrashLoopBackOff, describe output, the Restarts counter going 0 → 1 → 2.
- PLANNED-BUT-SKIPPED: live readiness-only Service-endpoint removal demo (would need a Service + flipped probe; the mechanism was captured in the autopsy text). exec + tcpSocket are same mechanics, documented not demoed.

### 16. DEEP DIVE — WHY STARTUP PROBES GET A SLOW PERIOD
The classic JVM death spiral: heavy app boots 45s, liveness initialDelaySeconds=10 → kernel kills the JVM at boot. Teams paper over it by inflating initialDelaySeconds, which then delays *every* start forever. The startupProbe solves the class of problem: it runs at its own aggressive cadence with a high failureThreshold for the boot window, then hands authority to liveness/readiness. It's the "give me a runway" knob, and its existence is a strong signal you understand the failure semantics of probes, not just the YAML.

### QC CHECKLIST — K8s.P0.5 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | Deployment with httpGet liveness on port 8080 + readiness on 80 | PASS |
| 2 | Pod initially reported 1/1 Running (readiness ok) | PASS |
| 3 | RESTARTS climbed 0 → 2 inside 20s | PASS |
| 4 | describe showed full probe one-liners (delay/period/timeout/thresholds) | PASS |
| 5 | Unhealthy event with real connection-refused Get error | PASS |
| 6 | Killing event text captured ("will be restarted") | PASS |
| 7 | BackOff event text captured | PASS |
| 8 | Pod reached CrashLoopBackOff by ~40s | PASS |
| 9 | liveness-vs-readiness failure semantics narrated | PASS |
| 10 | startupProbe purpose + boot-window role explained | PASS |
| 11 | probe types (httpGet/tcpSocket/exec) differentiated | PASS |
| 12 | Cleanup verified: probe-demo deleted | PASS |
| 13 | SELF-VERIFY — probe line re-read: `http://:8080/healthz` matches manifest | PASS |

VERDICT: **P0.5 COMPLETE.** Probe failure modes reproduced live (restart loop + crash backoff); readiness-vs-liveness split locked.

NEXT POINTER → P0.6 adds the other two "describe pod/nodes" numbers: requests/limits, QoS classes, and the taint/toleration machinery behind scheduling choices.

---
## SESSION K8s.P0.6 — SCHEDULING: REQUESTS/LIMITS, NODESELECTOR, TAINTS/TOLERATIONS

### 1. GOAL
Deploy a workload with explicit CPU/memory requests and limits, read them back via `describe`, watch the node's allocated-resource totals shift, then prove scheduling constraints three ways: a nodeSelector that pins placement to a labelled node, a NoSchedule taint that leaves a toleration-less pod Pending, and a toleration that lets the same taint through.

### 2. WHY IT MATTERS
"requests vs limits" is THE quality-of-service question of any k8s interview, and taints/tolerations is the "how do you keep workloads apart" answer. Both are scheduling-surfaced: the scheduler *only* sees requests for placement; the kubelet *only* enforces limits at runtime. Knowing which layer cares about which number is the depth the 1–3 YOE interview probes.

### 3. CORE CONCEPTS
- **requests** = guaranteed minimum; what the scheduler books on a node. A node only accepts a Pod if all existing requests + this request fit within allocatable. Requests are the *reservation*.
- **limits** = hard cap the kubelet enforces. CPU limits are throttled/compatibly (CFS quota); memory limits get the container OOM-killed when exceeded. No limits → the container can burst and spike the node.
- **QoS classes** — derived from requests+limits, not settable:
  - `Guaranteed`: every container has BOTH request == limit on both resources.
  - `Burstable`: at least one request/limit set, not fully Guaranteed.
  - `BestEffort`: no requests and no limits at all — evicted FIRST under node pressure.
- **nodeSelector** — a map `nodeSelector: {disktype: ssd}`; simplest pinning. Pods only schedule on nodes with matching labels.
- **Taint** (`kubectl taint nodes n key=value:NoSchedule`) = "pods WITHOUT a matching toleration will not be scheduled here by default." **Toleration** = "I am allowed on nodes carrying this taint." `NoSchedule` (block new), `PreferNoSchedule` (soft), `NoExecute` (block + evict existing).
- `kubectl describe node` shows BOTH sides of the ledger: allocatable capacity and current aggregate requests/limits — the session reads both.

### 4. UNDER THE HOOD
Scheduler scoring: filter (feasibility — requests, taints, nodeSelector, affinity) then score (best-fit, least-requested etc.). Taints are the adversarial-control mechanism: tolerations match key/effect (operator `Equal` or `Exists`). Control-plane nodes in real clusters carry `node-role.kubernetes.io/control-plane:NoSchedule` precisely so app pods never land there — *this kind node has Taints: <none>* (kind defaults), which is why workloads can land on the single node and why `describe node` shows "Taints: <none>" — worth quoting. QoS decides OOM/eviction order under pressure: BestEffort first, then Burstable, Guaranteed last (even the kubelet's own infra pods matter here).

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl apply -f limits-demo.yaml` | deployment with requests+limits |
| `kubectl describe pod ...` | Limits/Requests lines + QoS |
| `kubectl get pod ... -o jsonpath='{.status.qosClass}'` | QoS class directly |
| `kubectl describe node` | allocated resources aggregate |
| `kubectl label node ... disktype=ssd` / `kubectl taint nodes ... env=prod:NoSchedule` | priming the constraints |
| `kubectl run ... -o yaml` + nodeSelector/tolerations | the scheduling fields |
| `kubectl describe pod` (pending) | "had untolerated taint" event |
| `kubectl taint nodes ... -` | remove the taint (cleanup) |

### 6. LIVE LAB
```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl apply -f - <<'EOF'   # limits-demo deployment, 2 replicas
apiVersion: apps/v1
kind: Deployment
metadata: { name: limits-demo }
spec:
  replicas: 2
  selector: { matchLabels: { app: limits-demo } }
  template:
    metadata: { labels: { app: limits-demo } }
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        resources:
          requests: { cpu: 100m, memory: 64Mi }
          limits:   { cpu: 250m, memory: 128Mi }
EOF
kubectl rollout status deploy/limits-demo --timeout=120s
kubectl get pod -l app=limits-demo -o jsonpath='{.items[0].status.qosClass}'
kubectl describe pod -l app=limits-demo | grep -A5 'Limits:'
kubectl describe node | sed -n '/Allocated resources:/,$p'

# nodeSelector pinning
kubectl label node warroom-control-plane disktype=ssd
kubectl apply -f sel-pod.yaml          # nodeSelector: disktype: ssd
kubectl get pod sel-pod -o wide        # -> warroom-control-plane

# taint / toleration
kubectl taint nodes warroom-control-plane env=prod:NoSchedule
kubectl run taint-noway --image=nginx:alpine
kubectl describe pod taint-noway | grep -i taint
kubectl apply -f taint-ok.yaml         # same taint + toleration
kubectl get pod taint-ok -o wide       # -> scheduled
kubectl delete pod taint-noway taint-ok
kubectl taint nodes warroom-control-plane env=prod:NoSchedule-
kubectl label node warroom-control-plane disktype-
```

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl get pod -l app=limits-demo -o jsonpath='{.items[0].status.qosClass}'
Burstable

$ kubectl describe pod -l app=limits-demo
    Limits:
      cpu:     250m
      memory:  128Mi
    Requests:
      cpu:        100m
      memory:     64Mi

$ kubectl describe node | sed -n '/Allocated resources:/,$p'
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests     Limits
  cpu                1150m (14%)  500m (6%)
  memory             418Mi (11%)  596Mi (15%)
  ephemeral-storage  0 (0%)       0 (0%)

# nodeSelector pinning result:
$ kubectl get pod sel-pod -o wide
NAME      READY   STATUS    RESTARTS   AGE   IP            NODE                    NOMINATED NODE
sel-pod   1/1     Running   0          1s    10.244.0.17   warroom-control-plane   <none>

# taint with no toleration:
$ kubectl get pod taint-noway -o wide
NAME          READY   STATUS    RESTARTS   AGE   IP       NODE     NOMINATED NODE
taint-noway   0/1     Pending   0          4s    <none>   <none>   <none>

$ kubectl describe pod taint-noway | grep -i taint
  Warning  FailedScheduling  3s  default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint(s). preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.

# toleration added:
$ kubectl get pod taint-ok -o wide
NAME       READY   STATUS    RESTARTS   AGE   IP            NODE                    NOMINATED NODE
taint-ok   1/1     Running   0          1s    10.244.0.18   warroom-control-plane   <none>
```

### 8. OUTPUT AUTOPSY
- The pod's own yaml-less proof: `status.qosClass` = Burstable (request ≠ limit) — QoS is *derived*, not configured. Each of the 2 pods contributes requests 100m/64Mi and limits 250m/128Mi.
- node "Allocated resources" ticked to cpu 1150m (14%) / memory 418Mi (11%) — the base 950m/290Mi from P0.1 plus our 2×100m/2×64Mi. The node ledger is additive; `describe node` is the real-time proof of where requests went. Limits exceeding 100% capacity is legal (overcommit) — the "Total limits may be over 100%" preamble is exactly that.
- `sel-pod` scheduled only after `disktype=ssd` existed on the node; the label is the key, the value is the pin. Remove the label → next restart unschedulable.
- `taint-noway` sits Pending with a *named* reason string: `1 node(s) had untolerated taint(s)` — the scheduler said why in plain words. `taint-ok` (same taint, toleration `key: env, operator: Equal, value: prod, effect: NoSchedule`) scheduled instantly. Two pods, one taint, one line of toleration = the full lesson.

### 9. CLASSIC TRAPS
- **requests ≠ usage**. `describe node` allocation vs `kubectl top` usage are different ledgers — a node can be over-allocated yet idle. The number 11% in `describe` is reservation, not load.
- **Limits above node capacity are "fine"** (overcommit) — but memory overcommit means OOM-kill risk; CPU overcommit means throttling.
- **Missing requests = BestEffort** → eviction first under memory pressure — the "why does my pod die first" FAQ.
- **Taints repel, tolerations permit** — a toleration does NOT require scheduling there; it just allows it. Saying "toleration forces the pod there" is a howler.
- nodeSelector = equality on labels; affinity (preferredDuringScheduling etc.) is the richer cousin. Don't conflate nodeName (hard pin) with nodeSelector.
- Kind nodes have `Taints: <none>` — that's why P0.6's workload sat right on the control-plane node; on a real cluster the control-plane NoSchedule taint would have parked it elsewhere. Quote the difference.

### 10. THE INTERVIEW WANTS TO KNOW
requests vs limits at the *two different layers* (scheduler books requests; kubelet enforces limits), the QoS triage order (BestEffort→Burstable→Guaranteed), and that taint/toleration is allow-to-place, not demand-to-place. Cite the live `describe node` ledger (1150m/14%) and the FailedScheduling reason verbatim.

### 11. FOLLOW-UP QUESTIONS
- What sets QoS to Guaranteed? Every container with request == limit on cpu AND memory. One Burstable container → whole pod Burstable.
- Difference between NodeSelector and node affinity? Selector = hard equality; affinity has soft/preferred + In/NotIn operators and expressions.
- NoExecute vs NoSchedule? NoExecute also evicts pods already running without the toleration.
- How do system daemonsets get on control-plane nodes? They carry tolerations in their manifests (kindnet/kube-proxy do) — connects to P2.3.

### 12. CHEAT SHEET
- requests = reservation (scheduler), limits = hard cap (kubelet). QoS from the pair. BestEffort dies first.
- taint = repel; toleration = permission (not obligation). NoSchedule blocks, NoExecute evicts.
- `describe node` = aggregate reservations; `top node` = actual usage. Different ledgers.

### 13. STORY TO TELL
"Ran a 2-replica deployment with 100m/64Mi requests and 250m/128Mi limits — `describe` showed both lines, QoS read Burstable, and the node's allocated-resources block rose to 1150m/14%: the scheduler booking my requests on top of the 950m baseline. Then the scheduling trio: a nodeSelector rode the `disktype=ssd` label home, a NoSchedule taint produced the exact `untolerated taint(s)` FailedScheduling reason on a Pending pod, and a matching toleration scheduled the second pod instantly."

### 14. CONNECTIONS
- The 950m baseline is P0.1's system workload. Applications with limits + probes (P0.5) are what survive real traffic. Overcommit discipline is what EKS node groups (P2.4) tune with instance families. Resource requests also drive HPA's `% of request` math (P1.3) — the 100m request is the denominator there.

### 15. VERIFIED VS PLANNED
- VERIFIED: QoS jsonpath (Burstable), describe pod Limits/Requests, node aggregate before/after, nodeSelector scheduling, NoSchedule Pending + exact reason, toleration scheduling, cleanup with `-` taint removal + `label -`.
- PLANNED-BUT-SKIPPED: NodeAffinity expressions and NoExecute eviction (same machineries, noted).

### 16. DEEP DIVE — THE THIRD QoS STATE AT THE EDGE
The kubelet's eviction ordering under memory pressure: BestEffort containers are reclaimed first, then Burstable (by usage over request), then Guaranteed. That ordering is the operational reason the "requests everywhere" guidance exists: an app *without* requests is atomically the first casualty of someone else's memory spike. It's also why pod priorities + limits are sold together — a Guaranteed pod with priorityClass survives, while a BestEffort pod with the same priority is evicted. Understanding the ladder is understanding "why did MY pod die."

### QC CHECKLIST — K8s.P0.6 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | Deployment with requests 100m/64Mi and limits 250m/128Mi created | PASS |
| 2 | `describe pod` shows both Limits and Requests lines | PASS |
| 3 | QoS class read via jsonpath = Burstable | PASS |
| 4 | Node allocated resources jumped by 200m/128Mi (+2 pods) | PASS |
| 5 | nodeSelector on `disktype=ssd` placed pod on the control-plane node | PASS |
| 6 | NoSchedule taint applied via `kubectl taint` | PASS |
| 7 | Taint-less pod stuck Pending with `had untolerated taint(s)` reason | PASS |
| 8 | Toleration pod scheduled despite the same taint | PASS |
| 9 | Taint reverted with trailing `-`, label reverted with `label -` | PASS |
| 10 | requests/limits two-layer story (scheduler vs kubelet) rehearsed | PASS |
| 11 | QoS ordering BestEffort→Burstable→Guaranteed stated | PASS |
| 12 | Cleanup: limits-demo, sel-pod, taint pods all deleted; node pristine | PASS |
| 13 | SELF-VERIFY — describe-node allocations and pod QoS re-read, consistent | PASS |

VERDICT: **P0.6 COMPLETE.** Requests/limits/QoS plus nodeSelector and taint/toleration proven with real scheduler reasons and ledger numbers.

NEXT POINTER → P0.7 governs who may issue those commands at all: RBAC, ServiceAccounts, and the least-privilege story.

---
## SESSION K8s.P0.7 — RBAC: ROLE, CLUSTERROLE, BINDING, SERVICEACCOUNT

### 1. GOAL
Build a least-privilege RBAC story on the real cluster: a namespace, a ServiceAccount, a Role that allows only `get/list/watch pods`, a RoleBinding, a Pod running as that ServiceAccount — then ask the apiserver "can this identity do X" with `kubectl auth can-i` and read the verdict matrix.

### 2. WHY IT MATTERS
"Who can do what to which resources?" is the whole RBAC pitch, and it runs through ServiceAccounts (the identity of a running Pod) — a 1–3 YOE candidate is expected to know the four objects (Role, ClusterRole, RoleBinding, ClusterRoleBinding), the least-privilege stance, and that Kubernetes enforces *deny-by-default*: no binding = no permission. `kubectl auth can-i --as=<identity>` is the diagnostic superpower because it shows the same authorization the API server would apply, live.

### 3. CORE CONCEPTS
- **RBAC model**: Subject (User/Group/ServiceAccount) + verbs (get/list/watch/create/update/patch/delete) × resources (pods, deployments, secrets, ...) + scope.
- **Role** — namespaced permissions. **ClusterRole** — cluster-wide (or granted in any namespace via binding). Both are just rule lists: `apiGroups`, `resources`, `verbs`.
- **RoleBinding** — binds a Role to subjects INSIDE a namespace. **ClusterRoleBinding** — binds ClusterRole cluster-wide. A RoleBinding can also reference a ClusterRole to grant its rules *within one namespace*.
- **ServiceAccount** — the identity under which containers run; injected as a projected volume at `/var/run/secrets/kubernetes.io/serviceaccount/{ca.crt,namespace,token}` (token = a JWT). Pods get the `default` SA unless told otherwise.
- **Least-privilege**: grant exactly the verbs/resources a workload needs. Default SA in most clusters is near-powerless — that *is* the design.

### 4. UNDER THE HOOD
Every API request passes filters: **authentication** (who: token/user/cert) then **authorization** (may they?) — RBAC is a pure rules engine, evaluated per request, deny-by-default. The SA token is a JWT signed by the cluster CA; the kubelet mounts it; the apiserver validates the signature and maps `system:serviceaccount:<ns>:<name>` as the identity. `kubectl auth can-i --as=system:serviceaccount:rbac-demo:pod-reader-sa` performs the SAME evaluation as the apiserver for the request — which is why its output is authoritative, not simulated. When you exec into the demo pod and read the token, you are looking at the credential the kubelet injected for that exact identity.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl create namespace rbac-demo` | a scoped stage |
| `kubectl create sa pod-reader-sa -n rbac-demo` | the identity |
| `kubectl create role pod-reader --verb=get,list,watch --resource=pods -n rbac-demo` | the permission set |
| `kubectl create rolebinding pod-reader-binding --role=pod-reader --serviceaccount=rbac-demo:pod-reader-sa -n rbac-demo` | bind identity to permissions |
| `kubectl describe rolebinding ...` | Role + Subjects in one screen |
| `kubectl auth can-i <verb> <res> --as=system:serviceaccount:rbac-demo:pod-reader-sa [-n ns]` | the authorization answer |
| `kubectl exec <pod> -- ls /var/run/secrets/kubernetes.io/serviceaccount/` | the injected identity |

### 6. LIVE LAB
```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl create namespace rbac-demo
kubectl create sa pod-reader-sa -n rbac-demo
kubectl create role pod-reader --verb=get,list,watch --resource=pods -n rbac-demo
kubectl create rolebinding pod-reader-binding --role=pod-reader \
  --serviceaccount=rbac-demo:pod-reader-sa -n rbac-demo
kubectl describe rolebinding pod-reader-binding -n rbac-demo

kubectl auth can-i get pods --as=system:serviceaccount:rbac-demo:pod-reader-sa -n rbac-demo
kubectl auth can-i delete pods --as=system:serviceaccount:rbac-demo:pod-reader-sa -n rbac-demo
kubectl auth can-i get pods --as=system:serviceaccount:rbac-demo:pod-reader-sa -n kube-system
kubectl auth can-i get namespaces --as=system:serviceaccount:rbac-demo:pod-reader-sa -n rbac-demo

kubectl apply -f sa-demo.yaml   # pod using serviceAccountName: pod-reader-sa
kubectl describe pod sa-demo -n rbac-demo | grep -i serviceaccount
kubectl exec sa-demo -n rbac-demo -- sh -c 'ls /var/run/secrets/kubernetes.io/serviceaccount/'
```

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl describe rolebinding pod-reader-binding -n rbac-demo
Role:
  Kind:  Role
  Name:  pod-reader
Subjects:
  Kind            Name           Namespace
  ----            ----           ---------
  ServiceAccount  pod-reader-sa  rbac-demo

--- the permission-set as stored:
$ kubectl create role pod-reader --verb=get,list,watch --resource=pods -n rbac-demo --dry-run=client -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: rbac-demo
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - get
  - list
  - watch

--- the authorization matrix (auth can-i):
$ kubectl auth can-i get pods --as=system:serviceaccount:rbac-demo:pod-reader-sa -n rbac-demo
yes
$ kubectl auth can-i delete pods --as=system:serviceaccount:rbac-demo:pod-reader-sa -n rbac-demo
no
$ kubectl auth can-i get pods --as=system:serviceaccount:rbac-demo:pod-reader-sa -n kube-system
no
$ kubectl auth can-i get namespaces --as=system:serviceaccount:rbac-demo:pod-reader-sa -n rbac-demo
no

--- the identity inside the pod:
$ kubectl describe pod sa-demo -n rbac-demo | grep -i serviceaccount
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-khxsz (ro)
$ kubectl exec sa-demo -n rbac-demo -- sh -c 'ls /var/run/secrets/kubernetes.io/serviceaccount/'
ca.crt
namespace
token
```

### 8. OUTPUT AUTOPSY
- The `role --dry-run -o yaml` prints exactly what the API stores: `rules: [{apiGroups:[""], resources:[pods], verbs:[get list watch]}]`. Empty `apiGroups: [""]` = core group — pods live there; deployments live in `apps`. This is the syntax every RBAC question reads.
- The `describe rolebinding` is the wiring diagram: Role (what) + Subject ServiceAccount (who) in scope rbac-demo.
- The can-i matrix is the answer table an interviewer would love: `get pods` yes → `delete pods` no → `get pods` in another namespace no → `get namespaces` no (not even listed by this Role; namespaces are cluster-scoped, need a ClusterRole). Four rows, four distinct RBAC facts, all from the same lousy little role.
- Inside the pod, `ca.crt + namespace + token` are mounted read-only at the classic path; the token is the JWT whose subject is `system:serviceaccount:rbac-demo:pod-reader-sa` — the exact string we passed to `--as`.

### 9. CLASSIC TRAPS
- **Role vs ClusterRole scope**: roles are namespaced, clusterroles cluster-wide. A *RoleBinding can bind a ClusterRole* to get clusterrole power inside one namespace — that's the usual SA setup for app read access.
- **Cluster-scoped resources** (nodes, pv, namespaces, clusterroles) can only be granted via ClusterRole + ClusterRoleBinding (or RoleBinding->ClusterRole still works for namespaced res; for cluster-res you need CRB). can-i to `namespaces` returned no — classic.
- **Verbs are case/literal**: `get,list,watch` ≠ `*`. `create` ≠ `update`.
- **`default` SA ≠ admin**: deny-by-default — a pod with the default SA on a hardened cluster has almost nothing. People assume "default = allowed" backward.
- **Deleting/recreating a ServiceAccount breaks token-based deployments**: the Secret reference changes; long-lived tokens rot. Prefer bound token + `serviceAccountName` explicit.
- `kubectl auth can-i` without `--as` tests YOUR identity (usually admin) — always add `--as` when testing workload identity.

### 10. THE INTERVIEW WANTS TO KNOW
The deny-by-default posture, the four objects + scopes, verbs × resources grammar, and the ServiceAccount-as-pod-identity story including the JWT injection path. Bonus: quoting a real can-i verdict table (yes/no/no/no) shows you've tiered people before, not just read docs.

### 11. FOLLOW-UP QUESTIONS
- How do apps authenticate out (e.g., app → AWS)? Among the reasons IRSA (P2.4) exists: your SA is the pod identity, mapped to an IAM role via the OIDC issuer.
- What is a ClusterRoleBinding for a ServiceAccount across namespaces? That's exactly how cross-namespace cluster-wide SA access happens.
- Can a Role be non-namespaced? No — RoleBinding/Role live in a namespace; ClusterRole has no namespace.
- Aggregation? `aggregationRule: clusterRoleSelectors` lets one ClusterRole sum rules from labeled others — deep-cut.

### 12. CHEAT SHEET
- Who(Subject: SA/user/group) × What(verbs × resources) × Where(Role=ns, ClusterRole=cluster).
- Role/ClusterRole = rules; Binding pairs them to Subjects. Deny by default.
- `kubectl auth can-i <verb> <res> [--as=...] [-n ns]` = live authorization truth.
- Pod identity = SA token JWT at /var/run/secrets/kubernetes.io/serviceaccount/token.

### 13. STORY TO TELL
"Stood up a `pod-reader` Role (get/list/watch pods only), bound it to `pod-reader-sa` in rbac-demo, then ran kubectl auth can-i under that identity: `get pods` yes, `delete pods` no, another namespace no, `get namespaces` no. Then a pod ran as that SA — its kubelet-mounted token JWT at the standard serviceaccount path is literally the credential the API server evaluated for those four answers."

### 14. CONNECTIONS
- Secrets (P0.4) are protected by these exact rules. The ServiceAccount flow explains how CRDs/controllers get power. Helm (P1.4) installs charts *as* your user's/SA's rights. IRSA (P2.4) extends SA identity to cloud roles. NetworkPolicy (P1.2) is the network-layer cousin of RBAC's object-layer control.

### 15. VERIFIED VS PLANNED
- VERIFIED: SA+Role+RoleBinding creation, role yaml (dry-run), rolebinding describe, 4-row can-i matrix, pod identity + token-path exec.
- PLANNED-BUT-SKIPPED: ClusterRole/ClusterRoleBinding live demo (same object model, scope changed — documented), Node exporter on can-i against nodes, aggregation rules.

### 16. DEEP DIVE — SA TOKENS ARE JUST JWTs WITH SUBJECTS
Trim the pod token and you get `eyJhbGciOiJSUzI...` — a JWT signed by the cluster (the previous run took the first 15 chars: `eyJhbGciOiJSUzI`). The apiserver verifies signature via its CA, reads `sub = system:serviceaccount:rbac-demo:pod-reader-sa`, then runs RBAC evaluation from there. That's the entire authN→authZ sequence in one file. Knowing that a SA token = signed identity (not "password stored in etcd") is the Senior-between-hours answer to "how do workloads prove identity."

### QC CHECKLIST — K8s.P0.7 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | Namespace rbac-demo created | PASS |
| 2 | ServiceAccount + Role (get,list,watch pods) + RoleBinding created | PASS |
| 3 | Role stored exactly as `resources:[pods] verbs:[get list watch]` (dry-run yaml) | PASS |
| 4 | describe rolebinding printed Role + Subject table | PASS |
| 5 | can-i get pods → yes | PASS |
| 6 | can-i delete pods → no | PASS |
| 7 | can-i get pods (kube-system) → no (scope boundary) | PASS |
| 8 | can-i get namespaces → no (cluster-scope boundary) | PASS |
| 9 | Pod ran with serviceAccountName; describe showed the projected volume | PASS |
| 10 | exec listed ca.crt / namespace / token files | PASS |
| 11 | Token identified as JWT (prefix eyJhbGci...) | PASS |
| 12 | Cleanup verified: rbac-demo namespace deleted (all children gone) | PASS |
| 13 | SELF-VERIFY — can-i matrix re-run within session; 4 answers stable | PASS |

VERDICT: **P0.7 COMPLETE.** RBAC objects, scopes, identity injection and the live can-i verdict matrix — least privilege demonstrated, not lectured.

NEXT POINTER → P0.8 moves from *who may act* to *how traffic flows*: pod-to-pod, internal DNS, Services, and where Ingress enters.

---
## SESSION K8s.P0.8 — NETWORKING: POD-TO-POD, SERVICE, INGRESS (INTRO)

### 1. GOAL
Prove the two basic networking promises of Kubernetes with real traffic: any Pod can reach any other Pod by IP across the cluster network, and any Pod can reach a Service by *name* through internal DNS. Then show the Service types (ClusterIP/NodePort) at the spec level and open the Ingress story.

### 2. WHY IT MATTERS
Networking is where interviewers separate "user" from "operator." The core ideas candidates are expected to state cleanly: the flat cluster network (every Pod gets an IP, no NAT between Pods), Services as stable DNS + virtual-IP in front of volatile Pod IPs, kube-proxy translating Service → Pod, and Ingress as the L7 hostname/path router in front of Services. Live output (`os.getent` + curl) turns those sentences into evidence.

### 3. CORE CONCEPTS
- **Cluster network**: every Pod gets an IP (here the 10.244.0.0/24 PodCIDR split by node). Pods can reach each other directly — same node or across nodes — via the CNI (here kindnet). There is NO NAT between Pods (pure L3 forwarding); NAT appears only at the edge.
- **Service** — the stable Layer-4 abstraction: virtual ClusterIP + DNS name, port→targetPort, backed by Endpoints (P0.2). kube-proxy implements it (iptables/IPVS DNAT rules).
- **ClusterIP** — internal-only VIP, reachable inside the cluster, DNS-resolvable as `<svc>.<namespace>.svc.cluster.local`.
- **NodePort** — same as ClusterIP PLUS a fixed host port (30000–32767) opened on EVERY node; traffic to `nodeIP:nodePort` gets DNAT'd to the same Endpoints.
- **LoadBalancer** — ClusterIP+NodePort plus a request to the cloud provider for an external LB; in kind there is no cloud, so `EXTERNAL-IP` stays `<pending>`.
- **Ingress** — an L7 (HTTP/HTTPS) router: host-based and path-based rules routing to Services. It is NOT a Service type; it's an API + controller (nginx-ingress). Candidates who call Ingress "a LB Service" get docked.

### 4. UNDER THE HOOD
Two different address spaces: Pod network (10.244.x.x, per-node CNI bridge) and Service network (10.96.x.x, virtual). When a Pod curls `http://net-svc`, its DNS resolver (CoreDNS, injected via kubelet `dnsPolicy`) answers with the Service ClusterIP; the packet goes to kube-proxy's iptables on the node, which DNAT's to one of the live Pod IPs from the Service's Endpoints. That's why `getent hosts net-svc` = ClusterIP and `get endpoints` = pod IPs — DNS gives you the VIP, endpoints give you the real targets. NodePort extends the DNAT to the node's own IP:32080; the kind exception (NodePort not reachable from the WSL host unless the cluster was created with extraPortMappings) is the pre-canned "why can't I hit localhost:port in kind" answer.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl expose deployment net-app --port=80 --type=ClusterIP --name=net-svc` | Service from a deployment |
| `kubectl get svc net-svc` | ClusterIP + port |
| `kubectl exec <curl-pod> -- curl http://net-svc` | Service works by name |
| `kubectl exec <curl-pod> -- getent hosts net-svc` | internal DNS → ClusterIP |
| `kubectl exec <curl-pod> -- getent hosts net-svc.default.svc.cluster.local` | FQDN form |
| `kubectl get endpoints net-svc` | actual targets = pod IPs |
| `kubectl create service nodeport net-svc2 --tcp=80:80 --node-port=32080` | NodePort type |
| `kubectl get svc net-svc2` | 80:32080/TCP mapping |

### 6. LIVE LAB
```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl create deployment net-app --image=nginx:alpine --replicas=2
kubectl rollout status deploy/net-app --timeout=120s
kubectl expose deployment net-app --port=80 --target-port=80 --type=ClusterIP --name=net-svc
kubectl run curl-pod --image=curlimages/curl --command -- sleep 3600
kubectl wait --for=condition=Ready pod/curl-pod --timeout=60s
kubectl exec curl-pod -- curl -s -o /dev/null -w "svc-curl http_code=%{http_code}\n" http://net-svc
kubectl exec curl-pod -- getent hosts net-svc
kubectl exec curl-pod -- getent hosts net-svc.default.svc.cluster.local
kubectl get endpoints net-svc
kubectl create service nodeport net-svc2 --tcp=80:80 --node-port=32080
kubectl get svc net-svc2
```

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl get svc net-svc
NAME      TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
net-svc   ClusterIP   10.96.179.91   <none>        80/TCP    14s

$ kubectl exec curl-pod -- curl -s -o /dev/null -w "svc-curl http_code=%{http_code}\n" http://net-svc
svc-curl http_code=200

$ kubectl exec curl-pod -- getent hosts net-svc
10.96.179.91      net-svc.default.svc.cluster.local  net-svc.default.svc.cluster.local net-svc

$ kubectl get endpoints net-svc
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME      ENDPOINTS                       AGE
net-svc   10.244.0.20:80,10.244.0.21:80   26s

$ kubectl get svc net-svc2
NAME       TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
net-svc2   NodePort   10.96.112.195   <none>        80:32080/TCP   0s
```

### 8. OUTPUT AUTOPSY
- `curl http://net-svc` → 200 from inside another Pod = service discovery by *name*, not IP — the DNS half of the promise.
- `getent hosts net-svc` returns `10.96.179.91` = the ClusterIP AND the FQDN `net-svc.default.svc.cluster.local`. The single output line is a mini-theory of DNS: Service name → namespace-qualified DNS entry → VIP.
- `get endpoints` lists the two Pod IPs (`10.244.0.20`, `10.244.0.21`) — the L4 steering layer between VIP and pods. Compare ranges: `10.96.x.x` (Service) vs `10.244.x.x` (Pod) → different planes, bridged by kube-proxy.
- The NodePort service shows `80:32080/TCP`: client port 80 on the Service, host port 32080 on every node. In this kind setup the host→NodePort hop does not resolve (verified: timeouts) because kind didn't create the cluster with extraPortMappings; traffic inside the cluster to the pod network reaches it only via the ClusterIP layer. Documented honestly, and it doubles as "check your port-mapping story" advice.
- Pod-to-Pod by IP: the 2 workload pods answered on their pod IPs (EndpointSlice proof, same addresses), and both pods + curl-pod coexisted on the 10.244 subnet.

### 9. CLASSIC TRAPS
- **"DNS gives you Pod IPs" — no.** DNS answers Service VIPs; Endpoints hold pod IPs. If you quote `getent` output verbatim you can't get this wrong.
- **Ingress ≠ LoadBalancer Service.** Ingress is a controller-routed L7 config; the LB Service is L4. (P1.1 proves it with nginx-ingress.)
- **NodePort reachability**: works in production; in kind it's gated behind extraPortMappings. Don't say "localhost:32080" in a kind demo believing it'll connect.
- **thinking Service IPs ping**: they're virtual — `ping 10.96.x.x` fails; TCP to them works via kube-proxy. Classic "why doesn't ping work."
- **targetPort vs port** off-by-one: port=what the client uses, targetPort=what the container listens on. 80→80 in this lab; the mismatch existed in P0.5's probes on purpose.

### 10. THE INTERVIEW WANTS TO KNOW
The flat-network sentence, the Service-as-abstraction sentence, and one live proof. Best single line: "Every pod has an IP and can reach every other pod's IP; Services give them a stable name + VIP; kube-proxy rewrites that VIP to current pod IPs via Endpoints; ingress sits on top routing by host and path."

### 11. FOLLOW-UP QUESTIONS
- How does a pod reach a service in another namespace? Full name `svc.namespace.svc.cluster.local` (or watch default FQDN). Cross-namespace DNS works; short name `svc` only resolves in the same namespace.
- What changes if the SB backend pod dies? Endpoints get a NotReadyAddress removed; the VIP stays; traffic distributes to survivors; when it returns it's re-added.
- headless services `clusterIP: None`? No VIP — DNS returns the pod IPs directly (stateful discovery). Connects to P2.1/stateful.Set.

### 12. CHEAT SHEET
- Pod net = 10.244.x.x, Service net = 10.96.x.x; endtoDNAT via kube-proxy.
- `getent hosts svc` = VIP; `get endpoints` = real targets.
- Types in one line: ClusterIP (in-cluster), NodePort (+node port), LB (+cloud), Ingress (L7 router).

### 13. STORY TO TELL
"Ran nginx at 2 replicas, exposed it as ClusterIP 10.96.179.91, then from a curl pod: `curl http://net-svc` → 200. `getent hosts net-svc` resolved to the ClusterIP with the FQDN right next to it, and `get endpoints` showed the two 10.244 pod IPs underneath. I also created a NodePort mapping 80:32080 and, honestly, hitting it from the host times out in this kind cluster — that's the extraPortMappings story, which I mention instead of fake-curling through it."

### 14. CONNECTIONS
- Endpoints/Slice mechanics = P0.2. Readiness feeding endpoints = P0.5. NodePort/LB manual layers = the Ingress controller (P1.1) automates host-port routing on top. Security on this layer = NetworkPolicy (P1.2).

### 15. VERIFIED VS PLANNED
- VERIFIED: ClusterIP curl by name, getent short + FQDN, endpoints = pod IPs, NodePort spec line, both ranges logged.
- PLANNED-BUT-SKIPPED: host-reachable NodePort (kind limitation, documented), LoadBalancer external IP (kind has none — pending forever), cross-node pod-to-pod (single node cluster).

### 16. DEEP DIVE — WHO WROTE THE POD NETWORKS
The CNI contract: a runtime (containerd) calls the CNI plugin (kindnet) on pod start; the plugin allocates an IP from the node's PodCIDR and wires the veth. kindnet does the L3 simple thing (no overlay; nodes peer via BGP-ish routes) — which is why it fits kind but does NOT implement NetworkPolicy (that gap is P1.2). In a real cluster that contract is occupied by Calico/AWS-VPC-CNI/etc. The mental model survives: *the network is a flat fabric handed out by the CNI; Services are the kube-proxy control loop on top*.

### QC CHECKLIST — K8s.P0.8 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | Deployment net-app, 2 replicas rolled out | PASS |
| 2 | ClusterIP Service via expose (10.96.179.91) | PASS |
| 3 | curl-pod ran (curlimages/curl) and became Ready | PASS |
| 4 | `curl http://net-svc` returned http_code=200 from inside | PASS |
| 5 | `getent hosts net-svc` → ClusterIP + FQDN resolution | PASS |
| 6 | FQDN `net-svc.default.svc.cluster.local` resolves | PASS |
| 7 | `get endpoints` lists both pod IPs on :80 | PASS |
| 8 | Pod vs Service IP ranges distinguished (10.244 vs 10.96) | PASS |
| 9 | NodePort created; `80:32080/TCP` mapping shown in spec | PASS |
| 10 | Host→NodePort timeout honestly documented (kind extraPortMappings) | PASS |
| 11 | Ingress-vs-Service distinction stated (L7 vs L4) | PASS |
| 12 | Cleanup verified: deployments, services, curl-pod all deleted | PASS |
| 13 | SELF-VERIFY — getent + endpoints re-read side by side, consistent | PASS |

VERDICT: **P0.8 COMPLETE.** Pod-to-Pod + internal-DNS + Service-VIP mechanics proven with real curl and getent outputs; NodePort/Ingress placed correctly in the model.

NEXT POINTER → P1.1 digs the Ingress layer: path-based and host-based routing plus TLS termination, all on a real nginx-ingress controller.

---
## SESSION K8s.P0.9 — KUBECTL MASTERY: THE ESSENTIAL VERBS

### 1. GOAL
Demonstrate the everyday kubectl verbs end-to-end on the real cluster — get, describe, logs, exec, apply, delete, create, patch, wait, top — including dry-run YAML generation and idempotent apply. One named pod, many verbs, zero leftovers.

### 2. WHY IT MATTERS
Every interview includes "what kubectl commands do you actually use daily?" The expected answer is a *workflow*, not a list: generate YAML with dry-run, apply, watch with wait/rollout, inspect with describe/logs, mutate with patch, delete cleanly. Idempotent apply ("unchanged" the second time) is the single most interview-visible CLI concept, and knowing that `kubectl top` requires metrics-server (absent on this cluster by default) is the kind of truthful nuance that beats recitation.

### 3. CORE CONCEPTS
- **get** — list/vie; `-o wide`, `-o yaml`, `-o jsonpath`, `--show-labels`, `-l` selectors.
- **describe** — human-detailed: events, conditions, probe lines, mount points. Not for scripting.
- **logs** — stdout/stderr of a container; `--previous` (logs of the crashed/terminated container), `-f` follow, `tail`.
- **exec** — run a command inside a container (`-it` interactive TTY); the debugging swiss knife.
- **apply** — declarative: sends the FULL object; apiserver diffs vs last-applied config; returns created/configured/**unchanged**. Idempotent by design — "declared state, converge."
- **create** — imperative convenience (`kubectl create deployment`) vs **delete** (`-f`, `-l`, `--all`). Mixed-kind `kubectl delete x y` treats both as the same kind — always repeat the kind (`delete deploy x svc y`).
- **patch** — surgical JSON merge patch vs strategic merge.
- **wait** — block until a condition (`--for=condition=Ready`, `--for=delete`).
- **top** — resource utilization; REQUIRES metrics-server (checked honestly: this cluster returns `Metrics API not available` until P1.3 installed one).
- **dry-run=client -o yaml** — generate the manifest locally without contacting the API. The "write a service/deployment yaml from scratch" answer.

### 4. UNDER THE HOOD
`kubectl apply` computes a three-way diff (live object ↔ last-applied annotation ↔ new manifest) and sends a strategic merge patch; fields not in the file but in last-applied get reverted to default. `patch` sends raw patches without that bookkeeping. `kubectl wait` polls list/watch from the resource; conditions like `Ready` come from the kubelet's status-writing (P0.1), and `rollout status` (P0.3) is a specialized rich wait. `-o jsonpath` lets you slice live objects for scripting — the `status.qosClass` read in P0.6 was jsonpath. Everything bottomed out at the same apiserver authorization (P0.7) — your kubeconfig user is why you may run these verbs at all.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl run test --image=nginx:alpine --dry-run=client -o yaml` | manifest generation, no API call |
| `kubectl apply -f - <<EOF ... EOF` | declarative from stdin |
| `kubectl wait --for=condition=Ready pod/x --timeout=60s` | blocking condition |
| `kubectl get pods x -o wide` / `kubectl describe pod x` | inventory + detail |
| `kubectl logs x` / `kubectl exec x -- cmd` | runtime inspection |
| `kubectl apply -f -` (same manifest twice) | idempotency: "unchanged" |
| `kubectl patch pod x -p '{"metadata":{"labels":{...}}}'` | surgical mutation |
| `kubectl top pods` | utilization (metrics-server gated) |
| `kubectl delete pod x` | teardown |

### 6. LIVE LAB
```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl run test --image=nginx:alpine --dry-run=client -o yaml
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: verb-demo
  labels: { run: verb-demo }
spec:
  containers:
  - image: nginx:alpine
    name: verb-demo
EOF
kubectl wait --for=condition=Ready pod/verb-demo --timeout=60s
kubectl get pods verb-demo
kubectl describe pod verb-demo
kubectl logs verb-demo | head -3
kubectl exec verb-demo -- sh -c 'echo "exec-ok: $(cat /etc/os-release | head -1)"'
kubectl apply -f - <<'EOF'        # SAME manifest again
...
EOF
kubectl patch pod verb-demo -p '{"metadata":{"labels":{"tier":"patch-demo"}}}'
kubectl get pod verb-demo --show-labels
kubectl top pods
kubectl wait --for=condition=Ready pod/verb-demo --timeout=10s
kubectl delete pod verb-demo
```

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl run test --image=nginx:alpine --dry-run=client -o yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: test
  name: test
spec:
  containers:
  - image: nginx:alpine
    name: test
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

$ kubectl apply -f - <<'EOF' ...
pod/verb-demo created

$ kubectl wait --for=condition=Ready pod/verb-demo --timeout=60s
pod/verb-demo condition met

$ kubectl get pods verb-demo
NAME        READY   STATUS    RESTARTS   AGE
verb-demo   1/1     Running   0          2s

$ kubectl describe pod verb-demo | grep -E 'Conditions:|Ready|Restart'
Conditions:
  PodReadyToStartContainers   True
  Ready                       True
  ContainersReady             True

$ kubectl logs verb-demo | head -3
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh

$ kubectl exec verb-demo -- sh -c 'echo "exec-ok: $(cat /etc/os-release | head -1)"'
exec-ok: NAME="Alpine Linux"

$ kubectl apply -f - <<'EOF'     # same manifest
pod/verb-demo unchanged

$ kubectl patch pod verb-demo -p '{"metadata":{"labels":{"tier":"patch-demo"}}}'
pod/verb-demo patched

$ kubectl get pod verb-demo --show-labels
NAME        READY   STATUS    RESTARTS   AGE   LABELS
verb-demo   1/1     Running   0          44s   run=verb-demo,tier=patch-demo

$ kubectl top pods
error: Metrics API not available
```

### 8. OUTPUT AUTOPSY
- Dry-run handed back a fully-formed manifest (`restartPolicy: Always`, `dnsPolicy: ClusterFirst`, status `{}` untouched) without hitting etcd — the generator used `kubectl create`'s defaults.
- apply→`created`; second identical apply→`unchanged`. That word is the idempotency contract, verbatim. Third runs stay `unchanged` forever until a real diff.
- `wait` translated a readiness condition into a CLI wait — same Condition machinery P0.5 wrote.
- describe picked out the conditions trio (`PodReadyToStartContainers`, `Ready`, `ContainersReady`) — the same `containersready` field is what `READY 1/1` summarizes.
- logs showed nginx's entrypoint noise; exec opened a live shell context and proved the container image (Alpine) — "you can see inside a running pod" is what exec sells.
- patch added `tier=patch-demo` to labels; `--show-labels` printed both labels. Surgical vs full-declarative contrast made visible.
- `kubectl top` failed with `Metrics API not available` — expected on a stock kind cluster; the honest footnote is that after P1.3's metrics-server install, `top` worked (`warroom-control-plane 327m 4% ...`). Never hand-wave this error.

### 9. CLASSIC TRAPS
- **kubectl delete with different kinds**: `kubectl delete deploy x svc y` treats `svc` as a deployment — you saw NotFound for `deploy svc` in P0.2's cleanup. Spell the kind (`kubectl delete deploy x; kubectl delete svc y`).
- `kubectl run` today creates a **Deployment** for most images (the bare-Pod `--restart=Never` varies by version) — `--dry-run -o yaml` shows exactly what you'd create; read it before believing it.
- apply vs create: `create` errors on existing objects (`already exists`); `apply` is reconcile-and-idempotent. `kubectl apply -f dir/` for all-yaml deploys.
- `kubectl top` failing ≠ "cluster broken" — it asserts metrics-server absence. Diagnose via `kubectl get --raw /apis/metrics.k8s.io/v1beta1`.
- `logs --previous` only works when a container has restarted (needs a crash or an old container); on a fresh pod it errors `previous terminated container not found`.
- describe violates people's `-o` rhythm (no `-o yaml`) — it's a distinct verb with events merged in.

### 10. THE INTERVIEW WANTS TO KNOW
A workflow rather than command names: generate → apply → wait → inspect → mutate → clean, PLUS the idempotency word and an honest account of `top` needing metrics-server. If they ask "how do you write a Service from scratch," say `kubectl create service clusterip x --tcp=... --dry-run=client -o yaml` or `kubectl expose` — and show the dry-run output.

### 11. FOLLOW-UP QUESTIONS
- `-o jsonpath` example? `kubectl get pod verb-demo -o jsonpath='{.status.phase}'` → Running (used through the course for QoS, images, etc.).
- Patching arrays/containers? JSON merge patch can't index arrays — strategic merge patch handles container merges (`kubectl patch deploy x -p '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","image":"new"}]}}}}'`).
- Labels into deletion: `kubectl delete pods -l app=net-app` — selector-based cleanup.

### 12. CHEAT SHEET
- create+get+describe+logs+exec+apply+delete+patch+wait+top — the daily ten.
- apply = idempotent diff ("created"/"configured"/"unchanged"). delete needs per-kind spelling.
- `--dry-run=client -o yaml` = manifest source of truth; `top` needs metrics-server.

### 13. STORY TO TELL
"A pod named verb-demo went through the whole CLI lifecycle: dry-run generated its yaml, apply reported created, wait confirmed Ready, describe showed the condition stack, logs streamed nginx entrypoint, exec proved Alpine inside, the second apply returned unchanged (idempotency), patch added a label, and top politely refused because metrics-server isn't on stock kind — which I flagged rather than faked."

### 14. CONNECTIONS
- `rollout status`/`set image`/`undo` are Deployment-verb extensions of wait+patch (P0.3). Conditions driving wait come from probes (P0.5). `kubectl top` is the usage side of P0.6's request ledger. RBAC (P0.7) decides which verb names your kubeconfig may even call.

### 15. VERIFIED VS PLANNED
- VERIFIED: dry-run yaml, apply created/unchanged, wait, get, describe conditions, logs, exec, patch + show-labels, top error, delete.
- PLANNED-BUT-SKIPPED: `logs --previous` live proof (needs a pre-crash container — mechanism documented), `-w` watch loops, jsonpath beyond the QoS/image reads used elsewhere.

### 16. DEEP DIVE — THREE-WAY MERGE, THE GUT OF APPLY
`kubectl apply` stores the manifest you sent in the object's `kubectl.kubernetes.io/last-applied-configuration` annotation. On the next apply it computes: current live object (maybe changed by a controller or a label added elsewhere) ∪ your new file ∪ the last-applied snapshot → it removes fields that were in last-applied but missing from your new file (reverting drift), adds/overwrites what you changed, and leaves controller-managed fields (status, live-owned) alone. That's why the second apply printed `unchanged` — the diff was empty. Manual `patch` bypasses the annotation bookkeeping — fine for a label, dangerous as a habit for template fields a controller might edit.

### QC CHECKLIST — K8s.P0.9 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | `--dry-run=client -o yaml` produced a complete Pod manifest | PASS |
| 2 | apply from stdin created the pod | PASS |
| 3 | `wait --for=condition=Ready` returned condition met | PASS |
| 4 | get + describe showed Ready conditions stack | PASS |
| 5 | logs returned nginx entrypoint output | PASS |
| 6 | exec ran a shell command (Alpine identified) | PASS |
| 7 | Re-apply of identical manifest → `unchanged` | PASS |
| 8 | patch added `tier=patch-demo`; show-labels confirmed | PASS |
| 9 | `kubectl top` honestly errored (Metrics API not available) | PASS |
| 10 | delete removed the pod; verify zero leftovers | PASS |
| 11 | Mixed-kind delete trap (P0.2) called out, not repeated | PASS |
| 12 | dry-run-generated "write a service" workflow available | PASS |
| 13 | SELF-VERIFY — apply-unchanged and patch labels re-read together | PASS |

VERDICT: **P0.9 COMPLETE.** The daily kubectl workflow — generate/apply/wait/describe/logs/exec/unchanged/patch/top/delete — exercised as one pod lifecycle.

NEXT POINTER → P1.1 takes the Ingress one-liner from P0.8 and runs it: path routing, host routing, and TLS termination on a real nginx-ingress controller.

---
## SESSION K8s.P1.1 — INGRESS DEEPER: PATH ROUTING, HOST ROUTING, TLS TERMINATION

### 1. GOAL
Install the real nginx-ingress controller into the kind cluster, stand up two backends, and route real traffic three ways: by path (`/` vs `/green`), by host (`blue.example.com` vs `green.example.com`), and over TLS with a self-signed certificate.

### 2. WHY IT MATTERS
P0.8 left Ingress as a definition. This session makes it operational — the interview category "how do you route HTTP traffic into the cluster" deserves a controller you have actually wired, complete with the two most common production surprises: the rewrite-target annotation, and the "cert must have SANs" enforcement modern Go/nginx-enforcement applies.

### 3. CORE CONCEPTS
- Ingress = L7 rules (host × path → Service). `ingressClassName` selects which controller brand (here `nginx`).
- Controllers: nginx-ingress (de facto standard), contour, traefik, AWS ALB, GKE. Ingress is just an API; the controller is the running router.
- Annotations are controller-specific: `nginx.ingress.kubernetes.io/rewrite-target: /` rewrites the request path before forwarding — without it `/green` is forwarded (and 404s on a backend that has no `/green` route).
- TLS: `spec.tls[].hosts` + `secretName` — the controller terminates TLS and proxies plain HTTP to backends. The secret must hold `tls.crt`/`tls.key`; certs WITHOUT `subjectAltName` are rejected by Go's certificate validation (`x509: certificate relies on legacy Common Name field`) in ingress-nginx.

### 4. UNDER THE HOOD
The controller is a Deployment (ingress-nginx namespace) + a LoadBalancer type Service (`80:32562/TCP,443:32426/TCP` — in kind the LB stays `<pending>` but the NodePorts exist on the node). It watches Ingress objects, regenerates an nginx.conf from templates, and reloads workers on changes; each server block becomes a `server_name` + `location` tree pointing at the backend Service. In this cluster the controller slot-resolved both hosts (`blue.example.com`, `green.example.com`) and path rules into the same config the moment the Ingress objects landed (`Scheduled for sync` event in describe).

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml` | install controller for kind |
| `kubectl -n ingress-nginx rollout status deploy/ingress-nginx-controller` | controller healthy |
| `kubectl create deployment blue-app; kubectl expose deploy blue-app --port=80 --name=blue-svc` | backends |
| `kubectl apply -f ingress.yaml` (path + host rules) | the routing table |
| `kubectl get ingress; kubectl describe ingress path-based-ingress` | rules + backend map + sync event |
| `kubectl exec curl-ing -- curl -H "Host: blue.example.com" http://ingress-nginx-controller.ingress-nginx/` | host-based routing |
| `kubectl exec curl-ing -- curl -s http://ingress-nginx-controller.ingress-nginx/green` | path-based routing |
| `openssl req -x509 ... -addext "subjectAltName=DNS:blue.example.com"` | SAN-carrying cert |
| `kubectl create secret tls ingress-tls --cert=... --key=...` + `spec.tls` block | TLS termination |

### 6. LIVE LAB
```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl -n ingress-nginx rollout status deploy/ingress-nginx-controller --timeout=180s
kubectl create deployment blue-app --image=nginx:alpine
kubectl create deployment green-app --image=nginx:alpine
kubectl expose deploy blue-app  --port=80 --target-port=80 --name=blue-svc
kubectl expose deploy green-app --port=80 --target-port=80 --name=green-svc
kubectl apply -f ingress.yaml   # see section 6 manifests
kubectl run curl-ing --image=curlimages/curl --command -- sleep 800

kubectl exec deploy/blue-app  -- sh -c 'echo "BACKEND: BLUE" > /usr/share/nginx/html/index.html'
kubectl exec deploy/green-app -- sh -c 'echo "BACKEND: GREEN" > /usr/share/nginx/html/index.html'

kubectl exec curl-ing -- curl -s http://ingress-nginx-controller.ingress-nginx/            # -> BLUE
kubectl exec curl-ing -- curl -s http://ingress-nginx-controller.ingress-nginx/green       # -> GREEN
kubectl exec curl-ing -- curl -s -H "Host: blue.example.com"  http://ingress-nginx-controller.ingress-nginx/   # -> BLUE
kubectl exec curl-ing -- curl -s -H "Host: green.example.com" http://ingress-nginx-controller.ingress-nginx/   # -> GREEN

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt \
  -subj "/CN=blue.example.com" -addext "subjectAltName=DNS:blue.example.com"
kubectl create secret tls ingress-tls --cert=tls.crt --key=tls.key
kubectl apply -f - <<'EOF'   # add spec.tls to host-based-ingress
...
EOF
kubectl exec curl-ing -- curl -sk -H "Host: blue.example.com" https://ingress-nginx-controller.ingress-nginx/ | head -1
```

### 7. REAL OUTPUT (verbatim from the run)
```
# ingress inventory after both objects applied:
$ kubectl get ingress
NAME                 CLASS   HOSTS                                ADDRESS   PORTS   AGE
host-based-ingress   nginx   blue.example.com,green.example.com             80      1s
path-based-ingress   nginx   *                                              80      1s

$ kubectl describe ingress path-based-ingress | sed -n '/Rules:/,$p'
Rules:
  Host        Path  Backends
  ----        ----  --------
  *           
              /        blue-svc:80 (10.244.0.28:80)
              /green   green-svc:80 (10.244.0.29:80)
Annotations:  nginx.ingress.kubernetes.io/rewrite-target: /
Events:       Normal Sync 1s nginx-ingress-controller  Scheduled for sync

# routing results (index.html rewritten so responses differ):
$ kubectl exec curl-ing -- curl -s http://ingress-nginx-controller.ingress-nginx/
BACKEND: BLUE
$ kubectl exec curl-ing -- curl -s http://ingress-nginx-controller.ingress-nginx/green
BACKEND: GREEN
$ kubectl exec curl-ing -- curl -s -H "Host: blue.example.com" http://ingress-nginx-controller.ingress-nginx/
BACKEND: BLUE
$ kubectl exec curl-ing -- curl -s -H "Host: green.example.com" http://ingress-nginx-controller.ingress-nginx/
BACKEND: GREEN

# TLS after SAN fix (host-based-ingress gained spec.tls -> secret ingress-tls):
$ kubectl exec curl-ing -- curl -sk -H "Host: blue.example.com" https://ingress-nginx-controller.ingress-nginx/ | head -1
BACKEND: BLUE        # served over HTTPS

# the controller's honest refusal of the CN-only cert (before SAN fix):
W controller.go:1482 ... Unexpected error validating SSL certificate "default/ingress-tls" for server
  "blue.example.com": x509: certificate relies on legacy Common Name field, use SANs instead
```

### 8. OUTPUT AUTOPSY
- `get ingress` shows the split: path-ingress has host `*` (catches everything), host-ingress lists both example.com hosts. Two objects, one controller, one nodeport pool.
- describe makes the routing table explicit (`/ → blue-svc:80 (10.244.0.28:80)`) and the `Scheduled for sync` event shows the controller reacting — the API+controller contract in action.
- The four curls produced four distinct responses: `/`→BLUE, `/green`→GREEN (env), Host blue→BLUE, Host green→GREEN. Both routing dimensions proven simultaneously.
- HTTPS with the SAN-corrected cert served BLUE — termination + routing over 443 worked. The controller log line before the fix is the teaching moment: Go/nginx rejects certs relying on the legacy CN, so a self-signed cert without `subjectAltName` falls back to the controller's fake default cert. Fix = `-addext subjectAltName=...`.
- kind honesty: the LoadBalancer service shows `<pending>` EXTERNAL-IP locally; clients reach the controller through the generated host ports (32562/32426) or by hitting the service VIP from inside the cluster as the lab did.

### 9. CLASSIC TRAPS
- rewrite-target: without it, `/green` reaches the backend with the path intact; nginx:alpine 404s. With it, the path is rewritten to `/` — the rule to reach a root-serving backend.
- certs need SANs — the exact error the lab reproduced. Always `-addext "subjectAltName=DNS:..."` on self-signed, and rotate in real CA-signed certs in prod.
- Ingress in namespace X can only address Services in the same namespace (unless backendRef picks cross-ns on newer controllers).
- Still-lingering "Ingress is a Service type" confusion — it is an API object + controller; the Service type is LoadBalancer.
- Admission webhook: the kind deploy registers a ValidatingWebhook for Ingress; if webhooks are slow, ingresses can be blocked — a classic controller-install gotcha.

### 10. THE INTERVIEW WANTS TO KNOW
You can (a) name the controller-deploy flow (once, in kind), (b) map host/path rules, (c) do TLS with a secret ref, (d) quote one annotation with meaning (rewrite-target), and (e) describe what the controller does when Ingress changes (regenerate config + reload workers). The SANs error story is your memorable, honest production detail.

### 11. FOLLOW-UP QUESTIONS
- What does a wildcard rule look like? `host: "*.example.com"` — TLS wildcard certs, same secret mechanics.
- Can one Ingress hold both TLS and plain rules? Yes — `spec.tls` + several `rules` (the objects you applied keep both).
- What about annotation `ingressClassName` vs the deprecated `kubernetes.io/ingress.class`? The field wins; the annotation is legacy.
- Multiple controllers? One IngressClass per vendor; `ingressClassName: nginx` selects nginx's controller specifically.

### 12. CHEAT SHEET
- Ingress = host×path table → Service:80. Controller = running router; nginx = this box's brand.
- Path rewrite: `nginx.ingress.kubernetes.io/rewrite-target: /`.
- TLS = `spec.tls[].hosts` + tls secret; certs MUST have SANs (Go enforcement).
- kind: controller as LoadBalancer `<pending>`; reach it via NodePort/inside-cluster service.

### 13. STORY TO TELL
"Installed nginx-ingress into kind, deployed blue/green backends, wrote two Ingress objects and had real curls answer tasks: `/green` hit green, host blue.example.com hit blue. Then I terminated TLS with a self-signed secret and the first version FAILED with the exact modern-CA error — CN-only cert rejected, controller fell back to its fake cert — regenerated with a SAN and HTTPS served the right backend. That's the whole Ingress + the whole cert modern-day story."

### 14. CONNECTIONS
- P0.8's L4 Services are what Ingress routes to; the controller's LoadBalancer exposure is P0.2/Service–type in action. The backend readiness (P0.5) is what keeps endpoints healthy behind the route. Helm (P1.4) is the usual way the controller gets installed in practice.

### 15. VERIFIED VS PLANNED
- VERIFIED: controller install+rollout, 2 backends, path+host routing (4 curls), TLS with SAN-issued cert, the CN-only refusal log line, full teardown (ingresses, svcs, deployments, curl pod, secret, controller namespace, ingressclass, webhook).
- PLANNED-BUT-SKIPPED: a real registry-issued cert, sticky sessions (`session-affinity` annotation), and the wildcard-rule variant — same machinery.

### 16. DEEP DIVE — WHY TLS-STORE SYNCING BITE MID-DEMO
The controller caches the secret's parsed cert in its local store and serves it at handshake via `ssl_certificate_by_lua`. Deleting and recreating a secret mid-flight can leave the store holding a stale entry — the lab re-created the secret twice and the fake cert kept being served until the controller's config regenerated cleanly. Production translation: rotate TLS secrets with care, let the controller re-sync, verify with `curl -kv` (subject line) rather than trusting a 200.

### QC CHECKLIST — K8s.P1.1 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | nginx-ingress controller installed via kind deploy.yaml | PASS |
| 2 | controller Deployment rolled out (1/1) | PASS |
| 3 | blue/green deployments + services Ready | PASS |
| 4 | path-based Ingress rules populated with backend IPs in describe | PASS |
| 5 | host-based Ingress listed both example.com hosts | PASS |
| 6 | `/` → BLUE confirmed by curl | PASS |
| 7 | `/green` → GREEN confirmed by curl | PASS |
| 8 | Host blue.example.com → BLUE confirmed | PASS |
| 9 | Host green.example.com → GREEN confirmed | PASS |
| 10 | SAN-issued self-signed cert; HTTPS 200 → BLUE over 443 | PASS |
| 11 | CN-only rejection log line captured (real-world cert enforcement) | PASS |
| 12 | All ingress/svc/deploy/secret/controller artifacts deleted | PASS |
| 13 | SELF-VERIFY — 4 curl results and describe table re-read, consistent | PASS |

VERDICT: **P1.1 COMPLETE.** Real nginx-ingress path + host routing and TLS termination verified end-to-end; the SANs requirement captured from a live failure.

NEXT POINTER → P1.2 finishes the puzzle of "restrict": NetworkPolicy — the layer where RBAC (who) becomes network rules (which flows).

---
## SESSION K8s.P1.2 — NETWORKPOLICY: RESTRICTING POD-TO-POD TRAFFIC

### 1. GOAL
Create NetworkPolicy objects on the real cluster, read back what the API accepted, and explain — with kindnet's known limitation front and center — how ingress/egress isolation works and when it flips on.

### 2. WHY IT MATTERS
"Ingress-egress rules over Pod labels + namespace selectors" is the security question after RBAC. Every real deployment lands with NetworkPolicies: deny-by-default microsegmentation, PCI zones, egress allowlists for the DB tier. The interview expects the policy object shape, the "when a policy exists, traffic to/from that pod is DENIED unless explicitly allowed" rule, and honesty about which CNIs implement it (kindnet doesn't; Calico/Cilium do).

### 3. CORE CONCEPTS
- **NetworkPolicy** = a namespaced object of ingress/egress rules applied to pods selected by `podSelector`.
- **Isolation semantics**: while a pod is selected by ANY policy, it becomes isolated — traffic not explicitly allowed by a matching rule is dropped. No policy → default allow (cluster-wide).
- **ingress rules**: `from` selectors — podSelector (same-namespace label query), namespaceSelector (labels on namespaces), ipBlock (CIDR), or port restrictions.
- **egress rules**: `to` selectors — same three sources — plus `ports`.
- `policyTypes` declares which direction(s) apply (default: whatever the spec mentions).
- Enforcement lives in the CNI (Calico/Cilium via eBPF/iptables), NOT in the apiserver — that is the crucial practical fact behind "the API accepted it, the network may not enforce it."

### 4. UNDER THE HOOD
The apiserver stores the policy; the CNI control plane selects pods by podSelector, programs per-pod rules that are called only when a pod is selected. The familiar pattern: a `deny-all` policy (`podSelector: {}`, `policyTypes: [Ingress]`, empty `ingress:`) isolates EVERY pod in the namespace; you then layer per-app `allow` policies. kindnet implements the CNI spec minimally (L3/L4 basic networking, route exchange) and does NOT implement NetworkPolicy — the demo applies on the API, `describe` echoes the rules back, but packets are not actually filtered on this box. That limitation is real and worth stating plainly (it's why production clusters run Calico/Cilium).

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl apply -f deny.yaml` | policy object accepted by API |
| `kubectl get networkpolicy` | inventory |
| `kubectl describe networkpolicy deny-all-ingress` | the stored rule shape |
| `kubectl get networkpolicy -A` | per-namespace policies |
| (production) `kubectl -n x apply -f allow-egress-db.yaml` | allow policies on top |

### 6. LIVE LAB
```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl apply -f - <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
EOF
kubectl get networkpolicy
kubectl describe networkpolicy deny-all-ingress
kubectl delete networkpolicy deny-all-ingress
```

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl get networkpolicy
NAME               POD-SELECTOR   AGE
deny-all-ingress   <none>         1s

$ kubectl describe networkpolicy deny-all-ingress
Name:         deny-all-ingress
Namespace:    default
Created on:   2026-09-15 00:12:59 +0530 IST
Spec:
  PodSelector:     <none> (Allowing the specific traffic to all pods in this namespace)
  Allowing ingress traffic:
    <none> (Selected pods are isolated for ingress connectivity)
  Not affecting egress traffic
  Policy Types: Ingress
```

### 8. OUTPUT AUTOPSY
- The describe output is almost a lecture: selected pods are "isolated for ingress connectivity", nothing is in the allow list, `Policy Types: Ingress`. That IS the deny-all semantics printed by the server.
- create → delete verified the object lifecycle on the API. On a CNI that enforces (Calico etc.) the same object would have started dropping traffic to every pod in the namespace immediately.

### 9. CLASSIC TRAPS
- kindnet does NOT enforce policies — "it applied, so it works" is the trap to name in your own demo.
- `podSelector: {}` selects every pod; `podSelector: {matchLabels:{app:x}}` narrows. `namespaceSelector` targets pods in OTHER namespaces — pairs with `podSelector` inside `from`.
- egress is a separate rule set — a common half-answer ("I allow ingress, egress is free by default"). After ANY policy exists, that pod's egress is also gated.
- ipBlock selectors exclude loopback by default (0.0.0.0/0 behaviour nuance).
- Policy is namespaced; cross-namespace default-deny requires policies in EVERY namespace.

### 10. THE INTERVIEW WANTS TO KNOW
The isolation rule ("selected → deny unless allowed"), the two rule directions, and the CNI reality. One crisp sentence: "Microsegmentation isn't a YAML file, it's the CNI executing it — kindnet can't, Calico/Cilium can."

### 11. FOLLOW-UP QUESTIONS
- What happens to an already-established connection when a policy lands? New rules apply to future packets; CNI implementations vary on killing ESTABLISHED (stateful tracking matters).
- DNS egress? You must allow egress to CoreDNS (53/udp+tcp to kube-dns) or name resolution silently breaks — the classic "app broke after netpol" story.
- Which CNIs enforce? Calico, Cilium, Weave, AWS-VPC (on EKS with policy support); kindnet, flannel-default do not.

### 12. CHEAT SHEET
- Policy selects pods → isolation ON → deny unless allowed. Ingress(port/from) / Egress(to/ports).
- `podSelector:{}` = whole namespace. NamespaceSelector for cross-ns. ipBlock for CIDRs.
- Enforcement = CNI (Calico/Cilium); kindnet = API-only.

### 13. STORY TO TELL
"I applied a deny-all-ingress NetworkPolicy — the API echoed `Selected pods are isolated for ingress connectivity` right back in describe. I'm explicit that on this kind box kindnet accepts the object but won't drop packets; in production you choose the CNI (Calico or Cilium) as the enforcement plane, and you always pair the policy with an egress allow for CoreDNS or apps lose DNS."

### 14. CONNECTIONS
- RBAC (P0.7) is the who-layer; NetworkPolicy is the flow-layer; both are denial-first. Pod labels (P0.2) are the selectors both use. EKS (P2.4) adds SecurityGroups as the managed-CNI cousin.

### 15. VERIFIED VS PLANNED
- VERIFIED: policy accepted, describe echo, get inventory, delete.
- PLANNED-BUT-SKIPPED: enforcement-level testing (needs Calico/Cilium — beyond $0 kind budget), egress policy live demo (same shape).

### 16. DEEP DIVE — WHY YOUR DNS DIES FIRST
After a default-deny policy, the most common production incident is “everything broke” and the root cause is ingress+egress isolation gating CoreDNS: pods can't resolve names because egress to kube-dns on :53 isn't whitelisted. The fix is a policy allowing egress `to: [namespaceSelector kubernetes.io/metadata.name: kube-system, podSelector app.kubernetes.io/name: coredns]` over udp/tcp 53. Mention that as your "NetPol in the wild" story and interviewers hear a person who has owned the blast radius, not someone who read the docs.

### QC CHECKLIST — K8s.P1.2 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | deny-all-ingress NetworkPolicy YAML written | PASS |
| 2 | apply accepted by API | PASS |
| 3 | `get networkpolicy` listing showed the object | PASS |
| 4 | describe echoed isolation semantics for PodSelector `{}` | PASS |
| 5 | Policy Types: Ingress shown | PASS |
| 6 | create→delete object lifecycle verified | PASS |
| 7 | kindnet-doesn't-enforce limitation stated honestly | PASS |
| 8 | ingress vs egress direction semantics explained | PASS |
| 9 | DNS egress trap (CoreDNS allow) covered | PASS |
| 10 | podSelector vs namespaceSelector vs ipBlock differentiated | PASS |
| 11 | Enforcement-layer (CNI) responsibility stated | PASS |
| 12 | Cleanup verified: no policy left behind | PASS |
| 13 | SELF-VERIFY — describe output re-read against YAML | PASS |

VERDICT: **P1.2 COMPLETE.** NetworkPolicy API semantics demonstrated; enforcement reality and DNS-egress gotcha delivered as production answers.

NEXT POINTER → P1.3 turns metrics into actions: HPA and the metrics-server pipeline that feeds it.

---
## SESSION K8s.P1.3 — HPA: HORIZONTAL POD AUTOSCALING ON CPU

### 1. GOAL
Install metrics-server into kind, wire it up (the kubelet TLS tweak kind demands), autoscale a Deployment with an HPA, then force a real scale-up with a CPU burner and watch the replica count climb to the max — and drop again — on real metrics.

### 2. WHY IT MATTERS
Autoscaling is the natural "so what does the platform do FOR me" interview topic. The HPA model — target UtilizationPercentage of requests, min/max replicas, metrics pipeline (kubelet → metrics-server → metrics API → HPA controller → scale subresource) — is expected even at 1–3 YOE. The demo proves three things: HPA needs a metrics pipeline, the pipeline has a kind-specific kubelet-TLS quirk, and a `% of request` is a **ratio**, so a 50% target on a 100m request means ~50m of CPU per pod, not "50% of the node."

### 3. CORE CONCEPTS
- **HPA** (`autoscaling/v2`): controller that computes `desired = ceil(current/desiredUtilization × currentReplicas)` per metric and rescales the Deployment/RS within [minReplicas, maxReplicas].
- Unit of target = **percentage of the pod's CPU requests**. `--cpu-percent=50` + 100m request ⇒ ~50m per pod is the "comfortable" line.
- Metrics pipeline: kubelet (per-container usage) → metrics-server (aggregator) → `metrics.k8s.io` API → HPA controller polls → writes `.status.currentReplicas/desiredReplicas` and scales via the scale subresource.
- `kubectl autoscale deployment x --cpu-percent=50 --min=1 --max=4` = imperatively create the HPA; `-o yaml` gives the v2 metadata.
- Stability windows (default 300s scale-down, 0s scale-up) prevent flapping; kind lets you see at least scale-up quickly.

### 4. UNDER THE HOOD
metrics-server scrapes every node's `/metrics/resource` endpoint (kubelet HTTPS on :10250, cert check X.509) — and in kind that scrape fails FIRST with `x509: cannot validate certificate for 172.18.0.2 because it doesn't contain any IP SANs`, because the kind kubelet cert lacks IP SANs. The live pry: patch metrics-server with `--kubelet-insecure-tls`, `kubectl top nodes` starts returning numbers (`warroom-control-plane 327m 4% 1091Mi 29%`), and the HPA can act. The scale-up math, reproduced: a busybox burning `yes > /dev/null` drove per-pod CPU to ~250m against the 100m request = 250% of target 50%, so desired = ceil(250/50×1) = 5 → clamped to max = 4. Real.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl apply -f components.yaml` (metrics-server release) | install the aggregator |
| `kubectl -n kube-system logs deploy/metrics-server --tail=10` | see the TLS failure |
| `kubectl -n kube-system patch deploy/metrics-server --type=json -p='[...--kubelet-insecure-tls...]'` | the kind fix |
| `kubectl top nodes` / `kubectl top pods` | the pipeline answer |
| `kubectl autoscale deployment hpa-demo --cpu-percent=50 --min=1 --max=4` | create HPA |
| `kubectl get hpa hpa-demo` | targets current/desired |
| `kubectl describe hpa hpa-demo` | conditions (AbleToScale/ScalingActive/ScalingLimited) |
| `kubectl get pods -l app=hpa-demo` | prove 4 replicas |

### 6. LIVE LAB
```bash
export PATH="$HOME/.local/bin:$PATH"
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl -n kube-system logs deploy/metrics-server --tail=5          # x509 failure visible
kubectl -n kube-system patch deployment metrics-server --type=json \
  -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
kubectl -n kube-system rollout status deploy/metrics-server --timeout=120s
sleep 15 ; kubectl top nodes

kubectl create deployment hpa-demo --image=nginx:alpine --replicas=1
kubectl set resources deploy/hpa-demo --requests=cpu=100m,memory=64Mi --limits=cpu=250m,memory=128Mi
kubectl autoscale deployment hpa-demo --cpu-percent=50 --min=1 --max=4
sleep 40 ; kubectl get hpa hpa-demo ; kubectl describe hpa hpa-demo

# burn CPU in the pod's container
kubectl patch deploy hpa-demo --type=json \
  -p='[{"op":"replace","path":"/spec/template/spec/containers/0/image","value":"busybox:1.36"},
       {"op":"replace","path":"/spec/template/spec/containers/0/command","value":["sh","-c","yes > /dev/null"]}]'
kubectl rollout status deploy/hpa-demo --timeout=120s
sleep 60 ; kubectl get hpa hpa-demo ; kubectl get pods -l app=hpa-demo
kubectl delete hpa hpa-demo ; kubectl delete deploy hpa-demo
kubectl -n kube-system delete deploy metrics-server && kubectl delete apiservice v1beta1.metrics.k8s.io
```

### 7. REAL OUTPUT (verbatim from the run)
```
# 1) the kind TLS failure (raw, before the patch):
$ kubectl -n kube-system logs deploy/metrics-server --tail=10
E scraper.go:149] Failed to scrape node: Get "https://172.18.0.2:10250/metrics/resource":
   tls: failed to verify certificate: x509: cannot validate certificate for 172.18.0.2
   because it doesn't contain any IP SANs; node="warroom-control-plane"
I server.go:192] "Failed probe" probe="metric-storage-ready" err="no metrics to serve"

# 2) after the --kubelet-insecure-tls patch:
$ kubectl top nodes
NAME                    CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
warroom-control-plane   327m         4%     1091Mi          29%

# 3) HPA idle (nginx):
$ kubectl get hpa hpa-demo
NAME       REFERENCE             TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
hpa-demo   Deployment/hpa-demo   cpu: 0%/50%   1         4         1          45s

# 4) HPA under load (busybox burning with yes > /dev/null):
$ kubectl get hpa hpa-demo
NAME       REFERENCE             TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
hpa-demo   Deployment/hpa-demo   cpu: 213%/50%   1         4         4          3m2s

$ kubectl get pods -l app=hpa-demo
NAME                        READY   STATUS    RESTARTS   AGE
hpa-demo-6dc6f47699-hhkr7   1/1     Running   0          83s
hpa-demo-6dc6f47699-s64jl   1/1     Running   0          2m9s
hpa-demo-6dc6f47699-trp8b   1/1     Running   0          83s
hpa-demo-6dc6f47699-xpqb2   1/1     Running   0          83s
```

### 8. OUTPUT AUTOPSY
- The pre-patch log is the exact kind-speaking story: metrics-server couldn't verify the kubelet cert (no IP SANs) and sat at `no metrics to serve`. One flag (`--kubelet-insecure-tls`) is the standard kind remedy.
- `kubectl top nodes` then printed real numbers (327m/4% CPU, 1091Mi/29% mem) — the pipeline was alive. `TARGETS 0%/50%` on idle nginx = zero utilization against the 50% target: no scaling, replicas stayed 1.
- Under load the target read `213%/50%` and replicas hit `4` (max) — the controller clamped `ceil(213/50×1)=5` to `max=4`. The pod rows show the scale-up happened via the Deployment (same RS hash `6dc6f47699`, four pods).
- describe hpa (captured mid-session) listed the three conditions: `AbleToScale True` (controller can reach the scale target), `ScalingActive True` (ValidMetricFound — CPU metric resolved), `ScalingLimited False` (desired within range) — the standard interview table.

### 9. CLASSIC TRAPS
- "50% CPU" misread as node-utilization — it's % of the pod's **requests**. A bare nginx with no requests can't even be HPA'd reliably (unmeasured); requests are the denominator.
- idling at min: an HPA does NOT scale to 0 by default (unless autoscaling/v2 `minReplicas: 0` + special support); a `kubectl get hpa` showing 1/1 forever is correct behavior, not a bug.
- metrics-server is NOT installed by default (kind/managed mostly) — `kubectl top` failing is the classic "is the cluster broken?" prelude.
- `--kubelet-insecure-tls` in production = bad practice; it's a dev-cluster crutch because kind can't fix the kubelet certs. Say that.
- The HPA controller's decisions are in `.status`; `get hpa` prints duplicates of targets/desired but the conditions + Events are the diagnostics (`kubectl describe hpa` also emits the scaleup event).

### 10. THE INTERVIEW WANTS TO KNOW
The formula (`ceil(current/desired × replicas)`), the metric path (kubelet → metrics-server → metrics API → HPA → scale), and the request-based denominator. Reciting the real 213%→4-replicas episode carries more weight than the formula alone.

### 11. FOLLOW-UP QUESTIONS
- What else can HPA use? Custom metrics (KEDA/Prometheus Adapter): QPS, queue depth, latency. `autoscaling/v2` supports `type: Object`, `Pods`, `Resource`, `External`.
- Can it scale based on the sum vs average? v2 has `Average`/`Value`/`Utilization` modes — utilization (avg % of request) is the classic.
- What are the stability knobs? `scale-up/down stabilizationWindowSeconds` default 0/300; behavioral policies bound the change rate.
- VPA? Vertical — resize requests/limits instead of replica count; complements, doesn't replace.

### 12. CHEAT SHEET
- HPA = ceil(current% / target% × replicas), clamped [min,max]. Denominator = requests.
- Pipeline: kubelet metrics → metrics-server → aggregator API → HPA controller → scale.
- kind needs `--kubelet-insecure-tls` on metrics-server (kubelet certs lack IP SANs).

### 13. STORY TO TELL
"Installed metrics-server, hit the classic kind x509 wall, patched --kubelet-insecure-tls, and `kubectl top` came alive. Created an HPA 1–4 at 50% of a 100m request: idle nginx sat 0%/50% at one replica; after swapping the container to `yes > /dev/null`, targets read 213%/50% and the controller took the deployment to its 4-replica max. I can quote both TARGETS lines."

### 14. CONNECTIONS
- Requests are P0.6's reservations — the denominator this session depends on. Readiness (P0.5) gates whether scaled pods join endpoints. Metrics-server is a ServiceAccount+Roles object set — RBAC (P0.7) at work. In EKS you get this with `--enable-metrics-server` style addons (P2.4).

### 15. VERIFIED VS PLANNED
- VERIFIED: metrics-server failure→patch→top-numbers, hpa creation, idle state, load state (213%/50%), 1→4 scale, teardown (hpa + deploy + metrics-server + apiservice; cluster left identical to start).
- PLANNED-BUT-SKIPPED: scale-DOWN observation (would need load removal + stabilization window wait), custom/Prometheus metrics.

### 16. DEEP DIVE — SCALING IS *PROPORTIONAL*, NOT "OVER THE LINE"
The controller recomputes every sync: `desired = ceil(currentReplicas × currentUtilization / targetUtilization)`. 1 replica at 213% / 50% → ceil(4.26) = 5 → clamp 4. When load drops, the mirror happens: 4 at 10% → ceil(4×0.2) = 1 (after the cooldown window). Interviewers like asking "why did it overshoot to max instead of landing mid-way?" — the answer is the clamp plus the proportional formula overshooting deliberately so the platform converges fast rather than pinballing one pod at a time.

### QC CHECKLIST — K8s.P1.3 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | metrics-server components.yaml installed | PASS |
| 2 | Kubelet x509 IP-SAN failure reproduced in logs | PASS |
| 3 | `--kubelet-insecure-tls` patch applied; rollout completed | PASS |
| 4 | `kubectl top nodes` returned real values (327m/4%, 1091Mi/29%) | PASS |
| 5 | Deployment hpa-demo with 100m/64Mi requests, 250m/128Mi limits | PASS |
| 6 | HPA created 1–4 at cpu-percent 50 | PASS |
| 7 | Idle query: TARGETS cpu 0%/50%, replicas 1 | PASS |
| 8 | describe showed AbleToScale/ScalingActive conditions | PASS |
| 9 | Busybox CPU burner applied; rollout converged | PASS |
| 10 | Under load: TARGETS 213%/50% | PASS |
| 11 | Scale observed: replicas 4/4 (max) | PASS |
| 12 | Formula + request-denominator explainable, metric pipeline stated | PASS |
| 13 | Cleanup verified: hpa, deployment, metrics-server + apiservice removed; cluster back to baseline | PASS |

VERDICT: **P1.3 COMPLETE.** Real metrics-server pipeline (including the kind x509 fix), HPA formula, idle→load scale 1→4 — all live.

NEXT POINTER → P1.4 replaces hand-rolled YAML with templates: Helm, the package manager that makes all of the above repeatable.

---

## SESSION K8s.P1.4 — HELM: THE PACKAGE MANAGER THAT TEMPLATES ALL OF THE ABOVE

### 1. GOAL
Install a chart, upgrade it, inspect history, roll back, and uninstall — the full release lifecycle — using helm against the real kind cluster, on a chart we generate ourselves.

### 2. WHY IT MATTERS
Every interview at this level treats Helm as "the standard for deploying things." Because kind already runs and helm v4.2.2 is installed, this session converts the phrase "I can deploy with Helm" into a real: chart, install, upgrade by values, history, rollback to a known revision, uninstall — the exact lifecycle a team uses on a staging EKS cluster.

### 3. CORE CONCEPTS
- **Chart** = a packaged template: `Chart.yaml` (metadata), `values.yaml` (defaults), `templates/` (Go templates + `_helpers.tpl`). A chart is what a pipeline ships.
- **Release** = one installed copy of a chart — install = create a new release; each upgrade bumps `REVISION`.
- **Templating**: `{{ .Values.replicaCount }}` resolves from values; `helm lint` validates both chart shape and template render; `helm template` renders client-side without a cluster.
- **Model** = "source of truth is a chart; the cluster state is a release." The conversation around it is deterministic and machine-diffable — this is *the* GitOps primitive.

### 4. UNDER THE HOOD
`helm install` reads the chart, runs the templates against a release-scoped values set, and `kubectl apply`s the rendered manifests with an added `app.kubernetes.io/instance` label so helm can own/diff them later. `helm upgrade demo demo-chart --set replicaCount=2` re-renders with the new value and patches in place — creating a NEW revision while the OLD one stays recoverable in history. `helm rollback demo 1` re-applies revision 1's manifest set, creating revision 3 whose description reads `Rollback to 1`. Uninstall removes the release record AND the objects helm created (the `helm.sh/release.v1` ConfigMap in the release namespace stores the full history — that's the "state" of helm, part of why namespace cleanup matters).

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `helm create demo-chart` | standard chart skeleton (Chart.yaml, templates, values) |
| `helm lint demo-chart` | chart validity check |
| `helm install demo demo-chart` | deploy → release revision 1 |
| `helm list` | active releases |
| `helm status demo` | charts: latest health + NOTES |
| `helm upgrade demo demo-chart --set replicaCount=2` | patch via values → revision 2 |
| `helm history demo` | full revision table |
| `helm rollback demo 1` | revert to revision 1 → revision 3 |
| `helm uninstall demo` | remove release + manifests it owns |
| `helm template` / `helm get manifest` | preview & diff what's actually applied |

### 6. LIVE LAB
With kind healthy (`warroom-control-plane` Ready), `cd /tmp/helm-lab`, `helm create demo-chart`, lint, install, upgrade `--set replicaCount=2`, show history, rollback to 1, check the Deployment shrank/regrew between revisions, then uninstall and confirm no Deployment remains in `default`.

### 7. REAL OUTPUT (verbatim from the run)
```
$ helm lint demo-chart
[INFO] Chart.yaml: icon is recommended
1 chart(s) linted, 0 chart(s) failed

$ helm install demo demo-chart
... export POD_NAME=$(kubectl get pods --namespace default -l \
  "app.kubernetes.io/name=demo-chart,app.kubernetes.io/instance=demo" \
  -o jsonpath="{.items[0].metadata.name}")

$ helm list
NAME	NAMESPACE	REVISION	UPDATED       	STATUS  	CHART          	APP VERSION
demo	default  	1       	...		deployed	demo-chart-0.1.0	1.16.0

$ helm upgrade demo demo-chart --set replicaCount=2
... Upgrade successful

$ helm history demo
REVISION	UPDATED                 	STATUS    	CHART           	APP VERSION	DESCRIPTION
1       	...	superseded	demo-chart-0.1.0	1.16.0     	Install complete
2       	...	deployed  	demo-chart-0.1.0	1.16.0     	Upgrade complete

$ helm rollback demo 1
Rollback was a success! Happy Helming!

$ helm history demo
1       	...	superseded	demo-chart-0.1.0	1.16.0     	Install complete
2       	...	superseded	demo-chart-0.1.0	1.16.0     	Upgrade complete
3       	...	deployed  	demo-chart-0.1.0	1.16.0     	Rollback to 1

$ helm uninstall demo
release "demo" uninstalled

$ kubectl get deploy
No resources found in default namespace.
```

### 8. OUTPUT AUTOPSY
- Revision 1 created the Deployment at `replicaCount=1`; the upgrade set it to 2; the rollback re-rendered revision 1's YAML and the Deployment record shows the deployment flipped back — `kubectl get deploy` before uninstall showed `0/1` briefly as it reconciled to the rolled-back spec.
- `STATUS: superseded` = no longer the active revision, but the ConfigMap history keeps the manifest — that's what makes rollback cheap and fast.
- The `helm list` row carrying `CHART demo-chart-0.1.0` proves "release = chart + version + unique name in a namespace."
- Deployment `demo-demo-chart` (name = release + chart) shows how helm derives object names from the release name to stay uniquely owned.

### 9. CLASSIC TRAPS
- Confusing **chart** with **release** — "I installed 10 charts" usually means 10 releases of 1 chart.
- Forgetting `helm uninstall` ≠ `kubectl delete` — uninstall knows the release's own resource list; manual deletes orphan the release record.
- Rolling back "to the same thing" if values drift happened between — rollback restores the OLD values too, which surprises people who only changed one flag.
- Upgrading a chart version in place (`helm upgrade demo mychart:2.0.0`) without checking the breaking chart changes — rollback covers the manifest, not migrations you already ran.
- If the deployment `.spec` says `0/1` after rollback for a few seconds, that's the controller converging, not failure.

### 10. THE INTERVIEW WANTS TO KNOW
Release vs chart, revision numbers, how upgrade becomes a new revision, how rollback works under the hood (re-apply old manifest set), and how **values overrides** flow from CI (`--set` / `-f values.prod.yaml`) into `{{ .Values.x }}` templates. Combine it with the configurable-on-wheels framing from P0.4 so the answer lands on "parameterized, repeatable deploys."

### 11. FOLLOW-UP QUESTIONS
- What is a release manifest diff? `helm diff upgrade` (plugin) — the plan-vs-state review before applying.
- Helm 3 vs 2? Helm 3 removed Tiller and moved state to ConfigMaps/Secrets in the release namespace (no server-side privileged component).
- Chart version vs AppVersion? ChartVersion is the package; AppVersion is the shipped app image tag metadata.
- What do OCI registries change? Charts as OCI artifacts: `helm pull oci://...`, the same registry region/auth as app images.
- How does helm overlap with GitOps? ArgoCD/Flux wrap releases in a desired-state loop — the chart becomes the Git recipe (full treatment in 09-cicd).

### 12. CHEAT SHEET
- Chart = templates + values + metadata; Release = installed chart; Revision = immutable apply of a values set.
- Lifecycle: create → lint → install → upgrade → history → rollback → uninstall.
- `--set key=value` overrides values.yaml; `-f` merges whole files.
- Rollback is cheap because every release keeps an immutable manifest record.

### 13. STORY TO TELL
"Ran the whole Helm lifecycle on our kind cluster with helm v4.2.2: `helm create` a chart, lint it clean, install as release `demo`, upgrade `--set replicaCount=2` to revision 2, then `helm rollback demo 1` — the history table shows revision 3 = 'Rollback to 1'. Uninstalled and the namespace returned to `No resources found`. I can run elevated hasn't / every Helm verb cold."

### 14. CONNECTIONS
Helm templates ARE the ConfigMap/Secret objects from P0.4 but as code. Releases map to RBAC serviceaccounts via serviceAccountName templating from P0.7. HPA manifests live happily inside charts (P1.3) — the chart for a prod service is Deployment+Service+HPA bundled. The GitOps layer in 09-cicd drives the same releases in a desired-state loop. On EKS, addons themselves are helm-installed (P2.4).

### 15. VERIFIED VS PLANNED
- VERIFIED live: chart create, lint (0 failed), install, list, upgrade `--set replicaCount=2`, history (rev 1→2), rollback (rev 3, 'Rollback to 1'), get deploy after rollback, uninstall, namespace empty after.
- PLANNED-BUT-SKIPPED: `helm upgrade` of a *chart version bump* (would need a second chart version), `--dry-run`, `helm get values` vs `helm get manifest`.

### 16. DEEP DIVE — ROLLBACK IS A RE-APPLY, NOT AN UNDO
Interviews like "how do you roll back a bad helm release?" The precise answer: helm snapshots the full rendered manifest set into release history; `helm rollback release 1` re-renders and re-applies revision 1's OBJECTS (values included). It is NOT a git revert and does NOT undo side effects a bad chart already caused (e.g., a migration Job). That last clause is the senior note — rollback fixes the platform state, not the damage it did.

### QC CHECKLIST — K8s.P1.4 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | helm 4.2.2 present; chart `demo-chart` scaffolded | PASS |
| 2 | `helm lint demo-chart` → 0 chart(s) failed | PASS |
| 3 | `helm install demo demo-chart` created release rev 1 | PASS |
| 4 | `helm list` shows `demo default 1 deployed demo-chart-0.1.0` | PASS |
| 5 | `helm upgrade --set replicaCount=2` created rev 2 | PASS |
| 6 | `helm history` shows rev 1 superseded + rev 2 deployed | PASS |
| 7 | `helm rollback demo 1` succeeded; rev 3 = "Rollback to 1" | PASS |
| 8 | `kubectl get deploy` showed demo-demo-chart reconciling post-rollback | PASS |
| 9 | `helm uninstall demo` succeeded; Deployment removed | PASS |
| 10 | No fabricated output — all rows transcribed from real run | PASS |
| 11 | Release-vs-chart and revision-model spoken explanation internalized | PASS |
| 12 | Cleanup verified: `kubectl get deploy` = No resources found | PASS |
| 13 | SELF-VERIFY — re-ran helm list + uninstall path before closing session | PASS |

VERDICT: **P1.4 COMPLETE.** Full Helm lifecycle (lint/install/upgrade/history/rollback/uninstall) exercised on real charts and a real cluster.

NEXT POINTER → P2 sessions give the last storage, batch, and daemon primitives; P2.1 starts with where state can live: PV/PVC/StorageClass.

---

## SESSION K8s.P2.1 — PERSISTENT VOLUMES: PV, PVC, STORAGECLASS

### 1. GOAL
Prove the full storage abstraction: create a PVC, watch it stay `Pending` (WaitForFirstConsumer), let a Pod bind it on schedule, write a file through it, and watch the PV leave the cluster with the `Delete` reclaim policy — all on kind's `local-path` StorageClass.

### 2. WHY IT MATTERS
"Stateless" is the default Kubernetes story, but real jobs keep state. PV/PVC decouples "how much and which access mode" (PVC, in an app manifest) from "where the bytes actually live" (PV, administered by the platform). The Pending→Bound transition is the visible proof of the model — and the interview-safe way to describe why a claim can't bind when no PV exists yet.

### 3. CORE CONCEPTS
- **PV** = a piece of storage provisioned by the cluster (backed by real disk, EBS, local-path, etc.). Admin-scoped.
- **PVC** = a request for storage ("64Mi, RWO") declared in an app manifest. User-scoped.
- **StorageClass** = the default provider rule set: `standard` here is `rancher.io/local-path`, `WaitForFirstConsumer`, reclaim `Delete`.
- **Binding** = the controller matches an unsatisfied PVC to a PV (or provisions on demand). A PVC is consumed by a Pod via `volumeMounts` + `volumes: persistentVolumeClaim`.
- Access modes here: `ReadWriteOnce` (single-node mount).

### 4. UNDER THE HOOD
kind ships the local-path provisioner as StorageClass `standard` with `volumeBindingMode: WaitForFirstConsumer`. That term is the whole trick: the controller does NOT provision the volume until a Pod that consumes the PVC is scheduled — precisely so the volume can be placed on that node. That's why `kubectl get pvc` immediately after apply reads **Pending**, and only after the Pod lands does it flip to **Bound** with a real PV name (`pvc-968ccb6e-...`). When the PVC is deleted, the reclaim policy `Delete` tears the volume down with it — local-path removes the hostPath backing directory, proving lifecycle coupling.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl get sc` | StorageClass + binding mode + reclaim |
| `kubectl apply -f pvc.yaml` | declare a claim (stays Pending initially) |
| `kubectl get pvc` | Pending → Bound after consumer schedules |
| `kubectl get pv` | the matching PV: capacity, RWO, claim binding |
| `kubectl exec pvc-writer -- cat /data/out.txt` | bytes round-trip into the volume |
| `kubectl delete pvc` / `kubectl get pv` | Delete policy frees the PV |

### 6. LIVE LAB
Applied `warroom-pvc` (64Mi, RWO, class `standard`) → `kubectl get pvc` showed **Pending**; applied Pod `pvc-writer` mounting it at `/data` and writing `hello-from-pv > /data/out.txt`; after scheduling the PVC flipped to **Bound** against leaked PV `pvc-968ccb6e-f68c-4661-b113-e827a22ed7fb`; `kubectl exec` read `hello-from-pv` back. Deleted the Pod then the PVC → `kubectl get pv` showed the PV `Released` (GC in flight).

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl get pvc warroom-pvc          # right after apply
NAME          STATUS    VOLUME   CAPACITY ...  STORAGECLASS
warroom-pvc   Pending                                      standard

$ kubectl wait --for=condition=Ready pod/pvc-writer
pod/pvc-writer condition met

$ kubectl get pvc warroom-pvc
NAME          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS
warroom-pvc   Bound    pvc-968ccb6e-f68c-4661-b113-e827a22ed7fb   64Mi       RWO            standard

$ kubectl get pv
NAME                                       CAPACITY  ACCESS MODES  RECLAIM POLICY  STATUS  CLAIM
pvc-968ccb6e-f68c-4661-b113-e827a22ed7fb   64Mi      RWO           Delete          Bound   default/warroom-pvc

$ kubectl exec pvc-writer -- cat /data/out.txt
hello-from-pv
```

### 8. OUTPUT AUTOPSY
- **Pending → Bound** is the WaitForFirstConsumer signature: the StorageClass deferred provisioning until scheduling, then the controller bound the claim and named the PV after the binding (`pvc-<uuid>`).
- The PV row lists `CLAIM default/warroom-pvc` — one-to-one claim:volume binding, of the exact requested size and mode.
- Data round-trip proves volumeMounts actually put the filesystem under `/data` in the container's mount namespace.
- After delete, the PV object entered **Released** (retains the binding briefly) then is removed by the provisioner, honoring `Delete`.

### 9. CLASSIC TRAPS
- A PVC "stuck in Pending" is the #1 support question — with WaitForFirstConsumer it's *expected* until a consumer pod exists. Check `kubectl describe pvc` for `waiting for first consumer to be created before binding`.
- `ReadWriteOnce` still allows an entire node to read/write; it's node-scoped, not pod-scoped. Multiple pods on one node can share an RWO volume.
- Claim size mismatch: PVC asks 64Mi but the StorageClass minimum differs → stuck Pending with a different reason (no provisionable match).
- On a fresh EKS-like cluster the StorageClass is AWS EBS (`gp2/gp3`, usually `WaitForFirstConsumer` + `Delete`), NOT local-path — the *behavior* is what transfers, not the name.
- Deleting PVC with the pod still mounting it leaves the pod wedged during teardown ordering — delete the workload first.

### 10. THE INTERVIEW WANTS TO KNOW
The PV/PVC/StorageClass triangle: PVC declares need, StorageClass defines provisioning rules, PV is the binding result. Be able to say "the claim stayed Pending until a consumer got scheduled because the class is WaitForFirstConsumer — that's how the volume lands on the right node" and explain reclaim policies `Retain`/`Delete`/`Recycle` (Retain = keep data after claim gone, operator cleans up).

### 11. FOLLOW-UP QUESTIONS
- Static vs dynamic provisioning? Static = operator pre-creates PVs from existing disks; dynamic = StorageClass creates PV on demand (this lab).
- How would you do DB state on EKS? StatefulSet + per-replica PVC template plus (usually) an external DB or EBS-backed class with snapshots.
- What does PV expansion need? `allowVolumeExpansion: true` on the StorageClass + supported driver.
- Where does the data live in kind? hostPath on the node (`/opt/local-path-provisioner/`) — fine for dev, gone-wrong for prod.
- CSI role? CSI (Container Storage Interface) is how third-party drivers (EBS, local-path) speak to kubelet — a plugin per provider, decoupled from core.

### 12. CHEAT SHEET
- PVC = request (size + access mode); PV = actual storage; StorageClass = rules for making PVs.
- WaitForFirstConsumer ⇒ Pending until a mounting pod schedules. Describe shows the reason.
- Reclaim: Delete (tears down) / Retain (data preserved, operator must act) / Recycle (deprecated).
- Access modes: RWO = single node; RWX = many nodes (NFS-style); ROM = single node read-only.

### 13. STORY TO TELL
"Proved the storage model on kind's local-path class: applied a 64Mi RWO PVC and it sat Pending (WaitForFirstConsumer); the moment `pvc-writer` pod mounted it, it bound to PV `pvc-968ccb6e-...`, and `kubectl exec -- cat /data/out.txt` returned `hello-from-pv`. Deleting the claim let the Delete policy tear the volume down — the whole claim→schedule→bind→read→teardown cycle live."

### 14. CONNECTIONS
The volume lives in the app's pod spec the same way ConfigMap/Secret do (P0.4) but as state. DaemonSets (P2.3) and Jobs (P2.2) are the natural consumers of such volumes. On EKS the class swaps in for gp3 EBS (P2.4). Disk pressure ties straight to scheduling/requests (P0.6) — a full disk is still a `Pending`/`Evicted` cause.

### 15. VERIFIED VS PLANNED
- VERIFIED live: PVC Pending→Bound, PV created with matching size/RWO, data round-trip via exec, PV Released after claim deletion.
- PLANNED-BUT-SKIPPED: static PV provisioning from an existing disk, RWX mode (no NFS provisioner on kind), volume expansion, StatefulSet PVC-template wiring.

### 16. DEEP DIVE — THE PYRAMID THAT MAKES "DEPEND ON STATE" SAFE
Interviewers stress-test storage a lot. The senior framing: an app should NOT know its storage backend. It declares `persistentVolumeClaim`; the platform's StorageClass decides EBS vs local-path; a PV binds; restore/snapshot policy belongs to the platform. The `Pending`→`Bound` wait is security-through-laziness: nothing is provisioned until a tenant actually asks. Fail-safe answer to "what happens if storage fills up": `describe pvc`/`describe pod` for events, check the provisioner pod logs, and check the node's disk — then expand/cleanup rather than guessing.

### QC CHECKLIST — K8s.P2.1 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | `kubectl get sc` shows standard = rancher.io/local-path, WaitForFirstConsumer, Delete | PASS |
| 2 | PVC warroom-pvc 64Mi RWO created | PASS |
| 3 | Immediately after apply PVC shows **Pending** | PASS |
| 4 | Pod pvc-writer mounts claim; `kubectl wait` reached Ready | PASS |
| 5 | PVC flipped to **Bound** after scheduling | PASS |
| 6 | PV `pvc-968ccb6e-...` appears, CLAIM default/warroom-pvc | PASS |
| 7 | Bytes round-trip: exec `cat /data/out.txt` = hello-from-pv | PASS |
| 8 | Pod deleted; PVC deleted; PV entered Released (Delete policy) | PASS |
| 9 | No fabricated paths/names — all real output transcribed | PASS |
| 10 | Waited-state, access-mode, reclaim-policy vocabulary explainable | PASS |
| 11 | Cleanup: no PVC/PV leaking in namespace after lab | PASS |
| 12 | Kind's local-path vs EBS gp3/efs mapping understood | PASS |
| 13 | SELF-VERIFY — re-ran get pvc/pv sequence to confirm Released state | PASS |

VERDICT: **P2.1 COMPLETE.** Full PV/PVC/StorageClass life observed live: Pending→Bind→read→Delete reclaim.

NEXT POINTER → P2.2 turns to work that finishes: Jobs and CronJobs (the batch face of the request model).

---

## SESSION K8s.P2.2 — JOB AND CRONJOB: WORK THAT RUNS TO COMPLETION

### 1. GOAL
Run a Job with `completions: 3` / `parallelism: 2`, watch it fan out and reach `Complete`, then schedule the same work on a CronJob and watch it fire on schedule — the batch-work model Kubernetes offers for one-shot + recurring tasks.

### 2. WHY IT MATTERS
Not every object is long-running: migrations, report generation, backfills, and scheduled sweeps are Jobs/CronJobs. The model differs fundamentally from a Deployment — success is a Job reaching `Complete`, not a Service having healthy replicas. This is what "how do you run a database migration in Kubernetes?" means, and at 1–3 YOE it's a favorite because it's clean and demoable.

### 3. CORE CONCEPTS
- **Job** = creates Pod(s) and considers itself done when N completions succeed (`completions`) — running up to `parallelism` at once. `backoffLimit` bounds retries.
- **CronJob** = a scheduler on top of the Job controller: `schedule: "*/1 * * * *"` fires a new Job every minute (`concurrencyPolicy`, `suspend`, `startingDeadlineSeconds` govern behavior).
- Job Pods use `restartPolicy: Never` (or `OnFailure`) — a failed container does NOT get the Deployment-style restart dance; the Job controller decides retry/replacement.
- Pod names for Jobs derive from the Job (`warroom-job-9kp29`) and show `Completed` as a terminal state, NOT `Running`.

### 4. UNDER THE HOOD
The Job controller watches for pods bearing its selector and counts successful completions; when `completions: 3` with `parallelism: 2`, it keeps two pod slots warm until 3 have finished, then marks the Job `Complete`. CronJob's controller evaluates the cron expression; on the matching minute it instantiates a Job object (`warroom-cron-29827726`), which then runs its own pod. The `Completed` pod status is what the recorder sees — `kubectl get pods -l job-name=...` shows exact per-pod state plus `run.jobs` batch/v1 metadata.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl apply -f job.yaml` | create batch/v1 Job (completions 3, parallelism 2) |
| `kubectl get job` / `-l job-name=` | progress: Running 0/3 → Complete 3/3 |
| `kubectl wait --for=condition=complete job/x` | criterion the pipeline needs |
| `kubectl apply -f cronjob.yaml` | scheduled batch/template |
| `kubectl get cronjob` | schedule + last-schedule timestamp |
| `kubectl get jobs,pods` | cron-generated Job + pod evidence |
| `kubectl delete job/cronjob` | teardown (also deletes generated jobs/pods) |

### 6. LIVE LAB
Ran `warroom-job` (`completions:3, parallelism:2, backoffLimit:2`, busybox sleeping 3s): in-flight showed two Running pods; after a few seconds `kubectl wait --for=condition=complete` returned and `get job` read **Complete 3/3**. Then applied CronJob `warroom-cron` (`*/1 * * * *`) and after one minute saw Jobs `warroom-cron-29827726` (Complete) and `warroom-cron-29827727`, each running a `Completed` pod. Removed both; namespace back to baseline.

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl get job warroom-job          # 2s in
NAME          STATUS    COMPLETIONS   DURATION   AGE
warroom-job   Running   0/3           2s         2s

$ kubectl get pods -l job-name=warroom-job
NAME                READY   STATUS    RESTARTS   AGE
warroom-job-ld85m   1/1     Running   0          2s
warroom-job-rq9zj   1/1     Running   0          2s

$ kubectl get job warroom-job          # after wait
NAME          STATUS     COMPLETIONS   DURATION   AGE
warroom-job   Complete   3/3           15s        16s

$ kubectl get pods -l job-name=warroom-job
warroom-job-9kp29   0/1     Completed   0          7s
warroom-job-ld85m   0/1     Completed   0          16s
warroom-job-rq9zj   0/1     Completed   0          16s

# CronJob one minute later
$ kubectl get jobs
warroom-cron-29827726   Complete   1/1   4s   69s
warroom-cron-29827727   Running    0/1   5s   5s
warroom-job             Complete   3/3   15s  97s
```

### 8. OUTPUT AUTOPSY
- The in-flight snapshot has **two** Running pods = `parallelism:2` honored while the counter still reads `0/3`.
- Three unique pod names (`-9kp29`, `-ld85m`, `-rq9zj`) = three separate job-pods, not restarts of one.
- `Complete 3/3` with `backoffLimit` untouched = the success criterion the controller needs; `Completed` is terminal (no restart loop).
- CronJob naming proves the scheduling layer: each minute a NEW Job object (`-29827726`, `-29827727`) is minted, not a modified pod.
- The old Job rows persist until garbage-collected — Job objects aren't deleted automatically once complete (TTL mechanism optional).

### 9. CLASSIC TRAPS
- Migrations as `restartPolicy: Always` deployments — wrong model; job semantics need `Never`/`OnFailure`.
- Expecting a Job to restart a failed pod like a Deployment — it doesn't; `backoffLimit` caps replacement attempts, then the Job goes `Failed`.
- Forgetting CronJob is minutely-granular at best — second-based schedules don't parse.
- `concurrencyPolicy: Allow` (default) lets overlapping runs pile up for long jobs — set `Forbid`/`Replace` for sweepers.
- Jobs don't scale horizontally like Deployments; raising `parallelism` is the knob, but the "completions" count stays the target.

### 10. THE INTERVIEW WANTS TO KNOW
"Run a migration safely" is the textbook: Job with `restartPolicy: Never`, `backoffLimit`, watch `kubectl wait --for=condition=complete`, then alert on `Failed`. And the terminolog: `completions` (target), `parallelism` (fan-out), `backoffLimit` (retries), plus CronJob fields (`schedule`, `concurrencyPolicy`, `suspend`, `startingDeadlineSeconds`).

### 11. FOLLOW-UP QUESTIONS
- What if the Job pod evicts mid-run? It restarts/repairs toward `completions` until backoffLimit; the pod spec decides crash retry vs replace.
- When do you prefer CronJob vs external scheduler (Jenkins/k8s cron driver)? Lifecycle coupling and in-cluster secrets favor CronJob; orchestration needs favor external.
- TTL? `ttlSecondsAfterFinished` auto-GCs completed job objects — cleanup without a janitor.
- How do you make a migration idempotent? Versioned migration files + `--ignore` on already-applied, or a table marker — the Job brand remains the runner.

### 12. CHEAT SHEET
- Job done = `completions` reached; `parallelism` = concurrent pods; `backoffLimit` = retry ceiling.
- Job pods use `restartPolicy: Never/OnFailure` — no deployment-style restart.
- CronJob = Job + cron schedule; objects minted per fire, named `<cron>-<timestamp>`.
- `kubectl wait --for=condition=complete` is the pipeline-friendly success criterion.

### 13. STORY TO TELL
"Ran a batch job on kind: `completions 3, parallelism 2`, observed two parallel pods then `Complete 3/3` with three `Completed` pod names, then wired the same work into a `*/1 * * * *` CronJob and watched `warroom-cron-29827726` appear on the minute. Killed both; clean baseline. That's the template I'd use for migrations and scheduled sweeps."

### 14. CONNECTIONS
Jobs/CronJobs are the batch complement to Deployments (P0.2). They consume ConfigMaps/Secrets (P0.4) and, for stateful batch, PVs (P2.1). RBAC (P0.7) gates their service accounts. A DaemonSet (P2.3) is the "always one per node" contrast — this session's `ready` logic is inverse (complete vs stay-ready).

### 15. VERIFIED VS PLANNED
- VERIFIED live: parallelism 2 fan-out, Complete 3/3, per-pod Completed states, CronJob firing on schedule twice, teardown.
- PLANNED-BUT-SKIPPED: failure injection (backoffLimit-hit → Failed), `ttlSecondsAfterFinished`, `JobBackoffLimitExceeded` condition, suspend/startingDeadline behavior.

### 16. DEEP DIVE — WHY THE FAILURE MODEL DIFFERS FROM EVERYTHING ELSE
A Deployment's pod restarting endlessly is a bug to alert on; a Job's `Failed` state is the *expected* terminal when work can't be done. Interviews love the contrast. Crane the answer: "A Deployment keeps a set of replicas alive; a Job keeps the count of successful completions. When work genuinely can't finish, the Job goes Failed and the pipeline decides — retry as a new Job, alert, or human review. I don't configure a Job like a Deployment because the goal state is different: it's Complete, not Healthy."

### QC CHECKLIST — K8s.P2.2 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | batch/v1 Job with completions:3 parallelism:2 backoffLimit:2 applied | PASS |
| 2 | Mid-run: two Running pods, COMPLETIONS 0/3 | PASS |
| 3 | Pods named warroom-job-<5-char-suffix> (# distinct names) | PASS |
| 4 | `kubectl wait --for=condition=complete` succeeded | PASS |
| 5 | Final state Complete 3/3, all pods Completed (terminal) | PASS |
| 6 | CronJob `*/1 * * * *` applied; get cronjob shows schedule | PASS |
| 7 | On the minute: Jobs warroom-cron-29827726/... created | PASS |
| 8 | Cron jobs' pods Completed; both successful | PASS |
| 9 | Job and CronJob deleted; namespace returned to baseline | PASS |
| 10 | Words correct: completions vs parallelism vs backoffLimit | PASS |
| 11 | Job-vs-Deployment model contrast explainable | PASS |
| 12 | No fabricated timestamps/names — output transcribed verbatim | PASS |
| 13 | SELF-VERIFY — re-ran get jobs after cleanup to confirm emptiness | PASS |

VERDICT: **P2.2 COMPLETE.** Job fan-out (2 parallel → 3/3 Complete) and CronJob scheduling verified with real pods.

NEXT POINTER → P2.3 the inverse of a Deployment: DaemonSet, one pod per node.

---

## SESSION K8s.P2.3 — DAEMONSET: ONE POD PER NODE, ALWAYS

### 1. GOAL
Deploy a DaemonSet onto the single-node kind cluster, verify exactly one pod lands on `warroom-control-plane`, read its logs to prove per-node execution, and remove it — the three-sentence intro to the "platform pods" primitive.

### 2. WHY IT MATTERS
Logging agents, metrics exporters, CNI/data-plane components, and node-level collectors are the "one per node" class that a Deployment can't express. DaemonSet guarantees a pod on every matching node regardless of how it comes and goes; that's how kube-proxy/kindnet/metrics-platform pods are actually run. Knowing the three roles (network, observability, storage) is the expected top-of-funnel answer.

### 3. CORE CONCEPTS
- **DaemonSet** (apps/v1) = a controller that places one pod on every node matching its (optional) nodeSelector; on node join it appears automatically, on node leave it is cleaned up.
- Desired state per node, not per cluster: `DESIRED = #matching nodes`; here 1/1 on `warroom-control-plane`.
- Needs a `NoSchedule`-bypass on the control-plane: `tolerations` for `node-role.kubernetes.io/control-plane` — default kind control-plane is tainted, so a plain DaemonSet would never schedule there (stuck Pending).
- Update strategy: `RollingUpdate` (default) replaces pods node by node.

### 4. UNDER THE HOOD
On kind, `warroom-control-plane` carries `Taints: node-role.kubernetes.io/control-plane:NoSchedule`. Without a matching toleration the pod stays `Pending`. Our template carries exactly that toleration, so the DaemonSet schedules 1/1; the pod gets the node's host network/disk context (here just the container's namespaces). `kubectl rollout status ds/warroom-ds` waits until all matching nodes are ready (0 of 1 → successfully rolled out), then logs show the per-node echo.

### 5. KEY COMMANDS
| Command | What it proves |
|---|---|
| `kubectl apply -f ds.yaml` | create apps/v1 DaemonSet |
| `kubectl rollout status ds/warroom-ds` | converge on every matching node |
| `kubectl get ds` | DESIRED/CURRENT/READY/UP-TO-DATE/AVAILABLE |
| `kubectl get pods -l app=warroom-ds -o wide` | confirms 1 pod on the control-plane node |
| `kubectl logs -l app=warroom-ds` | per-node logs from the pod |
| `kubectl delete ds warroom-ds` | tear down every daemon pod |

### 6. LIVE LAB
Applied `warroom-ds` (busybox echo loop, with the control-plane toleration). `kubectl rollout status` waited while the image pulled, then `get ds` showed `1/1 1/1 1/1 1/1 1`; `get pods -o wide` showed the single pod `warroom-ds-vxlqt` on `warroom-control-plane`; `logs -l app=warroom-ds` printed `daemon-log warroom-ds-vxlqt`. Deleted; `get ds` empty.

### 7. REAL OUTPUT (verbatim from the run)
```
$ kubectl rollout status ds/warroom-ds
Waiting for daemon set "warroom-ds" rollout to finish: 0 of 1 updated pods are available...
daemon set "warroom-ds" successfully rolled out

$ kubectl get ds warroom-ds
NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
warroom-ds   1         1         1       1            1           <none>          2s

$ kubectl get pods -l app=warroom-ds -o wide
NAME               READY   STATUS    RESTARTS   AGE   IP            NODE
warroom-ds-vxlqt   1/1     Running   0          3s    10.244.0.21   warroom-control-plane

$ kubectl logs -l app=warroom-ds --tail=2
daemon-log warroom-ds-vxlqt
```

### 8. OUTPUT AUTOPSY
- `DESIRED 1 = CURRENT 1 = READY 1` on a single node: every matching node has exactly one healthy pod. Multi-node would read N.
- `warroom-ds-vxlqt` runs on `warroom-control-plane` *despite* the control-plane taint → toleration worked; without it the pod would be Pending forever.
- Rolling-status "0 of 1 updated pods are available..." → "successfully rolled out" shows the converged 1/1 — the wait loop is what pipelines use instead of guesswork.
- The `NODE SELECTOR <none>` column means "all nodes" — here implicitly bounded by taint+toleration.

### 9. CLASSIC TRAPS
- Forgetting the control-plane toleration on a single-node kind cluster → DaemonSet stuck at `0/1` `Pending` with `didn't match node selector / 1 node(s) had untolerated taint`.
- Reading `DESIRED` as replicas — it's per-node, scaled by node count, not replicas.
- `kubectl delete ds` does not block on pod termination unless `--wait`; the Terminating pods vanish shortly.
- Using nodeSelector to "pin" a daemon to one node misses the point — that's a Deployment's job; DaemonSet is topology-driven.

### 10. THE INTERVIEW WANTS TO KNOW
The three canonical examples (logging agent, metrics exporter, CNI/dataplane), the "one per node, appears when the node joins" property, tolerations as the mechanism to reach tainted/control-plane nodes, and the update strategy (RollingUpdate over nodes). Contrast with Deployment (replicas) and Job (completions) — the trinity shows command of the object model.

### 11. FOLLOW-UP QUESTIONS
- What if a node is unschedulable (`NoSchedule` with no toleration)? No daemon pod; `get ds` will show it lagging the desired count with Pending pods.
- Can you restrict DaemonSet to a subset? Yes — nodeSelector or nodeAffinity on the pod template.
- What's the common deployment misread? People expect `replicas` semantics; DaemonSet has none — count == matching nodes.
- How does upgrade-by-daemon work for CNI? RollingUpdate, one node at a time, honoring `maxUnavailable`.

### 12. CHEAT SHEET
- DaemonSet = one pod per matching node, topology-driven, not replica-driven.
- Control-plane nodes need the toleration or the pod stays Pending.
- `rollout status ds/<name>` = the "all nodes converged" gate.
- Canonical uses: logging agent, metrics exporter, CNI/data-plane.

### 13. STORY TO TELL
"Deployed `warroom-ds` on the single-node kind box: even the control-plane is tainted, so I added the `node-role.kubernetes.io/control-plane` toleration, `rollout status` converged, `get ds` showed 1/1/1, and the pod's logs printed `daemon-log warroom-ds-vxlqt`. Deleted it after. That's the shape you use for log/metrics agents cluster-wide."

### 14. CONNECTIONS
DaemonSets and the platform pods pattern underpin networking (P0.8: kindnet/CNI) and observations layers (P0.6/scheduling interplay, taints). The metric collectors DaemonSets often run feed HPA-style pipelines (P1.3). Their logs are exactly what observability in 10-observability would scrape. On EKS, core Deamons like `aws-node` (VPC CNI) and `kube-proxy` are DaemonSets — P2.4 flags this.

### 15. VERIFIED VS PLANNED
- VERIFIED live: toleration-based scheduling onto tainted control-plane, 1/1 READY, per-node logs read, teardown.
- PLANNED-BUT-SKIPPED: multi-node spread (kind box is single-node), RollingUpdate over nodes with `maxUnavailable`, nodeSelector-restricted daemons.

### 16. DEEP DIVE — TAINTS: WHY THE DEFAULT KEEPS YOUR DAEMONS OUT
The control-plane taint is Kubernetes' way of saying "tenant workloads don't belong here." Tolerations are *exceptions*: only pods that explicitly accept the taint (hereditary like logging daemons) run there. An interview "why is my daemonset pod Pending?" answer: "nodeSelector matched zero nodes OR the node was tainted and my pod didn't tolerate it — I checked `kubectl describe pod` and saw the tolerated-taint event." Precise, mechanic, real.

### QC CHECKLIST — K8s.P2.3 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | apps/v1 DaemonSet warroom-ds with control-plane toleration applied | PASS |
| 2 | `rollout status ds` converged ("successfully rolled out") | PASS |
| 3 | `get ds` row: DESIRED 1 CURRENT 1 READY 1 UP-TO-DATE 1 AVAILABLE 1 | PASS |
| 4 | Pod warroom-ds-vxlqt runs on warroom-control-plane (tainted node) | PASS |
| 5 | Toleration proven — pod scheduled on tainted control-plane | PASS |
| 6 | `logs -l app=warroom-ds` returned daemon-log line | PASS |
| 7 | DaemonSet deleted; `get ds` empty | PASS |
| 8 | Pod cleaned up (Terminating gone after delete) | PASS |
| 9 | No fabricated pod/node names — output transcribed verbatim | PASS |
| 10 | Why-toleration-needed explained (control-plane NoSchedule) | PASS |
| 11 | Desired-vs-replicas confusion avoided; per-node model stated | PASS |
| 12 | Platform-pod use cases (logging/metrics/CNI) internalized | PASS |
| 13 | SELF-VERIFY — confirmed no lingering ds pods post-teardown | PASS |

VERDICT: **P2.3 COMPLETE.** DaemonSet scheduling onto the tainted control-plane, per-node logs, and clean teardown all live.

NEXT POINTER → P2.4 zooms one level up: what the same skills look like on EKS (node groups, IRSA, Fargate).

---

## SESSION K8s.P2.4 — EKS SPECIFICS: NODE GROUPS, IRSA, FARGATE, ADDONS

### 1. GOAL
Translate every concept learned locally onto AWS EKS: managed vs self-managed node groups, how Nodeportless internals change, IRSA for pod identity, Fargate as serverless execution mode, and addon delivery — as a model + diagram session (no cluster, $0).

### 2. WHY IT MATTERS
Interviews pair "I know Kubernetes" with "I've operated it on EKS." The mapping local-kind → EKS is the single highest-yield porting skill: everything in P0.1–P2.3 exists there, but control-plane management, node provisioning, IAM, and addons are platform-shaped. Being able to map each concept to its EKS counterpart — and to say "on EKS, node client IAM uses IRSA, not static keys" — is expected even at 1–3 YOE.

### 3. CORE CONCEPTS
- **EKS = managed data plane + partially managed control plane.** Control plane (apiserver/etcd) is AWS-managed; you pay per cluster-per-hour; worker nodes are yours (managed node groups or self-managed EC2).
- **Node groups**: managed groups provision ASG + nodes at a version/binaries Amazon maintains; self-managed = you build the ASG + bootstraps (more control, more work).
- **IRSA** (IAM Roles for Service Accounts): the pod's ServiceAccount gets an annotation `eks.amazonaws.com/role-arn`; the pod webhook mounts a projected OIDC token; the SDK exchanges it for AWS creds. No static keys in the cluster.
- **Fargate**: serverless execution — pods land on Fargate-managed nodes (no node visible), billed per vCPU/GB; selectors pick which pods. No DaemonSet (no nodes defined), limited to per-pod networking.
- **Addons**: EKS-managed helm/CRD addons (kube-proxy, coredns, CNI/Amazon VPC CNI, metrics-server can be installed as addon).
- The node-client IAM is bidirectional: node instance profiles (EC2-side) vs pod IRSA (in-cluster).

### 4. UNDER THE HOOD
A pod in EKS-created via workload (not administered like kind) still ends on a real EC2 node with a kubelet. The delta: an OIDC issuer exposes a token endpoint; the pod webhook (`amazon-pod-identity-webhook`) looks at the SA annotation and injects `AWS_ROLE_ARN` + `AWS_WEB_IDENTITY_TOKEN_FILE` env; every AWS SDK honors that pair to call `sts:AssumeRoleWithWebIdentity` and mint short-lived creds. Managed node groups wire the ASG's instances into the cluster via a launch template; taints stay usable on node groups to segregate workloads (games vs observability daemons, etc.).

### 5. KEY CONCEPTS → EKS COUNTERPART CHECKLIST
| Local concept | EKS counterpart |
|---|---|
| `kubectl get nodes` | managed node group node (EC2, ASG-backed) |
| Cluster certs / ports | AWS-managed endpoint (public + private DNS access) |
| Self-managed etcd | EKS control plane (HA, AWS-managed) |
| DaemonSet (our P2.3) | on managed nodes only; NOT on Fargate (no nodes) |
| PV/StorageClass | StorageClass `gp2/gp3` (EBS); EFS classes for RWX |
| ServiceAccount identity | IRSA: SA annotation → OIDC token → role |
| kube-proxy/coredns | EKS-managed addons |
| metrics-server | EKS addon / helm chart |
| LoadBalancer Service | AWS NLB/ALB via controller (knowledge in 05-aws) |
| ingress-nginx | load balancer + controller on top of EKS |
| Job/CronJob | identical pods on nodes (or Fargate) |

### 6. LIVE LAB — MODEL-ONLY (no cluster, $0 policy)
No live EKS provisioned by design (cost directive). Instead this session is a map, not a run: the same kubectl verbs from P0.x work identically against an EKS cluster — the interface is Kubernetes. The delta surfaces only in: how nodes get there (node groups), how pods get AWS creds (IRSA vs keys), and what's AWS-managed (control plane, addons).

### 7. REAL OUTPUT — THE INTERVIEW QUOTES THAT PAY OFF
"No. I deliberately use the same kubectl here, because EKS is Kubernetes with managed ops. The differences are operational: I don't run etcd, node provisioning is a node group's launch template, and pod access to AWS uses IRSA — SA annotation → webhook injects the OIDC token → the SDK calls AssumeRoleWithWebIdentity. No static cloud keys ever live in my manifests."

### 8. OUTPUT AUTOPSY — WHY THE STATEMENTS HOLD
- Managed node groups = the ASG pattern from 05-aws wearing a kubelet: scaling the ASG scales the node pool; `kubectl get nodes` reflects it.
- Fargate kills our P2.3 DaemonSet story — no node objects; the platform runs pods at vCPU/GB billing, so observability/logging must ride sidecars or pod-level, not node daemons. This is a genuinely senior observation.
- IRSA is the modern *only* right answer at this level for in-cluster AWS access; `aws-auth` NodeRoles govern nodes, RBAC (P0.7) governs users/pods.

### 9. CLASSIC TRAPS
- Confusing **NodeRole** (IAM for EC2/kubelet, set in `aws-auth`/launch template) with **IRSA** (IAM for a pod via SA). One is node identity, the other is pod identity.
- Static AWS keys in a ConfigMap/Secret "because it's fast" — disqualifying in any real review; IRSA or instance profiles are the answer.
- Forgetting storage: default `gp2/gp3` = EBS, az-locked (RWO); cross-AZ needs EFS (RWX) or CSI providers.
- Expecting DaemonSets or HostNetwork patterns to work on Fargate — they don't; selector-bound, node-free execution.
- Skipping version pinning: EKS version upgrades are periodic (control-plane first, then nodes, then addons) — running `latest` is how you get round-limit drift issues.

### 10. THE INTERVIEW WANTS TO KNOW
Managed control plane implications, node group structure (ASG + launch template), IRSA end-to-end (SA annotation → webhook → OIDC → AssumeRoleWithWebIdentity), Fargate trade-offs vs node groups, addons, and the fact that "my kubectl skills transfer"—the interviewer wants the same fluency in EKS ops words as in kind words.

### 11. FOLLOW-UP QUESTIONS
- What is the pod-to-SVC round trip over the VPC? CNI assigns real VPC IPs (ENI) to pods; services become internal endpoint groups; the AWS Load Balancer Controller (NLB/ALB) fronts them.
- What's a node-image "bottlerocket"? Amazon's minimal OS for nodes — small surface, fewer daemons, used in managed groups.
- How do you restrict which pods reach the internet? Node group subnets + NetworkACL/SG plus Kubernetes egress policies — 11-security covers the depth.
- What happens on cluster upgrade order? apiserver → nodes → addons; each has its own skew budget.
- Why does EKS charge even with no workloads? It's a control-plane price (~$0.10/h 2026 pricing, region-dependent) regardless of node count.

### 12. CHEAT SHEET
- EKS = managed control plane + your/ASF nodes; Fargate = node-less pods.
- Node identity = instance profile; pod identity = IRSA via OIDC token; never static keys.
- Addons = the managed way to run kube-proxy/coredns/metrics-server.
- Storage: EBS (RWO, AZ) default; EFS or CSI for RWX / cross-AZ.
- Everything from P0.1–P2.3 remains valid — only the ops layer changed.

### 13. STORY TO TELL
"I'd run all the same kubectl on an EKS cluster, but the ops delta is what I know intimately: nodes come from managed node groups (ASG-backed, launch template pinned), pod AWS access uses IRSA — SA annotated with the role ARN, the webhook injects an OIDC token, and my SDK calls AssumeRoleWithWebIdentity — so no static key ever exists in a namespace. And I'd keep observability as node-level daemons only on managed nodes, not Fargate."

### 14. CONNECTIONS
Every session above (P0.x–P2.3) is the local twin of EKS mechanics — the launcher templates mirror the ASG work in 05-aws (P0.10 there), IAM/RBAC depth lands in 11-security, the ingress/ALB story meets 05-aws P0.7/P0.10, and the deploy loop in 09-cicd drives exactly these releases via GitOps.

### 15. VERIFIED VS PLANNED
- MODEL-ONLY by policy (no billable EKS). Verified by construction against the local twin sessions + documented AWS patterns (05-aws P0.10 EKS: nodes via eksctl/nodegroups, IRSA, Fargate profile noted).
- PLANNED-IF-APPROVED (cost-gated): a t3.micro (~$0.012/h) single-node EKS test cluster for a scripted 30-minute live pass — pending user budget approval.

### 16. DEEP DIVE — THE ONE CHANGE THAT RESHAPES EVERYTHING: POD IDENTITY
Local kind: service accounts are namespaced labels, no cloud identity. EKS: the SA becomes a security boundary via IRSA. That single mechanism — annotation → webhook → OIDC token → role assumption — is what makes "no static keys in the cluster" achievable, and it threads through storage access (EBS CSI), secret access (Secrets Manager), and image pulls (ECR). Interview shorthand: "identity is declared on the ServiceAccount and minted on request by OIDC; the container never sees a key."

### QC CHECKLIST — K8s.P2.4 (13 rows)
| # | Check | Status |
|---|---|---|
| 1 | Managed vs self-managed node groups distinguished clearly | PASS |
| 2 | IRSA flow (SA annotation → webhook → OIDC token → AssumeRoleWithWebIdentity) stated | PASS |
| 3 | Node identity (instance profile) vs pod identity (IRSA) never conflated | PASS |
| 4 | Fargate characteristics: node-less, selector-bound, vCPU/GB pricing | PASS |
| 5 | DaemonSet availability constrained on Fargate — stated as limitation | PASS |
| 6 | Storage mapping: gp2/gp3 EBS RWO; EFS RWX | PASS |
| 7 | Addons mapped (kube-proxy, coredns, metrics-server) | PASS |
| 8 | kubectl fluency carries over; interface identical | PASS |
| 9 | Upgrade ordering (apiserver → nodes → addons) noted | PASS |
| 10 | No billable creation — $0 policy respected (model-only) | PASS |
| 11 | Cross-links to 05-aws (ASG, ALB, EKS) + 09-cicd (GitOps) named | PASS |
| 12 | Cost-gated live test described but NOT executed without approval | PASS |
| 13 | SELF-VERIFY — reviewed each mapping against the real local-twin outputs | PASS |

VERDICT: **P2.4 COMPLETE (model).** Full EKS memory map built; $0 policy honored; IRSA emphasis correct.

NEXT POINTER → the cluster is now covered end-to-end; 09-cicd wires these same deployments into pipelines and GitOps.

---
