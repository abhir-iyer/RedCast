import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load the datasets
df_main = pd.read_csv("data/reddit_data.csv")
df_sentiment = pd.read_csv("data/sentiment_data.csv")

# Merge datasets on 'title' to get sentiment columns
df = pd.merge(df_main, df_sentiment.drop_duplicates(subset="title"), on="title", how="left")

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])

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

# Visualization 3: Score vs Number of Comments by Sentiment
scatter_fig = px.scatter(
    df.dropna(subset=['sentiment_score']),
    x='score', y='num_comments',
    color='sentiment_score',
    title='💬 Score vs Number of Comments by Sentiment'
)

# Visualization 4: Sentiment Distribution
if 'sentiment' in df.columns and df['sentiment'].notna().sum() > 0:
    sentiment_dist_fig = px.histogram(
        df.dropna(subset=['sentiment']),
        x='sentiment',
        color='sentiment',
        title='🎭 Sentiment Distribution'
    )
else:
    sentiment_dist_fig = px.histogram(title="🎭 Sentiment Distribution (No Data Available)")

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "RedCast - Reddit Virality Dashboard"

# Layout with Tabs and Footer
app.layout = html.Div([
    html.H1("🧠 RedCast - Reddit Virality Dashboard", style={'textAlign': 'center'}),
    
    dcc.Tabs([
        dcc.Tab(label='Sentiment Over Time', children=[dcc.Graph(figure=sentiment_fig)]),
        dcc.Tab(label='Post Volume', children=[dcc.Graph(figure=volume_fig)]),
        dcc.Tab(label='Score vs Comments', children=[dcc.Graph(figure=scatter_fig)]),
        dcc.Tab(label='Sentiment Breakdown', children=[dcc.Graph(figure=sentiment_dist_fig)]),
    ]),

    html.Div(id="back-to-top-anchor"),

    html.Footer(
        "Built by Abhir Iyer",
        style={
            'textAlign': 'center',
            'padding': '1rem',
            'marginTop': '2rem',
            'fontSize': '14px',
            'color': '#aaa',
            'borderTop': '1px solid #eee',
        }
    )
])

if __name__ == '__main__':
    app.run(debug=True)
