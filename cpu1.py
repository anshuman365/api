import time
import random

class VirtualCPU:
    def __init__(self):
        """Initialize CPU components"""
        self.registers = {"ACC": 0, "TMP": 0}  # ACC = Accumulator, TMP = Temporary Storage
        self.memory = {}  # Simulated RAM
        self.clock_speed = 0.5  # 0.5s per cycle (adjustable)

    def load_number(self, n):
        """Load a number into the accumulator"""
        self.registers["ACC"] = n
        self.memory[n] = []  # Store steps for reference
        print(f"Loaded number {n} into ACC")

    def execute_collatz(self):
        """Execute the Collatz Conjecture problem step by step"""
        steps = 0
        n = self.registers["ACC"]

        while n != 1:
            time.sleep(self.clock_speed)  # Simulate CPU cycle
            self.memory[self.registers["ACC"]].append(n)

            if n % 2 == 0:
                self.alu_operation("DIV", 2)  # ACC = ACC / 2
            else:
                self.alu_operation("MUL", 3)  # ACC = ACC * 3
                self.alu_operation("ADD", 1)  # ACC = ACC + 1
            
            n = self.registers["ACC"]
            steps += 1
            print(f"Step {steps}: ACC = {n}")

        print(f"Collatz Conjecture solved in {steps} steps.\nFinal State: {self.memory}")

    def alu_operation(self, operation, value):
        """Simulate ALU operations (Addition, Multiplication, Division)"""
        if operation == "ADD":
            self.registers["ACC"] += value
        elif operation == "MUL":
            self.registers["ACC"] *= value
        elif operation == "DIV":
            self.registers["ACC"] //= value  # Integer division
        print(f"ALU {operation} {value} -> ACC = {self.registers['ACC']}")

# ---- Run the Virtual CPU ----
if __name__ == "__main__":
    cpu = VirtualCPU()
    
    # Generate a random starting number
    start_number = random.randint(10, 100)
    
    cpu.load_number(start_number)  # Load number into ACC
    cpu.execute_collatz()  # Execute calculations
