import time
import random
import threading
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import json

class VirtualCPU:
    def __init__(self, cpu_id):
        """Initialize CPU components"""
        self.cpu_id = cpu_id
        self.registers = {"ACC": 0}
        self.memory = {}
        self.cache = {}
        self.clock_speed = 0.05  # Adjustable clock cycle speed
        self.execution_data = []  # Log execution data

    def load_number(self, n):
        """Load a number into the ACC register"""
        self.registers["ACC"] = n
        print(f"CPU-{self.cpu_id}: Loaded number {n} into ACC")

    def execute_collatz(self):
        """Execute the Collatz Conjecture problem"""
        steps = 0
        n = self.registers["ACC"]
        start_time = time.time()  # Benchmark Start

        while n != 1:
            time.sleep(self.clock_speed)  # Simulate CPU cycle

            # Use cache if available
            if n in self.cache:
                print(f"CPU-{self.cpu_id}: Cache Hit! ACC = {self.cache[n]}")
                n = self.cache[n]
                continue

            # Apply Collatz Rule
            if n % 2 == 0:
                n //= 2
            else:
                n = (n * 3) + 1

            # Detect Loop and Stop Execution
            if n in self.memory:
                print(f"CPU-{self.cpu_id}: Loop detected! Breaking.")
                break
            self.memory[n] = steps

            self.cache[self.registers["ACC"]] = n  # Store in cache
            self.registers["ACC"] = n  # Update ACC
            steps += 1

            # Log Execution Data
            self.execution_data.append({"CPU": self.cpu_id, "Step": steps, "ACC": n})

            print(f"CPU-{self.cpu_id}: Step {steps} -> ACC = {n}")

        end_time = time.time()  # Benchmark End
        execution_time = round(end_time - start_time, 5)

        print(f"CPU-{self.cpu_id}: Collatz Conjecture solved in {steps} steps. Time Taken: {execution_time} sec")

        # Save Execution Data to File
        with open(f"cpu_{self.cpu_id}_execution.json", "w") as file:
            json.dump(self.execution_data, file, indent=4)

# ---- Deep Learning Model for Prediction ----
def train_deep_learning_model():
    """Train a deep learning model to predict Collatz steps"""
    X_train = np.array(range(2, 1000)).reshape(-1, 1)
    y_train = np.array([collatz_steps(n) for n in range(2, 1000)])

    model = Sequential([
        Dense(16, activation='relu', input_shape=(1,)),
        Dense(16, activation='relu'),
        Dense(1)  # Output: Predicted Steps
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=100, verbose=0)

    return model

def collatz_steps(n):
    """Calculate exact Collatz steps for a given number"""
    steps = 0
    while n != 1:
        n = (n // 2) if (n % 2 == 0) else (3 * n + 1)
        steps += 1
    return steps

# ---- Run Multi-Core Virtual CPU ----
def run_cpu(cpu_id, model):
    """Run a CPU instance with AI prediction"""
    cpu = VirtualCPU(cpu_id)
    start_number = random.randint(10, 100)
    cpu.load_number(start_number)

    # Predict Steps using Deep Learning Model
    predicted_steps = int(model.predict(np.array([[start_number]]))[0][0])
    print(f"CPU-{cpu_id}: Predicted Steps by AI = {predicted_steps}")

    cpu.execute_collatz()

# Train Deep Learning Model
deep_learning_model = train_deep_learning_model()

# Create four CPU threads (multi-core simulation)
cpu_threads = []
for i in range(4):
    thread = threading.Thread(target=run_cpu, args=(i+1, deep_learning_model))
    cpu_threads.append(thread)
    thread.start()

# Wait for all CPUs to complete
for thread in cpu_threads:
    thread.join()