import datetime
from collections import namedtuple
import psutil, time

RamInfo = namedtuple('RamInfo', ['total', 'available', 'used', 'free', 'ram_percent', 'ram_percent_txt', 'ram'])


def truncate(num, n):
    integer = int(num * (10**n)) / (10**n)
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
head_csv_disk = 'disk_free,disk_used,percent\n'
head_csv_ram = 'ram_free,ram_used,ram_percent\n'
repeat_time = 1 # thời gian monitor lặp lại
# đo lường mức độ sử dụng tài nguyên trung bình trong một khoảng thời gian mesure_workload (giây) để đưa ra cảnh báo
mesure_workload = 10

ram_warning = 50
disk_warning = 90


def start():
    list_avg_ram = []
    list_avg_disk = []
    with open(file_disk, 'w', encoding='utf-8') as f: f.write(head_csv_disk)
    with open(file_ram, 'w', encoding='utf-8') as f: f.write(head_csv_ram)

    while True:
        if len(list_avg_disk) >= mesure_workload / repeat_time:
            avg_ram = sum(list_avg_ram) / len(list_avg_ram)
            avg_disk = sum(list_avg_disk) / len(list_avg_disk)

            print(avg_ram)
            print(avg_disk)
            if avg_ram > ram_warning:
                # TODO: warning ram overload
                print(f'Ram overload {datetime.datetime.now()}')
                pass
            if avg_disk > disk_warning:
                # TODO: warning disk overload
                print(f'Disk overload {datetime.datetime.now()}')
                pass

            list_avg_ram.clear()
            list_avg_disk.clear()

        disk = get_disk_info()
        list_avg_disk.append(disk['disk_percent'])
        result = str(disk['disk_free']) + ',' + str(disk['disk_used']) + ',' + str(disk['disk_percent']) + '\n'
        with open(file_disk, 'a', encoding='utf-8') as f:
            f.write(result)

        ram = get_ram_info()
        list_avg_ram.append(ram['ram_percent'])
        result = str(ram['ram_free']) + ',' + str(ram['ram_used']) + ',' + str(ram['ram_percent']) + '\n'
        with open(file_ram, 'a', encoding='utf-8') as f:
            f.write(result)

        time.sleep(repeat_time)

start()


