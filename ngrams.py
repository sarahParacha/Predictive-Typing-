# Learned from: http://www.albertauyeung.com/post/generating-ngrams-python/
import nltk, re, string, collections
from nltk.util import ngrams 

s = "Natural-language processing (NLP) is an area of computer science and artificial intelligence concerned with the interactions between computers and human (natural) languages.";
print(s)
tokenized = s.split()
Trigrams = ngrams(tokenized,3)
listOfTrigrams = list(Trigrams)
# printing only 10 ngrams
print(listOfTrigrams[:10])
print(len(listOfTrigrams))


