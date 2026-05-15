# VibeIQ 🎵

## Spotify Audio Intelligence Dashboard

This is an interactive Spotify analytics dashboard built using Python, Streamlit, Pandas, Plotly, and Seaborn. The project explores Spotify track data to uncover insights related to song popularity, artist trends, danceability, energy, valence, and listener behavior through dynamic visualizations and audio feature analysis.

---

## Features

### Interactive Dashboard
- Multi-tab dashboard interface
- Real-time filtering using Streamlit sidebar controls
- Dynamic charts and responsive analytics

### Audio Intelligence Analysis
- Correlation heatmap for Spotify audio features
- Danceability vs popularity analysis
- Popularity distribution histograms
- Explicit vs non-explicit content comparison
- Mood composition analysis

### Popularity Insights
- Popularity tier segmentation
- Artist popularity analysis
- Track-level analytics
- Listener behavior insights

### Data Processing
- Artist data cleaning and transformation
- Exploded artist analysis for collaborations
- Feature engineering using Pandas
- Cached data loading for faster performance

---

## Tech Stack

### Languages & Libraries
- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- Seaborn
- Matplotlib

---

## Dashboard Sections

### Overview
Provides a high-level summary of Spotify track data including:
- Total songs
- Total artists
- Average popularity
- Average danceability
- Top artist analysis
- Popularity distribution

### Audio Intelligence
Explores relationships between Spotify audio features such as:
- Danceability
- Energy
- Valence
- Tempo
- Popularity
- Acousticness

Includes:
- Correlation heatmaps
- Scatter plots
- Histograms
- Box plots
- Mood analysis

### Popularity Insights
Analyzes the factors influencing track popularity through:
- Popularity tier segmentation
- Explicit content comparison
- Audio feature trends
- Listener engagement patterns

---

## Project Structure

```bash
spotify-dashboard/
│
├── app/
│   └── dashboard.py
│
├── data/
│   └── spotify/
│       └── data.csv
│
├── notebooks/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/vibeiq.git
cd vibeiq
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Dashboard

```bash
streamlit run app/dashboard.py
```

---

## Dataset

This project uses Spotify track metadata and audio feature datasets containing:
- Track information
- Artist information
- Popularity metrics
- Audio feature analysis
- Explicit content indicators

---

## Key Insights

- Highly danceable tracks tend to maintain moderate-to-high popularity.
- High-energy songs often dominate upper popularity tiers.
- Explicit tracks show distinct popularity distributions compared to non-explicit tracks.
- Audio features such as energy and loudness demonstrate strong positive correlation.

---

## Future Improvements

- Spotify API integration
- Recommendation system
- Genre clustering analysis
- Machine learning-based popularity prediction
- User authentication and personalized analytics
- Advanced UI customization

---

## Deployment

The dashboard can be deployed using:
- Streamlit Community Cloud
- Render
- Hugging Face Spaces

---

## Author

Built by Amar Gurung as a portfolio project focused on data analysis, visualization, and interactive dashboard development using Python.
