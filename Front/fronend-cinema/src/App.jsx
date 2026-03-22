import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import Login from './pages/Login';
import Home from './pages/Home';
import ListaSessoes from './pages/ListaSessoes';
import CompraIngresso from './pages/CompraIngresso';

const NavBar = () => {
  const { token, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const sair = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav style={{ padding: '15px', background: '#333', color: 'white', display: 'flex', justifyContent: 'space-between' }}>
      <div>
        <Link to="/" style={{ color: 'white', textDecoration: 'none', fontWeight: 'bold', fontSize: '1.2rem' }}>CineReserve</Link>
      </div>
      <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
        <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>Filmes</Link>
        {token ? (
          <button onClick={sair} style={{ background: 'transparent', border: '1px solid white', color: 'white', cursor: 'pointer', padding: '5px 10px', borderRadius: '4px' }}>Sair</button>
        ) : (
          <Link to="/login" style={{ color: 'white', textDecoration: 'none' }}>Fazer Login</Link>
        )}
      </div>
    </nav>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <NavBar />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Home />} />
          <Route path="/filme/:filmeId/sessoes" element={<ListaSessoes />} />
          
          {/* ATUALIZA ESTA ROTA AQUI 👇 */}
          <Route path="/sessao/:sessaoId/comprar" element={<CompraIngresso />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;