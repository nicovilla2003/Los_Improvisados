import React, { useState } from "react";
import "./App.css";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Aquí luego llamaremos al backend:
    // fetch("http://127.0.0.1:8000/auth/login", {...})
    console.log("Login enviado:", { username, password });
  };

  return (
    <div className="App">
      <div className="login-page">
        {/* Lado izquierdo con imagen */}
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

        {/* Lado derecho con el formulario */}
        <div className="login-right">
          <div className="login-right-inner">
            <header className="login-header">
              <h2 className="login-header-title">Login Gym Icesi</h2>
            </header>

            <main className="login-card">
              <h1 className="login-title">Inicia sesión</h1>

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
                  />
                </div>

                <button type="submit" className="login-submit-button">
                  Ingresar
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

export default App;