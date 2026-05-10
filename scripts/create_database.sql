-- ============================================================
--  BASE DE DATOS: aseguradora  (v3 - final)
--
--  Cambios respecto a v1 original:
--
--  1. Se eliminó `asegurado_poliza` — el titular ya vive en
--     poliza.id_asegurado; los dependientes van en la nueva
--     tabla `poliza_dependiente`.
--
--  2. `beneficio` ya no duplica nombre/descripcion/monto_cobertura
--     de producto_beneficio; esos datos se leen con JOIN.
--     Solo guarda lo propio de la póliza contratada:
--     monto_override, costo_aplicado, y a quién aplica.
--
--  3. `seguimiento` se convierte en el folio/caso y se agrega
--     `seguimiento_contacto` como tabla de interacciones, que
--     soporta contacto en ambas direcciones (agente ↔ asegurado).
--
--  4. `beneficiario` ahora puede ligarse a un beneficio
--     específico (para dependientes) o a toda la póliza
--     (para el titular). Esto refleja la lógica real de
--     pólizas como MetLife donde cada beneficio de un
--     dependiente tiene su propio beneficiario registrado.
--
-- ============================================================

DROP DATABASE IF EXISTS aseguradora;
CREATE DATABASE IF NOT EXISTS aseguradora CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aseguradora;


-- ============================================================
--  AGENTE
--  Usuarios del sistema (admins y agentes de ventas)
-- ============================================================
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


-- ============================================================
--  PRODUCTO_POLIZA
--  Catálogo de tipos de póliza disponibles para contratar
--  Ej: "Cuidándote", "Cobertura Básica", "Plan Familiar"
-- ============================================================
CREATE TABLE IF NOT EXISTS producto_poliza (
    id_producto  INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre       VARCHAR(150) NOT NULL UNIQUE,
    descripcion  TEXT,
    tipo_seguro  VARCHAR(100) NOT NULL,   -- gastos médicos, vida, auto, etc.
    prima_base   FLOAT        NOT NULL,   -- prima mensual de referencia
    activo       BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at   DATETIME     NULL
);


-- ============================================================
--  PRODUCTO_BENEFICIO
--  Beneficios/coberturas base que incluye cada producto.
--  Son la "plantilla"; al contratar una póliza se referencian
--  desde `beneficio` con JOIN (no se copian).
-- ============================================================
CREATE TABLE IF NOT EXISTS producto_beneficio (
    id_producto_beneficio INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_producto           INT          NOT NULL,
    nombre_beneficio      VARCHAR(255) NOT NULL,
    descripcion           VARCHAR(500) NOT NULL,
    monto_cobertura       FLOAT        NOT NULL,
    costo_extra           FLOAT        NULL,
    incluido_base         BOOLEAN      NOT NULL DEFAULT TRUE,  -- TRUE = sin costo extra
    activo                BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at            DATETIME     NULL,
    FOREIGN KEY (id_producto) REFERENCES producto_poliza(id_producto) ON DELETE CASCADE
);


-- ============================================================
--  ASEGURADO
--  Persona física registrada en el sistema.
--  Tanto titulares como dependientes que tengan su propio
--  expediente se registran aquí.
-- ============================================================
CREATE TABLE IF NOT EXISTS asegurado (
    id_asegurado          INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre                VARCHAR(100) NOT NULL,
    apellido_paterno      VARCHAR(100) NOT NULL,
    apellido_materno      VARCHAR(100) NOT NULL,
    rfc                   VARCHAR(20)  NOT NULL UNIQUE,
    correo                VARCHAR(255),
    celular               VARCHAR(15),
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


-- ============================================================
--  POLIZA
--  Contrato de seguro.
--  poliza.id_asegurado = el TITULAR (no se repite en otra tabla).
-- ============================================================
CREATE TABLE IF NOT EXISTS poliza (
    id_poliza         INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_asegurado      INT          NOT NULL,   -- titular de la póliza
    id_producto       INT          NOT NULL,   -- producto del catálogo
    numero_poliza     VARCHAR(100) NOT NULL UNIQUE,
    fecha_inicio      DATE         NOT NULL,
    fecha_vencimiento DATE         NOT NULL,
    estatus           ENUM('activa', 'vencida', 'cancelada') NOT NULL,
    prima_mensual     FLOAT        NOT NULL,   -- puede diferir de prima_base si hay ajustes
    created_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at        DATETIME     NULL,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE,
    FOREIGN KEY (id_producto)  REFERENCES producto_poliza(id_producto) ON DELETE RESTRICT
);


-- ============================================================
--  POLIZA_DEPENDIENTE
--  Familiares/dependientes cubiertos por la póliza además
--  del titular.
--
--  ¿Por qué no se incluye al titular aquí?
--    Porque poliza.id_asegurado ya lo define.
--
--  ¿Por qué id_asegurado y no solo un nombre?
--    Porque un dependiente puede tener su propio expediente
--    y eventualmente contratar su propia póliza.
-- ============================================================
CREATE TABLE IF NOT EXISTS poliza_dependiente (
    id_poliza_dependiente INT  NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_poliza             INT  NOT NULL,
    id_asegurado          INT  NOT NULL,
    parentesco            ENUM('conyuge', 'hijo', 'dependiente') NOT NULL,
    created_at            DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at            DATETIME NULL,
    FOREIGN KEY (id_poliza)    REFERENCES poliza(id_poliza)       ON DELETE CASCADE,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE,
    UNIQUE KEY uq_poliza_dependiente (id_poliza, id_asegurado)
);


-- ============================================================
--  BENEFICIO
--  Coberturas vigentes de una póliza contratada.
--
--  No duplica nombre/descripcion/monto del catálogo — esos
--  se obtienen con JOIN a producto_beneficio.
--
--  Alcances:
--    id_asegurado IS NULL     → aplica a toda la póliza (titular)
--    id_asegurado NOT NULL    → aplica solo a ese dependiente
--
--  Beneficio extra (sin catálogo):
--    id_producto_beneficio = NULL
--    nombre_beneficio_extra y descripcion_extra obligatorios
-- ============================================================
CREATE TABLE IF NOT EXISTS beneficio (
    id_beneficio           INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_poliza              INT          NOT NULL,
    id_producto_beneficio  INT          NULL,     -- NULL si es beneficio extra
    id_asegurado           INT          NULL,     -- NULL = toda la póliza / NOT NULL = dependiente específico
    nombre_beneficio_extra VARCHAR(255) NULL,     -- solo cuando id_producto_beneficio IS NULL
    descripcion_extra      VARCHAR(500) NULL,     -- solo cuando id_producto_beneficio IS NULL
    monto_override         FLOAT        NULL,     -- solo si se cambió el monto base del catálogo
    costo_aplicado         FLOAT        NOT NULL, -- congelado al contratar
    vigente                BOOLEAN      NOT NULL DEFAULT TRUE,
    deleted_at             DATETIME     NULL,
    FOREIGN KEY (id_poliza)             REFERENCES poliza(id_poliza)                         ON DELETE CASCADE,
    FOREIGN KEY (id_producto_beneficio) REFERENCES producto_beneficio(id_producto_beneficio) ON DELETE SET NULL,
    FOREIGN KEY (id_asegurado)          REFERENCES asegurado(id_asegurado)                   ON DELETE SET NULL
);


-- ============================================================
--  BENEFICIARIO
--  Personas que RECIBEN el dinero en caso de siniestro.
--  (diferente a los dependientes cubiertos por la póliza)
--
--  Dos alcances según la lógica de pólizas reales:
--
--    id_beneficio IS NULL  → beneficiario de toda la póliza
--                            (caso típico del titular)
--
--    id_beneficio NOT NULL → beneficiario de ese beneficio
--                            específico (caso de dependientes:
--                            ej. la hija tiene sus propios
--                            beneficiarios en BAC, EG1, CR1...)
-- ============================================================
CREATE TABLE IF NOT EXISTS beneficiario (
    id_beneficiario          INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_asegurado             INT          NOT NULL,   -- de quién es este beneficiario
    id_poliza                INT          NULL,       -- póliza general
    id_beneficio             INT          NULL,       -- beneficio específico (dependiente)
    nombre_completo          VARCHAR(255) NOT NULL,
    parentesco               VARCHAR(50)  NOT NULL,
    porcentaje_participacion FLOAT        NOT NULL,
    telefono                 VARCHAR(20),
    created_at               DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at               DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at               DATETIME     NULL,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE,
    FOREIGN KEY (id_poliza)    REFERENCES poliza(id_poliza)        ON DELETE CASCADE,
    FOREIGN KEY (id_beneficio) REFERENCES beneficio(id_beneficio)  ON DELETE CASCADE
);


-- ============================================================
--  SEGUIMIENTO
--  Folio/caso — agrupa todas las interacciones sobre un mismo
--  asunto entre un asegurado y su agente responsable.
-- ============================================================
CREATE TABLE IF NOT EXISTS seguimiento (
    id_seguimiento INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    folio          VARCHAR(20)  NOT NULL UNIQUE,   -- ej: "SEG-2026-001"
    id_asegurado   INT          NOT NULL,
    id_agente      INT          NOT NULL,          -- agente responsable del caso
    asunto         VARCHAR(255) NOT NULL,
    created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at     DATETIME     NULL,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE,
    FOREIGN KEY (id_agente)    REFERENCES agente(id_agente)       ON DELETE CASCADE
);


-- ============================================================
--  SEGUIMIENTO_CONTACTO
--  Cada interacción registrada dentro de un folio.
--  Soporta contacto en ambas direcciones: el agente puede
--  contactar al asegurado o viceversa.
--
--  No repite id_agente/id_asegurado porque ya están en
--  `seguimiento` y se obtienen con JOIN.
-- ============================================================
CREATE TABLE IF NOT EXISTS seguimiento_contacto (
    id_contacto    INT           NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_seguimiento INT           NOT NULL,
    iniciado_por   ENUM('agente', 'asegurado') NOT NULL,
    tipo_contacto  ENUM('llamada', 'visita', 'mensaje') NOT NULL,
    observaciones  VARCHAR(1000) NOT NULL,
    resultado      ENUM('resuelto', 'pendiente', 'sin_respuesta') NOT NULL,
    fecha_hora     DATETIME      NOT NULL,
    created_at     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at     DATETIME      NULL,
    FOREIGN KEY (id_seguimiento) REFERENCES seguimiento(id_seguimiento) ON DELETE CASCADE
);


-- ============================================================
--  DATOS INICIALES
-- ============================================================

-- ------------------------------------------------------------
--  1. AGENTES
-- ------------------------------------------------------------
INSERT INTO agente (clave_agente, cedula, nombre, apellido_paterno, apellido_materno, correo, telefono, rol, password, created_at, updated_at)
VALUES
('admin1','1234567890','Administrador','Sistema','Demo','admin@seguros.com','5512345678','admin','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW()),
('agente1','1000000001','Juan','Pérez','López','juan@correo.com','5550000001','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW()),
('agente2','1000000002','María','Gómez','Hernández','maria@correo.com','5550000002','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW()),
('agente3','1000000003','Luis','Martínez','Ruiz','luis@correo.com','5550000003','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW()),
('agente4','1000000004','Ana','Ramírez','Soto','ana@correo.com','5550000004','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW()),
('agente5','1000000005','Carlos','Torres','Mendoza','carlos@correo.com','5550000005','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW()),
('agente6','1000000006','Sofía','Vargas','Castillo','sofia@correo.com','5550000006','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW()),
('agente7','1000000007','Diego','Rojas','Figueroa','diego@correo.com','5550000007','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW()),
('agente8','1000000008','Lucía','Silva','Paredes','lucia@correo.com','5550000008','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW()),
('agente9','1000000009','Miguel','Cruz','Ortega','miguel@correo.com','5550000009','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW()),
('agente10','1000000010','Valeria','Flores','Navarro','valeria@correo.com','5550000010','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW());


-- ------------------------------------------------------------
--  2. CATÁLOGO DE PRODUCTOS
-- ------------------------------------------------------------
INSERT INTO producto_poliza (nombre, descripcion, tipo_seguro, prima_base) VALUES
('Cuidándote',       'Póliza de gastos médicos mayores con amplia red de hospitales y cobertura nacional.',    'Gastos Médicos Mayores', 1200.00),
('Vida Plus',        'Seguro de vida con suma asegurada flexible y protección por accidentes.',               'Vida',                   650.00),
('Plan Familiar',    'Cobertura integral para titular, cónyuge e hijos con beneficios preventivos incluidos.','Gastos Médicos Mayores', 2100.00),
('Básico Accidentes','Cobertura esencial ante accidentes personales, ideal como complemento.',                'Accidentes Personales',  300.00);


-- ------------------------------------------------------------
--  3. BENEFICIOS BASE POR PRODUCTO
-- ------------------------------------------------------------

-- Cuidándote (id_producto = 1)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(1, 'Hospitalización',       'Gastos de internamiento en hospital de la red.',              5000000.00, NULL,   TRUE),
(1, 'Cirugía',               'Honorarios médicos y gastos quirúrgicos.',                    3000000.00, NULL,   TRUE),
(1, 'Médico a domicilio',    'Hasta 3 consultas anuales sin costo adicional.',                 3000.00, NULL,   TRUE),
(1, 'Maternidad',            'Cobertura de parto normal y cesárea.',                          80000.00, 240.00, FALSE),
(1, 'Dental preventivo',     'Limpieza y revisión anual incluida.',                            2500.00, 95.00,  FALSE);

-- Vida Plus (id_producto = 2)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(2, 'Suma asegurada por fallecimiento',  'Pago único a beneficiarios en caso de fallecimiento.',           1000000.00, NULL,   TRUE),
(2, 'Doble indemnización accidente',     'Doble de la suma asegurada si el fallecimiento es por accidente.',2000000.00, NULL,   TRUE),
(2, 'Invalidez total permanente',        'Anticipo del 100% de la suma asegurada.',                         1000000.00, NULL,   TRUE),
(2, 'Enfermedades graves',               'Diagnóstico de cáncer, infarto o EVC cubre hasta el 50%.',         500000.00, 180.00, FALSE);

-- Plan Familiar (id_producto = 3)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(3, 'Hospitalización familiar',   'Cobertura de internamiento para todos los miembros.',                 8000000.00, NULL,   TRUE),
(3, 'Cirugía',                    'Honorarios médicos y gastos quirúrgicos para titular y familia.',     5000000.00, NULL,   TRUE),
(3, 'Consultas preventivas',      'Hasta 6 consultas anuales por miembro cubierto.',                        6000.00, NULL,   TRUE),
(3, 'Vacunas infantiles',         'Esquema completo de vacunación para hijos menores de 12 años.',         5000.00, NULL,   TRUE),
(3, 'Maternidad',                 'Cobertura de parto normal y cesárea.',                                  100000.00, NULL,   TRUE),
(3, 'Odontología básica',         'Limpiezas, extracciones y radiografías.',                                8000.00, 120.00, FALSE);

-- Básico Accidentes (id_producto = 4)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(4, 'Muerte accidental',           'Pago único a beneficiarios por fallecimiento en accidente.',           300000.00, NULL,  TRUE),
(4, 'Gastos médicos por accidente','Atención de urgencia y hospitalización por accidente.',                 50000.00, NULL,  TRUE),
(4, 'Invalidez parcial',           'Indemnización proporcional según tabla de invalideces.',               150000.00, NULL,  TRUE);


-- ------------------------------------------------------------
--  4. ASEGURADOS (10 titulares + 4 familiares)
-- ------------------------------------------------------------
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

-- Familia Mendoza-Vega (para demo de familia completa en una póliza)
INSERT INTO asegurado (
    nombre, apellido_paterno, apellido_materno, rfc, correo, celular,
    calle, numero_exterior, numero_interior, colonia, municipio, estado,
    codigo_postal, id_agente_responsable
) VALUES
('Roberto', 'Mendoza', 'Castro',  'MECR780512HDF', 'roberto.mendoza@example.com', '5521000001', 'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', (SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Patricia', 'Vega', 'Suárez',    'VESP820318MDF', 'patricia.vega@example.com',   '5521000002', 'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', (SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Emilio', 'Mendoza', 'Vega',     'MEVE100601HDF', NULL,                          NULL,          'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', (SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Camila', 'Mendoza', 'Vega',     'MEVC130915MDF', NULL,                          NULL,          'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', (SELECT id_agente FROM agente WHERE clave_agente = 'admin1'));


-- ------------------------------------------------------------
--  5. PÓLIZAS (10 históricas vencidas + 1 familiar activa)
-- ------------------------------------------------------------
INSERT INTO poliza (
    id_asegurado, id_producto, numero_poliza,
    fecha_inicio, fecha_vencimiento, estatus, prima_mensual
)
VALUES
((SELECT id_asegurado FROM asegurado WHERE rfc = 'GARL800101XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Cuidándote'),       'POL001', '2024-01-01', '2025-01-01', 'vencida',   500),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'MASL900202XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Vida Plus'),        'POL002', '2024-02-01', '2025-02-01', 'vencida',   650),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'PECH850303XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Plan Familiar'),    'POL003', '2024-03-01', '2025-03-01', 'vencida',  2100),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'GORA870404XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Vida Plus'),        'POL004', '2024-04-01', '2025-04-01', 'vencida',   650),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'ROVM820505XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Básico Accidentes'),'POL005', '2024-05-01', '2025-05-01', 'vencida',   300),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'FLOC910606XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Plan Familiar'),    'POL006', '2024-06-01', '2025-06-01', 'vencida',  2100),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'SIMD930707XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Cuidándote'),       'POL007', '2024-07-01', '2025-07-01', 'vencida',  1200),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'CRVN940808XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Básico Accidentes'),'POL008', '2024-08-01', '2025-08-01', 'vencida',   300),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'RAOL950909XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Plan Familiar'),    'POL009', '2024-09-01', '2025-09-01', 'vencida',  2100),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'VASM961010XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Vida Plus'),        'POL010', '2024-10-01', '2025-10-01', 'vencida',   650);

-- Póliza familiar activa (con cobertura vigente hasta 2027)
INSERT INTO poliza (
    id_asegurado, id_producto, numero_poliza,
    fecha_inicio, fecha_vencimiento, estatus, prima_mensual
) VALUES (
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'),
    (SELECT id_producto FROM producto_poliza WHERE nombre = 'Plan Familiar'),
    'POL-FAM-001',
    '2026-01-01',
    '2027-01-01',
    'activa',
    2220.00   -- prima_base (2100) + costo_extra odontología (120)
);


-- ------------------------------------------------------------
--  6. DEPENDIENTES CUBIERTOS POR POL-FAM-001
-- ------------------------------------------------------------
INSERT INTO poliza_dependiente (id_poliza, id_asegurado, parentesco)
VALUES
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'), (SELECT id_asegurado FROM asegurado WHERE rfc = 'VESP820318MDF'), 'conyuge'),
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'), (SELECT id_asegurado FROM asegurado WHERE rfc = 'MEVE100601HDF'), 'hijo'),
((SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'), (SELECT id_asegurado FROM asegurado WHERE rfc = 'MEVC130915MDF'), 'hijo');


-- ------------------------------------------------------------
--  7. BENEFICIOS DE CADA PÓLIZA
-- ------------------------------------------------------------

-- 7a. Beneficios para POL001-POL010 (pólizas vencidas)
--     Se copian desde producto_beneficio con JOIN.
INSERT INTO beneficio (id_poliza, id_producto_beneficio, id_asegurado, costo_aplicado, vigente)
SELECT
    p.id_poliza,
    pb.id_producto_beneficio,
    NULL,                                       -- aplica a toda la póliza (titular)
    CASE WHEN pb.incluido_base THEN 0 ELSE COALESCE(pb.costo_extra, 0) END,
    TRUE
FROM poliza p
JOIN producto_poliza pp ON p.id_producto = pp.id_producto
JOIN producto_beneficio pb ON pb.id_producto = pp.id_producto
WHERE p.id_producto IS NOT NULL
  AND pb.activo = TRUE
  AND pb.deleted_at IS NULL
  AND pb.incluido_base = TRUE;

-- 7b. Beneficios para POL-FAM-001 (activa) desde producto_beneficio
INSERT INTO beneficio (id_poliza, id_producto_beneficio, id_asegurado, costo_aplicado, vigente)
SELECT
    p.id_poliza,
    pb.id_producto_beneficio,
    NULL,                                       -- aplica a toda la póliza
    CASE WHEN pb.incluido_base THEN 0 ELSE COALESCE(pb.costo_extra, 0) END,
    TRUE
FROM poliza p
JOIN producto_poliza pp ON p.id_producto = pp.id_producto
JOIN producto_beneficio pb ON pb.id_producto = pp.id_producto
WHERE p.numero_poliza = 'POL-FAM-001'
  AND pb.activo = TRUE
  AND pb.deleted_at IS NULL
  AND pb.incluido_base = TRUE;

-- Override: Hospitalización familiar se aumentó a 10M
UPDATE beneficio
SET monto_override  = 10000000.00
WHERE id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001')
  AND id_producto_beneficio = (
      SELECT id_producto_beneficio
      FROM producto_beneficio pb
      JOIN producto_poliza pp ON pb.id_producto = pp.id_producto
      WHERE pp.nombre = 'Plan Familiar' AND pb.nombre_beneficio = 'Hospitalización familiar'
  );

-- 7c. Beneficio extra personalizado para la cónyuge (Patricia)
INSERT INTO beneficio (
    id_poliza, id_producto_beneficio, id_asegurado,
    nombre_beneficio_extra, descripcion_extra,
    costo_aplicado, vigente
) VALUES (
    (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'),
    NULL,   -- beneficio extra, no viene del catálogo
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'VESP820318MDF'),   -- solo Patricia
    'Rehabilitación postparto',
    'Sesiones de fisioterapia y psicología postparto, hasta 10 sesiones al año.',
    180.00,
    TRUE
);

-- 7d. Beneficio extra personalizado para Emilio (hijo)
INSERT INTO beneficio (
    id_poliza, id_producto_beneficio, id_asegurado,
    nombre_beneficio_extra, descripcion_extra,
    costo_aplicado, vigente
) VALUES (
    (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'),
    NULL,
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'MEVE100601HDF'),   -- solo Emilio
    'Apoyo escolar',
    'Cobertura de gastos educativos por incapacidad temporal del titular.',
    90.00,
    TRUE
);


-- ------------------------------------------------------------
--  8. BENEFICIARIOS
-- ------------------------------------------------------------

-- 8a. Beneficiarios de las pólizas individuales (POL001-POL010)
INSERT INTO beneficiario (id_asegurado, id_poliza, nombre_completo, parentesco, porcentaje_participacion, telefono)
VALUES
((SELECT id_asegurado FROM asegurado WHERE rfc = 'GARL800101XXX'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL001'), 'Ana García',    'Hija',   50.0, '5511000001'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'MASL900202XXX'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL002'), 'Luis García',   'Hijo',   50.0, '5511000002'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'PECH850303XXX'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL003'), 'María Pérez',   'Esposa', 100.0,'5511000003'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'GORA870404XXX'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL004'), 'Carlos Ramírez','Hijo',   50.0, '5511000004'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'ROVM820505XXX'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL005'), 'Sofía Rojas',   'Hija',   50.0, '5511000005'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'FLOC910606XXX'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL006'), 'Diego Flores',  'Esposo', 100.0,'5511000006'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'SIMD930707XXX'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL007'), 'Valeria Silva', 'Hija',   50.0, '5511000007'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'CRVN940808XXX'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL008'), 'Miguel Navarro','Hijo',   50.0, '5511000008'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'RAOL950909XXX'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL009'), 'Luis Ortega',   'Padre',  50.0, '5511000009'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'VASM961010XXX'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL010'), 'María Soto',    'Madre',  50.0, '5511000010');

-- 8b. Beneficiarios de la familia Mendoza-Vega (POL-FAM-001)
--     Beneficiarios generales de la póliza (id_beneficio = NULL):
--     los hijos son beneficiarios del titular (50% cada uno)
INSERT INTO beneficiario (id_asegurado, id_poliza, nombre_completo, parentesco, porcentaje_participacion, telefono)
VALUES
((SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'), 'Emilio Mendoza Vega', 'Hijo',  50.0, '5521000003'),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'), 'Camila Mendoza Vega', 'Hijo',  50.0, '5521000004'),
-- El titular es beneficiario de la cónyuge (100%)
((SELECT id_asegurado FROM asegurado WHERE rfc = 'VESP820318MDF'), (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'), 'Roberto Mendoza Castro', 'Esposo', 100.0, '5521000001');

-- 8c. Beneficiario del beneficio extra de Patricia (id_beneficio != NULL)
--     Roberto Mendoza es el beneficiario designado para "Rehabilitación postparto" de Patricia
INSERT INTO beneficiario (id_asegurado, id_beneficio, nombre_completo, parentesco, porcentaje_participacion, telefono)
SELECT
    a.id_asegurado,
    b.id_beneficio,
    'Roberto Mendoza Castro',
    'Esposo',
    100.0,
    '5521000001'
FROM asegurado a
JOIN beneficio b ON b.id_asegurado = a.id_asegurado AND b.nombre_beneficio_extra = 'Rehabilitación postparto'
WHERE a.rfc = 'VESP820318MDF';

-- 8d. Beneficiario del beneficio extra de Emilio (id_beneficio != NULL)
--     Roberto (padre) y Camila (hermana) son beneficiarios de "Apoyo escolar" de Emilio
INSERT INTO beneficiario (id_asegurado, id_beneficio, nombre_completo, parentesco, porcentaje_participacion, telefono)
SELECT
    a.id_asegurado,
    b.id_beneficio,
    'Roberto Mendoza Castro',
    'Padre',
    50.0,
    '5521000001'
FROM asegurado a
JOIN beneficio b ON b.id_asegurado = a.id_asegurado AND b.nombre_beneficio_extra = 'Apoyo escolar'
WHERE a.rfc = 'MEVE100601HDF';

INSERT INTO beneficiario (id_asegurado, id_beneficio, nombre_completo, parentesco, porcentaje_participacion, telefono)
SELECT
    a.id_asegurado,
    b.id_beneficio,
    'Camila Mendoza Vega',
    'Hermana',
    50.0,
    '5521000004'
FROM asegurado a
JOIN beneficio b ON b.id_asegurado = a.id_asegurado AND b.nombre_beneficio_extra = 'Apoyo escolar'
WHERE a.rfc = 'MEVE100601HDF';


-- ------------------------------------------------------------
--  9. SEGUIMIENTO (folios)
-- ------------------------------------------------------------
INSERT INTO seguimiento (folio, id_asegurado, id_agente, asunto)
VALUES
('SEG-2025-001',
 (SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'),
 (SELECT id_agente FROM agente WHERE clave_agente = 'admin1'),
 'Contratación de Plan Familiar'),
('SEG-2025-002',
 (SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'),
 (SELECT id_agente FROM agente WHERE clave_agente = 'admin1'),
 'Solicitud de ajuste de cobertura'),
('SEG-2025-003',
 (SELECT id_asegurado FROM asegurado WHERE rfc = 'GARL800101XXX'),
 (SELECT id_agente FROM agente WHERE clave_agente = 'agente1'),
 'Renovación de póliza'),
('SEG-2025-004',
 (SELECT id_asegurado FROM asegurado WHERE rfc = 'MASL900202XXX'),
 (SELECT id_agente FROM agente WHERE clave_agente = 'agente2'),
 'Cambio de beneficiarios');


-- ------------------------------------------------------------
-- 10. SEGUIMIENTO_CONTACTO (interacciones dentro de cada folio)
-- ------------------------------------------------------------
INSERT INTO seguimiento_contacto (id_seguimiento, iniciado_por, tipo_contacto, observaciones, resultado, fecha_hora)
VALUES
-- Caso SEG-2025-001: tres contactos
( (SELECT id_seguimiento FROM seguimiento WHERE folio = 'SEG-2025-001'),
  'agente', 'llamada',
  'El cliente confirmó los datos de sus familiares y aprobó la prima mensual.',
  'resuelto', '2025-01-03 10:30:00' ),
( (SELECT id_seguimiento FROM seguimiento WHERE folio = 'SEG-2025-001'),
  'agente', 'mensaje',
  'Se envió PDF de la póliza y tabla de beneficios por WhatsApp.',
  'pendiente', '2025-01-05 16:00:00' ),
( (SELECT id_seguimiento FROM seguimiento WHERE folio = 'SEG-2025-001'),
  'asegurado', 'llamada',
  'El cliente llamó para preguntar sobre la cobertura de maternidad. Se le explicó que aplica para la cónyuge.',
  'resuelto', '2025-01-10 09:15:00' ),

-- Caso SEG-2025-002: un contacto
( (SELECT id_seguimiento FROM seguimiento WHERE folio = 'SEG-2025-002'),
  'agente', 'visita',
  'Visita domiciliaria para revisar el aumento de cobertura de Hospitalización familiar a 10M.',
  'resuelto', '2025-01-20 14:00:00' ),

-- Caso SEG-2025-003: un contacto
( (SELECT id_seguimiento FROM seguimiento WHERE folio = 'SEG-2025-003'),
  'agente', 'llamada',
  'Recordatorio de renovación de póliza. El cliente indicó que desea mantener las mismas condiciones.',
  'pendiente', '2025-11-15 11:00:00' ),

-- Caso SEG-2025-004: un contacto
( (SELECT id_seguimiento FROM seguimiento WHERE folio = 'SEG-2025-004'),
  'asegurado', 'mensaje',
  'La asegurada solicitó formato para actualizar beneficiarios.',
  'resuelto', '2025-06-01 15:30:00' );


-- ============================================================
--  CONSULTAS DE EJEMPLO
-- ============================================================

-- ------------------------------------------------------------
-- 1. Todos los beneficios de una póliza con monto efectivo
-- ------------------------------------------------------------
-- SELECT
--     COALESCE(pb.nombre_beneficio, b.nombre_beneficio_extra)  AS beneficio,
--     COALESCE(pb.descripcion,      b.descripcion_extra)       AS descripcion,
--     COALESCE(b.monto_override,    pb.monto_cobertura)        AS monto_efectivo,
--     b.costo_aplicado,
--     CASE
--         WHEN b.id_asegurado IS NULL THEN 'Toda la póliza'
--         ELSE CONCAT(a.nombre, ' ', a.apellido_paterno)
--     END AS aplica_a
-- FROM beneficio b
-- LEFT JOIN producto_beneficio pb ON b.id_producto_beneficio = pb.id_producto_beneficio
-- LEFT JOIN asegurado a           ON b.id_asegurado          = a.id_asegurado
-- WHERE b.id_poliza = 1 AND b.vigente = TRUE;


-- ------------------------------------------------------------
-- 2. Todas las personas cubiertas por una póliza
--    (titular + dependientes)
-- ------------------------------------------------------------
-- SELECT
--     a.nombre, a.apellido_paterno, a.apellido_materno,
--     'titular' AS rol_en_poliza
-- FROM poliza p
-- JOIN asegurado a ON p.id_asegurado = a.id_asegurado
-- WHERE p.id_poliza = 1
--
-- UNION ALL
--
-- SELECT
--     a.nombre, a.apellido_paterno, a.apellido_materno,
--     pd.parentesco AS rol_en_poliza
-- FROM poliza_dependiente pd
-- JOIN asegurado a ON pd.id_asegurado = a.id_asegurado
-- WHERE pd.id_poliza = 1 AND pd.deleted_at IS NULL;


-- ------------------------------------------------------------
-- 3. Historial completo de un folio de seguimiento
-- ------------------------------------------------------------
-- SELECT
--     s.folio,
--     s.asunto,
--     CONCAT(a.nombre,  ' ', a.apellido_paterno)  AS asegurado,
--     CONCAT(ag.nombre, ' ', ag.apellido_paterno) AS agente,
--     sc.iniciado_por,
--     sc.tipo_contacto,
--     sc.observaciones,
--     sc.resultado,
--     sc.fecha_hora
-- FROM seguimiento_contacto sc
-- JOIN seguimiento s  ON sc.id_seguimiento = s.id_seguimiento
-- JOIN asegurado a    ON s.id_asegurado    = a.id_asegurado
-- JOIN agente ag      ON s.id_agente       = ag.id_agente
-- WHERE s.folio = 'SEG-2026-001'
-- ORDER BY sc.fecha_hora;


-- ------------------------------------------------------------
-- 4. Beneficiarios de una póliza completa (titular)
-- ------------------------------------------------------------
-- SELECT
--     b.nombre_completo,
--     b.parentesco,
--     b.porcentaje_participacion,
--     'Póliza completa' AS aplica_a
-- FROM beneficiario b
-- WHERE b.id_poliza = 1 AND b.id_beneficio IS NULL AND b.deleted_at IS NULL;


-- ------------------------------------------------------------
-- 5. Beneficiarios por beneficio específico (dependiente)
--    Ej: quién cobra el BAC o EG1 si le pasa algo a la hija
-- ------------------------------------------------------------
-- SELECT
--     ben.nombre_completo,
--     ben.parentesco,
--     ben.porcentaje_participacion,
--     COALESCE(pb.nombre_beneficio, bef.nombre_beneficio_extra) AS beneficio,
--     CONCAT(a.nombre, ' ', a.apellido_paterno) AS asegurado_del_beneficio
-- FROM beneficiario ben
-- JOIN beneficio bef              ON ben.id_beneficio           = bef.id_beneficio
-- LEFT JOIN producto_beneficio pb ON bef.id_producto_beneficio  = pb.id_producto_beneficio
-- LEFT JOIN asegurado a           ON bef.id_asegurado           = a.id_asegurado
-- WHERE bef.id_poliza = 1 AND ben.id_beneficio IS NOT NULL AND ben.deleted_at IS NULL;
