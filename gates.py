import numpy as np
import qiskit


def cnx(qc, *qubits): #controlled(N-1)Not
    #print(qubits)
    n=len(qubits)
    if len(qubits) > 3:
        last = qubits[-1]
        # A matrix: (made up of a  and Y rotation, lemma4.3)
        qc.crz(np.pi/2, qubits[n-2], qubits[-1])
        #qc.cu3(np.pi/2, 0, 0, qubits[-2],qubits[-1])
        qc.cu(np.pi/2,0, 0, 0, qubits[n-2], qubits[n-1])

        # Control not gate
        cnx(qc,*qubits[:n-2],qubits[n-1])
        
        # B matrix (opposite angle)
        #qc.cu3(-np.pi/2, 0, 0, qubits[-2], qubits[-1])
        qc.cu(-np.pi/2, 0, 0, 0, qubits[n-2], qubits[n-1])
        
        # Control
        cnx(qc,*qubits[:n-2],qubits[n-1])
        
        # C matrix (final rotation)
        qc.crz(-np.pi/2,qubits[n-2],qubits[n-1])
    elif len(qubits)==3:
        qc.ccx(*qubits)
    elif len(qubits)==2:
        qc.cx(*qubits)
        
        
        
def increment_gate_n(qwc, q, subnode, n):
    # Ensure q is a list of qubits
    for i in range(n-1): 
        # Obtaining a sublist of qubits
        lst = q[1+i:n].copy()
        # Reversing the order of the sublist
        lst1 = lst[::-1] 
        # Applying the controlled-not gate to the sublist and a single qubit
        cnx(qwc, [subnode], *lst1, q[i])
    # Applying the controlled-not gate to the subnode and the last qubit in the list
    cnx(qwc, [subnode], q[n-1]) 
    # Adding a barrier to the circuit
    qwc.barrier()
    return qwc

# Function for implementing the decrement gate for quantum walks
def decrement_gate_n(qwc, q, subnode, n):
    # Applying the X-gate to the subnode and each qubit in the register
    qwc.x(subnode)
    for x in range(0, n):
        qwc.x(q[x])
             
    for i in range(n-1): 
        # Obtaining a sublist of qubits
        lst = q[1+i:n].copy()
        # Reversing the order of the sublist
        lst1 = lst[::-1]
        # Applying the X-gate to the ith qubit
        qwc.x(q[i])
        # Applying the controlled-not gate to the sublist and the ith qubit
        cnx(qwc, [subnode], *lst1, q[i])
    # Applying the X-gate to the last qubit
    qwc.x(q[n-1])    
    # Applying the controlled-not gate to the subnode and the last qubit
    cnx(qwc, [subnode], q[n-1])
    # Applying the X-gate to the subnode
    qwc.x(subnode)
    return qwc     