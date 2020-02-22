#----------------------------------------------------------------------------
#A short program illustrating the generation of ngrams using python libraries.
#To run the program, ensure that the nltk library is installed. To do so the
#following command needs to be run: pip3 install nltk (for Python 3).
#Website Resource: http://www.albertauyeung.com/post/generating-ngrams-python/
#----------------------------------------------------------------------------
import re, string, collections
from collections import OrderedDict
from pprint import pprint
from pymongo import MongoClient
from nltk.util import ngrams 

testFilePath = "Test Data/gettysburg.txt"

f = open(testFilePath, "r")

if f.mode != 'r': 
    print("Failed to open test file")
    raise SystemExit

testString = f.read()
# Strip non-ascii characters
s = re.sub(r'[^\x00-\x7F]+',' ', testString)
# Strip punctuation
s = s.translate(str.maketrans('', '', string.punctuation))
# Strip newlines
s = s.replace('\n', ' ')
# Convert to lowercase
s = s.lower()

print(s)
tokenized = s.split()
Trigrams = ngrams(tokenized,3)
listOfTrigrams = list(Trigrams)
print(listOfTrigrams[:10])
print(len(listOfTrigrams))

print("Inserting trigrams to MongoDB@localhost")
mongoClient = MongoClient("localhost")
db = mongoClient.ngrams

buckets = {'a': {}, 'b': {}, 'c': {}, 'd': {}, 'e': {}, 'f': {}, 'g': {}, 'h': {}, 'i': {}, 'j': {}, 'k': {}, 'l': {}, 'm': {},
            'n': {}, 'o': {}, 'p': {}, 'q': {}, 'r': {}, 's': {}, 't': {}, 'u': {}, 'v': {}, 'w': {}, 'x': {}, 'y': {}, 'z': {}}

# Get word count
words = s.split()
for word in words:
    c = word[0]
    if word in buckets[c]:
        buckets[c][word] = buckets[c][word] + 1
    else:
        buckets[c][word] = 1

for bucket in buckets:
    # Sort bucket
    buckets[bucket] = OrderedDict(sorted(buckets[bucket].items(), key=lambda x: x[1], reverse=True))
    # Set mongo item _id
    buckets[bucket]['_id'] = bucket
    db.buckets.replace_one({'_id': bucket}, buckets[bucket], upsert=True)

pprint(buckets)
