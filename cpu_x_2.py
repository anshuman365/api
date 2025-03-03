import time
import random
import threading
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from flask import Flask, render_template, request, jsonify

# Check Multi-GPU Support
physical_devices = tf.config.experimental.list_physical_devices('GPU')
strategy = tf.distribute.MirroredStrategy() if len(physical_devices) > 1 else tf.distribute.get_strategy()

# Flask App Initialization
app = Flask(__name__)

# Global Storage for Execution Logs
execution_logs = []

class VirtualCPU:
    def __init__(self, cpu_id):
        self.cpu_id = cpu_id
        self.registers = {"ACC": 0}
        self.memory = {}
        self.cache = {}
        self.clock_speed = 0.05
        self.execution_data = []

    def log_to_web(self, message):
        """Log execution data to the web interface"""
        log_entry = {"cpu": self.cpu_id, "message": message}
        execution_logs.append(log_entry)

    def load_number(self, n):
        """Load a number into ACC"""
        self.registers["ACC"] = n
        self.log_to_web(f"CPU-{self.cpu_id}: Loaded number {n} into ACC")

    def execute_collatz(self):
        """Execute Collatz Conjecture"""
        steps = 0
        n = self.registers["ACC"]
        start_time = time.time()

        while n != 1:
            time.sleep(self.clock_speed)

            if n in self.cache:
                self.log_to_web(f"CPU-{self.cpu_id}: Cache Hit! ACC = {self.cache[n]}")
                n = self.cache[n]
                continue

            n = n // 2 if n % 2 == 0 else (n * 3) + 1

            if n in self.memory:
                self.log_to_web(f"CPU-{self.cpu_id}: Loop detected! Breaking.")
                break
            self.memory[n] = steps

            self.cache[self.registers["ACC"]] = n
            self.registers["ACC"] = n
            steps += 1

            self.execution_data.append({"CPU": self.cpu_id, "Step": steps, "ACC": n})
            self.log_to_web(f"CPU-{self.cpu_id}: Step {steps} -> ACC = {n}")

        end_time = time.time()
        execution_time = round(end_time - start_time, 5)
        self.log_to_web(f"CPU-{self.cpu_id}: Collatz solved in {steps} steps. Time: {execution_time} sec")

        with open(f"cpu_{self.cpu_id}_execution.json", "w") as file:
            json.dump(self.execution_data, file, indent=4)

# ---- Optimized Deep Learning Model ----
def train_deep_learning_model():
    """Train a deep learning model for Collatz steps prediction"""
    with strategy.scope():
        X_train = np.array(range(2, 2000)).reshape(-1, 1)
        y_train = np.array([collatz_steps(n) for n in range(2, 2000)])

        model = Sequential([
            Dense(32, activation='relu', input_shape=(1,)),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(1)
        ])

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=150, verbose=0)

    return model

def collatz_steps(n):
    """Calculate exact Collatz steps for a given number"""
    steps = 0
    while n != 1:
        n = (n // 2) if (n % 2 == 0) else (3 * n + 1)
        steps += 1
    return steps

# ---- Flask Routes ----
@app.route('/')
def index():
    """Render the main webpage"""
    return render_template('index.html', logs=execution_logs)

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    """Start multi-threaded CPU execution"""
    execution_logs.clear()
    deep_learning_model = train_deep_learning_model()
    cpu_threads = []

    for i in range(4):
        cpu = VirtualCPU(i + 1)
        thread = threading.Thread(target=run_cpu, args=(cpu, deep_learning_model))
        cpu_threads.append(thread)
        thread.start()

    for thread in cpu_threads:
        thread.join()

    return jsonify({"message": "Simulation Completed", "logs": execution_logs})

def run_cpu(cpu, model):
    """Run a CPU instance with AI prediction"""
    start_number = random.randint(10, 100)
    cpu.load_number(start_number)

    predicted_steps = int(model.predict(np.array([[start_number]]))[0][0])
    cpu.log_to_web(f"CPU-{cpu.cpu_id}: AI Predicted Steps = {predicted_steps}")

    cpu.execute_collatz()

# ---- Run Flask App ----
if __name__ == '__main__':
    app.run(debug=True)