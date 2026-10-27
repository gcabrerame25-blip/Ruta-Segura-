# ==============================================================================
# PROYECTO: RutaSegura - Sistema de Indicadores de Riesgo Vial
# ARCHIVO: modelo.py
# CAPA: Modelo (Limpieza ETL y Algoritmo de Severidad EPDO)
# ==============================================================================

import pandas as pd
import numpy as np


class ModeloRutaSegura:
    def __init__(self):
        # Ponderaciones oficiales según metodología HSM / AASHTO
        self.PESO_FALLECIDO = 12
        self.PESO_HERIDO = 3
        self.PESO_DANOS_MATERIALES = 1

    def depurar_datos_accidentes(self, df_acc: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia valores nulos o inconsistentes en el dataset de accidentes.
        """
        df = df_acc.copy()
        columnas_severidad = ['fallecidos', 'heridos', 'danos_materiales']
        
        for col in columnas_severidad:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            else:
                df[col] = 0
                
        return df

    def calcular_indice_epdo(self, df_accidentes: pd.DataFrame, df_flujo: pd.DataFrame) -> pd.DataFrame:
        """
        Ejecuta la fórmula EPDO y normaliza el riesgo cruzando la gravedad
        de los siniestros con el flujo vehicular (IMDA).
        """
        # 1. Limpieza inicial del dataset
        df_acc = self.depurar_datos_accidentes(df_accidentes)
        df_fluj = df_flujo.copy()

        # 2. Ponderación EPDO por registro de accidente
        df_acc['puntos_epdo'] = (
            (df_acc['fallecidos'] * self.PESO_FALLECIDO) +
            (df_acc['heridos'] * self.PESO_HERIDO) +
            (df_acc['danos_materiales'] * self.PESO_DANOS_MATERIALES)
        )

        # 3. Agrupación por Concesión y Tramo Vial
        resumen_accidentes = df_acc.groupby(['id_ruta', 'ubicacion', 'concesion']).agg(
            total_fallecidos=('fallecidos', 'sum'),
            total_heridos=('heridos', 'sum'),
            puntos_epdo_totales=('puntos_epdo', 'sum')
        ).reset_index()

        resumen_flujo = df_fluj.groupby('concesion').agg(
            flujo_vehicular_total=('veh_total', 'sum')
        ).reset_index()

        # 4. Cruce de Datasets y Normalización
        df_unificado = pd.merge(
            resumen_accidentes, 
            resumen_flujo, 
            on='concesion', 
            how='left'
        ).fillna({'flujo_vehicular_total': 1})

        # Cálculo normalizado: (Puntos EPDO acumulados / Flujo Vehicular Total) * 1,000,000 de vehículos
        df_unificado['indice_riesgo'] = np.where(
            df_unificado['flujo_vehicular_total'] > 0,
            (df_unificado['puntos_epdo_totales'] / df_unificado['flujo_vehicular_total']) * 1000000,
            0
        )

        # Redondeo y asignación de Estado
        df_unificado['indice_riesgo'] = df_unificado['indice_riesgo'].round(2)
        df_unificado['estado'] = df_unificado['indice_riesgo'].apply(
            lambda val: 'Crítico' if val >= 480 else ('Medio' if val >= 250 else 'Seguro')
        )

        return df_unificado.sort_values(by='indice_riesgo', ascending=False)
