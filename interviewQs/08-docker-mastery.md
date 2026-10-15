# Docker & Container Internals Mastery — Interview Engineering Guide

This guide covers the 12 core containerization, runtime troubleshooting, and Docker architecture interview questions (Section 7 of the Cloud & DevOps curriculum). Answers are formulated from an enterprise SRE / Platform Engineering perspective, focusing on Linux kernel primitives (cgroups, namespaces, copy-on-write storage), signal propagation, and production failure modes.

---

## Question Index

| # | Topic | Key SRE Focus |
| :--- | :--- | :--- |
| **7.1** | Container Exits Immediately | PID 1 lifecycle, foreground vs background execution, `daemon off;` |
| **7.2** | Purpose of `EXPOSE` in Dockerfile | Metadata documentation vs runtime `-p` network namespace DNAT |
| **7.3** | Port Not Accessible on Localhost | `127.0.0.1` vs `0.0.0.0` socket binding, iptables bridge routing |
| **7.4** | Data Persistence Across Lifecycle | UnionFS copy-on-write ephemeral layer vs Docker volumes / bind mounts |
| **7.5** | Build Cache Invalidation | Docker layer caching heuristics, `COPY` ordering, build arguments |
| **7.6** | Permission Denied Inside Container | Linux UID/GID namespace mappings, rootless containers, file mode bits |
| **7.7** | Host Disk Space Exhaustion | `docker system prune`, dangling layers, container log driver rotation |
| **7.8** | Live Container Debugging | `docker exec`, `nsenter`, ephemeral debug containers, `/proc` inspection |
| **7.9** | Container Registry Architecture | ECR/GHCR/Harbor, immutable image tags, pull-through cache, vulnerability scanning |
| **7.10** | `CMD` vs `ENTRYPOINT` Mechanics | Exec form vs shell form, parameter concatenation, signal interception |
| **7.11** | Core Day-to-Day Docker Operations | Essential operational and investigative CLI commands |
| **7.12** | Forceful Container Termination | `SIGTERM` vs `SIGKILL` (137 exit code), graceful shutdown, kernel D-state hangs |

---

### Question 7.1: A container exits immediately upon start. How do you troubleshoot and fix it?

#### Production Reality & Failure Mechanism
A Docker container is not a virtual machine; it is an isolated set of Linux processes bounded by kernel namespaces and cgroups. A container remains in the `running` state **if and only if** its designated root process (PID 1) remains active in the foreground.

If the entrypoint script spawns a background daemon (e.g., `systemctl start nginx`, `service mysql start`, or a script ending with `&`) and exits, PID 1 terminates. When PID 1 exits, the Linux kernel terminates the container's PID namespace, transitioning the container to `Exited (0)` or `Exited (1)`.

#### Step-by-Step Triage Workflow

1. Inspect Exit Code and State:
   ```bash
   docker ps -a --filter "status=exited"
   docker inspect <container_id> --format '{{.State.ExitCode}} | Error: {{.State.Error}}'
   ```
2. Extract the Process Output:
   ```bash
   # Check stdout and stderr streams of the deceased PID 1
   docker logs <container_id> --tail 50
   ```
3. Run Interactively with an Overridden Entrypoint:
   If the container fails before logging anything, override the entrypoint to launch a basic shell:
   ```bash
   docker run -it --rm --entrypoint /bin/sh <image_name>
   ```

#### Common Root Causes and Fixes
- Backgrounded Daemons: For services like Nginx or Apache, ensure they run in the foreground:
  ```dockerfile
  # Incorrect (exits immediately)
  CMD service nginx start

  # Correct (blocks PID 1 in foreground)
  CMD ["nginx", "-g", "daemon off;"]
  ```
- Missing Script Shebang or Executable Bits: An entrypoint script lacking `chmod +x` or lacking `#!/bin/sh` yields `exec: "entrypoint.sh": permission denied` or `file not found`.
- Missing Environment Variables / Secret Dependencies: If the binary expects required environment variables (e.g., `DATABASE_URL`) and panics on startup, it exits with non-zero exit codes.

---

### Question 7.2: What is the exact purpose of `EXPOSE` in a Dockerfile? Does it publish the port?

#### The Critical Distinction
`EXPOSE` does **not** publish ports, nor does it configure packet filtering rules on the host network.

`EXPOSE` functions purely as **architectural documentation and metadata** between the image author and the image consumer.

```
+-------------------------------------------------------------+
| Dockerfile: EXPOSE 8080                                      |
| -> Writes metadata: {"ExposedPorts": {"8080/tcp": {}}}       |
| -> NO iptables rules created. Port UNREACHABLE from host.    |
+-------------------------------------------------------------+
                              vs
+-------------------------------------------------------------+
| Runtime: docker run -p 80:8080                               |
| -> Creates host iptables DNAT rule:                          |
|    Host 0.0.0.0:80 ---> Container IP:8080                    |
| -> Port ACTIVE and accessible externally.                    |
+-------------------------------------------------------------+
```

#### Behavioral Details
- If you run `docker run -d my-app` (where the image contains `EXPOSE 8080`), port 8080 is accessible only to other containers connected to the same bridge network via the container's private IP. It is completely inaccessible from the host's localhost or public interface.
- If you run `docker run -P my-app` (capital `-P`), Docker inspects all `EXPOSE` directives in the image metadata and dynamically maps each exposed port to a random high-order ephemeral port on the host (e.g., `32768-60999`).
- Explicit binding with `-p <host_port>:<container_port>` works **even if the Dockerfile does not have an `EXPOSE` directive**.

---

### Question 7.3: The port is mapped (`-p 8080:8080`), but the service is inaccessible on localhost. What is wrong?

#### The `127.0.0.1` vs `0.0.0.0` Upstream Binding Trap
This is the most common microservice networking bug in containerization.

When an application server (Node.js Express, Python Flask/FastAPI, Go HTTP server) starts inside the container, it binds to a network interface:
- If the application code binds to `localhost` or `127.0.0.1`:
  It binds **exclusively to the container's loopback interface (`lo`)**.
  Traffic originating from the host passes through the Docker bridge network (`docker0`) and arrives at the container's virtual ethernet interface (`eth0`). Because the application is listening only on `lo`, the kernel drops the packet and responds with `Connection Refused`.
- The Fix: The application inside the container must bind to all interfaces (`0.0.0.0` or `::` for IPv6):
  ```python
  # Broken inside Docker
  app.run(host="127.0.0.1", port=8080)

  # Correct for Docker
  app.run(host="0.0.0.0", port=8080)
  ```

#### Other Diagnostic Vectors
1. Check Listening Sockets Inside Container:
   ```bash
   docker exec -it <container_id> netstat -tlpn
   # or
   docker exec -it <container_id> ss -tulpn
   # Ensure it shows 0.0.0.0:8080, NOT 127.0.0.1:8080
   ```
2. Verify Host iptables DNAT Forwarding:
   ```bash
   iptables -t nat -L DOCKER -n -v
   # Verify packet counter increments when sending curl requests
   ```
3. Host Firewall (`ufw` or `firewalld`): Some enterprise Linux hosts drop bridged Docker traffic if `net.ipv4.ip_forward` is disabled in `/etc/sysctl.conf`.

---

### Question 7.4: When a container stops, its data is lost. How does container storage work, and how do you ensure persistence?

#### Container Storage Architecture: Storage Drivers & CoW
Every container uses a Copy-on-Write (CoW) storage driver (typically `overlay2` on modern Linux):
1. Image Layers (Read-Only): Immutable layers shared across all containers running the same image.
2. Container Layer (Read-Write / Ephemeral): A thin, writable scratch layer created on top of the image stack when the container boots.
   - When files are written or modified, they are copied up from lower layers into this writable layer.
   - **Lifecycle:** When the container is destroyed (`docker rm`), this writable layer is deleted from the host filesystem (`/var/lib/docker/overlay2/`).

```
+-----------------------------------------------------------------+
| Writable Container Layer (Ephemeral: destroyed on 'docker rm')  |
+-----------------------------------------------------------------+
| Read-Only Image Layer N (Application code)                      |
+-----------------------------------------------------------------+
| Read-Only Image Layer 1 (Base OS / Ubuntu / Alpine)             |
+-----------------------------------------------------------------+
```

#### Production Persistence Mechanisms

1. Named Volumes (Managed by Docker):
   - Stored in `/var/lib/docker/volumes/<volume_name>/_data`.
   - Completely independent of the container lifecycle; preserved when containers are stopped, upgraded, or destroyed.
   - Managed via Docker API (`docker volume create`, `docker volume ls`).
   ```bash
   docker run -d -v postgres_data:/var/lib/postgresql/data postgres:16
   ```

2. Bind Mounts:
   - Mounts an explicit, absolute path from the host filesystem into the container (`/opt/app/config:/etc/app/config`).
   - Dependent on the host machine's directory structure and permissions. Common for configuration injection and local developer hot-reloading.
   ```bash
   docker run -d -v /data/mysql:/var/lib/mysql mysql:8.0
   ```

3. `tmpfs` Mounts:
   - Stored in host memory (RAM) only. Never written to the writable layer or host disk. Ideal for high-performance temporary caches or sensitive secrets.

---

### Question 7.5: Code changes are not reflected after rebuilding the Docker image. How does the build cache work, and how do you resolve this?

#### Docker Layer Caching Heuristics
During `docker build`, Docker evaluates each instruction in the Dockerfile from top to bottom:
- For non-`COPY` instructions (`RUN`, `ENV`): Docker checks if the exact string of the instruction matches an existing cached layer.
- For `COPY` / `ADD` instructions: Docker computes a checksum (hash) of the files being copied from the host context. If the checksum matches the cache, Docker skips execution and reuses the cached layer.
- **The Invalidation Cascade:** As soon as a single layer's cache is invalidated (e.g., source file modified), **all subsequent layers below it are forcibly re-executed**.

#### Why Code Changes Are Missed (The Trap)
If source code is copied into the image *before* dependency installation, or if the build context excludes changed files:
1. `.dockerignore` Exclusion: The developer edited files that are matched by a rule in `.dockerignore`.
2. Wrong Instruction Order: Copying the entire directory before downloading dependencies causes expensive cache misses on every minor edit:
   ```dockerfile
   # Anti-pattern: Invalidates dependency cache on every single line of code edited
   COPY . /app
   RUN npm install

   # Enterprise Best Practice: Layer Caching Optimization
   COPY package.json package-lock.json /app/
   RUN npm ci  # Cached unless package-lock.json changes
   COPY . /app # Fast cache invalidation for application logic only
   ```
3. Resolving Forcefully:
   ```bash
   # Force fresh rebuild bypassing all cached intermediate layers
   docker build --no-cache -t my-app:v2 .
   ```

---

### Question 7.6: You encounter "Permission Denied" errors inside a container accessing mounted files. What is the cause and resolution?

#### Cause: Linux UID/GID Namespace Reality
Containers share the host kernel. By default, user namespaces are not remapped:
- A process running as user `node` inside the container with UID `1000` is seen by the host Linux kernel as UID `1000`.
- If a bind mount on the host (`/data/uploads`) is owned by host user `root` (UID `0`) with permissions `drwxr-xr-x` (755), and the container process runs as UID `1000`, the container process cannot write to that directory, triggering `EACCES: permission denied`.

#### Enterprise Resolutions

1. Match UID/GID at Runtime:
   Pass the host user's UID and GID dynamically when launching the container:
   ```bash
   docker run -u $(id -u):$(id -g) -v $(pwd)/data:/app/data my-image
   ```

2. Establish Non-Root Users in Multi-Stage Builds:
   Create a dedicated system user and set appropriate ownership before switching contexts:
   ```dockerfile
   FROM node:20-alpine
   WORKDIR /app
   RUN addgroup -S appgroup && adduser -S appuser -G appgroup
   COPY --chown=appuser:appgroup . /app
   USER appuser
   CMD ["node", "server.js"]
   ```

3. Enable Docker User Namespaces (`userns-remap`):
   Configure `/etc/docker/daemon.json` with `"userns-remap": "default"`. This translates container UID 0 (root) to an unprivileged high-range UID on the host (e.g., UID `100000`), protecting host files even if a container breakout occurs.

---

### Question 7.7: The Docker host is running out of disk space (`/var/lib/docker` 100% full). How do you safely remediate this?

#### Emergency Triage Order
When disk space hits 100%, Docker cannot create writable layers, pull new images, or even write container logs.

1. Inspect Disk Usage Breakdown:
   ```bash
   docker system df
   docker system df -v
   ```

2. Remove Dangling and Stopped Artifacts:
   ```bash
   # Removes stopped containers, dangling images, and unused build cache
   docker system prune -f

   # Comprehensive purge: removes all stopped containers, unused networks,
   # unused images (not just dangling), and build cache
   docker system prune -a --volumes -f
   ```
   *(Caution: `--volumes` will delete unattached volumes. Verify data persistence requirements before executing).*

3. Clean BuildKit Cache:
   ```bash
   docker builder prune -a -f
   ```

#### Preventing Recurrence: Container Log Rotation
In 80% of enterprise production outages, `/var/lib/docker/containers/<id>/<id>-json.log` consumes hundreds of gigabytes because log rotation was never configured.

Configure global log rotation in `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "3"
  }
}
```
Reload the daemon: `systemctl reload docker`.

---

### Question 7.8: How do you inspect and debug a live, running production container without disturbing the application?

#### The Troubleshooting Hierarchy

1. Execute a Process Inside the Container Namespace:
   ```bash
   docker exec -it <container_id> /bin/sh
   ```

2. What If the Image Has No Shell (`distroless` or `scratch`)?
   In secure, minimal images where `/bin/sh`, `curl`, and `netstat` are deliberately omitted:
   - Method A: Linux `nsenter` (Execute on host using container's PID):
     ```bash
     # Find container PID on host
     PID=$(docker inspect --format '{{.State.Pid}}' <container_id>)

     # Join container's network namespace using host binaries
     nsenter -t $PID -n ip a
     nsenter -t $PID -n netstat -tlpn
     nsenter -t $PID -n tcpdump -i eth0 port 80
     ```
   - Method B: Attach a Debug Container Sharing the Network Namespace:
     ```bash
     # Launch a network troubleshooting container sharing the target's network stack
     docker run -it --rm --network container:<target_container_id> nicolaka/netshoot
     ```

3. Real-Time Resource Monitoring:
   ```bash
   # Live CPU, memory, network I/O, and block I/O stream
   docker stats --no-stream
   ```

4. Process Tree Inspection:
   ```bash
   # View running processes within the container's PID namespace
   docker top <container_id>
   ```

---

### Question 7.9: How do you evaluate and select a container registry, and what security practices must be enforced?

#### Registry Landscape Comparison

| Feature | AWS ECR | GitHub Container Registry (GHCR) | Harbor (Self-Hosted) | Docker Hub |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Use Case** | AWS Cloud-native workloads | GitHub Actions CI/CD workflows | Enterprise on-prem / air-gapped | Open-source public sharing |
| **Authentication** | AWS IAM / IRSA / STS tokens | GitHub Personal Access Tokens / `GITHUB_TOKEN` | LDAP / OIDC / RBAC | Username / API Key |
| **Security Scanning** | Native AWS Inspector / Clair | GitHub Advanced Security | Trivy / Clair integration | Snyk integration |
| **Network Isolation** | AWS VPC Endpoints (PrivateLink) | Public endpoints | Internal corporate LAN / Private VPC | Public internet |

#### Mandatory Enterprise Registry Controls
1. Tag Immutability: Prevent overwriting mutable tags like `:latest` or `:v1.0.0`. Enforcing immutability prevents supply-chain tampering and guarantees that testing in staging accurately reflects what runs in production.
2. Automated Vulnerability Scanning on Push: Configure registries to trigger static vulnerability scans (CVE detection) automatically when an image is pushed. Block CI/CD pipeline promotions if `CRITICAL` CVEs are detected.
3. Lifecycle Expiration Policies: Automatically purge untagged images and non-production feature-branch tags older than 14 days to prevent storage bloat.
4. Pull-Through Caching: Deploy ECR Pull-Through Cache or Harbor replication to proxy external public registries (Docker Hub, Quay), shielding production from public rate limits and upstream registry outages.

---

### Question 7.10: What is the exact technical difference between `CMD` and `ENTRYPOINT` in a Dockerfile?

#### The Operating Principle
- `ENTRYPOINT`: Defines the **immutable executable** that is invoked when the container boots.
- `CMD`: Defines the **default parameters / arguments** passed to the `ENTRYPOINT`.

#### Exec Form vs Shell Form

| Form | Syntax | Process Hierarchy | Signal Handling |
| :--- | :--- | :--- | :--- |
| **Exec Form (Recommended)** | `ENTRYPOINT ["nginx", "-g", "daemon off;"]` | Target binary runs directly as **PID 1** | Direct `SIGTERM` reception; graceful shutdown works. |
| **Shell Form (Avoid)** | `ENTRYPOINT nginx -g "daemon off;"` | Executed as `/bin/sh -c "nginx ..."` | Shell runs as PID 1; child process does NOT receive `SIGTERM`. |

#### Combining `ENTRYPOINT` and `CMD` (The Gold Standard Pattern)
```dockerfile
# Immutable base executable
ENTRYPOINT ["python", "app.py"]

# Default parameters that can be overridden by the user at runtime
CMD ["--port", "8080", "--workers", "4"]
```

#### Runtime Execution Scenarios:
1. Running with defaults:
   ```bash
   docker run my-image
   # Executes: python app.py --port 8080 --workers 4
   ```
2. Overriding default arguments:
   ```bash
   docker run my-image --port 9090 --workers 8
   # Executes: python app.py --port 9090 --workers 8
   ```
3. Overriding the entrypoint completely:
   ```bash
   docker run --entrypoint /bin/sh my-image
   # Executes: /bin/sh
   ```

---

### Question 7.11: List the essential day-to-day Docker operational commands used in production troubleshooting.

#### Lifecycle & Execution
```bash
# Run detached container with memory limit and restart policy
docker run -d --name web --memory="512m" --restart=unless-stopped -p 80:80 nginx:alpine

# Execute non-invasive command inside container
docker exec -it web ps aux

# View resource utilization metrics across all containers
docker stats --no-stream
```

#### Inspection & Log Analysis
```bash
# Stream last 100 lines with timestamps
docker logs -f --tail 100 -t web

# Extract specific JSON attributes (e.g. IP address, health status)
docker inspect --format '{{.NetworkSettings.IPAddress}}' web
docker inspect --format '{{json .State.Health}}' web
```

#### Housekeeping & Maintenance
```bash
# Check filesystem utilization
docker system df

# Purge dangling images and build cache safely
docker image prune -f
docker builder prune -f
```

---

### Question 7.12: When and why would you use `docker kill` or `docker rm -f`? Explain Exit Code 137.

#### Termination Signals: `SIGTERM` vs `SIGKILL`
When stopping a container gracefully via `docker stop <container_id>`:
1. Docker sends `SIGTERM` (Signal 15) to the PID 1 process inside the container.
2. Docker starts a default grace period timer of **10 seconds**.
3. The application is expected to catch `SIGTERM`, stop accepting new inbound connections, flush pending database buffers, finish active requests, and terminate.
4. If the process terminates within 10 seconds, the container exits with code `0`.
5. If the timer expires and PID 1 is still running, Docker sends `SIGKILL` (Signal 9), which cannot be caught or ignored by any process.

#### The Origin of Exit Code 137
In Linux, when a process is killed by an unhandled signal, its exit code is calculated as:
$$\text{Exit Code} = 128 + \text{Signal Number}$$

Since `SIGKILL` is Signal `9`:
$$128 + 9 = 137$$

Therefore, **Exit Code 137 means the process was terminated forcibly by `SIGKILL`**.

#### The Two Causes of Exit Code 137:
1. Grace Period Timeout / Force Kill: `docker stop` timed out after 10 seconds and issued `SIGKILL`, or an operator executed `docker kill <id>` / `docker rm -f <id>`.
2. Linux Kernel OOM Killer: The container's memory footprint exceeded the cgroup memory limit (`--memory="512m"`). The Linux kernel Out-Of-Memory Killer immediately sent `SIGKILL` to the offending process.
   - Verify via inspect:
     ```bash
     docker inspect <container_id> --format '{{.State.OOMKilled}}'
     # Returns: true if killed by kernel cgroup memory exhaustion
     ```

#### When Is `docker rm -f` Appropriate?
- Development / Test Environments: Rapidly destroying scratch environments without waiting for 10-second timeout loops.
- Frozen Processes: When an application is stuck in an infinite CPU loop or deadlocked thread and fails to respond to `SIGTERM`.
- **Warning in Production:** `docker rm -f` or `docker kill` should never be the default operating procedure for databases (PostgreSQL, MySQL) or queue workers (Kafka, Redis), as sudden termination risks in-flight write corruption and uncommitted transaction aborts.
