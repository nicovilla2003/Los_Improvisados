import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Sidebar.css';

const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, isAdmin, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getMenuItems = () => {
    if (isAdmin) {
      return [
        { path: '/admin', label: 'Dashboard', icon: '📊' },
        { path: '/admin/students', label: 'Estudiantes', icon: '👥' },
        { path: '/admin/trainers', label: 'Entrenadores', icon: '💪' },
        { path: '/admin/assignments', label: 'Asignaciones', icon: '🔗' },
      ];
    }

    if (user?.role === 'EMPLOYEE') {
      return [
        { path: '/trainer', label: 'Dashboard', icon: '📊' },
        { path: '/trainer/students', label: 'Mis Estudiantes', icon: '👥' },
        { path: '/trainer/routines', label: 'Rutinas', icon: '📝' },
        { path: '/trainer/exercises', label: 'Ejercicios', icon: '🏋️' },
      ];
    }

    if (user?.role === 'STUDENT') {
      return [
        { path: '/student', label: 'Dashboard', icon: '📊' },
        { path: '/student/progress', label: 'Mi Progreso', icon: '📈' },
      ];
    }

    return [];
  };

  const menuItems = getMenuItems();

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <img src="/icesi-logo-white.png" alt="Icesi" className="sidebar-logo" />
        <h2>Gym Icesi</h2>
      </div>

      <div className="sidebar-user">
        <div className="user-avatar">{user?.username?.[0]?.toUpperCase()}</div>
        <div className="user-info">
          <p className="user-name">{user?.username}</p>
          <p className="user-role">
            {isAdmin ? 'Administrador' : user?.role === 'EMPLOYEE' ? 'Entrenador' : 'Estudiante'}
          </p>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="sidebar-footer">
        <button onClick={handleLogout} className="logout-button">
          <span className="nav-icon">🚪</span>
          <span>Cerrar Sesión</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;