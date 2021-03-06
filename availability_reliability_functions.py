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

def dijkstraCalculation(graph, first, last, mode):
    min_path = nx.dijkstra_path(graph, first, last)
    H = graph.copy()
    for i in range(len(min_path)):
        if i < len(min_path) - 1:
            H.remove_edge(min_path[i], min_path[i + 1])
    try:
        not_min_path = nx.dijkstra_path(H, last, first)
    except Exception as e:
        return e

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

def getAllPaths(graph, source, target):
    paths = []
    for path in nx.all_simple_paths(graph, source=source, target=target):
        paths.append(path)

    paths = sorted(paths, key=lambda x: len(x))
    return paths

def averageAvailabilityDijkstra(graph):
    nodes = graph.nodes()
    all_availabilities = []
    for node in nodes:
        for node1 in nodes:
            if node1 > node:
                try:
                    all_availabilities.append(dijkstraCalculation(graph, node, node1, 'A'))
                except Exception as e:
                    return e
    sum_availabilities = 0
    for number in all_availabilities:
        sum_availabilities += number
    average = sum_availabilities / len(all_availabilities)
    return average

def stAvailabilityDijkstra(graph):
    nodes = graph.nodes()
    min_availability = 1000
    for node in nodes:
        for node1 in nodes:
            if node1 > node:
                try:
                    current = dijkstraCalculation(graph, node, node1, 'A')
                except Exception as e:
                    return e
                if current < min_availability:
                    min_availability = current
    return min_availability

def averageAvailabilityAbraham(graph):
    nodes = graph.nodes()
    all_availabilities = []
    for node in nodes:
        for node1 in nodes:
            if node1 > node:
                paths = getAllPaths(graph, node, node1)
                all_availabilities.append(abraham(graph, paths, 'A'))
    sum_availabilities = 0
    for number in all_availabilities:
        sum_availabilities += number
    average = sum_availabilities / len(all_availabilities)
    return average

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

def transformation(graph, t):
    transformed_graph = nx.Graph()
    nodes = graph.nodes()
    for node in nodes:
        lamb1 = graph.node[node]['failure_intensity']
        lamb1 = lamb1 / math.pow(10, 9)
        a, r = transformationCalculate(lamb1, graph.node[node]['repair_intensity'], t, 1)
        transformed_graph.add_node(node, A=a, R=r)

    for u, v, k in graph.edges(data=True):
        lamb1 = k['failure_intensity']
        lamb1 = lamb1 / math.pow(10, 9)
        mttr = k['repair_intensity']
        we = k['weight']
        a, r = transformationCalculate(lamb1, mttr, t, we)
        transformed_graph.add_edge(u, v, A=a, R=r, weight=k['weight'])
    return transformed_graph

def transformationCalculate(lamb, mttr, t, weight):
    if lamb == 0:
        return 1, 1
    mttf = (1 / lamb)/weight
    a = mttf / (mttf + mttr)
    r = math.exp(-lamb * t)
    return a, r
