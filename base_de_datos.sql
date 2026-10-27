-- ============================================================================
-- PROYECTO: RutaSegura (2022-2025)
-- MOTOR: Microsoft SQL Server
-- MODELO FÍSICO: Alineado al Excel "RutaSegura_Datos_Normalizados_2022_2025_v2"
-- ============================================================================

USE master;
GO

-- 1. Crear Base de Datos (Si existe, la recrea limpia)
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'BD_RutaSegura')
BEGIN
    ALTER DATABASE BD_RutaSegura SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE BD_RutaSegura;
END
GO

CREATE DATABASE BD_RutaSegura;
GO

USE BD_RutaSegura;
GO

-- =======================================================
-- 2. CREACIÓN DE TABLAS DIMENSIONALES (MAESTRAS)
-- =======================================================

CREATE TABLE DIM_CONCESION (
    id_concesion INT IDENTITY(1,1) NOT NULL,
    siglas VARCHAR(20) NULL,             
    nombre_concesion VARCHAR(250) NOT NULL, 
    CONSTRAINT PK_CONCESION PRIMARY KEY (id_concesion)
);

CREATE TABLE DIM_TRAMO_RED_VIAL (
    id_rvn INT NOT NULL,                 
    id_concesion INT NULL,               
    departamento VARCHAR(100) NULL,      
    codigo_ruta VARCHAR(50) NULL,        
    trayectoria VARCHAR(500) NULL,       
    km_inicio DECIMAL(10,3) NULL,        
    km_final DECIMAL(10,3) NULL,         
    longitud DECIMAL(10,3) NULL,         
    nro_carriles INT NULL,               
    superficie VARCHAR(100) NULL,        
    estado VARCHAR(100) NULL,            
    CONSTRAINT PK_TRAMO PRIMARY KEY (id_rvn),
    CONSTRAINT FK_TRAMO_CONCESION FOREIGN KEY (id_concesion) REFERENCES DIM_CONCESION(id_concesion)
);

CREATE TABLE DIM_PEAJE (
    codigo_peaje VARCHAR(50) NOT NULL,   
    nombre_peaje VARCHAR(150) NOT NULL,  
    departamento VARCHAR(100) NOT NULL,  
    administracion VARCHAR(100) NULL,    
    CONSTRAINT PK_PEAJE PRIMARY KEY (codigo_peaje)
);

-- =======================================================
-- 3. CREACIÓN DE TABLAS DE HECHOS (TRANSACCIONALES)
-- =======================================================

CREATE TABLE HECHO_ACCIDENTES (
    id_accidente INT IDENTITY(1,1) NOT NULL,
    id_concesion INT NULL,               
    anio INT NOT NULL,                   
    mes INT NOT NULL,                    
    tipo_accidente VARCHAR(150) NULL,    
    causa_accidente VARCHAR(250) NULL,   
    tipo_transporte VARCHAR(150) NULL,   
    tipo_vehiculo VARCHAR(150) NULL,     
    clima VARCHAR(50) NULL,              
    tramo_referencia VARCHAR(250) NULL,  
    cantidad_veh_involucrados INT NULL,  
    cantidad_afectados INT NULL,         
    CONSTRAINT PK_ACCIDENTE PRIMARY KEY (id_accidente),
    CONSTRAINT FK_ACCIDENTE_CONCESION FOREIGN KEY (id_concesion) REFERENCES DIM_CONCESION(id_concesion)
);

CREATE TABLE HECHO_FLUJO_VEHICULAR (
    id_flujo INT IDENTITY(1,1) NOT NULL,
    codigo_peaje VARCHAR(50) NOT NULL,   
    anio INT NOT NULL,                   
    mes INT NOT NULL,                    
    periodo INT NOT NULL,                
    veh_ligeros_total INT DEFAULT 0,     
    veh_pesados_total INT DEFAULT 0,     
    veh_total INT DEFAULT 0,             
    veh_imd INT DEFAULT 0,               
    CONSTRAINT PK_FLUJO PRIMARY KEY (id_flujo),
    CONSTRAINT FK_FLUJO_PEAJE FOREIGN KEY (codigo_peaje) REFERENCES DIM_PEAJE(codigo_peaje)
);
GO

PRINT '¡Éxito! Base de datos BD_RutaSegura y todas las tablas han sido creadas correctamente.';


USE BD_RutaSegura;
GO

-- ============================================================================
-- 1. TRIGGER DE VALIDACIÓN (Para la tabla HECHO_FLUJO_VEHICULAR)
-- ============================================================================
-- Propósito: Evitar que se ingresen cantidades negativas de vehículos.

CREATE TRIGGER TRG_Validar_Flujo_Negativo
ON HECHO_FLUJO_VEHICULAR
AFTER INSERT, UPDATE
AS
BEGIN
    -- Verificamos si hay algún registro con valores menores a cero
    IF EXISTS (
        SELECT 1 
        FROM inserted 
        WHERE veh_ligeros_total < 0 OR veh_pesados_total < 0 OR veh_total < 0
    )
    BEGIN
        -- Si encuentra un error, lanza un mensaje y deshace la transacción
        RAISERROR ('ERROR: No se pueden registrar cantidades de vehículos con valores negativos en el peaje.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO

-- ============================================================================
-- 2. TRIGGER DE AUDITORÍA (Para la tabla HECHO_ACCIDENTES)
-- ============================================================================
-- Primero, creamos una tabla pequeña para guardar el historial de quién registra datos
CREATE TABLE AUDITORIA_ACCIDENTES (
    id_auditoria INT IDENTITY(1,1) PRIMARY KEY,
    id_accidente INT,
    usuario_bd VARCHAR(100),
    fecha_operacion DATETIME,
    accion VARCHAR(50)
);
GO

-- Ahora creamos el trigger que llenará esa tabla automáticamente
CREATE TRIGGER TRG_Auditar_Nuevos_Accidentes
ON HECHO_ACCIDENTES
AFTER INSERT
AS
BEGIN
    -- Se inserta el registro en la tabla de auditoría usando los datos recién cargados (inserted)
    INSERT INTO AUDITORIA_ACCIDENTES (id_accidente, usuario_bd, fecha_operacion, accion)
    SELECT 
        i.id_accidente, 
        SYSTEM_USER, -- Captura el usuario de SQL Server que hizo la carga
        GETDATE(),   -- Captura la fecha y hora exacta
        'NUEVO ACCIDENTE REGISTRADO'
    FROM inserted i;
END;
GO

PRINT '¡Triggers de Validación y Auditoría creados con éxito!';
