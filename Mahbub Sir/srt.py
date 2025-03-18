import time
import matplotlib.pyplot as plt


# Run the process for its burst time
def run_task(process_id, exec_time):
    time.sleep(exec_time)  # Simulate the process by sleeping for burst time


def srt(process_data):
    time_elapsed = 0
    process_schedule = []
    queue = []
    waiting_time = [0] * len(process_data)
    turnaround_time = [0] * len(process_data)
    remaining_burst = [burst for _, _, burst in process_data]
    entry_times = []
    exit_times = []
    processes = []

    # Sort processes by arrival time
    process_data.sort(key=lambda x: x[1])

    i = 0
    while i < len(process_data) or queue:
        # Add processes to the queue that have arrived by the current time
        while i < len(process_data) and process_data[i][1] <= time_elapsed:
            queue.append(process_data[i])
            i += 1

        # If queue is empty, system is idle, so increase the time
        if not queue:
            time_elapsed += 1
            continue

        # Select the process with the shortest remaining burst time
        queue.sort(key=lambda x: x[2])  # Sort by remaining burst time
        process_id, arrival, burst = queue.pop(0)

        start_time = time_elapsed
        exec_time = 1  # Process runs for 1 unit of time
        run_task(process_id, exec_time)  # Simulate process execution

        # Update the process's remaining burst time
        idx = next(index for index, data in enumerate(process_data) if data[0] == process_id)
        remaining_burst[idx] -= exec_time
        time_elapsed += exec_time
        process_schedule.append((process_id, time_elapsed))

        # If the process still has burst time left, re-enqueue it
        if remaining_burst[idx] > 0:
            queue.append(process_data[idx])

        else:
            # Process completed, calculate exit and turnaround time
            exit_times.append(time_elapsed)
            turnaround_time[idx] = time_elapsed - arrival
            entry_times.append(start_time)

    # Calculate waiting time
    for idx, (_, arrival, burst) in enumerate(process_data):
        waiting_time[idx] = turnaround_time[idx] - burst

    return process_schedule, waiting_time, turnaround_time, entry_times, exit_times


def plot_gantt_chart(process_schedule):
    plt.figure(figsize=(10, 5))
    last_time = 0
    for process_id, end_time in process_schedule:
        plt.barh(f"P{process_id}", end_time - last_time, left=last_time, edgecolor="black")
        last_time = end_time

    plt.xlabel("Time")
    plt.ylabel("Process")
    plt.title("Shortest Remaining Time (SRT) Scheduling Gantt Chart")
    plt.show()


if __name__ == "__main__":
    num_process = int(input("Number of processes: "))

    process_data = []
    for i in range(num_process):
        arrival = float(input(f"Enter arrival time for process {i + 1}: "))
        burst = float(input(f"Enter burst time for process {i + 1}: "))
        process_data.append((i, arrival, burst))

    # Execute Shortest Remaining Time (SRT) Scheduling
    process_schedule, waiting_time, turnaround_time, entry_times, exit_times = srt(process_data)

    # Display results
    print("\nProcess Schedule (Process ID = Completion Time):")
    for entry in process_schedule:
        print(f"P{entry[0]} = {entry[1]}")

    print("\nWaiting and Turnaround Times:")
    for idx, (process_id, arrival, burst) in enumerate(process_data):
        print(f"Process {process_id} - Waiting Time: {waiting_time[idx]}, Turnaround Time: {turnaround_time[idx]}")

    # Plot the Gantt Chart
    plot_gantt_chart(process_schedule)
