import networkx as nx
import matplotlib.pyplot as plt
import random as rand


def makeMap(m, n, gapfreq):
    g = nx.grid_2d_graph(m, n)
    one_weights = [(1,100)]
    # - weights is a list of (weight,cumulativefrequency) pairs
    # - one_weights: all edges have cost 1
    # two_weights = [(1,50),(2,100)]
    # - two_weights: 1,2 equally likely 50-50
    # three_weights = [(1,33),(2,67),(5,100)]
    # - three_weights: 1,2,5 equally likely 33-34-33
    # four_weights = [(1,10),(4,50),(6,90),(10,100)]
    # - four_weights: 10% @ 1, 40% @ 4, 40% @ 6, 10% @ 10
    # five_weights = [(1,5),(2,10),(3,100)]
    # - five weight: 5% @ 1, 5% @ 2, 90% @ 3
    prune(g, gapfreq)
    setWeights(g, one_weights)
    return g


def setWeights(g, weights):
    # setting weights...
    # weights are [(w,cf) ... ]
    # w is the weight, cf is the cumulative frequency
    for (i, j) in nx.edges(g):
        c = rand.randint(1,100)
        w = [a for (a,b) in weights if b >= c] # drop all pairs whose cf is < c
        g.edge[i][j]['weight'] = w[0]  # take the first weight in w
    return


def draw(g):
    # just for visualization
    pos = {n: n for n in nx.nodes(g)}
    nx.draw_networkx_nodes(g, pos, node_size=20)
    edges = nx.edges(g)
    nx.draw_networkx_edges(g, pos, edgelist=edges, width=1)
    plt.axis('off')
    plt.savefig("simplegrid.png")  # save as png
    plt.show()  # display
    return


def prune(g, gapf):
    """poke random holes the __g by deleting random nodes, with frequency gapf.
       Then clean up by deleting all but the largest connected component.
        """
    # creating gaps...
    for node in nx.nodes(g):
        if rand.random() < gapf:
            g.remove_node(node)
    # deleting small connected components...
    comps = sorted(nx.connected_components(g), key=len, reverse=False)
    while len(comps) > 1:
        nodes = comps[0]
        for node in nodes:
            g.remove_node(node)
        comps.pop(0)

# dim = 40  # one side of a square map;
# gapfreq = 0.25  # how drastic to make the random gaps in the graph;
#                # use a value < 0.3; higher values cut out too much
# w = makeMap(dim, dim, gapfreq)
# draw(w)
# dir(w)
