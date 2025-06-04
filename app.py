import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the main Reddit dataset
df_main = pd.read_csv("data/reddit_data.csv")
df_main['date'] = pd.to_datetime(df_main['date'])

# Load sentiment dataset
df_sentiment = pd.read_csv("data/sentiment_data.csv")

# Merge on title to include sentiment columns
df = pd.merge(df_main, df_sentiment, on='title', how='left')

# Initialize app
app = dash.Dash(__name__)
app.title = "RedCast - Reddit Virality Dashboard"

# Visualization 1: Sentiment over time
sentiment_fig = px.line(
    df.groupby('date')['sentiment_score'].mean().reset_index(),
    x='date', y='sentiment_score',
    title='📉 Average Sentiment Over Time'
)

# Visualization 2: Post volume
volume_fig = px.bar(
    df.groupby('date').size().reset_index(name='count'),
    x='date', y='count',
    title='📈 Post Volume Over Time'
)

# Visualization 3: Score vs Comments colored by sentiment score
scatter_fig = px.scatter(
    df.dropna(subset=['sentiment_score']),
    x='score', y='num_comments',
    color='sentiment_score',
    title='💬 Score vs Comments by Sentiment Score',
    hover_data=['title']
)

# Visualization 4: Sentiment distribution
sentiment_dist_fig = px.histogram(
    df.dropna(subset=['sentiment']),
    x='sentiment',
    title='🎭 Sentiment Distribution',
    color='sentiment'
)

# Visualization 5: Virality distribution (if available)
if 'viral' in df.columns:
    viral_dist_fig = px.histogram(
        df.dropna(subset=['viral']),
        x='viral',
        title='🔥 Virality Distribution',
        color='viral'
    )
else:
    viral_dist_fig = px.histogram(
        title='🔥 Virality column missing'
    )

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
