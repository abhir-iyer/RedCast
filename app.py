import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load datasets
df_main = pd.read_csv("data/reddit_data.csv")
df_sentiment = pd.read_csv("data/sentiment_data.csv")

# Merge on title (if available), else skip
if 'date' in df_sentiment.columns:
    df_sentiment['date'] = pd.to_datetime(df_sentiment['date'])
    df_main['date'] = pd.to_datetime(df_main['date'])
    df = pd.merge(df_main, df_sentiment, on='date', how='left')
else:
    df = df_main
    df['date'] = pd.to_datetime(df['date'])

app = dash.Dash(__name__)
app.title = "RedCast - Reddit Virality Dashboard"

def fallback_figure(title_text="⚠️ No Data Available"):
    fig = go.Figure()
    fig.update_layout(
        title=title_text,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[dict(text="No data to display", x=0.5, y=0.5,
                          showarrow=False, font=dict(size=20))]
    )
    return fig

# Visualization 1: Sentiment over time
try:
    sentiment_fig = px.line(
        df.groupby('date')['sentiment_score'].mean().reset_index(),
        x='date', y='sentiment_score',
        title='📉 Average Sentiment Over Time'
    )
except Exception:
    sentiment_fig = fallback_figure("📉 Average Sentiment Over Time")

# Visualization 2: Post volume over time
try:
    volume_fig = px.bar(
        df.groupby('date').size().reset_index(name='count'),
        x='date', y='count',
        title='📈 Post Volume Over Time'
    )
except Exception:
    volume_fig = fallback_figure("📈 Post Volume Over Time")

# Visualization 3: Score vs Comments
try:
    scatter_fig = px.scatter(df, x='score', y='num_comments',
                             color='sentiment_score',
                             title='💬 Score vs Number of Comments by Sentiment')
except Exception:
    scatter_fig = fallback_figure("💬 Score vs Comments")

# Visualization 4: Sentiment distribution
try:
    sentiment_dist_fig = px.histogram(
        df, x='sentiment', color='sentiment',
        title='🎭 Sentiment Distribution'
    )
except Exception:
    sentiment_dist_fig = fallback_figure("🎭 Sentiment Distribution")

# Visualization 5: Virality distribution
try:
    viral_dist_fig = px.histogram(
        df, x='viral', color='viral',
        title='🔥 Virality Distribution'
    )
except Exception:
    viral_dist_fig = fallback_figure("🔥 Virality Distribution")

# Layout
app.layout = html.Div([
    html.H1("🧠 RedCast - Reddit Virality Dashboard", style={'textAlign': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Sentiment Over Time', children=[dcc.Graph(figure=sentiment_fig)]),
        dcc.Tab(label='Post Volume', children=[dcc.Graph(figure=volume_fig)]),
        dcc.Tab(label='Score vs Comments', children=[dcc.Graph(figure=scatter_fig)]),
        dcc.Tab(label='Sentiment Breakdown', children=[dcc.Graph(figure=sentiment_dist_fig)]),
        dcc.Tab(label='Virality Analysis', children=[dcc.Graph(figure=viral_dist_fig)]),
    ]),
    html.Div(id="back-to-top-anchor")
])

if __name__ == '__main__':
    app.run(debug=True)
