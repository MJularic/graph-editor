import networkx as nx
from networkx import Graph
import math
from abraham import abraham


def calculateReliability(graph, path):
    reliability = 1
    for i in range(len(path)):
        reliability *= graph.node[path[i]]['R']

    for i in range(len(path) - 1):
        if (i < len(path) - 1):
            reliability *= graph.get_edge_data(path[i], path[i + 1])['R']
    return reliability


def calculateAvailability(graph, path):
    availability = 1
    for i in range(len(path)):
        availability *= graph.node[path[i]]['A']

    for i in range(len(path) - 1):
        if (i < len(path) - 1):
            availability *= graph.get_edge_data(path[i], path[i + 1])['A']
    return availability


# 8a+izracun, 9a
def dijkstraFunctionReliability(graph, first, last):
    minpath = nx.dijkstra_path(graph, first, last)
    H = graph.copy()
    for i in range(len(minpath)):
        if (i < len(minpath) - 1):
            H.remove_edge(minpath[i], minpath[i + 1])

    notminpath = nx.dijkstra_path(H, first, last)

    upR = calculateReliability(graph, minpath)

    downR = calculateReliability(graph, notminpath)

    paralel1R = upR / (graph.node[minpath[0]]['R'] * graph.node[minpath[len(minpath) - 1]]['R'])
    paralel2R = downR / (graph.node[notminpath[0]]['R'] * graph.node[notminpath[len(notminpath) - 1]]['R'])
    paralelFinalR = (1 - (1 - paralel1R) * (1 - paralel2R))

    finalR = graph.node[minpath[0]]['R'] * graph.node[minpath[len(minpath) - 1]]['R'] * paralelFinalR
    print("Dijkstra function reliability " + str(finalR))
    return finalR


# 8a+izracun, 9a
def dijkstraFunctionAvailability(graph, first, last):
    minpath = nx.dijkstra_path(graph, first, last)
    H = graph.copy()
    for i in range(len(minpath)):
        if (i < len(minpath) - 1):
            H.remove_edge(minpath[i], minpath[i + 1])

    notminpath = nx.dijkstra_path(H, first, last)

    upA = calculateAvailability(graph, minpath)

    downA = calculateAvailability(graph, notminpath)

    paralel1A = upA / (graph.node[minpath[0]]['A'] * graph.node[minpath[len(minpath) - 1]]['A'])
    paralel2A = downA / (graph.node[notminpath[0]]['A'] * graph.node[notminpath[len(notminpath) - 1]]['A'])
    paralelFinalA = (1 - (1 - paralel1A) * (1 - paralel2A))

    finalA = graph.node[minpath[0]]['A'] * graph.node[minpath[len(minpath) - 1]]['A'] * paralelFinalA
    print("Dijkstra function availability" + str(finalA))
    return finalA


# 8c
def getAllPaths(graph, source, target):
    paths = []
    for path in nx.all_simple_paths(graph, source=source, target=target):
        paths.append(path)
    number = len(paths)
    return paths


# za sve parove cvorova
# 10
def averageAvailabilityDijkstra(graph):
    nodes = graph.nodes()
    allAvailabilities = []
    for node in nodes:
        for node1 in nodes:
            if (node1 > node):
                allAvailabilities.append(dijkstraFunctionAvailability(graph, node, node1))
    sum = 0
    for number in allAvailabilities:
        sum += number
    average = sum / len(allAvailabilities)
    print("Average availabilitsy is: " + str(average))
    return average


# 10
def stAvailabilityDijkstra(graph):
    nodes = graph.nodes()
    minAvailability = 1000
    for node in nodes:
        for node1 in nodes:
            if (node1 > node):
                curr = dijkstraFunctionAvailability(graph, node, node1)
                if (curr < minAvailability):
                    minAvailability = curr
    print("st Availability is: " + str(minAvailability))
    return minAvailability


# 10
def averageAvailabilityAbraham(graph):
    nodes = graph.nodes()
    allAvailabilities = []
    for node in nodes:
        for node1 in nodes:
            if (node1 > node):
                paths = getAllPaths(graph, node, node1)
                allAvailabilities.append(abraham(graph, paths))
    sum = 0
    for number in allAvailabilities:
        sum += number
    average = sum / len(allAvailabilities)
    print("Average availability is: " + str(average))
    return average


# 10
def stAvailabilityAbraham(graph):
    nodes = graph.nodes()
    minAvailability = 1000
    for node in nodes:
        for node1 in nodes:
            if (node1 > node):
                paths = getAllPaths(graph, node, node1)
                curr = abraham(graph, paths)
                if (curr < minAvailability):
                    minAvailability = curr
    print("st Availability is: " + str(minAvailability))
    return minAvailability


# 8b+izracun, 9a
# TREBAJU SAMO VRHOVI U oblikzu [1, 2, 3, 4] gdje su 1,2,3,4 vrhovi koji ulaze u taj put
def customPathAvailability(graph, path1, path2):
    upA = calculateAvailability(graph, path1)


    downA = calculateAvailability(graph, path2)
    paralel1A = upA / (graph.node[path1[0]]['A'] * graph.node[path1[len(path1) - 1]]['A'])
    paralel2A = downA / (graph.node[path2[0]]['A'] * graph.node[path2[len(path2) - 1]]['A'])
    paralelFinalA = (1 - (1 - paralel1A) * (1 - paralel2A))
    finalA = graph.node[path1[0]]['A'] * graph.node[path1[len(path1) - 1]]['A'] * paralelFinalA
    print("CUSTOM Avail" + str(finalA))
    return finalA


# 8b+izracun, 9b
def customPathReliability(graph, path1,
                          path2):  # TREBAJU SAMO VRHOVI U oblikzu [1, 2, 3, 4] gdje su 1,2,3,4 vrhovi koji ulaze u taj put
    upR = calculateReliability(graph, path1)

    downR = calculateReliability(graph, path2)

    paralel1R = upR / (graph.node[path1[0]]['R'] * graph.node[path1[len(path1) - 1]]['R'])
    paralel2R = downR / (graph.node[path2[0]]['R'] * graph.node[path2[len(path2) - 1]]['R'])
    paralelFinalR = (1 - (1 - paralel1R) * (1 - paralel2R))

    finalR = graph.node[path1[0]]['R'] * graph.node[path1[len(path1) - 1]]['R'] * paralelFinalR

    print("CUSTOM REL" + str(finalR))
    return finalR


def transformation(graph, t):
    novi = nx.Graph()
    nodes = graph.nodes()
    for i in range(1, len(nodes) + 1):
        a, r = transformationCalculate(graph.node[i]['lamb'], graph.node[i]['mi'], t)
        novi.add_node(i, A=a, R=r)

    for u, v, k in graph.edges(data=True):
        lamb1 = k['lamb']
        mi1 = k['mi']
        a, r = transformationCalculate(lamb1, mi1, t)
        novi.add_edge(u, v, A=a, R=r, weight=k['weight'])
    return novi


def transformationCalculate(lamb, mi, t):
    MTTF = 1 / lamb
    MTTR = 1 / mi
    A = MTTF / (MTTF + MTTR)
    R = math.exp(-lamb * t)
    # print("Izracunati A "+str(A)+" i R "+str(R))
    return A, R


# nx.draw(G)
# plt.show()

F = nx.Graph()

F.add_node(1, lamb=0.4, mi=0.999)
F.add_node(2, lamb=0.2, mi=0.2)
F.add_node(3, lamb=0.8, mi=0.44)
F.add_node(4, lamb=0.9, mi=0.32)

e1 = (1, 2)
e2 = (2, 4)
e3 = (1, 3)
e4 = (3, 4)
e5 = (2, 3)

F.add_edge(1, 2, lamb=0.85, mi=0.85, weight=5)  # moze ici umjesto F.add_edge(*e1, lamb=0.85, mi=0.85, weight=5)
F.add_edge(*e2, lamb=0.85, mi=0.56, weight=6)
F.add_edge(*e3, lamb=0.85, mi=0.34, weight=1)
F.add_edge(*e4, lamb=0.85, mi=0.76, weight=2)
F.add_edge(*e5, lamb=0.85, mi=0.34, weight=3)

pocetni = 1
krajnji = 4

G = transformation(F, 1)

# izracun A i R kad putevi nisu zadani - 9.a 8.a
dijkstraFunctionAvailability(G, pocetni, krajnji)
dijkstraFunctionReliability(G, pocetni, krajnji)

# izracun A i R kad putevi jesu zadani - 9.a 8.b
customPathAvailability(G, [1, 3, 4], [1, 2, 4])
customPathReliability(G, [1, 3, 4], [1, 2, 4])

# 9.a 8.c
print("abraham R:" + str(abraham(G, getAllPaths(G, pocetni, krajnji))))

# 9.b 8.a
averageAvailabilityDijkstra(G)
stAvailabilityDijkstra(G)

# 9.b 8.c
averageAvailabilityAbraham(G)
stAvailabilityAbraham(G)



