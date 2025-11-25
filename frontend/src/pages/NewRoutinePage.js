import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createRoutine, getAllExercises } from '../services/api';
import api from '../services/api';
import '../styles/Dashboard.css';

const NewRoutinePage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [exercises, setExercises] = useState([]);
  const [message, setMessage] = useState({ type: '', text: '' });
  
  const [routineData, setRoutineData] = useState({
    name: '',
    description: '',
    difficulty: 'beginner',
  });

  const [selectedExercises, setSelectedExercises] = useState([]);

  useEffect(() => {
    loadExercises();
  }, []);

  const loadExercises = async () => {
    try {
      const data = await getAllExercises();
      setExercises(data);
    } catch (error) {
      console.error('Error cargando ejercicios:', error);
      showMessage('error', 'Error al cargar ejercicios');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setRoutineData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAddExercise = (exercise) => {
    if (selectedExercises.find(ex => ex.exercise_id === exercise.id)) {
      showMessage('error', 'Este ejercicio ya está en la rutina');
      return;
    }

    setSelectedExercises(prev => [...prev, {
      exercise_id: exercise.id,
      exercise_name: exercise.name,
      order_index: prev.length + 1,
      sets: 3,
      reps: 10,
      duration_seconds: null,
    }]);
  };

  const handleRemoveExercise = (exerciseId) => {
    setSelectedExercises(prev =>
      prev
        .filter(ex => ex.exercise_id !== exerciseId)
        .map((ex, index) => ({ ...ex, order_index: index + 1 }))
    );
  };

  const handleExerciseConfigChange = (exerciseId, field, value) => {
    setSelectedExercises(prev =>
      prev.map(ex =>
        ex.exercise_id === exerciseId
          ? { ...ex, [field]: value ? parseInt(value) : null }
          : ex
      )
    );
  };

  const moveExercise = (index, direction) => {
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= selectedExercises.length) return;

    const newExercises = [...selectedExercises];
    [newExercises[index], newExercises[newIndex]] = [newExercises[newIndex], newExercises[index]];
    
    setSelectedExercises(
      newExercises.map((ex, idx) => ({ ...ex, order_index: idx + 1 }))
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (selectedExercises.length === 0) {
      showMessage('error', 'Debes agregar al menos un ejercicio a la rutina');
      return;
    }

    try {
      setLoading(true);
      
      // Crear la rutina
      const routine = await createRoutine(routineData);
      
      // Agregar ejercicios a la rutina
      for (const exercise of selectedExercises) {
        await api.post('/routine-exercises', {
          routine_id: routine.id,
          exercise_id: exercise.exercise_id,
          order_index: exercise.order_index,
          sets: exercise.sets,
          reps: exercise.reps,
          duration_seconds: exercise.duration_seconds,
        });
      }

      showMessage('success', 'Rutina creada exitosamente');
      setTimeout(() => {
        navigate('/trainer/routines');
      }, 1500);
    } catch (error) {
      console.error('Error creando rutina:', error);
      showMessage('error', error.response?.data?.detail || 'Error al crear rutina');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (type, text) => {
    setMessage({ type, text });
    setTimeout(() => setMessage({ type: '', text: '' }), 5000);
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Crear Nueva Rutina</h1>
        <p>Define una rutina de entrenamiento con ejercicios específicos</p>
      </header>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-card">
          <h2>Información de la Rutina</h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div className="form-group">
              <label htmlFor="name">Nombre de la Rutina *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={routineData.name}
                onChange={handleInputChange}
                required
                placeholder="Ej: Full Body Principiantes"
              />
            </div>

            <div className="form-group">
              <label htmlFor="difficulty">Nivel de Dificultad *</label>
              <select
                id="difficulty"
                name="difficulty"
                value={routineData.difficulty}
                onChange={handleInputChange}
                required
              >
                <option value="beginner">Principiante</option>
                <option value="intermediate">Intermedio</option>
                <option value="advanced">Avanzado</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="description">Descripción</label>
              <textarea
                id="description"
                name="description"
                value={routineData.description}
                onChange={handleInputChange}
                placeholder="Describe el objetivo y características de esta rutina..."
                rows="3"
                style={{
                  padding: '10px 12px',
                  border: '1px solid #d1d5db',
                  borderRadius: '6px',
                  fontSize: '14px',
                  fontFamily: 'inherit',
                }}
              />
            </div>
          </div>
        </div>

        <div className="form-card">
          <h2>Ejercicios de la Rutina</h2>
          
          {selectedExercises.length > 0 && (
            <div style={{ marginBottom: '24px' }}>
              <h3 style={{ fontSize: '16px', marginBottom: '12px' }}>
                Ejercicios Agregados ({selectedExercises.length})
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {selectedExercises.map((exercise, index) => (
                  <div
                    key={exercise.exercise_id}
                    style={{
                      background: '#f9fafb',
                      padding: '16px',
                      borderRadius: '8px',
                      border: '1px solid #e5e7eb',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                      <span style={{ fontSize: '20px', fontWeight: '600' }}>
                        {exercise.order_index}.
                      </span>
                      <span style={{ flex: 1, fontWeight: '600' }}>
                        {exercise.exercise_name}
                      </span>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <button
                          type="button"
                          onClick={() => moveExercise(index, 'up')}
                          disabled={index === 0}
                          style={{
                            padding: '4px 8px',
                            border: 'none',
                            background: index === 0 ? '#e5e7eb' : '#5454e9',
                            color: 'white',
                            borderRadius: '4px',
                            cursor: index === 0 ? 'not-allowed' : 'pointer',
                          }}
                        >
                          ↑
                        </button>
                        <button
                          type="button"
                          onClick={() => moveExercise(index, 'down')}
                          disabled={index === selectedExercises.length - 1}
                          style={{
                            padding: '4px 8px',
                            border: 'none',
                            background: index === selectedExercises.length - 1 ? '#e5e7eb' : '#5454e9',
                            color: 'white',
                            borderRadius: '4px',
                            cursor: index === selectedExercises.length - 1 ? 'not-allowed' : 'pointer',
                          }}
                        >
                          ↓
                        </button>
                        <button
                          type="button"
                          onClick={() => handleRemoveExercise(exercise.exercise_id)}
                          className="button-danger-sm"
                        >
                          ✕
                        </button>
                      </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
                      <div>
                        <label style={{ fontSize: '12px', color: '#6b7280', display: 'block', marginBottom: '4px' }}>
                          Series
                        </label>
                        <input
                          type="number"
                          value={exercise.sets || ''}
                          onChange={(e) => handleExerciseConfigChange(exercise.exercise_id, 'sets', e.target.value)}
                          min="1"
                          style={{
                            width: '100%',
                            padding: '8px',
                            border: '1px solid #d1d5db',
                            borderRadius: '4px',
                            fontSize: '14px',
                          }}
                        />
                      </div>
                      <div>
                        <label style={{ fontSize: '12px', color: '#6b7280', display: 'block', marginBottom: '4px' }}>
                          Repeticiones
                        </label>
                        <input
                          type="number"
                          value={exercise.reps || ''}
                          onChange={(e) => handleExerciseConfigChange(exercise.exercise_id, 'reps', e.target.value)}
                          min="1"
                          style={{
                            width: '100%',
                            padding: '8px',
                            border: '1px solid #d1d5db',
                            borderRadius: '4px',
                            fontSize: '14px',
                          }}
                        />
                      </div>
                      <div>
                        <label style={{ fontSize: '12px', color: '#6b7280', display: 'block', marginBottom: '4px' }}>
                          Duración (seg)
                        </label>
                        <input
                          type="number"
                          value={exercise.duration_seconds || ''}
                          onChange={(e) => handleExerciseConfigChange(exercise.exercise_id, 'duration_seconds', e.target.value)}
                          min="1"
                          placeholder="Opcional"
                          style={{
                            width: '100%',
                            padding: '8px',
                            border: '1px solid #d1d5db',
                            borderRadius: '4px',
                            fontSize: '14px',
                          }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div>
            <h3 style={{ fontSize: '16px', marginBottom: '12px' }}>
              Ejercicios Disponibles
            </h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
              gap: '12px',
              maxHeight: '400px',
              overflowY: 'auto',
              padding: '4px',
            }}>
              {exercises.map((exercise) => (
                <div
                  key={exercise.id}
                  onClick={() => handleAddExercise(exercise)}
                  style={{
                    background: 'white',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    padding: '12px',
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = '#5454e9';
                    e.currentTarget.style.background = '#f3f4ff';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = '#e5e7eb';
                    e.currentTarget.style.background = 'white';
                  }}
                >
                  <div style={{ fontWeight: '600', marginBottom: '4px' }}>
                    {exercise.name}
                  </div>
                  <div style={{ fontSize: '12px', color: '#6b7280' }}>
                    {exercise.type} • {exercise.difficulty}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
          <button
            type="button"
            onClick={() => navigate('/trainer/routines')}
            className="button-secondary"
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="button-primary"
            disabled={loading || selectedExercises.length === 0}
          >
            {loading ? 'Creando...' : 'Crear Rutina'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default NewRoutinePage;