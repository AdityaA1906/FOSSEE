import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download required packages
nltk.download('vader_lexicon', quiet=True)

# Sample text
texts = [
    "I love using NLTK, it's amazing and very useful!",
    "The movie was terrible and boring.",
    "It was an okay experience, nothing special."
]

sia = SentimentIntensityAnalyzer()

print("--- Sentiment Analysis (VADER) ---")
for text in texts:
    scores = sia.polarity_scores(text)
    print(f"\nText: {text}")
    print(f"Scores: {scores}")
    
    if scores['compound'] >= 0.05:
        print("Verdict: Positive")
    elif scores['compound'] <= -0.05:
        print("Verdict: Negative")
    else:
        print("Verdict: Neutral")
