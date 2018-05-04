import pyglet


def load_images(image):
    node_img = pyglet.resource.image(image)
    node_img.anchor_x = 12
    node_img.anchor_y = 12
    return pyglet.sprite.Sprite(node_img)


def draw_edges(graph, scale, offset):
    for edge in graph.edges_iter():
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (
            offset[0] + graph.node[edge[0]]["x"] * scale,
            offset[1] + graph.node[edge[0]]["y"] * scale,
            offset[0] + graph.node[edge[1]]["x"] * scale,
            offset[1] + graph.node[edge[1]]["y"] * scale)))


def draw_nodes(graph, scale, offset, selected, selected_sprite, node_sprite):
    for node in graph.nodes_iter():
        if node == selected:
            selected_sprite.position = (offset[0] + graph.node[node]["x"] * scale,
                                             offset[1] + graph.node[node]["y"] * scale)
            selected_sprite.draw()
        else:
            node_sprite.position = (offset[0] + graph.node[node]["x"] * scale,
                                         offset[1] + graph.node[node]["y"] * scale)
            node_sprite.draw()