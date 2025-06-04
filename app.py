import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load main and sentiment datasets
df_main = pd.read_csv("data/reddit_data.csv")
df_sentiment = pd.read_csv("data/sentiment_data.csv")

# Convert date column
df_main['date'] = pd.to_datetime(df_main['date'])

# Merge on title
df = pd.merge(df_main, df_sentiment, on='title', how='left')

# Initialize app
app = dash.Dash(__name__)
app.title = "RedCast - Reddit Virality Dashboard"

# ======== Visualization 1: Sentiment Over Time ========
if 'sentiment_score' in df.columns and df['sentiment_score'].notna().any():
    sentiment_fig = px.line(
        df.groupby('date')['sentiment_score'].mean().reset_index(),
        x='date', y='sentiment_score',
        title='📉 Average Sentiment Over Time'
    )
else:
    sentiment_fig = px.line(title="⚠️ Sentiment Score Data Not Available")

# ======== Visualization 2: Post Volume Over Time ========
volume_fig = px.bar(
    df.groupby('date').size().reset_index(name='count'),
    x='date', y='count',
    title='📈 Post Volume Over Time'
)

# ======== Visualization 3: Score vs Comments ========
if 'sentiment_score' in df.columns:
    scatter_fig = px.scatter(
        df.dropna(subset=['sentiment_score']),
        x='score', y='num_comments',
        color='sentiment_score',
        title='💬 Score vs Comments by Sentiment Score',
        hover_data=['title']
    )
else:
    scatter_fig = px.scatter(title="⚠️ Cannot Plot Score vs Comments — Sentiment Score Missing")

# ======== Visualization 4: Sentiment Distribution ========
if 'sentiment' in df.columns:
    sentiment_dist_fig = px.histogram(
        df.dropna(subset=['sentiment']),
        x='sentiment',
        color='sentiment',
        title='🎭 Sentiment Distribution'
    )
else:
    sentiment_dist_fig = px.histogram(title="⚠️ Sentiment Column Missing")

# ======== Visualization 5: Virality Breakdown ========
if 'viral' in df.columns:
    viral_dist_fig = px.histogram(
        df.dropna(subset=['viral']),
        x='viral',
        color='viral',
        title='🔥 Virality Distribution'
    )
else:
    viral_dist_fig = px.histogram(title="⚠️ Virality Data Not Available")

# Layout
app.layout = html.Div([
    html.H1("🧠 RedCast - Reddit Virality Dashboard", style={'textAlign': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Sentiment Over Time', children=[dcc.Graph(figure=sentiment_fig)]),
        dcc.Tab(label='Post Volume', children=[dcc.Graph(figure=volume_fig)]),
        dcc.Tab(label='Score vs Comments', children=[dcc.Graph(figure=scatter_fig)]),
        dcc.Tab(label='Sentiment Breakdown', children=[dcc.Graph(figure=sentiment_dist_fig)]),
        dcc.Tab(label='Virality Analysis', children=[dcc.Graph(figure=viral_dist_fig)])
    ]),
    html.Div(id="back-to-top-anchor")
])

if __name__ == '__main__':
    app.run(debug=True)
