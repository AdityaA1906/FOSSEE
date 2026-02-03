import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download required packages
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Initialize Stemmer and Lemmatizer
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# Sample words
words = ["running", "flies", "happily", "better", "cats"]

print(f"{'Word':<15} {'Stemming':<15} {'Lemmatization':<15}")
print("-" * 45)

for w in words:
    stem = ps.stem(w)
    lemma = lemmatizer.lemmatize(w, pos='v') # 'v' for verb usually gives interesting changes
    print(f"{w:<15} {stem:<15} {lemma:<15}")
