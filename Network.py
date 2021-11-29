import networkx as nx
import random
import numpy as np
import time
import matplotlib.pyplot as plt

"""
Function
----------
This function aims to get an ER Network

Parameters
----------
1. Node_num : The number of the network
2. K: The average degree of the network
3. Infected_init_num: The number of the vertices infected at first
"""

def ER_Network(Node_num = 1000, K = 20, Infected_init_num = 10):

    # Calculate the Link_p
    Link_p = K / Node_num

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

    # Ensure the network is fully connected and the error of <k> is tolerable
    while nx.is_connected(G) == False or Degree_bias(G, K) > 0.001:
        print("Fail to create!")
        G = nx.erdos_renyi_graph(Node_num, Link_p)

    print("2.Network is generated!")

    G.name = "ER"

    return G, Infected

"""
Function
----------
This function aims to get an WS Network

Parameters
----------
1. Node_num : The number of the network
2. K: The average degree of the network
3. Link_p: The reconnect probability
4. Infected_init_num: The number of the vertices infected at first
5. Lower: The lower limit of the degree
"""
def WS_Network(Node_num = 1000, K = 20, Link_p = 0.5, Infected_init_num = 10, Lower = 4):

    # Generate the random infected node
    Infected = []
    while (len(Infected) < Infected_init_num):
        x = random.randint(0, Node_num - 1)
        if x not in Infected:
            Infected.append(x)

    print("1.Infected nodes are generated!")

    # Create the ER Graph
    G = nx.random_graphs.watts_strogatz_graph(Node_num, K, Link_p)

    # Ensure the network is fully connected and the error of <k> is tolerable
    while nx.is_connected(G) == False or Degree_bias(G, K) > 0.001:
        print("Fail to create!")
        G = nx.random_graphs.watts_strogatz_graph(Node_num, K, Link_p)

    print("2.Network is generated!")

    G.name = "WS"

    return G, Infected

"""
Function
----------
This function aims to get an BA Network

Parameters
----------
1. Node_num : The number of the network
2. Edge_num: The edge added per round, nearly equals the half of the <k>
3. Infected_init_num: The number of the vertices infected at first
"""
def BA_Network(Node_num = 1000, Edge_num = 1, Infected_init_num = 10):

    # Generate the random infected node
    Infected = []
    while (len(Infected) < Infected_init_num):
        x = random.randint(0, Node_num - 1)
        if x not in Infected:
            Infected.append(x)

    print("1.Infected nodes are generated!")

    # Create the ER Graph
    G = nx.random_graphs.barabasi_albert_graph(Node_num, Edge_num)

    while nx.is_connected(G) == False:
        print("Fail to create!")
        G = nx.random_graphs.barabasi_albert_graph(Node_num, Edge_num)
        ps = nx.shell_layout(G)

    print("2.Network is generated!")

    G.name = "BA"

    return G, Infected


"""
Function
----------
This function aims to get an Network from the real dataset
 
Parameters
----------
1. File_path : The Path of the dataset
2. Infected_init_num: The number of the vertices infected at first
"""
def Real_Network(File_path, Infected_init_num = 10):

    # Create the ScaleFree Graph
    ID = []

    G = nx.Graph()
    for line in open(File_path):
        strlist = line.split()
        n1 = int(strlist[0])
        n2 = int(strlist[1])
        G.add_edges_from([(n1, n2)])  # G.add_edges_from([(n1, n2)])
        ID.append(n1)
        ID.append(n2)

    ID = np.unique(ID)
    # Generate the random infected node
    Infected = []
    while (len(Infected) < Infected_init_num):
        x = random.randint(0, len(ID) - 1)
        if ID[x] not in Infected:
            Infected.append(ID[x])

    print("1.Infected nodes are generated!")

    print("2.Network is generated!")

    G.name = "ScaleFree"

    return G, Infected