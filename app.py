import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/meetgoel/ML-Projects/refs/heads/main/Datasets/netflix_titles.csv"
    return pd.read_csv(url)

df = load_data()

# Title
st.title("🎬 Netflix Titles Dashboard")

# Dataset Overview
st.header("Dataset Overview")
col1, col2 = st.columns(2)
with col1:
    st.write("Shape of dataset:", df.shape)
    st.dataframe(df.head())
with col2:
    st.write("Missing values:")
    st.dataframe(df.isnull().sum())

# Sidebar filters
st.sidebar.header("Filters")
selected_type = st.sidebar.multiselect("Select Type", df['type'].dropna().unique(), default=df['type'].dropna().unique())
selected_country = st.sidebar.multiselect("Select Country", df['country'].dropna().unique()[:20])

filtered_df = df[df['type'].isin(selected_type)]
if selected_country:
    filtered_df = filtered_df[filtered_df['country'].isin(selected_country)]

# Visualization 1: Count of Titles by Type
st.header("Count of Titles by Type")
fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x='type', ax=ax, palette="Set2")
st.pyplot(fig)

# Visualization 2: Top 10 Countries with Most Titles
st.header("Top 10 Countries with Most Titles")
fig, ax = plt.subplots()
filtered_df['country'].value_counts().head(10).plot(kind='bar', ax=ax, color="skyblue")
ax.set_ylabel("Count")
ax.set_title("Top 10 Countries")
st.pyplot(fig)

# Visualization 3: Titles Added Over Time
st.header("Titles Added Over Time")
fig, ax = plt.subplots()
filtered_df['date_added'] = pd.to_datetime(filtered_df['date_added'], errors='coerce')
filtered_df.groupby(filtered_df['date_added'].dt.year).size().plot(ax=ax, marker='o')
ax.set_ylabel("Number of Titles")
ax.set_xlabel("Year")
ax.set_title("Titles Added Over Years")
st.pyplot(fig)

# Raw Data Expander
with st.expander("View Raw Data"):
    st.dataframe(filtered_df)
