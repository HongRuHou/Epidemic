import networkx as nx
import random
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

"""
Function
----------
This function aims to achieve the simulation of SIR Model

Parameters
----------
1. G : Input Graph
2. Infected : The ndarray including the nodes infected at first
3. Gamma: Transmission probability
4. Beta: Recovery probability
5. Epoch : The iterations in total
6. Drawing: Whether to draw the pic in this function
"""
def Evolution_SIR(G, Infected, Gamma = 0.5, Beta = 0.50, Epoch = 20, Drawing = False):

    # Get the number of the nodes
    Node_num = len(G.nodes)

    # Initialize the state of the nodes, -1 denotes a recovered node, 1 denotes a suspetible node while 0 denotes an infected node
    Node_state = np.ones(Node_num).astype(np.int8)
    Node_state[Infected] = 0

    # Get the Adjacent matrix of the Graph
    A = np.array(nx.adjacency_matrix(G).astype(np.int8).todense())

    print("3.Adjacent Matrix is prepared!")

    x_label = [0]
    Infected_label = [len(Infected)]
    Recovery_label = [0]

    ### Problem describe
    for i in range(1, Epoch):

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

        Recovery_label.append(len(Recovry_iter))

        # Set the recovery node state to -1
        Node_state[Recovry_iter] = -1

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

    if Drawing == True:
        plt.xlabel("Iteration")
        plt.ylabel("Number")
        plt.plot(x_label,Recovery_label,label="Recovered")
        plt.plot(x_label,Infected_label,label="Infected")

        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(1))
        plt.xlim(-0.5, Epoch)

        plt.legend()
        plt.savefig("Output/"+str(G.name)+"/output_SIS.jpg")
        plt.close()

    return Infected_label, Recovery_label