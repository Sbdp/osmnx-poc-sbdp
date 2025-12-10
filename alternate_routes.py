import osmnx as ox
import networkx as nx
from itertools import islice

def run_extended_poc():
    # 1. SETUP: Define locations (Lat, Lon)
    place = "San Francisco, California, USA"
    
    # Start: Alamo Square
    start_point = (37.7763, -122.4328) 
    # End: Ferry Building
    end_point   = (37.7955, -122.3937) 

    # 2. DOWNLOAD MAP
    print(f"Downloading map for {place}...")
    G = ox.graph_from_place(place, network_type="drive")
    
    # Add travel time weights (optional but recommended for driving)
    '''G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)'''

    # 3. GET NEAREST NODES
    # ox.nearest_nodes(G, X=Longitude, Y=Latitude)
    orig_node = ox.nearest_nodes(G, start_point[1], start_point[0])
    dest_node = ox.nearest_nodes(G, end_point[1], end_point[0])
    
    # 4. CALCULATE ROUTES (Top 2)
    print("Calculating primary and alternate routes...")
    
    try:
        route1 = nx.shortest_path(G, orig_node, dest_node, weight='travel_time')
        print("Primary route calculated successfully!")
    except nx.NetworkXNoPath:
        print("No path is possible between these points!")
        return

    '''try:
        # returns a generator of paths from shortest to longest
        path_generator = nx.shortest_simple_paths(G, orig_node, dest_node, weight='travel_time')
        
        # Take the top 2
        routes = list(islice(path_generator, 2))
        
        if not routes:
            print("No routes found.")
            return

        print(f"Found {len(routes)} path(s).")'''
        
    # 5. VISUALIZE
    # Colors: Blue (Primary), Red (Alternate)
    # Note: If only 1 route exists, we slice the color list to match
    colors = ['b', 'r'][:len(route1)]
        
    ox.plot_graph_routes(
        G, 
        route1, 
        route_colors=colors, 
        route_linewidth=5, 
        node_size=0,
        figsize=(12, 12)
    )
        
    '''except nx.NetworkXNoPath:
        print("No path is possible between these points!")'''

if __name__ == "__main__":
    run_extended_poc()
