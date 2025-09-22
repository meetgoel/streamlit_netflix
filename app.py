import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Header with submission info
st.title("🎬 Netflix Titles Dashboard with Insights")
st.markdown("""
**Student Name:** Meet Goel  
**Student ID:** GH1035975  
**Submitted to:** Prof. Mehran Monavari
""")
st.markdown("---")  # horizontal line

# Load dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/meetgoel/ML-Projects/refs/heads/main/Datasets/netflix_titles.csv"
    df = pd.read_csv(url)
    df['director'].fillna('Unknown', inplace=True)
    df['cast'].fillna('Unknown', inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df.dropna(subset=['date_added', 'rating', 'duration'], inplace=True)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    return df

df = load_data()

# --------------------------
# Sidebar Filters
# --------------------------
st.sidebar.header("Filter Dashboard")

# Content Type Filter
content_type = st.sidebar.multiselect(
    "Select Content Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)

# Country Filter
countries = st.sidebar.multiselect(
    "Select Countries",
    options=df['country'].unique(),
    default=df['country'].unique()
)

# Year Added Filter
year_range = st.sidebar.slider(
    "Select Year Added Range",
    min_value=int(df['year_added'].min()),
    max_value=int(df['year_added'].max()),
    value=(int(df['year_added'].min()), int(df['year_added'].max()))
)

# Rating Filter
ratings = st.sidebar.multiselect(
    "Select Ratings",
    options=df['rating'].unique(),
    default=df['rating'].unique()
)

# Apply filters
filtered_df = df[
    (df['type'].isin(content_type)) &
    (df['country'].isin(countries)) &
    (df['year_added'] >= year_range[0]) & 
    (df['year_added'] <= year_range[1]) &
    (df['rating'].isin(ratings))
]

# Sidebar KPIs
st.sidebar.markdown("### Quick Stats")
st.sidebar.write("Total Movies:", len(filtered_df[filtered_df['type']=="Movie"]))
st.sidebar.write("Total TV Shows:", len(filtered_df[filtered_df['type']=="TV Show"]))
st.sidebar.write("Oldest Content Year:", filtered_df['release_year'].min())
st.sidebar.write("Newest Content Year:", filtered_df['release_year'].max())

# --------------------------
# Tabs
# --------------------------
tabs = st.tabs([
    "Dataset Overview",
    "Content Type Distribution",
    "Content Growth Over Time",
    "Country Analysis",
    "Genre Breakdown",
    "Content Ratings",
    "Release Year Distribution",
    "Top Directors"
])

# Tab 1: Dataset Overview
with tabs[0]:
    st.header("Dataset Overview")
    st.markdown("This tab gives a quick look at the dataset, including the number of rows, columns, and missing values.")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Shape of filtered dataset:", filtered_df.shape)
        st.dataframe(filtered_df.head(11))
    with col2:
        st.write("Missing values:")
        st.dataframe(filtered_df.isnull().sum())

# Tab 2: Content Type Distribution
with tabs[1]:
    st.subheader("Distribution of Content Type (Movies vs. TV Shows)")
    st.markdown("Shows the proportion of Movies vs TV Shows in the filtered dataset.")
    type_counts = filtered_df['type'].value_counts().to_frame()
    st.bar_chart(type_counts)

# Tab 3: Content Growth Over Time
with tabs[2]:
    st.subheader("How has Netflix's content grown over time?")
    st.markdown("Shows the yearly growth of Movies and TV Shows added to Netflix.")
    content_added = filtered_df.groupby(['year_added','type']).size().unstack(fill_value=0)
    st.area_chart(content_added)

# Tab 4: Country Analysis
with tabs[3]:
    st.subheader("Top 10 Countries with Most Content")
    st.markdown("Shows which countries contribute the most content in the filtered dataset.")
    top_10_countries = filtered_df['country'].value_counts().head(10).to_frame()
    st.bar_chart(top_10_countries)

# Tab 5: Genre Breakdown
with tabs[4]:
    st.subheader("Top Genres in Movies vs TV Shows")
    st.markdown("Shows popular genres for Movies and TV Shows in the filtered dataset.")
    movies_df = filtered_df[filtered_df['type']=="Movie"]
    tv_df = filtered_df[filtered_df['type']=="TV Show"]

    movie_genres = movies_df['listed_in'].str.split(', ').explode().value_counts().head(10).to_frame()
    tv_genres = tv_df['listed_in'].str.split(', ').explode().value_counts().head(10).to_frame()

    col1, col2 = st.columns(2)
    with col1:
        st.write("🎬 Movie Genres")
        st.bar_chart(movie_genres)
    with col2:
        st.write("📺 TV Show Genres")
        st.bar_chart(tv_genres)

# Tab 6: Content Ratings
with tabs[5]:
    st.subheader("Content Ratings Distribution (by Type)")
    st.markdown("Shows how ratings are distributed among Movies and TV Shows in the filtered dataset.")
    rating_counts = filtered_df.groupby(['rating','type']).size().unstack(fill_value=0)
    st.bar_chart(rating_counts)

# Tab 7: Release Year Distribution
with tabs[6]:
    st.subheader("Content Distribution by Release Year (Movies vs TV Shows)")
    st.markdown("Shows the distribution of content by release year for Movies and TV Shows.")
    release_year_counts = filtered_df.groupby(['release_year','type']).size().unstack(fill_value=0)
    st.line_chart(release_year_counts)

# Tab 8: Top Directors
with tabs[7]:
    st.subheader("Top 10 Directors by Number of Titles")
    st.markdown("Shows the top directors in the filtered dataset by number of titles contributed.")
    directors = filtered_df['director'].str.split(', ').explode().value_counts()
    directors = directors[directors.index!='Unknown'].head(10).to_frame()
    st.bar_chart(directors)
