# The Entertainment Knowledge Graph

An IR project based on Knowledge Graph Structures for movies and actors/actresses analysis. 


# Project Details

<b><u>Project Title</u></b>: The Entertainment Knowledge Graph 

<b><u>Domain of Project</u></b>:  Entertainment (Movies, television programs and celebrity content



## Project Description

This project is dedicated to the comprehensive use of knowledge graphs and semantic analysis within the entertainment domain. The primary entities include movies, TV shows, actors, and actresses, along with their associated attributes and interconnections. Our approach incorporates techniques such as entity ranking, linking, entity-based retrieval models, personalized recommendations, document filtering, and knowledge graph expansion. The knowledge graph will represent movies, TV shows, actors, genres, and the intricate relationships between them. This structured representation enhances the retrieval of valuable insights beyond what is possible with unstructured text alone.



# Algorithms/Approaches Used

1. ### Entity Recognition and Linking
Utilized Named Entity Recognition (NER) to identify key entities such as movie titles, actors, genres, and other relevant attributes.
Applied entity linking techniques to match these entities with those in our knowledge graph, ensuring consistency and accuracy in entity representation.

2. ### Knowledge Graph Construction
Built a graph database to represent entities and their relationships using libraries like NetworkX.
Defined nodes for each entity type (e.g., movie, actor, genre) and edges to capture their interrelationships, allowing for structured representation and easy traversal.

3. ### Entity-Based Retrieval Models
Implemented retrieval models that use entities as the core components to enhance search accuracy.
Focused on entity-ranking techniques to prioritize relevant entities, improving the precision of query responses.

4. ### Entity Recommendation
Developed an entity recommendation engine that suggests related movies, actors, or genres based on user preferences and existing connections in the knowledge graph.
Used collaborative filtering and content-based filtering approaches for personalized recommendations.

5. ### Document Filtering
Applied document filtering techniques to remove irrelevant or redundant information from the dataset.
Focused on identifying and retaining documents rich in entities and their attributes, which contribute to the knowledge graph.

6. ### Knowledge Graph Population and Expansion
Periodically updated and expanded the knowledge graph to incorporate new data on movies, TV shows, and actors.
Ensured that the graph evolves with emerging trends in entertainment, enhancing its informational value over time.

7. ### Semantic Search and Entity Ranking
Used semantic search to understand context and retrieve the most relevant entities and information based on user queries.
Implemented entity ranking algorithms to prioritize key entities, refining the retrieval process and enhancing user experience.



### A. Web Scraping(Actors/Actresses data)

<b><u>Associated Files</u></b>: Scraper_For_Actors.py   

This python code file is used for scraping actor data from Wikipedia and storing it.    
Scraped Data from Wikipedia by Even going through the underlying links which increased the corpus exhaustively

The Functions Used :   
<b>1. wiki_scrape(page)</b>
This Looks for a page on Wikipedia
extracts it,parses it and the underlying link and keeps on fetching data from those links. 

<b><u>For Example</u></b> for a query as wiki_scrape("Robert Downey Jr.") Made it crawl 800+ links

<b>2. wiki_page(page)</b>
This just fetches the data from the very first hit it gets on Wikipedia
the query for this function needs to be very precise

<b><u>For Example</u></b> wiki_page("The Avengers") will not fetch the movie synopsis of the MCU's Avengers but just links and names of other movies/entities with the same name or context.


### B. Knowledge Graph for Actors

<b><u>Associated Files</u></b>: Knowledge_Graph_for_Actors.py      

Based on the data crawled and collected for Actors and Movies , I created a knowledge graph to perform "Entity-Entity pair based on Relation" Query.   

The sentences were tokenized and the Entity-Relation-Entity were identified and put into the Knowledge Graph   
The knowledge graph was visualized using Networkx   

<b><u>Output</u></b>:Below is the knowledge graph representing top 250 actors along with their extracted entities (subject-object pairs) and the predicates (relation between entities).      
![](src/img/KG.png)   
The networkx library was used to create a network from this data frame. The nodes will represent the entities and the edges or connections between the nodes will represent the relations between the nodes.   
It is going to be a directed graph. In other words, the relation between any connected node pair is not two-way, it is only from one node to another. For example, “John eats pasta”
![](src/img/RKG.png)
The above figure represents a sub-knowledge graph based on the relation "starred in" for actors. 


### C. Ranked Retrieval model(Actors)

<b><u>Associated Files</u></b>: RankedRetrieval_actors.py   
Based on the Data Scraped I created a Ranked Retrieval System using tf-idf ranking.  
Since the Boolean Model only fetches complete matches, it doesn’t address the problem of the documents being partially matched. The Vector Space Model solves this problem by introducing vectors of index items each assigned with weights. The weights are ranged from positive (if matched completely or to some extent) to negative (if unmatched or completely oppositely matched) if documents are present. Term Frequency - Inverse Document Frequency (tf-idf) is one of the most popular techniques where weights are terms (e.g. words, keywords, phrases etc.) and dimensions is number of words inside corpus. 
Therefore I created a ranked retrieval based on tf-idf ranking

<b><u>Output</u></b>

1. Below is the output showing for the query "The Avengers"
![](![alt text](<src/img/Screenshot (10).png>)) 
![](![alt text](<src/img/Screenshot (11).png>))



### D. Movies dataset
 
Instead of scraping, the dataset of over 83,000 IMDb movies was directly downloaded and stored in final_dataset.csv. 
Title, Date, Run Time, Genre, Rating Score, Description, Director, Stars, VotesGross   



### E. Knowledge Graph for Movies

<b><u>Associated Files</u></b>: KnowledgeGraph_movies_recommender_system.py 

It works on the basis of final_dataset_imdb.csv.  

**NOTE** :  All the graphs would be saved as .pdf file in the code directory. One has to view the pdf file where he can zoom and every node will be visible in HD resolution.     
The above code file defines 3 different types of knowledge graph structures related to movies:   

#### 1. Movie detail graph for a single movie  

![](src/img/movie_detail_page-0001.jpg) 

The above figure shows the detailed view of a given movie name showing all its details like director, cast, release date, etc.

#### 2. Movie Comparison graph between two movies.   

1st movie : Captain america: Civil war
2nd movie : Iron Man

![](src/img/movie_similarity_page-0001.jpg)

The above figure shows the comparison between 2 input movie names on basis of genre, languages and director.

#### 3.Knowledge graph of 1000 movies. 

![](src/img/my_graph_page-0001.jpg)

The blue nodes near the edges of the graph represent genres, edges of same color represent same genre movies.   

A movie node's color is derived by the combination of its genres color. Therefore movies with similar characteristics would be of same color and in the same color.    

Properties of graph : 

a. There is homogeneity between the movies belonging to the same color. (Represented by same color.)

b. There is heterogeneity among  movies from different clusters. (Represented by different colors.)


### C. Movie Recommendation System

<b><u>Associated Files</u></b>: KnowledgeGraph_movies_recommender_system.py

Given a movie name it will return a list of top 10 similar movies along with their matching scores.   

It is based on an empirically derived ranking system which takes into account all the movie details like genres, crew,

director, writer, year, other user reviews, etc. 

**Example** : For movie - Captain America - Civil War

![](![alt text](image.png))



# References

1. Wikipedia
2. IMDB
3. networkx
4. **Research Paper** :  Knowledge Graphs: An Information Retrieval Perspective

# Thank You