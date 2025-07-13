import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Signup = () => {
  const navigate = useNavigate();
  
  const handleSignup = (e) => {
    e.preventDefault();
    navigate('/chat');
  };
  
  return (
    <div className='signup-container'>
      <h2>Sign Up</h2>
      <form onSubmit={handleSignup}>
        <input type='text' placeholder='Name' required />
        <input type='email' placeholder='Email' required />
        <input type='password' placeholder='Password' required />
        <button type='submit'>Sign Up</button>
      </form>
      <p>Already have an account? <Link to='/'>Login</Link></p>
    </div>
  );z
};

export default Signup;
