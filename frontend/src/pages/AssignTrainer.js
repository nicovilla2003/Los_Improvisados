import React, { useState, useEffect } from 'react';
import { getAllStudents, getAllTrainers } from '../services/api';
import api from '../services/api';
import '../styles/Dashboard.css';

const AssignTrainer = () => {
  const [students, setStudents] = useState([]);
  const [trainers, setTrainers] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState('');
  const [selectedTrainer, setSelectedTrainer] = useState('');
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [studentsData, trainersData] = await Promise.all([
        getAllStudents(),
        getAllTrainers(),
      ]);
      
      setStudents(studentsData);
      setTrainers(trainersData || [
        { id: '1007', first_name: 'Paula', last_name: 'Ramírez' },
        { id: '1008', first_name: 'Andrés', last_name: 'Castro' },
      ]);
      
      // Cargar asignaciones existentes
      loadAssignments();
    } catch (error) {
      console.error('Error cargando datos:', error);
      showMessage('error', 'Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  const loadAssignments = async () => {
    try {
      // Aquí cargarías las asignaciones desde el backend
      // const response = await api.get('/assignments');
      // setAssignments(response.data);
      
      // Placeholder data
      setAssignments([
        { student_id: '2001', trainer_id: '1007', student_name: 'Laura Hernández', trainer_name: 'Paula Ramírez' },
        { student_id: '2002', trainer_id: '1007', student_name: 'Pedro Martínez', trainer_name: 'Paula Ramírez' },
      ]);
    } catch (error) {
      console.error('Error cargando asignaciones:', error);
    }
  };

  const handleAssign = async (e) => {
    e.preventDefault();
    
    if (!selectedStudent || !selectedTrainer) {
      showMessage('error', 'Selecciona un estudiante y un entrenador');
      return;
    }

    try {
      setLoading(true);
      // await api.post('/assignments', {
      //   student_id: selectedStudent,
      //   trainer_id: selectedTrainer,
      // });
      
      showMessage('success', 'Asignación realizada exitosamente');
      setSelectedStudent('');
      setSelectedTrainer('');
      loadAssignments();
    } catch (error) {
      console.error('Error al asignar:', error);
      showMessage('error', error.response?.data?.detail || 'Error al realizar asignación');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveAssignment = async (studentId, trainerId) => {
    if (!window.confirm('¿Estás seguro de eliminar esta asignación?')) {
      return;
    }

    try {
      setLoading(true);
      // await api.delete(`/assignments/${studentId}/${trainerId}`);
      
      showMessage('success', 'Asignación eliminada');
      loadAssignments();
    } catch (error) {
      console.error('Error al eliminar asignación:', error);
      showMessage('error', 'Error al eliminar asignación');
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
        <h1>Asignación de Entrenadores</h1>
        <p>Gestiona las asignaciones estudiante-entrenador</p>
      </header>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="form-card">
        <h2>Nueva Asignación</h2>
        <form onSubmit={handleAssign} className="assignment-form">
          <div className="form-group">
            <label htmlFor="student">Estudiante</label>
            <select
              id="student"
              value={selectedStudent}
              onChange={(e) => setSelectedStudent(e.target.value)}
              disabled={loading}
              required
            >
              <option value="">Seleccionar estudiante</option>
              {students.map((student) => (
                <option key={student.id} value={student.id}>
                  {student.first_name} {student.last_name} ({student.id})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="trainer">Entrenador</label>
            <select
              id="trainer"
              value={selectedTrainer}
              onChange={(e) => setSelectedTrainer(e.target.value)}
              disabled={loading}
              required
            >
              <option value="">Seleccionar entrenador</option>
              {trainers.map((trainer) => (
                <option key={trainer.id} value={trainer.id}>
                  {trainer.first_name} {trainer.last_name}
                </option>
              ))}
            </select>
          </div>

          <button type="submit" className="button-primary" disabled={loading}>
            {loading ? 'Asignando...' : 'Asignar'}
          </button>
        </form>
      </div>

      <div className="dashboard-section">
        <div className="section-header">
          <h2>Asignaciones Actuales</h2>
        </div>
        
        {assignments.length === 0 ? (
          <div className="empty-state">
            <p>No hay asignaciones registradas</p>
          </div>
        ) : (
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Estudiante</th>
                  <th>Entrenador</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {assignments.map((assignment, index) => (
                  <tr key={index}>
                    <td>{assignment.student_name}</td>
                    <td>{assignment.trainer_name}</td>
                    <td>
                      <button
                        onClick={() => handleRemoveAssignment(assignment.student_id, assignment.trainer_id)}
                        className="button-danger-sm"
                        disabled={loading}
                      >
                        Eliminar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default AssignTrainer;