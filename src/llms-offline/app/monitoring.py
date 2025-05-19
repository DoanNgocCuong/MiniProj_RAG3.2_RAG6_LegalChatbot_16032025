import torch
import psutil
import logging
from datetime import datetime

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_gpu_memory_info():
    """Lấy thông tin sử dụng VRAM của GPU"""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated() / 1024**3  # GB
        reserved = torch.cuda.memory_reserved() / 1024**3    # GB
        return {
            'allocated_gb': round(allocated, 2),
            'reserved_gb': round(reserved, 2),
            'device_name': torch.cuda.get_device_name(0)
        }
    return None

def get_system_memory_info():
    """Lấy thông tin sử dụng RAM của hệ thống"""
    memory = psutil.virtual_memory()
    return {
        'total_gb': round(memory.total / 1024**3, 2),
        'used_gb': round(memory.used / 1024**3, 2),
        'percent': memory.percent
    }

def log_resource_usage(operation: str):
    """Log thông tin sử dụng tài nguyên"""
    gpu_info = get_gpu_memory_info()
    mem_info = get_system_memory_info()
    
    log_msg = f"[{operation}] "
    if gpu_info:
        log_msg += f"GPU: {gpu_info['device_name']} - VRAM: {gpu_info['allocated_gb']}GB (allocated) / {gpu_info['reserved_gb']}GB (reserved) | "
    log_msg += f"RAM: {mem_info['used_gb']}GB/{mem_info['total_gb']}GB ({mem_info['percent']}%)"
    
    logger.info(log_msg)

def clear_gpu_memory():
    """Xóa cache GPU một cách an toàn"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        logger.info("GPU memory cache cleared") 