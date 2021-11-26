import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def ScaleFree():

    filename = "Dataset/out.edgelist"

    G = nx.Graph()
    for line in open(filename) :
        strlist = line.split()
        n1 = int(strlist[0])
        n2 = int(strlist[1])
        G.add_edges_from([(n1, n2)]) #G.add_edges_from([(n1, n2)])

    print("Init finish")

    #nx.draw(G)

    print(np.array(nx.adjacency_matrix(G).astype(np.int8).todense()))

    print(len(G.nodes))

    plt.show()

kind = "ScaleFree"

if kind == "ScaleFree":
    print(111)