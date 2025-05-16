from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)
DATABASE = 'expenses.db'

# --- Helper Functions ---
def open_db():
    return sqlite3.connect(DATABASE)

def close_db(conn):
    conn.close()

def init_db():
    conn = open_db()
    conn.execute('CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, description TEXT, amount REAL)')
    conn.commit()
    close_db(conn)

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

# --- WebSocket Events ---
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    conn = open_db()
    expenses = conn.execute('SELECT description, amount FROM expenses ORDER BY id DESC').fetchall()
    close_db(conn)
    data = [{'description': exp[0], 'amount': exp[1]} for exp in expenses]
    emit('load_expenses', data)

@socketio.on('new_expense')
def handle_expense(data):
    print(f"New expense received: {data}")
    conn = open_db()
    conn.execute('INSERT INTO expenses (description, amount) VALUES (?, ?)', (data['description'], data['amount']))
    conn.commit()
    close_db(conn)
    socketio.emit('expense_added', data)

# --- Run App ---
if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
