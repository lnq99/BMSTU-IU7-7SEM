import networkx as nx
import matplotlib.pyplot as plt
from netgraph import Graph


def adjacency_matrix_to_edges(mat):
    edges = []
    nrows = len(mat)
    ncols = len(mat[0])
    for i in range(nrows):
        for j in range(ncols):
            val = mat[i][j]
            if val:
                edges.append([i + 1, j + 1, val])
    return edges


g = nx.DiGraph()


def draw_graph(weighted_edges, axs):
    g.clear()
    g.add_weighted_edges_from(weighted_edges)
    labels = nx.get_edge_attributes(g, 'weight')
    # pos = nx.circular_layout(g)
    # nx.draw(g, pos, with_labels=True, connectionstyle='arc3,rad=0.05')
    # nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, label_pos=0.2)

    Graph(g, node_labels=True, edge_labels=labels,
          ax=axs,
          node_color='g', node_size=8,
          node_label_fontdict=dict(size=10, weight='bold'),
          edge_label_fontdict=dict(size=8, weight='bold'),
          edge_label_position=0.2, edge_layout='curved', edge_width=1,
          edge_alpha=1, arrows=True, scale=(
              4, 4))
