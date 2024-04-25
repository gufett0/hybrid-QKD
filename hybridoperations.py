from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile 
from numpy.random import randint


############### AQKD ################


#generate a quantumcircuit, by encoding each bit of alice's message on qubit in the X or Z basis at random. 
#0 : prepare in Zbasis , 1: prepare in the X-basis.  

def Bases_preparation_AQKD(B):
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
def measure_message_AQKD(message, bases):
     
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


############### ASQKD1 ################

def Bases_preparation_ASQKD1(B):
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
                  #  R.append(0) #removed for ASQKD 1. 
                else:
                    qc.x(0)
                    qc.h(0)
                   # R.append(1) #removed for ASQKD 1. 

        S.append(qc)
    return S,R

#Applying measurement to simulate results of each qubits 
def measure_message_ASQKD1(message, bases):
     
    simulator = AerSimulator()
    #print(bases)
    measurements = []
    for q in range(len(bases)):
        if bases[q] == 1: # measuring in Z-basis 
            message[q].measure(0,0)
        #if bases[q] == 0: # measuring in X-basis, all these are not removed for # ASQKD 1. 
         #   message[q].h(0)
         #   message[q].measure(0,0)
        #aer_sim = Aer.get_backend('aer_simulator')
            
            transpiled_qc = transpile(message[q], backend=AerSimulator())  
            result = simulator.run(transpiled_qc,  shots=1, memory=True).result()
            measured_bit = int(result.get_memory()[0])
            measurements.append(measured_bit)
    return measurements



############### ASQKD2 ################

#generate a quantumcircuit, by encoding each bit of alice's message on qubit in the X or Z basis at random. 
#0 : prepare in Zbasis , 1: prepare in the X-basis.  

def Bases_preparation_ASQKD2(B):
 
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
            ##else: Removed for ASQKD 2 - Produces single photons only in the computational basis. 
          #      r=randint(2, size=1)
               # if r == 0:
           #         qc.h(0)
                  #  R.append(0) #removed for ASQKD 1. 
              #  else:
            #        qc.x(0)
             #       qc.h(0)
                   # R.append(1) #removed for ASQKD 1. 

                S.append(qc) # Added under the main condition. 
 
    return S,R

#Applying measurement to simulate results of each qubits 
def measure_message_ASQKD2(message, bases):
   
    simulator = AerSimulator()
    #print(bases)
    measurements = []
    for q in range(len(message)):
        #if bases[q] == 1: # measuring in Z-basis  Removed because they are all in Z-basis. 
            message[q].measure(0,0)
        #if bases[q] == 0: # measuring in X-basis, all these are not removed for # ASQKD 1. 
         #   message[q].h(0)
         #   message[q].measure(0,0)
        #aer_sim = Aer.get_backend('aer_simulator')
         
            transpiled_qc = transpile(message[q], backend=AerSimulator()) #these are moved under the first condition. 
            result = simulator.run(transpiled_qc,  shots=1, memory=True).result()
            measured_bit = int(result.get_memory()[0])
            measurements.append(measured_bit)
    return measurements