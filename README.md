# 🧠 RedCast – Reddit Virality Dashboard

RedCast is a lightweight, interactive dashboard built with Plotly Dash to analyze the virality of Reddit posts from r/AskReddit using time series trends, sentiment analysis, and post metadata.

## 📂 Project Structure

```
RedCast/
│
├── app.py                  # Main Dash application
├── requirements.txt        # Python dependencies
├── render.yaml             # (Optional) Render deployment configuration
├── data/
│   └── reddit_data.csv     # Reddit posts with sentiment and metadata
└── assets/                 # (Optional) Custom CSS or favicon
```

## 🚀 Features

- 📈 Sentiment trend over time (BERT-based sentiment scoring)
- 📊 Post volume visualization
- 📊 Average upvotes and comment engagement by day
- 📌 Virality breakdown of posts
- 🔍 Fully interactive and mobile responsive

## 🛠️ Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/RedCast.git
cd RedCast
```

2. Create virtual environment (optional):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
python app.py
```

5. Open in your browser:
```
http://127.0.0.1:8050/
```

## ☁️ Deploying on Render

- Upload the repo
- Ensure `requirements.txt` and `render.yaml` exist
- Set build command: `pip install -r requirements.txt`
- Start command: `python app.py`

## 🧠 Credits

- Reddit API via PRAW
- Hugging Face Transformers (DistilBERT)
- Plotly Dash
