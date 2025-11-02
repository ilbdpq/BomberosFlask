DROP TABLE IF EXISTS personal;
DROP TABLE IF EXISTS unidades;
DROP TABLE IF EXISTS eventos;
DROP TABLE IF EXISTS conductas;
DROP TABLE IF EXISTS asistencias_cab;
DROP TABLE IF EXISTS asistencias_det;

-- Tabla personal
CREATE TABLE personal (
    legajo           TEXT    PRIMARY KEY UNIQUE,
    dni              INTEGER NOT NULL UNIQUE,
    username         TEXT    NOT NULL UNIQUE,
    password         TEXT    NOT NULL,
    apellido_nombre  TEXT    NOT NULL,
    telefono         INTEGER,
    fecha_nacimiento TEXT    NOT NULL,
    provincia        TEXT    NOT NULL,
    lugar            TEXT    NOT NULL,
    permisos         INTEGER NOT NULL DEFAULT 0
);

-- Tabla unidades
CREATE TABLE unidades (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT    NOT NULL,
    estado INTEGER NOT NULL DEFAULT 1
);

-- Tabla eventos
CREATE TABLE eventos (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT    NOT NULL,
    puntos REAL    NOT NULL
);

-- Tabla conductas
CREATE TABLE conductas (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    legajo TEXT    NOT NULL,
    fecha  TEXT    NOT NULL,
    punto  INTEGER NOT NULL
);

-- Tablas asistencias
CREATE TABLE asistencias_cab (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    id_evento          INTEGER NOT NULL,
    fecha_creada       TEXT    NOT NULL,
    fecha_aceptada     TEXT,
    legajo_responsable TEXT,
    descripcion        TEXT,
    FOREIGN KEY (id_evento) REFERENCES eventos(id),
    FOREIGN KEY (legajo_responsable) REFERENCES personal(legajo)
);

CREATE TABLE asistencias_det (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cab    INTEGER NOT NULL,
    legajo    TEXT    NOT NULL,
    id_unidad INTEGER,
    estado    INTEGER NOT NULL,
    FOREIGN KEY (id_cab) REFERENCES asistencias_cab(id),
    FOREIGN KEY (legajo) REFERENCES personal(legajo),
    FOREIGN KEY (id_unidad) REFERENCES unidades(id)
);

-- Indices
CREATE INDEX idx_personal_user ON personal(username);
CREATE INDEX idx_personal_legajo ON personal(legajo);
CREATE INDEX idx_personal_dni ON personal(dni);
CREATE INDEX idx_conductas_legajo ON conductas(legajo);
CREATE INDEX idx_asistencias_cab_evento ON asistencias_cab(id_evento);
CREATE INDEX idx_asistencias_cab_responsable ON asistencias_cab(legajo_responsable);
CREATE INDEX idx_asistencias_det_cab ON asistencias_det(id_cab);
CREATE INDEX idx_asistencias_det_legajo ON asistencias_det(legajo);
CREATE INDEX idx_asistencias_det_unidad ON asistencias_det(id_unidad);

-- Datos iniciales
INSERT INTO personal (legajo, dni, username, password, apellido_nombre, telefono, fecha_nacimiento, provincia, lugar, permisos) VALUES
('033-072-R7', 43767657, 'gfprimo', 'admin', 'Primo, Gianfranco', NULL, '2001-12-05', 'Santa Fe', 'Totoras', 2),
('033-040-R7', 29260710, 'gvignatti', 'admin', 'Vignatti, Giuliano', NULL, '1994-06-16', 'Santa Fe', 'Totoras', 2),
('033-042-R7', 26112825, 'pelli', 'user', 'Valor, Juan Manual', NULL, '1982-09-26', 'Santa Fe', 'Totoras', 1),
('033-043-R7', 36467096, 'kokan', 'user', 'Nocioni, Franco', NULL, '1977-08-25', 'Santa Fe', 'Totoras', 1),
('033-035-R7', 25205874, 'nocionifranco', 'user', 'Almirón, Abel', NULL, '1992-11-07', 'Santa Fe', 'Totoras', 1);