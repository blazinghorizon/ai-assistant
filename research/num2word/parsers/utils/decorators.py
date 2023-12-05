import gc
import torch
from typing import Callable

def collect_cache() -> None:
    torch.cuda.empty_cache()
    gc.collect()

def free_cache(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        collect_cache()
        return result
    
    return wrapper