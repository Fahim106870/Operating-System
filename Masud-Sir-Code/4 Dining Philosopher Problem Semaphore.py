import threading
import time
import matplotlib.pyplot as plt

philosopher = 5
Chopstick = [False] * philosopher
lock = threading.Lock()
state_history = []

def log_state(philosopher_id, state):
    with lock:
        state_history.append((time.time(), philosopher_id, state))

def wait(n, philosopher_id):
    global Chopstick
    while True:
        with lock:
            if not Chopstick[n]:
                Chopstick[n] = True
                return
        log_state(philosopher_id, "Waiting")
        time.sleep(0.01)

def signal(n):
    global Chopstick
    with lock:
        Chopstick[n] = False

def eating(x, n):
    log_state(n, "Thinking")
    time.sleep(1)  # simulate thinking

    wait(n, n)
    wait((n + 1) % 5, n)

    log_state(n, "Eating")
    print("\nEating", n)
    time.sleep(3)  # simulate eating

    signal(n)
    signal((n + 1) % 5)

    log_state(n, "Thinking")
    print("\nThinking", n, threading.current_thread().name)

threads = []
for i in range(5):
    t = threading.Thread(target=eating, args=('x', i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# --- Plot the Graph ---
start_time = state_history[0][0]
timestamps = [(t - start_time) for t, _, _ in state_history]
philosophers = [p for _, p, _ in state_history]
states = [s for _, _, s in state_history]


color_map = {'Thinking': 'green', 'Waiting': 'orange', 'Eating': 'red'}
colors = [color_map[s] for s in states]

plt.figure(figsize=(12, 6))
plt.scatter(timestamps, philosophers, c=colors, s=50)
plt.yticks(range(philosopher), [f"Philosopher {i}" for i in range(philosopher)])
plt.xlabel("Time (s)")
plt.ylabel("Philosopher")
plt.title("Dining Philosophers State Timeline")
legend_labels = [plt.Line2D([0], [0], marker='o', color='w', label=key,
                            markerfacecolor=value, markersize=10)
                 for key, value in color_map.items()]
plt.legend(handles=legend_labels)
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()
