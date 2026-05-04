-- ============================================================
--  BASE DE DATOS: aseguradora
--  Versión con catálogo de productos de póliza
-- ============================================================

DROP DATABASE IF EXISTS aseguradora;
CREATE DATABASE IF NOT EXISTS aseguradora CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aseguradora;


-- ------------------------------------------------------------
--  AGENTE
--  Usuarios del sistema (admins y agentes de ventas)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS agente (
    id_agente        INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    clave_agente     VARCHAR(100) NOT NULL UNIQUE,
    cedula           VARCHAR(10)  NOT NULL UNIQUE,
    nombre           VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    correo           VARCHAR(255) NOT NULL UNIQUE,
    telefono         VARCHAR(20),
    rol              ENUM('admin', 'agente') NOT NULL,
    password         VARCHAR(255) NOT NULL,
    created_at       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at       DATETIME     NULL
);


-- ------------------------------------------------------------
--  PRODUCTO_POLIZA  ← NUEVO
--  Catálogo de tipos de póliza disponibles para contratar
--  Ej: "Cuidándote", "Cobertura Básica", "Plan Familiar"
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS producto_poliza (
    id_producto  INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre       VARCHAR(150) NOT NULL UNIQUE,
    descripcion  TEXT,
    tipo_seguro  VARCHAR(100) NOT NULL,  -- gastos médicos, vida, auto, etc.
    prima_base   FLOAT        NOT NULL,  -- prima mensual de referencia
    activo       BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at   DATETIME     NULL
);


-- ------------------------------------------------------------
--  PRODUCTO_BENEFICIO  ← NUEVO
--  Beneficios / coberturas base que incluye cada producto
--  Al contratar una póliza, se copian automáticamente a `beneficio`
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS producto_beneficio (
    id_producto_beneficio INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_producto           INT          NOT NULL,
    nombre_beneficio      VARCHAR(255) NOT NULL,
    descripcion           VARCHAR(500) NOT NULL,
    monto_cobertura       FLOAT        NOT NULL,
    costo_extra           FLOAT        NULL,
    incluido_base         BOOLEAN      NOT NULL DEFAULT TRUE,  -- TRUE = incluido sin costo extra
    activo                BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at            DATETIME     NULL,
    FOREIGN KEY (id_producto) REFERENCES producto_poliza(id_producto) ON DELETE CASCADE
);


-- ------------------------------------------------------------
--  ASEGURADO
--  Persona física registrada en el sistema (titular o familiar)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS asegurado (
    id_asegurado          INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre                VARCHAR(100) NOT NULL,
    apellido_paterno      VARCHAR(100) NOT NULL,
    apellido_materno      VARCHAR(100) NOT NULL,
    rfc                   VARCHAR(20)  NOT NULL UNIQUE,
    correo                VARCHAR(255),
    celular               VARCHAR(10),
    calle                 VARCHAR(255) NOT NULL,
    numero_exterior       VARCHAR(50)  NOT NULL,
    numero_interior       VARCHAR(50),
    colonia               VARCHAR(100) NOT NULL,
    municipio             VARCHAR(100) NOT NULL,
    estado                VARCHAR(100) NOT NULL,
    codigo_postal         VARCHAR(20)  NOT NULL,
    id_agente_responsable INT,
    created_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at            DATETIME     NULL,
    FOREIGN KEY (id_agente_responsable) REFERENCES agente(id_agente) ON DELETE SET NULL
);


-- ------------------------------------------------------------
--  POLIZA
--  Contrato de seguro firmado por un asegurado
--  Ahora referencia al producto del catálogo
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS poliza (
    id_poliza         INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_asegurado      INT          NOT NULL,    -- titular de la póliza
    id_producto       INT          NOT NULL,    -- ← producto del catálogo
    numero_poliza     VARCHAR(100) NOT NULL UNIQUE,
    fecha_inicio      DATE         NOT NULL,
    fecha_vencimiento DATE         NOT NULL,
    estatus           ENUM('activa', 'vencida', 'cancelada') NOT NULL,
    prima_mensual     FLOAT        NOT NULL,    -- puede diferir de prima_base si hay ajustes
    created_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at        DATETIME     NULL,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE,
    FOREIGN KEY (id_producto)  REFERENCES producto_poliza(id_producto) ON DELETE RESTRICT
);


-- ------------------------------------------------------------
--  BENEFICIARIO
--  Personas que reciben el beneficio en caso de siniestro
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS beneficiario (
    id_beneficiario          INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_asegurado             INT          NOT NULL,
    id_poliza                INT          NULL,
    nombre_completo          VARCHAR(255) NOT NULL,
    parentesco               VARCHAR(50)  NOT NULL,
    porcentaje_participacion FLOAT        NOT NULL,
    telefono                 VARCHAR(20),
    created_at               DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at               DATETIME     NULL,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE,
    FOREIGN KEY (id_poliza) REFERENCES poliza(id_poliza) ON DELETE CASCADE
);


-- ------------------------------------------------------------
--  ASEGURADO_POLIZA
--  Personas cubiertas dentro de una póliza (titular + familiares)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS asegurado_poliza (
    id_asegurado_poliza INT  NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_poliza           INT  NOT NULL,
    id_asegurado        INT  NOT NULL,
    tipo_participante   ENUM('titular', 'conyuge', 'hijo', 'dependiente') NOT NULL,
    created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at          DATETIME NULL,
    FOREIGN KEY (id_poliza)    REFERENCES poliza(id_poliza)       ON DELETE CASCADE,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE,
    UNIQUE KEY uq_poliza_asegurado (id_poliza, id_asegurado)
);


-- ------------------------------------------------------------
--  BENEFICIO
--  Coberturas vigentes de una póliza contratada.
--
--  Flujo de uso:
--    1. Al crear la póliza, se copian aquí los registros de
--       producto_beneficio del producto elegido.
--    2. Si un beneficio base necesita un monto distinto para
--       este asegurado, se usa monto_override (si es NULL se
--       aplica el monto del producto_beneficio original).
--    3. Se pueden agregar beneficios extra sin id_producto_beneficio.
--
--  Dos alcances:
--    id_asegurado_poliza IS NULL  → aplica a toda la póliza
--    id_asegurado_poliza NOT NULL → aplica solo a esa persona
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS beneficio (
    id_beneficio          INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_poliza             INT          NOT NULL,
    id_producto_beneficio INT          NULL,    -- NULL si es beneficio extra personalizado
    id_asegurado_poliza   INT          NULL,    -- NULL si aplica a toda la póliza
    nombre_beneficio      VARCHAR(255) NOT NULL,
    descripcion           VARCHAR(500) NOT NULL,
    monto_cobertura       FLOAT        NOT NULL, -- valor efectivo (ya aplicado override si hubo)
    costo_aplicado        FLOAT        NOT NULL, -- costo congelado al momento de contratar
    monto_override        FLOAT        NULL,     -- solo si se modificó el monto base del producto
    vigente               BOOLEAN      NOT NULL DEFAULT TRUE,
    deleted_at            DATETIME     NULL,
    FOREIGN KEY (id_poliza)             REFERENCES poliza(id_poliza)                     ON DELETE CASCADE,
    FOREIGN KEY (id_producto_beneficio) REFERENCES producto_beneficio(id_producto_beneficio) ON DELETE SET NULL,
    FOREIGN KEY (id_asegurado_poliza)   REFERENCES asegurado_poliza(id_asegurado_poliza)  ON DELETE SET NULL
);


-- ------------------------------------------------------------
--  SEGUIMIENTO
--  Registro de contactos / interacciones con asegurados
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS seguimiento (
    id_seguimiento INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_asegurado   INT          NOT NULL,
    id_agente      INT          NOT NULL,
    tipo_contacto  ENUM('llamada', 'visita', 'mensaje') NOT NULL,
    observaciones  TEXT         NOT NULL,
    resultado      ENUM('resuelto', 'pendiente', 'sin_respuesta') NOT NULL,
    fecha_hora     DATETIME     NOT NULL,
    created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at     DATETIME     NULL,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE,
    FOREIGN KEY (id_agente)    REFERENCES agente(id_agente)       ON DELETE CASCADE
);


-- ============================================================
--  DATOS INICIALES
-- ============================================================

-- ------------------------------------------------------------
--  Agente administrador
-- ------------------------------------------------------------
INSERT IGNORE INTO agente (
    clave_agente, cedula, nombre, apellido_paterno, apellido_materno,
    correo, telefono, rol, password, created_at, updated_at
) VALUES (
    'admin1', '1234567890', 'Administrador', 'Sistema', 'Demo',
    'admin@seguros.com', '5512345678', 'admin', '561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c', NOW(), NOW()
);


-- ------------------------------------------------------------
--  Catálogo de productos (pólizas disponibles)
-- ------------------------------------------------------------
INSERT INTO producto_poliza (nombre, descripcion, tipo_seguro, prima_base) VALUES
(
    'Cuidándote',
    'Póliza de gastos médicos mayores con amplia red de hospitales y cobertura nacional.',
    'Gastos Médicos Mayores',
    1200.00
),
(
    'Vida Plus',
    'Seguro de vida con suma asegurada flexible y protección por accidentes.',
    'Vida',
    650.00
),
(
    'Plan Familiar',
    'Cobertura integral para titular, cónyuge e hijos con beneficios preventivos incluidos.',
    'Gastos Médicos Mayores',
    2100.00
),
(
    'Básico Accidentes',
    'Cobertura esencial ante accidentes personales, ideal como complemento.',
    'Accidentes Personales',
    300.00
);


-- ------------------------------------------------------------
--  Beneficios base por producto
-- ------------------------------------------------------------

-- Cuidándote (id_producto = 1)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(1, 'Hospitalización',       'Gastos de internamiento en hospital de la red.',              5000000.00, NULL, TRUE),
(1, 'Cirugía',               'Honorarios médicos y gastos quirúrgicos.',                    3000000.00, NULL, TRUE),
(1, 'Médico a domicilio',    'Hasta 3 consultas anuales sin costo adicional.',                 3000.00, NULL, TRUE),
(1, 'Maternidad',            'Cobertura de parto normal y cesárea.',                          80000.00, 240.00, FALSE),
(1, 'Dental preventivo',     'Limpieza y revisión anual incluida.',                            2500.00, 95.00, FALSE);

-- Vida Plus (id_producto = 2)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(2, 'Suma asegurada por fallecimiento', 'Pago único a beneficiarios en caso de fallecimiento.',  1000000.00, NULL, TRUE),
(2, 'Doble indemnización accidente',   'Doble de la suma asegurada si el fallecimiento es por accidente.', 2000000.00, NULL, TRUE),
(2, 'Invalidez total permanente',      'Anticipo del 100% de la suma asegurada.',                1000000.00, NULL, TRUE),
(2, 'Enfermedades graves',             'Diagnóstico de cáncer, infarto o EVC cubre hasta el 50%.', 500000.00, 180.00, FALSE);

-- Plan Familiar (id_producto = 3)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(3, 'Hospitalización familiar',   'Cobertura de internamiento para todos los miembros.',        8000000.00, NULL, TRUE),
(3, 'Cirugía',                    'Honorarios médicos y gastos quirúrgicos para titular y familia.', 5000000.00, NULL, TRUE),
(3, 'Consultas preventivas',      'Hasta 6 consultas anuales por miembro cubierto.',               6000.00, NULL, TRUE),
(3, 'Vacunas infantiles',         'Esquema completo de vacunación para hijos menores de 12 años.',  5000.00, NULL, TRUE),
(3, 'Maternidad',                 'Cobertura de parto normal y cesárea.',                         100000.00, NULL, TRUE),
(3, 'Odontología básica',         'Limpiezas, extracciones y radiografías.',                       8000.00, 120.00, FALSE);

-- Básico Accidentes (id_producto = 4)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(4, 'Muerte accidental',          'Pago único a beneficiarios por fallecimiento en accidente.',  300000.00, NULL, TRUE),
(4, 'Gastos médicos por accidente','Atención de urgencia y hospitalización por accidente.',       50000.00, NULL, TRUE),
(4, 'Invalidez parcial',          'Indemnización proporcional según tabla de invalideces.',      150000.00, NULL, TRUE);



-- =========================
-- 1. INSERTS AGENTE (10)
-- =========================
INSERT INTO agente (clave_agente, cedula, nombre, apellido_paterno, apellido_materno, correo, telefono, rol, password)
VALUES
('agente1','1000000001','Juan','Pérez','López','juan@correo.com','5550000001','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c'),
('agente2','1000000002','María','Gómez','Hernández','maria@correo.com','5550000002','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c'),
('agente3','1000000003','Luis','Martínez','Ruiz','luis@correo.com','5550000003','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c'),
('agente4','1000000004','Ana','Ramírez','Soto','ana@correo.com','5550000004','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c'),
('agente5','1000000005','Carlos','Torres','Mendoza','carlos@correo.com','5550000005','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c'),
('agente6','1000000006','Sofía','Vargas','Castillo','sofia@correo.com','5550000006','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c'),
('agente7','1000000007','Diego','Rojas','Figueroa','diego@correo.com','5550000007','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c'),
('agente8','1000000008','Lucía','Silva','Paredes','lucia@correo.com','5550000008','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c'),
('agente9','1000000009','Miguel','Cruz','Ortega','miguel@correo.com','5550000009','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c'),
('agente10','1000000010','Valeria','Flores','Navarro','valeria@correo.com','5550000010','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c');


INSERT INTO asegurado (
    nombre, apellido_paterno, apellido_materno, rfc, correo, celular,
    calle, numero_exterior, numero_interior, colonia, municipio, estado,
    codigo_postal, id_agente_responsable
)
VALUES
('Pedro','García','López','GARL800101XXX','pedro.garcia@example.com','5511110001','Calle Falsa','123',NULL,'Centro','Ciudad','Estado1','01000',(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Lucía','Martínez','Sánchez','MASL900202XXX','lucia.martinez@example.com','5511110002','Av. Reforma','45','A','Juárez','Ciudad','Estado2','01010',(SELECT id_agente FROM agente WHERE clave_agente = 'agente2')),
('Carlos','Pérez','Hernández','PECH850303XXX','carlos.perez@example.com','5511110003','Calle Luna','78',NULL,'Roma','Ciudad','Estado3','01020',(SELECT id_agente FROM agente WHERE clave_agente = 'agente3')),
('Ana','Gómez','Ramírez','GORA870404XXX','ana.gomez@example.com','5511110004','Calle Sol','9','B','Polanco','Ciudad','Estado4','01030',(SELECT id_agente FROM agente WHERE clave_agente = 'agente4')),
('Miguel','Rojas','Vargas','ROVM820505XXX','miguel.rojas@example.com','5511110005','Av. Central','12',NULL,'Condesa','Ciudad','Estado5','01040',(SELECT id_agente FROM agente WHERE clave_agente = 'agente5')),
('Sofía','Flores','Castillo','FLOC910606XXX','sofia.flores@example.com','5511110006','Calle Real','56','C','Narvarte','Ciudad','Estado6','01050',(SELECT id_agente FROM agente WHERE clave_agente = 'agente6')),
('Diego','Silva','Mendoza','SIMD930707XXX','diego.silva@example.com','5511110007','Av. Libertad','34',NULL,'Juárez','Ciudad','Estado7','01060',(SELECT id_agente FROM agente WHERE clave_agente = 'agente7')),
('Valeria','Cruz','Navarro','CRVN940808XXX','valeria.cruz@example.com','5511110008','Calle Verde','22','D','Centro','Ciudad','Estado8','01070',(SELECT id_agente FROM agente WHERE clave_agente = 'agente8')),
('Luis','Ramírez','Ortega','RAOL950909XXX','luis.ramirez@example.com','5511110009','Av. Naranja','7',NULL,'Roma','Ciudad','Estado9','01080',(SELECT id_agente FROM agente WHERE clave_agente = 'agente9')),
('María','Vargas','Soto','VASM961010XXX','maria.vargas@example.com','5511110010','Calle Azul','11','E','Condesa','Ciudad','Estado10','01090',(SELECT id_agente FROM agente WHERE clave_agente = 'agente10'));

INSERT INTO beneficiario (id_asegurado, nombre_completo, parentesco, porcentaje_participacion, telefono)
VALUES
((SELECT id_asegurado FROM asegurado WHERE rfc = 'GARL800101XXX'), 'Ana García', 'Hija', 50.0, '5511000001'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'MASL900202XXX'), 'Luis García', 'Hijo', 50.0, '5511000002'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'PECH850303XXX'), 'María Pérez', 'Esposa', 100.0, '5511000003'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'GORA870404XXX'), 'Carlos Ramírez', 'Hijo', 50.0, '5511000004'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'ROVM820505XXX'), 'Sofía Rojas', 'Hija', 50.0, '5511000005'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'FLOC910606XXX'), 'Diego Flores', 'Esposo', 100.0, '5511000006'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'SIMD930707XXX'), 'Valeria Silva', 'Hija', 50.0, '5511000007'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'CRVN940808XXX'), 'Miguel Navarro', 'Hijo', 50.0, '5511000008'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'RAOL950909XXX'), 'Luis Ortega', 'Padre', 50.0, '5511000009'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'VASM961010XXX'), 'María Soto', 'Madre', 50.0, '5511000010');

INSERT INTO poliza (
    id_asegurado,
    id_producto,
    numero_poliza,
    fecha_inicio,
    fecha_vencimiento,
    estatus,
    prima_mensual
)
VALUES
((SELECT id_asegurado FROM asegurado WHERE rfc = 'GARL800101XXX'),(SELECT id_producto FROM producto_poliza WHERE nombre = 'Cuidándote'),'POL001','2024-01-01','2025-01-01','activa',500),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'MASL900202XXX'),(SELECT id_producto FROM producto_poliza WHERE nombre = 'Vida Plus'),'POL002','2024-02-01','2025-02-01','activa',650),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'PECH850303XXX'),(SELECT id_producto FROM producto_poliza WHERE nombre = 'Plan Familiar'),'POL003','2024-03-01','2025-03-01','activa',2100),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'GORA870404XXX'),(SELECT id_producto FROM producto_poliza WHERE nombre = 'Vida Plus'),'POL004','2024-04-01','2025-04-01','activa',650),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'ROVM820505XXX'),(SELECT id_producto FROM producto_poliza WHERE nombre = 'Básico Accidentes'),'POL005','2024-05-01','2025-05-01','activa',300),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'FLOC910606XXX'),(SELECT id_producto FROM producto_poliza WHERE nombre = 'Plan Familiar'),'POL006','2024-06-01','2025-06-01','activa',2100),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'SIMD930707XXX'),(SELECT id_producto FROM producto_poliza WHERE nombre = 'Cuidándote'),'POL007','2024-07-01','2025-07-01','activa',1200),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'CRVN940808XXX'),(SELECT id_producto FROM producto_poliza WHERE nombre = 'Básico Accidentes'),'POL008','2024-08-01','2025-08-01','activa',300),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'RAOL950909XXX'),(SELECT id_producto FROM producto_poliza WHERE nombre = 'Plan Familiar'),'POL009','2024-09-01','2025-09-01','activa',2100),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'VASM961010XXX'),(SELECT id_producto FROM producto_poliza WHERE nombre = 'Vida Plus'),'POL010','2024-10-01','2025-10-01','activa',650);


INSERT INTO asegurado_poliza (id_poliza, id_asegurado, tipo_participante)
VALUES
-- Titulares
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL001'),(SELECT id_asegurado FROM asegurado WHERE rfc = 'GARL800101XXX'),'titular'),
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL002'),(SELECT id_asegurado FROM asegurado WHERE rfc = 'MASL900202XXX'),'titular'),
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL003'),(SELECT id_asegurado FROM asegurado WHERE rfc = 'PECH850303XXX'),'titular'),
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL004'),(SELECT id_asegurado FROM asegurado WHERE rfc = 'GORA870404XXX'),'titular'),
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL005'),(SELECT id_asegurado FROM asegurado WHERE rfc = 'ROVM820505XXX'),'titular'),
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL006'),(SELECT id_asegurado FROM asegurado WHERE rfc = 'FLOC910606XXX'),'titular'),
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL007'),(SELECT id_asegurado FROM asegurado WHERE rfc = 'SIMD930707XXX'),'titular'),
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL008'),(SELECT id_asegurado FROM asegurado WHERE rfc = 'CRVN940808XXX'),'titular'),
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL009'),(SELECT id_asegurado FROM asegurado WHERE rfc = 'RAOL950909XXX'),'titular'),
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL010'),(SELECT id_asegurado FROM asegurado WHERE rfc = 'VASM961010XXX'),'titular');

UPDATE beneficiario
SET id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL001')
WHERE id_asegurado = (SELECT id_asegurado FROM asegurado WHERE rfc = 'GARL800101XXX');

UPDATE beneficiario
SET id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL002')
WHERE id_asegurado = (SELECT id_asegurado FROM asegurado WHERE rfc = 'MASL900202XXX');

UPDATE beneficiario
SET id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL003')
WHERE id_asegurado = (SELECT id_asegurado FROM asegurado WHERE rfc = 'PECH850303XXX');

UPDATE beneficiario
SET id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL004')
WHERE id_asegurado = (SELECT id_asegurado FROM asegurado WHERE rfc = 'GORA870404XXX');

UPDATE beneficiario
SET id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL005')
WHERE id_asegurado = (SELECT id_asegurado FROM asegurado WHERE rfc = 'ROVM820505XXX');

UPDATE beneficiario
SET id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL006')
WHERE id_asegurado = (SELECT id_asegurado FROM asegurado WHERE rfc = 'FLOC910606XXX');

UPDATE beneficiario
SET id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL007')
WHERE id_asegurado = (SELECT id_asegurado FROM asegurado WHERE rfc = 'SIMD930707XXX');

UPDATE beneficiario
SET id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL008')
WHERE id_asegurado = (SELECT id_asegurado FROM asegurado WHERE rfc = 'CRVN940808XXX');

UPDATE beneficiario
SET id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL009')
WHERE id_asegurado = (SELECT id_asegurado FROM asegurado WHERE rfc = 'RAOL950909XXX');

UPDATE beneficiario
SET id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL010')
WHERE id_asegurado = (SELECT id_asegurado FROM asegurado WHERE rfc = 'VASM961010XXX');


-- ============================================================
--  DATOS DE PRUEBA: familia completa en una sola póliza
--  Producto: Plan Familiar (id_producto = 3)
-- ============================================================

-- ------------------------------------------------------------
--  1. Asegurados (titular + familiares)
-- ------------------------------------------------------------
INSERT INTO asegurado (
    nombre, apellido_paterno, apellido_materno, rfc, correo, celular,
    calle, numero_exterior, numero_interior, colonia, municipio, estado,
    codigo_postal, id_agente_responsable
) VALUES
-- Titular
('Roberto', 'Mendoza', 'Castro', 'MECR780512HDF', 'roberto.mendoza@example.com', '5521000001',
 'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', (SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
-- Cónyuge
('Patricia', 'Vega', 'Suárez', 'VESP820318MDF', 'patricia.vega@example.com', '5521000002',
 'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', (SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
-- Hijo 1
('Emilio', 'Mendoza', 'Vega', 'MEVE100601HDF', NULL, NULL,
 'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', (SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
-- Hijo 2
('Camila', 'Mendoza', 'Vega', 'MEVC130915MDF', NULL, NULL,
 'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', (SELECT id_agente FROM agente WHERE clave_agente = 'admin1'));


-- ------------------------------------------------------------
--  2. Beneficiarios del titular
-- ------------------------------------------------------------
INSERT INTO beneficiario (id_asegurado, nombre_completo, parentesco, porcentaje_participacion, telefono)
VALUES
-- Los hijos son beneficiarios del titular (50% cada uno)
((SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'), 'Emilio Mendoza Vega',  'Hijo', 50.0, '5521000003'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'), 'Camila Mendoza Vega',  'Hijo', 50.0, '5521000004'),
-- El titular es beneficiario de la cónyuge (100%)
((SELECT id_asegurado FROM asegurado WHERE rfc = 'VESP820318MDF'), 'Roberto Mendoza Castro', 'Esposo', 100.0, '5521000001');


-- ------------------------------------------------------------
--  3. Póliza (contratada por el titular)
-- ------------------------------------------------------------
INSERT INTO poliza (
    id_asegurado, id_producto, numero_poliza,
    fecha_inicio, fecha_vencimiento, estatus, prima_mensual
) VALUES (
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'),
    (SELECT id_producto FROM producto_poliza WHERE nombre = 'Plan Familiar'),
    'POL-FAM-001',
    '2025-01-01',
    '2026-01-01',
    'activa',
    2100.00
);


-- ------------------------------------------------------------
--  4. Personas cubiertas dentro de la póliza
-- ------------------------------------------------------------
INSERT INTO asegurado_poliza (id_poliza, id_asegurado, tipo_participante)
VALUES
(
    (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'),
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'),
    'titular'
),
(
    (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'),
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'VESP820318MDF'),
    'conyuge'
),
(
    (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'),
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'MEVE100601HDF'),
    'hijo'
),
(
    (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'),
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'MEVC130915MDF'),
    'hijo'
);

UPDATE beneficiario
SET id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001')
WHERE id_asegurado IN (
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'),
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'VESP820318MDF')
);


-- ------------------------------------------------------------
--  5. Beneficios copiados del producto + uno con override
--     (simula que al titular se le ajustó Hospitalización familiar)
-- ------------------------------------------------------------
INSERT INTO beneficio (
    id_poliza, id_producto_beneficio,
    id_asegurado_poliza,
    nombre_beneficio, descripcion,
    monto_cobertura, costo_aplicado, monto_override, vigente
)
SELECT
    (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'),
    pb.id_producto_beneficio,
    NULL,                           -- aplica a toda la póliza
    pb.nombre_beneficio,
    pb.descripcion,
    pb.monto_cobertura,
    CASE WHEN pb.incluido_base = TRUE THEN 0 ELSE COALESCE(pb.costo_extra, 0) END,
    NULL,                           -- sin override: se usa el monto base
    TRUE
FROM producto_beneficio pb
WHERE pb.id_producto = (SELECT id_producto FROM producto_poliza WHERE nombre = 'Plan Familiar')
    AND pb.activo = TRUE
    AND pb.deleted_at IS NULL
  AND pb.incluido_base = TRUE;

-- Override a nivel póliza en Hospitalización familiar
UPDATE beneficio
SET monto_override  = 10000000.00,
    monto_cobertura = 10000000.00
WHERE id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001')
  AND nombre_beneficio = 'Hospitalización familiar';

-- Beneficio adicional personalizado solo para la cónyuge
INSERT INTO beneficio (
    id_poliza, id_producto_beneficio, id_asegurado_poliza,
    nombre_beneficio, descripcion, monto_cobertura, costo_aplicado, monto_override, vigente
) VALUES (
    (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'),
    NULL,   -- beneficio extra, no viene del catálogo
    (SELECT ap.id_asegurado_poliza
     FROM asegurado_poliza ap
     JOIN asegurado a ON a.id_asegurado = ap.id_asegurado
     WHERE ap.id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001')
       AND a.rfc = 'VESP820318MDF'),
    'Rehabilitación postparto',
    'Sesiones de fisioterapia y psicología postparto, hasta 10 sesiones al año.',
    15000.00,
    180.00,
    NULL,
    TRUE
);

UPDATE poliza
SET prima_mensual = (
    (SELECT prima_base FROM producto_poliza WHERE nombre = 'Plan Familiar') + 180.00
)
WHERE numero_poliza = 'POL-FAM-001';


-- ------------------------------------------------------------
--  6. Seguimientos de ejemplo sobre el titular
-- ------------------------------------------------------------
INSERT INTO seguimiento (id_asegurado, id_agente, tipo_contacto, observaciones, resultado, fecha_hora)
VALUES
(
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'),
    (SELECT id_agente FROM agente WHERE clave_agente = 'admin1'),
    'llamada',
    'El cliente confirmó los datos de sus familiares y aprobó la prima mensual de $2,100.',
    'resuelto',
    '2025-01-03 10:30:00'
),
(
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'),
    (SELECT id_agente FROM agente WHERE clave_agente = 'admin1'),
    'mensaje',
    'Se envió PDF de la póliza y tabla de beneficios por WhatsApp. Pendiente firma digital.',
    'pendiente',
    '2025-01-05 16:00:00'
);
