import pymongo, getpass, urllib.parse
from flask import Flask, render_template
from flask_socketio import SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

if input("Connect to remote mongo server? y/n: ") == "y":
    mongoBaseUrl = "sorcerodb-9qoxc.mongodb.net/test"
    mongoUser = input("Enter mongoDB username: ")
    mongoPass = getpass.getpass("Enter mongoDB password: ")
    mongoUrl = "mongodb+srv://" + urllib.parse.quote(mongoUser) + ":" + urllib.parse.quote(mongoPass) + "@" + mongoBaseUrl
    print("Connecting to  MongoDB on " + mongoBaseUrl)
else:
    mongoUrl = "localhost"
    print("Connecting to MongoDB on " + mongoUrl)

try:
	timeoutDelay = 10000
	mongoClient = pymongo.MongoClient(mongoUrl, timeoutDelay)
	# Send request to check connection
	mongoClient.server_info()
except pymongo.errors.ServerSelectionTimeoutError as err:
	print(err)
	print("Server selection timed out (" + timeoutDelay + " ms)")
	exit()

print("Connected to mongoDB.")
db = mongoClient.ngrams


mongoClient = pymongo.MongoClient(mongoUrl)
db = mongoClient.ngrams
buckets = db.buckets

@app.route('/')
def serve():
    return render_template('search.html.jinja')

@socketio.on('textInput')
def textInput(json):
    text = json['data']
    bucket = buckets.find_one({'_id': {"$regex": "^"+text}})
    if bucket is not None:
        return list(bucket)[1:]

if __name__ == '__main__':
    socketio.run(app)
