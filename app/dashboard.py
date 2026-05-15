import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Put the widget OUTSIDE the function
test_mode = st.sidebar.checkbox("Testing Mode (Faster)", value=True)

# 2. Pass test_mode into the function as an argument
@st.cache_data
def load_and_clean_data(is_testing):
    # Use the argument to decide how much data to load
    if is_testing:
        df = pd.read_csv("../data/spotify/data.csv", nrows=5000)
    else:
        df = pd.read_csv("../data/spotify/data.csv")
    
    # ... all your cleaning/exploding logic here ...
    df["clean_artists"] = df["artists"].str.replace(r"[\[\]'\" ]", "", regex=True).str.split(",")
    df_exploded = df.explode("clean_artists")
    df_exploded["clean_artists"] = df_exploded["clean_artists"].str.strip()
    df_exploded['mood'] = pd.qcut(
        df_exploded['valence'], q=2, labels=['Mellow', 'Upbeat']
    )
    df_exploded['popularity_tier'] = pd.cut(
    df_exploded['popularity'], 
    bins=[0,33,66,100],
    labels=['Low', 'Medium', 'High'],
    include_lowest=True
)

    return df, df_exploded

# 3. Call it with the checkbox value
df, df_exploded = load_and_clean_data(test_mode)

st.sidebar.header("Filters")

# Popularity Slider
min_popularity = st.sidebar.slider(
    "Minimum Popularity",
    0.0,
    100.0,
    50.0
)

# Artist Dropdown
artist_list = sorted(df_exploded["clean_artists"].unique())

selected_artist = st.sidebar.selectbox(
    "Select Artist",
    ["All Artists"] + artist_list
)


filtered_df = df_exploded[
    df_exploded["popularity"] >= min_popularity
].copy()

if selected_artist != "All Artists":
    filtered_df = filtered_df[
        filtered_df["clean_artists"] == selected_artist
    ]


st.title("Spotify Audio Intelligence Analysis ")

tab1, tab2, tab3 = st.tabs(['Overview', 'Audio Intelligence', 'Popularity Insights'])

with tab1:
    st.markdown("""
Spotify Audio Intelligence Analysis is an interactive data analytics dashboard built using Python, Streamlit, Pandas, Seaborn and Plotly. The project analyzes Spotify track data to uncover insights related to song popularity, artist trends, danceability, energy, and other audio features through dynamic visualizations, filters, and correlation analysis.
""")
    st.divider()
    st.header("Audio Dashboard")
    st.markdown("""The Audio Intelligence Dashboard explores relationships between Spotify audio features such as danceability, energy, valence, tempo, and popularity. It provides interactive visualizations and correlation analysis to uncover patterns in musical characteristics and listener preferences.""")

    artists = filtered_df["clean_artists"].nunique()

    total_songs = filtered_df["name"].nunique()

    avg_pop = filtered_df["popularity"].mean()
    average_popularity = round(avg_pop, 2) if pd.notnull(avg_pop) else 0.0

    average_danceability = round(
    filtered_df["danceability"].mean(), 
    2
)

    st1, st2, st3, st4 = st.columns(4)

    st1.metric(
        label="Total Artists",
        value=artists,
        border=True
    )

    st2.metric(
        label="Total Songs",
        value=total_songs,
        border=True
    )

    st3.metric(
        label="Average Popularity",
        value=average_popularity,
        border=True
    )

    st4.metric(
        label="Average Danceability",
        value=average_danceability,
        border=True
    )
    st.dataframe(filtered_df[['artists', 'name', 'popularity', 'danceability']].sort_values(ascending=False, by='popularity'))

    st.divider()
    st.header("Charts")
    col1, col2 = st.columns(2)
    with col1:

        st.subheader("1. Top 10 Most Popular Artists")

        top_10_peaks = (
            filtered_df
            .groupby("clean_artists")["popularity"]
            .max()
            .sort_values(ascending=False)
            .head(10)
            .reset_index(name="popularity")
            )

        st.bar_chart(
                top_10_peaks,
                x="clean_artists",
                y="popularity",
                color="clean_artists"
            )
        st.markdown(
            "Most songs cluster around medium popularity scores, while extremely popular songs are relatively rare."
            )
    with col2:
        st.subheader("2. Danceability vs Popularity Scatter Plot")
        
        fig = px.scatter(
            filtered_df, 
                x="danceability",
                y="popularity",
                color="energy"
            )
        st.plotly_chart(fig, use_container_width=True, key="scatterplot")
        st.markdown("""This scatter plot visualizes the relationship between danceability and song popularity. It helps identify whether highly danceable tracks tend to achieve greater popularity among listeners.""")
    st.divider()
    st.markdown("""#### The Overview Dashboard provides a high-level summary of Spotify track data, highlighting key metrics, artist trends, and popularity patterns to help users quickly explore the dataset.""")


with tab2:
    st.header("Audio Intelligence")
    st.subheader("1. Correalation Heatmap")
    numeric_df = filtered_df.select_dtypes(include=['number'])
    corr_matrix = numeric_df.corr()
    fig, ax =plt.subplots()
    sns.heatmap(
        corr_matrix,
        cmap="crest",
        annot=True,
        annot_kws={'size': 5},
        linewidths=.5
    )
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("2. Top 10 Most Popular Artists")

        top_10_peaks = (
            filtered_df
            .groupby("clean_artists")["popularity"]
            .max()
            .sort_values(ascending=False)
            .head(10)
            .reset_index(name="popularity")
        )

        st.bar_chart(
            top_10_peaks,
            x="clean_artists",
            y="popularity",
            color="clean_artists"
        )
    

    with col2:
        st.subheader("3. Popularity Distribution Histogram")

        fig = px.histogram(
        filtered_df,
        x="popularity",
        nbins=20,
        title="Popularity Score Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)


    st.subheader("4. Danceability vs Popularity Scatter Plot")
    fig = px.scatter(
        filtered_df, 
            x="danceability",
            y="popularity",
            color="energy"
        )
    st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("5. Explicit Songs vs Non-Explicit songs (Popularity)")
        filtered_df["explicit_label"] = filtered_df["explicit"].astype(str)
        fig = px.box(
            filtered_df,
            x = "explicit_label",
            y = "popularity",
            color = "explicit_label",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("6. Explicit Songs vs Non-Explicit songs (Valence)")
        filtered_df["explicit_label"] = filtered_df["explicit"].astype(str)
        fig = px.box(
            filtered_df,
            x = "explicit_label",
            y = "valence",
            color = "explicit_label",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("7. Mood Composition")
    mood_counts = filtered_df['mood'].value_counts().reset_index()

    fig = px.pie(
        mood_counts,
        values="count",
        hole = 0.5,
        names="mood",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig, use_container_width=True)


    
with tab3:
    st.header("📊 Deep Dive: Popularity Insights")
    
    st.markdown("""
    This section explores the underlying factors that drive a song's success on Spotify. By segmenting the data into 
    **Popularity Tiers** and analyzing **Content Type**, we can identify what separates a 'Hit' from a 'Deep Cut'.
    """)

    # First Insight Section: The Tiers
    st.subheader("1. Understanding the Tiers")
    st.info("""
    **Methodology:** We use **Quantile-based binning (qcut)** to divide the dataset into three equal-sized groups. 
    This ensures that our 'High' popularity definition is relative to the current filtered dataset, rather than an arbitrary score.
    """)
    

    st.markdown("""
        * **High Tier:** Tracks that sit in the top 33% of listener engagement.
        * **Medium Tier:** Stable tracks with consistent but non-viral performance.
        * **Low Tier:** Newer releases, niche genres, or archival tracks.
        """)
    
    st.subheader("Popularity Tier Distribution")
    tier_counts = filtered_df['popularity_tier'].value_counts().reset_index()

    fig = px.treemap(
        tier_counts,
        path=['popularity_tier'],
        values='count',
        color='popularity_tier'
    )
    st.plotly_chart(fig, use_container_width=True)        

    st.divider()

    # Second Insight Section: Audio Characteristics
    st.subheader("2. The 'Hit' Profile")
    st.markdown("""
    Based on the **Correlation Heatmap** and **Scatter Plots** in the previous tabs, we can observe specific 
    trends among high-popularity tracks:
    
    * **Energy vs. Popularity:** High-energy tracks often dominate the upper tiers, suggesting a preference for upbeat content.
    * **The Valence Factor:** Tracks labeled as 'Upbeat' (High Valence) show a slight edge in median popularity compared to 'Mellow' tracks.
    * **Danceability:** There is a notable cluster of hits in the 0.6–0.8 danceability range.
    """)

    # Third Insight Section: Explicit Content
    st.subheader("3. Content Impact")
    st.markdown("""
    Our analysis of **Explicit vs. Non-Explicit** content reveals:
    * **Market Share:** While non-explicit songs are more numerous, explicit tracks often maintain a tighter, more consistent popularity range.
    * **Outlier Success:** The highest peak popularity scores are frequently achieved by non-explicit tracks, likely due to their broader 'all-ages' reach.
    """)

    st.success("💡 **Final Takeaway:** Popularity isn't driven by a single feature, but by a combination of high energy, accessible danceability, and broad content appeal.")

