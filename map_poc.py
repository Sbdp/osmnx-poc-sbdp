import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import random

# Optional: Configure OSMnx to log useful info and use cache (speeds up repeated runs)
ox.settings.log_console = True
ox.settings.use_cache = True

# Define the location
place_name = "Piedmont, California, USA"

# Download the graph
# 'network_type' can be 'drive', 'walk', 'bike', 'all', etc.
print(f"Downloading map for {place_name}...")
G = ox.graph_from_place(place_name, network_type="drive")

# Plot the raw graph to verify
fig, ax = ox.plot_graph(G, node_size=0, edge_color="w", edge_linewidth=0.5)

# Calculate basic stats
stats = ox.basic_stats(G)

print(f"Number of nodes: {stats['n']}")
print(f"Number of edges: {stats['m']}")
print(f"Average street length: {stats['edge_length_avg']:.2f} meters")



# Get all nodes from the graph
nodes = list(G.nodes)

# Pick a random origin and destination
origin_node = nodes[0]              # First node in the list
destination_node = nodes[-1]        # Last node in the list

# OR pick random nodes:
# origin_node = random.choice(nodes)
# destination_node = random.choice(nodes)

print(f"Calculating route from Node {origin_node} to Node {destination_node}...")

# Calculate the shortest path using Dijkstra's algorithm (weighted by length)
route = nx.shortest_path(G, origin_node, destination_node, weight='length')

print("Route calculated successfully!")

# Plot the route
# route_color: Color of the path
# route_linewidth: Thickness of the path
fig, ax = ox.plot_graph_route(
    G, 
    route, 
    route_color="r", 
    route_linewidth=4, 
    node_size=0, 
    bgcolor="k"
)
