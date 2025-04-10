Tôi sẽ phân tích cách đo lường tài nguyên của bot khi chạy local thông qua các khía cạnh:

1. **Q: Làm sao để đo CPU và Memory Usage?**
   ```bash
   # Linux/Mac
   top -pid $(pgrep -f "python rag_backend.py")
   
   # Windows (PowerShell)
   Get-Process -Name python | Where-Object {$_.CommandLine -like "*rag_backend.py*"} | Select-Object CPU,WorkingSet,PM
   ```

2. **Q: Đo lường API calls và costs?**
   - OpenAI API:
     ```python
     # Thêm logging vào rag_backend.py
     import logging
     
     logging.info(f"Token used: {response.usage.total_tokens}")
     logging.info(f"Estimated cost: ${response.usage.total_tokens * 0.002/1000}")
     ```
   
   - Qdrant API:
     ```python
     # Log số lượng vector searches
     logging.info(f"Vector search count: {search_count}")
     logging.info(f"Vector dimensions: {vector_dim}")
     ```

3. **Q: Đo Network Usage?**
   ```python
   # Thêm middleware để track requests
   from time import time
   
   def track_network():
       start = time()
       bytes_sent = 0
       bytes_received = 0
       
       # Track request size
       bytes_sent += len(request.data)
       
       # Track response size
       bytes_received += len(response.data)
       
       duration = time() - start
       logging.info(f"Request duration: {duration}s")
       logging.info(f"Data transferred: {(bytes_sent + bytes_received)/1024:.2f}KB")
   ```

4. **Q: Đo Storage Usage?**
   ```python
   import os
   
   def check_storage():
       vector_db_size = os.path.getsize("path/to/vector/db")
       model_size = os.path.getsize("path/to/model")
       cache_size = os.path.getsize("path/to/cache")
       
       total = vector_db_size + model_size + cache_size
       logging.info(f"Total storage used: {total/1024/1024:.2f}MB")
   ```

5. **Q: Performance Monitoring Script:**
   ```python
   import psutil
   import time
   
   def monitor_resources():
       while True:
           process = psutil.Process()
           
           # CPU
           cpu_percent = process.cpu_percent()
           
           # Memory
           memory_info = process.memory_info()
           ram_used = memory_info.rss / 1024 / 1024  # MB
           
           # Disk I/O
           io_counters = process.io_counters()
           
           logging.info(f"""
           Resource Usage:
           CPU: {cpu_percent}%
           RAM: {ram_used:.2f}MB
           Disk Read: {io_counters.read_bytes/1024/1024:.2f}MB
           Disk Write: {io_counters.write_bytes/1024/1024:.2f}MB
           """)
           
           time.sleep(60)  # Log every minute
   ```

6. **Q: Cost Estimation per Request:**
   ```python
   class CostTracker:
       def __init__(self):
           self.openai_cost_per_1k_tokens = 0.002
           self.qdrant_cost_per_query = 0.000001
           
       def calculate_request_cost(self, tokens_used, vector_searches):
           openai_cost = (tokens_used * self.openai_cost_per_1k_tokens) / 1000
           qdrant_cost = vector_searches * self.qdrant_cost_per_query
           return openai_cost + qdrant_cost
   ```

7. **Q: Dashboard để theo dõi:**
   ```python
   from flask import Flask
   from flask_cors import CORS
   import dash
   import dash_core_components as dcc
   import dash_html_components as html
   
   app = Flask(__name__)
   CORS(app)
   
   dash_app = dash.Dash(__name__, server=app)
   dash_app.layout = html.Div([
       dcc.Graph(id='resource-usage'),
       dcc.Graph(id='api-costs'),
       dcc.Graph(id='response-times'),
       dcc.Interval(id='interval', interval=5000)
   ])
   ```

Ước tính tài nguyên cần thiết cho local deployment:

1. **Minimum Requirements:**
   - CPU: 2 cores
   - RAM: 4GB
   - Storage: 2GB
   - Network: 10Mbps

2. **Recommended Requirements:**
   - CPU: 4 cores
   - RAM: 8GB
   - Storage: 5GB
   - Network: 50Mbps

3. **Cost Factors:**
   - OpenAI API calls
   - Vector database queries
   - Storage for embeddings
   - Network bandwidth

4. **Optimization Tips:**
   ```python
   # 1. Caching
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def get_embedding(text):
       return model.encode(text)
   
   # 2. Batch Processing
   def batch_process_queries(queries, batch_size=10):
       for i in range(0, len(queries), batch_size):
           batch = queries[i:i+batch_size]
           process_batch(batch)
   
   # 3. Resource Limits
   import resource
   
   def limit_memory():
       soft, hard = resource.getrlimit(resource.RLIMIT_AS)
       resource.setrlimit(resource.RLIMIT_AS, (8 * 1024 * 1024 * 1024, hard))
   ```

Bạn muốn tôi implement monitoring system nào trước để bắt đầu theo dõi resource usage?
