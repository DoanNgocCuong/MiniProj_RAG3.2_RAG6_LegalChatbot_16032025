2025-05-20 01:09:32.264 | 2025-05-19 18:09:32 | [Before model load] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 0.0GB (allocated) / 0.0GB (reserved) | RAM: 1.89GB/7.63GB (28.5%)
2025-05-20 01:09:33.831 | 2025-05-19 18:09:33 | We will use 90% of the memory on device 0 for storing the model, and 10% for the buffer to avoid OOM. You can set `max_memory` in to a higher value to use more memory (at your own risk).
2025-05-20 01:14:17.323 | 
2025-05-20 01:14:17.351 | 2025-05-19 18:14:17 | [After model load] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.98GB (allocated) / 6.59GB (reserved) | RAM: 1.95GB/7.63GB (30.3%)
2025-05-20 01:14:17.359 | INFO:     Started server process [1]
2025-05-20 01:14:17.359 | INFO:     Waiting for application startup.
2025-05-20 01:14:17.360 | INFO:     Application startup complete.
2025-05-20 01:14:17.360 | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
2025-05-20 01:21:47.599 | INFO:     172.18.0.1:43368 - "GET /docs HTTP/1.1" 200 OK
2025-05-20 01:21:47.742 | INFO:     172.18.0.1:43368 - "GET /openapi.json HTTP/1.1" 200 OK
2025-05-20 01:21:56.255 | 2025-05-19 18:21:56 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.98GB (allocated) / 6.59GB (reserved) | RAM: 1.96GB/7.63GB (30.4%)
2025-05-20 01:21:56.264 | /app/app/inference.py:50: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
2025-05-20 01:21:56.264 |   with torch.cuda.amp.autocast():
2025-05-20 01:21:56.264 | `generation_config` default values have been modified to match model-specific defaults: {'bos_token_id': 128000, 'eos_token_id': [128001, 128008, 128009]}. If this is not desired, please set these values explicitly.
2025-05-20 01:22:00.770 | 2025-05-19 18:22:00 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.81GB/7.63GB (41.7%)
2025-05-20 01:22:00.773 | 2025-05-19 18:22:00 | GPU memory cache cleared
2025-05-20 01:22:00.774 | INFO:     172.18.0.1:43352 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:28:35.391 | 2025-05-19 18:28:35 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:28:39.925 | 2025-05-19 18:28:39 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.85GB/7.63GB (42.2%)
2025-05-20 01:28:39.927 | 2025-05-19 18:28:39 | GPU memory cache cleared
2025-05-20 01:28:39.928 | INFO:     172.18.0.1:52484 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:28:47.381 | 2025-05-19 18:28:47 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.2%)
2025-05-20 01:28:51.954 | 2025-05-19 18:28:51 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.85GB/7.63GB (42.2%)
2025-05-20 01:28:51.956 | 2025-05-19 18:28:51 | GPU memory cache cleared
2025-05-20 01:28:51.956 | INFO:     172.18.0.1:43490 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:29:01.423 | 2025-05-19 18:29:01 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.2%)
2025-05-20 01:29:06.224 | 2025-05-19 18:29:06 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:06.226 | 2025-05-19 18:29:06 | GPU memory cache cleared
2025-05-20 01:29:06.227 | INFO:     172.18.0.1:39902 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:29:22.833 | 2025-05-19 18:29:22 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:27.559 | 2025-05-19 18:29:27 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.84GB/7.63GB (42.0%)
2025-05-20 01:29:27.562 | 2025-05-19 18:29:27 | GPU memory cache cleared
2025-05-20 01:29:27.562 | INFO:     172.18.0.1:42740 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:29:43.758 | 2025-05-19 18:29:43 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:46.869 | 2025-05-19 18:29:46 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.6GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:46.872 | 2025-05-19 18:29:46 | GPU memory cache cleared
2025-05-20 01:29:46.872 | INFO:     172.18.0.1:50282 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:29:47.849 | 2025-05-19 18:29:47 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:52.174 | 2025-05-19 18:29:52 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:52.176 | 2025-05-19 18:29:52 | GPU memory cache cleared
2025-05-20 01:29:52.177 | INFO:     172.18.0.1:50282 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:29:54.945 | 2025-05-19 18:29:54 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:59.694 | 2025-05-19 18:29:59 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:29:59.696 | 2025-05-19 18:29:59 | GPU memory cache cleared
2025-05-20 01:29:59.697 | INFO:     172.18.0.1:50282 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:32:13.971 | 2025-05-19 18:32:13 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.85GB/7.63GB (42.1%)
2025-05-20 01:32:18.678 | 2025-05-19 18:32:18 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.84GB/7.63GB (42.0%)
2025-05-20 01:32:18.681 | 2025-05-19 18:32:18 | GPU memory cache cleared
2025-05-20 01:32:18.681 | INFO:     172.18.0.1:45634 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:32:19.910 | 2025-05-19 18:32:19 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.84GB/7.63GB (42.0%)
2025-05-20 01:32:24.279 | 2025-05-19 18:32:24 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.84GB/7.63GB (42.1%)
2025-05-20 01:32:24.283 | 2025-05-19 18:32:24 | GPU memory cache cleared
2025-05-20 01:32:24.283 | INFO:     172.18.0.1:45634 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:32:26.612 | 2025-05-19 18:32:26 | [Before generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.59GB (reserved) | RAM: 2.84GB/7.63GB (42.1%)
2025-05-20 01:32:31.120 | 2025-05-19 18:32:31 | [After generation] GPU: NVIDIA GeForce RTX 4060 Laptop GPU - VRAM: 5.99GB (allocated) / 6.61GB (reserved) | RAM: 2.84GB/7.63GB (42.1%)
2025-05-20 01:32:31.122 | 2025-05-19 18:32:31 | GPU memory cache cleared
2025-05-20 01:32:31.123 | INFO:     172.18.0.1:45634 - "POST /v1/generate HTTP/1.1" 200 OK
2025-05-20 01:43:00.801 | Loading checkpoint shards:   0%|          | 0/2 [00:00<?, ?it/s]
2025-05-20 01:43:00.801 | Loading checkpoint shards:  50%|█████     | 1/2 [03:36<03:36, 216.49s/it]
2025-05-20 01:43:00.801 | Loading checkpoint shards: 100%|██████████| 2/2 [04:43<00:00, 128.54s/it]
2025-05-20 01:43:00.801 | Loading checkpoint shards: 100%|██████████| 2/2 [04:43<00:00, 141.73s/it]