from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('new_expense')
def handle_expense(data):
    print(f"New expense received: {data}")
    
if __name__ == '__main__':
    socketio.run(app, debug=True)
