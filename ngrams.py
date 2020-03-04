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

# Try to launch graphical file selector, if this fails fallback to console
try:
	# Don't show blank tk root window
	root = tkinter.Tk()
	root.withdraw()	
	# Launch graphical file selector
	testFilePath = tkinter.filedialog.askopenfilename(initialdir = "./", title = "Select test data")
except _tkinter.TclError:
	# No graphical display available
	print("No display name and no $DISPLAY env variable")
	print("Using console")
	# https://github.com/tslight/treepick
	from treepick import pick
	## TODO: Should expand this to load all files selected instead of just the first
	testFilePath = pick(parent_path, False)[0]

f = open(testFilePath, "r", encoding="utf8")

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

if input("Connect to remote mongo server? y/n: ") == "y":
    mongoBaseUrl = "sorcerodb-9qoxc.mongodb.net/test"
    mongoUser = input("Enter mongoDB username: ")
    mongoPass = getpass.getpass("Enter mongoDB password: ")
    mongoUrl = "mongodb://" + urllib.parse.quote(mongoUser) + ":" + urllib.parse.quote(mongoPass) + "@" + mongoBaseUrl
    print("Inserting trigrams into MongoDB on " + mongoBaseUrl)
else:
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

# print(buckets)

for bucket in buckets:
    # print(buckets[bucket])
    # Sort bucket
    buckets[bucket] = OrderedDict(sorted(buckets[bucket].items(), key=lambda x: x[1], reverse=True))
    # Insert or replace mongo document
    db.buckets.replace_one({'_id': bucket}, buckets[bucket], upsert=True)


