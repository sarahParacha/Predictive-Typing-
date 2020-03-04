import pymongo, getpass, urllib.parse
from flask import Flask, render_template
from flask_socketio import SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

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

# Select MongoDB server
if input("Connect to remote mongo server? y/n: ") == "y":
    mongoBaseUrl = "sorcerodb-9qoxc.mongodb.net/test"
    mongoUser = input("Enter mongoDB username: ")
    mongoPass = getpass.getpass("Enter mongoDB password: ")
    mongoUrl = "mongodb+srv://" + urllib.parse.quote(mongoUser) + ":" + urllib.parse.quote(mongoPass) + "@" + mongoBaseUrl
    print("Connecting to  MongoDB on " + mongoBaseUrl)
else:
    mongoUrl = "localhost"
    print("Connecting to MongoDB on " + mongoUrl)

# Attempt to connect to MongoDB
try:
	timeoutDelay = 10000
	mongoClient = pymongo.MongoClient(mongoUrl, serverSelectionTimeoutMS=timeoutDelay)
	# Send request to check connection
	mongoClient.server_info()
except pymongo.errors.ServerSelectionTimeoutError as err:
	print(err)
	print("Server selection timed out (" + timeoutDelay + " ms)")
	exit()
print("Connected to mongoDB.")

# Select buckets document
mongoClient = pymongo.MongoClient(mongoUrl)
db = mongoClient.ngrams
buckets = db.buckets

print()
print("Listening...")

# Server search page on /
@app.route('/')
def serve():
    return render_template('search.html.jinja')

# Handle text input from search page
@socketio.on('textInput')
def textInput(json):
    text = parseText(json['data'])
    bucket = buckets.find_one({'_id': {"$regex": "^"+text}})    # Search for bucket _id beginning with input
    if bucket is not None:
        # First item is the bucket _id, so skip it. Only return first 20 items
        return list(bucket)[1:21]

if __name__ == '__main__':
    socketio.run(app)
