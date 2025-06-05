import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

# Load datasets
df_main = pd.read_csv("data/reddit_data.csv")
df_sentiment = pd.read_csv("data/sentiment_data.csv")

# Ensure correct columns
df_sentiment = df_sentiment[['title', 'sentiment', 'sentiment_score']].drop_duplicates()

# Drop existing sentiment columns from df_main if present to avoid suffix conflicts
df_main = df_main.drop(columns=[col for col in ['sentiment', 'sentiment_score'] if col in df_main.columns])

# Merge sentiment into main dataframe
df = pd.merge(df_main, df_sentiment, on='title', how='left')

# Convert date column
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# --- Visualization 1: Sentiment Over Time ---
try:
    sentiment_trend = df.dropna(subset=['date', 'sentiment_score'])
    sentiment_fig = px.line(
        sentiment_trend.groupby('date')['sentiment_score'].mean().reset_index(),
        x='date', y='sentiment_score',
        title='📉 Average Sentiment Over Time'
    )
except Exception:
    sentiment_fig = "No data available"

# --- Visualization 2: Post Volume Over Time ---
try:
    volume = df.dropna(subset=['date']).groupby('date').size().reset_index(name='count')
    volume_fig = px.bar(volume, x='date', y='count', title='📈 Post Volume Over Time')
except Exception:
    volume_fig = "No data available"

# --- Visualization 3: Score vs Comments by Sentiment ---
try:
    scatter_data = df.dropna(subset=['sentiment_score', 'score', 'num_comments'])
    scatter_fig = px.scatter(
        scatter_data, x='score', y='num_comments',
        color='sentiment_score', size_max=60,
        title='💬 Score vs Comments by Sentiment Score'
    )
except Exception:
    scatter_fig = "No data available"

# --- Visualization 4: Sentiment Distribution ---
try:
    sentiment_dist_fig = px.histogram(
        df.dropna(subset=['sentiment']),
        x='sentiment', color='sentiment',
        title='🎭 Sentiment Category Distribution'
    )
except Exception:
    sentiment_dist_fig = "No data available"

# Layout
app = dash.Dash(__name__)
app.title = "RedCast - Reddit Virality Dashboard"

app.layout = html.Div([
    html.H1("🧠 RedCast - Reddit Virality Dashboard", style={'textAlign': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Sentiment Over Time', children=[
            dcc.Graph(figure=sentiment_fig) if isinstance(sentiment_fig, Figure) else html.Div("No data to display")
        ]),
        dcc.Tab(label='Post Volume', children=[
            dcc.Graph(figure=volume_fig) if isinstance(volume_fig, Figure) else html.Div("No data to display")
        ]),
        dcc.Tab(label='Score vs Comments', children=[
            dcc.Graph(figure=scatter_fig) if isinstance(scatter_fig, Figure) else html.Div("No data to display")
        ]),
        dcc.Tab(label='Sentiment Breakdown', children=[
            dcc.Graph(figure=sentiment_dist_fig) if isinstance(sentiment_dist_fig, Figure) else html.Div("No data to display")
        ]),
    ]),
    html.Footer("Built by Abhir Iyer", style={
        'textAlign': 'center',
        'padding': '1rem',
        'marginTop': '2rem',
        'fontSize': '14px',
        'color': '#aaa',
        'borderTop': '1px solid #eee'
    })
])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=False)
