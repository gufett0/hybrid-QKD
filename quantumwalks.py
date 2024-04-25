import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from gates import increment_gate_n, decrement_gate_n
from qiskit.quantum_info import Statevector



#Define a function to set up the initial parameters for the quantum walk
def setup_parameters(m, omega, theta0, theta1, theta2):
    # Convert m from binary string to list of bits
    message_bits = list(map(int, m))
    
    # Define the coin operators
    C0 = np.array([[np.cos(theta0), np.sin(theta0)], [np.sin(theta0), -np.cos(theta0)]])
    C1 = np.array([[np.cos(theta1), np.sin(theta1)], [np.sin(theta1), -np.cos(theta1)]])
    C2 = np.array([[np.cos(theta2), np.sin(theta2)], [np.sin(theta2), -np.cos(theta2)]])
    
    # Prepare the initial coin state as |ψ⟩c = cos(ω)|0⟩+sin(ω)|1⟩
    initial_coin_state = np.cos(omega) * np.array([1, 0]) + np.sin(omega) * np.array([0, 1])
    
    return message_bits, C0, C1, C2, initial_coin_state
# We'll construct the quantum circuit that applies the evolution operators Uˆt based on the message bits 
# and initializes the quantum state |φ⟩0 with the initial coin state.

def construct_quantum_circuit_new(N,n, message_bits, C0, C1, C2, initial_coin_state):

    qnodes = QuantumRegister(N,'qc')
    qsubnodes = QuantumRegister(1,'qanc')
    csubnodes = ClassicalRegister(1,'canc')
    cnodes = ClassicalRegister(N,'cr')
    qwc = QuantumCircuit(qnodes, qsubnodes, cnodes, csubnodes)
    qwc.initialize(initial_coin_state, qsubnodes[0])
    
    for i in range(N):    
        if i < len(message_bits):
            bit = message_bits[i]
            coin_operator = C0 if bit == 0 else C1
        else:
            # Apply C2 when i exceeds message length but within total steps
            coin_operator = C2  
        
        target_qubit = qsubnodes[0]  # Loop through qubits to apply operator   
        qwc.unitary(coin_operator, target_qubit)

        increment_gate_n(qwc, qnodes, qsubnodes[0],N)
        decrement_gate_n(qwc,qnodes,qsubnodes[0],N)        
        
    qwc.measure_all()
    return qwc

#We'll execute the quantum circuit and obtain the final state |φ⟩final by simulating the quantum walk
def execute_quantum_circuit2(qc):
    qc.measure_all()
    qc.remove_final_measurements()
    statevector = Statevector(qc)
    probs=Statevector(statevector).probabilities()
 
    return probs

#Transform the Probability Distribution to a Binary Hash Value.
#This involves scaling the probabilities, taking the integer part, and converting to binary.

def bin2hex(bin_str):
    """Convert a binary string to hexadecimal."""
    return hex(int(bin_str, 2))[2:]

def transform_probabilities_to_hash2(probabilities, N, j, k):
    if probabilities is None:
        print("Error: Probabilities are None. Cannot transform to hash.")
        return None

    # Initialize the hash value as an empty string
    hash_value = ''
    
    # Iterate over the probabilities
    #for key, probability in probabilities.items():
    #print (probabilities)
 
    for probability in probabilities:
        # Amplify the probability by 10^j times
        amplified_probability = probability * (10 ** j)
 
        # Take the integer part modulo 2^k
        modulo_value = int(amplified_probability) % (2 ** k)
        
        # Convert the modulo value to binary and pad with zeros if necessary
        binary_value = format(modulo_value, f'0{k}b')
     #   print('binary value: ', binary_value)
        
        # Append the binary value to the hash value
        hash_value += binary_value
    
    # Ensure the hash value is of length nk
    # Adjust the length by trimming or padding as necessary
    hash_value = hash_value[:N * k] # Trim to the exact length
    if len(hash_value) < N * k:
        hash_value += '0' * (N * k - len(hash_value)) # Pad with zeros if necessary
 
    return hash_value


def plot_horizontal_line_with_steps(array1, array2):
    # Initialize variables for plotting
    x_values = []
    y_values = []
    red_dots_x = []
    red_dots_y = []
    horizontal_line = [array1[0]] * len(array1)

    for i in range(len(array1)):
        x_values.append(i)
        y_values.append(horizontal_line[i])

        # Check if two corresponding entries are not equal
        if array1[i] != array2[i]:
            red_dots_x.append(i)
            red_dots_y.append(horizontal_line[i])

    plt.plot(x_values, y_values, color='blue')
    # Overlay red dots
    plt.scatter(red_dots_x, red_dots_y, color='red', label='Differences')
    plt.legend()
    plt.xlabel('ith bit ')
    plt.ylabel('Check')
    plt.title('Interception test')
    plt.grid(True)
    plt.show()


def QWs(N,n,m,omega,theta0,theta1,theta2):
    n=5
    # Set up parameters
    message_bits, C0, C1, C2, initial_coin_state = setup_parameters(m, omega, theta0, theta1, theta2)
    # Construct the quantum circuit
    qc = construct_quantum_circuit_new(N, n, message_bits, C0, C1, C2, initial_coin_state)
    #qc.draw("mpl")
    # Execute the quantum circuit and obtain the probability distribution
    probabilities = execute_quantum_circuit2(qc)
    j=12
    k=8 
    hash_value = transform_probabilities_to_hash2(probabilities, N, j, k)
     
    hash_value1=np.array(list(map(int, hash_value)))
    return hash_value1



