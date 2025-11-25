import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAllRoutines, deleteRoutine } from '../services/api';
import api from '../services/api';
import '../styles/Dashboard.css';

const RoutinesPage = () => {
  const navigate = useNavigate();
  const [routines, setRoutines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    loadRoutines();
  }, []);

  const loadRoutines = async () => {
    try {
      setLoading(true);
      const data = await getAllRoutines();
      
      // Cargar ejercicios de cada rutina
      const routinesWithExercises = await Promise.all(
        data.map(async (routine) => {
          try {
            const response = await api.get(`/routine-exercises/${routine.id}`);
            return { ...routine, exercises: response.data };
          } catch (error) {
            return { ...routine, exercises: [] };
          }
        })
      );
      
      setRoutines(routinesWithExercises);
    } catch (error) {
      console.error('Error cargando rutinas:', error);
      showMessage('error', 'Error al cargar rutinas');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (routineId) => {
    if (!window.confirm('¿Estás seguro de eliminar esta rutina?')) {
      return;
    }

    try {
      setLoading(true);
      await deleteRoutine(routineId);
      showMessage('success', 'Rutina eliminada');
      loadRoutines();
    } catch (error) {
      console.error('Error eliminando rutina:', error);
      showMessage('error', error.response?.data?.detail || 'Error al eliminar rutina');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (type, text) => {
    setMessage({ type, text });
    setTimeout(() => setMessage({ type: '', text: '' }), 5000);
  };

  const getDifficultyBadge = (difficulty) => {
    const badges = {
      beginner: { label: 'Principiante', color: '#10b981' },
      intermediate: { label: 'Intermedio', color: '#f59e0b' },
      advanced: { label: 'Avanzado', color: '#ef4444' },
    };
    const badge = badges[difficulty] || badges.beginner;
    
    return (
      <span style={{
        padding: '4px 12px',
        borderRadius: '12px',
        fontSize: '12px',
        fontWeight: '600',
        backgroundColor: badge.color + '20',
        color: badge.color,
      }}>
        {badge.label}
      </span>
    );
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
        <h1>Mis Rutinas</h1>
        <p>Gestiona las rutinas de entrenamiento</p>
      </header>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      <div style={{ marginBottom: '24px' }}>
        <button
          onClick={() => navigate('/trainer/routines/new')}
          className="button-primary"
        >
          + Crear Nueva Rutina
        </button>
      </div>

      <div className="dashboard-section">
        <div className="section-header">
          <h2>Rutinas Creadas ({routines.length})</h2>
        </div>

        {routines.length === 0 ? (
          <div className="empty-state">
            <p>No has creado rutinas aún</p>
            <p className="empty-subtitle">Crea tu primera rutina para comenzar</p>
          </div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
            gap: '20px',
          }}>
            {routines.map((routine) => (
              <div
                key={routine.id}
                style={{
                  background: 'white',
                  border: '1px solid #e5e7eb',
                  borderRadius: '12px',
                  padding: '24px',
                  transition: 'all 0.2s',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
                  e.currentTarget.style.transform = 'translateY(-2px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.boxShadow = 'none';
                  e.currentTarget.style.transform = 'none';
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                  <div>
                    <h3 style={{ margin: '0 0 8px 0', fontSize: '20px', fontWeight: '600' }}>
                      {routine.name}
                    </h3>
                    {getDifficultyBadge(routine.difficulty)}
                  </div>
                  <div style={{ fontSize: '32px' }}>📝</div>
                </div>

                {routine.description && (
                  <p style={{ fontSize: '14px', color: '#6b7280', margin: '0 0 16px 0' }}>
                    {routine.description}
                  </p>
                )}

                <div style={{
                  background: '#f9fafb',
                  padding: '12px',
                  borderRadius: '8px',
                  marginBottom: '16px',
                }}>
                  <div style={{ fontSize: '13px', color: '#6b7280', marginBottom: '8px' }}>
                    <strong>{routine.exercises?.length || 0}</strong> ejercicios
                  </div>
                  {routine.exercises && routine.exercises.length > 0 && (
                    <div style={{ fontSize: '12px', color: '#9ca3af' }}>
                      {routine.exercises.slice(0, 3).map((ex, idx) => (
                        <div key={idx}>• Ejercicio {ex.exercise_id}</div>
                      ))}
                      {routine.exercises.length > 3 && (
                        <div>... y {routine.exercises.length - 3} más</div>
                      )}
                    </div>
                  )}
                </div>

                <div style={{
                  display: 'flex',
                  gap: '8px',
                  borderTop: '1px solid #e5e7eb',
                  paddingTop: '16px',
                }}>
                  <button
                    onClick={() => navigate(`/trainer/routines/${routine.id}`)}
                    className="button-secondary"
                    style={{ flex: 1 }}
                  >
                    Ver Detalles
                  </button>
                  <button
                    onClick={() => handleDelete(routine.id)}
                    className="button-danger-sm"
                    disabled={loading}
                  >
                    Eliminar
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default RoutinesPage;