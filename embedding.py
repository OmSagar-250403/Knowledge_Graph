import networkx as nx
from node2vec import Node2Vec

def generate_node2vec_embeddings(graph, dimensions=64, walk_length=30, num_walks=200, workers=4):
    node2vec = Node2Vec(graph, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=workers)
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    return model

if __name__ == "__main__":
    import graph  # Import the graph creation module
    import pandas as pd
    
    csv_file = "products.csv"
    df = pd.read_csv(csv_file)
    full_graph = graph.create_graph_from_csv(df)
    
    model = generate_node2vec_embeddings(full_graph)
    model.wv.save_word2vec_format("node2vec_embeddings.txt")
