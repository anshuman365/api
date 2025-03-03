import time
import random
import threading

class VirtualCPU:
    def __init__(self, cpu_id):
        """Initialize CPU components"""
        self.cpu_id = cpu_id  # Unique CPU identifier
        self.registers = {"ACC": 0, "R1": 0, "R2": 0, "R3": 0}  # General-purpose registers
        self.memory = {}  # Simulated RAM
        self.cache = {}  # Cache for faster access
        self.clock_speed = 0.3  # Adjustable clock cycle speed
        self.pipeline = []  # Pipeline instruction queue

    def load_number(self, n):
        """Load a number into the ACC register"""
        self.registers["ACC"] = n
        print(f"CPU-{self.cpu_id}: Loaded number {n} into ACC")

    def execute_collatz(self):
        """Execute the Collatz Conjecture problem with caching & pipelining"""
        steps = 0
        n = self.registers["ACC"]

        while n != 1:
            time.sleep(self.clock_speed)  # Simulate CPU cycle
            
            # Use cache if available
            if n in self.cache:
                print(f"CPU-{self.cpu_id}: Cache Hit! ACC = {self.cache[n]}")
                n = self.cache[n]
                continue

            # Store previous step in RAM (track visited numbers)
            if n not in self.memory:
                self.memory[n] = []
            self.memory[n].append(n)

            # Add instructions to pipeline (execute parallel operations)
            if n % 2 == 0:
                self.pipeline.append(("DIV", 2))  # ACC = ACC / 2
            else:
                self.pipeline.append(("MUL", 3))  # ACC = ACC * 3
                self.pipeline.append(("ADD", 1))  # ACC = ACC + 1

            # Execute pipeline
            while self.pipeline:
                instruction, value = self.pipeline.pop(0)
                self.alu_operation(instruction, value)

            # Store correct cache mapping (avoid overwriting with itself)
            new_value = self.registers["ACC"]
            if n not in self.cache:
                self.cache[n] = new_value
            
            n = new_value
            steps += 1
            print(f"CPU-{self.cpu_id}: Step {steps} -> ACC = {n}")

        print(f"CPU-{self.cpu_id}: Collatz Conjecture solved in {steps} steps.")

    def alu_operation(self, operation, value):
        """Simulate ALU operations (Addition, Multiplication, Division)"""
        if operation == "ADD":
            self.registers["ACC"] += value
        elif operation == "MUL":
            self.registers["ACC"] *= value
        elif operation == "DIV":
            self.registers["ACC"] //= value  # Integer division
        print(f"CPU-{self.cpu_id}: ALU {operation} {value} -> ACC = {self.registers['ACC']}")

# ---- Run Multi-Core Virtual CPU ----
def run_cpu(cpu_id):
    cpu = VirtualCPU(cpu_id)
    start_number = random.randint(10, 100)  # Generate a random starting number
    cpu.load_number(start_number)
    cpu.execute_collatz()

# Create two CPU threads (multi-core simulation)
cpu1 = threading.Thread(target=run_cpu, args=(1,))
cpu2 = threading.Thread(target=run_cpu, args=(2,))

cpu1.start()
cpu2.start()

cpu1.join()
cpu2.join()