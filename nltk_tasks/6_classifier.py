import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required packages
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

# 1. Prepare small sample dataset (Text, Category)
data = [
    ("I love this sandwich.", "pos"),
    ("This is an amazing place!", "pos"),
    ("I feel very good about these beers.", "pos"),
    ("This is my best work.", "pos"),
    ("What an awesome view", "pos"),
    ("I do not like this restaurant", "neg"),
    ("I am tired of this stuff.", "neg"),
    ("I can't deal with this", "neg"),
    ("He is my sworn enemy!", "neg"),
    ("My boss is horrible.", "neg")
]

# 2. Preprocess: Extract features
all_words = []
stop_words = set(stopwords.words('english'))

for (text, cat) in data:
    words = word_tokenize(text)
    # Remove stop words and punctuation for better features
    clean_words = [w.lower() for w in words if w.isalnum() and w.lower() not in stop_words]
    all_words.extend(clean_words)

# Frequency distribution of top words
word_features = list(nltk.FreqDist(all_words).keys())[:20]

def document_features(document):
    document_words = set(document.lower().split())
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

# 3. Create feature sets
featuresets = [(document_features(d), c) for (d,c) in data]

# 4. Train Naive Bayes Classifier
classifier = nltk.NaiveBayesClassifier.train(featuresets)

print("--- Naive Bayes Classifier ---")
print("Full Accuracy on Training Data:", nltk.classify.accuracy(classifier, featuresets))
classifier.show_most_informative_features(5)

# 5. Test on new sentence
test_sentence = "I feel amazing"
print(f"\nTest Sentence: '{test_sentence}'")
test_features = document_features(test_sentence)
print("Prediction:", classifier.classify(test_features))
