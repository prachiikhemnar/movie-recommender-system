import streamlit as st
import pandas as pd
import csv
import os
from movie_recommender import get_recommendations, get_movie_details

# Load movie data
df = pd.read_csv('movies.csv')

# Page config
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
            background-color: #f8f5f2;
            color: #3e2723;
        }

        h1, h2, h3 {
            color: #4e342e;
        }

        .stButton>button {
            background-color: #8d6e63;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6em 1.4em;
            font-weight: 600;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease-in-out;
        }

        .stButton>button:hover {
            background-color: #6d4c41;
            transform: scale(1.05);
        }

        .stTextInput>div>div>input {
            border-radius: 6px;
            padding: 10px;
            background-color: #fefcfb;
            color: #4e342e;
            border: 1px solid #d7ccc8;
        }

        .stAlert {
            background-color: #fbe9e7;
            border-left: 5px solid #a1887f;
        }

        .custom-footer {
            font-size: 13px;
            color: #5d4037;
            text-align: center;
            padding-top: 20px;
        }

        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🍿 Movie Recommender System")
st.markdown("##### Find your next favorite movie based on what you like 🎥")

# Centered Input Area
st.markdown("## 🎯 Enter a Movie Title")
input_col1, input_col2, input_col3 = st.columns([1, 2, 1])
with input_col2:
    selected_movie = st.text_input("Enter a movie title", key="movie_input")

# Centered Button
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    get_button_clicked = st.button("🎬 Get Recommendations")

# Content Columns
col1, col2 = st.columns([1, 2])

# Selected Movie Info + User Feedback
with col1:
    st.header("🎞️ Selected Movie Info")
    if selected_movie:
        matching_movies = df[df['title'].str.contains(selected_movie, case=False, na=False)]
        if not matching_movies.empty:
            exact_match = matching_movies[matching_movies['title'].str.lower() == selected_movie.lower()]
            if not exact_match.empty:
                movie_details = get_movie_details(exact_match.iloc[0]['title'])
            else:
                movie_details = get_movie_details(matching_movies.iloc[0]['title'])

            st.subheader(movie_details['title'])
            st.markdown(f"**📚 Genres:** {movie_details['genres']}")
            st.markdown(f"**📅 Release Date:** {movie_details['release_date']}")
            st.markdown(f"**⭐ Average Vote:** {movie_details['vote_average']}/10")
            st.markdown("**📝 Overview:**")
            st.markdown(movie_details['overview'])

            # --- User Ratings & Reviews Input ---
            user_rating = st.slider("Rate this movie (your view)", 0, 10, 5, key='rating_slider')
            user_comment = st.text_area("Your comment", key='comment_area')

            if st.button("Submit Feedback", key='submit_feedback'):
                feedback_file = 'user_feedback.csv'
                file_exists = os.path.isfile(feedback_file)
                try:
                    with open(feedback_file, mode='a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        if not file_exists:
                            writer.writerow(['movie_title', 'rating', 'comment'])
                        writer.writerow([movie_details['title'], user_rating, user_comment])
                    st.success("Thanks for your feedback!")
                except Exception as e:
                    st.error(f"Error saving feedback: {e}")
        else:
            st.warning("No matching movie found. Please try another title.")

# Recommendations
with col2:
    st.header("✨ Recommended Movies")
    if get_button_clicked:
        if selected_movie and not matching_movies.empty:
            with st.spinner("Finding similar movies..."):
                movie_id = matching_movies.iloc[0]['id']
                recommendations = get_recommendations(movie_id)

                for i, movie in enumerate(recommendations, 1):
                    with st.expander(f"{i}. {movie}"):
                        rec_details = get_movie_details(movie)
                        st.markdown(f"**📚 Genres:** {rec_details['genres']}")
                        st.markdown(f"**📅 Release Date:** {rec_details['release_date']}")
                        st.markdown(f"**⭐ Average Vote:** {rec_details['vote_average']}/10")
                        st.markdown("**📝 Overview:**")
                        st.markdown(rec_details['overview'])
        else:
            st.warning("Please enter a valid movie title to get recommendations.")

# Footer
st.markdown("---")
st.markdown('<div class="custom-footer">🎬 Movie Recommender • Designed with ❤️ by Prachi</div>', unsafe_allow_html=True)
