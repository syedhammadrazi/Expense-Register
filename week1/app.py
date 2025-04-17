# Week 1: Basic Flask Setup
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return 'Hello World from Flask!'

@socketio.on('connect')
def test_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, debug=True)