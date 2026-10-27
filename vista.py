# ==============================================================================
# PROYECTO: RutaSegura - Sistema de Indicadores de Riesgo Vial
# ARCHIVO: vista.py
# CAPA: Vista (Interfaz Web e Interacción de Usuario)
# Ejecución: streamlit run vista.py
# ==============================================================================

import streamlit as st
import streamlit.components.v1 as components
from controlador import ControladorRutaSegura

# Configuración de página de la aplicación web
st.set_page_config(
    page_title="RutaSegura - OSITRAN", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Ocultar elementos nativos de Streamlit para renderizar la web completa
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding: 0rem !important;}
    </style>
""", unsafe_allow_html=True)

# Instancia de la Capa de Control
controlador = ControladorRutaSegura()

# Código HTML/CSS/JS de la interfaz gráfica replicada desde Figma
CODIGO_WEB_FIGMA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RutaSegura - OSITRAN / SUPERVISIÓN VIAL</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-sidebar: #0b192c;
            --bg-main: #f4f6f9;
            --primary-blue: #1d61f2;
            --primary-hover: #144cc7;
            --card-bg: #ffffff;
            --text-dark: #1e293b;
            --text-muted: #64748b;
            --border-color: #e2e8f0;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; }
        body { background-color: var(--bg-main); color: var(--text-dark); height: 100vh; overflow: hidden; }

        /* PAGE 1: LOGIN (SPLIT SCREEN) */
        #page-login { display: flex; height: 100vh; width: 100vw; }
        .login-left { flex: 1.2; background: linear-gradient(135deg, #071325 0%, #0b192c 100%); color: #ffffff; padding: 3rem; display: flex; flex-direction: column; justify-content: space-between; position: relative; overflow: hidden; }
        .login-left::before { content: ''; position: absolute; top: -100px; right: -100px; width: 500px; height: 500px; border: 2px solid rgba(255, 255, 255, 0.05); border-radius: 50%; }
        .brand-logo { display: flex; align-items: center; gap: 12px; font-weight: 700; font-size: 1.2rem; }
        .brand-logo i { background: var(--primary-blue); color: white; padding: 8px 12px; border-radius: 8px; }
        .login-hero-text { max-width: 500px; z-index: 2; }
        .badge-tag { display: inline-block; background: rgba(29, 97, 242, 0.2); color: #60a5fa; font-size: 0.75rem; font-weight: 700; padding: 4px 12px; border-radius: 20px; letter-spacing: 1px; margin-bottom: 1.5rem; }
        .login-hero-text h1 { font-size: 2.5rem; line-height: 1.2; margin-bottom: 1rem; font-weight: 700; }
        .login-hero-text p { color: #94a3b8; font-size: 1rem; line-height: 1.5; }
        .login-footer-left { color: #64748b; font-size: 0.8rem; }
        .login-right { flex: 1; background: #ffffff; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 3rem; }
        .login-card { width: 100%; max-width: 380px; }
        .login-header-right span { color: var(--primary-blue); font-size: 0.75rem; font-weight: 700; letter-spacing: 1px; }
        .login-header-right h2 { font-size: 1.8rem; color: var(--text-dark); margin-top: 4px; margin-bottom: 6px; }
        .login-header-right p { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 2rem; }
        .form-group { margin-bottom: 1.2rem; }
        .form-group label { display: block; font-size: 0.8rem; font-weight: 600; color: var(--text-dark); margin-bottom: 6px; }
        .form-control { width: 100%; padding: 12px 14px; border: 1px solid var(--border-color); background: #f8fafc; border-radius: 8px; font-size: 0.9rem; color: var(--text-dark); outline: none; transition: all 0.2s; }
        .form-control:focus { border-color: var(--primary-blue); background: #ffffff; box-shadow: 0 0 0 3px rgba(29, 97, 242, 0.1); }
        .btn-primary { width: 100%; padding: 12px; background: var(--primary-blue); color: white; border: none; border-radius: 8px; font-size: 0.95rem; font-weight: 600; cursor: pointer; transition: background 0.2s; margin-top: 0.5rem; }
        .btn-primary:hover { background: var(--primary-hover); }
        .joint-initiative { margin-top: 3rem; text-align: center; border-top: 1px solid var(--border-color); padding-top: 1.5rem; }
        .joint-initiative span { font-size: 0.7rem; color: var(--text-muted); letter-spacing: 1px; font-weight: 600; }
        .joint-logos { display: flex; justify-content: center; gap: 20px; margin-top: 8px; font-size: 0.85rem; font-weight: 700; color: #475569; }

        /* APP LAYOUT (SIDEBAR + MAIN) */
        #page-app { display: none; height: 100vh; width: 100vw; }
        .sidebar { width: 250px; background: var(--bg-sidebar); color: #94a3b8; display: flex; flex-direction: column; justify-content: space-between; padding: 1.5rem 1rem; }
        .sidebar-brand { color: white; padding: 0 0.5rem 1.5rem 0.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
        .sidebar-menu { list-style: none; margin-top: 1.5rem; }
        .sidebar-item { margin-bottom: 6px; }
        .sidebar-link { display: flex; align-items: center; gap: 12px; padding: 10px 14px; color: #94a3b8; text-decoration: none; border-radius: 8px; font-size: 0.88rem; font-weight: 500; transition: all 0.2s; cursor: pointer; }
        .sidebar-link:hover, .sidebar-link.active { background: var(--primary-blue); color: #ffffff; }
        .sidebar-help-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 1rem; font-size: 0.75rem; margin-bottom: 1rem; }
        .sidebar-help-card h5 { color: white; margin-bottom: 4px; }
        .sidebar-help-card a { color: #60a5fa; text-decoration: none; font-weight: 600; display: inline-block; margin-top: 8px; }
        .logout-btn { display: flex; align-items: center; gap: 10px; color: #94a3b8; font-size: 0.85rem; cursor: pointer; padding: 8px; }
        .logout-btn:hover { color: white; }
        .main-content { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }
        .top-navbar { background: #ffffff; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); }
        .top-navbar-title span { font-size: 0.75rem; color: var(--primary-blue); font-weight: 700; letter-spacing: 0.5px; }
        .top-navbar-title h2 { font-size: 1.3rem; color: var(--text-dark); }
        .top-navbar-actions { display: flex; align-items: center; gap: 20px; }
        .search-box { position: relative; }
        .search-box input { padding: 8px 12px 8px 36px; border: 1px solid var(--border-color); background: #f8fafc; border-radius: 20px; font-size: 0.82rem; width: 220px; }
        .search-box i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; font-size: 0.85rem; }
        .user-profile { display: flex; align-items: center; gap: 10px; }
        .avatar { width: 36px; height: 36px; background: var(--primary-blue); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 700; }
        .user-info h4 { font-size: 0.85rem; color: var(--text-dark); }
        .user-info p { font-size: 0.72rem; color: var(--text-muted); }
        .dashboard-body { padding: 1.8rem 2rem; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2rem; margin-bottom: 1.5rem; }
        .kpi-card { background: var(--card-bg); border-radius: 12px; padding: 1.2rem 1.5rem; border: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: flex-start; }
        .kpi-info span { font-size: 0.8rem; color: var(--text-muted); font-weight: 500; }
        .kpi-info h3 { font-size: 1.8rem; color: var(--text-dark); margin: 6px 0; }
        .kpi-info p { font-size: 0.75rem; color: var(--text-muted); }
        .kpi-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; }
        .kpi-icon.blue { background: #eff6ff; color: var(--primary-blue); }
        .kpi-icon.red { background: #fef2f2; color: var(--danger-color); }
        .kpi-icon.green { background: #ecfdf5; color: var(--success-color); }
        .middle-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 1.2rem; margin-bottom: 1.5rem; }
        .card-panel { background: var(--card-bg); border-radius: 12px; border: 1px solid var(--border-color); padding: 1.2rem 1.5rem; }
        .panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
        .panel-header h3 { font-size: 0.95rem; color: var(--text-dark); }
        .panel-header p { font-size: 0.75rem; color: var(--text-muted); }
        .badge-filter { background: #f1f5f9; color: var(--text-dark); padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; border: 1px solid var(--border-color); }
        .map-placeholder { height: 220px; background: #f8fafc; border-radius: 8px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; border: 1px dashed var(--border-color); }
        .map-dots-container { width: 100%; height: 100%; position: relative; }
        .map-dot { position: absolute; width: 12px; height: 12px; border-radius: 50%; background: var(--success-color); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0.2); }
        .table-ranking { width: 100%; border-collapse: collapse; }
        .table-ranking tr { border-bottom: 1px solid var(--border-color); }
        .table-ranking td { padding: 10px 0; font-size: 0.8rem; }
        .table-main { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        .table-main th { text-align: left; font-size: 0.72rem; color: var(--text-muted); padding: 8px 12px; background: #f8fafc; text-transform: uppercase; }
        .table-main td { padding: 12px; font-size: 0.82rem; border-bottom: 1px solid var(--border-color); }
        .status-tag { padding: 3px 10px; border-radius: 12px; font-size: 0.72rem; font-weight: 600; }
        .status-tag.safe { background: #d1fae5; color: #065f46; }
        .upload-box { border: 2px dashed #cbd5e1; background: #f8fafc; border-radius: 12px; padding: 2.5rem; text-align: center; margin-top: 1rem; cursor: pointer; transition: all 0.2s; }
        .upload-box:hover { border-color: var(--primary-blue); background: #f1f5f9; }
        .upload-box i { font-size: 2rem; color: var(--primary-blue); background: #dbeafe; padding: 1rem; border-radius: 50%; margin-bottom: 1rem; }
        .terminal-box { background: #0f172a; color: #f8fafc; font-family: 'Courier New', Courier, monospace; padding: 1.2rem; border-radius: 8px; font-size: 0.8rem; margin-top: 1rem; line-height: 1.6; }
        .terminal-line.success { color: #4ade80; }
        .terminal-line.info { color: #38bdf8; }
        .terminal-line.warning { color: #facc15; }
    </style>
</head>
<body>
    <!-- PAGE 1: LOGIN -->
    <div id="page-login">
        <div class="login-left">
            <div class="brand-logo">
                <i class="fa-solid fa-route"></i>
                <span>RutaSegura<br><small style="font-size: 0.65rem; color: #94a3b8;">OSITRAN</small></span>
            </div>
            <div class="login-hero-text">
                <span class="badge-tag">INTELIGENCIA VIAL</span>
                <h1>Decisiones más seguras para las carreteras del Perú.</h1>
                <p>Sistema de Indicadores de Riesgo Vial para Tramos Concesionados.</p>
            </div>
            <div class="login-footer-left">© 2026 OSITRAN · República del Perú</div>
        </div>
        <div class="login-right">
            <div class="login-card">
                <div class="login-header-right">
                    <span>BIENVENIDO</span>
                    <h2>Iniciar Sesión</h2>
                    <p>Accede con tus credenciales institucionales.</p>
                </div>
                <form id="form-login">
                    <div class="form-group">
                        <label>Correo institucional / Usuario</label>
                        <input type="text" class="form-control" value="jocelin.perez0896@gmail.com" required>
                    </div>
                    <div class="form-group">
                        <label>Contraseña</label>
                        <input type="password" class="form-control" value="••••••••••••" required>
                    </div>
                    <div class="form-group">
                        <label>Rol de acceso</label>
                        <select id="select-rol" class="form-control">
                            <option value="Analista OSITRAN">Analista OSITRAN</option>
                            <option value="Administrador">Administrador</option>
                        </select>
                    </div>
                    <button type="submit" class="btn-primary">Ingresar al Sistema</button>
                </form>
                <div class="joint-initiative">
                    <span>UNA INICIATIVA CONJUNTA</span>
                    <div class="joint-logos">
                        <span>OSITRAN</span>
                        <span>MTC <small>PERÚ</small></span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- PAGE 2: APP MAIN -->
    <div id="page-app">
        <div class="sidebar">
            <div>
                <div class="sidebar-brand brand-logo">
                    <i class="fa-solid fa-route"></i>
                    <span>RutaSegura<br><small style="font-size: 0.65rem; color: #94a3b8;">OSITRAN</small></span>
                </div>
                <ul class="sidebar-menu">
                    <li class="sidebar-item"><a class="sidebar-link active" onclick="switchTab('tab-inicio', this)"><i class="fa-solid fa-house"></i> Inicio</a></li>
                    <li class="sidebar-item"><a class="sidebar-link" onclick="switchTab('tab-mapa', this)"><i class="fa-solid fa-map"></i> Mapa de Riesgos</a></li>
                    <li class="sidebar-item"><a class="sidebar-link" onclick="switchTab('tab-stats', this)"><i class="fa-solid fa-chart-simple"></i> Estadísticas</a></li>
                    <li class="sidebar-item"><a class="sidebar-link" onclick="switchTab('tab-gestion', this)"><i class="fa-solid fa-database"></i> Gestión de Datos</a></li>
                    <li class="sidebar-item"><a class="sidebar-link" onclick="switchTab('tab-perfil', this)"><i class="fa-solid fa-user"></i> Perfil</a></li>
                </ul>
            </div>
            <div>
                <div class="sidebar-help-card">
                    <h5>Centro de ayuda</h5>
                    <p>¿Necesitas asistencia con la plataforma?</p>
                    <a href="#">Contactar soporte</a>
                </div>
                <div class="logout-btn" onclick="logout()"><i class="fa-solid fa-arrow-right-from-bracket"></i><span>Cerrar sesión</span></div>
            </div>
        </div>

        <div class="main-content">
            <div class="top-navbar">
                <div class="top-navbar-title">
                    <span>OSITRAN · SUPERVISIÓN VIAL</span>
                    <h2 id="navbar-title-text">Panel de Control del Índice de Riesgo</h2>
                </div>
                <div class="top-navbar-actions">
                    <div class="search-box"><i class="fa-solid fa-magnifying-glass"></i><input type="text" placeholder="Buscar ruta o ubicación"></div>
                    <div class="user-profile">
                        <div class="avatar">AM</div>
                        <div class="user-info">
                            <h4>Andrea Morales</h4>
                            <p id="user-role-label">Analista OSITRAN</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="dashboard-body">
                <div id="tab-inicio" class="tab-content active">
                    <div class="kpi-grid">
                        <div class="kpi-card">
                            <div class="kpi-info"><span>Total de Rutas Analizadas</span><h3 id="kpi-rutas">64</h3><p>Archivo procesado correctamente</p></div>
                            <div class="kpi-icon blue"><i class="fa-solid fa-road"></i></div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-info"><span>Alertas Críticas Activas</span><h3 id="kpi-alertas">0</h3><p>Sin alertas registradas</p></div>
                            <div class="kpi-icon red"><i class="fa-solid fa-triangle-exclamation"></i></div>
                        </div>
                        <div class="kpi-card">
                            <div class="kpi-info"><span>Última actualización de BD</span><h3 id="kpi-fecha">26/10/26, 11:22 p. m.</h3><p>Sincronización exitosa</p></div>
                            <div class="kpi-icon green"><i class="fa-solid fa-clock"></i></div>
                        </div>
                    </div>

                    <div class="middle-grid">
                        <div class="card-panel">
                            <div class="panel-header"><div><h3>Mapa de calor de incidentes</h3><p>Concentración de riesgo en la red concesionada</p></div><span class="badge-filter">Últimos 30 días</span></div>
                            <div class="map-placeholder">
                                <div class="map-dots-container">
                                    <div class="map-dot" style="top: 30%; left: 20%;"></div>
                                    <div class="map-dot" style="top: 40%; left: 35%;"></div>
                                    <div class="map-dot" style="top: 55%; left: 40%;"></div>
                                    <div class="map-dot" style="top: 45%; left: 60%;"></div>
                                </div>
                            </div>
                        </div>
                        <div class="card-panel">
                            <div class="panel-header"><div><h3>Top 5 Rutas Peligrosas</h3><p>Índice de riesgo acumulado</p></div></div>
                            <table class="table-ranking">
                                <tr><td>1. Ubicación no especificada</td><td align="right"><b>0%</b></td></tr>
                                <tr><td>2. Ubicación no especificada</td><td align="right"><b>0%</b></td></tr>
                                <tr><td>3. Ubicación no especificada</td><td align="right"><b>0%</b></td></tr>
                                <tr><td>4. Ubicación no especificada</td><td align="right"><b>0%</b></td></tr>
                                <tr><td>5. Ubicación no especificada</td><td align="right"><b>0%</b></td></tr>
                            </table>
                        </div>
                    </div>

                    <div class="card-panel">
                        <div class="panel-header"><div><h3>Monitoreo de rutas</h3><p>Detalle actualizado del Índice de riesgo vial</p></div></div>
                        <table class="table-main">
                            <thead><tr><th>ID RUTA</th><th>UBICACIÓN</th><th>ÍNDICE DE RIESGO</th><th>ESTADO</th></tr></thead>
                            <tbody>
                                <tr><td><b>RV-001</b></td><td>Ubicación no especificada</td><td>0%</td><td><span class="status-tag safe">Seguro</span></td></tr>
                                <tr><td><b>RV-002</b></td><td>Ubicación no especificada</td><td>0%</td><td><span class="status-tag safe">Seguro</span></td></tr>
                                <tr><td><b>RV-003</b></td><td>Ubicación no especificada</td><td>0%</td><td><span class="status-tag safe">Seguro</span></td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div id="tab-gestion" class="tab-content">
                    <div class="card-panel" style="margin-bottom: 1.5rem;">
                        <div class="panel-header"><div><h3>Carga de Datos</h3><p>Columnas: ID Ruta, Ubicación, Índice de Riesgo y Estado.</p></div></div>
                        <div class="upload-box" onclick="alert('Dataset cargado en el motor.')">
                            <i class="fa-solid fa-cloud-arrow-up"></i>
                            <h4>Arrastra y suelta tu archivo aquí</h4>
                            <p>o haz clic para seleccionar · Excel o CSV, máximo 25 MB</p>
                        </div>
                    </div>
                    <div class="card-panel">
                        <div class="panel-header"><div><h3>Registro de actividad del sistema</h3><p>Ejecuciones y procesos recientes</p></div><span class="badge-filter" style="background: #ecfdf5; color: var(--success-color);">EN VIVO</span></div>
                        <div class="terminal-box">
                            <div class="terminal-line success">[09:42:08] SUCCESS Triggers de SQL Server ejecutados</div>
                            <div class="terminal-line success">[09:42:10] SUCCESS Modelo de Python actualizado</div>
                            <div class="terminal-line info">[09:42:11] INFO 248 rutas validadas correctamente</div>
                        </div>
                    </div>
                </div>
                <div id="tab-mapa" class="tab-content"><div class="card-panel"><h3>Vista del Mapa Geoespacial Completo</h3></div></div>
                <div id="tab-stats" class="tab-content"><div class="card-panel"><h3>Módulo de Estadísticas y Reportes PDF/Excel</h3></div></div>
                <div id="tab-perfil" class="tab-content"><div class="card-panel"><h3>Ajustes del Usuario y Permisos</h3></div></div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('form-login').addEventListener('submit', function(e) {
            e.preventDefault();
            const rol = document.getElementById('select-rol').value;
            document.getElementById('user-role-label').innerText = rol;
            document.getElementById('page-login').style.display = 'none';
            document.getElementById('page-app').style.display = 'flex';
        });

        function logout() {
            document.getElementById('page-app').style.display = 'none';
            document.getElementById('page-login').style.display = 'flex';
        }

        function switchTab(tabId, element) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.sidebar-link').forEach(link => link.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            element.classList.add('active');
        }
    </script>
</body>
</html>
"""

# Renderizar la interfaz web completa en la Capa de Vista
components.html(CODIGO_WEB_FIGMA, height=900, scrolling=True)
