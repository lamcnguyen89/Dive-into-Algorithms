# Useless comment2
"""
Chapter 11: Forging Ahead

This chapter is about 3 things: 
    1. Doing more with algorithms
    2. Using them in better and faster ways
    3. Solving their deepest mysteries

We will buiild a simple chatbot, discuss some of the hardest problems in the world, and discuss some of the deepest mysteries of the world of algorithms.
"""

# Page 202: Doing More with Algorithms:
    # Information Compresssion 
    # Cryptography for secure online communications
    # Parallel Distributed Computing
    # Quantum Computing


""" Page 203: Building a Chatbot"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
import numpy as np
import nltk, string
nltk.download('punkt')

# After importing modules, the next step is text normalization, the process of converting natural language text into standardized substrings which allows easy comparison between superficially different texts. To do this we:
    # Remove punctuation
    # Make everything lower case
    # Tokenization: converts a text string to a list of coherent substrings
    # Remove stems or gets rid of the derivations of words so they are pure

query = 'I want to learn about geometry algorithms'
queryLowerCase = query.lower()
remove_punctuation_map = dict((ord(char),None) for char in string.punctuation)
queryLowerCaseNoPunc= queryLowerCase.translate(remove_punctuation_map)
querytokenizedLowerCaseNoPunc= nltk.word_tokenize(queryLowerCaseNoPunc)
print(querytokenizedLowerCaseNoPunc)

# Remove Derivations of a word so that jump and jumper are the same to an algorithm:
stemmer = nltk.stem.porter.PorterStemmer()
def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]



# Lets create a function with all these normalization steps:
def normalize(text):

    remove_punctuation_map = dict((ord(char),None) for char in string.punctuation)

    stemmer = nltk.stem.porter.PorterStemmer()
    def stem_tokens(tokens):
        return [stemmer.stem(item) for item in tokens]
    
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

"""
PAGE 204: Text Vectorization
 Now we need to learn how to convert texts to numeric vectors in order to make it easier to make quantitative comparisons between numbers and vectors versus numbers and words.
"""

# TFIDF Vectorization:
vctrz = TfidfVectorizer(ngram_range = (1,1),tokenizer = normalize, stop_words = 'english')

# Now let's configure what the chatbot will be able to talk about:
alldocuments = [
    'Chapter 1. The algorithmic approach to problem solving.',
    'Chapter 2. Algorithms in History',
    'Chapter 3. Optimization like Gradient Descent and Gradient Ascent',
    'Chapter 4. Sorting and Searching',
    'Chapter 5. Pure Mathematics',
    'Chapter 6. More Advanced Optimization',
    'Chapter 7. Geometry',
    'Chapter 8. Language',
    'Chapter 10. Machine Learning',
    'Chapter 11. Where to Go and what to study next'
]

# We will now fit our TFIDF vectorizer to these chapter descriptions:
vctrz.fit(alldocuments)

# Now we create TFIDF Vectors for our chapter descriptions for a new query asking for a chapter about sorting and searching:
query = 'I want to read about how to search for items'
tfidf_reports = vctrz.transform(alldocuments).todense()
tfidf_question = vctrz.transform([query]).todense()

# Now we have converted our chapter descriptions into TFIDF Vectors, concluding that the chapter the user is looking for is the one whose description vector most closely matches the query vector.

"""
PAGE 206: Vector Similarity

How do we decide whether any two vectors are similar or not? We use a method called cosine similarity. If the cosine calculation is larger then zero, then the vectors are similar
"""

# Code to calculate Cosine Similarities:
row_similarities = [1 - spatial.distance.cosine(tfidf_reports[x],tfidf_question) for x in range(len(tfidf_reports))]


"""
PAGE 207: Simple Chatbot Function:
"""

def chatbot(query,allreports):
    clf = TfidfVectorizer(ngram_range = (1,1),tokenizer = normalize, stop_words = 'english')
    clf.fit(allreports)
    tfidf_reports = clf.transform(allreports).todense()
    tfidf_question = clf.transform([query]).todense()
    row_similarities = [1 - spatial.distance.cosine(tfidf_reports[x],tfidf_question) for x in range(len(tfidf_reports))]
    return(allreports[np.argmax(row_similarities)])
  
# Call function:
print(chatbot('Please tell me which chapter I can go to if I want to read about mathematics algorithms',alldocuments))