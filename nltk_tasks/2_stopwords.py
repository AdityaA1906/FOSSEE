import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required packages
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Sample text
text = "This is a sample sentence showing off the stop words filtration."

print("--- Original Text ---")
print(text)

stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(text)

# Remove stop words
filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

print("\n--- Filtered Text (Stop Words Removed) ---")
print(filtered_sentence)
