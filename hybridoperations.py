from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile 
from numpy.random import randint

#generate a quantumcircuit, by encoding each bit of alice's message on qubit in the X or Z basis at random. 
#0 : prepare in Zbasis , 1: prepare in the X-basis.  

def Bases_preparation(B):
    S=[]
    R=[]
    for i in range(len(B)):
        qc = QuantumCircuit(1,1)
        if B[i] == 1: # Prepare qubit in Z-basis
                r=randint(2, size=1)
                if r == 0:
                    R.append(0)
                    #pass
                else:
                    qc.x(0) 
                    R.append(1)
        else:
                r=randint(2, size=1)
                if r == 0:
                    qc.h(0)
                    R.append(0)
                else:
                    qc.x(0)
                    qc.h(0)
                    R.append(1)

        S.append(qc)
 
    return S,R

#Applying measurement to simulate results of each qubits 
def measure_message(message, bases):
     
    simulator = AerSimulator()
    #print(bases)
    measurements = []
    for q in range(len(bases)):
        if bases[q] == 1: # measuring in Z-basis 
            message[q].measure(0,0)
        if bases[q] == 0: # measuring in X-basis
            message[q].h(0)
            message[q].measure(0,0)
         
        transpiled_qc = transpile(message[q], 
                                  backend=AerSimulator())
        result = simulator.run(transpiled_qc,  shots=1, 
                               memory=True).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements