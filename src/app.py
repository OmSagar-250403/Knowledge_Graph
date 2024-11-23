import streamlit as st
from PIL import Image
import csv
from KnowledgeGraph_movies_recommender_system import KnowledgeGraph  # Import the class

# Set page configuration
st.set_page_config(
    page_title="Movie Knowledge Graph",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add a logo or header image (optional)
# st.image("logo_url", width=100)  # Uncomment and replace with your logo URL

def main():
    st.title("🎬 Movie Knowledge Graph")
    st.markdown("Welcome to the Movie Knowledge Graph! Explore movie similarities, details, and recommendations.")

    # Select the desired functionality
    option = st.selectbox(
        "Select an option:",
        ["Movie Similarity", "Movie Details", "Movie Recommendations"]
    )

    if option == "Movie Similarity":
        st.subheader("Compare Two Movies")
        col1, col2 = st.columns(2)  # Create two columns for side-by-side input

        with col1:
            movie1 = st.text_input("Enter Movie 1:")
        
        with col2:
            movie2 = st.text_input("Enter Movie 2:")

        if st.button("Compare Movies"):
            try:
                KG = KnowledgeGraph()  # Create an instance of KnowledgeGraph
                KG.movie_similarity(movie1, movie2)
                st.success("Similarity graph generated. Check the PDF.")

                # Display the PDF
                with open("movie_similarity.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button(
                    label="Download Similarity Graph",
                    data=PDFbyte,
                    file_name="movie_similarity.pdf",
                    mime='application/pdf'
                )
                st.image(Image.open("movie_similarity.pdf"))

            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Movie Details":
        st.subheader("Get Movie Details")
        movie_name = st.text_input("Enter Movie Name:")

        if st.button("Show Details"):
            try:
                KG = KnowledgeGraph()  # Create an instance of KnowledgeGraph
                KG.movie_details(movie_name)
                st.success("Movie details graph generated. Check the PDF.")

                # Display the PDF
                with open("movie_detail.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button(
                    label="Download Movie Details Graph",
                    data=PDFbyte,
                    file_name="movie_detail.pdf",
                    mime='application/pdf'
                )
                st.image(Image.open("movie_detail.pdf"))

            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Movie Recommendations":
        st.subheader("Get Movie Recommendations")
        movie1 = st.text_input("Enter Movie Name for Recommendations:")
        
        if st.button("Get Recommendations"):
            fun(movie1)

def fun(movie1):
    """
    Method to return list of best matching movies based on a ranking system.
    """
    try:
        with open('assets/final_dataset_imdb.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            movie1row = None
            for row in csv_reader:
                if row[2] == movie1:
                    movie1row = row
                    break

        if not movie1row:
            st.error(f"Movie '{movie1}' not found in the dataset.")
            return

        best_movies = []
        best_score = 0
        best_movie = ''
        
        with open('assets/final_dataset_imdb.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)  # Skip header
            for row in csv_reader:
                if row[1] == movie1row[1] or int(row[15]) < 5000 or int(row[3]) < 1950:
                    continue
                
                score = 0 
                
                if movie1row[3] == row[3]:
                    score += 2
                
                genresa1 = set(movie1row[5].split(", "))
                genresb1 = set(row[5].split(", "))
                score += 7 * len(genresa1.intersection(genresb1)) 
                
                diff = len(genresa1.union(genresb1)) - len(genresa1.intersection(genresb1))
                score -= diff
                
                if row[7] == movie1row[7]:
                    score += 1
                
                languages1a = set(movie1row[8].split(", "))
                languages1b = set(row[8].split(", "))
                score += len(languages1a.intersection(languages1b))

                if row[9] == movie1row[9]:
                    score += 3

                if row[10] == movie1row[10]:
                    score += 3

                actors1a = set(movie1row[12].split(", "))
                actors1b = set(row[12].split(", "))
                score += 4 * len(actors1a.intersection(actors1b))
                
                if row[11] == movie1row[11]:
                    score += 3

                score += 0.00000000000001 * float(row[15])

                if len(best_movies) < 10 or score > best_movies[-1][0]:                   
                    if len(best_movies) >= 10:
                        best_movies.pop(-1)
                    best_movies.append((score, row[2]))
                
                best_movies.sort(reverse=True)

        # Displaying the results on Streamlit
        st.write(f"**Best Movie Match for '{movie1}'**: {best_movie}")
        st.write(f"Score: {best_score}")
        
        st.write("### Top Recommended Movies:")
        for rank, (score, title) in enumerate(best_movies, start=1):
            st.write(f"**Rank {rank}:** {title} \nScore: {score}")

    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()