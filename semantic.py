import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load product data
product_data = pd.read_csv('products.csv')

# Load node embeddings
embeddings = []
with open('embeddings.txt', 'r') as f:
    for line in f:
        embeddings.append(np.array([float(x) for x in line.strip().split()]))
embeddings = np.array(embeddings)

# Print lengths to diagnose the issue
print(f"Number of products: {len(product_data)}")
print(f"Number of embeddings: {len(embeddings)}")

# Assuming partial alignment manually or using heuristics
known_products = [
    {"title": "Floral Print Summer Dress", "embedding": embeddings[0]},
    {"title": "Casual Striped Summer Dress", "embedding": embeddings[1]},
    # Add more known mappings here
]

# Create a mapping from titles to embeddings
title_to_embedding = {product['title']: product['embedding'] for product in known_products}

# Add embeddings to the product data where titles match
product_data['embedding'] = product_data['title'].map(title_to_embedding)

# Handle missing embeddings by assigning an average embedding
average_embedding = np.mean(embeddings, axis=0)
product_data['embedding'].fillna(value=list(average_embedding), inplace=True)

# Load pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_query_embedding(query):
    # Encode the query using the pre-trained sentence transformer
    query_embedding = model.encode([query])
    return query_embedding

def semantic_search(query, top_k=5):
    query_embedding = get_query_embedding(query)
    
    # Extract embeddings from the DataFrame
    product_embeddings = np.stack(product_data['embedding'].values)
    
    # Calculate cosine similarity between the query embedding and product embeddings
    similarities = cosine_similarity(query_embedding, product_embeddings)
    
    # Get the top_k most similar products
    top_k_indices = similarities[0].argsort()[-top_k:][::-1]
    
    # Collect results
    results = product_data.iloc[top_k_indices].copy()
    results['similarity_score'] = similarities[0][top_k_indices]
    
    return results

# Example usage
query = "summer dresses"
top_k_results = semantic_search(query, top_k=5)

# Display the results
for index, row in top_k_results.iterrows():
    print(f"Title: {row['title']}")
    print(f"Price: {row['price']}")
    print(f"Product Type: {row['product_type']}")
    print(f"Tags: {row['tags']}")
    print(f"Similarity Score: {row['similarity_score']}")
    print("-" * 50)
