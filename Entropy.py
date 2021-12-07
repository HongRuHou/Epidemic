import numpy as np
import math
import time
from scipy.io import  loadmat
from Network import *

def CalLength(List):
    _len = 0
    for l in List:
        _len = _len + len(str(l))
    return _len

def Entropy(A, Log = False):

    Node_num = A.shape[0]

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

        # print("Iter:" + str(k))

        # Get the first part of Pk
        Pk1 = Pk[0]

        # Get the v from Pk1
        v = Pk1[0]

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
        #Pk_1 = Pk_no_v.copy()
        Pk_1 = Pk_no_v

        # Find the neighbors of v
        Neighbor_v = np.where(A[v] == 1)

        Pk = []
        for i in range(0, len(Pk_1)):

            # Get the content of Pk_1 in order
            U = Pk_1[i]

            Neighbors_in_U = np.intersect1d(Neighbor_v, np.array(U))

            bitMaxlen = math.ceil(np.log2(len(U) + 1))

            # Change the neighbor's number into the binary format
            b = bin(len(Neighbors_in_U))[2:]

            # If the length of neighbor is 1
            if bitMaxlen == 1:
                B2.append(b)
            else:
                # If the length after alter the format is short , enlarging it
                # Multiply is faster than for, while the data iteration is huge
                if(len(b) < bitMaxlen):
                    str_b = "0"*(bitMaxlen - len(b))
                    b = str_b + b
                B1.append(b)

            # If there is no neighbors in Pk_1[i]
            Pk_temp = []
            if(len(Neighbors_in_U) == 0):
                Pk_temp.append(np.setdiff1d(U, Neighbors_in_U).tolist())
            elif (len(np.setdiff1d(U, Neighbors_in_U)) == 0):
                Pk_temp.append(Neighbors_in_U.tolist())
            else:
                Pk_temp.append(Neighbors_in_U.tolist())
                Pk_temp.append(np.setdiff1d(U, Neighbors_in_U).tolist())

            for p in Pk_temp:
                Pk.append(p)

    if Log == True:
        Output = open('Output/Compression/output.txt', 'w')
        Output.write("B1 is :" + str((B1))+"\n")
        Output.write("B2 is :" + str((B2)) + "\n")
        Output.write("B1 length is :" + str(CalLength(B1)) + "\n")
        Output.write("B2 length is :" + str(CalLength(B2)) + "\n")
        Output.write("Total length is :" + str(CalLength(B1) + CalLength(B2)) + "\n")
        Output.close()

    return CalLength(B1) + CalLength(B2)

def Reader(File_path):

    annots = loadmat(File_path)

    A = np.array(annots.get('A').todense()).astype(np.int8)

    G = nx.Graph(A)

    return np.array(nx.adjacency_matrix(G).todense()).astype(np.int8)

if __name__ == '__main__':

    File_path = 'Dataset/Compression/PPI.mat'

    A = Reader(File_path)

    Entropy(A)
