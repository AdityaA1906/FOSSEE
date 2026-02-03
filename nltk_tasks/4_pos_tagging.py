import nltk
from nltk.tokenize import word_tokenize

# Download required packages
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Sample text (News Snippet)
text = "Apple Inc. is planning to open a new store in Mumbai tomorrow."

print("--- Original Text ---")
print(text)

words = word_tokenize(text)
pos_tags = nltk.pos_tag(words)

print("\n--- POS Tags ---")
# Print list of tuples
print(pos_tags)

# Pretty print analysis
print("\n--- Analysis ---")
for word, tag in pos_tags:
    print(f"{word}: {tag}")
