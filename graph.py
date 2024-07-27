"""import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

def create_graph_from_csv(df):
    # Initialize a directed graph
    G = nx.DiGraph()

    # Add nodes and edges based on CSV data
    for _, row in df.iterrows():
        product_title = row['title']
        product_url = row['product_url']
        product_type = row['product_type']
        tags = row['tags'].split(', ')
        for tag in tags:
            G.add_node(product_title, type='product')
            G.add_node(tag.strip(), type='tag')
            G.add_node(product_type, type='type')
            G.add_edge(product_title, tag.strip())
            G.add_edge(tag.strip(), product_type)

    return G

def plot_graph(G, title, ax):
    pos = nx.spring_layout(G)  # Positions for all nodes
    node_labels = {node: node for node in G.nodes()}
    nx.draw_networkx(G, pos, labels=node_labels, with_labels=True, node_color='skyblue', node_size=1500, font_size=10, font_color='black', edge_color='gray', linewidths=0.5, arrows=True, ax=ax)
    ax.set_title(title)
    ax.axis('off')

if __name__ == "__main__":
    csv_file = "products.csv"  # Replace with your actual CSV file path
    df = pd.read_csv(csv_file)  # Read data from CSV file
    
    # Create graphs
    graph_one_product = create_graph_from_csv(df.head(1))  # First instance
    full_graph = create_graph_from_csv(df)  # Full CSV data

    # Plot both graphs together
    fig, axs = plt.subplots(1, 2, figsize=(24, 12))  # Two subplots side by side

    plot_graph(graph_one_product, 'Graph for First Product', axs[0])
    plot_graph(full_graph, 'Full Product Tags and Types Graph', axs[1])

    # Save the figure
    fig.savefig('product_graphs.png')
    
    plt.show()"""


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv('products.csv')

# Create a single graph from one instance
single_graph = nx.Graph()
product_node = df.iloc[0]['title']
single_graph.add_node(product_node)

properties = {
    'price': df.iloc[0]['price'],
    'image_url': df.iloc[0]['image_url'],
    'product_url': df.iloc[0]['product_url'],
    'product_type': df.iloc[0]['product_type'],
    'tags': df.iloc[0]['tags']
}
for property_name, property_value in properties.items():
    property_node = f"{product_node}_{property_name}"
    single_graph.add_node(property_node)
    single_graph.add_edge(product_node, property_node, label=property_name)

# Create the full graph
full_graph = nx.Graph()
for index, row in df.iterrows():
    product_node = row['title']
    full_graph.add_node(product_node)

    properties = {
        'price': row['price'],
        'image_url': row['image_url'],
        'product_url': row['product_url'],
        'product_type': row['product_type'],
        'tags': row['tags']
    }
    for property_name, property_value in properties.items():
        property_node = f"{product_node}_{property_name}"
        full_graph.add_node(property_node)
        full_graph.add_edge(product_node, property_node, label=property_name)

    similar_products = df[df['tags'] == row['tags']]
    for similar_product in similar_products['title']:
        if similar_product!= product_node:
            full_graph.add_edge(product_node, similar_product, label='similar_tags')

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))

# Draw the single graph
pos = nx.spring_layout(single_graph)
nx.draw(single_graph, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', linewidths=1, font_size=12, ax=ax1)
ax1.set_title("Single Graph")

# Draw the full graph
pos = nx.spring_layout(full_graph)
nx.draw(full_graph, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='black', linewidths=1, font_size=12, ax=ax2)
ax2.set_title("Full Graph")

# Save the figure to a PNG file
plt.savefig('graphs.png', bbox_inches='tight')

plt.show()