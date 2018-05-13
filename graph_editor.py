import os
import copy

import networkx as nx
from check_node_edge import *
from image_helper_functions import *
import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet.gl import *
from parameter_input import NetworkParameterInput


class App(pyglet.window.Window):
    def __init__(self):
        super(App, self).__init__(800, 600, "Graph Editor", resizable=True)
        self.set_minimum_size(640, 480)

        self.g = nx.Graph()
        self.mode = "node"
        self.selected = None
        self.offset = [0, 0]
        self.scale = 100.0
        self.zoom_step = 0
        self.help = False
        self.drag = False
        self.box = [0, 0, 1000, 1000]
        self.history = []
        self.history_index = -1
        self.sidebar_width = 300
        self.last_action = None

        # create vertex list
        self.statusbar = pyglet.graphics.vertex_list(4,
                                                     ('v2f', (0, 0, self.width, 0, self.width, 24, 0, 24)),
                                                     ('c3B', (30, 30, 30) * 4)
                                                     )
        self.line = pyglet.graphics.vertex_list(2,
                                                ('v2f', (self.width - 200, 2, self.width - 200, 22)),
                                                ('c3B', (80, 80, 80) * 2)
                                                )

        # labels
        self.cmd_label = pyglet.text.Label("Press 'h' for help", font_name='Sans', font_size=12, x=10, y=6)

        with open("help.txt") as help_file:
            self.help_label = pyglet.text.Label(help_file.read(), multiline=True, x=50, y=self.height - 50,
                                                width=self.width - 100, height=self.height - 100, anchor_y="top",
                                                font_name="monospace", font_size=12)
        # load images
        self.node_sprite = load_images("node.png")
        self.selected_sprite = load_images("selected.png")

    def undo(self):
        if self.history_index == -1:
            self.cmd_label.text = "There is no previous history"
        else:
            change = self.history[self.history_index]

            if change[0] == "add":
                self.g.remove_node(change[1])
            elif change[0] == "add edge":
                self.g.remove_edge(*change[1])
            elif change[0] == "del":
                self.g.add_node(change[1], **change[2])

                for node, attributes in change[3].iteritems():
                    self.g.add_edge(change[1], node, **attributes)
            elif change[0] == "del edge":
                self.g.add_edge(*change[1], **change[2])
            elif change[0] == "move":
                self.g.node[change[1]] = change[2]

                for node, attributes in change[3].iteritems():
                    self.g.add_edge(change[1], node, **attributes)

            self.history_index -= 1
            self.cmd_label.text = "'{0}' operation undone".format(change[0])

    def redo(self):
        if self.history_index == len(self.history) - 1:
            self.cmd_label.text = "Already at newest change"
        else:
            self.history_index += 1
            change = self.history[self.history_index]

            if change[0] == "add":
                self.g.add_node(change[1], **change[2])
            elif change[0] == "add edge":
                self.g.add_edge(*change[1], **change[2])
            elif change[0] == "del":
                self.g.remove_node(change[1])
            elif change[0] == "del edge":
                self.g.remove_edge(*change[1])
            elif change[0] == "move":
                self.g.node[change[1]] = change[4]

                for node, attributes in change[5].iteritems():
                    self.g.add_edge(change[1], node, **attributes)

            self.cmd_label.text = "'{0}' operation redone".format(change[0])

    def on_draw(self):
        self.clear()

        ox = self.offset[0]
        oy = self.offset[1]

        if self.help:
            self.help_label.draw()
        else:
            draw_edges(self.g, self.scale, self.offset, self.selected)
            draw_nodes(self.g, self.scale, self.offset, self.selected,
                       self.selected_sprite, self.node_sprite)

            # draw borders
            pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,
                                 ('v2f', (self.box[0] * self.scale + ox, self.box[1] * self.scale + oy,
                                          self.box[2] * self.scale + ox, self.box[1] * self.scale + oy,
                                          self.box[2] * self.scale + ox, self.box[3] * self.scale + oy,
                                          self.box[0] * self.scale + ox, self.box[3] * self.scale + oy)))

            # draw statusbar
            self.statusbar.draw(pyglet.gl.GL_QUADS)
            self.line.draw(pyglet.gl.GL_LINES)

            # draw mode in the statusbar
            mode_label = pyglet.text.Label(self.mode, font_name='Sans', font_size=12, x=self.width - 190, y=6)
            mode_label.draw()

            # draw command
            self.cmd_label.draw()

            if self.mode == "node" and self.last_action == "mouse_release":
                network_param_input = NetworkParameterInput(self.g, self.selected, "node")
                network_param_input.run()

            if self.mode == "modify":
                if self.selected is not None and self.g.has_node(self.selected):
                    if self.last_action == "mouse_release":
                        network_param_input = NetworkParameterInput(self.g, self.selected, "node")
                        network_param_input.run()
                if self.selected is not None and isEdge(self.g, self.selected):
                    if self.last_action == "mouse_release":
                        network_param_input = NetworkParameterInput(self.g, self.selected, "edge")
                        network_param_input.run()

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.last_action = "mouse_press"
        node = check_node(x, y, self.offset, self.g, self.scale)
        edge = check_edge(x, y, self.offset, self.g, self.scale)
        if node is not False:
            if self.mode == "modify":
                self.selected = node
        if edge is not False:
            if self.mode == "modify":
                self.selected = edge
        if self.mode == "modify" and edge is False and node is False:
            self.selected = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.last_action = "mouse_drag"
        if buttons & mouse.RIGHT:
            self.offset[0] += dx
            self.offset[1] += dy
        elif buttons & mouse.LEFT and self.mode == "modify":
            if self.g.has_node(self.selected):
                node = self.g.node[self.selected]

                if not self.drag:
                    # add to history
                    self.history_index += 1
                    del self.history[self.history_index:len(self.history)]
                    self.history.append(["move", self.selected, copy.copy(node), self.g[self.selected]])

                    self.drag = True

                node["x"] += dx / self.scale
                node["y"] += dy / self.scale

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.last_action = "mouse_release"
        if buttons & mouse.LEFT:
            if self.mode == "node":
                node = check_node(x, y, self.offset, self.g, self.scale)
                # check if a node has not been clicked
                if node is False:
                    self.g.add_node(len(self.g), x=float(x - self.offset[0]) / self.scale,
                                    y=float(y - self.offset[1]) / self.scale)
                    self.selected = len(self.g) - 1

                    # add to history
                    self.history_index += 1
                    del self.history[self.history_index:len(self.history)]
                    self.history.append(("add", self.selected, copy.copy(self.g.node[self.selected])))
                else:
                    self.selected = node
            elif self.mode == "edge":
                node = check_node(x, y, self.offset, self.g, self.scale)
                # check if a node has been clicked
                if node is not False:
                    # if the node was already selected deselect it
                    if self.selected == node:
                        self.selected = None
                    # if no node was selected select the current one
                    elif self.selected is None:
                        self.selected = node
                    # if a different node is already selected add an edge between the two
                    # but check if there is already an edge between the two: in this case
                    # just do nothing
                    else:
                        if node not in self.g[self.selected]:
                            self.g.add_edge(self.selected, node)
                            network_param_input = NetworkParameterInput(self.g, [self.selected, node], "edge")
                            network_param_input.run()
                            # add to history
                            self.history_index += 1
                            del self.history[self.history_index:len(self.history)]
                            self.history.append(("add edge", (self.selected, node), self.g[self.selected][node]))

                        self.selected = node
            elif self.mode == "delete":
                node = check_node(x, y, self.offset, self.g, self.scale)
                # check if a node has been clicked
                if node is not False:
                    # if the node was selected unselect it
                    if self.selected == node:
                        self.selected = None

                    # add to history
                    self.history_index += 1
                    del self.history[self.history_index:len(self.history)]
                    self.history.append(("del", node, self.g.node[node], self.g[node]))

                    # actually remove the node
                    self.g.remove_node(node)

                edge = check_edge(x, y, self.offset, self.g, self.scale)
                # check if an edge has been clicked
                if edge is not False:
                    # add to history
                    self.history_index += 1
                    del self.history[self.history_index:len(self.history)]
                    self.history.append(("del edge", edge, self.g[edge[0]][edge[1]]))

                    # actually remove the edge
                    self.g.remove_edge(*edge)

        # dragging of node ended update some stuff
        if self.drag:
            # update history
            self.history[-1].append(copy.copy(self.g.node[self.selected]))
            self.history[-1].append(copy.copy(self.g[self.selected]))

            self.drag = False

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.last_action = "mouse_scroll"
        self.zoom_step += scroll_y
        self.scale = 100 * 1.2 ** self.zoom_step

    def on_key_press(self, symbol, modifiers):
        self.last_action = "key_press"
        if symbol == key.H:
            self.help = True

    def on_key_release(self, symbol, modifiers):
        self.last_action = "key_release"
        if symbol == key.N:
            self.mode = "node"
        elif symbol == key.E:
            self.mode = "edge"
        elif symbol == key.D:
            self.mode = "delete"
        elif symbol == key.M:
            self.mode = "modify"
        elif symbol == key.S:
            nx.write_graphml(self.g, "graph.graphml")
            # get info about the file
            stat = os.stat("graph.graphml")
            num_nodes = len(self.g)
            size = stat.st_size / 1000.0
            # display info
            self.cmd_label.text = "{0} nodes written to graph.graphml ({1:,.1f}k)".format(num_nodes, size)
        elif symbol == key.L:
            try:
                self.g = nx.read_graphml("graph.graphml")
                # get info about the file
                stat = os.stat("graph.graphml")
                num_nodes = len(self.g)
                size = stat.st_size / 1000.0
                # display info
                self.cmd_label.text = "{0} nodes loaded from graph.graphml ({1:,.1f}k)".format(num_nodes, size)

                # clean up
                self.selected = None
            except IOError:
                # the file was missing
                self.cmd_label.text = "File graph.graphml not found"
        elif symbol == key.H:
            self.help = False
        elif symbol == key.Q:
            self.close()
        elif symbol == key.Z:
            self.undo()
        elif symbol == key.Y:
            self.redo()
        elif symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)
        elif symbol == key.ESCAPE:
            self.selected = None

    def on_resize(self, width, height):
        self.last_action = "resize"
        super(App, self).on_resize(width, height)

        self.help_label.y = self.height - 50
        self.help_label.width = self.width - 100
        self.help_label.height = self.height - 100

        self.statusbar.vertices[2] = self.width
        self.statusbar.vertices[4] = self.width

        self.line.vertices[0] = self.width - 200
        self.line.vertices[2] = self.width - 200


if __name__ == "__main__":
    window = App()
    pyglet.app.run()
