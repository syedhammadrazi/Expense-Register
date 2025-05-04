const socket = io();
const form = document.getElementById('expense-form');
const desc = document.getElementById('description');
const amount = document.getElementById('amount');

form.addEventListener('submit', e => {
  e.preventDefault();
  socket.emit('new_expense', { description: desc.value, amount: amount.value });
  desc.value = '';
  amount.value = '';
});