import React, { useState, useEffect } from 'react';
import BubblingFlask from '../components/BubblingFlask';
import { authAPI } from '../services/api';
import './Login.css';

// Simple local authentication (fallback if backend fails)
const localAuth = {
    signup: (username, password, email) => {
        const users = JSON.parse(localStorage.getItem('users') || '{}');
        if (users[username]) {
            throw new Error('Username already exists');
        }
        users[username] = { password, email, username };
        localStorage.setItem('users', JSON.stringify(users));
        return { username, email };
    },

    login: (username, password) => {
        const users = JSON.parse(localStorage.getItem('users') || '{}');
        const user = users[username];
        if (!user || user.password !== password) {
            throw new Error('Invalid credentials');
        }
        return { username: user.username, email: user.email };
    }
};

const Login = ({ onLoginSuccess }) => {
    const [mode, setMode] = useState('login');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [googleEmail, setGoogleEmail] = useState('');
    const [rememberMe, setRememberMe] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        // Load remembered credentials
        const remembered = localStorage.getItem('remembered_username');
        const rememberedPass = localStorage.getItem('remembered_password');
        if (remembered && rememberedPass) {
            setUsername(remembered);
            setPassword(atob(rememberedPass));
            setRememberMe(true);
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!username || !password) {
            setError('Please fill in all required fields');
            return;
        }

        setLoading(true);
        setError('');

        try {
            let result;
            if (mode === 'signup') {
                result = await authAPI.signup(username, password, email, rememberMe);
            } else {
                result = await authAPI.login(username, password, rememberMe);
            }

            setTimeout(() => {
                onLoginSuccess(result.user);
            }, 800);
        } catch (err) {
            setError(err.response?.data?.error || err.message || 'Authentication failed');
            setLoading(false);
        }
    };

    const handleGoogleLogin = async () => {
        if (!googleEmail) {
            setError('Please enter your email for Google login');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const result = await authAPI.googleLogin(googleEmail);
            setTimeout(() => {
                onLoginSuccess(result.user);
            }, 800);
        } catch (err) {
            setError('Google login failed');
            setLoading(false);
        }
    };

    const handleQuickLogin = async () => {
        setLoading(true);
        setError('');

        try {
            const result = await authAPI.googleLogin('demo@fosse.com');
            setTimeout(() => {
                onLoginSuccess(result.user);
            }, 800);
        } catch (err) {
            setError('Quick login failed');
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="login-page">
                <div className="login-container flex-center">
                    <BubblingFlask size={100} />
                </div>
            </div>
        );
    }

    return (
        <div className="login-page">
            <div className="login-container">
                <div className="login-card">
                    {/* Left Side - Login/Signup */}
                    <div className="login-left">
                        <div className="login-header">
                            <h1 className="login-title">Chemical Equipment</h1>
                            <h2 className="login-subtitle">Parameter Visualizer</h2>
                            <p className="login-description">FOSSE Program</p>
                        </div>

                        <div className="auth-tabs">
                            <button
                                className={`tab-button ${mode === 'login' ? 'active' : ''}`}
                                onClick={() => { setMode('login'); setError(''); }}
                            >
                                Login
                            </button>
                            <button
                                className={`tab-button ${mode === 'signup' ? 'active' : ''}`}
                                onClick={() => { setMode('signup'); setError(''); }}
                            >
                                Sign Up
                            </button>
                        </div>

                        <form className="login-form" onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label>Username</label>
                                <input
                                    type="text"
                                    className="form-input"
                                    placeholder="Enter username"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>Password</label>
                                <input
                                    type="password"
                                    className="form-input"
                                    placeholder="Enter password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </div>

                            {mode === 'signup' && (
                                <div className="form-group">
                                    <label>Email (optional)</label>
                                    <input
                                        type="email"
                                        className="form-input"
                                        placeholder="Enter email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                    />
                                </div>
                            )}

                            <label className="remember-me">
                                <input
                                    type="checkbox"
                                    checked={rememberMe}
                                    onChange={(e) => setRememberMe(e.target.checked)}
                                />
                                <span>Remember me</span>
                            </label>

                            {error && <div className="error-message">{error}</div>}

                            <button type="submit" className="submit-button">
                                {mode === 'login' ? 'Login' : 'Create Account'}
                            </button>
                        </form>
                    </div>

                    {/* Right Side - Google Login */}
                    <div className="login-right">
                        <div className="google-section">
                            <h3>Quick Access</h3>
                            <p className="google-description">Sign in with your Google account</p>

                            <div className="form-group">
                                <label>Email Address</label>
                                <input
                                    type="email"
                                    className="form-input"
                                    placeholder="your.email@example.com"
                                    value={googleEmail}
                                    onChange={(e) => setGoogleEmail(e.target.value)}
                                />
                            </div>

                            <button
                                className="google-button"
                                onClick={handleGoogleLogin}
                            >
                                <svg className="google-icon" viewBox="0 0 24 24" width="20" height="20">
                                    <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                                    <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                                    <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                                    <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                                </svg>
                                Sign in with Google
                            </button>

                            <div className="divider">
                                <span>OR</span>
                            </div>

                            <button
                                className="demo-button"
                                onClick={handleQuickLogin}
                            >
                                Quick Demo Login
                            </button>

                            <div className="security-note">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                                <span>Local authentication enabled</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;
