import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load data
df_main = pd.read_csv("data/reddit_data.csv")
df_sentiment = pd.read_csv("data/sentiment_data.csv")

# Clean duplicates if any
df_main = df_main.drop(columns=[col for col in ['sentiment', 'sentiment_score'] if col in df_main.columns])

# Merge based on title
df = pd.merge(df_main, df_sentiment[['title', 'sentiment', 'sentiment_score']], on='title', how='left')
df['date'] = pd.to_datetime(df['date'])

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "RedCast - Reddit Virality Dashboard"

# Visualizations

# 1. Sentiment Over Time
sentiment_fig = px.line(
    df.groupby('date')['sentiment_score'].mean().reset_index(),
    x='date', y='sentiment_score',
    title='📉 Average Sentiment Over Time'
)

# 2. Post Volume Over Time
volume_fig = px.bar(
    df.groupby('date').size().reset_index(name='count'),
    x='date', y='count',
    title='📈 Post Volume Over Time'
)

# 3. Score vs Comments (colored by sentiment)
scatter_fig = px.scatter(
    df, x='score', y='num_comments',
    color='sentiment_score',
    title='💬 Score vs Number of Comments by Sentiment'
)

# 4. Sentiment Distribution
if 'sentiment' in df.columns and df['sentiment'].notna().any():
    sentiment_dist_fig = px.histogram(
        df.dropna(subset=['sentiment']),
        x='sentiment',
        color='sentiment',
        title='🎭 Sentiment Distribution'
    )
else:
    sentiment_dist_fig = px.histogram(title="🎭 Sentiment Distribution (No Data)")

# 5. Virality Distribution (check existence)
if 'viral' in df.columns and df['viral'].notna().any():
    viral_dist_fig = px.histogram(
        df.dropna(subset=['viral']),
        x='viral',
        color='viral',
        title='🔥 Virality Distribution'
    )
else:
    viral_dist_fig = px.histogram(title="🔥 Virality Distribution (No Data)")

# Dashboard layout
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
