CREATE OR REPLACE PROCEDURE usuario.create_user(
    p_nombre        TEXT,
    p_apellido      TEXT,
    p_dni           VARCHAR(10),
    p_email         TEXT,
    p_password      TEXT,
    p_id_rol        INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_persona    INTEGER;
    v_existe_rol    INTEGER;
BEGIN

    ----------------------------------------------------
    -- VALIDACIONES GENERALES
    ----------------------------------------------------
    IF trim(coalesce(p_nombre,'')) = '' THEN
        RAISE EXCEPTION 'El nombre no puede estar vacío';
    END IF;

    IF trim(coalesce(p_apellido,'')) = '' THEN
        RAISE EXCEPTION 'El apellido no puede estar vacío';
    END IF;

    IF trim(coalesce(p_dni,'')) = '' THEN
        RAISE EXCEPTION 'El DNI no puede estar vacío';
    END IF;

    IF length(trim(p_dni)) < 8 or length(trim(p_dni)) >10 THEN
        RAISE EXCEPTION 'El DNI debe tener entre 8 y 10 caracteres';
    END IF;

    IF trim(coalesce(p_email,'')) = '' THEN
        RAISE EXCEPTION 'El email no puede estar vacío';
    END IF;

    IF p_email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Formato de email inválido';
    END IF;

    IF trim(coalesce(p_password,'')) = '' THEN
        RAISE EXCEPTION 'La contraseña no puede estar vacía';
    END IF;

    IF length(trim(p_password)) < 6 THEN
        RAISE EXCEPTION 'La contraseña debe tener al menos 6 caracteres';
    END IF;

    IF p_id_rol IS NULL OR p_id_rol <= 0 THEN
        RAISE EXCEPTION 'Debe indicar un id de rol válido';
    END IF;


    ----------------------------------------------------
    -- VALIDAR EXISTENCIA DEL ROL
    ----------------------------------------------------
    SELECT COUNT(*)
    INTO v_existe_rol
    FROM usuario.rol
    WHERE id_rol = p_id_rol;

    IF v_existe_rol = 0 THEN
        RAISE EXCEPTION 'Debe indicar un id de rol válido';
    END IF;


    ----------------------------------------------------
    -- INSERTAR PERSONA
    ----------------------------------------------------
    BEGIN
        INSERT INTO usuario.persona(
            nombre,
            apellido,
            dni
        )
        VALUES(
            trim(p_nombre),
            trim(p_apellido),
            trim(p_dni)
        )
        RETURNING id_persona
        INTO v_id_persona;


    EXCEPTION
        WHEN unique_violation THEN
            RAISE EXCEPTION 'El DNI ya existe en la base de datos';

        WHEN OTHERS THEN
            RAISE EXCEPTION 'Error al insertar persona: %', SQLERRM;
    END;


    ----------------------------------------------------
    -- INSERTAR USUARIO
    ----------------------------------------------------
    BEGIN
        INSERT INTO usuario.usuario(
            email,
            password,
            fecha_creacion,
            activo,
            id_persona,
            id_rol
        )
        VALUES(
            lower(trim(p_email)),
            p_password,
            CURRENT_DATE,
            TRUE,
            v_id_persona,
            p_id_rol
        );

   

    EXCEPTION
        WHEN unique_violation THEN
            RAISE EXCEPTION 'El email ya existe en la base de datos';

        WHEN foreign_key_violation THEN
            RAISE EXCEPTION 'Error de clave foránea al crear usuario';

        WHEN OTHERS THEN
            RAISE EXCEPTION 'Error al insertar usuario: %', SQLERRM;
    END;


    ----------------------------------------------------
    -- FIN OK
    ----------------------------------------------------
    RAISE NOTICE 'Usuario insertado correctamente';

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'ERROR: %', SQLERRM;
        RAISE;
        -- rollback automático al fallar el CALL
END;
$$;





CREATE OR REPLACE FUNCTION usuario.get_roles()
RETURNS TABLE (
    id_rol      INTEGER,
    nombre_rol  TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        r.id_rol,
        r.nombre_rol
    FROM usuario.rol r
    ORDER BY r.id_rol;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error en get_roles(): %', SQLERRM;
END;
$$;


CREATE OR REPLACE FUNCTION usuario.get_user_by_id(p_id_usuario INTEGER)
RETURNS TABLE (
    id_user INTEGER,
    email VARCHAR,
    nombre VARCHAR,
    apellido VARCHAR,
    dni VARCHAR,
    activo BOOLEAN,
    nombre_rol VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id_user,
        u.email::VARCHAR,          -- casteo explícito
        p.nombre::VARCHAR,
        p.apellido::VARCHAR,
        p.dni::VARCHAR,
        u.activo,
        r.nombre_rol::VARCHAR
    FROM usuario.usuario u
    INNER JOIN usuario.persona p ON u.id_persona = p.id_persona
    INNER JOIN usuario.rol r ON u.id_rol = r.id_rol
    WHERE u.id_user = p_id_usuario;
END;
$$ LANGUAGE plpgsql;
/*
In Neon, databases are stored on branches. By default, a project has one branch and one database.
You can select the branch and database to use from the drop-down menus above.

Try generating sample data and querying it by running the example statements below, or click
New Query to clear the editor.
*/
-- =====================================================
-- CREACIÓN DE TABLAS SEGÚN DER
-- PostgreSQL
-- =====================================================

-- Opcional: crear esquema
CREATE SCHEMA IF NOT EXISTS usuario;

-- =====================================================
-- TABLA: ROL
-- =====================================================
CREATE TABLE usuario.rol (
    id_rol       SERIAL PRIMARY KEY,
    nombre_rol   TEXT NOT NULL UNIQUE
);

-- =====================================================
-- TABLA: PERSONA
-- =====================================================
CREATE TABLE usuario.persona (
    id_persona   SERIAL PRIMARY KEY,
    nombre       TEXT NOT NULL,
    apellido     TEXT NOT NULL,
    dni          VARCHAR(10) NOT NULL UNIQUE
);

-- =====================================================
-- TABLA: USUARIO
-- =====================================================
CREATE TABLE usuario.usuario (
    id_user          SERIAL PRIMARY KEY,
    email            TEXT NOT NULL UNIQUE,
    password         TEXT NOT NULL,
    fecha_creacion   DATE NOT NULL DEFAULT CURRENT_DATE,
    activo           BOOLEAN NOT NULL DEFAULT TRUE,

    id_persona       INTEGER NOT NULL,
    id_rol           INTEGER NOT NULL,

    CONSTRAINT fk_usuario_persona
        FOREIGN KEY (id_persona)
        REFERENCES usuario.persona(id_persona)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_usuario_rol
        FOREIGN KEY (id_rol)
        REFERENCES usuario.rol(id_rol)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


CREATE OR REPLACE FUNCTION usuario.update_user(
    p_id_usuario INTEGER,
    p_nombre TEXT,
    p_apellido TEXT,
    p_dni VARCHAR,
    p_email TEXT,
    p_id_rol INTEGER
)
RETURNS TEXT AS $$
DECLARE
    v_id_persona INTEGER;
BEGIN
    -- 1. Validar que ningún campo obligatorio esté vacío o sea NULL
    IF p_id_usuario IS NULL OR  p_id_usuario<=0 THEN
        RAISE EXCEPTION 'Identificador de usuario inválido';
    END IF;
    
    IF p_nombre IS NULL OR TRIM(p_nombre) = '' THEN
        RAISE EXCEPTION 'El nombre no puede estar vacío';
    END IF;
    
    IF p_apellido IS NULL OR TRIM(p_apellido) = '' THEN
        RAISE EXCEPTION 'El apellido no puede estar vacío';
    END IF;
    
    IF p_dni IS NULL OR TRIM(p_dni) = '' THEN
        RAISE EXCEPTION 'El DNI no puede estar vacío';
    END IF;
    
    IF p_email IS NULL OR TRIM(p_email) = '' THEN
        RAISE EXCEPTION 'El email no puede estar vacío';
    END IF;
    
    IF p_id_rol IS NULL OR p_id_rol <= 0 THEN
        RAISE EXCEPTION 'El id del rol debe ser un número positivo';
    END IF;
    
    -- 2. Validar que el DNI no tenga más de 8 caracteres
    IF LENGTH(TRIM(p_dni)) < 8 or LENGTH(TRIM(p_dni)) > 10  THEN
        RAISE EXCEPTION 'El DNI debe tener entre 8 y 10 caracteres';
    END IF;
    
    -- 3. Verificar que el usuario exista
    SELECT id_persona INTO v_id_persona
    FROM usuario.usuario
    WHERE id_user = p_id_usuario;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Identificador de usuario inválido';
    END IF;
    
    -- 4. (Opcional) Verificar que el rol exista
    IF NOT EXISTS (SELECT 1 FROM usuario.rol WHERE id_rol = p_id_rol) THEN
        RAISE EXCEPTION 'No existe el rol con id %', p_id_rol;
    END IF;
    
    -- 5. Actualizar persona
    UPDATE usuario.persona
    SET nombre = TRIM(p_nombre),
        apellido = TRIM(p_apellido),
        dni = TRIM(p_dni)
    WHERE id_persona = v_id_persona;
    
    -- 6. Actualizar usuario
    UPDATE usuario.usuario
    SET email = TRIM(p_email),
        id_rol = p_id_rol
    WHERE id_user = p_id_usuario;
    
    -- Si todo sale bien, retornar mensaje de éxito
    RETURN 'Usuario actualizado correctamente';
    
EXCEPTION
    -- Capturar cualquier otra excepción (por ejemplo, violación de clave foránea, etc.)
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error al actualizar usuario: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;



/*
Modificación del usuario.exists_dni para que retorne una cadena vacía en caso de que no haya error y el msj
pertinente en caso de error
*/
CREATE OR REPLACE FUNCTION usuario.exists_dni(
    p_dni VARCHAR
)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    v_exists BOOLEAN;
BEGIN
    ----------------------------------------------------
    -- Validación: DNI vacío o solo espacios
    ----------------------------------------------------
    IF trim(coalesce(p_dni, '')) = '' THEN
        RETURN 'El DNI no puede ser vacío';
    END IF;

    ----------------------------------------------------
    -- Verificar existencia del DNI
    ----------------------------------------------------
    SELECT EXISTS (
        SELECT 1
        FROM usuario.persona
        WHERE dni = trim(p_dni)
    )
    INTO v_exists;

    ----------------------------------------------------
    -- Retornar según resultado
    ----------------------------------------------------
    IF v_exists THEN
        RETURN 'El DNI ya existe en la base de datos';
    ELSE
        RETURN '';   -- cadena vacía si no existe
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error en usuario.exists_dni(): %', SQLERRM;
        RETURN '';   -- ante cualquier error, retorna vacío
END;
$$;

/*
Modificación de la función usuario.exists_email para que retorne una cadena
*/
CREATE OR REPLACE FUNCTION usuario.exists_email(
    p_email VARCHAR
)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    v_existe BOOLEAN;
BEGIN
    ----------------------------------------------------
    -- Validación: email vacío o solo espacios
    ----------------------------------------------------
    IF trim(coalesce(p_email, '')) = '' THEN
        RETURN 'El email no puede ser vacío';
    END IF;

    ----------------------------------------------------
    -- Verificar existencia del email en la tabla usuario
    ----------------------------------------------------
    SELECT EXISTS (
        SELECT 1
        FROM usuario.usuario
        WHERE email = trim(p_email)
    )
    INTO v_existe;

    ----------------------------------------------------
    -- Retornar según resultado
    ----------------------------------------------------
    IF v_existe THEN
        RETURN 'El email ya existe en la base de datos';
    ELSE
        RETURN '';   -- cadena vacía si no existe
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error en usuario.exists_email(): %', SQLERRM;
        RETURN '';   -- ante cualquier error, retorna vacío
END;
$$;


/*
Código modificado de create_user
*/
CREATE OR REPLACE PROCEDURE usuario.create_user(
    p_nombre        TEXT,
    p_apellido      TEXT,
    p_dni           VARCHAR(10),
    p_email         TEXT,
    p_password      TEXT,
    p_id_rol        INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_persona    INTEGER;
    v_existe_rol    INTEGER;
BEGIN

    ----------------------------------------------------
    -- VALIDACIONES GENERALES
    ----------------------------------------------------
    IF trim(coalesce(p_nombre,'')) = '' THEN
        RAISE EXCEPTION 'El nombre no puede estar vacío';
    END IF;

    IF trim(coalesce(p_apellido,'')) = '' THEN
        RAISE EXCEPTION 'El apellido no puede estar vacío';
    END IF;

    IF trim(coalesce(p_dni,'')) = '' THEN
        RAISE EXCEPTION 'El DNI no puede estar vacío';
    END IF;

    IF trim(p_dni) !~ '^[0-9]+$' THEN
        RAISE EXCEPTION 'Ingrese sólo números al DNI';
    END IF;

    IF length(trim(p_dni)) < 8 OR length(trim(p_dni)) > 10 THEN
        RAISE EXCEPTION 'El DNI debe tener entre 8 y 10 caracteres';
    END IF;

    IF trim(coalesce(p_email,'')) = '' THEN
        RAISE EXCEPTION 'El email no puede estar vacío';
    END IF;

    IF p_email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Formato de email inválido';
    END IF;

    IF trim(coalesce(p_password,'')) = '' THEN
        RAISE EXCEPTION 'La contraseña no puede estar vacía';
    END IF;

    IF length(trim(p_password)) < 6 THEN
        RAISE EXCEPTION 'La contraseña debe tener al menos 6 caracteres';
    END IF;

    IF p_id_rol IS NULL OR p_id_rol <= 0 THEN
        RAISE EXCEPTION 'Debe indicar un id de rol válido';
    END IF;

    ----------------------------------------------------
    -- VALIDAR EXISTENCIA DEL ROL
    ----------------------------------------------------
    SELECT COUNT(*)
    INTO v_existe_rol
    FROM usuario.rol
    WHERE id_rol = p_id_rol;

    IF v_existe_rol = 0 THEN
        RAISE EXCEPTION 'Debe indicar un id de rol válido';
    END IF;

    ----------------------------------------------------
    -- INSERTAR PERSONA
    ----------------------------------------------------
    BEGIN
        INSERT INTO usuario.persona(
            nombre,
            apellido,
            dni
        )
        VALUES(
            trim(p_nombre),
            trim(p_apellido),
            trim(p_dni)
        )
        RETURNING id_persona
        INTO v_id_persona;

    EXCEPTION
        WHEN unique_violation THEN
            -- Mensaje exacto que espera la prueba
            RAISE EXCEPTION 'El DNI ya existe en base de datos';
        WHEN OTHERS THEN
            RAISE EXCEPTION 'Error al insertar persona: %', SQLERRM;
    END;

    ----------------------------------------------------
    -- INSERTAR USUARIO
    ----------------------------------------------------
    BEGIN
        INSERT INTO usuario.usuario(
            email,
            password,
            fecha_creacion,
            activo,
            id_persona,
            id_rol
        )
        VALUES(
            lower(trim(p_email)),
            p_password,
            CURRENT_DATE,
            TRUE,
            v_id_persona,
            p_id_rol
        );

    EXCEPTION
        WHEN unique_violation THEN
            RAISE EXCEPTION 'El email ya existe en base de datos';
        WHEN foreign_key_violation THEN
            RAISE EXCEPTION 'Error de clave foránea al crear usuario';
        WHEN OTHERS THEN
            RAISE EXCEPTION 'Error al insertar usuario: %', SQLERRM;
    END;

    ----------------------------------------------------
    -- FIN OK
    ----------------------------------------------------
    RAISE NOTICE 'Usuario insertado correctamente';

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'ERROR: %', SQLERRM;
        RAISE;
END;
$$;


/*
Modificación de usuario.control_update_dni
*/
CREATE OR REPLACE FUNCTION usuario.control_update_dni(
    p_id_usuario INTEGER,
    p_dni VARCHAR
)
RETURNS TEXT AS $$
DECLARE
    v_dni_clean VARCHAR;
    v_otro_usuario_exists BOOLEAN;
BEGIN
    -- 1. Validar id_usuario (nulo o <= 0)
    IF p_id_usuario IS NULL OR p_id_usuario <= 0 THEN
        RAISE EXCEPTION 'Identificador de usuario inválido';
    END IF;
    
    -- 2. Validar que el DNI no esté vacío
    IF p_dni IS NULL OR TRIM(p_dni) = '' THEN
        RAISE EXCEPTION 'El DNI no puede estar vacío';
    END IF;
    
    -- 3. Limpiar y validar longitud (entre 8 y 10 caracteres)
    v_dni_clean := TRIM(p_dni);
    IF LENGTH(v_dni_clean) < 8 OR LENGTH(v_dni_clean) > 10 THEN
        RAISE EXCEPTION 'El DNI debe tener entre 8 y 10 caracteres';
    END IF;

    IF v_dni_clean !~ '^[0-9]+$' THEN
    	RAISE EXCEPTION 'El DNI debe contener solo números';
    END IF;
    
    -- 4. Verificar si existe otro usuario (con id distinto) que tenga el mismo DNI
    SELECT EXISTS(
        SELECT 1
        FROM usuario.usuario u
        INNER JOIN usuario.persona p ON u.id_persona = p.id_persona
        WHERE p.dni = v_dni_clean
          AND u.id_user != p_id_usuario
    ) INTO v_otro_usuario_exists;
    
    -- 5. Si existe conflicto, lanzar excepción; si no, retornar cadena vacía
    IF v_otro_usuario_exists THEN
        RAISE EXCEPTION 'El DNI ya existe en la base de datos';
    ELSE
        RETURN “'';
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        -- Relanzar la excepción original (ya tiene el mensaje adecuado)
        RAISE;
END;
$$ LANGUAGE plpgsql;

/*
Modificación de usuario.control_update_email
*/
CREATE OR REPLACE FUNCTION usuario.control_update_email(
    p_id_usuario INTEGER,
    p_email TEXT
)
RETURNS TEXT AS $$
DECLARE
    v_email_clean TEXT;
    v_otro_usuario_exists BOOLEAN;
BEGIN
    -- 1. Validar que el id_usuario no sea nulo
    IF p_id_usuario IS NULL OR p_id_usuario <= 0 THEN
        RAISE EXCEPTION 'Identificador de usuario inválido';
    END IF;
    
    -- 2. Validar que el email no esté vacío
    IF p_email IS NULL OR TRIM(p_email) = '' THEN
        RAISE EXCEPTION 'El email no puede estar vacío';
    END IF;
    
    -- 3. Limpiar espacios en blanco
    v_email_clean := TRIM(p_email);
    
    -- 4. Validación rigurosa con expresión regular (estándar RFC 5322 simplificado)
    IF v_email_clean !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Formato de email inválido';
    END IF;
    
    -- 5. Verificar si existe otro usuario (con id distinto) que tenga el mismo email
    SELECT EXISTS(
        SELECT 1
        FROM usuario.usuario
        WHERE email = v_email_clean
          AND id_user != p_id_usuario
    ) INTO v_otro_usuario_exists;
    
      -- 5. Si existe conflicto, lanzar excepción; si no, retornar cadena vacía
    IF v_otro_usuario_exists THEN
        RAISE EXCEPTION 'El email ya existe en la base de datos';
    ELSE
        RETURN '';
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION SQLERRM;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION usuario.update_user(
    p_id_usuario INTEGER,
    p_nombre TEXT,
    p_apellido TEXT,
    p_dni VARCHAR,
    p_email TEXT,
    p_id_rol INTEGER
)
RETURNS TEXT AS $$
DECLARE
    v_id_persona INTEGER;
BEGIN
    -- 1. Validaciones
    IF p_id_usuario IS NULL OR p_id_usuario <= 0 THEN
        RAISE EXCEPTION 'Identificador de usuario inválido';
    END IF;

    IF p_nombre IS NULL OR TRIM(p_nombre) = '' THEN
        RAISE EXCEPTION 'El nombre no puede estar vacío';
    END IF;

    IF p_apellido IS NULL OR TRIM(p_apellido) = '' THEN
        RAISE EXCEPTION 'El apellido no puede estar vacío';
    END IF;

    IF p_dni IS NULL OR TRIM(p_dni) = '' THEN
        RAISE EXCEPTION 'El DNI no puede estar vacío';
    END IF;

    IF p_email IS NULL OR TRIM(p_email) = '' THEN
        RAISE EXCEPTION 'El email no puede estar vacío';
    END IF;

    IF (p_email) !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Formato de email inválido';
    END IF;

    IF p_id_rol IS NULL OR p_id_rol <= 0 THEN
        RAISE EXCEPTION 'Debe indicar un id de rol válido';
    END IF;

    IF LENGTH(TRIM(p_dni)) < 8 OR LENGTH(TRIM(p_dni)) > 10 THEN
        RAISE EXCEPTION 'El DNI debe tener entre 8 y 10 caracteres';
    END IF;

    -- 2. Verificar existencia del usuario
    SELECT id_persona INTO v_id_persona
    FROM usuario.usuario
    WHERE id_user = p_id_usuario;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Identificador de usuario inválido';
    END IF;

    -- 3. Verificar existencia del rol
    IF NOT EXISTS (SELECT 1 FROM usuario.rol WHERE id_rol = p_id_rol) THEN
        RAISE EXCEPTION 'Debe indicar un id de rol válido';
    END IF;

    -- 4. Actualizar persona (capturando DNI duplicado)
    BEGIN
        UPDATE usuario.persona
        SET nombre = TRIM(p_nombre),
            apellido = TRIM(p_apellido),
            dni = TRIM(p_dni)
        WHERE id_persona = v_id_persona;
    EXCEPTION
        WHEN unique_violation THEN
            RAISE EXCEPTION 'El DNI ya existe en la base de datos';
    END;

    -- 5. Actualizar usuario (capturando email duplicado)
    BEGIN
        UPDATE usuario.usuario
        SET email = TRIM(p_email),
            id_rol = p_id_rol
        WHERE id_user = p_id_usuario;
    EXCEPTION
        WHEN unique_violation THEN
            RAISE EXCEPTION 'El email ya existe en la base de datos';
        WHEN foreign_key_violation THEN
            RAISE EXCEPTION 'Error de clave foránea al crear usuario';
    END;

    -- Éxito
    RETURN '';
END;
$$ LANGUAGE plpgsql;





















Procedimientos y Funciones para los gráficos


CREATE OR REPLACE FUNCTION public.get_ventas_por_categoria_y_mes(
    p_fecha_inicio DATE,
    p_fecha_fin DATE,
    p_categoria_id INTEGER
)
RETURNS TABLE (
    mes_nombre TEXT,
    total_venta_neta NUMERIC
) AS $$
DECLARE
    v_categoria_nombre TEXT;
BEGIN
    -- Validar parámetros nulos o vacíos
    IF p_fecha_inicio IS NULL THEN
        RAISE EXCEPTION 'La fecha de inicio no puede estar vacía';
    END IF;
    
    IF p_fecha_fin IS NULL THEN
        RAISE EXCEPTION 'La fecha de fin no puede estar vacía';
    END IF;
    
    IF p_categoria_id IS NULL THEN
        RAISE EXCEPTION 'El ID de categoría no puede estar vacío';
    END IF;
    
    -- Validar que fecha_inicio sea menor o igual a fecha_fin
    IF p_fecha_inicio > p_fecha_fin THEN
        RAISE EXCEPTION 'La fecha de inicio no puede ser mayor que la fecha de fin';
    END IF;
    
    -- Verificar que la categoría exista
    SELECT category_name INTO v_categoria_nombre
    FROM dim_category
    WHERE category_id = p_categoria_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existe la categoría con ID %', p_categoria_id;
    END IF;
    
    -- Consulta principal
    RETURN QUERY
    SELECT 
        TO_CHAR(v.fecha, 'TMMonth') AS nombre_mes,
        SUM(v.venta_neta) AS total_venta
    FROM gold_ventas_interactivas v
    WHERE v.fecha BETWEEN p_fecha_inicio AND p_fecha_fin
      AND v.categoria = v_categoria_nombre
    GROUP BY DATE_TRUNC('month', v.fecha), TO_CHAR(v.fecha, 'TMMonth')
    ORDER BY DATE_TRUNC('month', v.fecha);
END;
$$ LANGUAGE plpgsql;


/*Calcula los KPIs para las ventas por meses y categorías dentro de un intervalo de tiempo*/
CREATE OR REPLACE FUNCTION public.get_kpi_categoria_y_mes(
    p_fecha_inicio DATE,
    p_fecha_fin DATE,
    p_categoria TEXT
)
RETURNS TABLE (
    promedio NUMERIC,
    maximo NUMERIC,
    minimo NUMERIC,
    mediana NUMERIC,
    desviacion_estandar NUMERIC
) AS $$
DECLARE
    v_categoria_clean TEXT;
BEGIN
    -- Validaciones
    IF p_fecha_inicio IS NULL THEN
        RAISE EXCEPTION 'La fecha de inicio no puede estar vacía';
    END IF;
    
    IF p_fecha_fin IS NULL THEN
        RAISE EXCEPTION 'La fecha de fin no puede estar vacía';
    END IF;
    
    IF p_categoria IS NULL OR TRIM(p_categoria) = '' THEN
        RAISE EXCEPTION 'El nombre de categoría no puede estar vacío';
    END IF;
    
    IF p_fecha_inicio > p_fecha_fin THEN
        RAISE EXCEPTION 'La fecha de inicio no puede ser mayor que la fecha de fin';
    END IF;
    
    v_categoria_clean := TRIM(p_categoria);
    
    -- Verificar que la categoría exista en la tabla de dimensiones (opcional pero recomendable)
    IF NOT EXISTS (SELECT 1 FROM public. gold_ventas_interactivas  WHERE categoria = v_categoria_clean) THEN
        RAISE EXCEPTION 'No existe la categoría’'
    END IF;
    
    -- Calcular estadísticas
    RETURN QUERY
    SELECT 
        ROUND(AVG(v.venta_neta)::NUMERIC, 2) AS promedio,
        ROUND(MAX(v.venta_neta)::NUMERIC, 2) AS maximo,
        ROUND(MIN(v.venta_neta)::NUMERIC, 2) AS minimo,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY v.venta_neta)::NUMERIC, 2) AS mediana,
        ROUND(STDDEV_SAMP(v.venta_neta)::NUMERIC, 2) AS desviacion_estandar
    FROM gold_ventas_interactivas v
    WHERE v.fecha BETWEEN p_fecha_inicio AND p_fecha_fin
      AND v.categoria = v_categoria_clean;
END;
$$ LANGUAGE plpgsql;
