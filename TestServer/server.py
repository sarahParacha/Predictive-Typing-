from flask import Flask, render_template
from flask_socketio import SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def serve():
    return render_template('search.html.jinja')

@socketio.on('textInput')
def textInput(json):
    print('Received text input: ' + str(json))


if __name__ == '__main__':
    socketio.run(app)