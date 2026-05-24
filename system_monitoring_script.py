import os , shutil  , time
def parse_cpu_stat():
        with open ('/proc/stat', 'r') as file:
            first_line = file.readline()
            matched_list  = first_line.split()
            matched_list.pop(0)
            idle_time = int(matched_list[3])+ int(matched_list[4])
            total_sum = 0
            for num in matched_list:
                  total_sum += int(num)

        return total_sum, idle_time 

store = []
def queue(value):
    if  len(store) < 2:
        store.append(value)
    elif len(store) == 2 :
          store.pop(0)
          store.append(value)
    return None


# calculates CPU percentage 
def get_cpu_percentage(store):
    if len(store) <2 :
         return None 
    old_total ,old_idle = store[0]
    new_total , new_idle = store[1]

    total_diff = new_total  - old_total
    idle_diff = new_idle - old_idle

    if total_diff == 0:
        return "CPU usage: 0.00%"
    
    cpu_usage = ((total_diff - idle_diff)/total_diff)*100 
    return cpu_usage 
 




 # read meminfo file       
def get_memory_percent():
        info= {}
        with open('/proc/meminfo', 'r') as file_1:
            # reads only five lines of the mentioned file. 
            for count , line in enumerate(file_1):
                if count ==5 :
                     break
                lines = line.split()
                if len(lines) >= 2:
                     keys = lines[0].strip(':')
                     value = int(lines[1])
                info[keys] = value
            ram_usage = ((info['MemTotal'] - info['MemAvailable'])/info['MemTotal'])*100
            return ram_usage 
        



def Disk_used():
    total , used , free = shutil.disk_usage("/")

    # bytes to gb
    gb_total = total/(1024**3)
    gb_used = used/(1024**3)
    gb_free = free / (1024**3)

    disk_usage = (gb_used /gb_total)*100


    print(f'Percentage of Memory used: {disk_usage:.2f}%')
    print(f'Total available memory: {gb_total:.2f}GB')
    print(f'Memmory used: {gb_used:.2f}GB')
    print(f'Avaliable memory: {gb_free:.2f}GB')
    return disk_usage





def check_thresholds(cpu_usage: float, ram_usage: float, disk_usage: float) -> None:
    # Check system metrics and print alerts if thresholds are exceeded
    thresholds = {
        "cpu": 80.0, 
        "memory": 85.0, 
        "disk": 80.0
    }
    if cpu_usage is not None and cpu_usage >= thresholds["cpu"] :
            print(f"[ALERT] CPU usage is high: {cpu_usage:.2f}%")

    if ram_usage >= thresholds["memory"]:
        print(f"[ALERT] RAM usage is high: {ram_usage:.2f}%")

    if disk_usage >= thresholds["disk"]:
        print(f"[ALERT] Disk usage is high: {disk_usage:.2f}%")
 


while True:
    value_1 = parse_cpu_stat()
    queue(value_1)   
    CPU_usage = get_cpu_percentage(store)
    if  CPU_usage is not None :
        print(f"CPU usage: {CPU_usage:.2f}%")

    RAM_usage = get_memory_percent()
    print(RAM_usage)

    DISK_usage = Disk_used()

    check_thresholds(CPU_usage,RAM_usage,DISK_usage)
    
    print('\n')
    time.sleep(2)