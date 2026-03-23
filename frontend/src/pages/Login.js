import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../api';

function Login({ onLogin }) {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(formData.username, formData.password);
      const { access_token, refresh_token, user } = response.data;

      onLogin({
        access_token,
        refresh_token,
        role: user?.role || 'user',
      });

      navigate('/');
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div style={{ textAlign: 'center', marginBottom: '0.5rem' }}>
          <span style={{ fontSize: '4rem', display: 'block', marginBottom: '1rem', filter: 'drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1))' }}>🔐</span>
        </div>
        <h1 className="login-title">VendorVerify</h1>
        <h2>Sign in to your account</h2>

        {error && (
          <div className="alert alert-danger" style={{ marginBottom: '1.5rem' }}>
            <span>⚠️</span> {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">
              <span>👤</span> Username
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter your username"
              required
              disabled={loading}
              autoComplete="username"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">
              <span>🔑</span> Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
              disabled={loading}
              autoComplete="current-password"
            />
          </div>

          <button 
            type="submit" 
            className="btn btn-primary btn-block" 
            disabled={loading}
            style={{
              background: loading ? 'var(--slate-400)' : 'var(--gradient-ocean)',
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.7 : 1
            }}
          >
            {loading ? (
              <>
                <span className="spinner" style={{ width: '20px', height: '20px', borderWidth: '2px', marginRight: '0.5rem', display: 'inline-block', verticalAlign: 'middle' }}></span>
                Signing in...
              </>
            ) : (
              <>
                <span>🚀</span> Sign In
              </>
            )}
          </button>
        </form>

        <div className="login-footer">
          <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--slate-600)' }}>
            <span style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>💡 Demo Credentials</span>
            Username: <strong style={{ color: 'var(--primary-600)' }}>admin</strong> / Password: <strong style={{ color: 'var(--primary-600)' }}>Admin@123</strong>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
