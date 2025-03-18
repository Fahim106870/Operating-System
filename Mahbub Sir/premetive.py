import matplotlib.pyplot as plt
from tabulate import tabulate

num_process = int(input("Number of processes: "))
process = []

for i in range(num_process):
    process_id = i
    arrival = int(input(f"Enter arrival time of process {process_id}: "))
    burst = int(input(f"Enter burst time of process {process_id}: "))
    priority = int(input(f"Enter priority of process {process_id}: "))
    entry_time = -1
    exit_time = -1
    work_done = 0
    data = [process_id, arrival, burst, priority, entry_time, exit_time, work_done]
    process.append(data)

# Sort highest priority first
process.sort(key=lambda x: x[3], reverse=True)

timeline = [-1 for i in range(500)]
start = 0
for i in range(num_process):
    cnt = 0
    start = process[i][1]
    while cnt < process[i][2]:
        while timeline[start] != -1:
            start += 1
        if timeline[start] == -1:
            timeline[start] = process[i][0]
            process[i][5] = start + 1
            cnt += 1
        start += 1

timeline = timeline[0:start]

# Calculate turnaround and waiting times
turnaround_time = []
waiting_time = []

# Sort
process.sort(key=lambda x: x[0])
for i in range(num_process):
    turnaround_time.append(process[i][5] - process[i][1])
    waiting_time.append(turnaround_time[i] - process[i][2])

#tabulation
table = []
for i in range(num_process):
    table.append([
        f"P{process[i][0]}",
        process[i][1],           # Arrival Time
        process[i][2],           # Burst Time
        process[i][3],           # Priority
        process[i][5],           # Exit Time
        turnaround_time[i],      # Turnaround Time
        waiting_time[i]          # Waiting Time
    ])

headers = ["Process", "Arrival Time", "Burst Time", "Priority", "Exit Time", "Turnaround Time", "Waiting Time"]

# table and cht
print("\nProcess Execution Results:\n")
print(tabulate(table, headers=headers, tablefmt="pretty"))
plt.figure(figsize=(10, 5))
last_time = 0
for process_id in timeline:
    plt.barh(f"P{process_id}", 1, left=last_time)
    last_time += 1

plt.xlabel("Time")
plt.ylabel("Processes")
plt.title("Process Execution Gantt Chart")
plt.show()


'''

3
0
4
4
2
4
10
3
2
1

'''
