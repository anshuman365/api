import time
import random
import threading
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import json
import tkinter as tk
from tkinter import scrolledtext

# Check for Multi-GPU Support
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 1:
    print("Multi-GPU Support Enabled!")
    strategy = tf.distribute.MirroredStrategy()
else:
    strategy = tf.distribute.get_strategy()

class VirtualCPU:
    def __init__(self, cpu_id, gui_log=None):
        """Initialize CPU components"""
        self.cpu_id = cpu_id
        self.registers = {"ACC": 0}
        self.memory = {}
        self.cache = {}
        self.clock_speed = 0.05  # Adjustable clock cycle speed
        self.execution_data = []  # Log execution data
        self.gui_log = gui_log  # GUI Logging

    def log_to_gui(self, message):
        """Log execution messages to the GUI"""
        if self.gui_log:
            self.gui_log.insert(tk.END, message + "\n")
            self.gui_log.see(tk.END)

    def load_number(self, n):
        """Load a number into the ACC register"""
        self.registers["ACC"] = n
        message = f"CPU-{self.cpu_id}: Loaded number {n} into ACC"
        print(message)
        self.log_to_gui(message)

    def execute_collatz(self):
        """Execute the Collatz Conjecture problem"""
        steps = 0
        n = self.registers["ACC"]
        start_time = time.time()  # Benchmark Start

        while n != 1:
            time.sleep(self.clock_speed)  # Simulate CPU cycle

            # Use cache if available
            if n in self.cache:
                message = f"CPU-{self.cpu_id}: Cache Hit! ACC = {self.cache[n]}"
                print(message)
                self.log_to_gui(message)
                n = self.cache[n]
                continue

            # Apply Collatz Rule
            if n % 2 == 0:
                n //= 2
            else:
                n = (n * 3) + 1

            # Detect Loop and Stop Execution
            if n in self.memory:
                message = f"CPU-{self.cpu_id}: Loop detected! Breaking."
                print(message)
                self.log_to_gui(message)
                break
            self.memory[n] = steps

            self.cache[self.registers["ACC"]] = n  # Store in cache
            self.registers["ACC"] = n  # Update ACC
            steps += 1

            # Log Execution Data
            self.execution_data.append({"CPU": self.cpu_id, "Step": steps, "ACC": n})

            message = f"CPU-{self.cpu_id}: Step {steps} -> ACC = {n}"
            print(message)
            self.log_to_gui(message)

        end_time = time.time()  # Benchmark End
        execution_time = round(end_time - start_time, 5)

        message = f"CPU-{self.cpu_id}: Collatz Conjecture solved in {steps} steps. Time Taken: {execution_time} sec"
        print(message)
        self.log_to_gui(message)

        # Save Execution Data to File
        with open(f"cpu_{self.cpu_id}_execution.json", "w") as file:
            json.dump(self.execution_data, file, indent=4)

# ---- Optimized Deep Learning Model ----
def train_deep_learning_model():
    """Train a deep learning model to predict Collatz steps"""
    with strategy.scope():  # Multi-GPU Training
        X_train = np.array(range(2, 2000)).reshape(-1, 1)
        y_train = np.array([collatz_steps(n) for n in range(2, 2000)])

        model = Sequential([
            Dense(32, activation='relu', input_shape=(1,)),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(1)  # Output: Predicted Steps
        ])

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=150, verbose=0)  # Increased training epochs

    return model

def collatz_steps(n):
    """Calculate exact Collatz steps for a given number"""
    steps = 0
    while n != 1:
        n = (n // 2) if (n % 2 == 0) else (3 * n + 1)
        steps += 1
    return steps

# ---- GUI for Real-Time Monitoring ----
class CPUGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual CPU Execution Log")

        self.log_area = scrolledtext.ScrolledText(self.root, width=80, height=30)
        self.log_area.pack(padx=10, pady=10)

        self.start_button = tk.Button(self.root, text="Start CPU Simulation", command=self.start_simulation)
        self.start_button.pack(pady=10)

    def start_simulation(self):
        """Start multi-threaded CPU execution"""
        deep_learning_model = train_deep_learning_model()

        cpu_threads = []
        for i in range(4):
            cpu = VirtualCPU(i + 1, self.log_area)
            thread = threading.Thread(target=run_cpu, args=(cpu, deep_learning_model))
            cpu_threads.append(thread)
            thread.start()

        for thread in cpu_threads:
            thread.join()

def run_cpu(cpu, model):
    """Run a CPU instance with AI prediction"""
    start_number = random.randint(10, 100)
    cpu.load_number(start_number)

    # Predict Steps using Deep Learning Model
    predicted_steps = int(model.predict(np.array([[start_number]]))[0][0])
    message = f"CPU-{cpu.cpu_id}: Predicted Steps by AI = {predicted_steps}"
    print(message)
    cpu.log_to_gui(message)

    cpu.execute_collatz()

# ---- Start GUI Application ----
if __name__ == "__main__":
    root = tk.Tk()
    app = CPUGUI(root)
    root.mainloop()