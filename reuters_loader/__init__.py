REUTERS_PATH = ''

from .loader import loadReutersFiles
from .tokenizer import *
import time 

docs = {}
start_time = time.perf_counter() # Use perf_counter for more precise measurements
docs = loadReutersFiles(REUTERS_PATH)
end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Parsed files in {elapsed_time:.4f} seconds")






