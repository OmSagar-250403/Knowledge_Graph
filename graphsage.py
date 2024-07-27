import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric
from torch_geometric.nn import SAGEConv
from torch_geometric.loader import NeighborLoader
from torch_geometric.utils import to_undirected
import pandas as pd
import numpy as np
from graph import full_graph

# Load the graph data from the previous code
graph_data = full_graph

# Load product data
product_data = pd.read_csv('products.csv')

# Ensure product_data has a unique identifier column named 'product_id'
product_ids = product_data['index'].values  # Changed 'product_id' to 'index' if 'index' is used as the identifier

# Get the node indices
node_indices = {node: i for i, node in enumerate(graph_data.nodes())}

# Convert the edge indices to integers
edges = [(node_indices[u], node_indices[v]) for u, v in graph_data.edges()]

# Convert the edge indices to a PyTorch tensor
edges_tensor = torch.tensor(np.array(edges).T, dtype=torch.long)

# Number of nodes
num_nodes = len(node_indices)

# Use identity features if no node features are available
x = torch.eye(num_nodes)

# Create a PyTorch Geometric data object
data = torch_geometric.data.Data(x=x, edge_index=edges_tensor)

# Convert edges to undirected
data.edge_index = to_undirected(data.edge_index)

# Create a GraphSAGE model
class SAGE(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(SAGE, self).__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        return x

# Initialize the model with appropriate input size
model = SAGE(in_channels=x.size(1), hidden_channels=128, out_channels=128)

# Create a neighbor sampler
sampler = NeighborLoader(data, num_neighbors=[10, 10], batch_size=128, shuffle=True)

# Train the model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Dummy labels (assuming a binary classification for the sake of the example)
data.y = torch.randint(0, 2, (num_nodes,), dtype=torch.long)

for epoch in range(4):
    total_loss = 0
    for batch in sampler:
        batch = batch.to(device)
        optimizer.zero_grad()
        out = model(batch.x, batch.edge_index)
        loss = criterion(out, batch.y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f'Epoch {epoch+1}, Loss: {total_loss / len(sampler)}')

# Get the node embeddings
model.eval()
with torch.no_grad():
    node_embeddings = model(data.x.to(device), data.edge_index.to(device))

# Save the node embeddings to a file along with their corresponding product IDs
with open('embeddings_with_ids.txt', 'w') as f:
    for product_id, embedding in zip(product_ids, node_embeddings.cpu().numpy()):
        embedding_str = ' '.join(map(str, embedding))
        f.write(f'{product_id}\t{embedding_str}\n')

print("Embeddings have been saved with product IDs.")
