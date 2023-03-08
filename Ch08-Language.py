"""
Chapter 08: Language

In this chapter we will discuss the differences between language and math that make language algorithms difficult.

We will then build a space insertion algorithm that can take any text in any language and insert spacees wherever they are missing.

After that we will build a phase completion algorithm that can imitate the style of a writer and find the most fitting next word in a phrase.


We will be relying on two new tools:

    1. List Comprehensions: enable us to quickly generate lists using  the logic of loops and iterations.
    2. Corpus: A body of text that will "teach" our algorithm the language and style we want it to use.

"""

# PAGE 150: Why are Algorithms hard?
"""

# Numbers are easy for computers to work with because there are predictable and precise patterns and systems and rules which is very well suited to the rules based and systems nature of computers and algorithms.

# In contrast, although language does have a certain set of rules, language in practice is not very predictable and the sytems and rules are regularly broken and changed. Alot of language is just memorizing large amounts of words and patterns... There aren't clear patterns that a computer can predict if it doesn't already have something stored in memory. 

# This lack of systemization and logic in language is what makes it hard for computers to work with language.
"""

# PAGE 150: Space Insertion:

# Below is imperfectly digitized text:
text = "The oneperfectly divine thing, the oneglimpse of God's paradisegiven on earth, is to fight a losingbattle - and notlose it"

# First we teach our algorithm some English words:
word_list = ['The','one','perfectly','divine']

# We will create and manipulate lists using comprehensions:
word_list_copy = [word for word in word_list]

# How to use a word list to find something:
has_n = [word for word in word_list if 'n' in word]
print('Words with an n: ' + str(has_n))


# Let's use python's re module to access text manipulation tools:
import re
locs = list(set([(m.start(),m.end()) for word in word_list for m in re.finditer(word,text)]))
# The above code creates a variable called locs that will contain the locations in the text of every word in our word list
# We use "for word in word_list" to iterate over every word in our word_list.
# We call "re.fintiter()" to find the selected word in our text and returns a list of every location where the word occurs.
print(locs) # Prints a list of ordered pairs called a tuple.


# PAGE 152: Dealing with Compound Words:
"""
In our algorithm we can make sure to check if the invalid word is actually a valid word that is just a compound word like the word "butterfly"
"""


# PAGE 153: Checking Between Existing Spaces for Potential Words

spacestarts = [m.start() for m in re.finditer(' ',text)]
spacestarts.append(-1)
spacestarts.append(len(text))
spacestarts.sort()

# It will be useful to have another list that records the locations of the first character of each potential word:
spacestarts_affine = [ss+1 for ss in spacestarts]
spacestarts_affine.sort()

# Now we get the substrings that are between two spaces:
between_spaces = [(spacestarts[k] + 1,spacestarts[k + 1]) for k in range(0,len(spacestarts) - 1)]

# Now consider all of the potential words that are between spaces and find the ones that are not valid(not in the word_list):
between_spaces_notvalid = [loc for loc in between_spaces if text[loc[0]:loc[1]] not in word_list]
print(str(between_spaces_notvalid))

# With the code above some of the words marked as invalid are actually valid. The reason they are marked invalid is because they aren't on the word list.


"""
PAGE 154: Using Imported Corpus to Check for Valid Words:

"""

import nltk
nltk.download('brown')

from nltk.corpus import brown
wordlist = set(brown.words())
word_list = list(wordlist)


# Before using this wordlist, we should cleanup punctuation marks that are considered words in this imported wordlist:
word_list = [word.replace('*','') for word in word_list]
word_list = [word.replace('[','') for word in word_list]
word_list = [word.replace(']','') for word in word_list]
word_list = [word.replace('?','') for word in word_list]
word_list = [word.replace('.','') for word in word_list]
word_list = [word.replace('+','') for word in word_list]
word_list = [word.replace('/','') for word in word_list]
word_list = [word.replace(';','') for word in word_list]
word_list = [word.replace(':','') for word in word_list]
word_list = [word.replace(',','') for word in word_list]
word_list = [word.replace(')','') for word in word_list]
word_list = [word.replace('(','') for word in word_list]
word_list.remove('')

# Let's rerun the check for innvalid words with our new imported word_list:
between_spaces_notvalid = [loc for loc in between_spaces if text[loc[0]:loc[1]] not in word_list]
print(str(between_spaces_notvalid))

# PAGE 155: Now we check in our word list for words that could be combined to form those invalid words: Begin with words that start just after a space:
partial_words = [loc for loc in locs if loc[0] in spacestarts_affine and loc[1] not in spacestarts]

# Next, let's look for words that end with a space. These could be the second half of an invalid word. To find them, we make some small changes to the previous logic:
partial_words_end = [loc for loc in locs if loc[0] not in spacestarts_affine and loc[1] in spacestarts]

"""
PAGE 156: Finding First and Second Halves of Potential Words:
Let's start by inserting a space into oneperfectly
"""

# Define a variable that stores the location of oneperfectly in our text:
loc = between_spaces_notvalid[0]

# List comprehension that finds the ending location of every valid word that begins at the same location as oneperfectly:
endsofbeginnings = [loc2[1] for loc2 in partial_words if loc2[0] == loc[0] and (loc2[1] - loc[0]) > 1]

# List comprehension that will find the beginning location of every valid word that ends at the same place as oneperfectly:
beginningsofends = [loc2[0] for loc2 in partial_words_end  if loc2[1] == loc[1] and (loc2[1] - loc[0]) > 1]

# Now we just need to find whether any locations are contained in both endsofbeginnings and beginningsofends. If there are, that means that our invalid word is indeed a combination of two valid words without a space. We use the intersection() function to find all elements that are shared by both lists:
pivot = list(set(endsofbeginnings).intersection(beginningsofends))

import numpy as np
pivot = np.min(pivot) # Take the smallest element of the list

# Next write one line that replaces our invalid word with the two valid component words plus a space:
textnew = text
textnew = textnew.replace(text[loc[0]:loc[1]],text[loc[0]:pivot]+' '+text[pivot:loc[1]])

# If we print textnew, we see the words put together:
print(textnew)

# PAGE 157: Function Putting all this code together:

import re
import numpy as np
import nltk
nltk.download('brown')

from nltk.corpus import brown
wordlist = set(brown.words())
word_list = list(wordlist)

word_list = [word.replace('*','') for word in word_list]
word_list = [word.replace('[','') for word in word_list]
word_list = [word.replace(']','') for word in word_list]
word_list = [word.replace('?','') for word in word_list]
word_list = [word.replace('.','') for word in word_list]
word_list = [word.replace('+','') for word in word_list]
word_list = [word.replace('/','') for word in word_list]
word_list = [word.replace(';','') for word in word_list]
word_list = [word.replace(':','') for word in word_list]
word_list = [word.replace(',','') for word in word_list]
word_list = [word.replace(')','') for word in word_list]
word_list = [word.replace('(','') for word in word_list]
word_list.remove('')


def insertspaces(text,word_list):

    locs = list(set([(m.start(),m.end()) for word in word_list for m in re.finditer(word,text)]))
    spacestarts = [m.start() for m in re.finditer(' ', text)]
    spacestarts.append(-1)
    spacestarts.append(len(text))
    spacestarts.sort()
    spacestarts_affine = [ss + 1 for ss in spacestarts]
    spacestarts_affine.sort()
    partial_words = [loc for loc in locs if loc[0] in spacestarts_affine and loc[1] not in spacestarts]
    partial_words_end = [loc for loc in locs if loc[0] not in spacestarts_affine and loc[1] in spacestarts]
    between_spaces = [(spacestarts[k] + 1,spacestarts[k+1]) for k in range(0,len(spacestarts) - 1)]
    between_spaces_notvalid = [loc for loc in between_spaces if text[loc[0]:loc[1]] not in word_list]
    textnew = text
    for loc in between_spaces_notvalid:
        endsofbeginnings = [loc2[1] for loc2 in partial_words if loc2[0] == loc[0] and (loc2[1] - loc[0]) > 1]
        beginningsofends = [loc2[0] for loc2 in partial_words_end  if loc2[1] == loc[1] and (loc2[1] - loc[0]) > 1]
        pivot = list(set(endsofbeginnings).intersection(beginningsofends))
        if(len(pivot) > 0):
            pivot = np.min(pivot)
            textnew = textnew.replace(text[loc[0]:loc[1]],text[loc[0]:pivot]+' '+text[pivot:loc[1]])
    textnew = textnew.replace(' ',' ')
    return(textnew)

# Now we can define any text and call our function as follows:

text = "The oneperfectly divine thing, the oneglimpse of God's paradisegiven on earth, is to fight a losingbattle - and notlose it."
print(insertspaces(text,word_list))



"""
PAGE 159: Phrase Completion

To add phrase completion similar to google search engines do is supposedly simple according to this book... We use a corpus. But we are also interested in how the words fit together.

In order to factor in how words fit together, we compile a list of n-grams from our corpus. An n-gram is simply a collection of n words that appear together.

"""

# Tokenizing and Getting N-grams
# Tokenizing means splitting a string into its component words, ignoring punctuation.

import requests
file = requests.get('http://www.bradfordtuckfield.com/shakespeare.txt')
file = file.text
text = file.replace('\n', '')

import nltk
nltk.download('punkt')
from nltk.util import ngrams
token = nltk.word_tokenize(text)
bigrams = ngrams(token,2)
trigrams = ngrams(token,3)
fourgrams = ngrams(token,4)
fivegrams = ngrams(token,5)
grams = [ngrams(token,2),ngrams(token,3),ngrams(token,4),ngrams(token,5)]

"""
PAGE 160: Our Strategy

When a user types in a search, we check how many words are in their search. In other words, a user enters an n-gram and we determine what n is. Then we add to the n meaning we search for an n+1 gram.

However not all suggestions are equally as good.So we can just suggest the n+1 gram that appears most frequently in our corpus.
"""

import requests
file = requests.get('http://www.bradfordtuckfield.com/shakespeare.txt')
file = file.text
text = file.replace('\n', '')
import nltk
from nltk.util import ngrams
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter

def search_suggestion(search_term, text):
    token = nltk.word_tokenize(text)
    bigrams = ngrams(token,2)
    trigrams = ngrams(token,3)
    fourgrams = ngrams(token,4)
    fivegrams = ngrams(token,5)
    grams = [bigrams,trigrams,fourgrams,fivegrams]
    split_term = tuple(search_term.split(' '))
    search_term_length = len(search_term.split(' '))
    counted_grams = Counter(grams[search_term_length-1])
    combined_term = "No suggested searches"
    matching_terms = [element for element in list(counted_grams.items()) if element[0][:-1] == tuple(split_term)]
    if(len(matching_terms) > 0):
        frequencies = [item[1] for item in matching_terms]
        maximum_frequency = np.max(frequencies)
        highest_frequency_term = [item[0] for item in matching_terms if item[1] == maximum_frequency][0]
        combined_term = ' '.join(highest_frequency_term)
    return(combined_term)

# Let's call our function:

print(search_suggestion('life is a', text))
