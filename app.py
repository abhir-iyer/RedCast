import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load data
df_main = pd.read_csv("data/reddit_data.csv")
df_sentiment = pd.read_csv("data/sentiment_data.csv")

# Remove existing sentiment_score column to prevent merge conflict
if 'sentiment_score' in df_main.columns:
    df_main = df_main.drop(columns=['sentiment_score'])

# Merge safely
df = pd.merge(df_main, df_sentiment[['title', 'sentiment', 'sentiment_score']], on='title', how='left')
df['date'] = pd.to_datetime(df['date'])

# === Visualization 1: Sentiment over time ===
if 'sentiment_score' in df.columns:
    sentiment_fig = px.line(
        df.dropna(subset=['sentiment_score']).groupby('date')['sentiment_score'].mean().reset_index(),
        x='date', y='sentiment_score',
        title='📉 Average Sentiment Over Time'
    )
else:
    sentiment_fig = px.line(title="📉 Sentiment Data Not Available")

# === Visualization 2: Post volume over time ===
volume_fig = px.bar(
    df.groupby('date').size().reset_index(name='count'),
    x='date', y='count',
    title='📈 Post Volume Over Time'
)

# === Visualization 3: Score vs Comments by Sentiment Score ===
if 'sentiment_score' in df.columns:
    scatter_fig = px.scatter(
        df.dropna(subset=['sentiment_score']),
        x='score', y='num_comments',
        color='sentiment_score',
        title='💬 Score vs Number of Comments by Sentiment Score'
    )
else:
    scatter_fig = px.scatter(title="💬 Sentiment Data Not Available")

# === Visualization 4: Sentiment Distribution ===
if 'sentiment' in df.columns and df['sentiment'].notna().any():
    sentiment_dist_fig = px.histogram(
        df.dropna(subset=['sentiment']),
        x='sentiment',
        color='sentiment',
        title='🎭 Sentiment Distribution'
    )
else:
    sentiment_dist_fig = html.Div([
        html.H3("🎭 Sentiment Distribution"),
        html.P("No sentiment labels available to display.", style={'color': 'gray'})
    ])

# === Visualization 5: Virality Distribution ===
if 'viral' in df.columns and df['viral'].notna().any():
    viral_dist_fig = px.histogram(
        df.dropna(subset=['viral']),
        x='viral',
        color='viral',
        title='🔥 Virality Distribution'
    )
else:
    viral_dist_fig = html.Div([
        html.H3("🔥 Virality Distribution"),
        html.P("No virality data available to display.", style={'color': 'gray'})
    ])

# === Initialize App ===
app = dash.Dash(__name__)
app.title = "RedCast - Reddit Virality Dashboard"

# === Layout ===
app.layout = html.Div([
    html.H1("🧠 RedCast - Reddit Virality Dashboard", style={'textAlign': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Sentiment Over Time', children=[
            dcc.Graph(figure=sentiment_fig)
        ]),
        dcc.Tab(label='Post Volume', children=[
            dcc.Graph(figure=volume_fig)
        ]),
        dcc.Tab(label='Score vs Comments', children=[
            dcc.Graph(figure=scatter_fig)
        ]),
        dcc.Tab(label='Sentiment Breakdown', children=[
            dcc.Graph(figure=sentiment_dist_fig) if isinstance(sentiment_dist_fig, px.Figure)
            else sentiment_dist_fig
        ]),
        dcc.Tab(label='Virality Analysis', children=[
            dcc.Graph(figure=viral_dist_fig) if isinstance(viral_dist_fig, px.Figure)
            else viral_dist_fig
        ])
    ]),
    html.Div(id="back-to-top-anchor")
])

if __name__ == '__main__':
    app.run(debug=True)
