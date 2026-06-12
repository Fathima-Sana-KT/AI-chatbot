import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Signup = () => {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  
  const handleSignup = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Signup failed');
      }

      setSuccess('Account created successfully! Redirecting to login...');
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (err) {
      console.error('Signup error:', err);
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className='signup-container'>
      <h2>Sign Up</h2>
      {error && <div style={{ color: 'red', marginBottom: '15px', fontWeight: 'bold' }}>{error}</div>}
      {success && <div style={{ color: 'green', marginBottom: '15px', fontWeight: 'bold' }}>{success}</div>}
      <form onSubmit={handleSignup}>
        <input 
          type='text' 
          placeholder='Name' 
          value={name}
          onChange={(e) => setName(e.target.value)}
          required 
        />
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
          {loading ? 'Creating Account...' : 'Sign Up'}
        </button>
      </form>
      <p>Already have an account? <Link to='/'>Login</Link></p>
    </div>
  );
};

export default Signup;

