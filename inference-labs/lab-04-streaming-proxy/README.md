# Lab 04 — Edge Ingress: Reverse Proxies, SSE Buffering & Timeout Tuning

**Objective:** Configure Nginx as a reverse proxy in front of an LLM inference daemon. Reproduce the catastrophic "Proxy Buffering Hang", fix it with streaming SSE directives, and calibrate timeouts to eliminate `504 Gateway Timeout` errors.

---

## 1. The Catastrophic "Proxy Buffering" Bug

By default, standard web proxies (Nginx, HAProxy, Envoy, AWS ALB) buffer responses from the upstream server until the entire body is received, optimizing network packets for static web pages.

**For an LLM streaming response, this destroys user experience:**
* The inference engine is actively generating tokens every 30ms.
* But the user stares at a blank screen for 8 seconds.
* Once the generation finishes (`[DONE]`), the proxy flushes the buffer and dumps the entire response at once.

---

## 2. The Nginx Configuration Fix

To enable true token-by-token streaming, you must explicitly disable proxy buffering on your inference locations:

```nginx
proxy_buffering off;
proxy_cache off;
proxy_set_header X-Accel-Buffering no;
```

Additionally, long reasoning chains or code generation requests can take 30–60 seconds. If `proxy_read_timeout` is left at the 60s default, complex generations terminate with **`504 Gateway Timeout`**. You must tune:

```nginx
proxy_read_timeout 300s;
proxy_connect_timeout 10s;
proxy_send_timeout 300s;
```

---

## 3. Hands-On Verification

1. Start Nginx with `nginx.conf`:
   ```bash
   nginx -c $(pwd)/nginx.conf
   ```
2. Test streaming directly through Nginx on port `80`:
   ```bash
   curl -N http://localhost/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "qwen2.5-coder:1.5b",
       "messages": [{"role": "user", "content": "Count from 1 to 20 slowly."}],
       "stream": true
     }'
   ```
   * The `-N` flag disables curl's internal buffering.
   * Verify that tokens stream onto your terminal in real time, character by character.
