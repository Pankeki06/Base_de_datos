-- ============================================================
--  DATOS DE MUESTRA ADICIONALES: Asegurados de Chiapas (Batch 2)
--  Ciudades: Tuxtla Gutiérrez y San Cristóbal de las Casas
-- ============================================================
USE aseguradora;

-- ============================================================
--  1. ASEGURADOS (Batch 2)
--     20 familias + 15 individuales
-- ============================================================
INSERT INTO asegurado (
    nombre, apellido_paterno, apellido_materno, rfc, correo, celular,
    calle, numero_exterior, numero_interior, colonia, municipio, estado,
    codigo_postal, tipo_asegurado, id_poliza, id_agente_responsable
) VALUES

-- === Familia 21 (Tuxtla) ===
('Arturo','Espinoza','Mendoza','ESMA740315HDF','arturo.espinoza@correo.com','9612341122','Av. Central Ote.','450',NULL,'El Mirador','Tuxtla Gutiérrez','Chiapas','29030','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Cecilia','Espinoza','Nájera','ESNC801020MDF','ceci.espinoza@correo.com','9612341123','Av. Central Ote.','450',NULL,'El Mirador','Tuxtla Gutiérrez','Chiapas','29030','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Renata','Espinoza','Nájera','ESNR150630MDF',NULL,NULL,'Av. Central Ote.','450',NULL,'El Mirador','Tuxtla Gutiérrez','Chiapas','29030','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Tomás','Espinoza','Nájera','ESNT190415HDF',NULL,NULL,'Av. Central Ote.','450',NULL,'El Mirador','Tuxtla Gutiérrez','Chiapas','29030','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 22 (San Cristóbal) ===
('Santiago','Herrera','Villanueva','HEVS690910HDF','santi.herrera@correo.com','9671122334','Crescencio Rosas','12','B','La Garita','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Mariana','Herrera','Luna','HELM750615MDF','mariana.herrera@correo.com','9671122335','Crescencio Rosas','12','B','La Garita','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Emilio','Herrera','Luna','HELE100820HDF',NULL,NULL,'Crescencio Rosas','12','B','La Garita','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Sofía','Herrera','Luna','HELS140130MDF',NULL,NULL,'Crescencio Rosas','12','B','La Garita','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 23 (Tuxtla) ===
('César Augusto','Camacho','Bravo','CABC820430HDF','cesar.camacho@correo.com','9613452233','9a. Sur','88',NULL,'Potinaspak','Tuxtla Gutiérrez','Chiapas','29040','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Paulina','Camacho','Domínguez','CAPD880520MDF','paulina.camacho@correo.com','9613452234','9a. Sur','88',NULL,'Potinaspak','Tuxtla Gutiérrez','Chiapas','29040','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Bruno','Camacho','Domínguez','CABD130910HDF',NULL,NULL,'9a. Sur','88',NULL,'Potinaspak','Tuxtla Gutiérrez','Chiapas','29040','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 24 (San Cristóbal) ===
('Germán','Pacheco','Ríos','PARG770810HDF','german.pacheco@correo.com','6672233445','Belisario Domínguez','56',NULL,'Barrio de Mexicanos','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Diana','Pacheco','Sosa','PADS830415MDF','diana.pacheco@correo.com','6672233446','Belisario Domínguez','56',NULL,'Barrio de Mexicanos','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Luciana','Pacheco','Sosa','PALU090630MDF',NULL,NULL,'Belisario Domínguez','56',NULL,'Barrio de Mexicanos','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Martín','Pacheco','Sosa','PAMS130815HDF',NULL,NULL,'Belisario Domínguez','56',NULL,'Barrio de Mexicanos','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 25 (Tuxtla) ===
('Héctor Hugo','Luna','Mendoza','LUMH790220HDF','hector.luna@correo.com','9614563344','2a. Poniente','34',NULL,'Plan de Ayala','Tuxtla Gutiérrez','Chiapas','29020','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Ivonne','Luna','Cruz','LUIC851115MDF','ivonne.luna@correo.com','9614563345','2a. Poniente','34',NULL,'Plan de Ayala','Tuxtla Gutiérrez','Chiapas','29020','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Hugo','Luna','Cruz','LUHC170930HDF',NULL,NULL,'2a. Poniente','34',NULL,'Plan de Ayala','Tuxtla Gutiérrez','Chiapas','29020','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Camila','Luna','Cruz','LUCC210415MDF',NULL,NULL,'2a. Poniente','34',NULL,'Plan de Ayala','Tuxtla Gutiérrez','Chiapas','29020','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 26 (San Cristóbal) ===
('Óscar','Domínguez','Pérez','DOPO750930HDF','oscar.dominguez@correo.com','6673344556','Sebastián Borrego','78',NULL,'Barrio El Cerrillo','San Cristóbal de las Casas','Chiapas','29220','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Erika','Domínguez','Herrera','DOHE810220MDF','erika.dominguez@correo.com','6673344557','Sebastián Borrego','78',NULL,'Barrio El Cerrillo','San Cristóbal de las Casas','Chiapas','29220','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Andrea','Domínguez','Herrera','DOHA150630MDF',NULL,NULL,'Sebastián Borrego','78',NULL,'Barrio El Cerrillo','San Cristóbal de las Casas','Chiapas','29220','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 27 (Tuxtla) ===
('Ignacio','Ríos','Vázquez','RIVI880615HDF','ignacio.rios@correo.com','9615674455','14 de Septiembre','120',NULL,'Lomas de Sayula','Tuxtla Gutiérrez','Chiapas','29033','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Daniela','Ríos','Aguilar','RIDA930930MDF','dani.rios@correo.com','9615674456','14 de Septiembre','120',NULL,'Lomas de Sayula','Tuxtla Gutiérrez','Chiapas','29033','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Marco','Ríos','Aguilar','RIMA180210HDF',NULL,NULL,'14 de Septiembre','120',NULL,'Lomas de Sayula','Tuxtla Gutiérrez','Chiapas','29033','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 28 (San Cristóbal) ===
('Julián','Cruz','Mendoza','CUMJ730515HDF','julian.cruz@correo.com','6674455667','Cristóbal Colón','45',NULL,'Barrio Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Nancy','Cruz','Ramírez','CURN791020MDF','nancy.cruz@correo.com','6674455668','Cristóbal Colón','45',NULL,'Barrio Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Jorge','Cruz','Ramírez','CURJ140315HDF',NULL,NULL,'Cristóbal Colón','45',NULL,'Barrio Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Valeria','Cruz','Ramírez','CURV180710MDF',NULL,NULL,'Cristóbal Colón','45',NULL,'Barrio Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 29 (Tuxtla) ===
('Esteban','Soto','Lara','SOLE800330HDF','esteban.soto@correo.com','9616785566','Central Poniente','340',NULL,'Centro','Tuxtla Gutiérrez','Chiapas','29000','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Fernanda','Soto','Meza','SOFM860425MDF','fer.soto@correo.com','9616785567','Central Poniente','340',NULL,'Centro','Tuxtla Gutiérrez','Chiapas','29000','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Lucas','Soto','Meza','SOLM120915HDF',NULL,NULL,'Central Poniente','340',NULL,'Centro','Tuxtla Gutiérrez','Chiapas','29000','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Paula','Soto','Meza','SOPM160115MDF',NULL,NULL,'Central Poniente','340',NULL,'Centro','Tuxtla Gutiérrez','Chiapas','29000','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 30 (San Cristóbal) ===
('Adrián','Molina','Bravo','MOBA820710HDF','adrian.molina@correo.com','6675566778','Dr. José Castellanos','23',NULL,'Barrio de La Merced','San Cristóbal de las Casas','Chiapas','29214','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Lorena','Molina','Castro','MOLC880310MDF','lorena.molina@correo.com','6675566779','Dr. José Castellanos','23',NULL,'Barrio de La Merced','San Cristóbal de las Casas','Chiapas','29214','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Diana','Molina','Castro','MODC140520MDF',NULL,NULL,'Dr. José Castellanos','23',NULL,'Barrio de La Merced','San Cristóbal de las Casas','Chiapas','29214','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 31 (Tuxtla) ===
('Víctor Manuel','Ortega','Silva','OVSO760420HDF','victor.ortega@correo.com','9617896677','Calzada al Sumidero','560',NULL,'Albania Baja','Tuxtla Gutiérrez','Chiapas','29010','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Patricia','Ortega','Nava','OVPN820815MDF','paty.ortega@correo.com','9617896678','Calzada al Sumidero','560',NULL,'Albania Baja','Tuxtla Gutiérrez','Chiapas','29010','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Emiliano','Ortega','Nava','OVEN110930HDF',NULL,NULL,'Calzada al Sumidero','560',NULL,'Albania Baja','Tuxtla Gutiérrez','Chiapas','29010','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 32 (San Cristóbal) ===
('Rafael','Gutiérrez','Mendoza','GUMR710815HDF','rafa.gutierrez@correo.com','6676677889','16 de Septiembre','89',NULL,'Barrio San Diego','San Cristóbal de las Casas','Chiapas','29218','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Alejandra','Gutiérrez','Ríos','GUAR780215MDF','ale.gutierrez@correo.com','6676677890','16 de Septiembre','89',NULL,'Barrio San Diego','San Cristóbal de las Casas','Chiapas','29218','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Mateo','Gutiérrez','Ríos','GUMR130410HDF',NULL,NULL,'16 de Septiembre','89',NULL,'Barrio San Diego','San Cristóbal de las Casas','Chiapas','29218','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Natalia','Gutiérrez','Ríos','GUNR170615MDF',NULL,NULL,'16 de Septiembre','89',NULL,'Barrio San Diego','San Cristóbal de las Casas','Chiapas','29218','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 33 (Tuxtla) ===
('Rodrigo','Velasco','Hernández','VEHR850520HDF','rodrigo.velasco@correo.com','9618907788','5 de Febrero','67',NULL,'Patria Nueva','Tuxtla Gutiérrez','Chiapas','29038','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Silvia','Velasco','Bravo','VESB910715MDF','silvia.velasco@correo.com','9618907789','5 de Febrero','67',NULL,'Patria Nueva','Tuxtla Gutiérrez','Chiapas','29038','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Olivia','Velasco','Bravo','VEOB180820MDF',NULL,NULL,'5 de Febrero','67',NULL,'Patria Nueva','Tuxtla Gutiérrez','Chiapas','29038','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 34 (San Cristóbal) ===
('Gerardo','Peña','Ortiz','PEOG780930HDF','gerardo.pena@correo.com','6677788990','Ejército Nacional','34',NULL,'Barrio El Mirador','San Cristóbal de las Casas','Chiapas','29219','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Karla','Peña','Sánchez','PEKS840430MDF','karla.pena@correo.com','6677788991','Ejército Nacional','34',NULL,'Barrio El Mirador','San Cristóbal de las Casas','Chiapas','29219','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Maximiliano','Peña','Sánchez','PEMS120630HDF',NULL,NULL,'Ejército Nacional','34',NULL,'Barrio El Mirador','San Cristóbal de las Casas','Chiapas','29219','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 35 (Tuxtla) ===
('Samuel','Aguilar','Cruz','AGCS810115HDF','samuel.aguilar@correo.com','9619018899','6a. Norte','78',NULL,'El Retiro','Tuxtla Gutiérrez','Chiapas','29043','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Tania','Aguilar','Méndez','AGMT870930MDF','tania.aguilar@correo.com','9619018900','6a. Norte','78',NULL,'El Retiro','Tuxtla Gutiérrez','Chiapas','29043','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Ian','Aguilar','Méndez','AGIM160310HDF',NULL,NULL,'6a. Norte','78',NULL,'El Retiro','Tuxtla Gutiérrez','Chiapas','29043','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Regina','Aguilar','Méndez','AGMR200520MDF',NULL,NULL,'6a. Norte','78',NULL,'El Retiro','Tuxtla Gutiérrez','Chiapas','29043','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 36 (San Cristóbal) ===
('Bruno','Salazar','Gómez','SAGB830520HDF','bruno.salazar@correo.com','6678899001','Ignacio Allende','12',NULL,'Barrio Santa Lucía','San Cristóbal de las Casas','Chiapas','29250','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Carolina','Salazar','Flores','SACF891020MDF','caro.salazar@correo.com','6678899002','Ignacio Allende','12',NULL,'Barrio Santa Lucía','San Cristóbal de las Casas','Chiapas','29250','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Elena','Salazar','Flores','SAEF150715MDF',NULL,NULL,'Ignacio Allende','12',NULL,'Barrio Santa Lucía','San Cristóbal de las Casas','Chiapas','29250','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 37 (Tuxtla) ===
('Francisco','Navarro','Reyes','NARF770330HDF','francisco.navarro@correo.com','9610129900','3a. Oriente Sur','145',NULL,'Solidaridad','Tuxtla Gutiérrez','Chiapas','29046','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Daniela','Navarro','Luna','NADL830615MDF','dani.navarro@correo.com','9610129901','3a. Oriente Sur','145',NULL,'Solidaridad','Tuxtla Gutiérrez','Chiapas','29046','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Leonardo','Navarro','Luna','NALL190415HDF',NULL,NULL,'3a. Oriente Sur','145',NULL,'Solidaridad','Tuxtla Gutiérrez','Chiapas','29046','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 38 (San Cristóbal) ===
('Tomás','Ibarra','Castro','IBCT800410HDF','tomas.ibarra@correo.com','6679900112','Margarita Maza de Juárez','56',NULL,'Barrio El Cerrillo','San Cristóbal de las Casas','Chiapas','29220','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Susana','Ibarra','Vega','IBVS860820MDF','susana.ibarra@correo.com','6679900113','Margarita Maza de Juárez','56',NULL,'Barrio El Cerrillo','San Cristóbal de las Casas','Chiapas','29220','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Ángel','Ibarra','Vega','IBVA140230HDF',NULL,NULL,'Margarita Maza de Juárez','56',NULL,'Barrio El Cerrillo','San Cristóbal de las Casas','Chiapas','29220','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Mariana','Ibarra','Vega','IBVM180910MDF',NULL,NULL,'Margarita Maza de Juárez','56',NULL,'Barrio El Cerrillo','San Cristóbal de las Casas','Chiapas','29220','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),

-- === Familia 39 (Tuxtla) ===
('Cristian','Fuentes','Mora','FUMC880630HDF','cristian.fuentes@correo.com','9611230011','Libertad','23',NULL,'Bosque Sur','Tuxtla Gutiérrez','Chiapas','29041','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Elena','Fuentes','Soto','FUES940215MDF','elena.fuentes@correo.com','9611230012','Libertad','23',NULL,'Bosque Sur','Tuxtla Gutiérrez','Chiapas','29041','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Dante','Fuentes','Soto','FUDS180410HDF',NULL,NULL,'Libertad','23',NULL,'Bosque Sur','Tuxtla Gutiérrez','Chiapas','29041','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Familia 40 (San Cristóbal) ===
('Mauricio','Delgado','Ríos','DERM750815HDF','mauricio.delgado@correo.com','6670011223','Santos Degollado','78',NULL,'Barrio de Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Renata','Delgado','Hernández','DERH810430MDF','renata.delgado@correo.com','6670011224','Santos Degollado','78',NULL,'Barrio de Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Lucía','Delgado','Hernández','DELU160630MDF',NULL,NULL,'Santos Degollado','78',NULL,'Barrio de Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Sebastián','Delgado','Hernández','DESH200915HDF',NULL,NULL,'Santos Degollado','78',NULL,'Barrio de Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),

-- === Individuales (Batch 2) ===
('Mónica','Reyes','Soto','RESM900415MDF','monica.reyes@correo.com','9612345566','Benito Juárez','89',NULL,'INFONAVIT','Tuxtla Gutiérrez','Chiapas','29050','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Ernesto','Lara','Bravo','LABE780930HDF','ernesto.lara@correo.com','6673456677','Efraín A. Gutiérrez','45',NULL,'Barrio El Cerrillo','San Cristóbal de las Casas','Chiapas','29220','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Nancy','Castro','Méndez','CAMN850520MDF','nancy.castro@correo.com','9614567788','Norte 3','120',NULL,'Las Granjas','Tuxtla Gutiérrez','Chiapas','29047','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Orlando','Silva','Vargas','SIVO820710HDF','orlando.silva@correo.com','6675678899','Fray Bartolomé de las Casas','34',NULL,'Barrio San Ramón','San Cristóbal de las Casas','Chiapas','29270','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Diana','Mora','Aguilar','MOAD910815MDF','diana.mora@correo.com','9616789900','Sur 8','56',NULL,'Terán','Tuxtla Gutiérrez','Chiapas','29030','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Ricardo','Soto','Luna','SOLR770220HDF','ricardo.soto@correo.com','6677890011','José María Morelos','89',NULL,'Barrio La Garita','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Paola','Bravo','Cruz','BRCP930430MDF','paola.bravo@correo.com','9618901122','Poniente 5','78',NULL,'Potinaspak','Tuxtla Gutiérrez','Chiapas','29040','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Hugo','Vega','Mendoza','VEMH810615HDF','hugo.vega@correo.com','6679012233','Francisco León','12',NULL,'Barrio de Mexicanos','San Cristóbal de las Casas','Chiapas','29240','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Karina','López','Silva','LOSK880720MDF','karina.lopez@correo.com','9610123344','9a. Oriente Norte','67',NULL,'El Jobo','Tuxtla Gutiérrez','Chiapas','29049','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Gerardo','Núñez','Bravo','NUBG790330HDF','gerardo.nunez@correo.com','6671234455','Prolongación Insurgentes','90',NULL,'Barrio de La Merced','San Cristóbal de las Casas','Chiapas','29214','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Andrea','Ramos','Hernández','RAHA920515MDF','andrea.ramos@correo.com','9612345566','15 de Septiembre','45',NULL,'Cerrito Buena Vista','Tuxtla Gutiérrez','Chiapas','29039','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Fabián','Cruz','Luna','CRLF850410HDF','fabian.cruz@correo.com','6673456677','Venustiano Carranza','67',NULL,'Barrio San Diego','San Cristóbal de las Casas','Chiapas','29218','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Liliana','Méndez','Soto','MESL900630MDF','lili.mendez@correo.com','9614567788','Cuarta Ote. Sur','34',NULL,'Lomas de Sayula','Tuxtla Gutiérrez','Chiapas','29033','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1')),
('Roberto','Ortiz','Vega','ORVR760815HDF','roberto.ortiz@correo.com','6675678899','Santos Degollado','23',NULL,'Barrio Guadalupe','San Cristóbal de las Casas','Chiapas','29230','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'agente1')),
('Sonia','Flores','Reyes','FORS880920MDF','sonia.flores@correo.com','9616789900','8a. Sur Ote.','56',NULL,'Plan de Ayala','Tuxtla Gutiérrez','Chiapas','29020','titular',NULL,(SELECT id_agente FROM agente WHERE clave_agente = 'admin1'));


-- ============================================================
--  2. PÓLIZAS (Batch 2)
-- ============================================================
INSERT INTO poliza (id_asegurado, id_producto, numero_poliza, fecha_inicio, fecha_vencimiento, estatus, prima_mensual)
VALUES
-- Familias
((SELECT id_asegurado FROM asegurado WHERE rfc='ESMA740315HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-001', '2026-01-01', '2027-01-01', 'activa',    2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='HEVS690910HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-002', '2025-08-01', '2026-08-01', 'activa',    2250.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='CABC820430HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-003', '2024-05-01', '2025-05-01', 'vencida',   2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='PARG770810HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-004', '2025-11-01', '2026-11-01', 'activa',    2350.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='LUMH790220HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-005', '2023-09-01', '2024-09-01', 'cancelada', 2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='DOPO750930HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-006', '2026-02-01', '2027-02-01', 'activa',    2220.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='RIVI880615HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-007', '2024-12-01', '2025-12-01', 'vencida',   2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='CUMJ730515HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-008', '2025-07-01', '2026-07-01', 'activa',    2150.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='SOLE800330HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-009', '2026-03-01', '2027-03-01', 'activa',    2300.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='MOBA820710HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-010', '2025-04-01', '2026-04-01', 'activa',    2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='OVSO760420HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-011', '2024-02-01', '2025-02-01', 'cancelada', 2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='GUMR710815HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-012', '2026-05-01', '2027-05-01', 'activa',    2400.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='VEHR850520HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-013', '2025-10-01', '2026-10-01', 'activa',    2200.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='PEOG780930HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-014', '2023-06-01', '2024-06-01', 'vencida',   2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='AGCS810115HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-015', '2026-06-01', '2027-06-01', 'activa',    2250.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='SAGB830520HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-016', '2025-01-01', '2026-01-01', 'activa',    2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='NARF770330HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-017', '2024-08-01', '2025-08-01', 'cancelada', 2100.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='IBCT800410HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-018', '2026-07-01', '2027-07-01', 'activa',    2350.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='FUMC880630HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-019', '2025-05-01', '2026-05-01', 'activa',    2150.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='DERM750815HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Plan Familiar'),    'FAM-CHIS2-020', '2024-03-01', '2025-03-01', 'vencida',   2100.00),
-- Individuales
((SELECT id_asegurado FROM asegurado WHERE rfc='RESM900415MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Vida Plus'),        'IND-CHIS2-001', '2026-01-01', '2027-01-01', 'activa',     650.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='LABE780930HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Cuidándote'),       'IND-CHIS2-002', '2024-06-01', '2025-06-01', 'vencida',   1200.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='CAMN850520MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Básico Accidentes'), 'IND-CHIS2-003', '2026-02-01', '2027-02-01', 'activa',     300.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='SIVO820710HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Vida Plus'),        'IND-CHIS2-004', '2025-09-01', '2026-09-01', 'activa',     650.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='MOAD910815MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Cuidándote'),       'IND-CHIS2-005', '2024-01-01', '2025-01-01', 'cancelada', 1200.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='SOLR770220HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Básico Accidentes'), 'IND-CHIS2-006', '2026-03-01', '2027-03-01', 'activa',     300.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='BRCP930430MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Vida Plus'),        'IND-CHIS2-007', '2023-07-01', '2024-07-01', 'vencida',    650.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='VEMH810615HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Cuidándote'),       'IND-CHIS2-008', '2025-12-01', '2026-12-01', 'activa',    1440.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='LOSK880720MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Básico Accidentes'), 'IND-CHIS2-009', '2026-04-01', '2027-04-01', 'activa',     300.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='NUBG790330HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Vida Plus'),        'IND-CHIS2-010', '2024-10-01', '2025-10-01', 'cancelada',  650.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='RAHA920515MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Cuidándote'),       'IND-CHIS2-011', '2025-11-01', '2026-11-01', 'activa',    1200.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='CRLF850410HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Básico Accidentes'), 'IND-CHIS2-012', '2026-05-01', '2027-05-01', 'activa',     300.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='MESL900630MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Vida Plus'),        'IND-CHIS2-013', '2024-04-01', '2025-04-01', 'vencida',    650.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='ORVR760815HDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Cuidándote'),       'IND-CHIS2-014', '2025-08-01', '2026-08-01', 'activa',    1200.00),
((SELECT id_asegurado FROM asegurado WHERE rfc='FORS880920MDF'), (SELECT id_producto FROM producto_poliza WHERE nombre='Básico Accidentes'), 'IND-CHIS2-015', '2026-06-01', '2027-06-01', 'activa',     300.00);


-- ============================================================
--  3. VINCULAR DEPENDIENTES A PÓLIZAS (Batch 2)
-- ============================================================
-- Familia 21
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-001') WHERE rfc='ESNC801020MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-001') WHERE rfc='ESNR150630MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-001') WHERE rfc='ESNT190415HDF';
-- Familia 22
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-002') WHERE rfc='HELM750615MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-002') WHERE rfc='HELE100820HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-002') WHERE rfc='HELS140130MDF';
-- Familia 23
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-003') WHERE rfc='CAPD880520MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-003') WHERE rfc='CABD130910HDF';
-- Familia 24
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-004') WHERE rfc='PADS830415MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-004') WHERE rfc='PALU090630MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-004') WHERE rfc='PAMS130815HDF';
-- Familia 25
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-005') WHERE rfc='LUIC851115MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-005') WHERE rfc='LUHC170930HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-005') WHERE rfc='LUCC210415MDF';
-- Familia 26
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-006') WHERE rfc='DOHE810220MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-006') WHERE rfc='DOHA150630MDF';
-- Familia 27
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-007') WHERE rfc='RIDA930930MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-007') WHERE rfc='RIMA180210HDF';
-- Familia 28
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-008') WHERE rfc='CURN791020MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-008') WHERE rfc='CURJ140315HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-008') WHERE rfc='CURV180710MDF';
-- Familia 29
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-009') WHERE rfc='SOFM860425MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-009') WHERE rfc='SOLM120915HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-009') WHERE rfc='SOPM160115MDF';
-- Familia 30
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-010') WHERE rfc='MOLC880310MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-010') WHERE rfc='MODC140520MDF';
-- Familia 31
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-011') WHERE rfc='OVPN820815MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-011') WHERE rfc='OVEN110930HDF';
-- Familia 32
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-012') WHERE rfc='GUAR780215MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-012') WHERE rfc='GUMR130410HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-012') WHERE rfc='GUNR170615MDF';
-- Familia 33
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-013') WHERE rfc='VESB910715MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-013') WHERE rfc='VEOB180820MDF';
-- Familia 34
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-014') WHERE rfc='PEKS840430MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-014') WHERE rfc='PEMS120630HDF';
-- Familia 35
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-015') WHERE rfc='AGMT870930MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-015') WHERE rfc='AGIM160310HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-015') WHERE rfc='AGMR200520MDF';
-- Familia 36
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-016') WHERE rfc='SACF891020MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-016') WHERE rfc='SAEF150715MDF';
-- Familia 37
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-017') WHERE rfc='NADL830615MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-017') WHERE rfc='NALL190415HDF';
-- Familia 38
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-018') WHERE rfc='IBVS860820MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-018') WHERE rfc='IBVA140230HDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-018') WHERE rfc='IBVM180910MDF';
-- Familia 39
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-019') WHERE rfc='FUES940215MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-019') WHERE rfc='FUDS180410HDF';
-- Familia 40
UPDATE asegurado SET tipo_asegurado='conyuge', id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-020') WHERE rfc='DERH810430MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-020') WHERE rfc='DELU160630MDF';
UPDATE asegurado SET tipo_asegurado='hijo',    id_poliza=(SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-020') WHERE rfc='DESH200915HDF';


-- ============================================================
--  4. BENEFICIOS (Batch 2)
-- ============================================================
-- 4a. Beneficios base incluidos
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
WHERE (p.numero_poliza LIKE 'FAM-CHIS2-%' OR p.numero_poliza LIKE 'IND-CHIS2-%')
  AND pb.activo = TRUE
  AND pb.deleted_at IS NULL
  AND pb.incluido_base = TRUE;

-- 4b. Odontología básica contratada en algunas familias
INSERT INTO beneficio (id_poliza, id_producto_beneficio, id_asegurado, costo_aplicado, vigente)
SELECT p.id_poliza, pb.id_producto_beneficio, NULL, pb.costo_extra, TRUE
FROM poliza p
JOIN producto_beneficio pb ON pb.id_producto = p.id_producto
WHERE p.numero_poliza IN ('FAM-CHIS2-002','FAM-CHIS2-008','FAM-CHIS2-012','FAM-CHIS2-016')
  AND pb.nombre_beneficio = 'Odontología básica'
  AND pb.activo = TRUE;

-- 4c. Maternidad para cónyuges en algunas pólizas familiares
INSERT INTO beneficio (id_poliza, id_producto_beneficio, id_asegurado, costo_aplicado, vigente)
SELECT p.id_poliza, pb.id_producto_beneficio, a.id_asegurado,
    CASE WHEN pb.incluido_base THEN 0 ELSE COALESCE(pb.costo_extra, 0) END,
    TRUE
FROM poliza p
JOIN producto_beneficio pb ON pb.id_producto = p.id_producto
JOIN asegurado a ON a.rfc IN ('ESNC801020MDF','HELM750615MDF','LUIC851115MDF','CURN791020MDF','GUAR780215MDF')
WHERE p.numero_poliza IN ('FAM-CHIS2-001','FAM-CHIS2-002','FAM-CHIS2-005','FAM-CHIS2-008','FAM-CHIS2-012')
  AND pb.nombre_beneficio = 'Maternidad'
  AND pb.activo = TRUE;


-- ============================================================
--  5. BENEFICIARIOS (Batch 2)
-- ============================================================
INSERT INTO beneficiario (id_poliza, id_asegurado, nombre_completo, parentesco, porcentaje_participacion, telefono)
VALUES
-- FAM-CHIS2-001
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-001'), (SELECT id_asegurado FROM asegurado WHERE rfc='ESMA740315HDF'), 'Cecilia Espinoza Nájera', 'Esposa', 100.0, '9612341123'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-001'), (SELECT id_asegurado FROM asegurado WHERE rfc='ESNC801020MDF'), 'Arturo Espinoza Mendoza', 'Esposo', 100.0, '9612341122'),
-- FAM-CHIS2-002
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-002'), (SELECT id_asegurado FROM asegurado WHERE rfc='HEVS690910HDF'), 'Mariana Herrera Luna', 'Esposa', 100.0, '9671122335'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-002'), (SELECT id_asegurado FROM asegurado WHERE rfc='HELM750615MDF'), 'Santiago Herrera Villanueva', 'Esposo', 100.0, '9671122334'),
-- FAM-CHIS2-003
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-003'), (SELECT id_asegurado FROM asegurado WHERE rfc='CABC820430HDF'), 'Paulina Camacho Domínguez', 'Esposa', 100.0, '9613452234'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-003'), (SELECT id_asegurado FROM asegurado WHERE rfc='CAPD880520MDF'), 'César Augusto Camacho Bravo', 'Esposo', 100.0, '9613452233'),
-- FAM-CHIS2-004
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-004'), (SELECT id_asegurado FROM asegurado WHERE rfc='PARG770810HDF'), 'Diana Pacheco Sosa', 'Esposa', 100.0, '6672233446'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-004'), (SELECT id_asegurado FROM asegurado WHERE rfc='PADS830415MDF'), 'Germán Pacheco Ríos', 'Esposo', 100.0, '6672233445'),
-- FAM-CHIS2-005
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-005'), (SELECT id_asegurado FROM asegurado WHERE rfc='LUMH790220HDF'), 'Ivonne Luna Cruz', 'Esposa', 100.0, '9614563345'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-005'), (SELECT id_asegurado FROM asegurado WHERE rfc='LUIC851115MDF'), 'Héctor Hugo Luna Mendoza', 'Esposo', 100.0, '9614563344'),
-- FAM-CHIS2-006
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-006'), (SELECT id_asegurado FROM asegurado WHERE rfc='DOPO750930HDF'), 'Erika Domínguez Herrera', 'Esposa', 100.0, '6673344557'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-006'), (SELECT id_asegurado FROM asegurado WHERE rfc='DOHE810220MDF'), 'Óscar Domínguez Pérez', 'Esposo', 100.0, '6673344556'),
-- FAM-CHIS2-007
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-007'), (SELECT id_asegurado FROM asegurado WHERE rfc='RIVI880615HDF'), 'Daniela Ríos Aguilar', 'Esposa', 100.0, '9615674456'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-007'), (SELECT id_asegurado FROM asegurado WHERE rfc='RIDA930930MDF'), 'Ignacio Ríos Vázquez', 'Esposo', 100.0, '9615674455'),
-- FAM-CHIS2-008
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-008'), (SELECT id_asegurado FROM asegurado WHERE rfc='CUMJ730515HDF'), 'Nancy Cruz Ramírez', 'Esposa', 100.0, '6674455668'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-008'), (SELECT id_asegurado FROM asegurado WHERE rfc='CURN791020MDF'), 'Julián Cruz Mendoza', 'Esposo', 100.0, '6674455667'),
-- FAM-CHIS2-009
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-009'), (SELECT id_asegurado FROM asegurado WHERE rfc='SOLE800330HDF'), 'Fernanda Soto Meza', 'Esposa', 100.0, '9616785567'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-009'), (SELECT id_asegurado FROM asegurado WHERE rfc='SOFM860425MDF'), 'Esteban Soto Lara', 'Esposo', 100.0, '9616785566'),
-- FAM-CHIS2-010
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-010'), (SELECT id_asegurado FROM asegurado WHERE rfc='MOBA820710HDF'), 'Lorena Molina Castro', 'Esposa', 100.0, '6675566779'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-010'), (SELECT id_asegurado FROM asegurado WHERE rfc='MOLC880310MDF'), 'Adrián Molina Bravo', 'Esposo', 100.0, '6675566778'),
-- FAM-CHIS2-011
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-011'), (SELECT id_asegurado FROM asegurado WHERE rfc='OVSO760420HDF'), 'Patricia Ortega Nava', 'Esposa', 100.0, '9617896678'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-011'), (SELECT id_asegurado FROM asegurado WHERE rfc='OVPN820815MDF'), 'Víctor Manuel Ortega Silva', 'Esposo', 100.0, '9617896677'),
-- FAM-CHIS2-012
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-012'), (SELECT id_asegurado FROM asegurado WHERE rfc='GUMR710815HDF'), 'Alejandra Gutiérrez Ríos', 'Esposa', 100.0, '6676677890'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-012'), (SELECT id_asegurado FROM asegurado WHERE rfc='GUAR780215MDF'), 'Rafael Gutiérrez Mendoza', 'Esposo', 100.0, '6676677889'),
-- FAM-CHIS2-013
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-013'), (SELECT id_asegurado FROM asegurado WHERE rfc='VEHR850520HDF'), 'Silvia Velasco Bravo', 'Esposa', 100.0, '9618907789'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-013'), (SELECT id_asegurado FROM asegurado WHERE rfc='VESB910715MDF'), 'Rodrigo Velasco Hernández', 'Esposo', 100.0, '9618907788'),
-- FAM-CHIS2-014
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-014'), (SELECT id_asegurado FROM asegurado WHERE rfc='PEOG780930HDF'), 'Karla Peña Sánchez', 'Esposa', 100.0, '6677788991'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-014'), (SELECT id_asegurado FROM asegurado WHERE rfc='PEKS840430MDF'), 'Gerardo Peña Ortiz', 'Esposo', 100.0, '6677788990'),
-- FAM-CHIS2-015
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-015'), (SELECT id_asegurado FROM asegurado WHERE rfc='AGCS810115HDF'), 'Tania Aguilar Méndez', 'Esposa', 100.0, '9619018900'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-015'), (SELECT id_asegurado FROM asegurado WHERE rfc='AGMT870930MDF'), 'Samuel Aguilar Cruz', 'Esposo', 100.0, '9619018899'),
-- FAM-CHIS2-016
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-016'), (SELECT id_asegurado FROM asegurado WHERE rfc='SAGB830520HDF'), 'Carolina Salazar Flores', 'Esposa', 100.0, '6678899002'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-016'), (SELECT id_asegurado FROM asegurado WHERE rfc='SACF891020MDF'), 'Bruno Salazar Gómez', 'Esposo', 100.0, '6678899001'),
-- FAM-CHIS2-017
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-017'), (SELECT id_asegurado FROM asegurado WHERE rfc='NARF770330HDF'), 'Daniela Navarro Luna', 'Esposa', 100.0, '9610129901'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-017'), (SELECT id_asegurado FROM asegurado WHERE rfc='NADL830615MDF'), 'Francisco Navarro Reyes', 'Esposo', 100.0, '9610129900'),
-- FAM-CHIS2-018
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-018'), (SELECT id_asegurado FROM asegurado WHERE rfc='IBCT800410HDF'), 'Susana Ibarra Vega', 'Esposa', 100.0, '6679900113'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-018'), (SELECT id_asegurado FROM asegurado WHERE rfc='IBVS860820MDF'), 'Tomás Ibarra Castro', 'Esposo', 100.0, '6679900112'),
-- FAM-CHIS2-019
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-019'), (SELECT id_asegurado FROM asegurado WHERE rfc='FUMC880630HDF'), 'Elena Fuentes Soto', 'Esposa', 100.0, '9611230012'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-019'), (SELECT id_asegurado FROM asegurado WHERE rfc='FUES940215MDF'), 'Cristian Fuentes Mora', 'Esposo', 100.0, '9611230011'),
-- FAM-CHIS2-020
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-020'), (SELECT id_asegurado FROM asegurado WHERE rfc='DERM750815HDF'), 'Renata Delgado Hernández', 'Esposa', 100.0, '6670011224'),
((SELECT id_poliza FROM poliza WHERE numero_poliza='FAM-CHIS2-020'), (SELECT id_asegurado FROM asegurado WHERE rfc='DERH810430MDF'), 'Mauricio Delgado Ríos', 'Esposo', 100.0, '6670011223'),
-- IND-CHIS2-001
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-001'), (SELECT id_asegurado FROM asegurado WHERE rfc='RESM900415MDF'), 'Jorge Reyes Soto', 'Padre', 100.0, NULL),
-- IND-CHIS2-002
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-002'), (SELECT id_asegurado FROM asegurado WHERE rfc='LABE780930HDF'), 'María Lara Bravo', 'Madre', 100.0, NULL),
-- IND-CHIS2-003
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-003'), (SELECT id_asegurado FROM asegurado WHERE rfc='CAMN850520MDF'), 'Pedro Castro Méndez', 'Padre', 100.0, NULL),
-- IND-CHIS2-004
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-004'), (SELECT id_asegurado FROM asegurado WHERE rfc='SIVO820710HDF'), 'Rosa Silva Vargas', 'Madre', 100.0, NULL),
-- IND-CHIS2-005
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-005'), (SELECT id_asegurado FROM asegurado WHERE rfc='MOAD910815MDF'), 'José Mora Aguilar', 'Padre', 100.0, NULL),
-- IND-CHIS2-006
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-006'), (SELECT id_asegurado FROM asegurado WHERE rfc='SOLR770220HDF'), 'Carmen Soto Luna', 'Madre', 100.0, NULL),
-- IND-CHIS2-007
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-007'), (SELECT id_asegurado FROM asegurado WHERE rfc='BRCP930430MDF'), 'Roberto Bravo Cruz', 'Padre', 100.0, NULL),
-- IND-CHIS2-008
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-008'), (SELECT id_asegurado FROM asegurado WHERE rfc='VEMH810615HDF'), 'Laura Vega Mendoza', 'Madre', 100.0, NULL),
-- IND-CHIS2-009
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-009'), (SELECT id_asegurado FROM asegurado WHERE rfc='LOSK880720MDF'), 'Miguel López Silva', 'Padre', 100.0, NULL),
-- IND-CHIS2-010
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-010'), (SELECT id_asegurado FROM asegurado WHERE rfc='NUBG790330HDF'), 'Ana Núñez Bravo', 'Madre', 100.0, NULL),
-- IND-CHIS2-011
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-011'), (SELECT id_asegurado FROM asegurado WHERE rfc='RAHA920515MDF'), 'Carlos Ramos Hernández', 'Padre', 100.0, NULL),
-- IND-CHIS2-012
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-012'), (SELECT id_asegurado FROM asegurado WHERE rfc='CRLF850410HDF'), 'Diana Cruz Luna', 'Madre', 100.0, NULL),
-- IND-CHIS2-013
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-013'), (SELECT id_asegurado FROM asegurado WHERE rfc='MESL900630MDF'), 'Fernando Méndez Soto', 'Padre', 100.0, NULL),
-- IND-CHIS2-014
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-014'), (SELECT id_asegurado FROM asegurado WHERE rfc='ORVR760815HDF'), 'María Ortiz Vega', 'Madre', 100.0, NULL),
-- IND-CHIS2-015
((SELECT id_poliza FROM poliza WHERE numero_poliza='IND-CHIS2-015'), (SELECT id_asegurado FROM asegurado WHERE rfc='FORS880920MDF'), 'Jorge Flores Reyes', 'Padre', 100.0, NULL);


-- ============================================================
--  6. SEGUIMIENTOS (Batch 2)
-- ============================================================
INSERT INTO seguimiento (folio, id_asegurado, id_agente, asunto)
VALUES
('SEG-CHIS2-2025-001', (SELECT id_asegurado FROM asegurado WHERE rfc='ESMA740315HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Alta Plan Familiar El Mirador'),
('SEG-CHIS2-2025-002', (SELECT id_asegurado FROM asegurado WHERE rfc='HEVS690910HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Revisión cobertura La Garita'),
('SEG-CHIS2-2025-003', (SELECT id_asegurado FROM asegurado WHERE rfc='CABC820430HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Renovación vencida Potinaspak'),
('SEG-CHIS2-2025-004', (SELECT id_asegurado FROM asegurado WHERE rfc='PARG770810HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Ajuste de prima mensual'),
('SEG-CHIS2-2025-005', (SELECT id_asegurado FROM asegurado WHERE rfc='LUMH790220HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Cancelación por mudanza'),
('SEG-CHIS2-2025-006', (SELECT id_asegurado FROM asegurado WHERE rfc='DOPO750930HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Contratación Plan Familiar El Cerrillo'),
('SEG-CHIS2-2025-007', (SELECT id_asegurado FROM asegurado WHERE rfc='RIVI880615HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Renovación automática Lomas de Sayula'),
('SEG-CHIS2-2025-008', (SELECT id_asegurado FROM asegurado WHERE rfc='CUMJ730515HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Cambio de beneficiarios Guadalupe'),
('SEG-CHIS2-2025-009', (SELECT id_asegurado FROM asegurado WHERE rfc='SOLE800330HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Contratación con dental incluido'),
('SEG-CHIS2-2025-010', (SELECT id_asegurado FROM asegurado WHERE rfc='MOBA820710HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Solicitud de siniestro menor'),
('SEG-CHIS2-2025-011', (SELECT id_asegurado FROM asegurado WHERE rfc='OVSO760420HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Cancelación formal Albania Baja'),
('SEG-CHIS2-2025-012', (SELECT id_asegurado FROM asegurado WHERE rfc='GUMR710815HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Contratación Plan Familiar Plus'),
('SEG-CHIS2-2025-013', (SELECT id_asegurado FROM asegurado WHERE rfc='VEHR850520HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Renovación Patria Nueva'),
('SEG-CHIS2-2025-014', (SELECT id_asegurado FROM asegurado WHERE rfc='PEOG780930HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Revisión vencida El Mirador'),
('SEG-CHIS2-2025-015', (SELECT id_asegurado FROM asegurado WHERE rfc='AGCS810115HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Alta Plan Familiar El Retiro'),
('SEG-CHIS2-2025-016', (SELECT id_asegurado FROM asegurado WHERE rfc='SAGB830520HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Cambio de agente Santa Lucía'),
('SEG-CHIS2-2025-017', (SELECT id_asegurado FROM asegurado WHERE rfc='NARF770330HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Cancelación Solidaridad'),
('SEG-CHIS2-2025-018', (SELECT id_asegurado FROM asegurado WHERE rfc='IBCT800410HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Contratación con maternidad'),
('SEG-CHIS2-2025-019', (SELECT id_asegurado FROM asegurado WHERE rfc='FUMC880630HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Renovación Bosque Sur'),
('SEG-CHIS2-2025-020', (SELECT id_asegurado FROM asegurado WHERE rfc='DERM750815HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Ajuste de suma asegurada'),
('SEG-CHIS2-2025-021', (SELECT id_asegurado FROM asegurado WHERE rfc='RESM900415MDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Contratación Vida Plus INFONAVIT'),
('SEG-CHIS2-2025-022', (SELECT id_asegurado FROM asegurado WHERE rfc='LABE780930HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Renovación vencida Cuidándote'),
('SEG-CHIS2-2025-023', (SELECT id_asegurado FROM asegurado WHERE rfc='CAMN850520MDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Alta Básico Accidentes Granjas'),
('SEG-CHIS2-2025-024', (SELECT id_asegurado FROM asegurado WHERE rfc='SIVO820710HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Revisión cobertura Vida Plus'),
('SEG-CHIS2-2025-025', (SELECT id_asegurado FROM asegurado WHERE rfc='MOAD910815MDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Cancelación Cuidándote Terán'),
('SEG-CHIS2-2025-026', (SELECT id_asegurado FROM asegurado WHERE rfc='SOLR770220HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Contratación Básico Accidentes'),
('SEG-CHIS2-2025-027', (SELECT id_asegurado FROM asegurado WHERE rfc='BRCP930430MDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Renovación Vida Plus vencida'),
('SEG-CHIS2-2025-028', (SELECT id_asegurado FROM asegurado WHERE rfc='VEMH810615HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Contratación Cuidándote Plus'),
('SEG-CHIS2-2025-029', (SELECT id_asegurado FROM asegurado WHERE rfc='LOSK880720MDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Alta Básico Accidentes El Jobo'),
('SEG-CHIS2-2025-030', (SELECT id_asegurado FROM asegurado WHERE rfc='NUBG790330HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Cancelación Vida Plus'),
('SEG-CHIS2-2025-031', (SELECT id_asegurado FROM asegurado WHERE rfc='RAHA920515MDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Renovación Cuidándote Buena Vista'),
('SEG-CHIS2-2025-032', (SELECT id_asegurado FROM asegurado WHERE rfc='CRLF850410HDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Contratación Básico Accidentes'),
('SEG-CHIS2-2025-033', (SELECT id_asegurado FROM asegurado WHERE rfc='MESL900630MDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Renovación vencida Vida Plus'),
('SEG-CHIS2-2025-034', (SELECT id_asegurado FROM asegurado WHERE rfc='ORVR760815HDF'), (SELECT id_agente FROM agente WHERE clave_agente='admin1'), 'Contratación Cuidándote Guadalupe'),
('SEG-CHIS2-2025-035', (SELECT id_asegurado FROM asegurado WHERE rfc='FORS880920MDF'), (SELECT id_agente FROM agente WHERE clave_agente='agente1'), 'Alta Básico Accidentes Ayala');


-- ============================================================
--  7. SEGUIMIENTO_CONTACTO (Batch 2)
-- ============================================================
INSERT INTO seguimiento_contacto (id_seguimiento, iniciado_por, tipo_contacto, observaciones, resultado, fecha_hora)
VALUES
-- SEG-CHIS2-2025-001 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-001'), 'agente', 'llamada', 'Cliente confirmó datos familiares y aceptó prima de $2,100.', 'resuelto', '2025-02-10 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-001'), 'asegurado', 'mensaje', 'Solicitó copia de póliza por correo.', 'pendiente', '2025-02-12 14:30:00'),
-- SEG-CHIS2-2025-002 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-002'), 'agente', 'llamada', 'Revisión anual sin cambios, cliente satisfecho.', 'resuelto', '2025-03-15 11:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-002'), 'asegurado', 'llamada', 'Consultó sobre red de hospitales en San Cristóbal.', 'resuelto', '2025-03-16 09:30:00'),
-- SEG-CHIS2-2025-003 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-003'), 'agente', 'llamada', 'Recordatorio de renovación vencida enviado.', 'sin_respuesta', '2025-04-20 13:00:00'),
-- SEG-CHIS2-2025-004 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-004'), 'agente', 'visita', 'Visita domiciliaria para ajuste de prima por nuevo dependiente.', 'resuelto', '2025-05-10 15:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-004'), 'asegurado', 'mensaje', 'Confirmó que realizará el pago de la diferencia.', 'pendiente', '2025-05-11 10:00:00'),
-- SEG-CHIS2-2025-005 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-005'), 'asegurado', 'visita', 'Cliente acudió a cancelar por mudanza a otro estado.', 'resuelto', '2025-01-25 16:00:00'),
-- SEG-CHIS2-2025-006 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-006'), 'agente', 'llamada', 'Contratación de Plan Familiar en El Cerrillo.', 'resuelto', '2025-06-05 10:30:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-006'), 'asegurado', 'llamada', 'Preguntó sobre cobertura de maternidad para cónyuge.', 'resuelto', '2025-06-06 11:00:00'),
-- SEG-CHIS2-2025-007 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-007'), 'agente', 'llamada', 'Renovación automática procesada, pago confirmado.', 'resuelto', '2025-07-12 09:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-007'), 'asegurado', 'mensaje', 'Agradeció confirmación de renovación.', 'resuelto', '2025-07-13 14:00:00'),
-- SEG-CHIS2-2025-008 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-008'), 'agente', 'llamada', 'Actualización de lista de beneficiarios solicitada.', 'resuelto', '2025-08-20 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-008'), 'asegurado', 'mensaje', 'Envió documentos de identificación actualizados.', 'pendiente', '2025-08-21 16:00:00'),
-- SEG-CHIS2-2025-009 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-009'), 'agente', 'visita', 'Visita para firma de anexo de odontología básica.', 'resuelto', '2025-09-15 14:00:00'),
-- SEG-CHIS2-2025-010 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-010'), 'agente', 'llamada', 'Registro de siniestro menor en La Merced.', 'resuelto', '2025-10-05 11:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-010'), 'asegurado', 'llamada', 'Confirmó cita médica programada para evaluación.', 'resuelto', '2025-10-06 09:30:00'),
-- SEG-CHIS2-2025-011 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-011'), 'asegurado', 'visita', 'Cliente acudió a oficina para solicitar cancelación formal.', 'resuelto', '2025-02-20 15:00:00'),
-- SEG-CHIS2-2025-012 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-012'), 'agente', 'llamada', 'Contratación Plan Familiar Plus con cobertura extendida.', 'resuelto', '2025-03-25 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-012'), 'asegurado', 'mensaje', 'Solicitó detalle de hospitales afiliados en Chiapas.', 'pendiente', '2025-03-26 11:00:00'),
-- SEG-CHIS2-2025-013 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-013'), 'agente', 'llamada', 'Renovación anual procesada exitosamente.', 'resuelto', '2025-04-15 09:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-013'), 'asegurado', 'llamada', 'Confirmó que desea mantener cobertura actual.', 'resuelto', '2025-04-16 10:00:00'),
-- SEG-CHIS2-2025-014 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-014'), 'agente', 'llamada', 'Se intentó contactar para renovación vencida sin éxito.', 'sin_respuesta', '2025-05-01 13:00:00'),
-- SEG-CHIS2-2025-015 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-015'), 'agente', 'visita', 'Visita domiciliaria para alta de Plan Familiar en El Retiro.', 'resuelto', '2025-06-10 15:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-015'), 'asegurado', 'mensaje', 'Confirmó datos de dependientes por WhatsApp.', 'pendiente', '2025-06-11 10:00:00'),
-- SEG-CHIS2-2025-016 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-016'), 'agente', 'llamada', 'Cambio de agente responsable aprobado.', 'resuelto', '2025-07-20 09:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-016'), 'asegurado', 'llamada', 'Consultó nombre y contacto del nuevo agente.', 'resuelto', '2025-07-21 11:00:00'),
-- SEG-CHIS2-2025-017 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-017'), 'asegurado', 'visita', 'Solicitó cancelación por cambio de empleador.', 'resuelto', '2025-08-15 16:00:00'),
-- SEG-CHIS2-2025-018 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-018'), 'agente', 'llamada', 'Contratación con cobertura de maternidad incluida.', 'resuelto', '2025-09-01 10:30:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-018'), 'asegurado', 'mensaje', 'Agradeció información sobre beneficio de maternidad.', 'resuelto', '2025-09-02 14:00:00'),
-- SEG-CHIS2-2025-019 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-019'), 'agente', 'llamada', 'Renovación de póliza familiar en Bosque Sur.', 'resuelto', '2025-10-10 09:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-019'), 'asegurado', 'llamada', 'Confirmó que realizará pago antes del vencimiento.', 'resuelto', '2025-10-11 10:00:00'),
-- SEG-CHIS2-2025-020 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-020'), 'agente', 'llamada', 'Ajuste de suma asegurada por cambio de estado civil.', 'resuelto', '2025-11-20 11:00:00'),
-- SEG-CHIS2-2025-021 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-021'), 'agente', 'llamada', 'Contratación Vida Plus individual en INFONAVIT.', 'resuelto', '2025-01-15 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-021'), 'asegurado', 'mensaje', 'Solicitó pago anual en lugar de mensual.', 'pendiente', '2025-01-16 09:00:00'),
-- SEG-CHIS2-2025-022 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-022'), 'agente', 'llamada', 'Recordatorio de renovación vencida de Cuidándote.', 'sin_respuesta', '2025-02-28 13:00:00'),
-- SEG-CHIS2-2025-023 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-023'), 'agente', 'llamada', 'Alta de Básico Accidentes para empleada doméstica.', 'resuelto', '2025-03-10 10:30:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-023'), 'asegurado', 'llamada', 'Preguntó sobre cobertura en actividades recreativas.', 'resuelto', '2025-03-11 09:00:00'),
-- SEG-CHIS2-2025-024 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-024'), 'agente', 'llamada', 'Revisión de cobertura Vida Plus antes de renovación.', 'resuelto', '2025-04-20 14:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-024'), 'asegurado', 'mensaje', 'Confirmó que actualizó datos en portal web.', 'pendiente', '2025-04-21 11:00:00'),
-- SEG-CHIS2-2025-025 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-025'), 'asegurado', 'visita', 'Solicitó cancelación de Cuidándote por cambio de empleo.', 'resuelto', '2025-05-15 16:00:00'),
-- SEG-CHIS2-2025-026 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-026'), 'agente', 'llamada', 'Contratación Básico Accidentes como complemento.', 'resuelto', '2025-06-01 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-026'), 'asegurado', 'llamada', 'Consultó red de hospitales en San Cristóbal.', 'resuelto', '2025-06-02 09:30:00'),
-- SEG-CHIS2-2025-027 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-027'), 'agente', 'llamada', 'Intento de renovación Vida Plus vencida sin respuesta.', 'sin_respuesta', '2025-07-10 11:00:00'),
-- SEG-CHIS2-2025-028 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-028'), 'agente', 'llamada', 'Contratación Cuidándote Plus con cobertura nacional.', 'resuelto', '2025-08-05 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-028'), 'asegurado', 'mensaje', 'Solicitó lista de hospitales afiliados en Tuxtla.', 'pendiente', '2025-08-06 14:00:00'),
-- SEG-CHIS2-2025-029 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-029'), 'agente', 'llamada', 'Alta Básico Accidentes para trabajador independiente.', 'resuelto', '2025-09-10 09:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-029'), 'asegurado', 'llamada', 'Confirmó que desea cobertura por un año.', 'resuelto', '2025-09-11 10:00:00'),
-- SEG-CHIS2-2025-030 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-030'), 'asegurado', 'visita', 'Acudió a oficina a cancelar Vida Plus por economía.', 'resuelto', '2025-10-25 15:00:00'),
-- SEG-CHIS2-2025-031 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-031'), 'agente', 'llamada', 'Renovación Cuidándote en Cerrito Buena Vista.', 'resuelto', '2025-11-15 10:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-031'), 'asegurado', 'mensaje', 'Agradeció recordatorio de renovación.', 'resuelto', '2025-11-16 09:00:00'),
-- SEG-CHIS2-2025-032 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-032'), 'agente', 'llamada', 'Contratación Básico Accidentes como complemento familiar.', 'resuelto', '2025-12-01 10:30:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-032'), 'asegurado', 'llamada', 'Consultó cobertura en deportes de aventura.', 'resuelto', '2025-12-02 11:00:00'),
-- SEG-CHIS2-2025-033 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-033'), 'agente', 'llamada', 'Renovación vencida Vida Plus, cliente no localizable.', 'sin_respuesta', '2025-01-30 13:00:00'),
-- SEG-CHIS2-2025-034 (2)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-034'), 'agente', 'visita', 'Visita domiciliaria para contratación Cuidándote Plus.', 'resuelto', '2025-02-15 14:00:00'),
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-034'), 'asegurado', 'mensaje', 'Confirmó firma de contrato digital.', 'pendiente', '2025-02-16 10:00:00'),
-- SEG-CHIS2-2025-035 (1)
((SELECT id_seguimiento FROM seguimiento WHERE folio='SEG-CHIS2-2025-035'), 'agente', 'llamada', 'Alta Básico Accidentes para empleado de construcción.', 'resuelto', '2025-03-20 11:00:00');