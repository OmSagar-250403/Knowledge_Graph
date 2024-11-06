import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np

def hello(self, movie1, movie2):
    """
    Method to plot detailed KG of comparison of 2 movies.
    """
    G = nx.MultiDiGraph()
    color_map = []
    node_sizes = []
    
    # Fetch movie1 details
    with open('assets/final_dataset_imdb.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[2] == movie1:
                row[1] = row[2]
                a = row[1]
                movie1row = row
                break

    # Fetch movie2 details
    with open('assets/final_dataset_imdb.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[2] == movie2:
                row[1] = row[2]
                b = row[1]
                
                # Add nodes for each movie title with color red
                G.add_node(row[1])
                color_map.append('red')
                node_sizes.append(20000)
                
                G.add_node(movie1row[1])
                color_map.append('red')
                node_sizes.append(20000)
                
                # Add genre nodes (yellow) and connect to each movie
                genres = list(row[5].split(", "))
                for x in genres:
                    if x not in G:
                        G.add_node(x)
                        color_map.append('yellow')
                        node_sizes.append(7000)
                    G.add_edge(row[1], x)
                
                genres = list(movie1row[5].split(", "))
                for x in genres:
                    if x not in G:
                        G.add_node(x)
                        color_map.append('yellow')
                        node_sizes.append(7000)
                    G.add_edge(movie1row[1], x)
                
                # Add language nodes (blue) and connect to each movie, limiting to 5 languages
                count = 0
                for i in list(row[8].split(", ")):
                    if i not in G:
                        G.add_node(i)
                        color_map.append('#ADD8E6')
                        node_sizes.append(7000)
                    G.add_edge(row[1], i)
                    if count > 4:
                        break
                    count += 1
                
                count = 0
                for i in list(movie1row[8].split(", ")):
                    if i not in G:
                        G.add_node(i)
                        color_map.append('#ADD8E6')
                        node_sizes.append(7000)
                    G.add_edge(movie1row[1], i)
                    if count > 4:
                        break
                    count += 1
                
                # Add director nodes (green) and connect to each movie
                G.add_node(row[9])
                color_map.append('#90EE90')
                node_sizes.append(7000)
                G.add_edge(row[1], row[9])
                
                if movie1row[9] not in G:
                    G.add_node(movie1row[9])
                    color_map.append('#90EE90')
                    node_sizes.append(7000)
                G.add_edge(movie1row[1], movie1row[9])
                
                # Add production company nodes (light cyan) and connect to each movie
                G.add_node(row[11])  # Production company for movie2
                color_map.append('#E0FFFF')  # Light Cyan
                node_sizes.append(7000)
                G.add_edge(row[1], row[11])  # Edge from movie2 to its production company
                
                if movie1row[11] not in G:
                    G.add_node(movie1row[11])  # Production company for movie1
                    color_map.append('#E0FFFF')  # Light Cyan
                    node_sizes.append(7000)
                G.add_edge(movie1row[1], movie1row[11])  # Edge from movie1 to its production company

                break

    # Plotting the graph
    plt.figure(figsize=(35, 35))
    pos = nx.planar_layout(G)
    pos[a] = np.array([1, 0])
    pos[b] = np.array([-1, 0])
    nx.draw(G, with_labels=True, node_color=color_map, node_size=node_sizes, edge_cmap=plt.cm.Blues, font_size=16, pos=pos)
    
    plt.savefig("movie_similarity.pdf")
    print("\nPlease Check movie_similarity.pdf in the current code directory\n")
