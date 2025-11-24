import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getAssignedStudents, getTrainerSummary } from '../services/api';
import '../styles/Dashboard.css';

const TrainerDashboard = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [students, setStudents] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, [user]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const studentsData = await getAssignedStudents();
      setStudents(studentsData);
      
      // Datos de resumen de ejemplo
      setSummary({
        totalStudents: studentsData.length,
        activeRoutines: 12,
        thisWeekSessions: 45,
        avgProgress: 78,
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
        <h1>Dashboard del Entrenador</h1>
        <p>Bienvenido, {user?.username}</p>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>Estudiantes Asignados</h3>
            <p className="stat-number">{summary?.totalStudents || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📝</div>
          <div className="stat-content">
            <h3>Rutinas Activas</h3>
            <p className="stat-number">{summary?.activeRoutines || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💪</div>
          <div className="stat-content">
            <h3>Sesiones Esta Semana</h3>
            <p className="stat-number">{summary?.thisWeekSessions || 0}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-content">
            <h3>Progreso Promedio</h3>
            <p className="stat-number">{summary?.avgProgress || 0}%</p>
          </div>
        </div>
      </div>

      <div className="dashboard-section">
        <div className="section-header">
          <h2>Mis Estudiantes</h2>
          <button 
            className="button-secondary"
            onClick={() => navigate('/trainer/students')}
          >
            Ver Todos
          </button>
        </div>
        
        {students.length === 0 ? (
          <div className="empty-state">
            <p>No tienes estudiantes asignados aún</p>
          </div>
        ) : (
          <div className="students-grid">
            {students.slice(0, 6).map((student) => (
              <div 
                key={student.id} 
                className="student-card"
                onClick={() => navigate(`/trainer/students/${student.id}`)}
              >
                <div className="student-avatar">
                  {student.first_name[0]}{student.last_name[0]}
                </div>
                <div className="student-info">
                  <h4>{student.first_name} {student.last_name}</h4>
                  <p>{student.email}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="dashboard-actions">
        <button 
          className="action-button primary"
          onClick={() => navigate('/trainer/routines/new')}
        >
          Crear Nueva Rutina
        </button>
        <button 
          className="action-button secondary"
          onClick={() => navigate('/trainer/exercises')}
        >
          Gestionar Ejercicios
        </button>
      </div>
    </div>
  );
};

export default TrainerDashboard;