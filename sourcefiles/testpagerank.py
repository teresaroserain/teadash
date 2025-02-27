from src.utils.utils import init_graph
import os


def PageRank_one_iter(graph, d):
    node_list = graph.nodes
    for node in node_list:
        node.update_pagerank(d, len(graph.nodes))
    graph.normalize_pagerank()
    # print(graph.get_pagerank_list())
    # print()


def PageRank(graph, d, iteration=100):
    k = 1
    while k < iteration:
    #for i in range(iteration):
        PageRank_one_iter(graph, d)
        k+=1


if __name__ == '__main__':

    iteration = 100
    damping_factor = 0.15

    graph = init_graph(os.path.join(os.path.dirname(__file__) +'/Datasets/graph_4.txt'))

    PageRank(iteration, graph, damping_factor)
    print(graph.get_pagerank_list())