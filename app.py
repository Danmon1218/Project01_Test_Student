import os
import json
from flask import Flask, render_template, jsonify, request
from informed import greedy_best_first, a_star
from uniformed import dfs, bfs, ucs, ids

app = Flask(__name__)

MAP_DATA_FILE = "map_data.json"


def load_map_data():
    """Load graph and location data from map_data.json if available."""
    if os.path.exists(MAP_DATA_FILE):
        try:
            with open(MAP_DATA_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {MAP_DATA_FILE}: {e}")
    return {
        "region": "State / Metro Area",
        "total_cities": 0,
        "total_edges": 0,
        "locations": {},
        "graph": {}
    }


@app.route("/")
def index():
    """Renders the main deployment webpage."""
    return render_template("index.html")


@app.route("/api/map", methods=["GET"])
def get_map():
    """Returns map locations and graph connections."""
    data = load_map_data()
    return jsonify(data)


@app.route("/api/search", methods=["POST"])
def search():
    """
    Search endpoint placeholder for deployment testing.
    """
    payload = request.get_json() or {}
    start = payload.get("start", "")
    goal = payload.get("goal", "")
    algorithm = payload.get("algorithm", "")


    #load the map data 
    data = load_map_data()
    graph = data["graph"]
    loc = data["locations"]




    cost = 0
    nodes_expanded = 0 

    if algorithm == "bfs":
        # print(graph.get("Bakersfield, CA").get("Barstow, CA"))
        # print(graph.get("graph"))
        # testing = "Bakersfield, CA"
        # print(graph.get(testing , {}))
        results = bfs(graph,start, goal)
    elif algorithm == "dfs":
        results = dfs(graph,start, goal)
    elif algorithm == "ucs":
        results = ucs(graph,start,goal)
    elif algorithm == "ids":
        results = ids(graph,start,goal)
    elif algorithm == "greedy":

        data = load_map_data()
        graph = dict(data["graph"])
        graph["locations"] = data["locations"]
        results = greedy_best_first(graph,start,goal)
    elif algorithm == "astar":
        data = load_map_data()
        graph = dict(data["graph"])
        graph["locations"] = data["locations"]
        results = a_star(graph,start,goal)
        


    return jsonify({
        "status": "ready",
        "message": f"Deployment server active. Request received for algorithm '{algorithm}' from '{start}' to '{goal}'.",
        "path": results["path"],
        "cost": results["distance"],
        "nodes_expanded": results["expanded"]
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 1218))
    app.run(host="0.0.0.0", port=port, debug=True)
