import React, { useState, useEffect } from 'react';
import { getAllExercises, createExercise, deleteExercise } from '../services/api';
import '../styles/Dashboard.css';

const ExercisesPage = () => {
  const [exercises, setExercises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });
  
  const [formData, setFormData] = useState({
    name: '',
    type: 'fuerza',
    description: '',
    duration_minutes: '',
    difficulty: 'beginner',
    video_url: '',
  });

  useEffect(() => {
    loadExercises();
  }, []);

  const loadExercises = async () => {
    try {
      setLoading(true);
      const data = await getAllExercises();
      setExercises(data);
    } catch (error) {
      console.error('Error cargando ejercicios:', error);
      showMessage('error', 'Error al cargar ejercicios');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await createExercise({
        ...formData,
        duration_minutes: formData.duration_minutes ? parseInt(formData.duration_minutes) : null,
      });
      
      showMessage('success', 'Ejercicio creado exitosamente');
      setShowCreateForm(false);
      setFormData({
        name: '',
        type: 'fuerza',
        description: '',
        duration_minutes: '',
        difficulty: 'beginner',
        video_url: '',
      });
      loadExercises();
    } catch (error) {
      console.error('Error creando ejercicio:', error);
      showMessage('error', error.response?.data?.detail || 'Error al crear ejercicio');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (exerciseId) => {
    if (!window.confirm('¿Estás seguro de eliminar este ejercicio?')) {
      return;
    }

    try {
      setLoading(true);
      await deleteExercise(exerciseId);
      showMessage('success', 'Ejercicio eliminado');
      loadExercises();
    } catch (error) {
      console.error('Error eliminando ejercicio:', error);
      showMessage('error', error.response?.data?.detail || 'Error al eliminar ejercicio');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (type, text) => {
    setMessage({ type, text });
    setTimeout(() => setMessage({ type: '', text: '' }), 5000);
  };

  const getTypeIcon = (type) => {
    const icons = {
      fuerza: '💪',
      cardio: '🏃',
      movilidad: '🧘',
    };
    return icons[type] || '🏋️';
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

  if (loading && !showCreateForm) {
    return (
      <div className="dashboard-container">
        <div className="loading">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Gestión de Ejercicios</h1>
        <p>Crea y administra los ejercicios disponibles</p>
      </header>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      <div style={{ marginBottom: '24px' }}>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="button-primary"
        >
          {showCreateForm ? 'Cancelar' : '+ Crear Nuevo Ejercicio'}
        </button>
      </div>

      {showCreateForm && (
        <div className="form-card">
          <h2>Nuevo Ejercicio</h2>
          <form onSubmit={handleSubmit} className="assignment-form">
            <div className="form-group">
              <label htmlFor="name">Nombre del Ejercicio *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
                placeholder="Ej: Press de banca"
              />
            </div>

            <div className="form-group">
              <label htmlFor="type">Tipo *</label>
              <select
                id="type"
                name="type"
                value={formData.type}
                onChange={handleInputChange}
                required
              >
                <option value="fuerza">Fuerza</option>
                <option value="cardio">Cardio</option>
                <option value="movilidad">Movilidad</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="difficulty">Dificultad *</label>
              <select
                id="difficulty"
                name="difficulty"
                value={formData.difficulty}
                onChange={handleInputChange}
                required
              >
                <option value="beginner">Principiante</option>
                <option value="intermediate">Intermedio</option>
                <option value="advanced">Avanzado</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="duration_minutes">Duración (minutos)</label>
              <input
                type="number"
                id="duration_minutes"
                name="duration_minutes"
                value={formData.duration_minutes}
                onChange={handleInputChange}
                placeholder="20"
                min="1"
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Descripción</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Describe el ejercicio..."
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

            <div className="form-group">
              <label htmlFor="video_url">URL de Video (opcional)</label>
              <input
                type="url"
                id="video_url"
                name="video_url"
                value={formData.video_url}
                onChange={handleInputChange}
                placeholder="https://youtube.com/..."
              />
            </div>

            <button type="submit" className="button-primary" disabled={loading}>
              {loading ? 'Creando...' : 'Crear Ejercicio'}
            </button>
          </form>
        </div>
      )}

      <div className="dashboard-section">
        <div className="section-header">
          <h2>Mis Ejercicios ({exercises.length})</h2>
        </div>

        {exercises.length === 0 ? (
          <div className="empty-state">
            <p>No has creado ejercicios aún</p>
            <p className="empty-subtitle">Crea tu primer ejercicio para comenzar</p>
          </div>
        ) : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: '16px',
          }}>
            {exercises.map((exercise) => (
              <div
                key={exercise.id}
                style={{
                  background: 'white',
                  border: '1px solid #e5e7eb',
                  borderRadius: '12px',
                  padding: '20px',
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
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px', marginBottom: '12px' }}>
                  <div style={{ fontSize: '32px' }}>
                    {getTypeIcon(exercise.type)}
                  </div>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ margin: '0 0 8px 0', fontSize: '18px', fontWeight: '600' }}>
                      {exercise.name}
                    </h3>
                    {getDifficultyBadge(exercise.difficulty)}
                  </div>
                </div>

                {exercise.description && (
                  <p style={{ fontSize: '14px', color: '#6b7280', margin: '0 0 12px 0' }}>
                    {exercise.description}
                  </p>
                )}

                <div style={{ display: 'flex', gap: '16px', fontSize: '13px', color: '#9ca3af', marginBottom: '16px' }}>
                  <span>📂 {exercise.type}</span>
                  {exercise.duration_minutes && <span>⏱️ {exercise.duration_minutes} min</span>}
                </div>

                {exercise.video_url && (
                  <a
                    href={exercise.video_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      display: 'inline-block',
                      fontSize: '13px',
                      color: '#5454e9',
                      textDecoration: 'none',
                      marginBottom: '16px',
                    }}
                  >
                    🎥 Ver video demo
                  </a>
                )}

                <div style={{ borderTop: '1px solid #e5e7eb', paddingTop: '16px' }}>
                  <button
                    onClick={() => handleDelete(exercise.id)}
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

export default ExercisesPage;