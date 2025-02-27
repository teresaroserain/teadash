import networkx as nx
import src.algorithms.GirvanNewman as gn
import plotly.graph_objects as go
import dash_core_components as dcc
import math

def networkGraph(df_interaction, applyAlgorithm):
    networkfigs = []
    G = nx.Graph()
    G = nx.from_pandas_edgelist(df_interaction, "Source", "Target")
    print("nodes ", G.nodes())
    if G.has_node(''):
        G.remove_node('')
    if G.has_node('Test student'):
        G.remove_node('Test student')
    if G.has_node('nan'):
        G.remove_node('nan')
    
    nan_nodes = []
    for node in G.nodes():
        print(type(node))
        if isinstance(node, float):
            if math.isnan(float(node)):
                print("node null ", node)
                nan_nodes.append(node)
    G.remove_nodes_from(nan_nodes)
           
    if applyAlgorithm == True:
        c = gn.girvan(G)
        for i in c:            
            G_temp = nx.Graph()
            G_temp.add_nodes_from(i.nodes())
            G_temp.add_edges_from(i.edges())
            pos = nx.fruchterman_reingold_layout(G_temp)
            print ("edges ", nx.edges(G_temp))
            print ("nodes  ", nx.nodes(G_temp))
            fig = showNetworkGraph(G_temp, pos)
            networkfigs.append(dcc.Graph(id='graph-{}'.format(i), figure=fig))
    else: 
        pos = nx.fruchterman_reingold_layout(G)
        fig = showNetworkGraph(G, pos)
        #networkfigs.append(dcc.Graph(id='graph-{}'.format(0), figure=fig))

    return fig

def showNetworkGraph (G, pos):
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y, text= text,
        textfont=dict(color='blue', size=10),
        textposition="middle right",
        mode='markers+text',
        hoverinfo= 'text',
        marker=dict(
            color='Green',
            size=10,
            line=dict(color='lightblue', width=1)))
    
    node_adjacencies = []
    #node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        #node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    #node_trace.text = node_text
    
    layout = dict(plot_bgcolor='white',
                paper_bgcolor='white',
                height=700,
                width=1500,
                #margin=dict(t=10, b=10, l=10, r=10, pad=0),
                xaxis=dict(linecolor='black',
                            showgrid=False,
                            showticklabels=False,
                            mirror=True),
                yaxis=dict(linecolor='black',
                            showgrid=False,
                            showticklabels=False,
                            mirror=True))

    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    fig.update_layout(clickmode='event+select')
    return fig

def show_network_cypto(G, pos):
    cy = nx.cytoscape_data(G)

    # Replacing dictionary key 'value' with 'label' in the nodes list of cy
    for n in cy["elements"]["nodes"]:
        for k, v in n.items():
            v["label"] = v.pop("value")

    # Adding positions of nodes from pos
    SCALING_FACTOR = 100
    for n, p in zip(cy["elements"]["nodes"], pos.values()):
        n["position"] = {"x": int(p[0] * SCALING_FACTOR), "y": int(p[1] * SCALING_FACTOR)} 

    elements=list(cy["elements"]["nodes"]+ cy["elements"]["edges"])
    
    """ fig = cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        layout={'name': 'breadthfirst'},
        style={'width': '600px', 'height': '400px'}
    ) """
    return elements