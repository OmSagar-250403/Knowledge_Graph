# Knowledge Graph-Based Movie Recommendation System

Welcome to the Knowledge Graph-Based Movie Recommendation System! This project leverages knowledge graphs and network analysis to explore movies' metadata, visualize connections between movies, and recommend similar movies based on various attributes.

# Table of Contents

Project Overview
Features
Requirements
Installation
Usage
1. Similar Movies Knowledge Graph
2. Movie Details Knowledge Graph
3. Movie Similarity Comparison
4. Movie Recommendation System
Sample Outputs
Project Structure
Contributing
License


# Project Overview
This project builds a knowledge graph of movies based on their metadata, such as genres, language, director, actors, and production company. By visualizing the relationships between movies and recommending similar films based on common characteristics, this system provides insights into movie patterns and helps users find films they may enjoy.

# Features
Graph-Based Movie Visualization: Explore movies through a visual knowledge graph that highlights relationships based on genres, languages, actors, and more.
Movie Comparison: Visually compare two movies by displaying their shared and unique attributes.
Recommendation System: Retrieve similar movies based on metadata, with a scoring system that considers genre, language, actors, director, and production company.

# Requirements
To run this project, ensure you have the following libraries installed:

Python 3.x
NetworkX
Matplotlib
NumPy

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
