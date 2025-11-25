import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAllRoutines } from '../services/api';
import api from '../services/api';
import '../styles/Dashboard.css';

const StudentRoutineProgress = () => {
  const navigate = useNavigate();
  const [routines, setRoutines] = useState([]);
  const [selectedRoutine, setSelectedRoutine] = useState(null);
  const [routineExercises, setRoutineExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [progressData, setProgressData] = useState({});

  useEffect(() => {
    loadRoutines();
  }, []);

  const loadRoutines = async () => {
    try {
      setLoading(true);
      const data = await getAllRoutines();
      setRoutines(data);
      
      if (data.length > 0) {
        loadRoutineDetails(data[0].id);
      }
    } catch (error) {
      console.error('Error cargando rutinas:', error);
      showMessage('error', 'Error al cargar rutinas');
    } finally {
      setLoading(false);
    }
  };

  const loadRoutineDetails = async (routineId) => {
    try {
      setLoading(true);
      const routine = routines.find(r => r.id === routineId) || 
                     (await api.get(`/routines/${routineId}`)).data;
      
      setSelectedRoutine(routine);
      
      // Cargar ejercicios de la rutina
      const exercisesResponse = await api.get(`/routine-exercises/${routineId}`);
      const exercises = exercisesResponse.data;
      
      // Cargar detalles de cada ejercicio
      const exercisesWithDetails = await Promise.all(
        exercises.map(async (re) => {
          try {
            const exerciseResponse = await api.get(`/exercises/${re.exercise_id}`);
            return {
              ...re,
              exercise: exerciseResponse.data,
            };
          } catch (error) {
            return {
              ...re,
              exercise: { id: re.exercise_id, name: `Ejercicio ${re.exercise_id}` },
            };
          }
        })
      );
      
      setRoutineExercises(exercisesWithDetails);
      
      // Inicializar datos de progreso vacíos
      const initialProgress = {};
      exercisesWithDetails.forEach(ex => {
        initialProgress[ex.id] = {
          completed: false,
          weight: '',
          reps: ex.reps || '',
          notes: '',
        };
      });
      setProgressData(initialProgress);
    } catch (error) {
      console.error('Error cargando detalles de rutina:', error);
      showMessage('error', 'Error al cargar detalles de la rutina');
    } finally {
      setLoading(false);
    }
  };

  const handleRoutineChange = (routineId) => {
    loadRoutineDetails(parseInt(routineId));
  };

  const handleProgressChange = (exerciseId, field, value) => {
    setProgressData(prev => ({
      ...prev,
      [exerciseId]: {
        ...prev[exerciseId],
        [field]: value,
      },
    }));
  };

  const handleToggleComplete = (exerciseId) => {
    setProgressData(prev => ({
      ...prev,
      [exerciseId]: {
        ...prev[exerciseId],
        completed: !prev[exerciseId].completed,
      },
    }));
  };

  const handleSaveProgress = async () => {
    try {
      setLoading(true);
      
      // Aquí guardarías el progreso en el backend
      // Por ahora solo mostramos un mensaje de éxito
      
      showMessage('success', '¡Progreso guardado exitosamente!');
      
      // Resetear el formulario
      const resetProgress = {};
      routineExercises.forEach(ex => {
        resetProgress[ex.id] = {
          completed: false,
          weight: '',
          reps: ex.reps || '',
          notes: '',
        };
      });
      setProgressData(resetProgress);
    } catch (error) {
      console.error('Error guardando progreso:', error);
      showMessage('error', 'Error al guardar progreso');
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

  const completedCount = Object.values(progressData).filter(p => p.completed).length;
  const totalExercises = routineExercises.length;
  const progressPercentage = totalExercises > 0 ? (completedCount / totalExercises) * 100 : 0;

  if (loading && !selectedRoutine) {
    return (
      <div className="dashboard-container">
        <div className="loading">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Mi Progreso en Rutinas</h1>
        <p>Registra tu progreso en cada ejercicio</p>
      </header>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      {routines.length === 0 ? (
        <div className="empty-state">
          <p>No tienes rutinas disponibles</p>
          <p className="empty-subtitle">Contacta a tu entrenador para que te asigne una rutina</p>
        </div>
      ) : (
        <>
          <div className="form-card">
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label htmlFor="routine">Seleccionar Rutina</label>
              <select
                id="routine"
                value={selectedRoutine?.id || ''}
                onChange={(e) => handleRoutineChange(e.target.value)}
                style={{ maxWidth: '500px' }}
              >
                {routines.map((routine) => (
                  <option key={routine.id} value={routine.id}>
                    {routine.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {selectedRoutine && (
            <>
              <div className="dashboard-section">
                <div style={{ marginBottom: '24px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                    <div>
                      <h2 style={{ margin: '0 0 8px 0' }}>{selectedRoutine.name}</h2>
                      {getDifficultyBadge(selectedRoutine.difficulty)}
                    </div>
                  </div>
                  
                  {selectedRoutine.description && (
                    <p style={{ color: '#6b7280', margin: '16px 0' }}>
                      {selectedRoutine.description}
                    </p>
                  )}

                  {/* Barra de progreso */}
                  <div style={{ marginTop: '24px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <span style={{ fontSize: '14px', fontWeight: '600' }}>
                        Progreso de la sesión
                      </span>
                      <span style={{ fontSize: '14px', color: '#6b7280' }}>
                        {completedCount} / {totalExercises} ejercicios
                      </span>
                    </div>
                    <div style={{
                      width: '100%',
                      height: '12px',
                      background: '#e5e7eb',
                      borderRadius: '6px',
                      overflow: 'hidden',
                    }}>
                      <div style={{
                        width: `${progressPercentage}%`,
                        height: '100%',
                        background: 'linear-gradient(90deg, #5454e9, #7c7ce9)',
                        transition: 'width 0.3s ease',
                      }} />
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  {routineExercises.map((routineExercise, index) => {
                    const progress = progressData[routineExercise.id] || {};
                    const isCompleted = progress.completed;

                    return (
                      <div
                        key={routineExercise.id}
                        style={{
                          background: isCompleted ? '#f0fdf4' : 'white',
                          border: `2px solid ${isCompleted ? '#10b981' : '#e5e7eb'}`,
                          borderRadius: '12px',
                          padding: '20px',
                          transition: 'all 0.3s',
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px' }}>
                          <div
                            onClick={() => handleToggleComplete(routineExercise.id)}
                            style={{
                              width: '40px',
                              height: '40px',
                              borderRadius: '50%',
                              border: `3px solid ${isCompleted ? '#10b981' : '#d1d5db'}`,
                              background: isCompleted ? '#10b981' : 'white',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              cursor: 'pointer',
                              flexShrink: 0,
                              transition: 'all 0.2s',
                            }}
                          >
                            {isCompleted && (
                              <span style={{ color: 'white', fontSize: '20px' }}>✓</span>
                            )}
                          </div>

                          <div style={{ flex: 1 }}>
                            <div style={{ marginBottom: '12px' }}>
                              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                                <span style={{ fontSize: '18px', fontWeight: '600' }}>
                                  {index + 1}. {routineExercise.exercise?.name || 'Ejercicio'}
                                </span>
                              </div>
                              
                              <div style={{ display: 'flex', gap: '16px', fontSize: '14px', color: '#6b7280' }}>
                                {routineExercise.sets && (
                                  <span>📊 {routineExercise.sets} series</span>
                                )}
                                {routineExercise.reps && (
                                  <span>🔢 {routineExercise.reps} reps</span>
                                )}
                                {routineExercise.duration_seconds && (
                                  <span>⏱️ {routineExercise.duration_seconds}s</span>
                                )}
                              </div>
                            </div>

                            <div style={{
                              display: 'grid',
                              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                              gap: '12px',
                              marginTop: '16px',
                            }}>
                              <div>
                                <label style={{ fontSize: '13px', color: '#6b7280', display: 'block', marginBottom: '4px' }}>
                                  Peso (kg)
                                </label>
                                <input
                                  type="number"
                                  value={progress.weight || ''}
                                  onChange={(e) => handleProgressChange(routineExercise.id, 'weight', e.target.value)}
                                  placeholder="0"
                                  min="0"
                                  step="0.5"
                                  style={{
                                    width: '100%',
                                    padding: '8px 12px',
                                    border: '1px solid #d1d5db',
                                    borderRadius: '6px',
                                    fontSize: '14px',
                                  }}
                                />
                              </div>

                              <div>
                                <label style={{ fontSize: '13px', color: '#6b7280', display: 'block', marginBottom: '4px' }}>
                                  Reps realizadas
                                </label>
                                <input
                                  type="number"
                                  value={progress.reps || ''}
                                  onChange={(e) => handleProgressChange(routineExercise.id, 'reps', e.target.value)}
                                  placeholder={routineExercise.reps || '0'}
                                  min="0"
                                  style={{
                                    width: '100%',
                                    padding: '8px 12px',
                                    border: '1px solid #d1d5db',
                                    borderRadius: '6px',
                                    fontSize: '14px',
                                  }}
                                />
                              </div>

                              <div style={{ gridColumn: 'span 2' }}>
                                <label style={{ fontSize: '13px', color: '#6b7280', display: 'block', marginBottom: '4px' }}>
                                  Notas
                                </label>
                                <input
                                  type="text"
                                  value={progress.notes || ''}
                                  onChange={(e) => handleProgressChange(routineExercise.id, 'notes', e.target.value)}
                                  placeholder="Cómo te sentiste, observaciones..."
                                  style={{
                                    width: '100%',
                                    padding: '8px 12px',
                                    border: '1px solid #d1d5db',
                                    borderRadius: '6px',
                                    fontSize: '14px',
                                  }}
                                />
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '24px' }}>
                <button
                  onClick={() => navigate('/student')}
                  className="button-secondary"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleSaveProgress}
                  className="button-primary"
                  disabled={loading || completedCount === 0}
                >
                  {loading ? 'Guardando...' : 'Guardar Progreso'}
                </button>
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
};

export default StudentRoutineProgress;