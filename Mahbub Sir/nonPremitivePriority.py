import matplotlib.pyplot as plt
from tabulate import tabulate
num_process = int(input("Number of process: "))

process = []

for i in range(num_process):
    #print("process :", i)
    process_id = i
    arrival = float(input(f"Enter arrival time of process {process_id}: "))
    burst = float(input(f"Enter burst time of process {process_id}: "))
    priority = float(input(f"Enter priority of process {process_id}: "))
    entry_time = -1
    exit_time = -1
    in_queue = False
    data = [process_id, arrival, burst, entry_time, exit_time, in_queue, priority]
    process.append(data)

process.sort(key=lambda x: x[6], reverse=True)
process.sort(key=lambda x: x[1])

time = 0.0
system_idle = 0
process_queue = []
process_schedule = []


def complete_process(i):
    global time, process, system_idle, process_queue, num_process

    for j in range(num_process):
        if process[j][0] == process_queue[0][0]:
            i = j
            break

    if time < process[i][1]:
        system_idle += abs(time - process[i][1])
        time = process[i][1]

    process_schedule.append(process_queue[0][0])
    process[i][3] = time
    time = time + process[i][2]
    process[i][4] = time

    process_queue.pop(0)

    for j in range(num_process):
        if process[j][1] <= time and process[j][5] == False:
            process[j][5] = True
            process_queue.append(process[j])

    process_queue.sort(key=lambda x: x[6], reverse=True)


x = 0
while len(process_schedule) < num_process:
    process[x][5] = True
    process_queue.append(process[x])
    while len(process_queue) != 0:
        complete_process(process_queue[0][0])
    for i in range(num_process):
        if not process[i][5]:
            x = i
            break

turnaround_time = []
waiting_time = []
process.sort(key=lambda x: x[3])

for i in range(num_process):
    turnaround_time.append(process[i][4] - process[i][1])
    waiting_time.append(turnaround_time[i] - process[i][2])

table = []
for i in range(num_process):
    table.append([
        f"P{process[i][0]}",         # Process ID
        process[i][1],               # Arrival Time
        process[i][2],               # Burst Time
        process[i][3],               # Start Time
        process[i][4],               # Finish Time
        turnaround_time[i],          # Turnaround Time
        waiting_time[i]              # Waiting Time
    ])

headers = ["Process", "Arrival", "Burst", "Start", "Finish", "Turnaround", "Waiting"]
print("\nScheduling Results:\n")
print(tabulate(table, headers=headers, tablefmt="pretty"))

raw_process_table = []
for i in range(num_process):
    raw_process_table.append([
        f"P{process[i][0]}",   # Process ID
        process[i][1],         # Arrival Time
        process[i][2],         # Burst Time
        process[i][6],         # Priority
        process[i][3],         # Start Time
        process[i][4],         # Finish Time
        process[i][5]          # In Queue (Final state, should be True)
    ])

raw_headers = ["Process", "Arrival", "Burst", "Priority", "Start", "Finish", "In Queue"]
print("\nRaw Process Data:\n")
print(tabulate(raw_process_table, headers=raw_headers, tablefmt="pretty"))

print("Total System Idle = ", system_idle)
print("System Utilization = ", ((time - system_idle) / time) * 100)

plt.barh(y=process_schedule, width=[i[2] for i in process], left=[i[3] for i in process])
plt.show()

'''
3
0
5
5
1
2
5
3
3
10
'''
