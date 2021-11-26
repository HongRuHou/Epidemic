import networkx as nx
import random
import numpy as np
import time
import matplotlib.pyplot as plt

"""
Function
----------
This function aims to get an Network

Parameters
----------
1. Kind : The kind of the network, including ER, WS, ...
2. Node_num : The number of the network
3. Coefficient: Coefficient of the Link probability
4. Infected_init_num: The number of the vertices infected at first
5. FilePath : The Path of the dataset
"""
def ER_Network(Node_num = 1000, Coefficient = 1, Infected_init_num = 10):

    # Calculate the probability among vertices
    Link_p = Coefficient * np.log(Node_num) / Node_num

    # Generate the random infected node
    Infected = []
    while (len(Infected) < Infected_init_num):
        x = random.randint(0, Node_num - 1)
        if x not in Infected:
            Infected.append(x)

    print("1.Infected nodes are generated!")

    # Create the ER Graph
    G = nx.erdos_renyi_graph(Node_num, Link_p)
    ps = nx.shell_layout(G)

    while nx.is_connected(G) == False:
        print("Fail to create!")
        G = nx.erdos_renyi_graph(Node_num, Link_p)
        ps = nx.shell_layout(G)

    print("2.Network is generated!")

    return G, Infected