import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Load CSVs
df_main = pd.read_csv("data/reddit_data.csv")
df_sentiment = pd.read_csv("data/sentiment_data.csv")

# Convert dates
df_main['date'] = pd.to_datetime(df_main['date'], errors='coerce')

# Merge sentiment score and categorical sentiment into main DataFrame
df = pd.merge(df_main, df_sentiment[['title', 'sentiment', 'sentiment_score']], on='title', how='left')

# Fallback for missing columns
if 'viral' not in df.columns:
    df['viral'] = df['score'] > df['score'].median()

# ===============================
# PLOT 1: Average Sentiment Over Time
# ===============================
sentiment_fig = px.line(
    df.groupby('date')['sentiment_score'].mean().reset_index(),
    x='date', y='sentiment_score',
    title='📉 Average Sentiment Over Time'
)

# ===============================
# PLOT 2: Post Volume Over Time
# ===============================
volume_fig = px.bar(
    df.groupby('date').size().reset_index(name='count'),
    x='date', y='count',
    title='📈 Post Volume Over Time'
)

# ===============================
# PLOT 3: Score vs Comments by Sentiment
# ===============================
scatter_fig = px.scatter(
    df, x='score', y='num_comments',
    color='sentiment',
    title='💬 Score vs Number of Comments by Sentiment'
)

# ===============================
# PLOT 4: Sentiment Distribution
# ===============================
sentiment_dist_fig = px.histogram(
    df[df['sentiment'].notna()],
    x='sentiment',
    title='🎭 Sentiment Distribution',
    color='sentiment'
)

# ===============================
# PLOT 5: Virality Distribution
# ===============================
viral_dist_fig = px.histogram(
    df[df['viral'].notna()],
    x='viral',
    title='🔥 Virality Distribution',
    color='viral'
)

# ===============================
# DASH APP LAYOUT
# ===============================
app = dash.Dash(__name__)
app.title = "RedCast - Reddit Virality Dashboard"

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
            dcc.Graph(figure=sentiment_dist_fig)
        ]),
        dcc.Tab(label='Virality Analysis', children=[
            dcc.Graph(figure=viral_dist_fig)
        ]),
    ]),
    html.Div(id="back-to-top-anchor")
])

if __name__ == '__main__':
    app.run(debug=True)
