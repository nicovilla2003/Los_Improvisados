import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAllStudents, getAllTrainers } from '../services/api';
import '../styles/Dashboard.css';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalStudents: 0,
    totalTrainers: 0,
    totalRoutines: 0,
    activeAssignments: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const students = await getAllStudents();
      // const trainers = await getAllTrainers();
      
      setStats({
        totalStudents: students.length,
        totalTrainers: 2, // Placeholder
        totalRoutines: 15, // Placeholder
        activeAssignments: 5, // Placeholder
      });
    } catch (error) {
      console.error('Error cargando datos:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Panel de Administración</h1>
        <p>Área de Bienestar - Gimnasio Icesi</p>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>Total Estudiantes</h3>
            <p className="stat-number">{stats.totalStudents}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💪</div>
          <div className="stat-content">
            <h3>Entrenadores</h3>
            <p className="stat-number">{stats.totalTrainers}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📝</div>
          <div className="stat-content">
            <h3>Rutinas Activas</h3>
            <p className="stat-number">{stats.totalRoutines}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔗</div>
          <div className="stat-content">
            <h3>Asignaciones</h3>
            <p className="stat-number">{stats.activeAssignments}</p>
          </div>
        </div>
      </div>

      <div className="admin-sections">
        <div className="admin-section-card" onClick={() => navigate('/admin/students')}>
          <div className="section-icon">👥</div>
          <h3>Gestión de Estudiantes</h3>
          <p>Ver y administrar todos los estudiantes registrados</p>
        </div>

        <div className="admin-section-card" onClick={() => navigate('/admin/trainers')}>
          <div className="section-icon">💪</div>
          <h3>Gestión de Entrenadores</h3>
          <p>Administrar entrenadores del gimnasio</p>
        </div>

        <div className="admin-section-card" onClick={() => navigate('/admin/assignments')}>
          <div className="section-icon">🔗</div>
          <h3>Asignaciones</h3>
          <p>Asignar estudiantes a entrenadores</p>
        </div>

        <div className="admin-section-card" onClick={() => navigate('/admin/reports')}>
          <div className="section-icon">📊</div>
          <h3>Reportes</h3>
          <p>Ver estadísticas y reportes generales</p>
        </div>
      </div>

      <div className="dashboard-section">
        <div className="section-header">
          <h2>Actividad Reciente</h2>
        </div>
        <div className="activity-list">
          <div className="activity-item">
            <span className="activity-icon">👤</span>
            <div className="activity-content">
              <p><strong>Laura Hernández</strong> completó una rutina</p>
              <span className="activity-time">Hace 2 horas</span>
            </div>
          </div>
          <div className="activity-item">
            <span className="activity-icon">🔗</span>
            <div className="activity-content">
              <p>Nueva asignación: <strong>Pedro Martínez</strong> → Paula Ramírez</p>
              <span className="activity-time">Hace 5 horas</span>
            </div>
          </div>
          <div className="activity-item">
            <span className="activity-icon">📝</span>
            <div className="activity-content">
              <p><strong>Andrés Castro</strong> creó una nueva rutina</p>
              <span className="activity-time">Ayer</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;