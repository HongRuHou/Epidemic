import numpy as np

arr1 = np.ones(10)
arr2 = np.zeros(10)

arr2[0:5] = 1

arr3 = arr1 + arr2

print(arr3)
