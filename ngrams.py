#----------------------------------------------------------------------------
#A short program illustrating the generation of ngrams using python libraries.
#To run the program, ensure that the nltk library is installed. To do so the
#following command needs to be run: pip3 install nltk (for Python 3).
#----------------------------------------------------------------------------
import re, string, collections, pymongo, getpass, urllib.parse
import tkinter
from collections import OrderedDict
from pprint import pprint
from nltk.util import ngrams 

def stripText(t):
    # Strip non-ascii characters
    t = re.sub(r'[^\x00-\x7F]+',' ', t)
    # Strip punctuation
    t = t.translate(str.maketrans('', '', string.punctuation))
    # Strip newlines
    t = t.replace('\n', ' ')
    # Convert to lowercase
    t = t.lower()
    return t

# Don't show blank root window
root = tkinter.Tk()
root.withdraw()
#
testFilePath = tkinter.filedialog.askopenfilename(initialdir = "./", title = "Select test data")

f = open(testFilePath, "r")

if f.mode != 'r': 
    print("Failed to open test file")
    raise SystemExit

testString = f.read()
s = stripText(testString)

print(s)
tokenized = s.split()
Trigrams = ngrams(tokenized,3)
listOfTrigrams = list(Trigrams)
print(listOfTrigrams[:10])
print(len(listOfTrigrams))

mongoUrl = "localhost"
print("Inserting trigrams into MongoDB on " + mongoUrl)

mongoClient = pymongo.MongoClient(mongoUrl)
db = mongoClient.ngrams

buckets = {}

for trigram in listOfTrigrams:
    bucket = trigram[0]
    trigramString = " ".join(trigram)
    if bucket not in buckets:
        buckets[bucket] = {}
    if trigramString in buckets[bucket]:
        buckets[bucket][trigramString] = buckets[bucket][trigramString] + 1
    else:
        buckets[bucket][trigramString] = 1

print(buckets)

for bucket in buckets:
    print(buckets[bucket])
    # Sort bucket
    buckets[bucket] = OrderedDict(sorted(buckets[bucket].items(), key=lambda x: x[1], reverse=True))
    # Insert or replace mongo document
    db.buckets.replace_one({'_id': bucket}, buckets[bucket], upsert=True)


