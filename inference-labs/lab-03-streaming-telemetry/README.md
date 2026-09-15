# Lab 03 — Streaming Telemetry & Latency Profiling (TTFT vs TPS)

**Objective:** Build high-precision telemetry for streaming autoregressive models. Benchmark Time To First Token (prefill phase) versus Tokens Per Second (decode phase) under increasing concurrency.

---

## 1. The Two Phases of LLM Generation

Unlike classical web servers where request duration equals computation time, LLM inference operates in two distinct phases with totally different hardware constraints:

```
User Prompt (N tokens)
       │
       ▼ [Phase 1: Prefill / Prompt Evaluation]
Compute-Bound: GPU cores run at 100% matrix multiplication.
Duration = TTFT (Time To First Token) + Queue Latency.
       │
       ▼ First token arrives
       │
       ▼ [Phase 2: Autoregressive Decode]
Memory-Bandwidth Bound: Model parameters transferred from VRAM per token.
Duration = Inter-Token Latency (ITL) × Output Length.
Total Tokens / Time = TPS (Tokens Per Second).
```

---

## 2. Running the Telemetry Profiler

1. Ensure your inference daemon is running on port 8000 (from Lab 02).
2. Install `httpx`:
   ```bash
   pip install httpx
   ```
3. Run the benchmark script:
   ```bash
   python benchmark_streaming.py --concurrency 1
   ```
4. Step up concurrency to 5 and then 10 users:
   ```bash
   python benchmark_streaming.py --concurrency 5
   python benchmark_streaming.py --concurrency 10
   ```

---

## 3. What to Observe in the Results

* **TTFT Inflation:** As concurrency scales, TTFT jumps from 80ms to 600ms+ because prompt prefill tasks queue up behind active decodes.
* **Per-User TPS vs Aggregate TPS:** Individual stream speed drops (e.g. 35 tok/s $\to$ 18 tok/s), but **System Aggregate TPS** (the sum of tokens emitted per second across all streams) increases until saturating the memory bus.
