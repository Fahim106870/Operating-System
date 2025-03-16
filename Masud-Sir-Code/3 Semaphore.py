import threading
import matplotlib.pyplot as plt
import time

# Shared data
Semaphore = 0
Limit = 5
semaphore_history = []       # Y-axis values (Semaphore levels)
operation_labels = []        # X-axis labels (Produced / Consumed)
lock = threading.Lock()

def wait():
    global Semaphore
    while True:
        with lock:
            if Semaphore > 0:
                Semaphore -= 1
                semaphore_history.append(Semaphore)
                operation_labels.append("Produced")
                return
        time.sleep(0.01)

def signal():
    global Semaphore
    while True:
        with lock:
            if Semaphore < Limit:
                Semaphore += 1
                semaphore_history.append(Semaphore)
                operation_labels.append("Consumed")
                return
        time.sleep(0.01)

def producer():
    for _ in range(10):
        wait()
        print("Produced")
        time.sleep(0.01)

def consumer():
    for _ in range(10):
        signal()
        print("Consumed")
        time.sleep(0.01)

# Start threads
t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)

t1.start()
t2.start()
t1.join()
t2.join()

# Prepare color coding: Purple = Produced, Green = Consumed
colors = ['blue' if op == "Produced" else 'green' for op in operation_labels]

# Plot
plt.figure(figsize=(12, 6))
plt.scatter(range(len(semaphore_history)), semaphore_history, c=colors, s=20)
plt.plot(semaphore_history, color='gray', linewidth=1, alpha=0.5)

# Labels and styling
plt.title("Semaphore Value Over Time with Produced and Consumed Events")
plt.xlabel("Operation Step")
plt.ylabel("Semaphore Value")
plt.ylim(0, Limit + 1)
plt.grid(True, linestyle='--', alpha=0.4)
legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label='Produced', markerfacecolor='blue', markersize=8),
                  plt.Line2D([0], [0], marker='o', color='w', label='Consumed', markerfacecolor='green', markersize=8)]
plt.legend(handles=legend_handles)
plt.tight_layout()
plt.show()
