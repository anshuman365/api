import numpy as np

class QuantumCircuit:
    def __init__(self):
        """Initialize a 2-qubit system in |00⟩ state"""
        self.state = np.array([[1], [0], [0], [0]], dtype=complex)  # |00⟩ state
    
    def apply_hadamard(self, qubit):
        """Applies Hadamard gate to the specified qubit"""
        H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        
        if qubit == 0:
            # Apply H to qubit 0 (Tensor Product with I)
            gate = np.kron(H, np.eye(2))
        else:
            # Apply H to qubit 1 (Tensor Product with I)
            gate = np.kron(np.eye(2), H)
        
        self.state = np.dot(gate, self.state)
        print(f"State after Hadamard on Qubit {qubit}:\n", self.state)
    
    def apply_cnot(self):
        """Applies CNOT gate (entangles qubits)"""
        CNOT = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ], dtype=complex)
        
        self.state = np.dot(CNOT, self.state)
        print("State after CNOT:\n", self.state)
    
    def measure(self):
        """Measures the qubits and collapses to |00⟩, |01⟩, |10⟩, or |11⟩"""
        probabilities = np.abs(self.state) ** 2
        outcomes = ["00", "01", "10", "11"]
        measured_state = np.random.choice(outcomes, p=probabilities.flatten())
        
        # Collapse to measured state
        if measured_state == "00":
            self.state = np.array([[1], [0], [0], [0]], dtype=complex)
        elif measured_state == "01":
            self.state = np.array([[0], [1], [0], [0]], dtype=complex)
        elif measured_state == "10":
            self.state = np.array([[0], [0], [1], [0]], dtype=complex)
        else:
            self.state = np.array([[0], [0], [0], [1]], dtype=complex)
        
        return measured_state

# ---- Simulation ----
if __name__ == "__main__":
    qc = QuantumCircuit()
    print("Initial State:\n", qc.state)

    qc.apply_hadamard(0)  # Apply Hadamard to Qubit 0
    qc.apply_cnot()  # Entangle Qubit 0 and 1

    measurement = qc.measure()
    print(f"Measured State: |{measurement}⟩")
    print("Final Collapsed State:\n", qc.state)
