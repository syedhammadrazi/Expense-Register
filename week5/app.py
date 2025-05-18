from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)
DATABASE = 'expenses.db'

# --- DB Helpers ---
def open_db():
    return sqlite3.connect(DATABASE)

def close_db(conn):
    conn.close()

def init_db():
    conn = open_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        description TEXT,
        amount REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    close_db(conn)

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

# --- WebSocket Events ---
@socketio.on('connect')
def handle_connect(sid):
    print(f'Client connected: {sid}')

    conn = open_db()
    expenses = conn.execute('SELECT id, description, amount, created_at FROM expenses ORDER BY id DESC').fetchall()
    close_db(conn)

    data = [{
        'id': exp[0],
        'description': exp[1],
        'amount': exp[2],
        'created_at': exp[3]
    } for exp in expenses]

    emit('load_expenses', data)

@socketio.on('new_expense')
def handle_expense(data):
    print(f"New expense received: {data}")
    conn = open_db()
    conn.execute(
        'INSERT INTO expenses (description, amount) VALUES (?, ?)',
        (data['description'], data['amount'])
    )
    conn.commit()
    new_exp = conn.execute(
        'SELECT id, description, amount, created_at FROM expenses ORDER BY id DESC LIMIT 1'
    ).fetchone()
    close_db(conn)

    expense = {
        'id': new_exp[0],
        'description': new_exp[1],
        'amount': new_exp[2],
        'created_at': new_exp[3]
    }

    socketio.emit('expense_added', expense)

@socketio.on('delete_expense')
def handle_delete_expense(data):
    expense_id = data.get('id')
    conn = open_db()
    conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    close_db(conn)
    print(f"Deleted expense ID {expense_id}")
    socketio.emit('expense_deleted', {'id': expense_id})

# --- Run App ---
if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
