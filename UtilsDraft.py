import numpy as np

arr1 = np.ones(10)
arr2 = np.zeros(10)

arr3 = arr2.copy()

arr3[:] = 1

print(arr3)
print(arr2)
