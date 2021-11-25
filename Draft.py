import networkx as nx
import random
import numpy as np
import time
import matplotlib.pyplot as plt

Node_num = 10000
Coefficient = 0.8
Link_p = Coefficient*np.log(Node_num)/Node_num

BeginT = time.time()

# Generate the random infected node
Infected_init_num = 10
Infected = []
while(len(Infected) < Infected_init_num):
    x = random.randint(0, Node_num - 1)
    if x not in Infected:
        Infected.append(x)
print("1.Infected nodes are generated!")

GenerateNodeT = time.time()

# Initialize the state of the nodes, 1 denotes a healthy node while 0 denotes an infected node
Node_state = np.ones(Node_num).astype(np.int8)
Node_state[Infected] = 0

# Create the Random Graph
er = nx.erdos_renyi_graph(Node_num, Link_p)
ps = nx.shell_layout(er)

while nx.is_connected(er) == False:
    print("Fail to create!")
    er = nx.erdos_renyi_graph(Node_num, Link_p)
    ps = nx.shell_layout(er)

GenerateNetworkT = time.time()

print("2.Network is generated!")

# Get the Adjacent matrix of the Graph
A = np.array(nx.adjacency_matrix(er).astype(np.int8).todense())

print("3.Adjacent Matrix is prepared!")

# Define the transmission probability
Gamma = 0.4      # Transmission probability
Last_Infected = Infected_init_num

### Problem describe
### With the scale of the network increasing, the line is impossible to control
# If the Infected number is less than the Node number, it means still remains improving
while(len(Infected) < Node_num):
    Tmp = Infected
    print("Curent Infected: "+str(len(Infected)))
    # First Control the Node Infected
    for infected_index in Infected:
        # Second transmit the virus on its neighbors
        # Try to accelerate with the numpy

        # Generate the array containing all the random seed's state
        y = np.random.rand(Node_num)
        y = y * Node_state
        y = y * A[infected_index]

        # Get the state of this iter
        Infected_iter = np.array(np.intersect1d(np.where(y < Gamma)[0],np.where(y > 0)[0]))

        # Refresh the spreading in real time
        Node_state[Infected_iter] = 0

        # Refresh the state of the nodes
        Tmp = np.union1d(Infected_iter, Tmp)

        Infected = Tmp

FinishT = time.time()

print("Init the nodes cost : "+str(GenerateNodeT - BeginT))
print("Gegerate Network cost : "+str(GenerateNetworkT - GenerateNodeT))
print("Calculation cost : "+str(FinishT - GenerateNetworkT))

# nx.draw(er, ps, with_labels = True, node_size = Node_num, font_size = 8, node_color = "#CCFFFF")
# nx.draw(er, ps, with_labels = True, node_size = Node_num, font_size = 8, node_color = "#ff3333", nodelist = Infected)
# plt.show()