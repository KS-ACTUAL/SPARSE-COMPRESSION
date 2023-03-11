from PIL import Image
import numpy as np
import re 
import matplotlib.pyplot as plt
import sys
import time
import array

img = Image.open('mnist1.jpg')
numpydata = np.asarray(img)

map_maps = {} ### {row : {column : value, column : value, ...}}


list_lists = [] ### [[row, [column, value], [column, value]],
              ### [row, [column, value], [column, value]], ....


def maps_compression():
    count = 0
    for i, j in enumerate(numpydata):
        if np.any(j):
            map_maps[i] = {}
        for k, l in enumerate(j):
            if l != 0: 
                count += 1
                map_maps[i][k] = l
    map_maps[numpydata.shape[0]+1] = {1 : numpydata.shape[0], 2 : numpydata.shape[1]}
    print("COUNT: ", count)
    return map_maps

def maps_decompress():
    data_size = np.array([map_maps[numpydata.shape[0]+1][1], map_maps[numpydata.shape[0]+1][2]])
    decompressed = np.zeros(data_size, dtype=int)
    for i, j in enumerate(decompressed):
        if i in map_maps.keys():
            for k in map_maps[i].keys():
                j[k] = map_maps[i][k]
    return decompressed

start = time.perf_counter_ns()
maps_compression()
end = time.perf_counter_ns()
print("\n")
print("Maps compression: {} ns".format(end - start))
# print("\n")
# print(map_maps)
print("\n")

start = time.perf_counter_ns()
maps_decompress()
end = time.perf_counter_ns()
print("Map-of-maps decompression: {} ns".format(end - start))

def lists_compression():
    for i, j in enumerate(numpydata):
        if np.any(j):
            list_lists.append([i])
        for k, l in enumerate(j):
            if l != 0:
                list_value = [k, l]
                list_lists[i].append(list_value)
    list_lists.append([numpydata.shape[0], numpydata.shape[1]])
    return list_lists

def lists_decompress():
    data_size = ([list_lists[-1][0], list_lists[-1][1]])
    decompressed = np.zeros(data_size, dtype=int)
    for j in list_lists[:-1]:
        for m in j[1:]:
            decompressed[j[0]][m[0]] = m[1]
    return decompressed

start = time.perf_counter_ns()
lists_compression()
end = time.perf_counter_ns()
print("\n")
print("Lists compression: {} ns".format(end - start))
# print("\n")
# print(lists_compression())
print("\n")

start = time.perf_counter_ns()
lists_decompress()
end = time.perf_counter_ns()
# print("\n")
print("List-of-list decompression: {} ns".format(end - start))
print("\n")