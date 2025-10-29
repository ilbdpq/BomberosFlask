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
    user             TEXT    NOT NULL UNIQUE,
    pass             TEXT    NOT NULL,
    apellido_nombre  TEXT    NOT NULL,
    telefono         INTEGER NOT NULL,
    fecha_nacimiento TEXT    NOT NULL,
    provincia        TEXT NOT NULL,
    lugar            TEXT NOT NULL
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
CREATE INDEX idx_personal_dni ON personal(dni);
CREATE INDEX idx_personal_user ON personal(user);
CREATE INDEX idx_conductas_legajo ON conductas(legajo);
CREATE INDEX idx_asistencias_cab_evento ON asistencias_cab(id_evento);
CREATE INDEX idx_asistencias_cab_responsable ON asistencias_cab(legajo_responsable);
CREATE INDEX idx_asistencias_det_cab ON asistencias_det(id_cab);
CREATE INDEX idx_asistencias_det_legajo ON asistencias_det(legajo);
CREATE INDEX idx_asistencias_det_unidad ON asistencias_det(id_unidad);