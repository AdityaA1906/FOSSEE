import nltk

# Download required packages
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# Sample text
text = "NLTK is a powerful library for natural language processing. It makes Python programming easy for NLP tasks."

print("--- Original Text ---")
print(text)
print("\n--- Sentence Tokenization ---")
sentences = nltk.sent_tokenize(text)
for i, sent in enumerate(sentences):
    print(f"{i+1}: {sent}")

print("\n--- Word Tokenization ---")
words = nltk.word_tokenize(text)
print(words)
