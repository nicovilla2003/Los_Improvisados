import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// Crear instancia de axios con configuración base
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar el token a todas las peticiones
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_role');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ============ AUTH ============
export const login = async (username, password) => {
  const response = await api.post('/auth/login', { username, password });
  return response.data;
};

export const adminLogin = async (username, password) => {
  const response = await api.post('/auth/admin-login', { username, password });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

// ============ STUDENTS ============
export const getAllStudents = async () => {
  const response = await api.get('/students/admin/all');
  return response.data;
};

export const getAssignedStudents = async () => {
  const response = await api.get('/students/assigned');
  return response.data;
};

export const getStudentById = async (studentId) => {
  const response = await api.get(`/students/${studentId}`);
  return response.data;
};

// ============ EXERCISES ============
export const getAllExercises = async () => {
  const response = await api.get('/exercises');
  return response.data;
};

export const getExerciseById = async (exerciseId) => {
  const response = await api.get(`/exercises/${exerciseId}`);
  return response.data;
};

export const createExercise = async (exerciseData) => {
  const response = await api.post('/exercises', exerciseData);
  return response.data;
};

export const updateExercise = async (exerciseId, exerciseData) => {
  const response = await api.put(`/exercises/${exerciseId}`, exerciseData);
  return response.data;
};

export const deleteExercise = async (exerciseId) => {
  const response = await api.delete(`/exercises/${exerciseId}`);
  return response.data;
};

// ============ ROUTINES ============
export const getAllRoutines = async () => {
  const response = await api.get('/routines');
  return response.data;
};

export const getRoutineById = async (routineId) => {
  const response = await api.get(`/routines/${routineId}`);
  return response.data;
};

export const createRoutine = async (routineData) => {
  const response = await api.post('/routines', routineData);
  return response.data;
};

export const updateRoutine = async (routineId, routineData) => {
  const response = await api.put(`/routines/${routineId}`, routineData);
  return response.data;
};

export const deleteRoutine = async (routineId) => {
  const response = await api.delete(`/routines/${routineId}`);
  return response.data;
};

export const assignRoutineToStudent = async (routineId, assignmentData) => {
  const response = await api.post(`/routines/${routineId}/assign`, assignmentData);
  return response.data;
};

// ============ PROGRESS ============
export const getProgressLogs = async (studentId) => {
  const response = await api.get(`/progress/students/${studentId}/logs`);
  return response.data;
};

export const createProgressLog = async (logData) => {
  const response = await api.post('/progress/logs', logData);
  return response.data;
};

export const updateProgressLog = async (logId, logData) => {
  const response = await api.put(`/progress/logs/${logId}`, logData);
  return response.data;
};

export const deleteProgressLog = async (logId) => {
  const response = await api.delete(`/progress/logs/${logId}`);
  return response.data;
};

// ============ TRAINERS ============
export const getAllTrainers = async () => {
  const response = await api.get('/trainers');
  return response.data;
};

export const getTrainerById = async (trainerId) => {
  const response = await api.get(`/trainers/${trainerId}`);
  return response.data;
};

export const getTrainerStudents = async (trainerId) => {
  const response = await api.get(`/trainers/${trainerId}/students`);
  return response.data;
};

export const getTrainerRoutines = async (trainerId) => {
  const response = await api.get(`/trainers/${trainerId}/routines`);
  return response.data;
};

// ============ STATS ============
export const getStudentSummary = async (studentId) => {
  const response = await api.get(`/stats/students/${studentId}/summary`);
  return response.data;
};

export const getProgressByExercise = async (studentId, exerciseId) => {
  const response = await api.get(`/stats/students/${studentId}/progress-by-exercise`, {
    params: { exercise_id: exerciseId }
  });
  return response.data;
};

export const getTrainerSummary = async (trainerId) => {
  const response = await api.get(`/stats/trainers/${trainerId}/students-summary`);
  return response.data;
};

export default api;