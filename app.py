import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load and merge datasets
df_main = pd.read_csv("data/reddit_data.csv")
df_sentiment = pd.read_csv("data/sentiment_data.csv")

# Merge on 'date' only
df = pd.merge(df_main, df_sentiment, on='date', how='left')
df['date'] = pd.to_datetime(df['date'])

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "RedCast - Reddit Virality Dashboard"

# Visualization 1: Average sentiment over time
sentiment_fig = px.line(
    df.groupby('date')['sentiment_score'].mean().reset_index(),
    x='date', y='sentiment_score',
    title='📉 Average Sentiment Over Time'
)

# Visualization 2: Post volume over time
volume_fig = px.bar(
    df.groupby('date').size().reset_index(name='count'),
    x='date', y='count',
    title='📈 Post Volume Over Time'
)

# Visualization 3: Score vs Comments colored by sentiment score
scatter_fig = px.scatter(
    df, x='score', y='num_comments',
    color='sentiment_score',
    title='💬 Score vs Number of Comments by Sentiment'
)

# Visualization 4: Sentiment category distribution
sentiment_dist_fig = px.histogram(
    df, x='sentiment',
    title='🎭 Sentiment Category Distribution',
    color='sentiment'
)

# Visualization 5: Virality breakdown
viral_dist_fig = px.histogram(
    df, x='viral',
    title='🔥 Virality Distribution',
    color='viral'
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
    html.Div(id="back-to-top-anchor")
])

if __name__ == '__main__':
    app.run(debug=True)
