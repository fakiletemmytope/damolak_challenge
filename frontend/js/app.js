const API_BASE_URL = '/auth';

// State
let isLogin = true;

// DOM Elements
const authCard = document.querySelector('.auth-card');
const dashboardCard = document.querySelector('#dashboard');
const authTitle = document.querySelector('#auth-title');
const authSubtitle = document.querySelector('#auth-subtitle');
const loginForm = document.querySelector('#login-form');
const registerForm = document.querySelector('#register-form');
const toggleText = document.querySelector('#toggle-text');
const alertContainer = document.querySelector('#alert-container');
const alertMessage = document.querySelector('#alert-message');

// Dashboard Elements
const userEmailDisplay = document.querySelector('#user-email-display');
const userIdDisplay = document.querySelector('#user-id');
const userRoleDisplay = document.querySelector('#user-role');
const userStatusDisplay = document.querySelector('#user-status');
const logoutBtn = document.querySelector('#logout-btn');


// -------------------- UI TOGGLE --------------------

document.addEventListener('click', (e) => {
    if (e.target && e.target.id === 'toggle-auth') {
        e.preventDefault();
        isLogin = !isLogin;
        updateUI();
    }
});

function updateUI() {
    if (isLogin) {
        authTitle.textContent = 'Welcome Back';
        authSubtitle.textContent = 'Please enter your details to sign in.';
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');

        toggleText.innerHTML =
            `Don't have an account? <a href="#" id="toggle-auth">Sign up</a>`;
    } else {
        authTitle.textContent = 'Create Account';
        authSubtitle.textContent = 'Join us by creating a new account.';
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');

        toggleText.innerHTML =
            `Already have an account? <a href="#" id="toggle-auth">Sign in</a>`;
    }
}


// -------------------- ALERTS --------------------

function showAlert(message, type = 'error') {
    alertMessage.textContent = message;
    alertMessage.className = `alert alert-${type}`;
    alertContainer.classList.remove('hidden');
}

function hideAlert() {
    alertContainer.classList.add('hidden');
}


// -------------------- AUTH STORAGE --------------------

function saveAuth(token, user) {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user', JSON.stringify(user));
}

function clearAuth() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
}


// -------------------- SESSION CHECK --------------------

function checkAuth() {
    const token = localStorage.getItem('access_token');
    const user = JSON.parse(localStorage.getItem('user') || 'null');

    if (token && user) {
        showDashboard(user);
    }
}


// -------------------- DASHBOARD --------------------

function showDashboard(user) {
    authCard.classList.add('hidden');
    dashboardCard.classList.remove('hidden');

    userEmailDisplay.textContent = user.email;
    userIdDisplay.textContent = user.id;
    userRoleDisplay.textContent = user.role;
    userStatusDisplay.textContent = user.is_active ? 'Active' : 'Inactive';
}

function showAuth() {
    dashboardCard.classList.add('hidden');
    authCard.classList.remove('hidden');
}


// -------------------- LOGIN --------------------

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideAlert();

    const email = document.querySelector('#login-email').value;
    const password = document.querySelector('#login-password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            saveAuth(data.token, data.user_details);
            showDashboard(data.user_details);
        } else {
            showAlert(data.detail || 'Login failed');
        }
    } catch (err) {
        showAlert('Network error. Backend not reachable.');
    }
});


// -------------------- REGISTER --------------------

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideAlert();

    const email = document.querySelector('#register-email').value;
    const password = document.querySelector('#register-password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            showAlert('Account created! Please sign in.', 'success');
            setTimeout(() => {
                isLogin = true;
                updateUI();
            }, 1200);
        } else {
            showAlert(data.detail || 'Registration failed');
        }
    } catch (err) {
        showAlert('Network error. Backend not reachable.');
    }
});


// -------------------- LOGOUT --------------------

logoutBtn.addEventListener('click', async () => {
    const token = localStorage.getItem('access_token');

    try {
        if (token) {
            await fetch(`${API_BASE_URL}/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
        }
    } catch (err) {
        console.error('Logout failed:', err);
    }

    clearAuth();
    showAuth();
});


// -------------------- INIT --------------------

updateUI();
checkAuth();