const API_BASE_URL = '/auth';

// State management
let isLogin = true;

// DOM Elements
const authCard = document.querySelector('.auth-card');
const dashboardCard = document.querySelector('#dashboard');
const authTitle = document.querySelector('#auth-title');
const authSubtitle = document.querySelector('#auth-subtitle');
const loginForm = document.querySelector('#login-form');
const registerForm = document.querySelector('#register-form');
const toggleAuth = document.querySelector('#toggle-auth');
const toggleText = document.querySelector('#toggle-text');
const alertContainer = document.querySelector('#alert-container');
const alertMessage = document.querySelector('#alert-message');

// Dashboard Elements
const userEmailDisplay = document.querySelector('#user-email-display');
const userIdDisplay = document.querySelector('#user-id');
const userRoleDisplay = document.querySelector('#user-role');
const userStatusDisplay = document.querySelector('#user-status');
const logoutBtn = document.querySelector('#logout-btn');

// Toggle between Login and Register
toggleAuth.addEventListener('click', (e) => {
    e.preventDefault();
    isLogin = !isLogin;
    
    if (isLogin) {
        authTitle.textContent = 'Welcome Back';
        authSubtitle.textContent = 'Please enter your details to sign in.';
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        toggleText.innerHTML = 'Don\'t have an account? <a href="#" id="toggle-auth">Sign up</a>';
    } else {
        authTitle.textContent = 'Create Account';
        authSubtitle.textContent = 'Join us by creating a new account.';
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        toggleText.innerHTML = 'Already have an account? <a href="#" id="toggle-auth">Sign in</a>';
    }
    
    // Re-attach listener because we replaced innerHTML
    document.querySelector('#toggle-auth').addEventListener('click', (e) => {
        e.preventDefault();
        toggleAuth.click();
    });
    
    hideAlert();
});

// Helper: Show Alert
function showAlert(message, type = 'error') {
    alertMessage.textContent = message;
    alertMessage.className = `alert alert-${type}`;
    alertContainer.classList.remove('hidden');
}

// Helper: Hide Alert
function hideAlert() {
    alertContainer.classList.add('hidden');
}

// Helper: Save Auth Data
function saveAuth(token, user) {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user', JSON.stringify(user));
}

// Helper: Clear Auth Data
function clearAuth() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
}

// Helper: Check Auth on Load
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const user = JSON.parse(localStorage.getItem('user'));
    
    if (token && user) {
        showDashboard(user);
    }
}

// Show Dashboard
function showDashboard(user) {
    authCard.classList.add('hidden');
    dashboardCard.classList.remove('hidden');
    userEmailDisplay.textContent = user.email;
    userIdDisplay.textContent = user.id;
    userRoleDisplay.textContent = user.role;
    userStatusDisplay.textContent = user.is_active ? 'Active' : 'Inactive';
}

// Show Auth Card
function showAuth() {
    dashboardCard.classList.add('hidden');
    authCard.classList.remove('hidden');
}

// Handle Login
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
        showAlert('Network error. Is the backend running?');
    }
});

// Handle Registration
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
            // Switch to login view
            setTimeout(() => toggleAuth.click(), 1500);
        } else {
            showAlert(data.detail || 'Registration failed');
        }
    } catch (err) {
        showAlert('Network error. Is the backend running?');
    }
});

// Handle Logout
logoutBtn.addEventListener('click', async () => {
    // Note: The backend logout expects a refresh_token cookie and blacklists it.
    // In a real app, we'd call the logout endpoint.
    try {
        await fetch(`${API_BASE_URL}/logout`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
    } catch (err) {
        console.error('Logout request failed', err);
    }
    
    clearAuth();
    showAuth();
});

// Init
checkAuth();
