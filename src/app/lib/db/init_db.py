from app.lib.db.client import ArangoClient

def init_db():
    client = ArangoClient()
    db = client.get_db()
    
    # Define Graph Name
    graph_name = "AdsGraph"
    
    # 1. Create Graph if not exists
    if not db.has_graph(graph_name):
        graph = db.create_graph(graph_name)
        print(f"Created Graph: {graph_name}")
    else:
        graph = db.graph(graph_name)

    # 2. Define Vertex Collections
    vertices = [
        "Customers",
        "Campaigns", 
        "AdGroups", 
        "Ads", 
        "Assets", 
        "Keywords",
        "UserCredentials", # Auth
        "DailyStats"       # Perf Data
    ]
    
    for v in vertices:
        if not graph.has_vertex_collection(v):
            graph.create_vertex_collection(v)
            print(f"Created Vertex Collection: {v}")

    # 3. Define Edge Definitions
    # (Relation Name, [From Collections], [To Collections])
    edges = [
        ("account_campaign", ["Customers"], ["Campaigns"]),
        ("campaign_adgroup", ["Campaigns"], ["AdGroups"]),
        ("adgroup_ad", ["AdGroups"], ["Ads"]),
        ("adgroup_keyword", ["AdGroups"], ["Keywords"]),
        ("ad_asset", ["Ads"], ["Assets"])
    ]
    
    for edge_name, from_cols, to_cols in edges:
        if not graph.has_edge_definition(edge_name):
            graph.create_edge_definition(
                edge_collection=edge_name,
                from_vertex_collections=from_cols,
                to_vertex_collections=to_cols
            )
            print(f"Created Edge Definition: {edge_name}")

    # 4. Create Indexes
    # Stats Index (Persistent on entity_id, date)
    if db.has_collection("DailyStats"):
        stats = db.collection("DailyStats")
        stats.add_persistent_index(fields=["entity_id", "date"], name="idx_stats_entity_date")
        print("Created Index: idx_stats_entity_date")

    print("Database Initialization Complete.")

if __name__ == "__main__":
    init_db()
