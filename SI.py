import networkx as nx
import random
import numpy as np
import time
import matplotlib.pyplot as plt

Node_num = 10000
Coefficient = 1
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

# Initialize the state of the nodes, 0 denotes a healthy node while 1 denotes an infected node
Node_state = np.zeros(Node_num).astype(np.int8)
Node_state[Infected] = 1

# Create the Random Graph
er = nx.erdos_renyi_graph(Node_num, Link_p)
ps = nx.shell_layout(er)

while nx.is_connected(er) == False:
    er = nx.erdos_renyi_graph(Node_num, Link_p)
    ps = nx.shell_layout(er)

GenerateNetworkT = time.time()

print("2.Network is generated!")

# Get the Adjacent matrix of the Graph
A = np.array(nx.adjacency_matrix(er).astype(np.int8).todense())

print("3.Adjacent Matrix is prepared!")

# Define the transmission probability
Gamma = 1.0      # Transmission probability
End_T = 1000
End_times = End_T
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
        for idx, Neighbor_Node in enumerate(A[infected_index]):
            # If the link lies between Infected and neighbor
            if Neighbor_Node == 1:
            # If the neighbor is not infected, try to infected
                if  Node_state[idx] == 0:
                    y = random.random()
                    if y < Gamma:
                        Tmp.append(idx)
                        Node_state[idx] = 1
            Last_Infected = len(Tmp)
    if(Last_Infected == len(Tmp)):
        End_times = End_times - 1
        print(End_times)
        if(End_times <= 0):
            break
    else:
        Infected = Tmp
        End_times = End_T

FinishT = time.time()

print("Init the nodes cost : "+str(GenerateNodeT - BeginT))
print("Gegerate Network cost : "+str(GenerateNetworkT- GenerateNodeT))
print("Calculation cost : "+str(FinishT - GenerateNetworkT))

nx.draw(er, ps, with_labels = True, node_size = Node_num, font_size = 8, node_color = "#CCFFFF")
nx.draw(er, ps, with_labels = True, node_size = Node_num, font_size = 8, node_color = "#ff3333", nodelist = Infected)
plt.show()