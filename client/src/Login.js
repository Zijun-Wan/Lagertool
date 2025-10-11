import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import './Login.css'; 

function Login() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    const success = searchParams.get('success');

    if (success === 'false') {
      alert('Login failed. Please try again.');
      navigate('/login', { replace: true });
    } else if (success === 'true') {
      navigate('/profile', { replace: true });
    }
  }, [searchParams, navigate]);

  async function handleLogin(e) {
    e.preventDefault(); // stops page from reloading

    try {
      const res = await fetch('api/login', {
        method: 'POST',
        credentials: 'include', // Include cookies for session management
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: username,
          password: password
        })
      });
      
      if (!res.ok) {
        throw new Error('Login failed');
      }

      const data = await res.json();

      if (data?.success) {
        navigate('/items', { replace: true });
      } else if (data?.message === 'User not found') {
        alert('Username not found.');
      } else if (data?.message === 'Incorrect password') {
        alert('Incorrect password. Please try again.');
      } else {
        alert('Login failed.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Login failed');
      return;
    }
  }

  function handlePasswordChange(e) {
    setPassword(e.target.value); // Update password state
  }

  function handleUsernameChange(e) {
    setUsername(e.target.value); // Update username state
  }

  function handleTogglePassword() {
    setShowPassword((v) => !v);
  }

  return (
    <div className="auth-page">
      <div className="login-container">
      <form onSubmit={handleLogin}>
        <h2 className="login-title">Login</h2>

        <div className="login-socials">
          <a href={'/auth/google'} className="social google" title="Sign in with Google">
            <i className="fab fa-google"></i>
          </a>
          <a href={'/auth/apple'} className="social apple" title="Sign in with Apple">
            <i className="fab fa-apple"></i>
          </a>
          <a href={'/auth/github'} className="social git-hub" title="Sign in with GitHub">
            <i className="fab fa-github"></i>
          </a>
        </div>
        
        <input className="login-input" type="text" placeholder="Username" required onChange={handleUsernameChange} value={username}/>
        <div className="password-wrapper">
          <input className="login-input" type={showPassword ? 'text' : 'password'} placeholder="Password" required onChange={handlePasswordChange} value={password} />
          <button className="toggle-eye" type="button" aria-label={showPassword ? 'Hide password' : 'Show password'} onClick={handleTogglePassword}>
            <i className={!showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'}></i>
          </button>
        </div>
        <button type="submit" className="login-button">Login</button>
        <p className="auth-footer">Don't have an account? <Link to="/register">Register</Link></p>
      </form>
      </div>
    </div>
  )
}

export default Login;