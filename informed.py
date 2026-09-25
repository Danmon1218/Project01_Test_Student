import math
import heapq

def haversine(coord1, coord2):
    lat1, lon1 = coord1["lat"], coord1["lon"]  
    lat2, lon2 = coord2["lat"], coord2["lon"]   
    R = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R*c

def greedy_best_first(graph, start, goal):
    """
    Greedy Best-First Search
    Returns: {"path": list, "expanded": list, "distance": float}
    """
    nodes_coords = graph.get("locations", {})
    if start not in nodes_coords or goal not in nodes_coords:
        return {"path": None, "expanded": [], "distance": 0.0}
        
    goal_coord = nodes_coords[goal]
    
    pq = []
    # Entry: (heuristic, counter, node, path, path_cost)
    counter = 0
    h_start = haversine(nodes_coords[start], goal_coord)
    heapq.heappush(pq, (h_start, counter, start, [start], 0.0))
    
    visited = set()
    expanded = []
    
    while pq:
        _, _, node, path, cost = heapq.heappop(pq)
        
        if node in visited:
            continue
            
        visited.add(node)
        expanded.append(node)
        
        if node == goal:
            return {"path": path, "expanded": expanded, "distance": round(cost, 2)}
            

        nearby = graph.get(node, {})
        neighbors = sorted(nearby)
        for n_name in neighbors:
            if n_name not in visited:
                counter += 1
                h_val = haversine(nodes_coords[n_name], goal_coord)
                heapq.heappush(pq, (h_val, counter, n_name, path + [n_name], cost + nearby.get(n_name)))
                
    return {"path": None, "expanded": expanded, "distance": 0.0}

def a_star(graph, start, goal):
    """
    A* Search
    Returns: {"path": list, "expanded": list, "distance": float}
    """
    nodes_coords = graph.get("locations", {})
    if start not in nodes_coords or goal not in nodes_coords:
        return {"path": None, "expanded": [], "distance": 0.0}
        
    goal_coord = nodes_coords[goal]
    
    pq = []
    # Entry: (f_cost, counter, node, path, g_cost)
    counter = 0
    h_start = haversine(nodes_coords[start], goal_coord)
    heapq.heappush(pq, (h_start, counter, start, [start], 0.0))
    
    visited = set()
    expanded = []
    
    while pq:
        f_cost, _, node, path, g_cost = heapq.heappop(pq)
        
        if node in visited:
            continue
            
        visited.add(node)
        expanded.append(node)
        
        if node == goal:
            return {"path": path, "expanded": expanded, "distance": round(g_cost, 2)}
            
        nearby = graph.get(node, {})
        neighbors = sorted(nearby)
        for n_name in neighbors:
            if n_name not in visited:
                counter += 1
                g_new = g_cost + nearby.get(n_name)
                h_val = haversine(nodes_coords[n_name], goal_coord)
                f_new = g_new + h_val
                heapq.heappush(pq, (f_new, counter, n_name, path + [n_name], g_new))
                
    return {"path": None, "expanded": expanded, "distance": 0.0}
