const socket = io();

const form = document.getElementById('expense-form');
const desc = document.getElementById('description');
const amount = document.getElementById('amount');
const list = document.getElementById('expense-list');

// Submit new expense
form.addEventListener('submit', e => {
  e.preventDefault();

  const description = desc.value.trim();
  const amountValue = parseFloat(amount.value);

  if (!description || isNaN(amountValue) || amountValue <= 0) {
    alert("Please enter a valid description and a positive amount.");
    return;
  }

  socket.emit('new_expense', {
    description: description,
    amount: amountValue.toFixed(2)
  });

  desc.value = '';
  amount.value = '';
});

// Load all expenses once on connect
socket.on('load_expenses', expenses => {
  list.innerHTML = '';
  for (const exp of expenses) {
    addExpenseToList(exp);
  }
});

// Add a newly submitted expense
socket.on('expense_added', expense => {
  addExpenseToList(expense, true);
});

// Remove an expense from the UI when deleted
socket.on('expense_deleted', data => {
  const item = document.getElementById(`expense-${data.id}`);
  if (item) item.remove();
});

// Add an expense to the UI
function addExpenseToList(exp, prepend = false) {
  const item = document.createElement('li');
  item.id = `expense-${exp.id}`;

  const formattedAmount = Number(exp.amount).toLocaleString(undefined, { minimumFractionDigits: 2 });
  const timestamp = new Date(exp.created_at).toLocaleString();

  item.textContent = `${exp.description} - $${formattedAmount} (${timestamp})`;

  // Add a delete button (anyone can delete in this version)
  const btn = document.createElement('button');
  btn.textContent = 'Delete';
  btn.style.marginLeft = '10px';
  btn.onclick = () => {
    socket.emit('delete_expense', { id: exp.id });
  };
  item.appendChild(btn);

  if (prepend) {
    list.prepend(item);
  } else {
    list.appendChild(item);
  }
}
