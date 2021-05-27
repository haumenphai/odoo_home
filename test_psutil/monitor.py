"""
[Unit]
Description=Monitor Server Ram, Cpu, Disk
After=multi-user.target
[Service]
Type=simple
ExecStart=/home/do/Desktop/file/service/.venv/bin/python3 /home/do/Desktop/file/service/monitor_disk_ram.py
ExecStop=/bin/kill -s QUIT $MAINPID
[Install]
WantedBy=multi-user.target

"""
from collections import namedtuple
import psutil, time, datetime, threading
from threading import Thread

RamInfo = namedtuple('RamInfo', ['total', 'available', 'used', 'free', 'ram_percent', 'ram_percent_txt', 'ram'])


def truncate(num, n):
    integer = int(num * (10 ** n)) / (10 ** n)
    return float(integer)


def current_milli_time():
    return round(time.time() * 1000)


def byte_to_gigabyte(byte):
    return byte / 1024 ** 3


def get_ram_info():
    ram = psutil.virtual_memory()
    swap_ram = psutil.swap_memory()

    return {
        'ram_total': truncate(byte_to_gigabyte(ram.total), 2),
        'ram_available': truncate(byte_to_gigabyte(ram.available), 2),
        'ram_used': truncate(byte_to_gigabyte(ram.used), 2),
        'ram_free': truncate(byte_to_gigabyte(ram.free), 2),
        'ram_percent': ram.percent,
        'ram_percent_txt': str(ram.percent) + ' %',
        'swap_ram_total': truncate(byte_to_gigabyte(swap_ram.total), 2),
        'swap_ram_used': truncate(byte_to_gigabyte(swap_ram.used), 2),
        'swap_ram_free': truncate(byte_to_gigabyte(swap_ram.free), 2),
        'swap_ram_percent': swap_ram.percent,
        'swap_ram_percent_txt': str(swap_ram.percent) + ' %',
        'ram': ram,
        'swap_ram': swap_ram
    }


def get_disk_info():
    disk = psutil.disk_usage('/')
    return {
        'disk_total': truncate(byte_to_gigabyte(disk.total), 2),
        'disk_used': truncate(byte_to_gigabyte(disk.used), 2),
        'disk_free': truncate(byte_to_gigabyte(disk.free), 2),
        'disk_percent': disk.percent,
        'disk_percent_txt': str(disk.percent) + ' %',
        'disk': disk
    }


folder_save = '/home/do/Desktop/file/'
file_disk = folder_save + 'disk.txt'
file_ram = folder_save + 'ram.txt'
file_cpu = folder_save + 'cpu.txt'
repeat_time = 1  # thời gian monitor lặp lại [ram, disk, cpu_prenc
# đo lường mức độ sử dụng tài nguyên trung bình trong một khoảng thời gian mesure_workload (giây) để đưa ra cảnh báo
mesure_workload = 10

ram_warning = 50
disk_warning = 90
cpu_warning = 90


def start_monitor_ram_and_disk():
    list_avg_ram = []
    list_avg_disk = []
    with open(file_disk, 'w', encoding='utf-8') as f:
        f.write('disk_free,disk_used,percent\n')
    with open(file_ram, 'w', encoding='utf-8') as f:
        f.write('ram_free,ram_used,ram_percent\n')

    while True:
        if len(list_avg_disk) >= mesure_workload / repeat_time:
            avg_ram = sum(list_avg_ram) / len(list_avg_ram)
            avg_disk = sum(list_avg_disk) / len(list_avg_disk)

            print(avg_ram)
            print(avg_disk)
            if avg_ram > ram_warning:
                # TODO: warning ram overload
                print(f'Ram overload {datetime.datetime.now()}')
            if avg_disk > disk_warning:
                # TODO: warning disk overload
                print(f'Disk overload {datetime.datetime.now()}')

            list_avg_ram.clear()
            list_avg_disk.clear()

        disk = get_disk_info()
        list_avg_disk.append(disk['disk_percent'])
        result = str(disk['disk_free']) + ',' + str(disk['disk_used']) + ',' + str(disk['disk_percent']) + '\n'
        with open(file_disk, 'a', encoding='utf-8') as f:
            f.write(result)
        print('monitor disk', result)

        print(threading.current_thread())

        ram = get_ram_info()
        list_avg_ram.append(ram['ram_percent'])
        result = str(ram['ram_free']) + ',' + str(ram['ram_used']) + ',' + str(ram['ram_percent']) + '\n'
        with open(file_ram, 'a', encoding='utf-8') as f:
            f.write(result)
        print('monitor ram', result)

        time.sleep(repeat_time)


def start_monitor_cpu():
    with open(file_cpu, 'w', encoding='utf-8') as f:
        f.write('percent\n')

    while True:
        percent = psutil.cpu_percent(interval=repeat_time)
        with open(file_cpu, 'a', encoding='utf-8') as f:
            f.write(str(percent) + '\n')
        print('monitor cpu:', percent)
        print(threading.current_thread())


def start_montior_warning_cpu():
    while True:
        percent = psutil.cpu_percent(interval=mesure_workload)
        if percent >= cpu_warning:
            # TODO: Warning
            print(f'Disk overload {datetime.datetime.now()}')
        print('warning cpu:', percent)

if __name__ == '__main__':
    thread_ram_disk = threading.Thread(target=start_monitor_ram_and_disk, name='Thread Monitor Ram Disk')
    thread_monitor_cpu = Thread(target=start_monitor_cpu, name='Thread Monitor Cpu')
    thread_warning_cpu = Thread(target=start_montior_warning_cpu, name='Thread Warning Cpu')

    thread_ram_disk.start()
    thread_monitor_cpu.start()
    thread_warning_cpu.start()
