const socket = io();

const form = document.getElementById('expense-form');
const desc = document.getElementById('description');
const amount = document.getElementById('amount');
const list = document.getElementById('expense-list');

// Submit a new expense
form.addEventListener('submit', e => {
  e.preventDefault();
  socket.emit('new_expense', {
    description: desc.value,
    amount: parseFloat(amount.value).toFixed(2)
  });
  desc.value = '';
  amount.value = '';
});

// Load all existing expenses (sent once on connect)
socket.on('load_expenses', expenses => {
  list.innerHTML = ''; // clear existing list
  for (const exp of expenses) {
    const item = document.createElement('li');
    item.textContent = `${exp.description} - $${exp.amount}`;
    list.appendChild(item);
  }
});

// Display newly added expenses
socket.on('expense_added', data => {
  const item = document.createElement('li');
  item.textContent = `${data.description} - $${data.amount}`;
  list.prepend(item);
});
