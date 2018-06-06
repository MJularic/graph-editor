import networkx as nx
import math
from abraham import abraham


def calculateReliability(graph, path):
    reliability = 1
    for i in range(len(path)):
        reliability *= graph.node[path[i]]['R']

    for i in range(len(path) - 1):
        if i < len(path) - 1:
            reliability *= graph.get_edge_data(path[i], path[i + 1])['R']
    return reliability


def calculateAvailability(graph, path):
    availability = 1
    for i in range(len(path)):
        availability *= graph.node[path[i]]['A']

    for i in range(len(path) - 1):
        if i < len(path) - 1:
            availability *= graph.get_edge_data(path[i], path[i + 1])['A']
    return availability


# 8a+izracun, 9a
def dijkstraCalculation(graph, first, last, mode):
    min_path = nx.dijkstra_path(graph, first, last)
    H = graph.copy()
    for i in range(len(min_path)):
        if i < len(min_path) - 1:
            H.remove_edge(min_path[i], min_path[i + 1])

    not_min_path = nx.dijkstra_path(H, first, last)

    if mode == 'A':
        up = calculateAvailability(graph, min_path)
        down = calculateAvailability(graph, not_min_path)

    if mode == 'R':
        up = calculateReliability(graph, min_path)
        down = calculateReliability(graph, not_min_path)

    paralel_1 = up / (graph.node[min_path[0]][mode] * graph.node[min_path[len(min_path) - 1]][mode])
    paralel_2 = down / (graph.node[not_min_path[0]][mode] * graph.node[not_min_path[len(not_min_path) - 1]][mode])
    paralel_final = (1 - (1 - paralel_1) * (1 - paralel_2))

    final_a = graph.node[min_path[0]][mode] * graph.node[min_path[len(min_path) - 1]][mode] * paralel_final
    return final_a


# 8c
def getAllPaths(graph, source, target):
    paths = []
    for path in nx.all_simple_paths(graph, source=source, target=target):
        paths.append(path)

    paths = sorted(paths, key=lambda x: len(x))
    return paths


# za sve parove cvorova
# 10
def averageAvailabilityDijkstra(graph):
    nodes = graph.nodes()
    all_availabilities = []
    for node in nodes:
        for node1 in nodes:
            if node1 > node:
                all_availabilities.append(dijkstraCalculation(graph, node, node1, 'A'))
    sum_availabilities = 0
    for number in all_availabilities:
        sum_availabilities += number
    average = sum_availabilities / len(all_availabilities)
    return average


# 10
def stAvailabilityDijkstra(graph):
    nodes = graph.nodes()
    min_availability = 1000
    for node in nodes:
        for node1 in nodes:
            if node1 > node:
                current = dijkstraCalculation(graph, node, node1, 'A')
                if current < min_availability:
                    min_availability = current
    return min_availability


# 10
def averageAvailabilityAbraham(graph):
    nodes = graph.nodes()
    all_availabilities = []
    for node in nodes:
        for node1 in nodes:
            if node1 > node:
                paths = getAllPaths(graph, node, node1)
                print(paths)
                all_availabilities.append(abraham(graph, paths, 'A'))
    sum_availabilities = 0
    for number in all_availabilities:
        sum_availabilities += number
    average = sum_availabilities / len(all_availabilities)
    return average


# 10
def stAvailabilityAbraham(graph):
    nodes = graph.nodes()
    min_availability = 1000
    for node in nodes:
        for node1 in nodes:
            if node1 > node:
                paths = getAllPaths(graph, node, node1)
                current = abraham(graph, paths, 'A')
                if current < min_availability:
                    min_availability = current
    return min_availability


# 8b+izracun, 9a
# TREBAJU SAMO VRHOVI U oblikzu [1, 2, 3, 4] gdje su 1,2,3,4 vrhovi koji ulaze u taj put
def customPath(graph, path1, path2, mode):
    if mode == 'A':
        up = calculateAvailability(graph, path1)
        down = calculateAvailability(graph, path2)
    if mode == 'R':
        up = calculateReliability(graph, path1)
        down = calculateAvailability(graph, path2)

    paralel_1 = up / (graph.node[path1[0]][mode] * graph.node[path1[len(path1) - 1]][mode])
    paralel_2 = down / (graph.node[path2[0]][mode] * graph.node[path2[len(path2) - 1]][mode])
    paralel_final = (1 - (1 - paralel_1) * (1 - paralel_2))
    final = graph.node[path1[0]][mode] * graph.node[path1[len(path1) - 1]][mode] * paralel_final
    return final


# 8b+izracun, 9b
def customPathReliability(graph, path1,
                          path2):  # TREBAJU SAMO VRHOVI U oblikzu [1, 2, 3, 4] gdje su 1,2,3,4 vrhovi koji ulaze u taj put
    up_r = calculateReliability(graph, path1)

    down_r = calculateReliability(graph, path2)

    paralel_1_r = up_r / (graph.node[path1[0]]['R'] * graph.node[path1[len(path1) - 1]]['R'])
    paralel_2_r = down_r / (graph.node[path2[0]]['R'] * graph.node[path2[len(path2) - 1]]['R'])
    paralel_final_r = (1 - (1 - paralel_1_r) * (1 - paralel_2_r))

    final_r = graph.node[path1[0]]['R'] * graph.node[path1[len(path1) - 1]]['R'] * paralel_final_r

    return final_r


def transformation(graph, t):
    novi = nx.Graph()
    nodes = graph.nodes()
    for node in nodes:
        a, r = transformationCalculate(graph.node[node]['failure_intensity'], graph.node[node]['repair_intensity'], t)
        novi.add_node(node, A=a, R=r)

    for u, v, k in graph.edges(data=True):
        lamb1 = k['failure_intensity']
        mi1 = k['repair_intensity']
        a, r = transformationCalculate(lamb1, mi1, t)
        novi.add_edge(u, v, A=a, R=r, weight=k['weight'])
    return novi


def transformationCalculate(lamb, mi, t):
    MTTF = 1 / lamb
    MTTR = 1 / mi
    A = MTTF / (MTTF + MTTR)
    R = math.exp(-lamb * t)
    return A, R
