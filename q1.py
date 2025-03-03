import numpy as np

class Qubit:
    def __init__(self):
        """Initialize a qubit in state |0⟩"""
        self.state = np.array([[1], [0]], dtype=complex)  # |0⟩ state
    
    def apply_hadamard(self):
        """Applies Hadamard gate to put the qubit into superposition"""
        H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        self.state = np.dot(H, self.state)
    
    def measure(self):
        """Measures the qubit and collapses it to |0⟩ or |1⟩ based on probabilities"""
        probabilities = np.abs(self.state) ** 2
        outcome = np.random.choice([0, 1], p=[probabilities[0, 0], probabilities[1, 0]])
        
        # After measurement, the state collapses to the observed value
        self.state = np.array([[1], [0]], dtype=complex) if outcome == 0 else np.array([[0], [1]], dtype=complex)
        return outcome

    def __str__(self):
        """Returns the current state of the qubit"""
        return f"Qubit state: {self.state.flatten()}"

# ---- Simulation ----
if __name__ == "__main__":
    qubit = Qubit()
    print("Initial Qubit State:", qubit)

    qubit.apply_hadamard()
    print("After Hadamard (Superposition):", qubit)

    measurement = qubit.measure()
    print(f"Measured Value: {measurement}")
    print("After Measurement:", qubit)
