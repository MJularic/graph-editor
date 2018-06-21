import networkx as nx
import math

G = nx.Graph()


def printme(G):
    print(G)
    return;


G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_edge(1, 2)
G[1][2]['weight'] = 5
G.add_edge(2, 4)
G.add_edge(1, 3)
G.add_edge(2, 3)
G.add_edge(3, 4)

N = G.nodes()
E = G.edges()
printme(N)
printme(E)

P = nx.dijkstra_path(G, 1, 4)
print(P)
number_of_variables = G.number_of_nodes() + G.number_of_edges()
rows = math.floor(number_of_variables / 2)
print(rows)
Matrix = [[0 for x in range(number_of_variables - rows)] for y in range(rows)]
print(Matrix)
Matrix[0][0] = 1

print("====================")

josko = [1,2,3]
for mama in josko:
    if mama == 2:
        josko.append(4)
    print(mama)