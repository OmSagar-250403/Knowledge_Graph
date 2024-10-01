import os
import pandas as pd
import spacy
import nltk
from spacy.matcher import Matcher
import networkx as nx
import matplotlib.pyplot as plt

# Load the large English NLP model
nlp = spacy.load('en_core_web_lg')

# Set pandas display option for better visibility
pd.set_option('display.max_colwidth', 200)

# Load and process the sentences
sentences = []
files = os.listdir('../actors and movies')

# Process each file in the directory
for file in files:
    file_path = '../actors and movies/' + str(file)
    
    # Check if the file is empty
    if os.stat(file_path).st_size == 0:
        print(f"Skipping empty file: {file}")
        continue
    
    # Try reading the file as JSON, handle invalid files
    try:
        df = pd.read_json(file_path)
        sentences.append(nltk.tokenize.sent_tokenize(df['text'][0]))
    except ValueError as e:
        print(f"Error reading {file}: {e}")
        continue

# Flatten the list of sentences
sentences = sum(sentences, [])
print(sentences)

def get_entities(sent):
  #print("get_entities_2")
  ## chunk 1
  ent1 = ""
  ent2 = ""

  prv_tok_dep = ""    # dependency tag of previous token in the sentence
  prv_tok_text = ""   # previous token in the sentence

  prefix = ""
  modifier = ""

  #############################################################
  
  for tok in nlp(sent):
    ## chunk 2
    # if token is a punctuation mark then move on to the next token
    if tok.dep_ != "punct":
      # check: token is a compound word or not
      if tok.dep_ == "compound":
        prefix = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          prefix = prv_tok_text + " "+ tok.text
      
      # check: token is a modifier or not
      if tok.dep_.endswith("mod") == True:
        modifier = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          modifier = prv_tok_text + " "+ tok.text
      
      ## chunk 3
      if tok.dep_.find("subj") == True:
        ent1 = modifier +" "+ prefix + " "+ tok.text
        prefix = ""
        modifier = ""
        prv_tok_dep = ""
        prv_tok_text = ""      

      ## chunk 4
      if tok.dep_.find("obj") == True:
        ent2 = modifier +" "+ prefix +" "+ tok.text
        
      ## chunk 5  
      # update variables
      prv_tok_dep = tok.dep_
      prv_tok_text = tok.text
  #############################################################

  return [ent1.strip(), ent2.strip()]



entity_pairs = []

for i in sentences:
  entity_pairs.append(get_entities(i))
print("Entity Pairs are : \n")
print(entity_pairs)



def get_relation(sent):
  #print("get_relation")
  doc = nlp(sent)

  # Matcher class object 
  matcher = Matcher(nlp.vocab)

  #define the pattern 
  pattern = [{'DEP':'ROOT'}, 
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},  
            {'POS':'ADJ','OP':"?"}] 

  matcher.add("matching_1", [pattern])  

  matches = matcher(doc)
  k = len(matches) - 1

  span = doc[matches[k][1]:matches[k][2]] 

  return(span.text)


relations = [get_relation(i) for i in sentences]
print("The Available Relations are :\n")
print(relations)
#print("The Available Relations are :\n")
#print(pd.Series(relations).value_counts()[:50])




# extract subject
source = [i[0] for i in entity_pairs]

# extract object
target = [i[1] for i in entity_pairs]

kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})


# create a directed-graph from a dataframe
G=nx.from_pandas_edgelist(kg_df, "source", "target", 
                          edge_attr=True, create_using=nx.MultiDiGraph())


plt.figure(figsize=(30,30))

pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
plt.savefig('./KG.png')
plt.show() # display the graph in the console


query=str(input("Enter the Relation You Wanna view in the Knowledge Graph :\n"))


G=nx.from_pandas_edgelist(kg_df[kg_df['edge']==query], "source", "target", 
                          edge_attr=True, create_using=nx.MultiDiGraph())

plt.figure(figsize=(30,30))
pos = nx.spring_layout(G, k = 0.5) # k regulates the distance between nodes
nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, pos = pos)
plt.savefig('./RKG.png')
plt.show()