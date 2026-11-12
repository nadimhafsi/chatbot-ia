const form = document.querySelector('#chat-form');
const input = document.querySelector('#message');
const messages = document.querySelector('#messages');
const statusLine = document.querySelector('#status');
const send = document.querySelector('#send');
const clear = document.querySelector('#clear');
let history = [];

function addBubble(text, role) {
  const bubble = document.createElement('div');
  bubble.className = `bubble ${role}`;
  bubble.textContent = text; // textContent évite l'injection HTML
  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
}

clear.addEventListener('click', () => {
  history = [];
  messages.replaceChildren();
  addBubble('Bonjour ! Nouvelle conversation. Comment puis-je vous aider ?', 'assistant');
  statusLine.textContent = '';
  input.focus();
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  input.value = '';
  addBubble(message, 'user');
  send.disabled = true;
  statusLine.textContent = 'L’assistant rédige une réponse…';
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history: history.slice(-12) })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Erreur inconnue.');
    addBubble(data.reply, 'assistant');
    history.push({ role: 'user', content: message }, { role: 'assistant', content: data.reply });
    history = history.slice(-12);
    statusLine.textContent = '';
  } catch (error) {
    statusLine.textContent = `Erreur : ${error.message}`;
  } finally {
    send.disabled = false;
    input.focus();
  }
});
