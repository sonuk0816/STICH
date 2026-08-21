/* =========================================================
   CONFIG
========================================================= */
const BRAND_NAME = "Stitch Culture";
const GREETING = `Hello! I am Stitch, your ${BRAND_NAME} virtual assistant. I can help you find products, check stock, or understand our policies. How can I assist you today?`;

/* =========================================================
   SEND MESSAGE FLOW (Connected to Python)
========================================================= */
function handleSendMessage() {
  const text = chatInput.value.trim();
  if (text === '') return;

  // 1. Show the user's message instantly
  appendMessage(text, 'user');
  chatInput.value = '';
  chatInput.focus();

  // 2. Show a "typing..." indicator
  showTypingIndicator();

  // 3. Make the REAL call to your FastAPI backend
  fetch('http://127.0.0.1:8000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text })
  })
  .then(res => res.json())
  .then(data => {
    removeTypingIndicator();
    appendMessage(data.reply, 'bot'); // Processing Genzz !!!
  })
  .catch(err => {
    removeTypingIndicator();
    appendMessage("Sorry, my server is offline right now.", 'bot');
    console.error(err);
  });
}

/* =========================================================
   ELEMENT REFERENCES
========================================================= */
const chatToggle = document.getElementById('chat-toggle');
const chatWindow = document.getElementById('chat-window');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');

let chatHasOpenedBefore = false;

/* =========================================================
   OPEN / CLOSE TOGGLE
========================================================= */
chatToggle.addEventListener('click', () => {
  const isOpen = chatWindow.classList.toggle('open');
  chatToggle.classList.toggle('open', isOpen);

  // Show the automatic greeting the first time the chat is opened
  if (isOpen && !chatHasOpenedBefore) {
    chatHasOpenedBefore = true;
    appendMessage(GREETING, 'bot');
  }

  if (isOpen) {
    chatInput.focus();
  }
});

/* =========================================================
   MESSAGE RENDERING HELPERS
========================================================= */
function appendMessage(text, sender) {
  const msg = document.createElement('div');
  msg.classList.add('msg', sender);
  msg.textContent = text;
  chatMessages.appendChild(msg);
  scrollToBottom();
}

function showTypingIndicator() {
  const indicator = document.createElement('div');
  indicator.classList.add('typing-indicator');
  indicator.id = 'typing-indicator';
  indicator.innerHTML = '<span></span><span></span><span></span>';
  chatMessages.appendChild(indicator);
  scrollToBottom();
}

function removeTypingIndicator() {
  const indicator = document.getElementById('typing-indicator');
  if (indicator) indicator.remove();
}

function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatSend.addEventListener('click', handleSendMessage);

chatInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    handleSendMessage();
  }
});

/* FAQ ACCORDION */
document.querySelectorAll('.faq-question').forEach(button => {
  button.addEventListener('click', () => {
    const item = button.closest('.faq-item');
    const isActive = item.classList.contains('active');

    // Close all other open FAQ items for a clean accordion behavior
    document.querySelectorAll('.faq-item').forEach(el => el.classList.remove('active'));

    if (!isActive) {
      item.classList.add('active');
    }
  });
});

/*CONTACT FORM (frontend-only placeholder handling)*/
const contactForm = document.querySelector('.contact-form');
if(contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thank you! Your message has been received. We will get back to you shortly.');
    contactForm.reset();
  });
}

/*MOBILE NAV TOGGLE (basic show/hide)*/
const navToggle = document.querySelector('.nav-toggle');
const navEl = document.querySelector('nav');
if(navToggle && navEl) {
  navToggle.addEventListener('click', () => {
    const isShown = navEl.style.display === 'block';
    navEl.style.display = isShown ? 'none' : 'block';
    if (!isShown) {
      navEl.style.position = 'absolute';
      navEl.style.top = '72px';
      navEl.style.left = '0';
      navEl.style.right = '0';
      navEl.style.background = '#fff';
      navEl.style.borderBottom = '1px solid var(--color-border)';
      navEl.style.padding = '20px 32px';
      navEl.querySelector('ul').style.flexDirection = 'column';
      navEl.querySelector('ul').style.gap = '20px';
    }
  });
}