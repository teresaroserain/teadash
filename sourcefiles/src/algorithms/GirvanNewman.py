import networkx as nx

def edge_to_remove(G):
    dict1 = nx.edge_betweenness_centrality(G)
    list_of_tuples = sorted(dict1.items())
    #list_of_tuples.sort(key = lambda x:x[1], reverse = True)
    return list_of_tuples[0][0] # (a,b)

def girvan(G):
    c = list(G.subgraph(c) for c in nx.connected_components(G))
    l = len(c)
    print(len(c))
    while l==1:
        G.remove_edge(*edge_to_remove(G))
        c = list(G.subgraph(c) for c in nx.connected_components(G))
        d = (G.subgraph(c) for c in nx.connected_components(G))
        l = len(c)

    return c