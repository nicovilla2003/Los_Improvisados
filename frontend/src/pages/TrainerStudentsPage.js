import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAssignedStudents } from '../services/api';
import '../styles/Dashboard.css';

const TrainerStudentsPage = () => {
  const navigate = useNavigate();
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadStudents();
  }, []);

  const loadStudents = async () => {
    try {
      setLoading(true);
      const data = await getAssignedStudents();
      setStudents(data);
    } catch (error) {
      console.error('Error cargando estudiantes:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredStudents = students.filter(student =>
    !searchTerm ||
    student.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
        <h1>Mis Estudiantes</h1>
        <p>Estudiantes asignados a tu cargo</p>
      </header>

      <div className="form-card">
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label htmlFor="search">Buscar Estudiante</label>
          <input
            type="text"
            id="search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar por nombre o email..."
            style={{ maxWidth: '500px' }}
          />
        </div>
      </div>

      <div className="dashboard-section">
        <div className="section-header">
          <h2>Estudiantes Asignados ({filteredStudents.length})</h2>
        </div>

        {filteredStudents.length === 0 ? (
          <div className="empty-state">
            <p>No tienes estudiantes asignados</p>
          </div>
        ) : (
          <div className="students-grid">
            {filteredStudents.map((student) => (
              <div
                key={student.id}
                style={{ cursor: 'pointer' }}
              >
                <div 
                  className="student-card"
                  onClick={() => navigate(`/trainer/students/${student.id}/progress`)}
                >
                  <div className="student-avatar">
                    {student.first_name[0]}{student.last_name[0]}
                  </div>
                  <div className="student-info">
                    <h4>{student.first_name} {student.last_name}</h4>
                    <p>{student.email}</p>
                    <p style={{ fontSize: '12px', color: '#9ca3af', marginTop: '4px' }}>
                      Código: {student.id}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TrainerStudentsPage;