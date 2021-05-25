
import psutil

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


x = psutil.disk_usage('/')
# cpu_used = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory()

# print('cpu percent', cpu_used)
ram_total = truncate(ram.total / 1024**3, 1)
ram_used = truncate(ram.used / 1024**3, 1)
ram_free = ram_total - ram_used
print(ram_total, ram_used, ram_free)
print(x)
