-- ============================================================
--  BASE DE DATOS: aseguradora  (v4 - final)
--
--  Cambios respecto a v3:
--
--  1. Se eliminó `poliza_dependiente` — el tipo de asegurado
--     y su vinculación a una póliza se maneja directo en
--     la tabla `asegurado` con los campos:
--       · tipo_asegurado: titular, conyuge, hijo, dependiente
--       · id_poliza: NULL si es titular, NOT NULL
--         si pertenece a la póliza de otro asegurado
--
--  2. `beneficiario` ahora usa id_asegurado para identificar
--     de quién es el beneficiario (titular o dependiente),
--     y se distingue por el tipo_asegurado del asegurado.
--
--  3. `beneficio` siempre referencia producto_beneficio
--     (no permite extras). id_asegurado NULL = titular.
--
--  4. `seguimiento` es un folio/caso; `seguimiento_contacto`
--     guarda cada interacción del historial.
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
-- ============================================================
CREATE TABLE IF NOT EXISTS producto_poliza (
    id_producto  INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre       VARCHAR(150) NOT NULL UNIQUE,
    descripcion  TEXT,
    tipo_seguro  VARCHAR(100) NOT NULL,
    prima_base   FLOAT        NOT NULL,
    activo       BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at   DATETIME     NULL
);


-- ============================================================
--  PRODUCTO_BENEFICIO
--  Coberturas base de cada producto del catálogo.
--  Los beneficios de una póliza siempre referencian aquí.
-- ============================================================
CREATE TABLE IF NOT EXISTS producto_beneficio (
    id_producto_beneficio INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_producto           INT          NOT NULL,
    nombre_beneficio      VARCHAR(255) NOT NULL,
    descripcion           VARCHAR(500) NOT NULL,
    monto_cobertura       FLOAT        NOT NULL,
    costo_extra           FLOAT        NULL,
    incluido_base         BOOLEAN      NOT NULL DEFAULT TRUE,
    activo                BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at            DATETIME     NULL,
    FOREIGN KEY (id_producto) REFERENCES producto_poliza(id_producto) ON DELETE CASCADE
);


-- ============================================================
--  ASEGURADO
--  Persona registrada en el sistema.
--
--  tipo_asegurado distingue si es titular o dependiente.
--  id_poliza solo se llena cuando es dependiente — indica
--  a qué póliza pertenece. Un dependiente solo puede
--  pertenecer a una póliza.
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
    tipo_asegurado        ENUM('titular', 'conyuge', 'hijo', 'dependiente') NOT NULL DEFAULT 'titular',
    id_poliza             INT          NULL,     -- NULL si es titular / NOT NULL si es dependiente
    id_agente_responsable INT,
    created_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at            DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at            DATETIME     NULL,
    FOREIGN KEY (id_agente_responsable) REFERENCES agente(id_agente) ON DELETE SET NULL
    -- FK a poliza se agrega después de crear la tabla poliza
);


-- ============================================================
--  POLIZA
--  Contrato de seguro. id_asegurado = el titular.
-- ============================================================
CREATE TABLE IF NOT EXISTS poliza (
    id_poliza         INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_asegurado      INT          NOT NULL,
    id_producto       INT          NOT NULL,
    numero_poliza     VARCHAR(100) NOT NULL UNIQUE,
    fecha_inicio      DATE         NOT NULL,
    fecha_vencimiento DATE         NOT NULL,
    estatus           ENUM('activa', 'vencida', 'cancelada') NOT NULL,
    prima_mensual     FLOAT        NOT NULL,
    created_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at        DATETIME     NULL,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE,
    FOREIGN KEY (id_producto)  REFERENCES producto_poliza(id_producto) ON DELETE RESTRICT
);

-- FK circular: asegurado.id_poliza → poliza
ALTER TABLE asegurado
    ADD CONSTRAINT fk_asegurado_poliza
    FOREIGN KEY (id_poliza) REFERENCES poliza(id_poliza) ON DELETE SET NULL;


-- ============================================================
--  BENEFICIO
--  Coberturas activas de una póliza contratada.
--  Siempre vienen del catálogo (id_producto_beneficio NOT NULL).
--
--  id_asegurado NULL     → aplica a toda la póliza (titular)
--  id_asegurado NOT NULL → aplica solo a ese dependiente
-- ============================================================
CREATE TABLE IF NOT EXISTS beneficio (
    id_beneficio          INT   NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_poliza             INT   NOT NULL,
    id_producto_beneficio INT   NOT NULL,
    id_asegurado          INT   NULL,     -- NULL = toda la póliza / NOT NULL = dependiente
    monto_override        FLOAT NULL,     -- NULL = usa el monto del catálogo
    costo_aplicado        FLOAT NOT NULL, -- congelado al momento de contratar
    vigente               BOOLEAN NOT NULL DEFAULT TRUE,
    deleted_at            DATETIME NULL,
    FOREIGN KEY (id_poliza)             REFERENCES poliza(id_poliza)                         ON DELETE CASCADE,
    FOREIGN KEY (id_producto_beneficio) REFERENCES producto_beneficio(id_producto_beneficio) ON DELETE RESTRICT,
    FOREIGN KEY (id_asegurado)          REFERENCES asegurado(id_asegurado)                   ON DELETE SET NULL
);


-- ============================================================
--  BENEFICIARIO
--  Quien recibe el dinero en caso de siniestro.
--
--  id_asegurado → de quién es este beneficiario
--                 (puede ser el titular o un dependiente)
--  id_poliza    → a qué póliza pertenece
--
--  Para saber si es del titular o de un dependiente basta
--  con revisar asegurado.tipo_asegurado del id_asegurado.
-- ============================================================
CREATE TABLE IF NOT EXISTS beneficiario (
    id_beneficiario          INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_poliza                INT          NOT NULL,
    id_asegurado             INT          NOT NULL,
    nombre_completo          VARCHAR(255) NOT NULL,
    parentesco               VARCHAR(50)  NOT NULL,
    porcentaje_participacion FLOAT        NOT NULL,
    telefono                 VARCHAR(20),
    created_at               DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at               DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at               DATETIME     NULL,
    FOREIGN KEY (id_poliza)    REFERENCES poliza(id_poliza)       ON DELETE CASCADE,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE
);


-- ============================================================
--  SEGUIMIENTO
--  Folio/caso — agrupa todas las interacciones sobre un
--  mismo asunto entre un asegurado y su agente.
-- ============================================================
CREATE TABLE IF NOT EXISTS seguimiento (
    id_seguimiento INT          NOT NULL PRIMARY KEY AUTO_INCREMENT,
    folio          VARCHAR(20)  NOT NULL UNIQUE,   -- ej: "SEG-2026-001"
    id_asegurado   INT          NOT NULL,
    id_agente      INT          NOT NULL,
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
--  Soporta contacto en ambas direcciones (agente ↔ asegurado).
--  No repite id_agente/id_asegurado — se obtienen con JOIN
--  desde seguimiento.
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
    updated_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at     DATETIME     NULL,
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
('agente1','1000000001','Juan','Pérez','López','juan@correo.com','5550000001','agente','561badc3e947be14672a3511feb3c633c3c349fec042da8b916829ee523a680c',NOW(),NOW());


-- ------------------------------------------------------------
--  2. CATÁLOGO DE PRODUCTOS
-- ------------------------------------------------------------
INSERT INTO producto_poliza (nombre, descripcion, tipo_seguro, prima_base) VALUES
('Plan Familiar',    'Cobertura integral para titular, cónyuge e hijos con beneficios preventivos incluidos.','Gastos Médicos Mayores', 2100.00),
('Vida Plus',        'Seguro de vida con suma asegurada flexible y protección por accidentes.',               'Vida',                   650.00),
('Cuidándote',       'Póliza de gastos médicos mayores con amplia red de hospitales y cobertura nacional.',    'Gastos Médicos Mayores', 1200.00),
('Básico Accidentes','Cobertura esencial ante accidentes personales, ideal como complemento.',                'Accidentes Personales',  300.00);


-- ------------------------------------------------------------
--  3. BENEFICIOS BASE POR PRODUCTO
-- ------------------------------------------------------------
-- Plan Familiar (id_producto = 1)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(1, 'Hospitalización familiar',   'Cobertura de internamiento para todos los miembros.',              8000000.00, NULL,  TRUE),
(1, 'Cirugía',                    'Honorarios médicos y gastos quirúrgicos para titular y familia.',  5000000.00, NULL,  TRUE),
(1, 'Consultas preventivas',      'Hasta 6 consultas anuales por miembro cubierto.',                     6000.00, NULL,  TRUE),
(1, 'Vacunas infantiles',         'Esquema completo de vacunación para hijos menores de 12 años.',      5000.00, NULL,  TRUE),
(1, 'Maternidad',                 'Cobertura de parto normal y cesárea.',                              100000.00, NULL,  TRUE),
(1, 'Odontología básica',         'Limpiezas, extracciones y radiografías.',                             8000.00, 120.00, FALSE);

-- Vida Plus (id_producto = 2)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(2, 'Suma asegurada por fallecimiento', 'Pago único a beneficiarios en caso de fallecimiento.',          1000000.00, NULL,   TRUE),
(2, 'Doble indemnización accidente',    'Doble de la suma asegurada si el fallecimiento es por accidente.',2000000.00, NULL,   TRUE),
(2, 'Invalidez total permanente',       'Anticipo del 100% de la suma asegurada.',                        1000000.00, NULL,   TRUE),
(2, 'Enfermedades graves',              'Diagnóstico de cáncer, infarto o EVC cubre hasta el 50%.',        500000.00, 180.00, FALSE);

-- Cuidándote (id_producto = 3)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(3, 'Hospitalización',       'Gastos de internamiento en hospital de la red.',              5000000.00, NULL,  TRUE),
(3, 'Cirugía',               'Honorarios médicos y gastos quirúrgicos.',                    3000000.00, NULL,  TRUE),
(3, 'Médico a domicilio',    'Hasta 3 consultas anuales sin costo adicional.',                 3000.00, NULL,  TRUE),
(3, 'Maternidad',            'Cobertura de parto normal y cesárea.',                          80000.00, 240.00, FALSE),
(3, 'Dental preventivo',     'Limpieza y revisión anual incluida.',                            2500.00, 95.00,  FALSE);

-- Básico Accidentes (id_producto = 4)
INSERT INTO producto_beneficio (id_producto, nombre_beneficio, descripcion, monto_cobertura, costo_extra, incluido_base) VALUES
(4, 'Muerte accidental',            'Pago único a beneficiarios por fallecimiento en accidente.',   300000.00, NULL, TRUE),
(4, 'Gastos médicos por accidente', 'Atención de urgencia y hospitalización por accidente.',         50000.00, NULL, TRUE),
(4, 'Invalidez parcial',            'Indemnización proporcional según tabla de invalideces.',      150000.00, NULL, TRUE);


-- ------------------------------------------------------------
--  4. ASEGURADOS
--      (Los dependientes se crean primero sin id_poliza)
-- ------------------------------------------------------------
INSERT INTO asegurado (
    nombre, apellido_paterno, apellido_materno, rfc, correo, celular,
    calle, numero_exterior, numero_interior, colonia, municipio, estado,
    codigo_postal, tipo_asegurado, id_poliza, id_agente_responsable
) VALUES
-- Familia Mendoza (titular + dependientes)
('Roberto', 'Mendoza', 'Castro',  'MECR780512HDF', 'roberto.mendoza@example.com', '5521000001', 'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', 'titular',     NULL, (SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Patricia','Vega',    'Suárez',  'VESP820318MDF', 'patricia.vega@example.com',   '5521000002', 'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', 'titular',     NULL, (SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Emilio',  'Mendoza', 'Vega',    'MEVE100601HDF', NULL,                          NULL,         'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', 'titular',     NULL, (SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Camila',  'Mendoza', 'Vega',    'MEVC130915MDF', NULL,                          NULL,         'Av. Insurgentes', '200', '3B', 'Del Valle', 'Benito Juárez', 'Ciudad de México', '03100', 'titular',     NULL, (SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
-- Titulares individuales
('Carlos',  'Ramírez', 'Soto',    'CARS850303XXX', 'carlos@example.com',          '5511110003', 'Calle Luna',      '78',  NULL, 'Roma',      'Ciudad',        'Estado3',            '01020', 'titular',     NULL, (SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Lucía',   'Martínez','Sánchez', 'MASL900202XXX', 'lucia@example.com',           '5511110002', 'Av. Reforma',     '45',  'A',  'Juárez',    'Ciudad',        'Estado2',            '01010', 'titular',     NULL, (SELECT id_agente FROM agente WHERE clave_agente = 'agente1'));


-- ------------------------------------------------------------
--  5. PÓLIZAS
-- ------------------------------------------------------------
INSERT INTO poliza (
    id_asegurado, id_producto, numero_poliza,
    fecha_inicio, fecha_vencimiento, estatus, prima_mensual
) VALUES
-- Póliza familiar activa (Roberto es titular)
((SELECT id_asegurado FROM asegurado WHERE rfc = 'MECR780512HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Plan Familiar'),    'POL-FAM-001', '2026-01-01', '2027-01-01', 'activa',  2220.00),
-- Pólizas individuales vencidas
((SELECT id_asegurado FROM asegurado WHERE rfc = 'CARS850303XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Vida Plus'),        'POL-IND-001', '2024-03-01', '2025-03-01', 'vencida',  650.00),
((SELECT id_asegurado FROM asegurado WHERE rfc = 'MASL900202XXX'), (SELECT id_producto FROM producto_poliza WHERE nombre = 'Cuidándote'),       'POL-IND-002', '2024-02-01', '2025-02-01', 'vencida', 1200.00);


-- ------------------------------------------------------------
--  6. VINCULAR DEPENDIENTES A PÓLIZA FAMILIAR
--      (Actualizar asegurado: tipo_asegurado + id_poliza)
-- ------------------------------------------------------------
UPDATE asegurado SET tipo_asegurado = 'conyuge', id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001') WHERE rfc = 'VESP820318MDF';
UPDATE asegurado SET tipo_asegurado = 'hijo',    id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001') WHERE rfc = 'MEVE100601HDF';
UPDATE asegurado SET tipo_asegurado = 'hijo',    id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001') WHERE rfc = 'MEVC130915MDF';


-- ------------------------------------------------------------
--  7. BENEFICIOS DE CADA PÓLIZA
-- ------------------------------------------------------------

-- 7a. Beneficios de POL-FAM-001 (Plan Familiar) — copia solo base activos
INSERT INTO beneficio (id_poliza, id_producto_beneficio, id_asegurado, costo_aplicado, vigente)
SELECT
    p.id_poliza,
    pb.id_producto_beneficio,
    NULL,  -- aplica al titular
    CASE WHEN pb.incluido_base THEN 0 ELSE COALESCE(pb.costo_extra, 0) END,
    TRUE
FROM poliza p
JOIN producto_poliza pp ON p.id_producto = pp.id_producto
JOIN producto_beneficio pb ON pb.id_producto = pp.id_producto
WHERE p.numero_poliza = 'POL-FAM-001'
  AND pb.activo = TRUE
  AND pb.deleted_at IS NULL
  AND pb.incluido_base = TRUE;

-- 7b. Beneficios de pólizas individuales vencidas (mismo patrón)
INSERT INTO beneficio (id_poliza, id_producto_beneficio, id_asegurado, costo_aplicado, vigente)
SELECT
    p.id_poliza,
    pb.id_producto_beneficio,
    NULL,
    CASE WHEN pb.incluido_base THEN 0 ELSE COALESCE(pb.costo_extra, 0) END,
    TRUE
FROM poliza p
JOIN producto_poliza pp ON p.id_producto = pp.id_producto
JOIN producto_beneficio pb ON pb.id_producto = pp.id_producto
WHERE p.numero_poliza IN ('POL-IND-001', 'POL-IND-002')
  AND pb.activo = TRUE
  AND pb.deleted_at IS NULL
  AND pb.incluido_base = TRUE;

-- 7c. Override: Hospitalización familiar de Plan Familiar → 10M
UPDATE beneficio
SET monto_override = 10000000.00
WHERE id_poliza = (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001')
  AND id_producto_beneficio = (
      SELECT id_producto_beneficio
      FROM producto_beneficio
      WHERE nombre_beneficio = 'Hospitalización familiar' AND activo = TRUE
  );

-- 7d. Beneficio ODONTOLÓGICO contratado (no base) en Plan Familiar
INSERT INTO beneficio (id_poliza, id_producto_beneficio, id_asegurado, costo_aplicado, vigente)
SELECT
    p.id_poliza,
    pb.id_producto_beneficio,
    NULL,
    pb.costo_extra,
    TRUE
FROM poliza p
JOIN producto_beneficio pb ON pb.id_producto = p.id_producto
WHERE p.numero_poliza = 'POL-FAM-001'
  AND pb.nombre_beneficio = 'Odontología básica'
  AND pb.activo = TRUE;

-- 7e. Beneficio específico para la cónyuge (Patricia) dentro de Plan Familiar
INSERT INTO beneficio (id_poliza, id_producto_beneficio, id_asegurado, costo_aplicado, vigente)
SELECT
    p.id_poliza,
    pb.id_producto_beneficio,
    a.id_asegurado,  -- Patricia
    CASE WHEN pb.incluido_base THEN 0 ELSE COALESCE(pb.costo_extra, 0) END,
    TRUE
FROM poliza p
JOIN producto_beneficio pb ON pb.id_producto = p.id_producto
JOIN asegurado a ON a.rfc = 'VESP820318MDF'
WHERE p.numero_poliza = 'POL-FAM-001'
  AND pb.nombre_beneficio = 'Maternidad'
  AND pb.activo = TRUE;


-- ------------------------------------------------------------
--  8. BENEFICIARIOS
-- ------------------------------------------------------------

-- 8a. Beneficiarios de Carlos Ramírez (POL-IND-001, titular)
INSERT INTO beneficiario (id_poliza, id_asegurado, nombre_completo, parentesco, porcentaje_participacion, telefono)
SELECT
    p.id_poliza,
    a.id_asegurado,
    'María Pérez',
    'Esposa',
    100.0,
    '5511000003'
FROM poliza p
JOIN asegurado a ON a.rfc = 'CARS850303XXX'
WHERE p.numero_poliza = 'POL-IND-001';

-- 8b. Beneficiarios de Lucía Martínez (POL-IND-002, titular)
INSERT INTO beneficiario (id_poliza, id_asegurado, nombre_completo, parentesco, porcentaje_participacion, telefono)
SELECT
    p.id_poliza,
    a.id_asegurado,
    'Luis García',
    'Hijo',
    100.0,
    '5511000002'
FROM poliza p
JOIN asegurado a ON a.rfc = 'MASL900202XXX'
WHERE p.numero_poliza = 'POL-IND-002';

-- 8c. Beneficiarios del titular Roberto (POL-FAM-001)
INSERT INTO beneficiario (id_poliza, id_asegurado, nombre_completo, parentesco, porcentaje_participacion, telefono)
SELECT
    p.id_poliza,
    a.id_asegurado,
    'Patricia Vega',
    'Esposa',
    100.0,
    '5521000002'
FROM poliza p
JOIN asegurado a ON a.rfc = 'MECR780512HDF'
WHERE p.numero_poliza = 'POL-FAM-001';

-- 8d. Beneficiarios de la cónyuge Patricia (dependiente, POL-FAM-001)
INSERT INTO beneficiario (id_poliza, id_asegurado, nombre_completo, parentesco, porcentaje_participacion, telefono)
SELECT
    p.id_poliza,
    a.id_asegurado,
    'Roberto Mendoza',
    'Esposo',
    100.0,
    '5521000001'
FROM poliza p
JOIN asegurado a ON a.rfc = 'VESP820318MDF'
WHERE p.numero_poliza = 'POL-FAM-001';

-- 8e. Beneficiarios del hijo Emilio (dependiente, POL-FAM-001)
INSERT INTO beneficiario (id_poliza, id_asegurado, nombre_completo, parentesco, porcentaje_participacion, telefono)
VALUES
(
    (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'),
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'MEVE100601HDF'),
    'Roberto Mendoza',
    'Padre',
    50.0,
    '5521000001'
),
(
    (SELECT id_poliza FROM poliza WHERE numero_poliza = 'POL-FAM-001'),
    (SELECT id_asegurado FROM asegurado WHERE rfc = 'MEVE100601HDF'),
    'Camila Mendoza',
    'Hermana',
    50.0,
    NULL
);


-- ------------------------------------------------------------
--  9. SEGUIMIENTO (Folios)
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
 (SELECT id_asegurado FROM asegurado WHERE rfc = 'CARS850303XXX'),
 (SELECT id_agente FROM agente WHERE clave_agente = 'agente1'),
 'Renovación de póliza Vida Plus'),
('SEG-2025-004',
 (SELECT id_asegurado FROM asegurado WHERE rfc = 'MASL900202XXX'),
 (SELECT id_agente FROM agente WHERE clave_agente = 'agente1'),
 'Cambio de beneficiarios');


-- ------------------------------------------------------------
-- 10. SEGUIMIENTO_CONTACTO (Interacciones dentro de cada folio)
-- ------------------------------------------------------------
INSERT INTO seguimiento_contacto (id_seguimiento, iniciado_por, tipo_contacto, observaciones, resultado, fecha_hora)
VALUES
-- Folio SEG-2025-001: Contratación Plan Familiar (3 contactos)
( (SELECT id_seguimiento FROM seguimiento WHERE folio = 'SEG-2025-001'),
  'agente', 'llamada',
  'El cliente confirmó los datos de sus familiares y aprobó la prima mensual de $2,220.',
  'resuelto', '2025-01-03 10:30:00' ),
( (SELECT id_seguimiento FROM seguimiento WHERE folio = 'SEG-2025-001'),
  'agente', 'mensaje',
  'Se envió PDF de la póliza y tabla de beneficios por WhatsApp.',
  'pendiente', '2025-01-05 16:00:00' ),
( (SELECT id_seguimiento FROM seguimiento WHERE folio = 'SEG-2025-001'),
  'asegurado', 'llamada',
  'El cliente llamó para preguntar sobre la cobertura de maternidad. Se le explicó que aplica para la cónyuge Patricia.',
  'resuelto', '2025-01-10 09:15:00' ),

-- Folio SEG-2025-002: Ajuste de cobertura (1 contacto)
( (SELECT id_seguimiento FROM seguimiento WHERE folio = 'SEG-2025-002'),
  'agente', 'visita',
  'Visita domiciliaria para revisar el aumento de cobertura de Hospitalización familiar a $10,000,000.',
  'resuelto', '2025-01-20 14:00:00' ),

-- Folio SEG-2025-003: Renovación (1 contacto)
( (SELECT id_seguimiento FROM seguimiento WHERE folio = 'SEG-2025-003'),
  'agente', 'llamada',
  'Recordatorio de renovación de póliza. El cliente indicó que desea mantener las mismas condiciones.',
  'pendiente', '2025-11-15 11:00:00' ),

-- Folio SEG-2025-004: Cambio de beneficiarios (1 contacto)
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
--     pb.nombre_beneficio,
--     pb.descripcion,
--     COALESCE(b.monto_override, pb.monto_cobertura) AS monto_efectivo,
--     b.costo_aplicado,
--     CASE
--         WHEN b.id_asegurado IS NULL THEN 'Toda la póliza'
--         ELSE CONCAT(a.nombre, ' ', a.apellido_paterno)
--     END AS aplica_a
-- FROM beneficio b
-- JOIN producto_beneficio pb ON b.id_producto_beneficio = pb.id_producto_beneficio
-- LEFT JOIN asegurado a      ON b.id_asegurado          = a.id_asegurado
-- WHERE b.id_poliza = 1 AND b.vigente = TRUE;


-- ------------------------------------------------------------
-- 2. Titular y dependientes de una póliza
-- ------------------------------------------------------------
-- SELECT
--     a.nombre, a.apellido_paterno, a.apellido_materno,
--     a.tipo_asegurado
-- FROM asegurado a
-- WHERE (a.id_asegurado = (SELECT id_asegurado FROM poliza WHERE id_poliza = 1))
--    OR (a.id_poliza = 1 AND a.tipo_asegurado != 'titular');


-- ------------------------------------------------------------
-- 3. Beneficiarios del titular de una póliza
-- ------------------------------------------------------------
-- SELECT b.*
-- FROM beneficiario b
-- JOIN poliza p ON b.id_poliza = p.id_poliza
-- WHERE b.id_poliza = 1
--   AND b.id_asegurado = p.id_asegurado
--   AND b.deleted_at IS NULL;


-- ------------------------------------------------------------
-- 4. Beneficiarios de un dependiente específico
-- ------------------------------------------------------------
-- SELECT b.*
-- FROM beneficiario b
-- JOIN asegurado a ON b.id_asegurado = a.id_asegurado
-- WHERE b.id_poliza = 1
--   AND a.tipo_asegurado != 'titular'
--   AND b.id_asegurado = ?;  -- id del dependiente


-- ------------------------------------------------------------
-- 5. Historial completo de un folio
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


-- ============================================================
--  ÍNDICES DE RENDIMIENTO (optimización listado asegurados)
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_asegurado_agente_deleted
    ON asegurado(id_agente_responsable, deleted_at);

CREATE INDEX IF NOT EXISTS idx_asegurado_poliza_tipo
    ON asegurado(id_poliza, tipo_asegurado);

CREATE INDEX IF NOT EXISTS idx_poliza_asegurado_deleted
    ON poliza(id_asegurado, deleted_at);

CREATE INDEX IF NOT EXISTS idx_beneficiario_asegurado_deleted
    ON beneficiario(id_asegurado, deleted_at);
