from matplotlib import pyplot as plt
from tabulate import tabulate

num_process = int(input("Number of process: "))
quantum = int(input("Enter the quantum value: "))

process = []

for i in range(num_process):
    process_id = i
    arrival = float(input(f"Enter arrival time of process {process_id}: "))
    burst = float(input(f"Enter burst time of process {process_id}: "))
    entry_time = -1
    exit_time = -1
    work_done = 0
    data = [process_id, arrival, burst, entry_time, exit_time, work_done]
    process.append(data)

process.sort(key=lambda x: x[1])

time = 0.0
process_schedule = []
waiting_time = []
turnaround_time = []
system_idle = 0

while True:
    for i in range(num_process):
        if time < process[i][1]:
            system_idle += abs(time - process[i][1])
            time = process[i][1]

        remaining = process[i][2] - process[i][5]
        if remaining <= 0:
            continue

        if remaining < quantum:
            process[i][5] += remaining
            time += remaining
        else:
            process[i][5] += quantum
            time += quantum

        process[i][4] = time
        process_schedule.append(f"P{process[i][0]} = {time}")

    if all(process[i][5] == process[i][2] for i in range(num_process)):
        break

# Calculate turnaround and waiting time
for i in range(num_process):
    tat = process[i][4] - process[i][1]
    wt = tat - process[i][2]
    turnaround_time.append(tat)
    waiting_time.append(wt)

#table
table = []
for i in range(num_process):
    table.append([
        f"P{process[i][0]}", process[i][1], process[i][2], process[i][4],
        turnaround_time[i], waiting_time[i]
    ])

headers = ["Process", "Arrival Time", "Burst Time", "Completion Time", "Turnaround Time", "Waiting Time"]

print("\nRound Robin Scheduling Results:")
print(tabulate(table, headers=headers, tablefmt="pretty"))

#process execution order
print("\nProcess Execution Order:")
print(" -> ".join(process_schedule))

#chart
plt.barh(y=[p[0] for p in process], width=[p[2] for p in process], left=[p[1] for p in process])
plt.xlabel("Time")
plt.ylabel("Process")
plt.title("Round Robin Scheduling (Approximate)")
plt.show()


'''
5
2
0
2
0
1
0
8
0
4
0
5

5
2
0
5
0
3
0
1
0
7
0
4
'''
