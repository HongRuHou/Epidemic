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
Infected_init_num = 100
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
Gamma = 0.50      # Transmission probability
Beta = 0.50       # Recovery probability

Last_Infected = Infected_init_num

x_label = []
Infected_label = []
Recovery_label = []

### Problem describe
for i in range(1, 500):

    x_label.append(i)
    # Fisrt Control the recovery of the Node Infected

    # Deep copy of Node_state
    Tmp_Node_state = Node_state.copy()
    zero_pos = np.array(np.where(Tmp_Node_state == 0)[0])
    one_pos = np.array(np.where(Tmp_Node_state == 1)[0])

    Tmp_Node_state[zero_pos] = 1
    Tmp_Node_state[one_pos] = 0

    x = np.random.rand(Node_num)
    x = x * Tmp_Node_state
    Recovry_iter = np.array(np.intersect1d(np.where(x < Beta)[0], np.where(x > 0)[0]))

    #print("Recovery in this iter is : "+ str(len(Recovry_iter)))
    Recovery_label.append(len(Recovry_iter))

    Node_state[Recovry_iter] = 1

    Infected = np.setdiff1d(Infected, Recovry_iter)

    Tmp = Infected.copy()

    # Second Control the Node Infected
    for infected_index in Infected:
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

    Infected = Tmp.copy()
    Infected_label.append(len(Infected))

FinishT = time.time()

print("Init the nodes cost : "+str(GenerateNodeT - BeginT))
print("Gegerate Network cost : "+str(GenerateNetworkT - GenerateNodeT))
print("Calculation cost : "+str(FinishT - GenerateNetworkT))

plt.xlabel("Iteration")
plt.ylabel("Number")
plt.plot(x_label,Recovery_label,label="Infected")
plt.plot(x_label,Infected_label,label="Recovered")
plt.legend()
plt.show()

# nx.draw(er, ps, with_labels = True, node_size = Node_num, font_size = 8, node_color = "#CCFFFF")
# nx.draw(er, ps, with_labels = True, node_size = Node_num, font_size = 8, node_color = "#ff3333", nodelist = Infected)
# plt.show()