module.exports = {
  apps: [{
    name: "inference-engine",
    script: "./llama-server",
    args: "-m ./qwen2.5-coder-1.5b-instruct-q4_k_m.gguf -ngl 99 -c 2048 -b 512 --host 127.0.0.1 --port 8000",
    cwd: "/home/practice/inference",
    instances: 1,
    autorestart: true,
    max_memory_restart: "3500M",
    watch: false,
    env: {
      CUDA_VISIBLE_DEVICES: "0"
    }
  }]
};
