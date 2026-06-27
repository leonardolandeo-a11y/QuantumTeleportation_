from qiskit import QuantumCircuit,QuantumRegister,ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np 
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram,plot_bloch_vector
cr = ClassicalRegister(3)
qr = QuantumRegister(3)

qc = QuantumCircuit(qr,cr)

# Define a unknown qubit
phi = 3.654
lam = 0
theta = 5.3
qc.u(theta,phi,lam,qr[0])
x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)
plot_bloch_vector([x,y,z])

qc.barrier()

# Create the entanglement qubit
qc.h(qr[1])
qc.cx(qr[1],qr[2])
qc.barrier()

# Operations
qc.cx(qr[0],qr[1])
qc.h(qr[0])
qc.barrier()

# Measures
qc.measure(qr[1],cr[1])
qc.measure(qr[0],cr[0])
qc.barrier()

# Conditions 
with qc.if_test((cr,1)):
    qc.z(2)
with qc.if_test((cr,2)):
    qc.x(2)
with qc.if_test((cr,3)):
    qc.z(2)
    qc.x(2)

# Measure of the qubit of bob
qc.measure(qr[2],cr[2])


# Simulator
simulator = AerSimulator()
result = simulator.run(qc,shots= 1024).result()
count = result.get_counts()
print(count)
plot_histogram(count)
qc.draw("mpl")
plt.show()