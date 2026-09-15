# Lab 01 — VRAM Budgeting & The CUDA OOM Boundary

**Objective:** Understand how model parameters, quantization precision, and KV cache context allocate physical GPU memory. Learn to calculate memory requirements before loading and reproduce a deterministic `CUDA out of memory` failure.

---

## 1. The VRAM Formula (Memorize This)

$$\text{Total VRAM Required} = \text{Model Weights} + \text{KV Cache Memory} + \text{CUDA Runtime Context (}\approx 400\text{MB)}$$

### A. Model Weights
$$\text{Weight VRAM (GB)} \approx \text{Parameters (Billions)} \times \text{Bytes per Parameter}$$
* **FP16 / BF16 (16-bit):** 2.0 bytes / param $\implies$ 7B model requires $\approx$ **14 GB**.
* **INT8 (8-bit):** 1.0 byte / param $\implies$ 7B model requires $\approx$ **7 GB**.
* **Q4_K_M (4-bit):** $\approx$ 0.55 bytes / param $\implies$ 7B model requires $\approx$ **3.9 GB**; a 1.5B model requires $\approx$ **1.1 GB**.

### B. KV Cache Memory (The Dynamic Variable)
$$\text{KV Cache (Bytes)} = 2 \times \text{Layers} \times \text{Heads} \times \text{HeadDim} \times \text{BytesPerVal} \times \text{ContextLength} \times \text{ConcurrentRequests}$$
Every active user session and every token of context consumes physical memory that persists across the generation stream.

---

## 2. Hands-On Exercises

### Exercise 1: Run the VRAM Calculator
```bash
python vram_calculator.py --params 1.5 --precision q4 --context 4096 --concurrency 5
```
Inspect the output. Compare a 1.5B model against a 7B model on a 4GB GPU.

### Exercise 2: Observe Clean Allocation on 4GB VRAM
1. Download a lightweight 1.5B 4-bit model:
   ```bash
   curl -L -o qwen2.5-coder-1.5b-instruct-q4_k_m.gguf \
     https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF/resolve/main/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf
   ```
2. Run `nvidia-smi` in watch mode:
   ```bash
   watch -n 0.5 nvidia-smi
   ```
3. Load the model with all layers offloaded to GPU:
   ```bash
   ./llama-server -m qwen2.5-coder-1.5b-instruct-q4_k_m.gguf -ngl 99 -c 2048 --port 8000
   ```
4. Observe memory jump from ~9 MiB to $\approx$ 1,450 MiB. The model fits comfortably with 2.5 GB headroom for KV Cache.

### Exercise 3: Trigger and Diagnose a Real `CUDA Out of Memory`
1. Attempt to force an 8B model or an oversized context window (`-c 32768` with large batch size) that exceeds 4096 MiB:
   ```bash
   ./llama-server -m qwen2.5-coder-1.5b-instruct-q4_k_m.gguf -ngl 99 -c 65536 -b 2048 --port 8000
   ```
2. Observe the terminal failure:
   ```
   ggml_cuda_init: allocating KV cache failed (out of memory)
   CUDA error: out of memory
   ```
3. **Key Lesson:** In production, you must set strict context bounds (`-c` or `--max-model-len`) to guarantee that concurrent requests cannot trigger unhandled CUDA allocations.
