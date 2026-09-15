# The Systems Engineer's Guide to AI/ML Fundamentals

**Author:** Srinivas Sarkar  
**Target:** Platform Engineers, DevOps Engineers, and SREs entering AI Infrastructure  
**Scope:** Plain-English, zero-math definitions of every essential AI/ML concept mapped to physical systems, memory, and networking realities.

---

## 1. The Core Data Units

| AI / ML Concept | What It Actually Is (Systems Translation) | Why Infrastructure Engineers Care |
| :--- | :--- | :--- |
| **Token** | A discrete chunk of text (~4 characters or 0.75 words). For example, `DevOps` is 2 tokens (`Dev` + `Ops`). | All throughput, pricing, context budgeting, and latency metrics are measured in tokens (Tokens/Sec, TTFT). |
| **Context Window** | The maximum memory buffer (Prompt + Generated Output) an LLM can hold during a single request (e.g. 4k, 8k, 32k, 128k tokens). | Direct linear driver of **KV Cache VRAM consumption**. Larger context limits risk sudden CUDA Out-of-Memory crashes. |
| **Parameters (e.g. 7B, 70B)** | The number of frozen floating-point numbers (weights) that make up the neural network. (7B = 7 Billion floats). | Determines the **minimum static RAM/VRAM floor** needed to load the model into hardware. |
| **Weights** | The static arrays of numbers saved inside binary files (`.safetensors`, `.gguf`, or `.onnx`). | The actual static build artifact you download, copy via `rsync`, and mount into inference containers. |

---

## 2. The AI Lifecycle: Where Platform Engineers Live

```
[ Pre-Training ] ──► [ Fine-Tuning (LoRA/SFT) ] ──► [ Inference / Serving ]
 10,000+ GPUs           Specializing on data             Deploying the frozen
 (OpenAI, Meta)         (Data Science / ML)               weights in production
   ❌ NOT YOU               ❌ NOT YOU                     ✅ YOUR ARENA (100%)
```

* **Pre-Training:** Training a foundation model from scratch. Requires massive clusters, high-speed InfiniBand networking, and months of compute. Handled by a handful of research frontier labs.
* **Fine-Tuning:** Taking an existing frozen base model and adjusting a small subset of weights on domain-specific datasets (e.g., medical or code data). Handled by internal ML researchers.
* **Inference (Serving):** Loading the finished, frozen model into memory to answer live user requests via HTTP/gRPC APIs in real time. **This is 100% Platform Engineering and Systems Operations.**

---

## 3. Precision, Bit-Width & Quantization

Quantization is the process of compressing model weights from high-precision floating-point representations to lower-bit integers.

| Format / Precision | Bytes per Weight | Memory Required (7B Model) | Operational Trade-Off |
| :--- | :--- | :--- | :--- |
| **FP32 (Single Precision)** | 4.0 bytes | ~28 GB | Maximum numerical precision; completely wasteful for inference. |
| **FP16 / BF16 (Half Precision)** | 2.0 bytes | ~14 GB | Industry standard baseline for datacenter inference (A100/H100). |
| **INT8 (8-bit Quantized)** | 1.0 byte | ~7.0 GB | 50% memory reduction with negligible perceptual accuracy loss. |
| **INT4 / Q4_K_M (4-bit)** | ~0.55 bytes | ~3.9 GB | 75% memory reduction; enables running 7B models on 4GB consumer GPUs or Apple Silicon. |

### Common Weight Formats:
* **GGUF:** Unified single-file binary format (weights + architecture metadata) optimized for fast CPU/Metal/consumer GPU inference via `llama.cpp`.
* **AWQ / GPTQ:** 4-bit quantization formats optimized specifically for NVIDIA Tensor Cores in production engines like `vLLM`.
* **Safetensors:** Fast, memory-mapped (`mmap`) format developed by Hugging Face that eliminates arbitrary code execution risks found in legacy Python pickle files.

---

## 4. Generation Mechanics & Memory Physics

### A. Autoregressive Generation (Why Responses Take Seconds)
LLMs do not generate full sentences at once. They predict **one single token at a time**, append that token to their prompt, and feed the entire sequence back into the model to predict the next token until an end-of-sequence token (`[DONE]`) is emitted.
* **Consequence:** Requests take seconds to complete, requiring **Server-Sent Events (SSE)** or WebSockets for real-time streaming to users.

### B. The KV Cache (Key-Value Cache)
During generation, recalculating past attention values for earlier tokens is an $O(N^2)$ operation. To make generation fast, the engine caches intermediate attention tensors (Keys and Values) in physical memory.
* **Systems Translation:** The KV Cache is a **dynamically growing in-memory state buffer** allocated per active user stream.
* **The Failure Mode:** If many concurrent users hold long context windows, the KV Cache exhausts remaining VRAM, causing an immediate kernel or CUDA Out-of-Memory (OOM) termination.

### C. Prefill vs. Decode (The Two Latency Phases)
1. **Prefill Phase (Prompt Evaluation):** The model ingests the entire input prompt simultaneously.
   * *Hardware Profile:* **Compute-Bound** (GPU cores at 100% matrix multiplication).
   * *Telemetry Metric:* **TTFT (Time To First Token)**.
2. **Decode Phase (Token Streaming):** The model emits tokens one-by-one.
   * *Hardware Profile:* **Memory-Bandwidth Bound** (reading all weights from memory to compute units per token).
   * *Telemetry Metric:* **TPS (Tokens Per Second)** and **ITL (Inter-Token Latency)**.

---

## 5. RAG & Vector Databases

Retrieval-Augmented Generation (RAG) is an architectural pattern that connects LLMs to external, private company data without retraining the model.

```
1. User Query: "How do I restart the database?"
       │
       ▼
2. Embedding Model: Converts text into a 1536-dimensional float vector.
       │
       ▼
3. Vector Database (Qdrant): Searches high-dimensional space for nearest matching document vectors.
       │
       ▼
4. Context Injection: Injects matching documentation snippets into the prompt.
       │
       ▼
5. LLM Completion: Answers accurately using the injected company context without hallucinating.
```

* **Embedding:** A mathematical function that maps text into semantic coordinates (vectors).
* **Vector Database:** An indexing engine (like **Qdrant**, Pinecone, or Milvus) that uses algorithms like **HNSW (Hierarchical Navigable Small World)** to perform fast approximate nearest-neighbor search across millions of vectors.

---

## 6. Sampling & Decoding Parameters

These are runtime parameters passed in HTTP request payloads that control how the model selects its next token:

* **Temperature (0.0 to 1.0):**
  * `0.0 – 0.2`: Sharpens probability distribution. Picks the mathematically highest probability token. Essential for coding, JSON output, and factual extraction.
  * `0.7 – 1.0`: Flattens probability distribution. Allows lower-probability tokens to be picked, generating varied and creative responses.
* **Top-P (Nucleus Sampling):** Selects candidate tokens only from the top cumulative probability mass (e.g. `0.90`), dynamically trimming unlikely tail tokens.
* **Top-K:** Restricts candidate selection to the top $K$ most likely tokens (e.g. top 40).

---

## 7. Agents, Tools & Function Calling

* **Function / Tool Calling:** LLMs cannot execute code or query APIs directly. 
  * The application provides a JSON schema defining available tools.
  * The model outputs a structured JSON payload: `{"tool": "execute_query", "params": {"sql": "..."}}`.
  * The backend platform executes the call and returns the output to the LLM.
* **AI Agent (e.g. LangGraph):** An autonomous execution loop where an LLM repeatedly analyzes a task, selects tools, inspects outputs, and iterates until the objective is reached.

---

## 8. The Rosetta Stone: AI Terms ⟶ Systems Equivalents

| AI / ML Concept | Classical Systems / DevOps Equivalent |
| :--- | :--- |
| **Model Weights** | Static binary artifact / executable image |
| **KV Cache** | In-memory session state / cache buffer |
| **PagedAttention** | Linux Virtual Memory Paging |
| **Continuous Batching** | Dynamic OS Process Scheduling |
| **Quantization** | Binary compression / reduced data types |
| **Embedding** | Hash / high-dimensional indexing key |
| **RAG** | Database query + template rendering |
| **TTFT (Time To First Token)** | Request Queue Wait Time + Initial Handshake Latency |
| **TPS (Tokens Per Second)** | Streaming I/O Throughput |
| **CUDA OOM** | Linux Kernel OOMKill (Exit Code 137) |
