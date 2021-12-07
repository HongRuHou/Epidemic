import networkx as nx
import numpy as np
import time
from Network import *
from SI import *
from SIS import  *
from networkx.algorithms.cluster import _triangles_and_degree_iter
from matplotlib.pyplot import MultipleLocator

def Degree(G, Print = False):
    """
    Function
    ----------
    This function aims to calculate of the average degree of a graph

    Parameters
    ----------
    1. G : Input Graph
    """

    if Print == True:
        print(G.name + " :" + str(np.mean(np.array(G.degree), axis=0)[1]))
    return np.mean(np.array(G.degree), axis=0)[1]


def Degree_bias(G, K):
    """
    Function
    ----------
    This function aims to calculate of bias among the average degree and the real degree

    Parameters
    ----------
    1. G : Input Graph
    2. K : Ideal degree
    """

    if K == 0:
        return 0
    bias = abs(Degree(G, Print=False) - K) / K
    return bias


def Clustering_coefficient(G):
    """
    Function
    ----------
    This function aims to calculate the Average Clustering coefficient

    Parameters
    ----------
    1. G : Input Graph
    """

    Clustering = nx.clustering(G)
    A = np.array([Clustering[i] for i in Clustering])

    return np.mean(A)


def Triangle_Counting(G):
    """
    Function
    ----------
    This function aims to calculate the Triangles in a network

    Parameters
    ----------
    1. G : Input Graph
    """
    triangles_contri = [
        (t, d * (d - 1)) for v, d, t, _ in _triangles_and_degree_iter(G)
    ]
    # If the graph is empty
    if len(triangles_contri) == 0:
        return 0
    triangles, contri = map(sum, zip(*triangles_contri))

    return sum(nx.triangles(G).values()) // 3


def MultiEvolution_SIS(G, Infected, Iteration = 1,):
    """
    Function
    ----------
    This function aims to simulate the iteration of the SIS Model

    Parameters
    ----------
    1. G : Input Graph
    """

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

    File_path = "Dataset/Facebook/facebook_combined.txt"
    Node_num = 4039
    K = 44
    Infected_init_num = 100

    # The state of whether to use the network or not
    # Denotes WS, ER, BA, Real, Karate respectively
    State = [1, 1, 1, 1, 0]

    network = []
    for idx, state in enumerate(State):
        if state == 1:
            if idx == 0:
                WS = WS_Network(Node_num=Node_num, K=K, Link_p=0.0)
                network.append([WS, []])
            elif idx == 1:
                ER = ER_Network(Node_num=Node_num, K=K)
                network.append([ER, []])
            elif idx == 2:
                BA = BA_Network(Node_num=Node_num, Edge_num=22)
                network.append([BA, []])
            elif idx == 3:
                Real = Real_Network(File_path=File_path)
                network.append([Real, []])
            elif idx == 4:
                Karate = Karate_club_Network()
                network.append([Karate, []])

    for G in network:
        print("Network : " + G[0].name +
              ", Degree : " + str(Degree(G[0])) +
              ", Clustering Coefficent : " + str(Clustering_coefficient(G[0])) +
              ", Triangle Count :" + str(Triangle_Counting(G[0])))

    # The average Iter
    Iter = 100

    EX = False

    # The number of the evolution in each Iter
    Epoch = 25
    Gamma = 0.10
    xlabel = np.arange(0, Epoch, 1).astype(np.int8)

    if EX == True:
        for G in network:
            # The variable in each iteration is Infected
            for i in range(0, Iter):
                Infected = []
                while (len(Infected) < Infected_init_num):
                    x = random.randint(0, Node_num - 1)
                    if x not in Infected:
                        Infected.append(x)

                print("Network :" + G[0].name + ", Iter : " + str(i))
                G[1].append(Evolution_SI(G = G[0], Infected = Infected, Gamma = Gamma, Epoch = Epoch))

            plt.xlabel("Iteration")
            plt.ylabel("Number")
            plt.plot(xlabel, np.mean(G[1], axis=0).astype(np.int32), label="Infected")

            ax = plt.gca()
            ax.xaxis.set_major_locator(MultipleLocator(1))
            plt.xlim(-0.5, Epoch)

            plt.legend()
            plt.savefig("Output/" + str(G[0].name) + "/2k_output_SI_gamma="+str(Gamma)+".jpg")
            plt.close()

if __name__ == '__main__':
    Evolution()