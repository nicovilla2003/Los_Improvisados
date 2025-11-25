import React, { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { login as apiLogin, adminLogin as apiAdminLogin } from "./services/api";
import Sidebar from "./components/sidebar";

// Pages
import StudentDashboard from "./pages/StudentDashboard";
import TrainerDashboard from "./pages/TrainerDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import AssignTrainer from "./pages/AssignTrainer";
import ExercisesPage from "./pages/ExercisesPage";
import RoutinesPage from "./pages/RoutinesPage";
import NewRoutinePage from "./pages/NewRoutinePage";
import StudentsListPage from "./pages/StudentsListPage";
import TrainerStudentsPage from "./pages/TrainerStudentsPage";
import StudentRoutineProgress from "./pages/StudentRoutineProgress";
import TrainerRoutineProgress from "./pages/TrainerRoutineProgress";

import "./App.css";

// Componente de Login
function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isAdminLogin, setIsAdminLogin] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      let response;
      if (isAdminLogin) {
        response = await apiAdminLogin(username, password);
      } else {
        response = await apiLogin(username, password);
      }

      // Guardar el token y role
      login(response.access_token, response.token_type, isAdminLogin);
      
      // La redirección se manejará automáticamente por el ProtectedRoute
    } catch (err) {
      console.error("Error en login:", err);
      setError(err.response?.data?.detail || "Error al iniciar sesión");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="login-page">
        <div className="login-left">
          <img
            src="/icesi-tower.jpg"
            alt="Torre Universidad Icesi"
            className="login-image"
          />
          <div className="login-left-overlay">
            <img
              src="/icesi-logo-white.png"
              alt="Universidad Icesi"
              className="login-logo"
            />
            <div className="login-left-bottom">
              <div className="login-tagline">Llega más lejos</div>
              <div className="login-site">icesi.edu.co</div>
            </div>
          </div>
        </div>

        <div className="login-right">
          <div className="login-right-inner">
            <header className="login-header">
              <h2 className="login-header-title">
                {isAdminLogin ? "Admin" : "Login"} Gym Icesi
              </h2>
            </header>

            <main className="login-card">
              <h1 className="login-title">Inicia sesión</h1>

              {error && (
                <div style={{
                  padding: "12px",
                  background: "#fee2e2",
                  border: "1px solid #f87171",
                  borderRadius: "6px",
                  color: "#991b1b",
                  marginBottom: "16px",
                  fontSize: "14px"
                }}>
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} className="login-form">
                <div className="login-form-group">
                  <label htmlFor="username">Usuario</label>
                  <input
                    id="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder=""
                    autoComplete="username"
                    required
                    disabled={loading}
                  />
                </div>

                <div className="login-form-group">
                  <label htmlFor="password">Contraseña</label>
                  <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder=""
                    autoComplete="current-password"
                    required
                    disabled={loading}
                  />
                </div>

                <div style={{ marginTop: "12px", marginBottom: "8px" }}>
                  <label style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "14px", cursor: "pointer" }}>
                    <input
                      type="checkbox"
                      checked={isAdminLogin}
                      onChange={(e) => setIsAdminLogin(e.target.checked)}
                      disabled={loading}
                    />
                    Iniciar como administrador
                  </label>
                </div>

                <button type="submit" className="login-submit-button" disabled={loading}>
                  {loading ? "Ingresando..." : "Ingresar"}
                </button>

                <div className="login-extra">
                  <a href="#" className="login-forgot-link">
                    ¿Olvidaste tu contraseña?
                  </a>
                </div>
              </form>
            </main>

            <footer className="login-footer">
              <p>Universidad Icesi, Calle 18 No. 122–135</p>
              <p>
                Cali - Colombia | Teléfono: 555 2334 | Fax: 555 1441<br />
                Copyright © {new Date().getFullYear()}{" "}
                <a
                  href="https://www.icesi.edu.co"
                  target="_blank"
                  rel="noreferrer"
                >
                  www.icesi.edu.co
                </a>
              </p>
            </footer>
          </div>
        </div>
      </div>
    </div>
  );
}

// Componente de Layout con Sidebar
function DashboardLayout({ children }) {
  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#f3f4f6" }}>
      <Sidebar />
      <div style={{ marginLeft: "280px", flex: 1 }}>
        {children}
      </div>
    </div>
  );
}

// Componente de Ruta Protegida
function ProtectedRoute({ children, allowedRoles = [], requireAdmin = false }) {
  const { isAuthenticated, loading, user, isAdmin } = useAuth();
  const role = localStorage.getItem("user_role");

  if (loading) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh" }}>
        Cargando...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (requireAdmin && !isAdmin) {
    return <Navigate to="/" replace />;
  }

  if (allowedRoles.length > 0 && !allowedRoles.includes(role)) {
    return <Navigate to="/" replace />;
  }

  return <DashboardLayout>{children}</DashboardLayout>;
}

// Componente principal de rutas
function AppRoutes() {
  const { isAuthenticated, isAdmin } = useAuth();
  const role = localStorage.getItem("user_role");

  // Determinar la ruta inicial según el rol
  const getDefaultRoute = () => {
    if (!isAuthenticated) return "/login";
    if (isAdmin) return "/admin";
    if (role === "EMPLOYEE") return "/trainer";
    if (role === "STUDENT") return "/student";
    return "/login";
  };

  return (
    <Routes>
      <Route path="/login" element={
        isAuthenticated ? <Navigate to={getDefaultRoute()} replace /> : <LoginPage />
      } />

      {/* Rutas de Estudiante */}
      <Route path="/student" element={
        <ProtectedRoute allowedRoles={["STUDENT"]}>
          <StudentDashboard />
        </ProtectedRoute>
      } />

      <Route path="/student/progress" element={
        <ProtectedRoute allowedRoles={["STUDENT"]}>
          <StudentRoutineProgress />
        </ProtectedRoute>
      } />

      {/* Rutas de Entrenador */}
      <Route path="/trainer" element={
        <ProtectedRoute allowedRoles={["EMPLOYEE"]}>
          <TrainerDashboard />
        </ProtectedRoute>
      } />

      <Route path="/trainer/exercises" element={
        <ProtectedRoute allowedRoles={["EMPLOYEE"]}>
          <ExercisesPage />
        </ProtectedRoute>
      } />

      <Route path="/trainer/routines" element={
        <ProtectedRoute allowedRoles={["EMPLOYEE"]}>
          <RoutinesPage />
        </ProtectedRoute>
      } />

      <Route path="/trainer/routines/new" element={
        <ProtectedRoute allowedRoles={["EMPLOYEE"]}>
          <NewRoutinePage />
        </ProtectedRoute>
      } />

      <Route path="/trainer/students" element={
        <ProtectedRoute allowedRoles={["EMPLOYEE"]}>
          <TrainerStudentsPage />
        </ProtectedRoute>
      } />

      <Route path="/trainer/students/:studentId/progress" element={
        <ProtectedRoute allowedRoles={["EMPLOYEE"]}>
          <TrainerRoutineProgress />
        </ProtectedRoute>
      } />

      {/* Rutas de Administrador */}
      <Route path="/admin" element={
        <ProtectedRoute requireAdmin={true}>
          <AdminDashboard />
        </ProtectedRoute>
      } />
      
      <Route path="/admin/assignments" element={
        <ProtectedRoute requireAdmin={true}>
          <AssignTrainer />
        </ProtectedRoute>
      } />

      <Route path="/admin/students" element={
        <ProtectedRoute requireAdmin={true}>
          <StudentsListPage />
        </ProtectedRoute>
      } />

      {/* Ruta por defecto */}
      <Route path="/" element={<Navigate to={getDefaultRoute()} replace />} />
      
      {/* Ruta 404 */}
      <Route path="*" element={<Navigate to={getDefaultRoute()} replace />} />
    </Routes>
  );
}

// App principal
function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;