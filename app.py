import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load preprocessed data
df = pd.read_csv("data/reddit_data.csv", parse_dates=["date"])

# Base charts
sentiment_fig = px.line(
    df.groupby("date")["sentiment_score"].mean().reset_index(),
    x="date", y="sentiment_score",
    title="📈 Average Sentiment Over Time",
    labels={"sentiment_score": "Avg Sentiment", "date": "Date"}
)

volume = df.groupby("date").size().reset_index(name="count")
volume_fig = px.line(
    volume, x="date", y="count",
    title="📊 Post Volume Over Time",
    labels={"count": "Number of Posts", "date": "Date"}
)

top_posts = df.nlargest(10, 'score')[['title', 'score']]
top_posts_fig = px.bar(
    top_posts,
    x='score', y='title',
    orientation='h',
    title='🏅 Top 10 Posts by Score (Upvotes)',
    labels={'score': 'Upvotes', 'title': 'Post Title'},
)
top_posts_fig.update_layout(yaxis={'categoryorder': 'total ascending'})

sentiment_dist_fig = px.histogram(
    df, x='sentiment',
    title='💬 Sentiment Distribution of Posts',
    labels={'sentiment': 'Sentiment Category'},
)

scatter_fig = px.scatter(
    df, x='num_comments', y='score',
    color='viral',
    title='🧪 Comments vs Score by Virality',
    labels={'num_comments': 'Comments', 'score': 'Score'},
)

daily_stats = df.groupby('date').agg({
    'sentiment_score': 'mean',
    'title': 'count'
}).reset_index()
daily_sentiment_volume = px.scatter(
    daily_stats,
    x='date', y='title',
    size='title',
    color='sentiment_score',
    color_continuous_scale='RdYlGn',
    title='📆 Post Volume Colored by Avg Sentiment',
    labels={'title': 'Post Count', 'sentiment_score': 'Avg Sentiment'},
)

# Create Dash app
app = dash.Dash(__name__)
server = app.server  # required for deployment

app.layout = html.Div([
    html.H1("🧠 RedCast - Reddit Virality Dashboard", style={'textAlign': 'center'}),

    dcc.Graph(figure=sentiment_fig),
    dcc.Graph(figure=volume_fig),
    dcc.Graph(figure=top_posts_fig),
    dcc.Graph(figure=sentiment_dist_fig),
    dcc.Graph(figure=scatter_fig),
    dcc.Graph(figure=daily_sentiment_volume),
])

if __name__ == "__main__":
    app.run(debug=True)