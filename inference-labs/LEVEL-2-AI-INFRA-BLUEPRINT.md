# Level-2: AI Infrastructure & Systems Engineering Blueprint

A production systems engineering roadmap designed to bridge the gap between classic Cloud/DevOps infrastructure and modern high-throughput LLM serving clusters.

---

## 1. The Architectural Philosophy: The Decoupled Serving Layer

In production enterprise architectures (such as multi-agent orchestration systems like BluBot), application developers focus on agents, intent classification, and AST traversal. 

The **Platform / SRE Engineer** owns the underlying physical substrate:
1. **Decoupled Daemon Execution:** Isolating models as operating system background daemons (`systemd` on Linux, `launchd` on macOS) rather than embedding weights inside application runtimes.
2. **Zero-Downtime Microservices:** Exposing standardized, OpenAI-compatible HTTP endpoints with automatic process supervision, `Restart=on-failure`, and graceful driver unbinding.
3. **Silicon & Network Optimization:** Eliminating edge proxy buffering hangs and allocating exact VRAM/RAM budgets to prevent catastrophic CUDA OOMs.

---

## 2. The Dual-Hardware Testbed (The Unfair Advantage)

Our systems labs operate across two contrasting hardware paradigms:

```
+-----------------------------------------------------------------------------------------+
| TARGET A: CONSTRAINED EDGE LINUX NODE                                                   |
| - Silicon: NVIDIA GeForce GTX 1050 Ti (4,096 MiB VRAM)                                  |
| - Architecture: Discrete GPU over PCIe bus | CUDA 12.8                                  |
| - Engineering Focus: Micro-budgeting VRAM, GQA memory compression, GPU layer offloading |
|   (-ngl), socket file descriptor limits (LimitNOFILE=65536), and Nginx SSE proxy tuning.|
+-----------------------------------------------------------------------------------------+
| TARGET B: HIGH-MEMORY BARE-METAL MAC STUDIO SERVER                                      |
| - Silicon: Apple M3 Ultra (28 cores: 20 perf, 8 eff | 256 GB Unified Memory)            |
| - Architecture: Unified Memory Architecture (UMA) | ~800 GB/s bandwidth | Apple MLX     |
| - Engineering Focus: Native BF16 unquantized serving, zero PCIe transfer latency,        |
|   macOS launchd process management, and private mesh networking via Tailscale.         |
+-----------------------------------------------------------------------------------------+
```

---

## 3. The 4 Completed Labs (Phase 1 Baseline)

| Lab | Name | Silicon Focus | Key Verified Result |
| :--- | :--- | :--- | :--- |
| **01** | **VRAM Budgeting** | Memory Ceilings & GQA | Predicted 1,412 MiB; measured 1,418 MiB on silicon (99.6% accuracy). Observed +836 MiB dynamic KV cache expansion at 32K context. |
| **02** | **Serving Daemons** | Supervisors & Layer Offload | Standardized on `/v1/chat/completions`. Proved automated `systemd` recovery from `kill -9` in exactly 3 seconds. |
| **03** | **Streaming Telemetry** | Latency SLIs (TTFT vs TPOT) | Dissected cold TTFT (1,619 ms) vs warm TTFT (152 ms). Discovered prefill queue inflation (P90 TTFT exploded to 14.4s under 8 users while throughput hit 401 TPS). |
| **04** | **Streaming Ingress** | Nginx SSE Reverse Proxy | Eliminated the 10-second proxy buffering hang using `proxy_buffering off;` and `X-Accel-Buffering: no;`. Tuned `proxy_read_timeout 300s;` to eliminate 504s. |

---

## 4. The 2-Track Weekly Operating Rhythm

To maintain peak momentum without burnout, the schedule is strictly bifurcated:

### Track 1: Weekdays (Monday – Friday | 45–60 mins)
* **Objective:** Pure Cloud, DevOps, and SRE Interview Mastery.
* **Topics:** Linux kernel triage (USE method, `/proc`), networking (TCP states, DNS), Kubernetes architecture (CNI, pod lifecycle, OOM 137), Terraform state locks, and FAANG incident trees.

### Track 2: Weekends (Saturday & Sunday | 2 hours/day)
* **Objective:** Deep AI Infrastructure Exploration, Benchmarking, and Public Sharing.
* **October Milestones:**
  * **Weekend 1 (Oct 3–4): Memory Topology & Interview Mastery**
    * Pen-and-paper drills on the 3 VRAM buckets (Weights, KV cache, Scratchpad).
    * Master the 25 core Inference interview questions in `interviewQs/`.
  * **Weekend 2 (Oct 10–11): The Observability Bridge**
    * Expose Prometheus metrics from Ollama / MLX and GPU utilization.
    * Build custom Grafana dashboards for TTFT, TPOT, and VRAM.
  * **Weekend 3 (Oct 17–18): The Hybrid Multi-Backend Gateway**
    * Configure Nginx as an intelligent edge router:
      * `/v1/chat` $\implies$ Linux GTX 1050 Ti (Qwen 1.5B via CUDA).
      * `/v1/translate` $\implies$ Mac Studio M3 Ultra (Sarvam Translate via MLX & Tailscale).
    * Benchmark hybrid network latency under concurrent streaming load.
  * **Weekend 4 (Oct 24–25): Engine Internals (PagedAttention & vLLM)**
    * Dissect PagedAttention non-contiguous block memory vs contiguous buffers.
    * Benchmark memory fragmentation and publish the monthly portfolio capstone.
