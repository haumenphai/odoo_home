import psutil

cpu_time = psutil.cpu_times()
print(cpu_time)

print(psutil.cpu_percent())
print(psutil.cpu_freq())
print(psutil.cpu_stats())
print(psutil.cpu_count())
print(psutil._cpu_times_deltas())