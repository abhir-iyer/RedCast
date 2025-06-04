import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load main and sentiment datasets
df_main = pd.read_csv("data/reddit_data.csv")
df_sentiment = pd.read_csv("data/sentiment_data.csv")

# Ensure date columns are datetime
df_main['date'] = pd.to_datetime(df_main['date'])
df_sentiment['date'] = pd.to_datetime(df_sentiment['date'])

# Merge on date
df = pd.merge(df_main, df_sentiment, on='date', how='left')

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "RedCast - Reddit Virality Dashboard"

# Visualization 1: Average Sentiment Over Time
sentiment_fig = px.line(
    df.groupby('date')['sentiment_score'].mean().reset_index(),
    x='date', y='sentiment_score',
    title='📉 Average Sentiment Over Time'
)

# Visualization 2: Post Volume Over Time
volume_fig = px.bar(
    df.groupby('date').size().reset_index(name='count'),
    x='date', y='count',
    title='📈 Post Volume Over Time'
)

# Visualization 3: Score vs Number of Comments Colored by Sentiment Score
scatter_fig = px.scatter(
    df, x='score', y='num_comments',
    color='sentiment_score',
    title='💬 Score vs Number of Comments by Sentiment Score',
    hover_data=['title']
)

# Visualization 4: Sentiment Distribution (if sentiment available)
sentiment_dist_fig = px.histogram(
    df.dropna(subset=['sentiment']),
    x='sentiment',
    title='🎭 Sentiment Distribution',
    color='sentiment'
)

# Visualization 5: Virality Analysis (if viral column exists)
if 'viral' in df.columns:
    viral_dist_fig = px.histogram(
        df.dropna(subset=['viral']),
        x='viral',
        title='🔥 Virality Distribution',
        color='viral'
    )
else:
    viral_dist_fig = px.histogram(
        title="No 'viral' column found"
    )

# Define layout
app.layout = html.Div([
    html.H1("🧠 RedCast - Reddit Virality Dashboard", style={'textAlign': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Sentiment Over Time', children=[dcc.Graph(figure=sentiment_fig)]),
        dcc.Tab(label='Post Volume', children=[dcc.Graph(figure=volume_fig)]),
        dcc.Tab(label='Score vs Comments', children=[dcc.Graph(figure=scatter_fig)]),
        dcc.Tab(label='Sentiment Breakdown', children=[dcc.Graph(figure=sentiment_dist_fig)]),
        dcc.Tab(label='Virality Analysis', children=[dcc.Graph(figure=viral_dist_fig)])
    ]),
    html.Div(id="back-to-top-anchor")  # For back-to-top button
])

if __name__ == '__main__':
    app.run(debug=True)
