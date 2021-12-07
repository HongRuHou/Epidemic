import networkx as nx
import random
import numpy as np
import time
import matplotlib.pyplot as plt
from Tools import *

def ER_Network(Node_num = 1000, K = 20, Connectivity = True):
    """
    Function
    ----------
    This function aims to get an ER Network

    Parameters
    ----------
    1. Node_num : The number of the network
    2. K: The average degree of the network
    3. Connectivity: Determine whether the ER network generated should be fully connected
    """
    # Calculate the Link_p
    Link_p = K / Node_num

    # Create the ER Graph
    G = nx.erdos_renyi_graph(Node_num, Link_p)
    ps = nx.shell_layout(G)

    # Ensure the network is fully connected and the error of <k> is tolerable
    if Connectivity == True:
        while nx.is_connected(G) == False or Degree_bias(G, K) > 0.001:
            #print(Degree(G))
            #print("Fail to create!")
            G = nx.erdos_renyi_graph(Node_num, Link_p)
    else:
        while Degree_bias(G, K) > 0.001:
            G = nx.erdos_renyi_graph(Node_num, Link_p)

    # print("1.ER Network is generated!")

    G.name = "ER"

    return G


def WS_Network(Node_num = 1000, K = 20, Link_p = 0.5):
    """
    Function
    ----------
    This function aims to get an WS Network

    Parameters
    ----------
    1. Node_num : The number of the network
    2. K: The average degree of the network
    3. Link_p: The reconnect probability
    """

    # Create the ER Graph
    G = nx.random_graphs.watts_strogatz_graph(Node_num, K, Link_p)

    # Ensure the network is fully connected and the error of <k> is tolerable
    while nx.is_connected(G) == False or Degree_bias(G, K) > 0.001:
        #print(Degree(G))
        #print("Fail to create!")
        G = nx.random_graphs.watts_strogatz_graph(Node_num, K, Link_p)

    print("1.WS Network is generated!")

    G.name = "WS"

    return G


def BA_Network(Node_num = 1000, Edge_num = 1):
    """
    Function
    ----------
    This function aims to get an BA Network

    Parameters
    ----------
    1. Node_num : The number of the network
    2. Edge_num: The edge added per round, nearly equals the half of the <k>
    """

    # Create the ER Graph
    G = nx.random_graphs.barabasi_albert_graph(Node_num, Edge_num)

    while nx.is_connected(G) == False:
        #print("Fail to create!")
        G = nx.random_graphs.barabasi_albert_graph(Node_num, Edge_num)
        ps = nx.shell_layout(G)

    print("1.BA Network is generated!")

    G.name = "BA"

    return G

def Real_Network(File_path):
    """
    Function
    ----------
    This function aims to get an Network from the real dataset

    Parameters
    ----------
    1. File_path : The Path of the dataset
    """
    # Create the ScaleFree Graph

    G = nx.Graph()
    for line in open(File_path):
        strlist = line.split()
        n1 = int(strlist[0])
        n2 = int(strlist[1])
        G.add_edges_from([(n1, n2)])  # G.add_edges_from([(n1, n2)])

    print("1.Real Network Network is generated!")

    G.name = "ScaleFree"

    return G



def Karate_club_Network():
    """
    Function
    ----------
    This function aims to get a Karate-club Network

    """
    G = nx.karate_club_graph()

    G.name = "Karate"

    return G