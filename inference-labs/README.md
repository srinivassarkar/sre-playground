# Inference Engineering Flight Simulator

Hands-on AI systems and inference infrastructure labs designed for Platform / DevOps engineers.
Tested on constrained hardware (**NVIDIA GTX 1050 Ti 4GB VRAM**) and scalable to **Apple Silicon (M3 Ultra / M4)** and cloud GPU clusters.

Zero fluff. Zero machine learning math. 100% systems engineering, VRAM budgeting, daemon management, latency telemetry, and streaming reverse proxies.

---

## The 4 Labs

| Lab | Focus | What You Learn & Measure |
|-----|-------|--------------------------|
| **01 — VRAM Budgeting** | Memory Ceilings & Quantization | Calculate model weight + KV Cache sizing; trigger and diagnose CUDA OOM crashes. |
| **02 — Serving Daemon** | OpenAI-Compatible Engines | Run `llama.cpp` server / Ollama with GPU layer offloading (`-ngl`); daemonize with `systemd` & `PM2`. |
| **03 — Streaming Telemetry** | Latency Profiling (TTFT vs TPS) | Measure Time To First Token (prefill) vs Inter-Token Latency (decode); run concurrency stress tests. |
| **04 — Streaming Proxy** | Edge Ingress & Nginx Tuning | Route streaming SSE tokens; observe the fatal proxy-buffering hang; tune read timeouts for zero 504s. |

---

## Hardware Testbeds

This suite is designed to be executed across:
1. **Target A (Constrained GPU):** Linux box with **NVIDIA GTX 1050 Ti (4GB VRAM)**, CUDA 12.x.
2. **Target B (Unified Memory Bare-Metal):** macOS with **Apple Silicon (M4 / M3 Ultra)** using Metal acceleration.
3. **Target C (Consumer CPU/WSL2):** Local workstation running quantized GGUF models on CPU threads.

---

## Structure

```
inference-labs/
├── lab-01-vram-budgeting/       # Formulas, memory allocation, OOM reproduction
├── lab-02-serving-daemon/       # Daemon configs, layer offloading, systemd & PM2
├── lab-03-streaming-telemetry/  # Async Python streaming profiler, TTFT/TPS metrics
├── lab-04-streaming-proxy/      # Nginx reverse proxy, SSE buffering vs streaming
└── interviewQs/                 # 25 core Inference Engineering interview questions
```
