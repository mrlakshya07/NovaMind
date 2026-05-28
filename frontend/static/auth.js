/**
 * Authentication utilities for NovaMind
 * Handles session management, logout, and user verification
 */

class AuthManager {
    constructor() {
        this.currentUser = null;
        this.isAuthenticated = false;
    }

    /**
     * Check if user is authenticated
     */
    async checkAuth() {
        try {
            const response = await fetch('/api/auth/me', {
                method: 'GET',
                credentials: 'include'
            });

            if (response.status === 401) {
                this.isAuthenticated = false;
                this.redirectToLogin();
                return false;
            }

            if (response.ok) {
                const data = await response.json();
                if (data.success && data.user) {
                    this.currentUser = data.user;
                    this.isAuthenticated = true;
                    return true;
                }
            }
        } catch (error) {
            console.error('Auth check error:', error);
        }

        this.isAuthenticated = false;
        return false;
    }

    /**
     * Logout user
     */
    async logout() {
        try {
            const response = await fetch('/api/auth/logout', {
                method: 'POST',
                credentials: 'include'
            });

            if (response.ok) {
                this.currentUser = null;
                this.isAuthenticated = false;
                this.redirectToLogin();
                return true;
            }
        } catch (error) {
            console.error('Logout error:', error);
        }

        // Force redirect even if logout fails
        this.redirectToLogin();
        return false;
    }

    /**
     * Redirect to login page
     */
    redirectToLogin() {
        // Only redirect if not already on auth pages
        const currentPath = window.location.pathname;
        if (currentPath !== '/login' && currentPath !== '/signup') {
            window.location.href = '/login';
        }
    }

    /**
     * Get current user
     */
    getCurrentUser() {
        return this.currentUser;
    }

    /**
     * Get user ID
     */
    getUserId() {
        return this.currentUser?.user_id || null;
    }

    /**
     * Get user email
     */
    getUserEmail() {
        return this.currentUser?.email || null;
    }
}

// Create global auth manager instance
const authManager = new AuthManager();

// Check authentication on page load
document.addEventListener('DOMContentLoaded', async () => {
    const currentPath = window.location.pathname;

    // Skip auth check for public pages
    if (currentPath === '/login' || currentPath === '/signup') {
        return;
    }

    // Check auth for protected pages
    await authManager.checkAuth();
});

/**
 * Add logout button to navbar if it exists
 */
function setupLogoutButton() {
    const nav = document.querySelector('nav');
    if (!nav) return;

    // Check if logout button already exists
    if (document.getElementById('logoutBtn')) return;

    // Create logout button
    const logoutBtn = document.createElement('button');
    logoutBtn.id = 'logoutBtn';
    logoutBtn.className = 'nav-btn logout-btn';
    logoutBtn.innerHTML = '<i class="bx bx-log-out"></i> Logout';
    logoutBtn.style.marginLeft = '10px';
    logoutBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        await authManager.logout();
    });

    // Find nav-links and add logout button
    const navLinks = nav.querySelector('.nav-links');
    if (navLinks) {
        navLinks.appendChild(logoutBtn);
    }
}

// Setup logout button after DOM loads
document.addEventListener('DOMContentLoaded', setupLogoutButton);

/**
 * Helper to make authenticated API calls
 */
async function authenticatedFetch(url, options = {}) {
    const defaultOptions = {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    };

    const response = await fetch(url, {
        ...defaultOptions,
        ...options
    });

    // Handle 401 - user not authenticated
    if (response.status === 401) {
        console.warn('Unauthorized - redirecting to login');
        authManager.redirectToLogin();
        throw new Error('Unauthorized');
    }

    return response;
}