#----------------------------------------------------------------------------
#A short program illustrating the generation of ngrams using python libraries.
#To run the program, ensure that the nltk library is installed. To do so the
#following command needs to be run: pip3 install nltk (for Python 3).
#Website Resource: http://www.albertauyeung.com/post/generating-ngrams-python/
#----------------------------------------------------------------------------
import nltk, re, string, collections
from nltk.util import ngrams 

s = "This is a test sentence used to demonstrate the ngrams generated using the python library named nltk used for natural language processing.";
print(s)
tokenized = s.split()
Trigrams = ngrams(tokenized,3)
listOfTrigrams = list(Trigrams)
print(listOfTrigrams[:10])
print(len(listOfTrigrams))


