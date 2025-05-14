import threading
import time
import tkinter as tk


class Locks:
    def __init__(self, gui):
        self.lock_1 = threading.RLock()
        self.lock_2 = threading.RLock()
        self.count = 0
        self.gui = gui  # Pass in the GUI object to update interface

    def log(self, message):
        print(message)  # Print to terminal
        self.gui.update_log(message)  # Print to GUI


def thread_1_routine(locks):
    tid = threading.current_thread().name
    locks.log(f"{tid}: Attempting to acquire lock_1")
    time.sleep(1)  # 1-second delay

    with locks.lock_1:
        locks.log(f"{tid}: Acquired lock_1")
        locks.gui.update_lock_status("lock_1", tid)
        time.sleep(1)  # 1-second delay

        locks.log(f"{tid}: Attempting to acquire lock_2")
        time.sleep(1)  # 1-second delay
        with locks.lock_2:
            locks.log(f"{tid}: Acquired lock_2")
            locks.gui.update_lock_status("lock_2", tid)
            locks.count += 1
            locks.log(f"{tid}: Updated count to {locks.count}")
            time.sleep(1)  # 1-second delay

        locks.gui.update_lock_status("lock_2", "Released")

    locks.gui.update_lock_status("lock_1", "Released")
    locks.log(f"{tid}: Released lock_1 and finished")


def thread_2_routine(locks):
    tid = threading.current_thread().name
    locks.log(f"{tid}: Attempting to acquire lock_2")
    time.sleep(1)  # 1-second delay

    with locks.lock_2:
        locks.log(f"{tid}: Acquired lock_2")
        locks.gui.update_lock_status("lock_2", tid)
        time.sleep(1)  # 1-second delay

        locks.log(f"{tid}: Attempting to acquire lock_1")
        time.sleep(1)  # 1-second delay
        with locks.lock_1:
            locks.log(f"{tid}: Acquired lock_1")
            locks.gui.update_lock_status("lock_1", tid)
            locks.count += 1
            locks.log(f"{tid}: Updated count to {locks.count}")
            time.sleep(1)  # 1-second delay

        locks.gui.update_lock_status("lock_1", "Released")

    locks.gui.update_lock_status("lock_2", "Released")
    locks.log(f"{tid}: Released lock_2 and finished")


class ThreadGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Thread Simulation")

        # Text area for logs
        self.log_text = tk.Text(root, height=15, width=50)
        self.log_text.grid(row=0, column=0, columnspan=3)

        # Labels for lock status
        self.lock_1_label = tk.Label(root, text="Lock 1: Released", fg="green")
        self.lock_1_label.grid(row=1, column=0, sticky="w")

        self.lock_2_label = tk.Label(root, text="Lock 2: Released", fg="green")
        self.lock_2_label.grid(row=2, column=0, sticky="w")

        # Buttons to start each thread
        self.thread_1_button = tk.Button(root, text="Start Thread 1", command=self.start_thread_1)
        self.thread_1_button.grid(row=3, column=0)

        self.thread_2_button = tk.Button(root, text="Start Thread 2", command=self.start_thread_2)
        self.thread_2_button.grid(row=3, column=1)

        # Final evaluation button
        self.evaluate_button = tk.Button(root, text="Evaluate Count", command=self.evaluate_count)
        self.evaluate_button.grid(row=3, column=2)

        # Initialize Locks object with GUI reference
        self.locks = Locks(self)

    def update_log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)  # Scroll to the bottom

    def update_lock_status(self, lock_name, status):
        if lock_name == "lock_1":
            self.lock_1_label.config(text=f"Lock 1: {status}", fg="red" if status != "Released" else "green")
        elif lock_name == "lock_2":
            self.lock_2_label.config(text=f"Lock 2: {status}", fg="red" if status != "Released" else "green")

    def start_thread_1(self):
        thread_1 = threading.Thread(target=thread_1_routine, args=(self.locks,), name="Thread-1")
        thread_1.start()
        self.update_log("Main: Started Thread 1")

    def start_thread_2(self):
        thread_2 = threading.Thread(target=thread_2_routine, args=(self.locks,), name="Thread-2")
        thread_2.start()
        self.update_log("Main: Started Thread 2")

    def evaluate_count(self):
        # Final count evaluation for correctness
        if self.locks.count == 2:
            self.update_log("Main: OK. Total count is 2")
        else:
            self.update_log(f"Main: ERROR! Total count is {self.locks.count}")


# Run the Tkinter GUI application
root = tk.Tk()
app = ThreadGUI(root)
root.mainloop()
