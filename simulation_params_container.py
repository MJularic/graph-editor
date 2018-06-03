from pyglet.window import key


class SimulationParamsContainer:
    def __init__(self):
        self.selected_nodes = []
        self.selected_path1 = []
        self.selected_path2 = []
        self.start_end_node = []
        self.path1 = False
        self.path2 = False
        self.path = None
        self.scope = None
        self.choose = False
        self.time = None

    def resetSimParams(self, symbol):
        if symbol == key.N or symbol == key.E or symbol == key.M or symbol == key.D or symbol == key.I \
                or symbol == "aborted_sim_param_selection":
            self.selected_nodes = []
            self.scope = None
            self.path = None
            self.start_end_node = []
            self.selected_nodes = []
            self.selected_path1 = []
            self.selected_path2 = []
            self.time = None
        return


    def isSelectPath(self):
        if self.scope == "node_pair" and self.path == "select_path":
            return True
        return False

    def isShortestPath(self):
        if self.scope == "node_pair" and self.path == "shortest_path":
            return True
        return False

    def addNetworkElementToSimulationParams(self, element, type="edge"):
        if self.isShortestPath():
            if type == "node":
                self.addStartEndNode(element, self.selected_nodes)
        if self.isSelectPath():
            if type == "node":
                self.addSelectPathNodePair(element)
            if self.path1:
                self.appendToPath(element, self.selected_path1)
            if self.path2:
                self.appendToPath(element, self.selected_path2)


    def addStartEndNode(self, element, field):
        if len(field) == 2:
            field.pop(0)
        field.append(element)

    def addSelectPathNodePair(self, element):
        if self.choose:
            self.addStartEndNode(element, self.start_end_node)

    def appendToPath(self, element, field):
        if element not in field and element not in self.start_end_node:
            field.append(element)

""""
    def checkPath(self):
        length_1 = len(self.selected_path1)
        length_2 = len(self.selected_path2)
        primary = False
        secondary = False
        if self.start_end_node[0] != self.selected_path1[0][0] \
                or self.start_end_node[1] != self.selected_path1[length_1-1][1]:
            primary = True
        if self.start_end_node[0] != self.selected_path2[0][0] \
                or self.start_end_node[1] != self.selected_path2[length_2-1][1]:
            secondary = True

        if primary and secondary:
            return "Primary and secondary path are invalid!!!"
        if primary:
            return "Primary path is invalid!!!"
        if secondary:
            return "Secondary path is invalid!!!"
        return "OK"
"""