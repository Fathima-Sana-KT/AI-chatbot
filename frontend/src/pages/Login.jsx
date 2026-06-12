import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Invalid email or password');
      }

      // Store JWT token and user info
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));

      navigate('/chat');
    } catch (err) {
      console.error('Login error:', err);
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className='login-container'>
      <h2>Login</h2>
      {error && <div style={{ color: 'red', marginBottom: '15px', fontWeight: 'bold' }}>{error}</div>}
      <form onSubmit={handleLogin}>
        <input 
          type='email' 
          placeholder='Email' 
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required 
        />
        <input 
          type='password' 
          placeholder='Password' 
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required 
        />
        <button type='submit' disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p>Don't have an account? <Link to='/signup'>Sign up</Link></p>
    </div>
  );
};

export default Login;

