import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [usernameError, setUsernameError] = useState('');

  useEffect(() => {
    setUsernameError('');
  }, [username]);

  async function handleRegister(e) {
    e.preventDefault();
    setUsernameError('');
    try {
      const res = await fetch('/api/register', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (!res.ok) {
        throw new Error('Registration failed');
      }

      const data = await res.json();

      if (data?.success) {
        navigate('/profile', { replace: true });
      } else if (data?.message === 'Username already exists') {
        setUsernameError('Username already exists');
        setPassword('');
      } else {
        alert(data?.message || 'Registration failed');
      }
    } catch (err) {
      alert('Registration failed');
    }
  }

  function handleUsernameChange(e) {
    setUsername(e.target.value);
    setUsernameError('');
  }

  function handlePasswordChange(e) {
    setPassword(e.target.value);
  }

  function handleTogglePassword() {
    setShowPassword((v) => !v);
  }

  return (
    <div className="auth-page">
      <div className="login-container">
      <form onSubmit={handleRegister}>
        <h2 className="login-title">Register</h2>

        <div className="login-socials">
          <a href={'/auth/google'} className="social google" title="Sign up with Google">
            <i className="fab fa-google"></i>
          </a>
          <a href={'/auth/apple'} className="social apple" title="Sign up with Apple">
            <i className="fab fa-apple"></i>
          </a>
          <a href={'/auth/github'} className="social git-hub" title="Sign up with GitHub">
            <i className="fab fa-github"></i>
          </a>
        </div>

        <input className="login-input" type="text" placeholder="Username" required value={username} onChange={handleUsernameChange} />
        {usernameError && (
          <div className="input-error">{usernameError}</div>
        )}
        <div className="password-wrapper">
          <input className="login-input" type={showPassword ? 'text' : 'password'} placeholder="Password" required value={password} onChange={handlePasswordChange} />
          <button className="toggle-eye" type="button" aria-label={showPassword ? 'Hide password' : 'Show password'} onClick={handleTogglePassword}>
            <i className={!showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'}></i>
          </button>
        </div>
        <button type="submit" className="login-button">Create account</button>
      </form>
      </div>
    </div>
  );
}

export default Register;


