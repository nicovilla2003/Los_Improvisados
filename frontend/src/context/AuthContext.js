import React, { createContext, useState, useContext, useEffect } from 'react';
import { getCurrentUser } from '../services/api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('access_token');
    const adminFlag = localStorage.getItem('is_admin') === 'true';
    
    if (token) {
      try {
        const userData = await getCurrentUser();
        setUser(userData);
        setIsAdmin(adminFlag);
      } catch (error) {
        console.error('Error verificando autenticación:', error);
        logout();
      }
    }
    setLoading(false);
  };

  const login = (token, role, adminFlag = false) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user_role', role);
    localStorage.setItem('is_admin', adminFlag.toString());
    setIsAdmin(adminFlag);
    checkAuth();
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('is_admin');
    setUser(null);
    setIsAdmin(false);
  };

  const value = {
    user,
    loading,
    isAdmin,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};