import time
import random
import threading

class VirtualCPU:
    def __init__(self, cpu_id):
        """Initialize CPU components"""
        self.cpu_id = cpu_id  # Unique CPU identifier
        self.registers = {"ACC": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0}  
        self.memory = {}  # Simulated RAM
        self.cache = {}  # Cache for faster access
        self.clock_speed = 0.1  # Adjustable clock cycle speed
        self.pipeline = []  # Pipeline instruction queue
        self.quantum_gates = self.init_quantum_gates()  # Simulated quantum gates

    def init_quantum_gates(self):
        """Initialize a set of quantum gates for advanced operations"""
        gates = {}
        for i in range(100):
            gates[f"QGate-{i}"] = lambda x: (x ^ (x >> 1)) & 0xFF  # Quantum XOR Shift
        return gates

    def load_number(self, n):
        """Load a number into the ACC register"""
        self.registers["ACC"] = n
        print(f"CPU-{self.cpu_id}: Loaded number {n} into ACC")

    def execute_collatz(self):
        """Execute the Collatz Conjecture problem with caching, pipelining & quantum gates"""
        steps = 0
        n = self.registers["ACC"]

        while n != 1:
            time.sleep(self.clock_speed)  # Simulate CPU cycle
            
            # Use cache if available
            if n in self.cache:
                print(f"CPU-{self.cpu_id}: Cache Hit! ACC = {self.cache[n]}")
                n = self.cache[n]
                continue

            # Store previous step in RAM
            if n not in self.memory:
                self.memory[n] = []
            self.memory[n].append(n)

            # Add instruction to pipeline (execute parallel operations)
            if n % 2 == 0:
                n //= 2  # ACC = ACC / 2
            else:
                n = (n * 3) + 1  # ACC = ACC * 3 + 1

            # Occasionally apply quantum gate to simulate randomness
            if random.random() < 0.2:  # 20% chance to apply a quantum gate
                q_gate_id = random.randint(0, 99)
                n = self.apply_quantum_gate(n, q_gate_id)

            self.cache[self.registers["ACC"]] = n  # Store correct value in cache
            self.registers["ACC"] = n  # Update ACC
            steps += 1

            print(f"CPU-{self.cpu_id}: Step {steps} -> ACC = {n}")

        print(f"CPU-{self.cpu_id}: Collatz Conjecture solved in {steps} steps.")

    def apply_quantum_gate(self, n, gate_id):
        """Apply a quantum logic gate transformation"""
        if gate_id in self.quantum_gates:
            n = self.quantum_gates[f"QGate-{gate_id}"](n)
            print(f"CPU-{self.cpu_id}: Applied Quantum Gate-{gate_id} -> ACC = {n}")
        return n

# ---- Run Multi-Core Virtual CPU ----
def run_cpu(cpu_id):
    cpu = VirtualCPU(cpu_id)
    start_number = random.randint(10, 100)  # Generate a random starting number
    cpu.load_number(start_number)
    cpu.execute_collatz()

# Create four CPU threads (multi-core simulation)
cpu_threads = []
for i in range(4):  # Simulate 4 CPUs
    thread = threading.Thread(target=run_cpu, args=(i+1,))
    cpu_threads.append(thread)
    thread.start()

# Wait for all CPUs to complete
for thread in cpu_threads:
    thread.join()