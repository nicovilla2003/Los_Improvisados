import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getProgressLogs, getStudentSummary } from '../services/api';
import '../styles/Dashboard.css';

const StudentDashboard = () => {
  const { user } = useAuth();
  const [summary, setSummary] = useState(null);
  const [recentLogs, setRecentLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, [user]);

  const loadDashboardData = async () => {
    if (!user?.student_id) return;
    
    try {
      setLoading(true);
      // Cargar resumen y logs recientes
      // const summaryData = await getStudentSummary(user.student_id);
      // const logsData = await getProgressLogs(user.student_id);
      
      // setSummary(summaryData);
      // setRecentLogs(logsData.slice(0, 5));
      
      // Datos de ejemplo mientras se implementan los endpoints
      setSummary({
        totalWorkouts: 24,
        thisWeekWorkouts: 4,
        currentStreak: 7,
        favoriteExercise: 'Press de banca',
      });
      
      setRecentLogs([
        { 
          id: 1, 
          date: '2025-11-20', 
          exercise: 'Press de banca', 
          weight: 60, 
          reps: 10, 
          sets: 3 
        },
        { 
          id: 2, 
          date: '2025-11-20', 
          exercise: 'Sentadilla', 
          weight: 80, 
          reps: 8, 
          sets: 4 
        },
      ]);
    } catch (error) {
      console.error('Error cargando datos del dashboard:', error);
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
        <h1>Mi Dashboard</h1>
        <p>Bienvenido de nuevo, {user?.username}</p>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🏋️</div>
          <div className="stat-content">
            <h3>Total Entrenamientos</h3>
            <p className="stat-number">{summary?.totalWorkouts || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <h3>Esta Semana</h3>
            <p className="stat-number">{summary?.thisWeekWorkouts || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔥</div>
          <div className="stat-content">
            <h3>Racha Actual</h3>
            <p className="stat-number">{summary?.currentStreak || 0} días</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <h3>Ejercicio Favorito</h3>
            <p className="stat-text">{summary?.favoriteExercise || 'N/A'}</p>
          </div>
        </div>
      </div>

      <div className="dashboard-section">
        <div className="section-header">
          <h2>Actividad Reciente</h2>
        </div>
        
        {recentLogs.length === 0 ? (
          <div className="empty-state">
            <p>No hay registros de entrenamiento aún</p>
            <p className="empty-subtitle">¡Comienza tu primera rutina!</p>
          </div>
        ) : (
          <div className="logs-list">
            {recentLogs.map((log) => (
              <div key={log.id} className="log-item">
                <div className="log-icon">💪</div>
                <div className="log-content">
                  <h4>{log.exercise}</h4>
                  <p className="log-details">
                    {log.sets} series × {log.reps} reps @ {log.weight}kg
                  </p>
                  <p className="log-date">{new Date(log.date).toLocaleDateString('es-ES')}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="dashboard-actions">
        <button className="action-button primary">
          Ver Mis Rutinas
        </button>
        <button className="action-button secondary">
          Registrar Progreso
        </button>
      </div>
    </div>
  );
};

export default StudentDashboard;