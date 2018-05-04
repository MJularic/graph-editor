import math


def check_node(x, y, offset, graph, scale):
    x = x - offset[0]
    y = y - offset[1]

    for node in graph.nodes_iter():
        d = (graph.node[node]["x"] * scale - x) ** 2 + (graph.node[node]["y"] * scale - y) ** 2
        if d < 36:
            return node

    return False


def check_edge(x, y, offset, graph, scale):
    x = x - offset[0]
    y = y - offset[1]

    for edge in graph.edges_iter():
        n1 = graph.node[edge[0]]
        n2 = graph.node[edge[1]]

        n1x = n1["x"] * scale
        n1y = n1["y"] * scale
        n2x = n2["x"] * scale
        n2y = n2["y"] * scale

        # circle containing the edge
        ccx = (n1x + n2x) / 2.0  # circle center x
        ccy = (n1y + n2y) / 2.0  # circle center y
        r = ((n1x - n2x) ** 2 + (n1y - n2y) ** 2) / 4.0  # squared radius

        # squared distance of the point (x, y) form the center of the circle above
        dp = (ccx - x) ** 2 + (ccy - y) ** 2

        if dp <= r:
            # magic, don't touch!
            a = n2y - n1y
            b = n1x - n2x
            c = n2x * n1y - n1x * n2y

            d = abs(a * x + b * y + c) / math.sqrt(a ** 2 + b ** 2)

            if d < 5:
                return edge

    return False
