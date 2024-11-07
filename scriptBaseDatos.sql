-- Tabla de roles
CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);



CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    correo VARCHAR(50) NOT NULL UNIQUE,
    contrasenia VARCHAR(100) NOT NULL,
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL
);

CREATE TABLE datos_personales_usuarios (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    nombres_apellidos VARCHAR(255),
    sexo VARCHAR(10),
    edad INT,
    estado_civil VARCHAR(20),
    fecha_nacimiento DATE,
    telefono VARCHAR(100),
    ocupacion VARCHAR(50),
    procedencia VARCHAR(100),
    religion VARCHAR(50),
    fecha DATE,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE

)

-- Tabla de proyectos
CREATE TABLE proyecto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE
);

-- Tabla de relación entre usuarios y proyectos
CREATE TABLE usuarios_proyecto (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    proyecto_id INT NOT NULL,
    PRIMARY KEY (user_id, proyecto_id),
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE
);

-- Tabla de alimentación
CREATE TABLE alimentacion (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    desayuno_hora TIME NOT NULL,
    almuerzo_hora TIME,
    cena_hora TIME,
    desayuno VARCHAR(100), // //  desayuno, almuerzo, cena otro solo esos podran ser elejidos
    almuerzo VARCHAR(100), // //  desayuno, almuerzo, cena otro solo esos podran ser elejidos
    cena VARCHAR(100), // //  desayuno, almuerzo, cena otro solo esos podran ser elejidos
    desayuno_saludable VARCHAR(50),
    almuerzo_saludable VARCHAR(50),
    cena_saludable VARCHAR(50),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de agua
CREATE TABLE agua (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    cantidad INT NOT NULL, //solo se medira en mililitros
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de esperanza
CREATE TABLE esperanza (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    tipo_practica VARCHAR(50) NOT NULL,  // 1 oracion leer 2 la biblia. solo se pueden esas 2
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de sol
CREATE TABLE sol (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    tiempo INT NOT NULL, // se calculara cantidad de minutos
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de aire
CREATE TABLE aire (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    tiempo INT NOT NULL, // Cantidad de minutos
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de sueño
CREATE TABLE dormir (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de despertar
CREATE TABLE despertar (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado VARCHAR(20) NOT NULL, // solo se podra ingresar si durmio "bien" o "mal"
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de ejercicio
CREATE TABLE ejercicio (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    tipo VARCHAR(50) NOT NULL, // solo se podra ingresar estos datos [caminata lenta, rapida, carrera o ejercicio guiado]
    tiempo INT NOT NULL, // solo sera en cantidad de minutos
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE datos_fisicos (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    peso DECIMAL(5, 2),               -- Peso en kg
    altura DECIMAL(4, 2),             -- Altura en metros
    imc DECIMAL(4, 2),                -- Índice de Masa Corporal
    radio_abdominal DECIMAL(5, 2),    -- Radio Abdominal en cm
    grasa_corporal DECIMAL(5, 2),     -- Grasa Corporal en %
    grasa_viseral DECIMAL(5, 2),      -- Grasa Visceral en %
    porcentaje_musculo NUMERIC(4,1),-------------------

    fecha DATE NOT NULL, -- Fecha de la medición
    tipo VARCHAR(20) NOT NULL,   -- 'inicial' o 'final' 

    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE signos_vitales (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    presion_sistolica INT,            -- Presión Arterial Sistólica en mmHg
    presion_diastolica INT,           -- Presión Arterial Diastólica en mmHg
    frecuencia_cardiaca INT,          -- Frecuencia Cardíaca en latidos/min
    frecuencia_respiratoria INT,      -- Frecuencia Respiratoria en respiraciones/min
    temperatura NUMERIC(3,1), -------------------
    saturacion_oxigeno INT, -------------------  

    fecha DATE NOT NULL, -- Fecha de la medición
    tipo VARCHAR(20) NOT NULL,   -- 'inicial' o 'final' 

    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE datos_muestras (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    colesterol_total DECIMAL(5, 2),   -- Colesterol Total en mg/dL
    colesterol_hdl DECIMAL(5, 2),     -- Colesterol HDL en mg/dL
    colesterol_ldl DECIMAL(5, 2),     -- Colesterol LDL en mg/dL
    trigliceridos DECIMAL(5, 2),      -- Triglicéridos en mg/dL
    glucosa DECIMAL(5, 2),  
    glicemia_basal NUMERIC(4,1),-------------------       -- Glucosa en mg/dL

    fecha DATE NOT NULL, -- Fecha de la medición
    tipo VARCHAR(20) NOT NULL,   -- 'inicial' o 'final' 

    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);



CREATE TABLE datos_habitos_agua(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,

    bebo_solo_agua_pura INT,
    bebo_8_vasos_agua INT,
    bebidas_con_azucar INT,
    bebo_agua_al_despertar INT,
    bebo_agua_antes_comidas INT,
    bebo_agua_para_dormir INT,

    fecha DATE NOT NULL, -- Fecha de la medición
    tipo VARCHAR(20) NOT NULL,   -- 'inicial' o 'final' 
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE datos_habitos_aire(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,

    tecnica_respiraciones_profundas INT,
    tiempo_tecnica_respiraciones INT,
    horario_tecnica_respiraciones_manana INT,
    horario_tecnica_respiraciones_noche INT,

    fecha DATE NOT NULL, -- Fecha de la medición
    tipo VARCHAR(20) NOT NULL,   -- 'inicial' o 'final' 
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE datos_habitos_alimentacion(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,

    consumo_3_comidas_horario_fijo INT, 
    consumo_5_porciones_frutas_verduras INT,
    consumo_3_porciones_proteinas INT,
    ingiero_otros_alimentos INT,
    consumo_carbohidratos INT,
    consumo_alimentos_fritos INT,
    consumo_alimentos_hechos_en_casa INT,
    consumo_liquidos_mientras_como INT,

    fecha DATE NOT NULL, -- Fecha de la medición
    tipo VARCHAR(20) NOT NULL,   -- 'inicial' o 'final' 
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE datos_habitos_temperancia(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,

    consumo_bebidas_alcoholicas INT,
    eventos_sociales_alcohol INT,
    consumo_sustancias_estimulantes INT,
    consumo_refrescos_cola INT,
    consumo_cigarrillos INT,
    consumo_comida_chatarra INT,
    pedir_mas_comida INT,
    agregar_mas_azucar INT,
    agregar_mas_sal INT,
    satisfecho_trabajo INT,
    tenso_nervioso_estresado INT,
    tiempo_libre_redes_sociales INT,
    satisfecho_relaciones_sociales INT,
    apoyo_familia_decisiones INT,

    fecha DATE NOT NULL, -- Fecha de la medición
    tipo VARCHAR(20) NOT NULL,   -- 'inicial' o 'final' 
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE datos_habitos_ejercicio(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,

    realizo_actividad_deportiva INT,
    ejercicio_fisico_diario INT,
    practico_deporte_tiempo_libre INT,
    dedicacion_30_minutos_ejercicio INT,
    ejercicio_carrera_bicicleta INT,

    fecha DATE NOT NULL, -- Fecha de la medición
    tipo VARCHAR(20) NOT NULL,   -- 'inicial' o 'final' 
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE datos_habitos_descanso(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,

    duermo_7_8_horas INT,
    despertar_durante_noche INT,
    dificultad_sueno_reparador INT,
    horario_sueno_diario INT,
    despertar_horario_diario INT,

    fecha DATE NOT NULL, -- Fecha de la medición
    tipo VARCHAR(20) NOT NULL,   -- 'inicial' o 'final' 
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE datos_habitos_sol(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,

    exposicion_sol_diaria INT,
    exposicion_sol_horas_seguras INT,
    exposicion_sol_20_minutos INT,
    uso_bloqueador_solar INT,

    fecha DATE NOT NULL, -- Fecha de la medición
    tipo VARCHAR(20) NOT NULL,   -- 'inicial' o 'final' 
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE datos_habitos_esperanza(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,

    ser_supremo_interviene INT,
    leo_biblia INT,
    practico_oracion INT,
    orar_y_estudiar_biblia_desarrollo_personal INT
    
    fecha DATE NOT NULL, -- Fecha de la medición
    tipo VARCHAR(20) NOT NULL,   -- 'inicial' o 'final' 
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
