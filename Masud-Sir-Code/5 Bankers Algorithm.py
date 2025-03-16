import numpy as np
import random

def bankers_algorithm(Allocation, Max, Available):
    Work = Available.copy()
    n = len(Allocation)
    Finish = [False for _ in range(n)]
    Need = np.subtract(Max, Allocation)
    print("\nNeed Matrix:")
    print(Need)
    process_done = []
    process_incomplete = n
    print("\nStarting Banker's Algorithm...\n")

    while True:
        if process_incomplete <= 0:
            print("Safe State Found!")
            print("Safe Sequence: ", ' → '.join([f'P{i}' for i in process_done]))
            break

        flag = True

        for i in range(n):
            if not Finish[i] and all(np.less_equal(Need[i], Work)):
                Finish[i] = True
                Work = np.add(Work, Allocation[i])
                process_done.append(i)
                process_incomplete -= 1
                flag = False

        if flag:
            print("Deadlock Detected!")
            break

np.random.seed()
n_processes = 5
n_resources = 3
Allocation = np.random.randint(0, 6, size=(n_processes, n_resources))
Max = Allocation + np.random.randint(0, 5, size=(n_processes, n_resources))
Available = np.random.randint(3, 10, size=n_resources)
print("Random Input Generated")
print("Allocation Matrix:\n", Allocation)
print("\nMax Matrix:\n", Max)
print("\nAvailable Resources:\n", Available)
bankers_algorithm(Allocation, Max, Available)
