import argparse

def calculate_vram(params_b, precision, context_len, concurrency, layers=28, heads=16, head_dim=64):
    bytes_per_param = {
        "fp16": 2.0,
        "bf16": 2.0,
        "int8": 1.0,
        "q8": 1.05,
        "q4": 0.56,
        "q4_k_m": 0.58
    }.get(precision.lower(), 0.58)

    # Weights
    weights_gb = (params_b * 1e9 * bytes_per_param) / (1024**3)
    
    # KV Cache per token per request (FP16 = 2 bytes)
    # 2 (for K and V) * layers * heads * head_dim * 2 bytes
    bytes_per_token = 2 * layers * heads * head_dim * 2
    total_kv_bytes = bytes_per_token * context_len * concurrency
    kv_cache_gb = total_kv_bytes / (1024**3)
    
    cuda_overhead_gb = 0.35  # ~350 MB CUDA context / scratch
    total_gb = weights_gb + kv_cache_gb + cuda_overhead_gb

    print(f"============================================================")
    print(f"📊 VRAM BUDGET ESTIMATOR: {params_b}B Model ({precision.upper()})")
    print(f"   Context: {context_len} tokens | Concurrency: {concurrency} users")
    print(f"============================================================")
    print(f"1. Model Weights:      {weights_gb:.2f} GB")
    print(f"2. KV Cache (Dynamic): {kv_cache_gb:.2f} GB")
    print(f"3. CUDA/Scratch Base:  {cuda_overhead_gb:.2f} GB")
    print(f"------------------------------------------------------------")
    print(f"🎯 Total VRAM Needed:  {total_gb:.2f} GB ({total_gb*1024:.0f} MB)")
    print(f"============================================================")
    if total_gb > 4.0:
        print("❌ EXCEEDS 4GB VRAM (Will crash a GTX 1050 Ti with CUDA OOM!)")
    else:
        print(f"✅ FITS ON 4GB GPU ({4.0 - total_gb:.2f} GB VRAM headroom remaining)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", type=float, default=1.5, help="Model parameters in Billions")
    parser.add_argument("--precision", type=str, default="q4_k_m", choices=["fp16", "int8", "q4_k_m"])
    parser.add_argument("--context", type=int, default=2048, help="Context window length")
    parser.add_argument("--concurrency", type=int, default=1, help="Max concurrent streams")
    args = parser.parse_args()
    calculate_vram(args.params, args.precision, args.context, args.concurrency)
