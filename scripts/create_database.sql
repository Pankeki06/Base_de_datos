Drop database aseguradora;
CREATE DATABASE IF NOT EXISTS aseguradora CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aseguradora;


CREATE TABLE IF NOT EXISTS agente (
    id_agente INT NOT NULL PRIMARY KEY auto_increment,
    clave_agente VARCHAR(100) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    correo VARCHAR(255) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    rol ENUM('admin', 'agente') NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME null
);

CREATE TABLE IF NOT EXISTS asegurado (
    id_asegurado INT NOT NULL PRIMARY KEY auto_increment,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    rfc VARCHAR(20) NOT NULL UNIQUE,
    correo VARCHAR(255),
    celular VARCHAR(10),
    calle VARCHAR(255) NOT NULL,
    numero_exterior VARCHAR(50) NOT NULL,
    numero_interior VARCHAR(50),
    colonia VARCHAR(100) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    codigo_postal VARCHAR(20) NOT NULL,
    id_agente_responsable INT,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME null,
    FOREIGN KEY (id_agente_responsable) REFERENCES agente(id_agente) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS beneficiario (
    id_beneficiario INT NOT NULL PRIMARY KEY auto_increment,
    id_asegurado INT NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    parentesco VARCHAR(50) NOT NULL,
    porcentaje_participacion FLOAT NOT NULL,
    telefono VARCHAR(20),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME null,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS poliza (
    id_poliza INT NOT NULL PRIMARY KEY auto_increment,
    id_asegurado INT NOT NULL,
    numero_poliza VARCHAR(100) NOT NULL UNIQUE,
    tipo_seguro VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    estatus ENUM('activa', 'vencida', 'cancelada') NOT NULL,
    prima_mensual FLOAT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME null,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS beneficio (
    id_beneficio INT NOT NULL PRIMARY KEY auto_increment,
    id_poliza INT NOT NULL,
    nombre_beneficio VARCHAR(255) NOT NULL,
    descripcion VARCHAR(500) NOT NULL,
    monto_cobertura FLOAT NOT NULL,
    vigente BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (id_poliza) REFERENCES poliza(id_poliza) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS seguimiento (
    id_seguimiento INT NOT NULL PRIMARY KEY auto_increment,
    id_asegurado INT NOT NULL,
    id_agente INT NOT NULL,
    tipo_contacto ENUM('llamada', 'visita', 'mensaje') NOT NULL,
    observaciones TEXT NOT NULL,
    resultado ENUM('resuelto', 'pendiente', 'sin_respuesta') NOT NULL,
    fecha_hora DATETIME NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME null,
    FOREIGN KEY (id_asegurado) REFERENCES asegurado(id_asegurado) ON DELETE CASCADE,
    FOREIGN KEY (id_agente) REFERENCES agente(id_agente) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sesion (
    id_sesion INT NOT NULL PRIMARY KEY auto_increment,
    id_agente INT NOT NULL,
    inicio_sesion DATETIME NOT NULL,
    fin_sesion DATETIME,
    FOREIGN KEY (id_agente) REFERENCES agente(id_agente) ON DELETE CASCADE
);

INSERT IGNORE INTO agente (
    id_agente,
    clave_agente,
    nombre,
    apellido_paterno,
    apellido_materno,
    correo,
    telefono,
    rol,
    password,
    created_at,
    updated_at
) VALUES (
    UUID(),
    'admin1',
    'Administrador',
    'Sistema',
    'Demo',
    'admin@seguros.com',
    '5512345678',
    'admin',
    '1234',
    NOW(),
    NOW()
);
