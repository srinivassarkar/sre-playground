import asyncio
import time
import json
import statistics
import argparse
import httpx

URL = "http://localhost:8000/v1/chat/completions"
MODEL = "qwen2.5-coder:1.5b"
PROMPT = "Explain the difference between TCP TIME_WAIT and CLOSE_WAIT in three crisp bullet points."

async def send_stream(client, user_id, max_tokens=100):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}],
        "stream": True,
        "max_tokens": max_tokens,
        "temperature": 0.1
    }
    
    start_time = time.perf_counter()
    first_token_time = None
    token_timestamps = []
    total_tokens = 0

    try:
        async with client.stream("POST", URL, json=payload, timeout=60.0) as resp:
            if resp.status_code != 200:
                print(f"[User {user_id}] HTTP {resp.status_code}")
                return None
                
            async for line in resp.aiter_lines():
                if not line or not line.startswith("data: "):
                    continue
                data_str = line[6:].strip()
                if data_str == "[DONE]":
                    break
                
                try:
                    chunk = json.loads(data_str)
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        now = time.perf_counter()
                        if first_token_time is None:
                            first_token_time = now
                        token_timestamps.append(now)
                        total_tokens += 1
                except Exception:
                    continue

        end_time = time.perf_counter()
        if first_token_time is None or total_tokens < 2:
            return None

        ttft_ms = (first_token_time - start_time) * 1000
        gen_duration = end_time - first_token_time
        tps = total_tokens / gen_duration if gen_duration > 0 else 0
        
        itls = [
            (token_timestamps[i] - token_timestamps[i-1]) * 1000 
            for i in range(1, len(token_timestamps))
        ]
        avg_itl = statistics.mean(itls) if itls else 0

        return {
            "user": user_id,
            "tokens": total_tokens,
            "ttft_ms": ttft_ms,
            "tps": tps,
            "avg_itl_ms": avg_itl,
            "total_s": end_time - start_time
        }
    except Exception as e:
        print(f"[User {user_id}] Error: {e}")
        return None

async def main(concurrency):
    print(f"============================================================")
    print(f"⚡ INFERENCE STREAMING BENCHMARK: Concurrency = {concurrency}")
    print(f"============================================================")
    
    limits = httpx.Limits(max_keepalive_connections=concurrency, max_connections=concurrency*2)
    async with httpx.AsyncClient(limits=limits) as client:
        tasks = [send_stream(client, i) for i in range(concurrency)]
        results = await asyncio.gather(*tasks)

    valid = [r for r in results if r is not None]
    if not valid:
        print("❌ All requests failed. Is your inference server running on port 8000?")
        return

    ttfts = sorted([r["ttft_ms"] for r in valid])
    tpss = [r["tps"] for r in valid]
    itls = [r["avg_itl_ms"] for r in valid]
    totals = sorted([r["total_s"] for r in valid])

    print(f"Success Rate:            {len(valid)}/{concurrency} ({(len(valid)/concurrency)*100:.1f}%)")
    print(f"Average Tokens Emitted:  {statistics.mean([r['tokens'] for r in valid]):.1f}")
    print(f"------------------------------------------------------------")
    print(f"1. TTFT (Time To First Token / Prefill Phase):")
    print(f"   - Min (Fastest):      {min(ttfts):.1f} ms")
    print(f"   - Median (p50):       {statistics.median(ttfts):.1f} ms")
    print(f"   - p90:                {ttfts[int(len(ttfts)*0.9)]:.1f} ms")
    print(f"   - p99:                {ttfts[-1]:.1f} ms")
    print(f"2. Generation Throughput (Decode Phase):")
    print(f"   - Mean Stream TPS:    {statistics.mean(tpss):.1f} tokens/sec")
    print(f"   - Aggregate Node TPS: {sum(tpss):.1f} tokens/sec")
    print(f"   - Inter-Token Delay:  {statistics.mean(itls):.1f} ms/token")
    print(f"3. E2E Duration:")
    print(f"   - p50 Latency:        {statistics.median(totals):.2f} s")
    print(f"============================================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", type=int, default=5)
    args = parser.parse_args()
    asyncio.run(main(args.concurrency))
