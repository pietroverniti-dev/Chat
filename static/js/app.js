// --- NAVIGAZIONE ---
function showLogin() {
    document.getElementById('loginView').classList.remove('hidden');
    document.getElementById('registerView').classList.add('hidden');
    document.getElementById('boardView').classList.remove('flex');
    document.getElementById('boardView').style.display = 'none';
}

function showRegister() {
    document.getElementById('loginView').classList.add('hidden');
    document.getElementById('registerView').classList.remove('hidden');
}

function showBoard(email) {
    document.getElementById('loginView').classList.add('hidden');
    document.getElementById('registerView').classList.add('hidden');
    const board = document.getElementById('boardView');
    board.classList.remove('hidden');
    board.style.display = 'flex';
    document.getElementById('userHeader').textContent = `Bacheca di ${email}`;
    loadMessages();
}

// --- API CALLS ---
async function apiCall(url, method, body) {
    const options = {
        method: method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (body) options.body = JSON.stringify(body);
    
    const res = await fetch(url, options);
    const data = await res.json();
    
    if (!res.ok) throw new Error(data.error || "Errore sconosciuto");
    return data;
}

// --- FUNZIONI DI APP ---

async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPass').value;
    try {
        const data = await apiCall('/api/login', 'POST', { email, password });
        showBoard(data.user.email);
    } catch (e) { alert(e.message); }
}

async function register() {
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPass').value;
    try {
        await apiCall('/api/register', 'POST', { email, password });
        alert("Registrazione completata! Ora accedi.");
        showLogin();
    } catch (e) { alert(e.message); }
}

async function logout() {
    await apiCall('/api/logout', 'POST');
    showLogin();
}

async function loadMessages() {
    try {
        const data = await apiCall('/api/messages', 'GET');
        const list = document.getElementById('messageList');
        list.innerHTML = '';
        
        data.items.forEach(msg => {
            const div = document.createElement('div');
            div.className = `message ${msg.is_mine ? 'mine' : 'others'}`;
            
            // Cestino (solo se il messaggio è mio)
            const deleteBtn = msg.is_mine 
                ? `<button class="delete-btn" onclick="deleteMessage('${msg.id}')"><i class="fa-solid fa-trash"></i></button>` 
                : '';

            div.innerHTML = `
                ${deleteBtn}
                <div class="msg-meta">
                    <span class="msg-author">${msg.author}</span>
                </div>
                <div class="msg-text">${msg.text}</div>
                <div class="msg-date">${msg.date}</div>
            `;
            list.appendChild(div);
        });
        
        // Scroll to bottom
        list.scrollTop = list.scrollHeight;
    } catch (e) {
        console.error(e);
        if(e.message === "Non autenticato") showLogin();
    }
}

async function postMessage() {
    const input = document.getElementById('msgInput');
    const text = input.value.trim();
    if (!text) return;

    try {
        await apiCall('/api/messages', 'POST', { text });
        input.value = '';
        loadMessages();
    } catch (e) { alert(e.message); }
}

async function deleteMessage(id) {
    if(!confirm("Vuoi eliminare questo messaggio?")) return;
    try {
        await apiCall(`/api/messages/${id}/delete`, 'DELETE');
        loadMessages();
    } catch (e) { alert(e.message); }
}

function handleEnter(e) {
    if (e.key === 'Enter') postMessage();
}

// --- INIZIALIZZAZIONE ---

// Check iniziale se l'utente è già loggato
loadMessages().then(() => {
    // Nota: qui non abbiamo l'email dell'utente salvata localmente, 
    // potremmo fare una chiamata '/api/me' per recuperarla, 
    // ma per ora mostriamo semplicemente la bacheca.
    document.getElementById('boardView').style.display = 'flex';
    document.getElementById('loginView').classList.add('hidden');
}).catch(() => showLogin());

// Auto-refresh ogni 5 secondi
setInterval(() => {
    if(document.getElementById('boardView').style.display !== 'none') {
        loadMessages();
    }
}, 5000);