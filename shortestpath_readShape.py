import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import copy
from datetime import datetime
start_time = datetime.now()

G = nx.read_shp('neac/sea_04_shape.shp',simplify=True)

print(G.nodes(data=True)[0:10])
print(G.edges(data=True)[0:10])
print(G.edges(data=True)[0][2]['distance'])
# NODES in G have no index, only coordinates and attributes (data=True)
# edge indicates coordinates or X Y  (distance)


# ---------------------give index to nodes--------
w_G=nx.Graph()
lat_lon_to_index = {}
for i, node in enumerate(G.nodes()): #adds nodes with index 0 till n nodes to the network.
    # print(node)
    w_G.add_node(i,lat_ton = node)
    lat_lon_to_index[node] = i

# NODES in w_G have index, use that index to build links

print(lat_lon_to_index)
print(lat_lon_to_index[(-172.0, -81.0)])
# lat_lon_to_index is a list where coordinates are index,
# by doing that: add_edge below can convert coordinates to index

# ---------------------build network--------
from geopy.distance import lonlat, distance
for edge in G.edges(data=True):
    print([lat_lon_to_index[edge[0]],lat_lon_to_index[edge[1]]]) # node index
    print(edge[0]) # edge[0] = coordinates

    dis_km = distance(lonlat(*edge[0]), lonlat(*edge[1])).km # look up node index by coordinates
    w_G.add_edge(lat_lon_to_index[edge[0]], lat_lon_to_index[edge[1]],distance=dis_km)
    # distance function uses (latitude, longtitue), shape uses (long, lat), needs conversion

    # w_G.add_edge(lat_lon_to_index[edge[0]], lat_lon_to_index[edge[1]], distance=edge[2]['cost'],id=edge[2]['edge_id'] )

print(w_G.nodes()[0:10])
print(w_G.edges(data = True)[0:10])
# (data=True) shows the attributes of the links/nodes

# ---------------------shortest path--------------------------

def single_dijkstra(graph, start, edge_weight_name):
    """Compute shortest distance between each pair of nodes in a graph.  Return a dictionary keyed on node pairs (tuples)."""
    distances = []
    for x in start:
        try:
            value_set = nx.single_source_dijkstra_path_length(graph, source=x,  weight=edge_weight_name)
        except nx.NetworkXNoPath:
            pass
        for key in value_set:

            distances.append([x,key,value_set[key]])
    return distances

node_pairs_shortest_paths = single_dijkstra(w_G, w_G.nodes()[0:100], 'distance')
output = pd.DataFrame(node_pairs_shortest_paths,columns=['start','end','distance'])

# --------------------outputs-----------------------------------------

output.to_csv('output_0927.csv')

node_list=[]
for key in lat_lon_to_index:
    node_list.append({'index':lat_lon_to_index[key],'coordinates':key })

a = pd.DataFrame(node_list, columns=['index','coordinates'])
a.to_csv('nodes.csv')
