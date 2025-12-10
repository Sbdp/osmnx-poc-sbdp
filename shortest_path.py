import osmnx as ox
import networkx as nx

def run_corrected_poc():
    # 1. SETUP
    #place = "San Francisco, California, USA"
    place = "Kolkata, West Bengal, India"
    start_point = (22.5392, 88.3700)#Park circus
    end_point   = (22.5839, 88.3434)#Howrah
    #start_point = (37.7763, -122.4328) # Alamo Square
    #end_point   = (37.7955, -122.3937) # Ferry Building

    # 2. DOWNLOAD MAP
    print(f"Downloading map for {place}...")
    G = ox.graph_from_place(place, network_type="drive")
    
    # Add travel time weights
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    # 3. GET NEAREST NODES
    orig_node = ox.nearest_nodes(G, start_point[1], start_point[0])
    dest_node = ox.nearest_nodes(G, end_point[1], end_point[0])
    
    # 4. CALCULATE PRIMARY ROUTE
    print("Calculating primary route...")
    try:
        route1 = nx.shortest_path(G, orig_node, dest_node, weight='travel_time')
    except nx.NetworkXNoPath:
        print("No route found at all.")
        return

    # 5. CALCULATE ALTERNATE ROUTE
    # Strategy: Create a temporary graph and remove the edges used in Route 1
    print("Calculating alternate route...")
    G_temp = G.copy()
    
    # Remove edges from the primary route to force a different path
    # We iterate through the list of nodes in the route (u, v)
    edges_removed = 0
    for u, v in zip(route1[:-1], route1[1:]):
        try:
            # Remove the edge connecting u and v
            # Note: In a MultiGraph, this removes all parallel edges between u and v
            if G_temp.has_edge(u, v):
                G_temp.remove_edge(u, v)
                edges_removed += 1
        except Exception:
            pass # Skip if edge already gone
            
    try:
        # Find the best path on the map where the first route is "closed"
        route2 = nx.shortest_path(G_temp, orig_node, dest_node, weight='travel_time')
        routes = [route1, route2]
        colors = ['b', 'r']
        print("Alternate route found.")
    except nx.NetworkXNoPath:
        # If removing the primary route makes the destination unreachable
        print("No alternate route possible (primary route is the only way).")
        routes = [route1]
        colors = ['b']

    # 6. VISUALIZE
    print("Plotting...")
    ox.plot_graph_routes(
        G, 
        routes, 
        route_colors=colors, 
        route_linewidth=4, 
        node_size=0,
        bgcolor='k',
        figsize=(10, 10)
    )

if __name__ == "__main__":
    run_corrected_poc()