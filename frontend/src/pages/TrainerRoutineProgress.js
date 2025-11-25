import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAssignedStudents } from '../services/api';
import api from '../services/api';
import '../styles/Dashboard.css';

const TrainerRoutineProgress = () => {
  const { studentId } = useParams();
  const navigate = useNavigate();
  const [students, setStudents] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [progressHistory, setProgressHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [recommendationText, setRecommendationText] = useState('');

  useEffect(() => {
    loadStudents();
  }, []);

  useEffect(() => {
    if (studentId && students.length > 0) {
      const student = students.find(s => s.id === studentId);
      if (student) {
        setSelectedStudent(student);
        loadStudentProgress(studentId);
      }
    }
  }, [studentId, students]);

  const loadStudents = async () => {
    try {
      setLoading(true);
      const data = await getAssignedStudents();
      setStudents(data);
      
      if (!studentId && data.length > 0) {
        setSelectedStudent(data[0]);
        loadStudentProgress(data[0].id);
      }
    } catch (error) {
      console.error('Error cargando estudiantes:', error);
      showMessage('error', 'Error al cargar estudiantes');
    } finally {
      setLoading(false);
    }
  };

  const loadStudentProgress = async (studentIdToLoad) => {
    try {
      setLoading(true);
      
      // Aquí cargarías el progreso real del estudiante desde el backend
      // const response = await api.get(`/progress/students/${studentIdToLoad}/logs`);
      // setProgressHistory(response.data);
      
      // Por ahora usamos datos de ejemplo
      setProgressHistory([
        {
          id: 1,
          date: '2025-11-24',
          routine_name: 'Fuerza full body principiantes',
          exercises: [
            { name: 'Press de banca', sets: 3, reps: 10, weight: 60, completed: true },
            { name: 'Sentadilla con barra', sets: 3, reps: 10, weight: 80, completed: true },
          ],
          notes: 'Buena sesión, pude aumentar peso en sentadilla',
        },
        {
          id: 2,
          date: '2025-11-22',
          routine_name: 'Fuerza full body principiantes',
          exercises: [
            { name: 'Press de banca', sets: 3, reps: 10, weight: 57.5, completed: true },
            { name: 'Sentadilla con barra', sets: 3, reps: 10, weight: 75, completed: true },
          ],
          notes: 'Me costó un poco el press de banca',
        },
        {
          id: 3,
          date: '2025-11-20',
          routine_name: 'Cardio y core',
          exercises: [
            { name: 'Trote en banda', sets: 1, duration: '20 min', completed: true },
            { name: 'Plancha abdominal', sets: 4, reps: 20, duration: '40s', completed: true },
          ],
          notes: 'Excelente cardio hoy',
        },
      ]);
    } catch (error) {
      console.error('Error cargando progreso:', error);
      showMessage('error', 'Error al cargar progreso del estudiante');
    } finally {
      setLoading(false);
    }
  };

  const handleStudentChange = (studentIdToSelect) => {
    const student = students.find(s => s.id === studentIdToSelect);
    if (student) {
      setSelectedStudent(student);
      loadStudentProgress(studentIdToSelect);
      navigate(`/trainer/students/${studentIdToSelect}/progress`);
    }
  };

  const handleSendRecommendation = async () => {
    if (!recommendationText.trim()) {
      showMessage('error', 'Por favor escribe una recomendación');
      return;
    }

    try {
      setLoading(true);
      
      // Aquí enviarías la recomendación al backend
      // await api.post('/recommendations', {
      //   student_id: selectedStudent.id,
      //   message: recommendationText,
      // });
      
      showMessage('success', 'Recomendación enviada exitosamente');
      setRecommendationText('');
    } catch (error) {
      console.error('Error enviando recomendación:', error);
      showMessage('error', 'Error al enviar recomendación');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (type, text) => {
    setMessage({ type, text });
    setTimeout(() => setMessage({ type: '', text: '' }), 5000);
  };

  if (loading && !selectedStudent) {
    return (
      <div className="dashboard-container">
        <div className="loading">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Progreso del Estudiante</h1>
        <p>Monitorea el rendimiento y envía recomendaciones</p>
      </header>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      {students.length === 0 ? (
        <div className="empty-state">
          <p>No tienes estudiantes asignados</p>
        </div>
      ) : (
        <>
          <div className="form-card">
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label htmlFor="student">Seleccionar Estudiante</label>
              <select
                id="student"
                value={selectedStudent?.id || ''}
                onChange={(e) => handleStudentChange(e.target.value)}
                style={{ maxWidth: '500px' }}
              >
                {students.map((student) => (
                  <option key={student.id} value={student.id}>
                    {student.first_name} {student.last_name} ({student.id})
                  </option>
                ))}
              </select>
            </div>
          </div>

          {selectedStudent && (
            <>
              <div className="dashboard-section">
                <div style={{
                  background: 'linear-gradient(135deg, #5454e9 0%, #7c7ce9 100%)',
                  color: 'white',
                  padding: '24px',
                  borderRadius: '12px',
                  marginBottom: '24px',
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{
                      width: '64px',
                      height: '64px',
                      borderRadius: '50%',
                      background: 'rgba(255, 255, 255, 0.2)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '28px',
                      fontWeight: '600',
                    }}>
                      {selectedStudent.first_name[0]}{selectedStudent.last_name[0]}
                    </div>
                    <div>
                      <h2 style={{ margin: '0 0 8px 0', fontSize: '24px' }}>
                        {selectedStudent.first_name} {selectedStudent.last_name}
                      </h2>
                      <p style={{ margin: 0, opacity: 0.9 }}>
                        {selectedStudent.email} • Código: {selectedStudent.id}
                      </p>
                    </div>
                  </div>
                </div>

                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                  gap: '16px',
                  marginBottom: '24px',
                }}>
                  <div style={{
                    background: '#f9fafb',
                    padding: '20px',
                    borderRadius: '12px',
                    border: '1px solid #e5e7eb',
                  }}>
                    <div style={{ fontSize: '14px', color: '#6b7280', marginBottom: '8px' }}>
                      Total Sesiones
                    </div>
                    <div style={{ fontSize: '32px', fontWeight: '700', color: '#111827' }}>
                      {progressHistory.length}
                    </div>
                  </div>

                  <div style={{
                    background: '#f9fafb',
                    padding: '20px',
                    borderRadius: '12px',
                    border: '1px solid #e5e7eb',
                  }}>
                    <div style={{ fontSize: '14px', color: '#6b7280', marginBottom: '8px' }}>
                      Esta Semana
                    </div>
                    <div style={{ fontSize: '32px', fontWeight: '700', color: '#111827' }}>
                      2
                    </div>
                  </div>

                  <div style={{
                    background: '#f9fafb',
                    padding: '20px',
                    borderRadius: '12px',
                    border: '1px solid #e5e7eb',
                  }}>
                    <div style={{ fontSize: '14px', color: '#6b7280', marginBottom: '8px' }}>
                      Última Sesión
                    </div>
                    <div style={{ fontSize: '18px', fontWeight: '600', color: '#111827' }}>
                      {progressHistory.length > 0 
                        ? new Date(progressHistory[0].date).toLocaleDateString('es-ES')
                        : 'N/A'
                      }
                    </div>
                  </div>
                </div>

                <h3 style={{ fontSize: '18px', marginBottom: '16px', fontWeight: '600' }}>
                  Historial de Entrenamientos
                </h3>

                {progressHistory.length === 0 ? (
                  <div className="empty-state">
                    <p>Este estudiante aún no ha registrado progreso</p>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    {progressHistory.map((session) => (
                      <div
                        key={session.id}
                        style={{
                          background: 'white',
                          border: '1px solid #e5e7eb',
                          borderRadius: '12px',
                          padding: '20px',
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                          <div>
                            <h4 style={{ margin: '0 0 8px 0', fontSize: '18px', fontWeight: '600' }}>
                              {session.routine_name}
                            </h4>
                            <p style={{ margin: 0, fontSize: '14px', color: '#6b7280' }}>
                              📅 {new Date(session.date).toLocaleDateString('es-ES', { 
                                weekday: 'long', 
                                year: 'numeric', 
                                month: 'long', 
                                day: 'numeric' 
                              })}
                            </p>
                          </div>
                          <span style={{
                            padding: '6px 12px',
                            background: '#d1fae5',
                            color: '#065f46',
                            borderRadius: '6px',
                            fontSize: '13px',
                            fontWeight: '600',
                          }}>
                            ✓ Completada
                          </span>
                        </div>

                        <div style={{
                          background: '#f9fafb',
                          borderRadius: '8px',
                          padding: '16px',
                          marginBottom: '12px',
                        }}>
                          <div style={{ fontSize: '13px', fontWeight: '600', marginBottom: '12px', color: '#374151' }}>
                            Ejercicios realizados:
                          </div>
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                            {session.exercises.map((exercise, idx) => (
                              <div key={idx} style={{ fontSize: '14px', color: '#4b5563' }}>
                                <span style={{ fontWeight: '600' }}>• {exercise.name}:</span>{' '}
                                {exercise.sets && <span>{exercise.sets} series</span>}
                                {exercise.reps && <span> × {exercise.reps} reps</span>}
                                {exercise.weight && <span> @ {exercise.weight}kg</span>}
                                {exercise.duration && <span> • {exercise.duration}</span>}
                              </div>
                            ))}
                          </div>
                        </div>

                        {session.notes && (
                          <div style={{
                            borderLeft: '3px solid #5454e9',
                            paddingLeft: '12px',
                            fontSize: '14px',
                            color: '#6b7280',
                            fontStyle: 'italic',
                          }}>
                            "{session.notes}"
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="form-card">
                <h2>Enviar Recomendación</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div className="form-group">
                    <label htmlFor="recommendation">Mensaje para el estudiante</label>
                    <textarea
                      id="recommendation"
                      value={recommendationText}
                      onChange={(e) => setRecommendationText(e.target.value)}
                      placeholder="Escribe tus observaciones, recomendaciones o felicitaciones..."
                      rows="4"
                      style={{
                        padding: '10px 12px',
                        border: '1px solid #d1d5db',
                        borderRadius: '6px',
                        fontSize: '14px',
                        fontFamily: 'inherit',
                      }}
                    />
                  </div>

                  <button
                    onClick={handleSendRecommendation}
                    className="button-primary"
                    disabled={loading || !recommendationText.trim()}
                  >
                    {loading ? 'Enviando...' : 'Enviar Recomendación'}
                  </button>
                </div>
              </div>
            </>
          )}
        </>
      )}
    </div>
  );
};

export default TrainerRoutineProgress;