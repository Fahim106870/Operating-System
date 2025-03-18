import time
import matplotlib.pyplot as plt
from multiprocessing import Process, current_process
from tabulate import tabulate

def run_task(process_id, burst_time):
    """
    Simulates a process running with a specific burst time.
    """
    print(f"Process {process_id} started with burst time {burst_time}")
    time.sleep(burst_time)  # Simulate the process by sleeping for burst time
    print(f"Process {process_id} completed after {burst_time} seconds")

if __name__ == "__main__":
    # Get the number of processes
    num_process = int(input("Number of processes: "))
    process_data = []

    # Collect process data
    for i in range(num_process):
        arrival = float(input(f"Enter arrival time for process {i + 1}: "))
        burst = float(input(f"Enter burst time for process {i + 1}: "))
        process_data.append((i, arrival, burst))

    # Sort processes by arrival time for FCFS scheduling
    process_data.sort(key=lambda x: x[1])

    # Scheduling and Execution
    current_time = 0
    system_idle = 0
    process_schedule = []
    entry_times = []
    exit_times = []
    turnaround_time = []
    waiting_time = []
    processes = []

    for process_id, arrival, burst in process_data:
        if current_time < arrival:
            system_idle += arrival - current_time
            current_time = arrival

        # Start the external process for each task
        start_time = current_time
        process = Process(target=run_task, args=(process_id, burst))
        process.start()  # Start the process
        process.join()  # Wait for the process to finish (simulating FCFS)

        end_time = start_time + burst
        entry_times.append(start_time)
        exit_times.append(end_time)
        current_time = end_time
        process_schedule.append(process_id)
        processes.append(process)

        # Calculate turnaround and waiting time
        turnaround_time.append(end_time - arrival)
        waiting_time.append(turnaround_time[-1] - burst)

    # Display results in a table format
    table = []
    for i, (process_id, arrival, burst) in enumerate(process_data):
        table.append([
            f"P{process_id}",
            arrival,
            burst,
            entry_times[i],
            exit_times[i],
            turnaround_time[i],
            waiting_time[i]
        ])

    headers = ["Process", "Arrival", "Burst", "Start Time", "Exit Time", "Turnaround Time", "Waiting Time"]
    print("\nScheduling Results:")
    print(tabulate(table, headers=headers, tablefmt="pretty"))

    # Display system utilization
    print("\nProcess Execution Order:", process_schedule)
    print("Total System Idle Time:", system_idle)
    print("System Utilization:", ((current_time - system_idle) / current_time) * 100, "%")

    # Plot Gantt Chart
    plt.barh(
        y=[f"P{process_id}" for process_id, _, _ in process_data],
        width=[burst for _, _, burst in process_data],
        left=entry_times
    )
    plt.xlabel("Time")
    plt.ylabel("Process")
    plt.title("FCFS Scheduling Gantt Chart")
    plt.show()
