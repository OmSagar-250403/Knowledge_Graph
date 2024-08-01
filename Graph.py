import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer

load_dotenv()  # Load the.env file

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

"""print("neo4j_uri : ", NEO4J_URI)
print("neo4j_username : ", NEO4J_USERNAME)
print("neo4j_password : ", NEO4J_PASSWORD)"""


graph=Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
)

#print(graph)

groq_api_key=" "
llm=ChatGroq(groq_api_key=os.getenv('GROQ_API_KEY'),model_name="Gemma-7b-It")
#print(llm)


text="""
Elon Reeve Musk (born June 28, 1971) is a businessman and investor known for his key roles in space
company SpaceX and automotive company Tesla, Inc. Other involvements include ownership of X Corp.,
formerly Twitter, and his role in the founding of The Boring Company, xAI, Neuralink and OpenAI.
He is one of the wealthiest people in the world; as of July 2024, Forbes estimates his net worth to be
US$221 billion.Musk was born in Pretoria to Maye and engineer Errol Musk, and briefly attended
the University of Pretoria before immigrating to Canada at age 18, acquiring citizenship through
his Canadian-born mother. Two years later, he matriculated at Queen's University at Kingston in Canada.
Musk later transferred to the University of Pennsylvania and received bachelor's degrees in economics
 and physics. He moved to California in 1995 to attend Stanford University, but dropped out after
  two days and, with his brother Kimbal, co-founded online city guide software company Zip2.
"""
 

documents=[Document(page_content=text)]
#print(documents)

llm_transformer=LLMGraphTransformer(llm=llm)
graph_documents=llm_transformer.convert_to_graph_documents(documents)
