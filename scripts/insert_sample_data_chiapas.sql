-- ============================================================
--  DATOS DE MUESTRA: Asegurados de Chiapas
--  Ciudades: Tuxtla Gutiérrez y San Cristóbal de las Casas
-- ============================================================
USE aseguradora;

-- ============================================================
--  1. ASEGURADOS
--     20 familias (titular + cónyuge + hijos) + 10 individuales
-- ============================================================
INSERT INTO asegurado (
    nombre, apellido_paterno, apellido_materno, rfc, correo, celular,
    calle, numero_exterior, numero_interior, colonia, municipio, estado,
    codigo_postal, tipo_asegurado, id_poliza, id_agente_responsable
) VALUES

-- === Familia 1 (Tuxtla) ===
('Jorge Alberto','López','Hernández','LOHJ750615HDF','jorge.lopez@correo.com','9611234567','Av. Central','125',NULL,'Centro','Tuxtla Gutiérrez','Chiapas','29000','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('María Guadalupe','López','Ruiz','LORM800320MDF','glopez@correo.com','9611234568','Av. Central','125',NULL,'Centro','Tuxtla Gutiérrez','Chiapas','29000','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Diego','López','Ruiz','LORD050410HDF',NULL,NULL,'Av. Central','125',NULL,'Centro','Tuxtla Gutiérrez','Chiapas','29000','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Fernanda','López','Ruiz','LORF080612MDF',NULL,NULL,'Av. Central','125',NULL,'Centro','Tuxtla Gutiérrez','Chiapas','29000','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 2 (San Cristóbal) ===
('Marco Antonio','Vásquez','Silva','VASM700825HDF','marco.vasquez@correo.com','9674567890','Real de Guadalupe','45',NULL,'Centro','San Cristóbal de las Casas','Chiapas','29200','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Rosa Elena','Vásquez','Morales','VASR750910MDF','relena.vasquez@correo.com','9674567891','Real de Guadalupe','45',NULL,'Centro','San Cristóbal de las Casas','Chiapas','29200','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Andrés','Vásquez','Morales','VASA120315HDF',NULL,NULL,'Real de Guadalupe','45',NULL,'Centro','San Cristóbal de las Casas','Chiapas','29200','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 3 (Tuxtla) ===
('Luis Fernando','García','Cruz','GACL850330HDF','luis.garcia@correo.com','9612345678','1a. Norte','78',NULL,'Terán','Tuxtla Gutiérrez','Chiapas','29030','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Claudia Patricia','García','Reyes','GARC900115MDF','claudia.garcia@correo.com','9612345679','1a. Norte','78',NULL,'Terán','Tuxtla Gutiérrez','Chiapas','29030','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Daniel','García','Reyes','GARD100520HDF',NULL,NULL,'1a. Norte','78',NULL,'Terán','Tuxtla Gutiérrez','Chiapas','29030','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Valentina','García','Reyes','GARV130430MDF',NULL,NULL,'1a. Norte','78',NULL,'Terán','Tuxtla Gutiérrez','Chiapas','29030','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Mateo','García','Reyes','GARM180615HDF',NULL,NULL,'1a. Norte','78',NULL,'Terán','Tuxtla Gutiérrez','Chiapas','29030','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 4 (San Cristóbal) ===
('Miguel Ángel','Torres','Flores','TOFM680710HDF','miguel.torres@correo.com','9671122334','Insurgentes','234','A','Cuxtitali','San Cristóbal de las Casas','Chiapas','29220','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Carmen Alicia','Torres','Pérez','TOFC720505MDF','carmen.torres@correo.com','9671122335','Insurgentes','234','A','Cuxtitali','San Cristóbal de las Casas','Chiapas','29220','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Lucía','Torres','Pérez','TOFL090830MDF',NULL,NULL,'Insurgentes','234','A','Cuxtitali','San Cristóbal de las Casas','Chiapas','29220','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 5 (Tuxtla) ===
('Juan Carlos','Ramírez','Aguilar','RAJC800120HDF','juan.ramirez@correo.com','9613456789','Belisario Domínguez','56',NULL,'Plan de Ayala','Tuxtla Gutiérrez','Chiapas','29020','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Ana Laura','Ramírez','Castillo','RALA850930MDF','ana.ramirez@correo.com','9613456790','Belisario Domínguez','56',NULL,'Plan de Ayala','Tuxtla Gutiérrez','Chiapas','29020','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Sofía','Ramírez','Castillo','RALS110715MDF',NULL,NULL,'Belisario Domínguez','56',NULL,'Plan de Ayala','Tuxtla Gutiérrez','Chiapas','29020','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Emiliano','Ramírez','Castillo','RALE150310HDF',NULL,NULL,'Belisario Domínguez','56',NULL,'Plan de Ayala','Tuxtla Gutiérrez','Chiapas','29020','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 6 (San Cristóbal) ===
('José Luis','Rodríguez','Mendoza','ROMJ760405HDF','jose.rodriguez@correo.com','9673344556','Francisco I. Madero','89','2','Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Gabriela','Rodríguez','Sánchez','RORG820720MDF','gaby.rodriguez@correo.com','9673344557','Francisco I. Madero','89','2','Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Mariana','Rodríguez','Sánchez','RORM160120MDF',NULL,NULL,'Francisco I. Madero','89','2','Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 7 (Tuxtla) ===
('Pedro Antonio','González','Ríos','GORP720310HDF','pedro.gonzalez@correo.com','9614567890','16 de Septiembre','90',NULL,'Las Granjas','Tuxtla Gutiérrez','Chiapas','29047','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Verónica Isabel','González','Luna','GORV780525MDF','vgonzalez@correo.com','9614567891','16 de Septiembre','90',NULL,'Las Granjas','Tuxtla Gutiérrez','Chiapas','29047','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Alejandro','González','Luna','GORA020830HDF',NULL,NULL,'16 de Septiembre','90',NULL,'Las Granjas','Tuxtla Gutiérrez','Chiapas','29047','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Natalia','González','Luna','GORN060115MDF',NULL,NULL,'16 de Septiembre','90',NULL,'Las Granjas','Tuxtla Gutiérrez','Chiapas','29047','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 8 (San Cristóbal) ===
('Francisco Javier','Hernández','Bravo','HEBF650820HDF','francisco.hernandez@correo.com','9675566778','20 de Noviembre','12',NULL,'Mexicanos','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Teresa Dolores','Hernández','Vargas','HEBT700215MDF','tere.hernandez@correo.com','9675566779','20 de Noviembre','12',NULL,'Mexicanos','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Ricardo','Hernández','Vargas','HEBR030930HDF',NULL,NULL,'20 de Noviembre','12',NULL,'Mexicanos','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Paula','Hernández','Vargas','HEBP070820MDF',NULL,NULL,'20 de Noviembre','12',NULL,'Mexicanos','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 9 (Tuxtla) ===
('Manuel Alejandro','Martínez','Ortiz','MAOM880615HDF','manuel.martinez@correo.com','9615678901','Emiliano Zapata','45',NULL,'El Jobo','Tuxtla Gutiérrez','Chiapas','29049','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Leticia María','Martínez','Domínguez','MAOL930405MDF','leti.martinez@correo.com','9615678902','Emiliano Zapata','45',NULL,'El Jobo','Tuxtla Gutiérrez','Chiapas','29049','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Isabela','Martínez','Domínguez','MAOI170910MDF',NULL,NULL,'Emiliano Zapata','45',NULL,'El Jobo','Tuxtla Gutiérrez','Chiapas','29049','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 10 (San Cristóbal) ===
('Roberto Carlos','Sánchez','Guerrero','SAGR740925HDF','roberto.sanchez@correo.com','9677890123','Comitán','67',NULL,'Santa Lucía','San Cristóbal de las Casas','Chiapas','29250','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Margarita Elena','Sánchez','Jiménez','SAGM790830MDF','magui.sanchez@correo.com','9677890124','Comitán','67',NULL,'Santa Lucía','San Cristóbal de las Casas','Chiapas','29250','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Carlos','Sánchez','Jiménez','SAGC080215HDF',NULL,NULL,'Comitán','67',NULL,'Santa Lucía','San Cristóbal de las Casas','Chiapas','29250','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Diana','Sánchez','Jiménez','SAGD110430MDF',NULL,NULL,'Comitán','67',NULL,'Santa Lucía','San Cristóbal de las Casas','Chiapas','29250','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Elena','Sánchez','Jiménez','SAGE150610MDF',NULL,NULL,'Comitán','67',NULL,'Santa Lucía','San Cristóbal de las Casas','Chiapas','29250','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 11 (Tuxtla) ===
('Diego Armando','Flores','Nuñez','FOND810720HDF','diego.flores@correo.com','9616789012','Cuauhtémoc','112','B','Albania Alta','Tuxtla Gutiérrez','Chiapas','29010','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Alejandra','Flores','Camacho','FONA860415MDF','ale.flores@correo.com','9616789013','Cuauhtémoc','112','B','Albania Alta','Tuxtla Gutiérrez','Chiapas','29010','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Sebastián','Flores','Camacho','FONS120915HDF',NULL,NULL,'Cuauhtémoc','112','B','Albania Alta','Tuxtla Gutiérrez','Chiapas','29010','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 12 (San Cristóbal) ===
('Fernando José','Ruiz','Medina','RUMF770520HDF','fernando.ruiz@correo.com','9678901234','Chiapa de Corzo','23',NULL,'El Cerrillo','San Cristóbal de las Casas','Chiapas','29260','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Diana Laura','Ruiz','Romero','RUMD830110MDF','diana.ruiz@correo.com','9678901235','Chiapa de Corzo','23',NULL,'El Cerrillo','San Cristóbal de las Casas','Chiapas','29260','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Santiago','Ruiz','Romero','RUMS040630HDF',NULL,NULL,'Chiapa de Corzo','23',NULL,'El Cerrillo','San Cristóbal de las Casas','Chiapas','29260','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Camila','Ruiz','Romero','RUMC080115MDF',NULL,NULL,'Chiapa de Corzo','23',NULL,'El Cerrillo','San Cristóbal de las Casas','Chiapas','29260','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 13 (Tuxtla) ===
('Raúl Eduardo','Jiménez','Castro','JICR840310HDF','raul.jimenez@correo.com','9617890123','Morelos','78',NULL,'Los Laureles','Tuxtla Gutiérrez','Chiapas','29043','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Gloria Patricia','Jiménez','Rivera','JICG890525MDF','gloria.jimenez@correo.com','9617890124','Morelos','78',NULL,'Los Laureles','Tuxtla Gutiérrez','Chiapas','29043','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Mateo','Jiménez','Rivera','JICM140815HDF',NULL,NULL,'Morelos','78',NULL,'Los Laureles','Tuxtla Gutiérrez','Chiapas','29043','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 14 (San Cristóbal) ===
('Ricardo Daniel','Aguilar','Chávez','AICR760910HDF','ricardo.aguilar@correo.com','9679012345','Hidalgo','56',NULL,'La Merced','San Cristóbal de las Casas','Chiapas','29214','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Fernanda','Aguilar','Medina','AICF820315MDF','fer.aguilar@correo.com','9679012346','Hidalgo','56',NULL,'La Merced','San Cristóbal de las Casas','Chiapas','29214','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Valeria','Aguilar','Medina','AICV060910MDF',NULL,NULL,'Hidalgo','56',NULL,'La Merced','San Cristóbal de las Casas','Chiapas','29214','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Tomás','Aguilar','Medina','AICT100415HDF',NULL,NULL,'Hidalgo','56',NULL,'La Merced','San Cristóbal de las Casas','Chiapas','29214','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 15 (Tuxtla) ===
('Alejandro Esteban','Ortiz','Silva','OISA900520HDF','alejandro.ortiz@correo.com','9618901234','Ocampo','34',NULL,'Patria Nueva','Tuxtla Gutiérrez','Chiapas','29038','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Mariana','Ortiz','Bravo','OISM950815MDF','mariana.ortiz@correo.com','9618901235','Ocampo','34',NULL,'Patria Nueva','Tuxtla Gutiérrez','Chiapas','29038','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Victoria','Ortiz','Bravo','OISV180120MDF',NULL,NULL,'Ocampo','34',NULL,'Patria Nueva','Tuxtla Gutiérrez','Chiapas','29038','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 16 (San Cristóbal) ===
('Eduardo Francisco','Castillo','Luna','CALE720830HDF','eduardo.castillo@correo.com','9670123456','Allende','89',NULL,'Cerro de Guadalupe','San Cristóbal de las Casas','Chiapas','29215','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Lucía','Castillo','Ríos','CALU780420MDF','lucia.castillo@correo.com','9670123457','Allende','89',NULL,'Cerro de Guadalupe','San Cristóbal de las Casas','Chiapas','29215','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Emilia','Castillo','Ríos','CARE160615MDF',NULL,NULL,'Allende','89',NULL,'Cerro de Guadalupe','San Cristóbal de las Casas','Chiapas','29215','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Hugo','Castillo','Ríos','CARH200930HDF',NULL,NULL,'Allende','89',NULL,'Cerro de Guadalupe','San Cristóbal de las Casas','Chiapas','29215','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 17 (Tuxtla) ===
('Armando Luis','Medina','Vásquez','MEVA800110HDF','armando.medina@correo.com','9619012345','Aldama','67',NULL,'Lomas de Sayula','Tuxtla Gutiérrez','Chiapas','29033','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Claudia Daniela','Medina','Herrera','MEVC851230MDF','clau.medina@correo.com','9619012346','Aldama','67',NULL,'Lomas de Sayula','Tuxtla Gutiérrez','Chiapas','29033','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Natalia','Medina','Herrera','MEVN130520MDF',NULL,NULL,'Aldama','67',NULL,'Lomas de Sayula','Tuxtla Gutiérrez','Chiapas','29033','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 18 (San Cristóbal) ===
('Daniel Andrés','Bravo','Domínguez','BADD910615HDF','daniel.bravo@correo.com','9671234567','5 de Mayo','45',NULL,'Pedregal San Antonio','San Cristóbal de las Casas','Chiapas','29216','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Elena','Bravo','Gómez','BADB960210MDF','elena.bravo@correo.com','9671234568','5 de Mayo','45',NULL,'Pedregal San Antonio','San Cristóbal de las Casas','Chiapas','29216','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Paula','Bravo','Gómez','BADP080430MDF',NULL,NULL,'5 de Mayo','45',NULL,'Pedregal San Antonio','San Cristóbal de las Casas','Chiapas','29216','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Javier','Bravo','Gómez','BADJ120830HDF',NULL,NULL,'5 de Mayo','45',NULL,'Pedregal San Antonio','San Cristóbal de las Casas','Chiapas','29216','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 19 (Tuxtla) ===
('Carlos Alberto','Reyes','Morales','REMC750430HDF','carlos.reyes@correo.com','9610123456','Pino Suárez','23',NULL,'Moctezuma','Tuxtla Gutiérrez','Chiapas','29040','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Isabel Cristina','Reyes','Aguilar','REMI800525MDF','isa.reyes@correo.com','9610123457','Pino Suárez','23',NULL,'Moctezuma','Tuxtla Gutiérrez','Chiapas','29040','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Leonardo','Reyes','Aguilar','REML150210HDF',NULL,NULL,'Pino Suárez','23',NULL,'Moctezuma','Tuxtla Gutiérrez','Chiapas','29040','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 20 (San Cristóbal) ===
('Jorge Luis','Guerrero','Vargas','GUVJ780720HDF','jorge.guerrero@correo.com','9672345678','Nicolás Bravo','78',NULL,'Vista Hermosa','San Cristóbal de las Casas','Chiapas','29217','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Ana Karen','Guerrero','Sánchez','GUVA830910MDF','ana.guerrero@correo.com','9672345679','Nicolás Bravo','78',NULL,'Vista Hermosa','San Cristóbal de las Casas','Chiapas','29217','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('María','Guerrero','Sánchez','GUVM100630MDF',NULL,NULL,'Nicolás Bravo','78',NULL,'Vista Hermosa','San Cristóbal de las Casas','Chiapas','29217','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Diego','Guerrero','Sánchez','GUVD140415HDF',NULL,NULL,'Nicolás Bravo','78',NULL,'Vista Hermosa','San Cristóbal de las Casas','Chiapas','29217','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Individuales ===
('María Elena','Cruz','Torres','CRME850615MDF','maria.cruz@correo.com','9611112233','Revolución','12',NULL,'INFONAVIT','Tuxtla Gutiérrez','Chiapas','29050','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('José Antonio','Morales','Castillo','MOCJ700310HDF','jose.morales@correo.com','9673456789','Benito Juárez','34',NULL,'San Diego','San Cristóbal de las Casas','Chiapas','29218','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Patricia Isabel','Luna','Ríos','LURP920520MDF','paty.luna@correo.com','9612223344','Insurgentes','56',NULL,'Solidaridad','Tuxtla Gutiérrez','Chiapas','29046','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Luis Ángel','Gómez','Hernández','GOHL880910HDF','luis.gomez@correo.com','9674567890','Sor Juana Inés de la Cruz','89',NULL,'El Mirador','San Cristóbal de las Casas','Chiapas','29219','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Guadalupe','Martínez','Bravo','MABG790815MDF','lupita.martinez@correo.com','9613334455','Madero','78',NULL,'Cerrito Buena Vista','Tuxtla Gutiérrez','Chiapas','29039','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Fernando','Pérez','Ortiz','PEOF820615HDF','fernando.perez@correo.com','9675678901','Flavio A. Paniagua','12',NULL,'San Ramón','San Cristóbal de las Casas','Chiapas','29270','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Rosa María','Domínguez','Chávez','DOCR900310MDF','rosa.dominguez@correo.com','9614445566','Guatemala','90',NULL,'Bosque Sur','Tuxtla Gutiérrez','Chiapas','29041','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Javier Ignacio','Hernández','Reyes','HERJ770420HDF','javier.hernandez@correo.com','9676789012','Diego Dugelay','45',NULL,'Centro','San Cristóbal de las Casas','Chiapas','29200','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Laura Elena','Nuñez','Flores','NUFL810915MDF','laura.nunez@correo.com','9615556677','Nicaragua','34',NULL,'Albania Baja','Tuxtla Gutiérrez','Chiapas','29010','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Cecilia','Romero','Aguilar','ROAC880210MDF','ceci.romero@correo.com','9677890123','Hermanos Domínguez','67',NULL,'Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1'));


-- ============================================================
--  2. PÓLIZAS
-- ============================================================
INSERT INTO poliza (id_asegurado, id_producto, numero_poliza, fecha_inicio, fecha_vencimiento, estatus, prima_mensual)
VALUES
-- Familias
((SELECT id_asegurado FROM asegurado WHERE rfc='LOHJ750615HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-001', '2026-01-01', '2027-01-01', 'activa',    2220.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='VASM700825HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-002', '2026-02-01', '2027-02-01', 'activa',    2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='GACL850330HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-003', '2025-06-01', '2026-06-01', 'activa',    2250.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='TOFM680710HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-004', '2024-03-01', '2025-03-01', 'vencida',   2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='RAJC800120HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-005', '2026-03-01', '2027-03-01', 'activa',    2300.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='ROMJ760405HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-006', '2024-01-01', '2025-01-01', 'cancelada', 2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='GORP720310HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-007', '2025-12-01', '2026-12-01', 'activa',    2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='HEBF650820HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-008', '2026-04-01', '2027-04-01', 'activa',    2400.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='MAOM880615HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-009', '2023-05-01', '2024-05-01', 'vencida',   2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='SAGR740925HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-010', '2025-09-01', '2026-09-01', 'activa',    2150.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='FOND810720HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Vida Plus'),        'FAM-CHIS-011', '2026-01-15', '2027-01-15', 'activa',     650.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='RUMF770520HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-012', '2025-11-01', '2026-11-01', 'activa',    2200.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='JICR840310HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-013', '2024-06-01', '2025-06-01', 'cancelada', 2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='AICR760910HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-014', '2026-05-01', '2027-05-01', 'activa',    2350.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='OISA900520HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-015', '2024-08-01', '2025-08-01', 'vencida',   2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='CALE720830HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-016', '2025-10-01', '2026-10-01', 'activa',    2250.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='MEVA800110HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-017', '2026-06-01', '2027-06-01', 'activa',    2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='BADD910615HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-018', '2025-07-01', '2026-07-01', 'activa',    2300.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='REMC750430HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS-019', '2024-02-01', '2025-02-01', 'cancelada', 2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='GUVJ780720HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Vida Plus'),        'FAM-CHIS-020', '2026-03-15', '2027-03-15', 'activa',     650.00),
-- Individuales
((SELECT id_asegurado FROM asegurado WHERE rfc='CRME850615MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Vida Plus'),        'IND-CHIS-001', '2026-01-01', '2027-01-01', 'activa',     650.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='MOCJ700310HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Cuidándote'),       'IND-CHIS-002', '2024-04-01', '2025-04-01', 'vencida',   1200.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='LURP920520MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Básico Accidentes'), 'IND-CHIS-003', '2026-02-01', '2027-02-01', 'activa',     300.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='GOHL880910HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Vida Plus'),        'IND-CHIS-004', '2025-08-01', '2026-08-01', 'activa',     650.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='MABG790815MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Cuidándote'),       'IND-CHIS-005', '2024-01-01', '2025-01-01', 'cancelada', 1200.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='PEOF820615HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Básico Accidentes'), 'IND-CHIS-006', '2026-04-01', '2027-04-01', 'activa',     300.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='DOCR900310MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Vida Plus'),        'IND-CHIS-007', '2023-06-01', '2024-06-01', 'vencida',    650.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='HERJ770420HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Cuidándote'),       'IND-CHIS-008', '2025-10-01', '2026-10-01', 'activa',    1440.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='NUFL810915MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Básico Accidentes'), 'IND-CHIS-009', '2025-12-01', '2026-12-01', 'activa',     300.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='ROAC880210MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Vida Plus'),        'IND-CHIS-010', '2024-09-01', '2025-09-01', 'vencida',    650.00);


-- ============================================================
--  3. VINCULAR DEPENDIENTES A PÓLIZAS
-- ============================================================
-- Familia 1
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-001') WHERE rfc='LORM800320MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-001') WHERE rfc='LORD050410HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-001') WHERE rfc='LORF080612MDF';
-- Familia 2
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-002') WHERE rfc='VASR750910MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-002') WHERE rfc='VASA120315HDF';
-- Familia 3
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-003') WHERE rfc='GARC900115MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-003') WHERE rfc='GARD100520HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-003') WHERE rfc='GARV130430MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-003') WHERE rfc='GARM180615HDF';
-- Familia 4
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-004') WHERE rfc='TOFC720505MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-004') WHERE rfc='TOFL090830MDF';
-- Familia 5
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-005') WHERE rfc='RALA850930MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-005') WHERE rfc='RALS110715MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-005') WHERE rfc='RALE150310HDF';
-- Familia 6
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-006') WHERE rfc='RORG820720MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-006') WHERE rfc='RORM160120MDF';
-- Familia 7
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-007') WHERE rfc='GORV780525MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-007') WHERE rfc='GORA020830HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-007') WHERE rfc='GORN060115MDF';
-- Familia 8
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-008') WHERE rfc='HEBT700215MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-008') WHERE rfc='HEBR030930HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-008') WHERE rfc='HEBP070820MDF';
-- Familia 9
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-009') WHERE rfc='MAOL930405MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-009') WHERE rfc='MAOI170910MDF';
-- Familia 10
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-010') WHERE rfc='SAGM790830MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-010') WHERE rfc='SAGC080215HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-010') WHERE rfc='SAGD110430MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-010') WHERE rfc='SAGE150610MDF';
-- Familia 11
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-011') WHERE rfc='FONA860415MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-011') WHERE rfc='FONS120915HDF';
-- Familia 12
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-012') WHERE rfc='RUMD830110MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-012') WHERE rfc='RUMS040630HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-012') WHERE rfc='RUMC080115MDF';
-- Familia 13
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-013') WHERE rfc='JICG890525MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-013') WHERE rfc='JICM140815HDF';
-- Familia 14
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-014') WHERE rfc='AICF820315MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-014') WHERE rfc='AICV060910MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-014') WHERE rfc='AICT100415HDF';
-- Familia 15
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-015') WHERE rfc='OISM950815MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-015') WHERE rfc='OISV180120MDF';
-- Familia 16
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-016') WHERE rfc='CALU780420MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-016') WHERE rfc='CARE160615MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-016') WHERE rfc='CARH200930HDF';
-- Familia 17
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-017') WHERE rfc='MEVC851230MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-017') WHERE rfc='MEVN130520MDF';
-- Familia 18
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-018') WHERE rfc='BADB960210MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-018') WHERE rfc='BADP080430MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-018') WHERE rfc='BADJ120830HDF';
-- Familia 19
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-019') WHERE rfc='REMI800525MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-019') WHERE rfc='REML150210HDF';
-- Familia 20
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-020') WHERE rfc='GUVA830910MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-020') WHERE rfc='GUVM100630MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-020') WHERE rfc='GUVD140415HDF';


-- ============================================================
--  4. BENEFICIOS
-- ============================================================
-- 4a. Beneficios base incluidos para todas las pólizas nuevas
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
WHERE (p.numero_poliza LIKE 'FAM-CHIS-%' OR p.numero_poliza LIKE 'IND-CHIS-%')
  AND pb.activo = TRUE
  AND pb.deleted_at IS NULL
  AND pb.incluido_base = TRUE;

-- 4b. Odontología básica contratada (extra) en algunas familias
INSERT INTO beneficio (id_poliza, id_producto_beneficio, id_asegurado, costo_aplicado, vigente)
SELECT p.id_poliza, pb.id_producto_beneficio, NULL, pb.costo_extra, TRUE
FROM poliza p
JOIN producto_beneficio pb ON pb.id_producto = p.id_producto
WHERE p.numero_poliza IN ('FAM-CHIS-001','FAM-CHIS-005','FAM-CHIS-010','FAM-CHIS-014')
  AND pb.nombre_beneficio = 'Odontología básica'
  AND pb.activo = TRUE;

-- 4c. Beneficio Maternidad para cónyuges en algunas pólizas familiares
INSERT INTO beneficio (id_poliza, id_producto_beneficio, id_asegurado, costo_aplicado, vigente)
SELECT p.id_poliza, pb.id_producto_beneficio, a.id_asegurado,
    CASE WHEN pb.incluido_base THEN 0 ELSE COALESCE(pb.costo_extra, 0) END,
    TRUE
FROM poliza p
JOIN producto_beneficio pb ON pb.id_producto = p.id_producto
JOIN asegurado a ON a.rfc IN ('LORM800320MDF','VASR750910MDF','GARC900115MDF','RALA850930MDF','SAGM790830MDF')
WHERE p.numero_poliza IN ('FAM-CHIS-001','FAM-CHIS-002','FAM-CHIS-003','FAM-CHIS-005','FAM-CHIS-010')
  AND pb.nombre_beneficio = 'Maternidad'
  AND pb.activo = TRUE;


-- ============================================================
--  5. BENEFICIARIOS
-- ============================================================
INSERT INTO beneficiario (id_poliza, id_asegurado, nombre_completo, parentesco, porcentaje_participacion, telefono)
VALUES
-- FAM-CHIS-001
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-001'), (SELECT id_asegurado FROM asegurado WHERE rfc='LOHJ750615HDF'), 'María Guadalupe López Ruiz', 'Esposa', 100.0, '9611234568'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-001'), (SELECT id_asegurado FROM asegurado WHERE rfc='LORM800320MDF'), 'Jorge Alberto López Hernández', 'Esposo', 100.0, '9611234567'),
-- FAM-CHIS-002
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-002'), (SELECT id_asegurado FROM asegurado WHERE rfc='VASM700825HDF'), 'Rosa Elena Vásquez Morales', 'Esposa', 100.0, '9674567891'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-002'), (SELECT id_asegurado FROM asegurado WHERE rfc='VASR750910MDF'), 'Marco Antonio Vásquez Silva', 'Esposo', 100.0, '9674567890'),
-- FAM-CHIS-003
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-003'), (SELECT id_asegurado FROM asegurado WHERE rfc='GACL850330HDF'), 'Claudia Patricia García Reyes', 'Esposa', 100.0, '9612345679'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-003'), (SELECT id_asegurado FROM asegurado WHERE rfc='GARC900115MDF'), 'Luis Fernando García Cruz', 'Esposo', 100.0, '9612345678'),
-- FAM-CHIS-004
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-004'), (SELECT id_asegurado FROM asegurado WHERE rfc='TOFM680710HDF'), 'Carmen Alicia Torres Pérez', 'Esposa', 100.0, '9671122335'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-004'), (SELECT id_asegurado FROM asegurado WHERE rfc='TOFC720505MDF'), 'Miguel Ángel Torres Flores', 'Esposo', 100.0, '9671122334'),
-- FAM-CHIS-005
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-005'), (SELECT id_asegurado FROM asegurado WHERE rfc='RAJC800120HDF'), 'Ana Laura Ramírez Castillo', 'Esposa', 100.0, '9613456790'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-005'), (SELECT id_asegurado FROM asegurado WHERE rfc='RALA850930MDF'), 'Juan Carlos Ramírez Aguilar', 'Esposo', 100.0, '9613456789'),
-- FAM-CHIS-006
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-006'), (SELECT id_asegurado FROM asegurado WHERE rfc='ROMJ760405HDF'), 'Gabriela Rodríguez Sánchez', 'Esposa', 100.0, '9673344557'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-006'), (SELECT id_asegurado FROM asegurado WHERE rfc='RORG820720MDF'), 'José Luis Rodríguez Mendoza', 'Esposo', 100.0, '9673344556'),
-- FAM-CHIS-007
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-007'), (SELECT id_asegurado FROM asegurado WHERE rfc='GORP720310HDF'), 'Verónica Isabel González Luna', 'Esposa', 100.0, '9614567891'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-007'), (SELECT id_asegurado FROM asegurado WHERE rfc='GORV780525MDF'), 'Pedro Antonio González Ríos', 'Esposo', 100.0, '9614567890'),
-- FAM-CHIS-008
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-008'), (SELECT id_asegurado FROM asegurado WHERE rfc='HEBF650820HDF'), 'Teresa Dolores Hernández Vargas', 'Esposa', 100.0, '9675566779'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-008'), (SELECT id_asegurado FROM asegurado WHERE rfc='HEBT700215MDF'), 'Francisco Javier Hernández Bravo', 'Esposo', 100.0, '9675566778'),
-- FAM-CHIS-009
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-009'), (SELECT id_asegurado FROM asegurado WHERE rfc='MAOM880615HDF'), 'Leticia María Martínez Domínguez', 'Esposa', 100.0, '9615678902'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-009'), (SELECT id_asegurado FROM asegurado WHERE rfc='MAOL930405MDF'), 'Manuel Alejandro Martínez Ortiz', 'Esposo', 100.0, '9615678901'),
-- FAM-CHIS-010
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-010'), (SELECT id_asegurado FROM asegurado WHERE rfc='SAGR740925HDF'), 'Margarita Elena Sánchez Jiménez', 'Esposa', 100.0, '9677890124'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-010'), (SELECT id_asegurado FROM asegurado WHERE rfc='SAGM790830MDF'), 'Roberto Carlos Sánchez Guerrero', 'Esposo', 100.0, '9677890123'),
-- FAM-CHIS-011
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-011'), (SELECT id_asegurado FROM asegurado WHERE rfc='FOND810720HDF'), 'Alejandra Flores Camacho', 'Esposa', 100.0, '9616789013'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-011'), (SELECT id_asegurado FROM asegurado WHERE rfc='FONA860415MDF'), 'Diego Armando Flores Nuñez', 'Esposo', 100.0, '9616789012'),
-- FAM-CHIS-012
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-012'), (SELECT id_asegurado FROM asegurado WHERE rfc='RUMF770520HDF'), 'Diana Laura Ruiz Romero', 'Esposa', 100.0, '9678901235'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-012'), (SELECT id_asegurado FROM asegurado WHERE rfc='RUMD830110MDF'), 'Fernando José Ruiz Medina', 'Esposo', 100.0, '9678901234'),
-- FAM-CHIS-013
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-013'), (SELECT id_asegurado FROM asegurado WHERE rfc='JICR840310HDF'), 'Gloria Patricia Jiménez Rivera', 'Esposa', 100.0, '9617890124'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-013'), (SELECT id_asegurado FROM asegurado WHERE rfc='JICG890525MDF'), 'Raúl Eduardo Jiménez Castro', 'Esposo', 100.0, '9617890123'),
-- FAM-CHIS-014
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-014'), (SELECT id_asegurado FROM asegurado WHERE rfc='AICR760910HDF'), 'Fernanda Aguilar Medina', 'Esposa', 100.0, '9679012346'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-014'), (SELECT id_asegurado FROM asegurado WHERE rfc='AICF820315MDF'), 'Ricardo Daniel Aguilar Chávez', 'Esposo', 100.0, '9679012345'),
-- FAM-CHIS-015
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-015'), (SELECT id_asegurado FROM asegurado WHERE rfc='OISA900520HDF'), 'Mariana Ortiz Bravo', 'Esposa', 100.0, '9618901235'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-015'), (SELECT id_asegurado FROM asegurado WHERE rfc='OISM950815MDF'), 'Alejandro Esteban Ortiz Silva', 'Esposo', 100.0, '9618901234'),
-- FAM-CHIS-016
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-016'), (SELECT id_asegurado FROM asegurado WHERE rfc='CALE720830HDF'), 'Lucía Castillo Ríos', 'Esposa', 100.0, '9670123457'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-016'), (SELECT id_asegurado FROM asegurado WHERE rfc='CALU780420MDF'), 'Eduardo Francisco Castillo Luna', 'Esposo', 100.0, '9670123456'),
-- FAM-CHIS-017
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-017'), (SELECT id_asegurado FROM asegurado WHERE rfc='MEVA800110HDF'), 'Claudia Daniela Medina Herrera', 'Esposa', 100.0, '9619012346'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-017'), (SELECT id_asegurado FROM asegurado WHERE rfc='MEVC851230MDF'), 'Armando Luis Medina Vásquez', 'Esposo', 100.0, '9619012345'),
-- FAM-CHIS-018
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-018'), (SELECT id_asegurado FROM asegurado WHERE rfc='BADD910615HDF'), 'Elena Bravo Gómez', 'Esposa', 100.0, '9671234568'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-018'), (SELECT id_asegurado FROM asegurado WHERE rfc='BADB960210MDF'), 'Daniel Andrés Bravo Domínguez', 'Esposo', 100.0, '9671234567'),
-- FAM-CHIS-019
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-019'), (SELECT id_asegurado FROM asegurado WHERE rfc='REMC750430HDF'), 'Isabel Cristina Reyes Aguilar', 'Esposa', 100.0, '9610123457'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-019'), (SELECT id_asegurado FROM asegurado WHERE rfc='REMI800525MDF'), 'Carlos Alberto Reyes Morales', 'Esposo', 100.0, '9610123456'),
-- FAM-CHIS-020
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-020'), (SELECT id_asegurado FROM asegurado WHERE rfc='GUVJ780720HDF'), 'Ana Karen Guerrero Sánchez', 'Esposa', 100.0, '9672345679'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS-020'), (SELECT id_asegurado FROM asegurado WHERE rfc='GUVA830910MDF'), 'Jorge Luis Guerrero Vargas', 'Esposo', 100.0, '9672345678'),
-- IND-CHIS-001
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS-001'), (SELECT id_asegurado FROM asegurado WHERE rfc='CRME850615MDF'), 'José Cruz Torres', 'Padre', 100.0, NULL),
-- IND-CHIS-002
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS-002'), (SELECT id_asegurado FROM asegurado WHERE rfc='MOCJ700310HDF'), 'María Morales Castillo', 'Madre', 100.0, NULL),
-- IND-CHIS-003
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS-003'), (SELECT id_asegurado FROM asegurado WHERE rfc='LURP920520MDF'), 'Ricardo Luna Ríos', 'Padre', 100.0, NULL),
-- IND-CHIS-004
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS-004'), (SELECT id_asegurado FROM asegurado WHERE rfc='GOHL880910HDF'), 'María Gómez Hernández', 'Madre', 100.0, NULL),
-- IND-CHIS-005
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS-005'), (SELECT id_asegurado FROM asegurado WHERE rfc='MABG790815MDF'), 'José Martínez Bravo', 'Padre', 100.0, NULL),
-- IND-CHIS-006
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS-006'), (SELECT id_asegurado FROM asegurado WHERE rfc='PEOF820615HDF'), 'Laura Pérez Ortiz', 'Madre', 100.0, NULL),
-- IND-CHIS-007
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS-007'), (SELECT id_asegurado FROM asegurado WHERE rfc='DOCR900310MDF'), 'Francisco Domínguez Chávez', 'Padre', 100.0, NULL),
-- IND-CHIS-008
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS-008'), (SELECT id_asegurado FROM asegurado WHERE rfc='HERJ770420HDF'), 'Carmen Hernández Reyes', 'Madre', 100.0, NULL),
-- IND-CHIS-009
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS-009'), (SELECT id_asegurado FROM asegurado WHERE rfc='NUFL810915MDF'), 'Roberto Nuñez Flores', 'Padre', 100.0, NULL),
-- IND-CHIS-010
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS-010'), (SELECT id_asegurado FROM asegurado WHERE rfc='ROAC880210MDF'), 'Antonio Romero Aguilar', 'Padre', 100.0, NULL);


-- ============================================================
--  6. SEGUIMIENTOS
-- ============================================================
INSERT INTO seguimiento (folio, id_asegurado, id_agente, asunto)
VALUES
('SEG-CHIS-2025-001', (SELECT id_asegurado FROM asegurado WHERE rfc='LOHJ750615HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Contratación de Plan Familiar'),
('SEG-CHIS-2025-002', (SELECT id_asegurado FROM asegurado WHERE rfc='VASM700825HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Revisión anual de cobertura'),
('SEG-CHIS-2025-003', (SELECT id_asegurado FROM asegurado WHERE rfc='GACL850330HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Cambio de domicilio registrado'),
('SEG-CHIS-2025-004', (SELECT id_asegurado FROM asegurado WHERE rfc='TOFM680710HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Renovación pendiente de póliza'),
('SEG-CHIS-2025-005', (SELECT id_asegurado FROM asegurado WHERE rfc='RAJC800120HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Alta nueva familiar completada'),
('SEG-CHIS-2025-006', (SELECT id_asegurado FROM asegurado WHERE rfc='ROMJ760405HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Solicitud de cancelación de póliza'),
('SEG-CHIS-2025-007', (SELECT id_asegurado FROM asegurado WHERE rfc='GORP720310HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Ajuste de prima mensual'),
('SEG-CHIS-2025-008', (SELECT id_asegurado FROM asegurado WHERE rfc='HEBF650820HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Contratación Plan Familiar Plus'),
('SEG-CHIS-2025-009', (SELECT id_asegurado FROM asegurado WHERE rfc='MAOM880615HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Revisión de siniestro reportado'),
('SEG-CHIS-2025-010', (SELECT id_asegurado FROM asegurado WHERE rfc='SAGR740925HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Actualización de beneficiarios'),
('SEG-CHIS-2025-011', (SELECT id_asegurado FROM asegurado WHERE rfc='FOND810720HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Contratación Vida Plus familiar'),
('SEG-CHIS-2025-012', (SELECT id_asegurado FROM asegurado WHERE rfc='RUMF770520HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Renovación automática de póliza'),
('SEG-CHIS-2025-013', (SELECT id_asegurado FROM asegurado WHERE rfc='JICR840310HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Cancelación por falta de pago'),
('SEG-CHIS-2025-014', (SELECT id_asegurado FROM asegurado WHERE rfc='AICR760910HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Contratación con cobertura extendida'),
('SEG-CHIS-2025-015', (SELECT id_asegurado FROM asegurado WHERE rfc='OISA900520HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Renovación vencida Plan Familiar'),
('SEG-CHIS-2025-016', (SELECT id_asegurado FROM asegurado WHERE rfc='CALE720830HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Cambio de agente responsable'),
('SEG-CHIS-2025-017', (SELECT id_asegurado FROM asegurado WHERE rfc='MEVA800110HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Ajuste de cobertura dental'),
('SEG-CHIS-2025-018', (SELECT id_asegurado FROM asegurado WHERE rfc='BADD910615HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Revisión médica programada'),
('SEG-CHIS-2025-019', (SELECT id_asegurado FROM asegurado WHERE rfc='REMC750430HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Cancelación a petición del cliente'),
('SEG-CHIS-2025-020', (SELECT id_asegurado FROM asegurado WHERE rfc='GUVJ780720HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Contratación Vida Plus familiar'),
('SEG-CHIS-2025-021', (SELECT id_asegurado FROM asegurado WHERE rfc='CRME850615MDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Contratación Vida Plus individual'),
('SEG-CHIS-2025-022', (SELECT id_asegurado FROM asegurado WHERE rfc='MOCJ700310HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Renovación Cuidándote'),
('SEG-CHIS-2025-023', (SELECT id_asegurado FROM asegurado WHERE rfc='LURP920520MDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Contratación Básico Accidentes'),
('SEG-CHIS-2025-024', (SELECT id_asegurado FROM asegurado WHERE rfc='GOHL880910HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Ajuste de suma asegurada'),
('SEG-CHIS-2025-025', (SELECT id_asegurado FROM asegurado WHERE rfc='MABG790815MDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Cancelación Cuidándote'),
('SEG-CHIS-2025-026', (SELECT id_asegurado FROM asegurado WHERE rfc='PEOF820615HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Alta Básico Accidentes'),
('SEG-CHIS-2025-027', (SELECT id_asegurado FROM asegurado WHERE rfc='DOCR900310MDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Renovación vencida Vida Plus'),
('SEG-CHIS-2025-028', (SELECT id_asegurado FROM asegurado WHERE rfc='HERJ770420HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Contratación Cuidándote Plus'),
('SEG-CHIS-2025-029', (SELECT id_asegurado FROM asegurado WHERE rfc='NUFL810915MDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Renovación Básico Accidentes'),
('SEG-CHIS-2025-030', (SELECT id_asegurado FROM asegurado WHERE rfc='ROAC880210MDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Revisión de póliza vencida');


-- ============================================================
--  7. SEGUIMIENTO_CONTACTO
-- ============================================================
INSERT INTO seguimiento_contacto (id_seguimiento, iniciado_por, tipo_contacto, observaciones, resultado, fecha_hora)
VALUES
-- SEG-CHIS-2025-001 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-001'), 'agente', 'llamada', 'El cliente confirmó los datos de su familia y aceptó la prima mensual de $2,220.', 'resuelto', '2025-01-10 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-001'), 'asegurado', 'mensaje', 'Solicitó copia de la póliza en PDF por correo electrónico.', 'pendiente', '2025-01-12 14:30:00'),
-- SEG-CHIS-2025-002 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-002'), 'agente', 'llamada', 'Se revisó la cobertura anual y se propuso ajuste sin costo adicional.', 'resuelto', '2025-02-15 11:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-002'), 'asegurado', 'llamada', 'Confirmó que desea mantener la cobertura actual.', 'resuelto', '2025-02-16 09:30:00'),
-- SEG-CHIS-2025-003 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-003'), 'agente', 'visita', 'Visita domiciliaria para actualizar datos de dirección en Terán.', 'resuelto', '2025-06-20 16:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-003'), 'agente', 'mensaje', 'Se envió confirmación de cambio de domicilio por WhatsApp.', 'pendiente', '2025-06-21 10:00:00'),
-- SEG-CHIS-2025-004 (1 contacto)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-004'), 'agente', 'llamada', 'Se notificó al cliente sobre la renovación vencida de su póliza.', 'sin_respuesta', '2025-04-10 13:00:00'),
-- SEG-CHIS-2025-005 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-005'), 'agente', 'llamada', 'Alta de nueva póliza familiar con cobertura completa.', 'resuelto', '2025-03-05 10:30:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-005'), 'asegurado', 'mensaje', 'Envió copia de identificaciones de los hijos.', 'resuelto', '2025-03-06 11:00:00'),
-- SEG-CHIS-2025-006 (1 contacto)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-006'), 'asegurado', 'visita', 'El cliente acudió a oficina a solicitar cancelación por mudanza.', 'resuelto', '2025-01-20 15:00:00'),
-- SEG-CHIS-2025-007 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-007'), 'agente', 'llamada', 'Se acordó ajuste de prima por cambio en edad de los dependientes.', 'resuelto', '2025-12-01 09:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-007'), 'asegurado', 'llamada', 'Cliente aceptó el nuevo monto de prima mensual.', 'resuelto', '2025-12-02 10:00:00'),
-- SEG-CHIS-2025-008 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-008'), 'agente', 'visita', 'Presentación de Plan Familiar Plus con cobertura extendida.', 'resuelto', '2025-04-15 14:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-008'), 'asegurado', 'mensaje', 'Confirmó contratación vía mensaje de texto.', 'pendiente', '2025-04-16 08:00:00'),
-- SEG-CHIS-2025-009 (1 contacto)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-009'), 'agente', 'llamada', 'Se registró siniestro menor y se coordinó cita médica.', 'sin_respuesta', '2025-05-22 11:30:00'),
-- SEG-CHIS-2025-010 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-010'), 'agente', 'llamada', 'Actualización de lista de beneficiarios de la póliza.', 'resuelto', '2025-09-10 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-010'), 'asegurado', 'mensaje', 'Envió documentos de identificación de nuevos beneficiarios.', 'pendiente', '2025-09-11 16:00:00'),
-- SEG-CHIS-2025-011 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-011'), 'agente', 'llamada', 'Contratación de Vida Plus con doble indemnización.', 'resuelto', '2025-01-18 09:30:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-011'), 'asegurado', 'llamada', 'Consultó sobre cobertura por invalidez total.', 'resuelto', '2025-01-19 11:00:00'),
-- SEG-CHIS-2025-012 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-012'), 'agente', 'llamada', 'Renovación automática procesada exitosamente.', 'resuelto', '2025-11-05 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-012'), 'asegurado', 'mensaje', 'Agradeció el recordatorio de renovación.', 'resuelto', '2025-11-06 09:00:00'),
-- SEG-CHIS-2025-013 (1 contacto)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-013'), 'agente', 'llamada', 'Se notificó cancelación por falta de pago de 3 mensualidades.', 'resuelto', '2025-07-15 13:00:00'),
-- SEG-CHIS-2025-014 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-014'), 'agente', 'visita', 'Visita domiciliaria para firmar anexo de cobertura extendida.', 'resuelto', '2025-05-20 15:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-014'), 'asegurado', 'llamada', 'Confirmó que recibió el anexo firmado.', 'resuelto', '2025-05-21 10:30:00'),
-- SEG-CHIS-2025-015 (1 contacto)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-015'), 'agente', 'llamada', 'Se envió recordatorio de renovación vencida sin respuesta.', 'sin_respuesta', '2025-09-01 11:00:00'),
-- SEG-CHIS-2025-016 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-016'), 'agente', 'llamada', 'Cambio de agente responsable aprobado por administración.', 'resuelto', '2025-10-12 09:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-016'), 'asegurado', 'mensaje', 'Cliente solicitó información del nuevo agente asignado.', 'pendiente', '2025-10-13 14:00:00'),
-- SEG-CHIS-2025-017 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-017'), 'agente', 'llamada', 'Se ofreció cobertura dental adicional con descuento.', 'resuelto', '2025-08-01 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-017'), 'asegurado', 'llamada', 'Aceptó agregar odontología básica a la póliza.', 'resuelto', '2025-08-02 11:30:00'),
-- SEG-CHIS-2025-018 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-018'), 'agente', 'visita', 'Revisión médica programada en clínica afiliada de San Cristóbal.', 'resuelto', '2025-07-10 08:30:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-018'), 'asegurado', 'mensaje', 'Confirmó asistencia a la cita médica programada.', 'pendiente', '2025-07-11 09:00:00'),
-- SEG-CHIS-2025-019 (1 contacto)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-019'), 'asegurado', 'visita', 'Cliente acudió a oficina a solicitar cancelación formal de la póliza.', 'resuelto', '2025-03-15 16:00:00'),
-- SEG-CHIS-2025-020 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-020'), 'agente', 'llamada', 'Contratación de Vida Plus para titular y cónyuge.', 'resuelto', '2025-03-20 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-020'), 'asegurado', 'llamada', 'Consultó términos de doble indemnización por accidente.', 'resuelto', '2025-03-21 09:30:00'),
-- SEG-CHIS-2025-021 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-021'), 'agente', 'llamada', 'Contratación de Vida Plus individual con prima anual.', 'resuelto', '2025-01-05 11:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-021'), 'asegurado', 'mensaje', 'Solicitó cambio a pago mensual en lugar de anual.', 'pendiente', '2025-01-06 10:00:00'),
-- SEG-CHIS-2025-022 (1 contacto)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-022'), 'agente', 'llamada', 'Recordatorio de renovación de póliza Cuidándote vencida.', 'sin_respuesta', '2025-05-01 13:00:00'),
-- SEG-CHIS-2025-023 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-023'), 'agente', 'llamada', 'Alta de póliza Básico Accidentes para trabajador independiente.', 'resuelto', '2025-02-10 10:30:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-023'), 'asegurado', 'llamada', 'Preguntó sobre cobertura en actividades recreativas.', 'resuelto', '2025-02-11 09:00:00'),
-- SEG-CHIS-2025-024 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-024'), 'agente', 'llamada', 'Se ajustó suma asegurada por cambio de estado civil.', 'resuelto', '2025-08-20 14:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-024'), 'asegurado', 'mensaje', 'Confirmó que actualizó sus datos en el portal.', 'pendiente', '2025-08-21 11:00:00'),
-- SEG-CHIS-2025-025 (1 contacto)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-025'), 'asegurado', 'visita', 'Cliente solicitó cancelación de Cuidándote por cambio de empleo.', 'resuelto', '2025-02-05 15:00:00'),
-- SEG-CHIS-2025-026 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-026'), 'agente', 'llamada', 'Contratación de Básico Accidentes como complemento.', 'resuelto', '2025-04-01 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-026'), 'asegurado', 'llamada', 'Consultó sobre red de hospitales en Tuxtla Gutiérrez.', 'resuelto', '2025-04-02 09:30:00'),
-- SEG-CHIS-2025-027 (1 contacto)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-027'), 'agente', 'llamada', 'Se intentó renovación de Vida Plus vencida sin éxito.', 'sin_respuesta', '2025-07-01 11:00:00'),
-- SEG-CHIS-2025-028 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-028'), 'agente', 'llamada', 'Contratación de Cuidándote Plus con cobertura nacional.', 'resuelto', '2025-09-15 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-028'), 'asegurado', 'mensaje', 'Solicitó lista de hospitales afiliados en Chiapas.', 'pendiente', '2025-09-16 14:00:00'),
-- SEG-CHIS-2025-029 (2 contactos)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-029'), 'agente', 'llamada', 'Renovación anual de Básico Accidentes aprobada.', 'resuelto', '2025-12-10 09:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-029'), 'asegurado', 'llamada', 'Confirmó que desea mantener la póliza activa.', 'resuelto', '2025-12-11 10:00:00'),
-- SEG-CHIS-2025-030 (1 contacto)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS-2025-030'), 'agente', 'llamada', 'Revisión de póliza vencida; cliente no desea renovar.', 'resuelto', '2025-10-01 13:00:00');
