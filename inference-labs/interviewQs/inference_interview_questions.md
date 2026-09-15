# Inference Engineering & AI Platform Master Interview Guide (25 Questions)

**Author:** Srinivas Sarkar  
**Target:** AI Platform Engineer, LLMOps, Inference Systems Engineer (Startups & AI Product Teams)  
**Scope:** Model serving architecture, VRAM management, KV cache, latency telemetry, streaming networking, and failure recovery.

---

### Q01: How do you calculate how much VRAM a model requires before deploying it to production?
**Answer:**
$$\text{Total VRAM} = \text{Model Weights} + \text{KV Cache Allocation} + \text{CUDA Context Overhead (}\approx 400\text{MB)}$$
* Weight calculation: $\text{Parameters (B)} \times \text{Bytes per Precision}$. (e.g. 7B in 4-bit $\approx 7 \times 0.58 = 4.06$ GB; in FP16 $\approx 7 \times 2 = 14$ GB).
* KV cache calculation: $2 \times \text{Layers} \times \text{Heads} \times \text{HeadDim} \times 2\text{ bytes} \times \text{ContextLength} \times \text{Concurrency}$.
* You must pre-allocate and bound the KV cache so that active user sessions never push total memory beyond physical VRAM, which causes fatal `CUDA Out of Memory` crashes.

---

### Q02: What is the technical difference between the Prefill Phase and the Decode Phase in LLM inference?
**Answer:**
* **Prefill Phase (Prompt Evaluation):** The model takes the entire input prompt ($N$ tokens) and processes it simultaneously through the transformer attention layers. It is **compute-bound** (matrix-multiplication heavy). Processing units run at 100% utilization. The duration of this phase is reflected as **TTFT (Time To First Token)**.
* **Decode Phase (Autoregressive Token Generation):** The model generates one token at a time. Each generated token requires reading all model weights from memory into the compute registers. It is **memory-bandwidth bound**. Compute utilization drops while the memory bus is saturated. The speed of this phase is measured in **TPS (Tokens Per Second)**.

---

### Q03: What is PagedAttention, and what fundamental OS concept does it borrow to solve KV cache fragmentation?
**Answer:**
* In naive inference engines, the KV cache requires contiguous physical memory allocation for the maximum possible context window of every request. This causes massive memory fragmentation and wastes up to 60–80% of VRAM on ungenerated tokens.
* **PagedAttention** (developed for vLLM) borrows the concept of **Virtual Memory Paging** from the Linux kernel. It divides the KV cache into fixed-size logical pages (blocks of tokens, e.g. 16 tokens per block).
* Pages are dynamically allocated in physical VRAM as tokens are generated and do not need to be contiguous. This allows multiple sequences (and parallel sampling / beam search) to share memory blocks, increasing system throughput by 2x–4x.

---

### Q04: What is Continuous Batching (Iteration-Level Scheduling), and why does it outperform static batching?
**Answer:**
* In static batching, an inference engine groups $N$ requests together. If Request A finishes in 50 tokens and Request B takes 500 tokens, the batch cannot accept new work until Request B completes. The GPU sits largely idle waiting for the longest request.
* **Continuous Batching** operates at the **iteration (token) level**. As soon as Request A emits a `[DONE]` token, it is immediately ejected from the batch, and a new incoming prompt is inserted into the batch on the very next token iteration. This keeps compute and memory pipelines continuously saturated.

---

### Q05: Why does standard Nginx configuration break LLM streaming responses, and how do you fix it?
**Answer:**
* Standard reverse proxies have `proxy_buffering on;` enabled by default to optimize network packets by waiting for the complete HTTP response body before sending it downstream.
* For streaming LLMs using Server-Sent Events (SSE), this causes the client to hang with a blank screen until the entire generation finishes, followed by a sudden dump of the whole text.
* **The Fix:** Explicitly disable proxy buffering and enable unbuffered streaming headers:
  ```nginx
  proxy_buffering off;
  proxy_cache off;
  proxy_set_header X-Accel-Buffering no;
  proxy_http_version 1.1;
  proxy_set_header Connection "";
  ```

---

### Q06: What causes a `504 Gateway Timeout` during LLM generation, and how do you configure proxy timeouts?
**Answer:**
* LLM generations (especially for code generation or complex reasoning) can run for 30 to 90 seconds.
* Most reverse proxies (Nginx, HAProxy, AWS ALB) have a default read timeout of 60 seconds. If generation exceeds this window without sending buffered bytes, the proxy terminates the TCP socket and returns HTTP 504.
* **The Fix:** Increase `proxy_read_timeout` to 300s or 600s, and implement periodic heartbeat comments (`: ping\n\n`) in your SSE stream to keep the TCP connection active.

---

### Q07: Explain Quantization formats: GGUF vs AWQ vs GPTQ vs FP8. When do you choose which?
**Answer:**
* **GGUF:** Binary format designed for CPU and Apple Silicon / consumer GPU inference (via `llama.cpp`). Embeds model architecture, metadata, and quantized weights in a single file. Ideal for local, edge, and hybrid bare-metal setups.
* **AWQ (Activation-aware Weight Quantization):** 4-bit weight-only quantization that protects the top 1% of salient weights that carry the most information. High accuracy, extremely fast inference on modern NVIDIA GPUs in vLLM.
* **GPTQ:** Post-training 4-bit quantization based on approximate second-order information. Optimized for NVIDIA GPU VRAM reduction.
* **FP8:** 8-bit floating point natively supported on newer architectures (NVIDIA Ada Lovelace / Hopper / H100). Delivers 2x speedup over FP16 with virtually zero accuracy loss.

---

### Q08: How do you handle an unexpected `CUDA Out of Memory` (OOM) crash in production?
**Answer:**
1. **Immediate Recovery:** Ensure the daemon is supervised by `systemd` or `PM2` with `Restart=on-failure` so the service restarts automatically.
2. **Root Cause Analysis:** Inspect the crash logs to determine whether OOM occurred during weight loading (oversized model) or during generation (KV cache exhaustion).
3. **Guardrail Implementation:** Set a strict `--max-model-len` or `-c` parameter to limit maximum context length, reduce `--max-num-seqs` (maximum concurrent sequences), or implement request queue shedding at the API gateway layer when concurrency exceeds safe limits.

---

### Q09: What is Speculative Decoding, and how does it accelerate generation speed?
**Answer:**
* Speculative Decoding pairs a large target model (e.g. 70B) with a tiny, fast draft model (e.g. 1B).
* The fast draft model speculatively generates $K$ candidate tokens quickly. The large target model evaluates all $K$ tokens in parallel in a single forward pass (prefill compute-bound step).
* Tokens that match the target model's distribution are accepted; incorrect tokens are discarded. Because evaluating $K$ tokens in parallel takes nearly the same time as generating 1 token autoregressively, speculative decoding achieves a 2x–3x speedup with identical mathematical output.

---

### Q10: What metrics do you monitor on GPU nodes running inference workloads?
**Answer:**
1. **GPU Volatile Utilization %:** Percentage of time GPU cores are actively executing kernels.
2. **GPU Memory Used vs Total:** Tracked via `nvidia-smi` or Prometheus DCGM exporter (`DCGM_FI_DEV_FB_USED`).
3. **GPU Temperature & Throttle Reasons:** Detecting thermal throttling or power cap throttling.
4. **TTFT (Time To First Token):** Service-level SLI for prompt wait time.
5. **Tokens Per Second (TPS):** Per-stream and aggregate generation throughput.
6. **Queue Depth:** Number of requests waiting in the inference engine's pending queue.

---

### Q11: How does Apple Silicon Unified Memory Architecture (UMA) compare to traditional NVIDIA discrete GPUs for LLM inference?
**Answer:**
* **Discrete GPUs (NVIDIA):** High memory bandwidth (up to 2–3 TB/s on H100), but VRAM is physically capped (e.g. 24GB on 4090, 80GB on H100). Moving weights across PCIe buses creates bottlenecks.
* **Apple Silicon UMA (M3 Ultra / M4):** CPU and GPU share a single physical pool of unified RAM (up to 256 GB on M3 Ultra) with memory bandwidth up to 800 GB/s. This allows running massive 70B or 120B models entirely in local memory that would otherwise require multiple enterprise GPUs.

---

### Q12: Why is Server-Sent Events (SSE) preferred over WebSockets for text generation streaming?
**Answer:**
* SSE operates over standard HTTP/1.1 or HTTP/2 connections using simple `text/event-stream` MIME types, making it lightweight, easily cacheable, and compatible with standard API gateways, firewalls, and proxies.
* WebSockets require a protocol upgrade handshake and maintain stateful bi-directional TCP framing, adding unnecessary complexity when communication is strictly unidirectional (server streaming tokens to client).

---

### Q13: What is Chunked Prefill, and why is it critical for multi-tenant inference services?
**Answer:**
* If one user submits a massive 16,000-token prompt, standard engines will monopolize the GPU compute cores for seconds to complete the prefill phase. During this time, all other active users experience sudden token delivery freezes (latency jitter).
* **Chunked Prefill** splits large prompts into smaller chunks (e.g. 512 tokens) and interleaves them with active decode iterations across other requests, flattening latency spikes.

---

### Q14: Explain the difference between Temperature, Top-P, and Top-K sampling parameters.
**Answer:**
* **Temperature:** Divides logits before softmax. Lower values ($<0.2$) sharpen probability distribution toward the most likely token (deterministic/coding); higher values ($>0.8$) flatten distribution (creative/diverse).
* **Top-K:** Limits candidate pool to the $K$ tokens with the highest probabilities.
* **Top-P (Nucleus Sampling):** Selects the smallest set of candidate tokens whose cumulative probability exceeds threshold $P$ (e.g. 0.90). Dynamically expands or shrinks candidate pool based on model confidence.

---

### Q15: How does vLLM handle multi-GPU tensor parallelism?
**Answer:**
* For models that exceed single-GPU VRAM (e.g. 70B model requiring ~35GB in 4-bit or ~140GB in FP16), **Tensor Parallelism** splits individual weight matrices across multiple GPUs (e.g. `--tensor-parallel-size 4`).
* Spreading layers across GPUs requires high-speed GPU-to-GPU interconnects (NVLink); GPUs synchronize intermediate activations after each layer using `AllReduce` operations.

---

### Q16: How do you implement automated healthchecks on an inference container in Kubernetes?
**Answer:**
* **Liveness Probe:** An HTTP endpoint (e.g. `GET /health` or `GET /v1/models`) that verifies the daemon process is alive and responsive.
* **Readiness Probe:** Evaluates whether model weights are fully loaded into VRAM and the engine is ready to accept traffic.
* **Gotcha:** Do NOT run a full generation request in your readiness probe under load, as it wastes GPU compute and triggers probe timeouts.

---

### Q17: What is the role of an inference model router or gateway (like LiteLLM or OpenRouter)?
**Answer:**
* A model gateway sits between clients and backend inference workers to provide: (1) Unified OpenAI-compatible API schemas. (2) Dynamic load balancing across multiple worker nodes based on queue depth. (3) Fallback routing (e.g. if local GPU cluster 5xxs, fail over to cloud API). (4) Rate-limiting and token budgeting per tenant.

---

### Q18: What is the impact of Linux `swappiness` and swap memory on GPU model workers?
**Answer:**
* When model weights or KV caches spill from VRAM into CPU RAM, that is slow. But if CPU RAM begins swapping anonymous pages onto disk (swap space), inference latency degrades by 1000x, causing complete service hangs.
* Production inference hosts should run with minimal swappiness (`vm.swappiness=1` or `0`) and prioritize OOM termination over disk thrashing.

---

### Q19: Why should you avoid using standard Kubernetes Horizontal Pod Autoscaler (HPA) CPU metrics for scaling inference pods?
**Answer:**
* Inference pods spend the decode phase memory-bandwidth bound, where CPU/GPU utilization can be low despite the node being completely saturated with concurrent requests.
* Scaling must be driven by custom metrics via **KEDA**: specifically **Queue Depth** (number of pending requests waiting in queue) or **KV Cache Usage %**.

---

### Q20: What is KV Cache Offloading, and what are its performance trade-offs?
**Answer:**
* When VRAM is full, idle KV cache blocks can be evicted to system CPU RAM. When the request resumes, the blocks are fetched back over PCIe.
* *Trade-off:* Prevents OOM crashes during long conversational sessions, but introduces significant PCIe transfer latency when paging blocks back into GPU memory.

---

### Q21: What is a System Prompt, and why is prompt prefix caching important?
**Answer:**
* A system prompt sets the persona and instructions for an agent (often 500–2000 tokens long) and is identical across all user requests.
* **Prefix Caching** allows the inference engine to compute the KV cache for the system prompt once and store it. Subsequent requests reuse the pre-computed KV cache, reducing TTFT to near zero.

---

### Q22: Explain the difference between Weight-Only Quantization and Full Weight-and-Activation Quantization (W8A8 / W4A4).
**Answer:**
* **Weight-Only Quantization (e.g. W4A16, AWQ):** Quantizes static model weights to 4-bit to save VRAM, but dequantizes them to FP16 on the fly for computation. Activations remain in FP16. Ideal for decode-bound consumer GPUs.
* **Weight-and-Activation Quantization (W8A8 / W4A4):** Both weights and dynamic activations are quantized. Matrix multiplications are executed directly in INT8 or INT4 tensor cores, providing massive compute speedups on enterprise hardware.

---

### Q23: How do you design zero-downtime model rollouts on a cluster?
**Answer:**
* Models take 30–120 seconds to load weights into VRAM. You cannot use rolling replacement without strict readiness gates.
* The new model pod must report ready only after weights are loaded into VRAM. Traffic is gradually shifted via blue-green deployment or canary routing at the ingress controller. Active streams on the old pod are allowed to drain before sending `SIGTERM`.

---

### Q24: What is the memory footprint of an unindexed raw vector in a Vector Database versus an in-memory HNSW graph?
**Answer:**
* A 1536-dimensional embedding stored as FP32 requires $1536 \times 4 = 6,144$ bytes (~6 KB).
* An in-memory **HNSW (Hierarchical Navigable Small World)** index adds graph links and metadata, which typically triples the memory footprint to ~18–20 KB per vector. One million vectors require ~18–20 GB of RAM.

---

### Q25: Why is the combination of traditional Linux/DevOps expertise and Inference Engineering so valuable to AI startups?
**Answer:**
* AI startups are bleeding money on GPU cloud bills and latency bottlenecks.
* Most developers know how to call APIs or write Python scripts, but few understand how to optimize memory ceilings, tune Nginx streaming buffers, supervisor-manage daemons, and debug kernel socket leaks under load.
* An engineer who can bridge **infrastructure reliability, Linux process mechanics, and model serving physics** directly reduces cloud expenditure, eliminates downtime, and accelerates product responsiveness.
