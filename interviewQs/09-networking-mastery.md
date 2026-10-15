# Cloud & Systems Networking Mastery — Interview Engineering Guide

This guide covers the 9 core networking and troubleshooting interview questions (Section 4 of the Cloud & DevOps curriculum). Answers are formulated from an enterprise SRE perspective, covering OSI encapsulation, transport protocols, reverse proxy mechanics, DNS resolution paths, and real-world latency triage.

---

## Question Index

| # | Topic | Key SRE Focus |
| :--- | :--- | :--- |
| **4.1** | DNS Architecture & Mechanics | Recursive resolvers, root, TLD, authoritative nameservers, TTL caching |
| **4.2** | Complete Request Flow (OSI Encapsulation) | Application to physical layer, ARP resolution, TCP 3-way handshake, TLS 1.3 |
| **4.3** | Forward Proxy vs Reverse Proxy | Client anonymity/egress inspection vs server shielding, TLS termination, load balancing |
| **4.4** | Latency & Slowness Triage | Isolating network vs application latency: RTT, TTFB, DNS lookup, TCP connect times |
| **4.5** | `curl` Works via IP, Fails via Domain | DNS resolution chain (`/etc/resolv.conf`, nsswitch), SNI headers, Host headers |
| **4.6** | HTTP 502 Bad Gateway Triage | Proxy-to-upstream failure, connection refused, port mismatch, socket exhaustion |
| **4.7** | `0.0.0.0` vs `127.0.0.1` | Loopback interface (`lo`) isolation vs all IPv4 interface socket binding (`INADDR_ANY`) |
| **4.8** | Public vs Private Subnets | AWS route tables, Internet Gateway (`0.0.0.0/0 -> igw`), NAT Gateway egress isolation |
| **4.9** | Remediation: Misconfigured Private Subnet | Non-destructive conversion: route table re-association, elastic IP assignment |

---

### Question 4.1: Explain DNS in simple terms, and describe the recursive resolution chain.

#### Conceptual Definition
The Domain Name System (DNS) is a distributed, hierarchical database that translates human-readable domain names (e.g., `api.production.internal` or `google.com`) into machine-routable IP addresses (e.g., `142.250.190.46` or `2607:f8b0:4005:808::200e`).

#### The Recursive Resolution Chain (Step-by-Step)
When a client application requests `https://api.github.com` and has no local cache:

```
[ Client ] 
    | (1. Query: api.github.com)
    v
[ Recursive Resolver (e.g., 8.8.8.8, AWS Route 53 Resolver 169.254.169.253) ]
    |
    |---> (2. Where is .com?) --------------> [ Root Nameserver (.) ]
    |<--- (3. Refer to .com TLD) -----------+
    |
    |---> (4. Where is github.com?) --------> [ TLD Nameserver (.com) ]
    |<--- (5. Refer to GitHub NS) ----------+
    |
    |---> (6. Where is api.github.com?) ----> [ Authoritative Nameserver (ns-1.github.com) ]
    |<--- (7. Returns IP: 140.82.121.4) ----+
    |
    v (8. Caches answer for TTL seconds & returns IP)
[ Client initiates TCP connection to 140.82.121.4 ]
```

#### Key DNS Record Types in Production
- `A` Record: Resolves an IPv4 address.
- `AAAA` Record: Resolves an IPv6 address.
- `CNAME` (Canonical Name): Maps an alias to another domain (cannot exist at the apex/root domain).
- `ALIAS` (AWS Route 53 Specific): Virtual record mapping apex domains (`example.com`) directly to AWS resources (ALBs, CloudFront) without incurring DNS query charges.
- `PTR` (Pointer): Reverse DNS lookup (IP to domain name).

---

### Question 4.2: Walk through the complete client-to-server request flow across the OSI model.

#### Phase 1: Application Layer (Layer 7)
1. User types `https://api.company.com/v1/users` into a browser.
2. The browser constructs an HTTP/1.1 or HTTP/2 `GET` request.

#### Phase 2: DNS & Address Resolution
3. The operating system checks `/etc/hosts` and local DNS resolver cache.
4. If missing, it performs recursive DNS resolution (UDP port 53) to obtain the server's IP address (`198.51.100.10`).

#### Phase 3: Transport Layer (Layer 4) — TCP & TLS Handshake
5. **TCP 3-Way Handshake:**
   - Client sends `SYN` (Sequence Number $X$).
   - Server returns `SYN-ACK` (Sequence Number $Y$, Acknowledgment $X+1$).
   - Client sends `ACK` (Acknowledgment $Y+1$). Connection state: `ESTABLISHED`.
6. **TLS 1.3 Handshake:**
   - Client sends `ClientHello` with supported cipher suites and Server Name Indication (SNI).
   - Server responds with `ServerHello`, TLS Certificate, and Key Exchange.
   - Symmetric AES-GCM session keys are established; all subsequent application traffic is encrypted.

#### Phase 4: Network Layer (Layer 3) — IP Routing
7. The OS encapsulates the TCP segment into an IP packet: Source IP (`Client IP`), Destination IP (`198.51.100.10`).
8. If the destination is outside the local subnet, the host checks its routing table (`ip route`) and determines the next-hop default gateway.

#### Phase 5: Data Link Layer (Layer 2) — ARP & Ethernet Framing
9. To send the packet to the local gateway, the host checks its ARP cache (`arp -n`).
10. If missing, an Address Resolution Protocol (ARP) broadcast (`Who has 192.168.1.1?`) resolves the gateway's Layer 2 MAC address.
11. An Ethernet frame is constructed with the Gateway's MAC as destination and Host MAC as source.

#### Phase 6: Physical Layer (Layer 1) & Reverse Decapsulation
12. Bits are modulated as optical, electrical, or radio signals across routers and internet backbones.
13. The destination server decapsulates the layers in reverse (Ethernet frame -> IP packet -> TCP stream -> TLS decryption -> HTTP processing in Nginx/Application).

---

### Question 4.3: What is the exact difference between a Forward Proxy and a Reverse Proxy?

#### The Fundamental Difference
- **Forward Proxy:** Acts on behalf of the **client**. The server does not know the real client.
- **Reverse Proxy:** Acts on behalf of the **server(s)**. The client does not know the real backend server.

```
FORWARD PROXY:
[ Internal Clients ] ---> [ Forward Proxy (Squid) ] ---> [ Internet / External APIs ]
(Protects clients, enforces corporate outbound filtering, content caching)

REVERSE PROXY:
[ External Internet ] ---> [ Reverse Proxy (Nginx / ALB) ] ---> [ Backend Microservices ]
(Protects servers, terminates TLS, load balances, mitigates DDoS)
```

#### Detailed Comparison

| Dimension | Forward Proxy | Reverse Proxy |
| :--- | :--- | :--- |
| **Who it Represents** | The Client | The Server / Cluster |
| **Client Awareness** | Client explicitly configures proxy (`HTTP_PROXY=...`) | Client has zero awareness; connects directly to proxy URL |
| **Primary Use Cases** | Corporate egress security, DLP, caching outbound traffic | Ingress load balancing, TLS offloading, rate limiting, WAF |
| **Common Software** | Squid, Envoy, Cloudflare Gateway, Zscaler | Nginx, HAProxy, Traefik, AWS Application Load Balancer |

---

### Question 4.4: A user reports that your web application is slow. How do you isolate network latency from application latency?

#### Methodical SRE Latency Breakdown
Never guess. Measure the request breakdown at the transport boundary using `curl` instrumentation:

```bash
curl -w "\
DNS Lookup:        %{time_namelookup}s\n\
TCP Connect:       %{time_connect}s\n\
TLS Handshake:     %{time_appconnect}s\n\
Pre-transfer:      %{time_pretransfer}s\n\
Start Transfer:    %{time_starttransfer}s (TTFB)\n\
------------------------------------\n\
Total Time:        %{time_total}s\n" \
-o /dev/null -s https://api.production.com/v1/health
```

#### Diagnosing the Culprit:
1. High `time_namelookup` (> 100ms):
   - **Root Cause:** DNS misconfiguration, overloaded nameservers, or missing DNS caching.
2. High `time_connect` - `time_namelookup` (> 150ms):
   - **Root Cause:** High network round-trip time (RTT), geographic distance, routing congestion, or MTU black holes.
   - Verify via `mtr` / `traceroute`:
     ```bash
     # Continuous ping and traceroute to isolate hop packet loss
     mtr -rw api.production.com
     ```
3. Normal `time_appconnect` but Massive `time_starttransfer` (TTFB):
   - **Root Cause:** **Application-level bottleneck**. The network delivered the bytes instantly, but the backend took 4 seconds to execute a slow SQL query, wait on a database lock, or process an unindexed API request before flushing the first byte.

---

### Question 4.5: `curl` succeeds when targeting the IP address directly, but fails when using the domain name. What are the failure modes?

#### 1. DNS Resolution Failure
The client operating system cannot resolve the domain to an IP address.
- Triage:
  ```bash
  dig api.company.com +trace
  nslookup api.company.com
  cat /etc/resolv.conf
  ```
- Common causes: Missing search domains in `/etc/resolv.conf`, expired domain registration, or misconfigured DNS records in Route 53.

#### 2. VirtualHost / HTTP `Host` Header Mismatch
When you run `curl http://198.51.100.10`, curl sends `Host: 198.51.100.10`.
When you run `curl http://api.company.com`, curl sends `Host: api.company.com`.
- If the web server (Nginx/Apache) is configured with a strict `server_name api.company.com;` block that rejects raw IP requests, or conversely, if the reverse proxy defaults to a 404 or drops traffic for unknown Host headers.
- Test with simulated host header:
  ```bash
  curl -H "Host: api.company.com" http://198.51.100.10
  ```

#### 3. TLS Server Name Indication (SNI) Mismatch
In HTTPS, modern servers host multiple TLS certificates on a single IP address. During the TLS handshake, the client must present the SNI hostname.
- If you `curl https://<IP>`, curl cannot send a valid SNI extension matching the certificate, causing the handshake to abort with `SSL certificate problem: certificate verify failed` or `SSL: no alternative certificate subject name matches target host name`.

---

### Question 4.6: An end-user receives an HTTP `502 Bad Gateway`. What is the technical mechanism, and how do you triage it?

#### The Technical Mechanism
A `502 Bad Gateway` error is generated **by a reverse proxy or load balancer** (e.g., Nginx, AWS ALB, Cloudflare).

It indicates that the proxy attempted to connect to an upstream backend server (e.g., Node.js, Gunicorn, Go, PHP-FPM), but the upstream responded with an invalid response, terminated the connection abruptly, or failed to accept the TCP connection.

```
[ Client ] ---> [ Reverse Proxy (Nginx / ALB) ] ---> [ Connection Refused / Crash ] -x-> [ Upstream App ]
                          |
   <--- (HTTP 502 Generated by Proxy)
```

#### Step-by-Step Triage Workflow

1. Inspect the Proxy Error Log (The Source of Truth):
   ```bash
   tail -n 50 /var/log/nginx/error.log
   ```
   Common log entries:
   - `connect() failed (111: Connection refused) while connecting to upstream`: The backend process is dead, crashed, or listening on the wrong port/socket.
   - `no live upstreams while connecting to upstream`: All backend target instances failed health checks.
   - `upstream prematurely closed connection while reading response header`: The application backend crashed (e.g., OOM or unhandled panic) halfway through processing the request.

2. Verify Backend Process State:
   ```bash
   systemctl status my-backend
   # or for containers:
   docker ps --filter "name=backend"
   ```

3. Check Listening Sockets & Port Bindings:
   ```bash
   ss -tulpn | grep <expected_port>
   ```

4. Security Groups / Firewall Rules:
   - Verify that the reverse proxy's IP/subnet is allowed ingress access to the upstream server's port.

---

### Question 4.7: What is the exact difference between `0.0.0.0` and `127.0.0.1`?

#### Technical Definition

| Address | Formal Name | Scope | Accessible From |
| :--- | :--- | :--- | :--- |
| `127.0.0.1` | Loopback Address (`localhost`) | Local host only | Only processes running on the exact same OS instance |
| `0.0.0.0` | Meta-address (`INADDR_ANY`) | Non-routable broadcast/wildcard | Binds the socket to **all available IPv4 network interfaces** |

#### Practical Engineering Implication
- When a server binds to `127.0.0.1:8080`:
  The operating system routes traffic through the virtual loopback adapter (`lo`). It is physically impossible for packets arriving from external network interfaces (`eth0`, Wi-Fi, Docker bridge) to reach this socket.
- When a server binds to `0.0.0.0:8080`:
  The process listens on `127.0.0.1`, its private LAN IP (`10.0.1.5`), and its public IP (`54.210.x.x`). Any external client that can route packets to the machine can communicate with the service (subject to firewall rules).

---

### Question 4.8: What defines an AWS subnet as "Public" vs "Private"?

#### The Defining Mechanism
In AWS VPC architecture, subnets do **not** have an intrinsic "public" or "private" property flag in their configuration.

A subnet is defined as **Public** or **Private** purely by the **routes configured in its associated Route Table**:

- **Public Subnet:**
  Its associated route table contains a default route (`0.0.0.0/0`) targeting an **Internet Gateway (`igw-xxxx`)**:
  ```
  Destination: 0.0.0.0/0  --->  Target: igw-0123456789abcdef0
  ```
  Instances with public IP addresses in this subnet can directly send and receive bi-directional internet traffic.

- **Private Subnet:**
  Its route table does **not** route directly to an Internet Gateway.
  Instead, outbound internet egress is routed through a **NAT Gateway (`nat-xxxx`)** situated in a public subnet:
  ```
  Destination: 0.0.0.0/0  --->  Target: nat-0123456789abcdef0
  ```
  Instances in this subnet can initiate outbound connections to the internet (e.g. for package updates), but external internet clients cannot directly initiate inbound connections to them.

---

### Question 4.9: You accidentally provisioned a subnet as private instead of public. How do you convert it with zero downtime?

#### Safe Remediation Procedure
Because public/private designation is determined by route table associations rather than subnet recreation, you do **not** need to destroy or delete the subnet.

1. Identify Route Tables:
   - Identify the target subnet ID (`subnet-01234567`).
   - Identify the existing Public Route Table containing the route `0.0.0.0/0 -> igw-xxxx`.

2. Re-associate the Subnet via CLI / Terraform:
   - Via AWS CLI:
     ```bash
     # Find current association ID
     ASSOC_ID=$(aws ec2 describe-route-tables \
       --filters "Name=association.subnet-id,Values=subnet-01234567" \
       --query "RouteTables[0].Associations[0].RouteTableAssociationId" --output text)

     # Replace association with Public Route Table
     aws ec2 replace-route-table-association \
       --association-id $ASSOC_ID \
       --route-table-id rtb-public-id
     ```
   - Via Terraform:
     Simply modify the `aws_route_table_association` resource to point `route_table_id` to the public route table. Terraform updates the association in place without destroying the subnet or instances.

3. Enable Auto-Assign Public IP (Optional):
   ```bash
   aws ec2 modify-subnet-attribute \
     --subnet-id subnet-01234567 \
     --map-public-ip-on-launch
   ```
