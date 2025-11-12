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
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre  TEXT    NOT NULL,
    patente TEXT    NOT NULL,
    estado  INTEGER NOT NULL DEFAULT 1
);

-- Tabla eventos
CREATE TABLE eventos (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT    NOT NULL,
    puntos REAL    NOT NULL
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

-- Vistas
CREATE VIEW calificaciones AS
    WITH
        cte_eventos AS (
            SELECT
                asistencias_cab.id_evento AS id,
                eventos.puntos,
                COUNT(*) AS total
            FROM
                asistencias_cab
                JOIN eventos ON eventos.id = asistencias_cab.id_evento
            WHERE
                asistencias_cab.fecha_aceptada IS NOT NULL
            GROUP BY
                asistencias_cab.id_evento
        ),
        cte_puntos AS (
            SELECT
                asistencias_det.legajo,
                COUNT(
                    NULLIF(asistencias_det.estado, 0)
                ) AS asistencias,
                cte_eventos.total,
                cte_eventos.puntos
            FROM
                asistencias_cab
                JOIN asistencias_det ON asistencias_det.id_cab = asistencias_cab.id
                JOIN cte_eventos ON cte_eventos.id = asistencias_cab.id_evento
            WHERE
                asistencias_cab.fecha_aceptada IS NOT NULL
            GROUP BY
                asistencias_det.legajo,
                asistencias_cab.id_evento
        )
    SELECT
        personal.apellido_nombre,
        cte_puntos.legajo,
        ROUND(
            SUM(asistencias * 1.0 / total * puntos),
            2
        ) AS puntaje
    FROM
        cte_puntos
    JOIN personal ON personal.legajo = cte_puntos.legajo
    GROUP BY
        cte_puntos.legajo
    ORDER BY
        personal.apellido_nombre;

-- Indices
CREATE INDEX idx_personal_user ON personal(username);
CREATE INDEX idx_personal_legajo ON personal(legajo);
CREATE INDEX idx_personal_dni ON personal(dni);
CREATE INDEX idx_eventos_nombre ON eventos(nombre);
CREATE INDEX idx_asistencias_cab_id ON asistencias_cab(id);
CREATE INDEX idx_asistencias_cab_evento ON asistencias_cab(id_evento);
CREATE INDEX idx_asistencias_cab_responsable ON asistencias_cab(legajo_responsable);
CREATE INDEX idx_asistencias_det_cab ON asistencias_det(id_cab);
CREATE INDEX idx_asistencias_det_legajo ON asistencias_det(legajo);
CREATE INDEX idx_asistencias_det_estado ON asistencias_det(estado);
CREATE INDEX idx_asistencias_det_unidad ON asistencias_det(id_unidad);

-- Datos iniciales
INSERT INTO personal (legajo, dni, username, password, apellido_nombre, telefono, fecha_nacimiento, provincia, lugar, permisos) VALUES
('033-080-R7', 39249172, 'alfeimariano', 'user', 'Alfei, Mariano', NULL, '1995-10-15', 'Santa Fe', 'Totoras', 1),
('033-035-R7', 25205874, 'almironabel', 'user', 'Almirón, Abel Armando', NULL, '1976-09-10', 'Santa Fe', 'Totoras', 1),
('033-083-R7', 46880785, 'almironsofia', 'user', 'Almirón, Sofia', NULL, '2005-10-17', 'Santa Fe', 'Totoras', 1),
('033-079-R7', 41656296, 'bustamantee', 'user', 'Bustamante, Emanuel Luis', NULL, '1999-06-22', 'Santa Fe', 'Totoras', 1),
('033-077-R7', 45267098, 'fontanaignacio', 'user', 'Fontana, Ignacio', NULL, '2003-12-10', 'Santa Fe', 'Totoras', 1),
('033-071-R7', 43492823, 'frattarigiuliana', 'user', 'Frattari, Giuliana Belen', NULL, '2001-08-17', 'Santa Fe', 'Totoras', 1),
('033-063-R7', 38086700, 'gonzalezgerman', 'user', 'Gonzalez, German Jesus', NULL, '1994-09-19', 'Santa Fe', 'San Genaro', 1),
('033-056-R7', 31435074, 'martinandres', 'user', 'Martin, Andres', NULL, '1985-04-02', 'Santa Fe', 'Totoras', 1),
('033-085-R7', 32114053, 'mirandamariana', 'user', 'Miranda, Mariana Betsabe', NULL, '1986-03-17', 'Santa Fe', 'Totoras', 1),
('033-043-R7', 36467096, 'nocionifranco', 'user', 'Nocioni, Franco', NULL, '1992-11-07', 'Santa Fe', 'Totoras', 1),
('033-062-R7', 40117507, 'ocampomaria', 'user', 'Ocampo, Maria del Rosario', NULL, '1997-01-31', 'Santa Fe', 'Cañada de Gómez', 1),
('033-084-R7', 43492869, 'ortizdaiana', 'user', 'Ortiz, Daiana Jazmin', NULL, '2002-01-30', 'Santa Fe', 'Totoras', 1),
('033-040-R7', 29260710, 'pelli', 'user', 'Pelli, Oscar Norberto', NULL, '1982-09-26', 'Santa Fe', 'Totoras', 1),
('033-072-R7', 43767657, 'gfprimo', 'admin', 'Primo, Gianfranco', NULL, '2001-12-05', 'Santa Fe', 'Totoras', 2),
('033-086-R7', 46998769, 'riosmaximo', 'user', 'Rios, Maximo Ian', NULL, '2006-06-13', 'Santa Fe', 'Totoras', 1),
('033-047-R7', 39248648, 'roldanfacundo', 'user', 'Roldan, Facundo Nicolas', NULL, '1995-02-08', 'Santa Fe', 'Totoras', 1),
('033-048-R7', 38239811, 'sanabrialucas', 'user', 'Sanabria, Lucas Jose', NULL, '1994-11-01', 'Santa Fe', 'Totoras', 1),
('033-073-R7', 43842037, 'sanellielias', 'user', 'Sanelli, Elias Natael', NULL, '2002-02-20', 'Santa Fe', 'Totoras', 1),
('033-032-R7', 29840984, 'schneidercristian', 'user', 'Schneider, Cristian Gaston', NULL, '1983-04-20', 'Santa Fe', 'Totoras', 1),
('033-088-R7', 47290524, 'segoviaesteban', 'user', 'Segovia Miranda, Esteban Emanuel', NULL, '2006-05-21', 'Santa Fe', 'Totoras', 1),
('033-042-R7', 26112825, 'valorkocian', 'user', 'Valor Kocian Kokan, Juan Manuel', NULL, '1977-08-25', 'Santa Fe', 'Totoras', 1),
('033-046-R7', 38239759, 'gvignatti', 'admin', 'Vignatti, Giuliano', NULL, '1994-06-16', 'Santa Fe', 'Totoras', 2);

INSERT INTO unidades (nombre, patente, estado) VALUES
('A Presto', 'AP', 1),
('Autobomba', 'IES048', 1),
('Autobomba', 'MAR287', 1),
('Autobomba', 'AB511FG', 1),
('Ambulancia', 'AA456EF', 1),
('Ambulancia', 'TCP405', 1),
('Cisterna', 'ERR404', 1);

INSERT INTO eventos (nombre, puntos) VALUES
('Sirena', 2.0),
('Práctica', 3.0),
('Fagina', 3.0),
('Especial', 1.0),
('Conducta', 1.0);