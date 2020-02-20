import nltk, re, string, collections
from nltk.util import ngrams 

s = "Natural-language processing (NLP) is an area of computer science and artificial intelligence concerned with the interactionsbetween computers and human (natural) languages.";
print(s)
tokenized = s.split()
Trigrams = ngrams(tokenized,3)
listOfTrigrams = list(Trigrams)
print(listOfTrigrams[:10])
print(len(listOfTrigrams))


