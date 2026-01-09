-- Script SQL para Sistema de Analítica Académica y Predicción de Deserción
-- Compatible con PostgreSQL

-- 1. Tabla de Programas Académicos
CREATE TABLE programas_academicos (
    programa_id SERIAL PRIMARY KEY,
    nombre_programa VARCHAR(100) NOT NULL,
    facultad VARCHAR(100) NOT NULL,
    nivel_formacion VARCHAR(50) NOT NULL, -- Pregrado, Posgrado
    total_creditos INTEGER NOT NULL
);

-- 2. Tabla de Estados Académicos (Catálogo)
CREATE TABLE estados_academicos (
    estado_id SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL UNIQUE -- Activo, En Riesgo, Desertor, Graduado
);

-- 3. Tabla de Estudiantes (Anonimizada)
CREATE TABLE estudiantes (
    estudiante_id VARCHAR(50) PRIMARY KEY, -- UUID o Hash anonimizado
    genero CHAR(1) CHECK (genero IN ('M', 'F', 'O')),
    fecha_nacimiento DATE,
    estrato_socioeconomico INTEGER CHECK (estrato_socioeconomico BETWEEN 1 AND 6),
    condicion_laboral VARCHAR(20) DEFAULT 'No trabaja',
    colegio_procedencia VARCHAR(50), -- Público, Privado
    municipio_residencia VARCHAR(100)
);

-- 4. Tabla de Cohortes
CREATE TABLE cohortes (
    cohorte_id SERIAL PRIMARY KEY,
    programa_id INTEGER REFERENCES programas_academicos(programa_id),
    anio INTEGER NOT NULL,
    periodo INTEGER CHECK (periodo IN (1, 2)),
    UNIQUE(programa_id, anio, periodo)
);

-- 5. Tabla de Matrículas Semestrales (Histórico Académico)
CREATE TABLE matriculas_semestrales (
    matricula_id SERIAL PRIMARY KEY,
    estudiante_id VARCHAR(50) REFERENCES estudiantes(estudiante_id),
    cohorte_id INTEGER REFERENCES cohortes(cohorte_id),
    anio_lectivo INTEGER NOT NULL,
    periodo_lectivo INTEGER CHECK (periodo_lectivo IN (1, 2)),
    semestre_ordinal INTEGER NOT NULL, -- 1, 2, 3...
    estado_academico_id INTEGER REFERENCES estados_academicos(estado_id),
    promedio_semestral DECIMAL(3,2),
    promedio_acumulado DECIMAL(3,2),
    creditos_matriculados INTEGER,
    creditos_aprobados INTEGER,
    materias_reprobadas INTEGER DEFAULT 0,
    CONSTRAINT chk_promedio CHECK (promedio_semestral BETWEEN 0 AND 5)
);

-- 6. Tabla de Apoyos Financieros
CREATE TABLE apoyos_financieros (
    apoyo_id SERIAL PRIMARY KEY,
    estudiante_id VARCHAR(50) REFERENCES estudiantes(estudiante_id),
    tipo_apoyo VARCHAR(50) NOT NULL, -- Beca, Crédito, Subsidio
    porcentaje_cobertura DECIMAL(5,2),
    periodo_asignacion VARCHAR(10) -- Ej: 2023-1
);

-- Índices para optimización de consultas analíticas
CREATE INDEX idx_estudiante_matricula ON matriculas_semestrales(estudiante_id);
CREATE INDEX idx_cohorte_matricula ON matriculas_semestrales(cohorte_id);
CREATE INDEX idx_estado_academico ON matriculas_semestrales(estado_academico_id);

-- Inserción de datos maestros iniciales
INSERT INTO estados_academicos (descripcion) VALUES 
('Activo'), ('En Riesgo'), ('Desertor'), ('Graduado'), ('Reserva de Cupo');

INSERT INTO programas_academicos (nombre_programa, facultad, nivel_formacion, total_creditos) VALUES 
('Ingeniería de Sistemas', 'Facultad de Ingeniería', 'Pregrado', 160),
('Ingeniería de Producción', 'Facultad de Ingeniería', 'Pregrado', 155);
