# Lab 02 — Serving Daemons: Layer Offloading & Supervisor Management

**Objective:** Deploy an OpenAI-compatible inference engine (`llama.cpp` server or Ollama) with GPU layer offloading, calibrate thread and batch settings, and daemonize it under `systemd` and `PM2` with automated crash recovery.

---

## 1. Core Daemon Flags (What Every SRE Must Know)

* **`-ngl` / `--n-gpu-layers <N>`:** Specifies how many transformer layers to offload to GPU VRAM. Setting `-ngl 99` offloads all layers. If a model is too large for your GPU (e.g. 7B on 4GB), setting `-ngl 18` offloads 18 layers to GPU VRAM and runs the remaining layers in CPU RAM (hybrid split execution).
* **`-c` / `--ctx-size <tokens>`:** The allocated context window. Crucial: memory for the KV cache is pre-reserved or paged based on this ceiling.
* **`-b` / `--batch-size <N>`:** Batch size for prompt evaluation (prefill phase). Higher values improve prefill speed but spike memory.
* **`-t` / `--threads <N>`:** Number of CPU worker threads used when layers fall back to system memory.

---

## 2. Production Daemon Supervisors

In production, you never run `python main.py` or `./server` interactively in a bash shell. You supervisor-manage it with auto-restart and resource limits.

### A. Deploying via systemd (Native Linux Service)
1. Copy `inference.service` to `/etc/systemd/system/inference.service`.
2. Reload and enable:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now inference.service
   ```
3. Inspect state:
   ```bash
   systemctl status inference.service
   journalctl -u inference.service -f
   ```

### B. Deploying via PM2 (Process Manager)
1. Start via ecosystem configuration:
   ```bash
   pm2 start ecosystem.config.js
   pm2 logs inference-engine
   pm2 monit
   ```
2. Verify automated recovery: kill the process PID with `kill -9 <PID>` and verify that PM2 respawns the daemon within 500ms.

---

## 3. Verify the OpenAI-Compatible API
Test the raw HTTP completion endpoint:
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-coder:1.5b",
    "messages": [{"role": "user", "content": "Write a 3-line bash healthcheck."}],
    "temperature": 0.2
  }'
```
