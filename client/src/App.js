import { BrowserRouter as Router, Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import Login from './Login';
import Home from './Home';
import Register from './Register';
import fetchJson from './lib/fetchJson';
import ItemTable from './itemTable';
import ItemDetail from './itemDetail';
import './App.css';

function AppInner() {

  const [user, setUser] = useState(null);
  const [loadingUser, setLoadingUser] = useState(true);

  const location = useLocation();
  useEffect(() => {
    let ignore = false;
    function onUserUpdated(e) {
      if (!ignore) setUser(e.detail);
    }
    window.addEventListener('user-updated', onUserUpdated);
    async function loadUser() {
      try {
        const me = await fetchJson('/api/me', { credentials: 'include' });
        if (!ignore) setUser(me);
      } catch (err) {
        if (!ignore) setUser(null);
      } finally {
        if (!ignore) setLoadingUser(false);
      }
    }
    loadUser();
    return () => { ignore = true; window.removeEventListener('user-updated', onUserUpdated); };
  }, [location.pathname]);

  return (
    <>
      <div className="topbar">
        <div className="topbar-left">
          <Link className="topbar-link" to="/">Home</Link>
          <Link className="topbar-link" to="/items">Items</Link>
        </div>
        <div className="topbar-right">
          {!loadingUser && !user && (
            <>
              <Link className="topbar-link" to="/login">Login</Link>
              <Link className="topbar-link primary" to="/register">Register</Link>
            </>
          )}
          {!loadingUser && user && (
            <>
              <span className="topbar-hello">Hi, {user.first_name} {user.last_name}</span>
              <form action="/logout" method="POST">
                <button className="logout-button" type="submit">Logout</button>
              </form>
            </>
          )}
        </div>
      </div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<Navigate to="/" replace />} />
        <Route path="/items" element={<ItemTable />} />
        <Route path="/items/:itemId" element={<ItemDetail />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <Router>
      <AppInner />
    </Router>
  );
}