import string, pymongo, re
from collections import OrderedDict

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

s = "This is a sentence"

# if input("Connect to remote mongo server? y/n: ") == "y":
#     mongoBaseUrl = "sorcerodb-9qoxc.mongodb.net/test"
#     mongoUser = input("Enter mongoDB username: ")
#     mongoPass = getpass.getpass("Enter mongoDB password: ")
#     mongoUrl = "mongodb://" + urllib.parse.quote(mongoUser) + ":" + urllib.parse.quote(mongoPass) + "@" + mongoBaseUrl
#     print("Inserting trigrams into MongoDB on " + mongoBaseUrl)
# else:
#     mongoUrl = "localhost"
#     print("Inserting trigrams into MongoDB on " + mongoUrl)

mongoUrl = "localhost"
print("Inserting trigrams into MongoDB on " + mongoUrl)

mongoClient = pymongo.MongoClient(mongoUrl)
db = mongoClient.ngrams

buckets = {'a': {}, 'b': {}, 'c': {}, 'd': {}, 'e': {}, 'f': {}, 'g': {}, 'h': {}, 'i': {}, 'j': {}, 'k': {}, 'l': {}, 'm': {},
            'n': {}, 'o': {}, 'p': {}, 'q': {}, 'r': {}, 's': {}, 't': {}, 'u': {}, 'v': {}, 'w': {}, 'x': {}, 'y': {}, 'z': {}}

# Get word count
words = stripText(s).split()
for word in words:
    c = word[0]
    if word in buckets[c]:
        buckets[c][word] = buckets[c][word] + 1
    else:
        buckets[c][word] = 1

for bucket in buckets:
    # Sort bucket
    buckets[bucket] = OrderedDict(sorted(buckets[bucket].items(), key=lambda x: x[1], reverse=True))
    # Insert or replace mongo document
    db.buckets.replace_one({'_id': bucket}, buckets[bucket], upsert=True)