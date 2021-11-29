import networkx as nx
import numpy as np
import time
from Network import *
from SI import *
from SIS import  *
from matplotlib.pyplot import MultipleLocator

"""
Function
----------
This function aims to calculate of the average degree of a graph

Parameters
----------
1. G : Input Graph
"""
def Degree(G, Print = True):
    if Print == True:
        print(G.name + " :" + str(np.mean(np.array(G.degree), axis=0)[1]))
    return np.mean(np.array(G.degree), axis=0)[1]

def Degree_bias(G, K):
    bias = abs(Degree(G, Print=True) - K) / K
    return bias


"""
Function
----------
This function aims to simulate the iteration of the SIS Model

Parameters
----------
1. G : Input Graph
"""
def MultiEvolution_SIS(G, Infected, Iteration = 1,):

    File_path = "Dataset/out.edgelist"
    Node_num = 20000
    ER_Coefficient = 2.355
    WS_Coefficient = 2
    Infected_init_num = 100

    WS, Infected_WS = WS_Network(Node_num = Node_num, Coefficient = WS_Coefficient, Infected_init_num = Infected_init_num)
    ER, Infected_ER = ER_Network(Node_num = Node_num, Coefficient = ER_Coefficient, Infected_init_num = Infected_init_num)
    BA, Infected_BA = BA_Network(Node_num=Node_num, Edge_num = 10, Infected_init_num = Infected_init_num)

    Degree(WS)
    Degree(ER)
    Degree(BA)

    WS_SI = []
    ER_SI = []
    BA_SI = []

    network = [[WS, WS_SI], [ER, ER_SI], [BA, BA_SI]]

    # Degree(WS)
    # Degree(ER)
    # Degree(BA)

    # The average Iter
    Iter = 1

    # The number of the evolution in each Iter
    Epoch = 20
    xlabel = np.arange(0, Epoch, 1).astype(np.int8)

    for G in network:
        for i in range(0, Iter):
            G[1].append(Evolution_SI(G = G[0], Infected = Infected_WS, Gamma = 0.5, Epoch = Epoch))

        plt.xlabel("Iteration")
        plt.ylabel("Number")
        plt.plot(xlabel, np.mean(G[1], axis=0).astype(np.int32), label="Infected")

        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(1))
        plt.xlim(-0.5, Epoch)

        plt.legend()
        plt.savefig("Output/" + str(G[0].name) + "/output_SI.jpg")
        plt.close()

def Evolution():

    File_path = "Dataset/out.edgelist"
    Node_num = 1000
    ER_Coefficient = 2.355
    WS_Coefficient = 2
    Infected_init_num = 100

    WS, Infected_WS = WS_Network(Node_num = Node_num, Coefficient = WS_Coefficient, Infected_init_num = Infected_init_num)
    ER, Infected_ER = ER_Network(Node_num = Node_num, Coefficient = ER_Coefficient, Infected_init_num = Infected_init_num)
    BA, Infected_BA = BA_Network(Node_num=Node_num, Edge_num = 10, Infected_init_num = Infected_init_num)

    Degree(WS)
    Degree(ER)
    Degree(BA)

    WS_SI = []
    ER_SI = []
    BA_SI = []

    network = [[WS, WS_SI], [ER, ER_SI], [BA, BA_SI]]

    # Degree(WS)
    # Degree(ER)
    # Degree(BA)

    # The average Iter
    Iter = 1

    # The number of the evolution in each Iter
    Epoch = 20
    xlabel = np.arange(0, Epoch, 1).astype(np.int8)

    for G in network:
        for i in range(0, Iter):
            G[1].append(Evolution_SI(G = G[0], Infected = Infected_WS, Gamma = 0.5, Epoch = Epoch))

        plt.xlabel("Iteration")
        plt.ylabel("Number")
        plt.plot(xlabel, np.mean(G[1], axis=0).astype(np.int32), label="Infected")

        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(1))
        plt.xlim(-0.5, Epoch)

        plt.legend()
        plt.savefig("Output/" + str(G[0].name) + "/output_SI.jpg")
        plt.close()