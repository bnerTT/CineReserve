import React, { createContext, useState } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  // Inicializa pegando o token do localStorage (caso o usuário já tenha logado antes)
  const [token, setToken] = useState(localStorage.getItem('access_token'));

  const login = (accessToken) => {
    localStorage.setItem('access_token', accessToken);
    setToken(accessToken);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};