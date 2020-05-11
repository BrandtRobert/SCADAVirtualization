import networkx as nx


class ControlGraph:

    def __init__(self, graph_file="./controlgraph/coloradoGasModel.graph"):
        self.graph: nx.DiGraph = nx.DiGraph(nx.read_gpickle(graph_file))

    def get_predecessors(self, node: str):
        return list(self.graph.predecessors(node))

    def get_leaf_nodes(self):
        return [
            x for x in self.graph.nodes()
            if self.graph.out_degree(x) < 2
        ]


def iterate_predecessors(leaves, control_graph):
    print(leaves)
    predecessors = []
    for l in leaves:
        if g.get_predecessors(l)[0] == 'cheyenne':
            continue
        predecessors = predecessors + g.get_predecessors(l)
    if len(predecessors) == 0:
        return
    iterate_predecessors(predecessors, control_graph)


if __name__ == "__main__":
    g = ControlGraph()
    # print(g.get_leaf_nodes())
    # starting_leaves = ['ds_trindad', 'ds_springfield']
    # iterate_predecessors(starting_leaves, g)
    print(g.graph.nodes)
    # for n in g.graph.nodes():
    #     print(n)
    #     print(g.graph.out_degree(n))
    #     print(g.graph.in_degree(n))

# if __name__ == "__main__":
#     graph = nx.DiGraph()
#     # Cheyenne and Children
#     graph.add_edge("cheyenne", "compressor_fort_collins")
#     graph.add_edge("cheyenne", "compressor_fort_morgan")
#
#     # Fort Morgan and Children
#     graph.add_edge("compressor_fort_morgan", "pp_fort_morgan")
#     graph.add_edge("compressor_fort_morgan", "compressor_longmont")
#     graph.add_edge("compressor_fort_morgan", "compressor_denver_watkins")
#
#     # Fort Collins and Children
#     graph.add_edge("compressor_fort_collins", "pp_fort_collins")
#     graph.add_edge("compressor_fort_collins", "compressor_longmont")
#
#     # Longmont and Children
#     graph.add_edge("compressor_longmont", "compressor_denver_watkins")
#     graph.add_edge("compressor_longmont", "compressor_cheyenne_wells")
#     graph.add_edge("compressor_longmont", "ds_longmont")
#
#     # Denver and Children
#     graph.add_edge("compressor_denver_watkins", "pp_denver")
#     graph.add_edge("compressor_denver_watkins", "compressor_colorado_springs")
#
#     # Cheyenne Wells and Children
#     graph.add_edge("compressor_cheyenne_wells", "pp_cheyenne_wells")
#     graph.add_edge("compressor_cheyenne_wells", "compressor_springfield")
#     graph.add_edge("compressor_cheyenne_wells", "compressor_colorado_springs")
#
#     # Colorado Springs and Children
#     graph.add_edge("compressor_colorado_springs", "pp_colorado_springs")
#     graph.add_edge("compressor_colorado_springs", "ds_trindad")
#
#     # Springfield and Children
#     graph.add_edge("compressor_springfield", "ds_springfield")
#
#     # nx.write_edgelist(graph, "coloradoGasModel.graph")
#     # print(list(graph.predecessors("cheyenne")))
#     nx.write_gpickle(graph, "coloradoGasModel.graph")
