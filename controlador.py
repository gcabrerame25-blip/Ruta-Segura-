# ==============================================================================
# PROYECTO: RutaSegura - Sistema de Indicadores de Riesgo Vial
# ARCHIVO: controlador.py
# CAPA: Control (Lógica de Negocio, Autenticación y Gestión de Alertas)
# ==============================================================================

import pandas as pd
from modelo import ModeloRutaSegura


class ControladorRutaSegura:
    def __init__(self):
        self.modelo = ModeloRutaSegura()
        self.UMBRAL_CRITICO_RIESGO = 480.0  # Umbral para disparo de alertas automáticas (RF10)
        
        # Diccionario de credenciales y roles autorizados (RF11 / RNF02)
        self.usuarios_registrados = {
            "jocelin.perez0896@gmail.com": {"clave": "ositran2026", "rol": "Analista OSITRAN"},
            "admin@rutasegura.gob.pe": {"clave": "admin2026", "rol": "Administrador"}
        }

    def autenticar_usuario(self, correo: str, clave: str, rol_solicitado: str):
        """
        Valida las credenciales ingresadas en la pantalla de Login (Capa de Vista).
        """
        if correo in self.usuarios_registrados:
            datos_user = self.usuarios_registrados[correo]
            if datos_user["clave"] == clave and datos_user["rol"] == rol_solicitado:
                return True, "Acceso concedido", datos_user["rol"]
            elif datos_user["clave"] == clave:
                return False, "El rol seleccionado no corresponde a las credenciales.", None
        return False, "Usuario o contraseña incorrectos.", None

    def solicitar_analisis_riesgo(self, df_accidentes: pd.DataFrame, df_flujo: pd.DataFrame):
        """
        Orquesta la llamada a la Capa de Modelo y procesa las alertas críticas.
        """
        # 1. Llamar a la Capa de Modelo para ejecutar el algoritmo EPDO
        df_resultados = self.modelo.calcular_indice_epdo(df_accidentes, df_flujo)

        # 2. Identificar tramos en estado de alerta (RF10)
        alertas_activas = []
        for _, fila in df_resultados.iterrows():
            if fila['indice_riesgo'] >= self.UMBRAL_CRITICO_RIESGO:
                alertas_activas.append({
                    "id_ruta": fila['id_ruta'],
                    "ubicacion": fila['ubicacion'],
                    "concesion": fila['concesion'],
                    "indice": fila['indice_riesgo'],
                    "nivel": "CRÍTICO",
                    "mensaje": f"El tramo supera el umbral de riesgo ({self.UMBRAL_CRITICO_RIESGO}). Requiere intervención."
                })

        return df_resultados, alertas_activas
