import streamlit as st
from PIL import Image
import csv
from src.KnowledgeGraph_movies_recommender_system import *  # Fixed import syntax

# Set page configuration
st.set_page_config(
    page_title="Movie Knowledge Graph",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🎬 Movie Knowledge Graph")
    st.markdown("Welcome to the Movie Knowledge Graph! Explore movie similarities, details, and recommendations.")

    option = st.selectbox(
        "Select an option:",
        ["Movie Similarity", "Knowledge Graph of Movies", "Movie Details", "Movie Recommendations"]
    )

    if option == "Movie Similarity":
        st.subheader("Compare Two Movies")
        col1, col2 = st.columns(2)

        with col1:
            movie1 = st.text_input("Enter Movie 1:")

        with col2:
            movie2 = st.text_input("Enter Movie 2:")

        if st.button("Compare Movies"):
            try:
                KG = KnowledgeGraph()
                KG.movie_similarity(movie1, movie2)
                st.success("Similarity graph generated. Check the PDF.")

                with open("movie_similarity.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button("Download Similarity Graph", PDFbyte, "movie_similarity.pdf", mime="application/pdf")

            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Knowledge Graph of Movies":
        st.subheader("Generate Knowledge Graph of Movies")
        language = st.text_input("Enter Language (e.g., 'Hindi'):", value="Hindi")
        year = st.text_input("Enter Year (e.g., '2020'):", value="2020")

        if st.button("Generate Graph"):
            try:
                KG = KnowledgeGraph()
                KG.similar_movies(language, year)
                st.success("Knowledge graph generated. Check the PDF.")

                with open("my_graph_zoomed.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button("Download Knowledge Graph", PDFbyte, "my_graph_zoomed.pdf", mime="application/pdf")

            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Movie Details":
        st.subheader("Get Movie Details")
        movie_name = st.text_input("Enter Movie Name:")

        if st.button("Show Details"):
            try:
                KG = KnowledgeGraph()
                KG.movie_details(movie_name)
                st.success("Movie details graph generated. Check the PDF.")

                with open("movie_detail.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button("Download Movie Details Graph", PDFbyte, "movie_detail.pdf", mime="application/pdf")

            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Movie Recommendations":
        st.subheader("Get Movie Recommendations")
        movie1 = st.text_input("Enter Movie Name for Recommendations:")

        if st.button("Get Recommendations"):
            recommend_movies(movie1)


def recommend_movies(movie1):
    try:
        with open('assets/final_dataset_imdb.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            movie1row = None
            for row in csv_reader:
                if row[2] == movie1:
                    movie1row = row
                    break

        if not movie1row:
            st.error(f"Movie '{movie1}' not found in the dataset.")
            return

        best_movies = []

        with open('assets/final_dataset_imdb.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # skip header
            for row in csv_reader:
                if row[1] == movie1row[1] or int(row[15]) < 5000 or int(row[3]) < 1950:
                    continue

                score = 0

                if movie1row[3] == row[3]:
                    score += 2

                genres1 = set(movie1row[5].split(", "))
                genres2 = set(row[5].split(", "))
                score += 7 * len(genres1.intersection(genres2))
                score -= len(genres1.union(genres2)) - len(genres1.intersection(genres2))

                if row[7] == movie1row[7]:
                    score += 1

                lang1 = set(movie1row[8].split(", "))
                lang2 = set(row[8].split(", "))
                score += len(lang1.intersection(lang2))

                if row[9] == movie1row[9]:
                    score += 3
                if row[10] == movie1row[10]:
                    score += 3

                actors1 = set(movie1row[12].split(", "))
                actors2 = set(row[12].split(", "))
                score += 4 * len(actors1.intersection(actors2))

                if row[11] == movie1row[11]:
                    score += 3

                score += 0.00000000000001 * float(row[15])

                if len(best_movies) < 10 or score > best_movies[-1][0]:
                    if len(best_movies) >= 10:
                        best_movies.pop(-1)
                    best_movies.append((score, row[2]))

                best_movies.sort(reverse=True)

        st.write(f"### Top Recommended Movies for '{movie1}':")
        for rank, (score, title) in enumerate(best_movies, start=1):
            st.write(f"**Rank {rank}:** {title} — Score: {round(score, 2)}")

    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
