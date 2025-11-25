import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAllStudents } from '../services/api';
import '../styles/Dashboard.css';

const StudentsListPage = () => {
  const navigate = useNavigate();
  const [students, setStudents] = useState([]);
  const [filteredStudents, setFilteredStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadStudents();
  }, []);

  useEffect(() => {
    filterStudents();
  }, [searchTerm, students]);

  const loadStudents = async () => {
    try {
      setLoading(true);
      const data = await getAllStudents();
      setStudents(data);
      setFilteredStudents(data);
    } catch (error) {
      console.error('Error cargando estudiantes:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterStudents = () => {
    if (!searchTerm) {
      setFilteredStudents(students);
      return;
    }

    const term = searchTerm.toLowerCase();
    const filtered = students.filter(student =>
      student.first_name.toLowerCase().includes(term) ||
      student.last_name.toLowerCase().includes(term) ||
      student.email.toLowerCase().includes(term) ||
      student.id.toLowerCase().includes(term)
    );
    setFilteredStudents(filtered);
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
        <h1>Estudiantes</h1>
        <p>Listado completo de estudiantes registrados</p>
      </header>

      <div className="form-card">
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label htmlFor="search">Buscar Estudiante</label>
          <input
            type="text"
            id="search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar por nombre, email o código..."
            style={{ maxWidth: '500px' }}
          />
        </div>
      </div>

      <div className="dashboard-section">
        <div className="section-header">
          <h2>Estudiantes Encontrados ({filteredStudents.length})</h2>
        </div>

        {filteredStudents.length === 0 ? (
          <div className="empty-state">
            <p>No se encontraron estudiantes</p>
          </div>
        ) : (
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Nombre</th>
                  <th>Email</th>
                  <th>Fecha de Nacimiento</th>
                  <th>Campus</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredStudents.map((student) => (
                  <tr key={student.id}>
                    <td style={{ fontWeight: '600' }}>{student.id}</td>
                    <td>{student.first_name} {student.last_name}</td>
                    <td>{student.email}</td>
                    <td>{new Date(student.birth_date).toLocaleDateString('es-ES')}</td>
                    <td>Campus {student.campus_code}</td>
                    <td>
                      <button
                        onClick={() => navigate(`/admin/students/${student.id}`)}
                        className="button-secondary"
                        style={{ padding: '6px 12px', fontSize: '13px' }}
                      >
                        Ver Detalles
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

export default StudentsListPage;