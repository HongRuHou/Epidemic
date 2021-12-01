import numpy as np
import math
from Network import *

def CalLength(List):
    _len = 0
    for l in List:
        _len = _len + len(str(l))
    return _len

def Entropy(G):

    Node_num = len(G)
    A = np.array(nx.adjacency_matrix(G).astype(np.int8).todense())

    # A = np.array([[0,1,1,0],
    #               [1,0,1,1],
    #               [1,1,0,0],
    #               [0,1,0,0]])

    # The data of the Entropy
    """
    1. Pk : The collection of Pk, Pk[0] is the target
    2. B1 : The set consists of the fragment whose length > 1
    3. B2 : The set consists of the fragment whose length = 1
    """
    Pk = []
    Pk.append(np.arange(0, Node_num, 1).tolist())
    B1 = []
    B2 = []

    # Iteration for all of the nodes
    for k in range(0, Node_num):
        # print("***************")
        # print("Pk is :" + str(Pk))

        # Get the first part of Pk
        Pk1 = Pk[0]

        # Get the v from Pk1
        v = Pk1[0]

        # print("V is :" + str(v))

        # Calculate the P_(k-1) - v
        Pk_no_v = Pk
        Pk_no_v_first = Pk_no_v[0]
        Pk_no_v_first.remove(v)

        # If the top of the P_(k-1) - v is [], remove it
        if len(Pk_no_v_first) == 0:
            Pk_no_v.remove(Pk_no_v[0])
        else:
            Pk_no_v[0] = Pk_no_v_first

        # Deep copy of Pk_no_v
        Pk_1 = Pk_no_v.copy()

        # print("Pk_1 is :" + str(Pk_1))

        # Find the neighbors of v
        Neighbor_v = np.where(A[v] == 1)

        Pk = []
        for i in range(0, len(Pk_1)):
            # print("---------------")

            # Get the content of Pk_1 in order
            U = Pk_1[i]

            # print("U is :" + str(U))

            Neighbors_in_U = np.intersect1d(Neighbor_v, np.array(U))

            bitMaxlen = math.ceil(np.log2(len(U) + 1))

            # Change the neighbor's number into the binary format
            b = bin(len(Neighbors_in_U))[2:]
            #print(bitMaxlen,b)

            # If the length of neighbor is 1
            if bitMaxlen == 1:
                B2.append(b)
            else:
                # If the length after alter the format is short , enlarging it
                if(len(b) < bitMaxlen):
                    str_b = ""
                    for j in range(0, bitMaxlen - len(b)):
                        str_b = str_b + str(0)
                    str_b = str_b + b
                    b = str_b
                B1.append(b)

            # print("---------------")

            # If there is no neighbors in Pk_1[i]
            Pk_temp = []
            if(len(Neighbors_in_U) == 0):
                Pk_temp.append(np.setdiff1d(U, Neighbors_in_U).tolist())
            elif (len(np.setdiff1d(U, Neighbors_in_U)) == 0):
                Pk_temp.append(Neighbors_in_U.copy().tolist())
            else:
                Pk_temp.append(Neighbors_in_U.copy().tolist())
                Pk_temp.append(np.setdiff1d(U, Neighbors_in_U).tolist())

            # print("Pk_temp : " + str(Pk_temp))

            for p in Pk_temp:
                Pk.append(p)

            # print("Pk : " + str(Pk))


        # print("***************")

    print("B1 is :" + str(B1))
    print("B2 is :" + str(B2))
    print("Total length is :" + str(CalLength(B1)+CalLength(B2)))

if __name__ == '__main__':

    er = nx.erdos_renyi_graph(8, 0.2)
    ps = nx.shell_layout(er)

    nx.draw(er, ps, with_labels=True, node_size=4, font_size=8, node_color="#CCFFFF")

    Entropy(er)

    plt.show()


