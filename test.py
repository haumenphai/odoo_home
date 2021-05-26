# result = self._exec('free')
# output = result.output
def test1():
    output = """total        used        free      shared  buff/cache   available
Mem:        8043444     6342964      275848      435236     1424632      962096
Swap:       2097148     1348352      748796
    """
#     output = """total        used        free      shared  buff/cache   available
# Mem:          7,7Gi       6,0Gi       284Mi       439Mi       1,4Gi       940Mi
# Swap:         2,0Gi       1,3Gi       700Mi
#     """
    mem_txt = output.split('\n')[1]
    mem_list = mem_txt[5::].strip().split()

    mem_used = float(mem_list[1]) / float(mem_list[0]) * 100
    mem_used_txt = str(round(mem_used)) + ' %'
    print(mem_used_txt)

# test1()

def test2():
    output = """top - 01:36:42 up 37 min,  1 user,  load average: 1.08, 1.52, 1.59
Tasks:  48 total,   1 running,  47 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   7854.9 total,   7537.2 free,    207.1 used,    110.6 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   7647.8 avail Mem 
"""
    available_cpu = output.split('\n')[2].split(',')[3].replace(' id', '')
    cpu_used = 100 - float(available_cpu)
    cpu_used_txt = str(cpu_used) + ' %'
    print(cpu_used_txt)

def test3():
    body = "Server %s\nCpu used: %s\nRam: %s\nDetail:\n%s" % ('1', '2', '3', 'aaa')
    print(body)
test3()