#----------------------------------------------------------------------------
#   A short program illustrating the generation of ngrams using python libraries.
#   To run the program, please install all dependencies in requirements.txt
#   -> pip install -r requirements.txt
#----------------------------------------------------------------------------
import sys, string, collections
import pymongo, getpass, urllib.parse
from collections import OrderedDict
from pprint import pprint
from nltk.util import ngrams

def main():
    # Read data
    testString = readFile(getFilename())
    s = parseText(testString)

    # Generate ngrams
    tokenized = s.split()
    Trigrams = ngrams(tokenized,3)
    listOfTrigrams = list(Trigrams)

    print(s[:2000])
    print(listOfTrigrams[:10])
    print(len(listOfTrigrams))

    buckets = bucketize(listOfTrigrams)

    # Store buckets in MongoDB
    mongoClient = connectToMongo()
    db = mongoClient.ngrams
    print("Storing buckets in MongoDB, please wait...")
    for bucket in buckets:
        db.buckets.replace_one({'_id': bucket}, buckets[bucket], upsert=True)
    print("Done.")

#-------------------------#
### Component Functions ###
#-------------------------#

# Take a filename and returns the content. Exits on failure
def readFile(filename, enc="utf8"):
    f = open(filename, "r", encoding=enc)
    if f.mode != 'r': 
        print("Failed to open test file")
        raise SystemExit

    return f.read()

# Displays file chooser and returns chosen file name
def getFilename():
    # Graphical file chooser may fail
    try:
        import tkinter
        # Tk requires a root window
        root = tkinter.Tk()
        # But we don't want to show it
        root.withdraw()
        return tkinter.filedialog.askopenfilename(initialdir = "./", title = "Select test data")
    except ImportError as err:
        print(err)
        print("Import error: is tk installed?")
        print("Falling back to CLI.")
        return input("Enter test data path: ")
    # Probably not in a graphical environment
    except _tkinter.TclError as err:
        print(err)
        print("No display name or $DISPLAY env variable found.")
        print()
        print("Falling back to CLI")
        print()
        return input("Enter test data path: ")

# Basic text parser
## TODO: Replace with more sophisticated parser
def parseText(t):
    # Strip non-ascii characters
    t = t.encode('ascii', 'ignore').decode()
    # Strip punctuation
    t = t.translate(str.maketrans('', '', string.punctuation))
    # Strip newlines
    t = t.replace('\n', ' ')
    # Convert to lowercase
    t = t.lower()
    return t    

# Generates buckets of tuples sorted by frequency
def bucketize(listOfTuples):
    buckets = {}
    for _tuple in listOfTuples:
        bucket = _tuple[0]    # Each first word becomes a bucket
        tupleString = " ".join(_tuple)
        if bucket not in buckets:    # Create bucket if it doesn't exist
            buckets[bucket] = {}
        if tupleString in buckets[bucket]:  # If string exists increase count
            buckets[bucket][tupleString] = buckets[bucket][tupleString] + 1
        else:
            buckets[bucket][tupleString] = 1

    # Sort buckets by frequency, descending
    for bucket in buckets:
        buckets[bucket] = OrderedDict(sorted(buckets[bucket].items(), key=lambda x: x[1], reverse=True))

    return buckets

# Select remote or local MongoDB server and return connection
# Blocks, and exits on failure
def connectToMongo():
    if input("Connect to remote MongoDB server? y/n: ") == "y":
        mongoBaseUrl = "sorcerodb-9qoxc.mongodb.net/test"
        mongoUser = input("Enter MongoDB username: ")
        mongoPass = getpass.getpass("Enter MongoDB password: ")
        # Generate connection string
        mongoUrl = "mongodb+srv://" + urllib.parse.quote(mongoUser) + ":" + urllib.parse.quote(mongoPass) + "@" + mongoBaseUrl
        print("Connecting to MongoDB on " + mongoBaseUrl)
    else:
        mongoUrl = "localhost"
        print("Connecting to MongoDB on " + mongoUrl)
    
    try:
        timeoutDelay = 10000
        mongoClient = pymongo.MongoClient(mongoUrl, serverSelectionTimeoutMS=timeoutDelay)
        mongoClient.server_info()   # Send request to check connection
        print("Connected to MongoDB.")
        return mongoClient
    except pymongo.errors.ServerSelectionTimeoutError as err:
	    print(err)
	    print("Server selection timed out (" + str(timeoutDelay) + " ms)")
	    exit()

# Run main
main()