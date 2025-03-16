import threading
import time
import matplotlib.pyplot as plt

Critical_item = 0
Producer_wish = False
Consumer_wish = False
turn = -1

# Stats counters
producer_count = 0
consumer_count = 0

# Locks for safe updates to shared counters
lock = threading.Lock()

def producer_want_to_produce():
    global Critical_item, Producer_wish, Consumer_wish, turn, producer_count
    Producer_wish = True
    turn = 1  # Give Consumer the chance

    while Consumer_wish and turn == 1:
        print('Producer is waiting and Consumer is in Critical section')
        time.sleep(0.01)

    # Critical Section
    Critical_item += 1
    for _ in range(7):
        with lock:
            producer_count += 1
        print("Producer critical section e ace")
        time.sleep(0.05)

    Producer_wish = False
    print('Producer critical section use kora ses')

def consumer_want_to_consume():
    global Critical_item, Producer_wish, Consumer_wish, turn, consumer_count
    Consumer_wish = True
    turn = 0  # Give Producer the chance

    while Producer_wish and turn == 0:
        print('Consumer is waiting and Producer is in Critical section')
        time.sleep(0.01)

    # Critical Section
    Critical_item -= 1
    for _ in range(5):
        with lock:
            consumer_count += 1
        print("Consumer critical section e ace")
        time.sleep(0.05)

    Consumer_wish = False
    print('Consumer critical section use kora ses')

# Create threads
t1 = threading.Thread(target=producer_want_to_produce)
t2 = threading.Thread(target=consumer_want_to_consume)

# Start threads
t1.start()
t2.start()

# Wait for both to finish
t1.join()
t2.join()

print("\nFinal Critical_item value:", Critical_item)
print("Producer accessed critical section:", producer_count, "times")
print("Consumer accessed critical section:", consumer_count, "times")

# Plotting the statistics
plt.figure(figsize=(6, 4))
plt.bar(["Producer", "Consumer"], [producer_count, consumer_count], color=["blue", "green"])
plt.title("Critical Section Access Count")
plt.ylabel("Access Count")
plt.xlabel("Thread")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
