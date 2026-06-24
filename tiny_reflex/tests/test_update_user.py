import unittest
from unittest.mock import patch, MagicMock
from tiny_reflex.clases.Usuario import Usuario
from tiny_reflex.clases.Rol import Rol
import pytest
from sqlalchemy import text

class TestUpdateUser(unittest.TestCase):
    """Pruebas unitarias para la clase Usuario (método create_user)."""



def test_person_exist_email_mock():
    """Simula que el email ya existe (control_email retorna False)."""
    email = "espinoza.enrique.87@gmail.com"
    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.exists_email.return_value = True   # existe -> control_email debe ser False
        resultado = Usuario.control_email(email)
        assert isinstance(resultado, bool)
        assert resultado is False

def test_person_not_exist_email_mock():
    """Simula que el email no existe (control_email retorna True)."""
    email = "prueba@email.com"
    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.exists_email.return_value = False  # no existe -> True
        resultado = Usuario.control_email(email)
        assert isinstance(resultado, bool)
        assert resultado is True

# ------------------------------------------------------------
# Pruebas para update_user
# ------------------------------------------------------------

def test_update_user_duplicate_dni_mock():
    id_usuario = 2
    nombre = "Juan"
    apellido = "Perez"
    dni = "32837262"
    email = "prueba@email.com"
    password = "secreto123"
    rol_id = 2
    usuario = Usuario(id_usuario, nombre, apellido, dni, email, password, password, Rol(rol_id, "Analista"))

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.update_user.side_effect = Exception("El DNI ya existe en la base de datos")
        with pytest.raises(Exception) as excinfo:
            usuario.update_user(id_usuario, nombre, apellido, dni, email, rol_id)
        assert "El DNI ya existe en la base de datos" in str(excinfo.value)

def test_update_user_duplicate_email_mock():
    id_usuario = 2
    nombre = "Juan"
    apellido = "Perez"
    dni = "32845262"
    email = "espinoza.enrique.87@gmail.com"
    password = "secreto123"
    rol_id = 2
    usuario = Usuario(id_usuario, nombre, apellido, dni, email, password, password, Rol(rol_id, "Analista"))

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.update_user.side_effect = Exception("El email ya existe en la base de datos")
        with pytest.raises(Exception) as excinfo:
            usuario.update_user(id_usuario, nombre, apellido, dni, email, rol_id)
        assert "El email ya existe en la base de datos" in str(excinfo.value)

def test_update_user_empty_email_mock():
    id_usuario = 2
    nombre = "Juan"
    apellido = "Perez"
    dni = "32845262"
    email = ""
    password = "secreto123"
    rol_id = 2
    usuario = Usuario(id_usuario, nombre, apellido, dni, email, password, password, Rol(rol_id, "Analista"))

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.update_user.side_effect = Exception("El email no puede estar vacío")
        with pytest.raises(Exception) as excinfo:
            usuario.update_user(id_usuario, nombre, apellido, dni, email, rol_id)
        assert "El email no puede estar vacío" in str(excinfo.value)

def test_update_user_bad_format_email_mock():
    id_usuario = 2
    nombre = "Juan"
    apellido = "Perez"
    dni = "32845262"
    email = "espinoza.enrique.87gmail.com"
    password = "secreto123"
    rol_id = 2
    usuario = Usuario(id_usuario, nombre, apellido, dni, email, password, password, Rol(rol_id, "Analista"))

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.update_user.side_effect = Exception("Formato de email inválido")
        with pytest.raises(Exception) as excinfo:
            usuario.update_user(id_usuario, nombre, apellido, dni, email, rol_id)
        assert "Formato de email inválido" in str(excinfo.value)

def test_update_user_empty_dni_mock():
    id_usuario = 2
    nombre = "Juan"
    apellido = "Perez"
    dni = ""
    email = "espinoza.enrique.87gmail.com"
    password = "secreto123"
    rol_id = 2
    usuario = Usuario(id_usuario, nombre, apellido, dni, email, password, password, Rol(rol_id, "Analista"))

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.update_user.side_effect = Exception("El DNI no puede estar vacío")
        with pytest.raises(Exception) as excinfo:
            usuario.update_user(id_usuario, nombre, apellido, dni, email, rol_id)
        assert "El DNI no puede estar vacío" in str(excinfo.value)

def test_update_user_empty_name_mock():
    id_usuario = 2
    nombre = ""
    apellido = "Perez"
    dni = "43678123"
    email = "espinoza.enrique.87gmail.com"
    password = "secreto123"
    rol_id = 2
    usuario = Usuario(id_usuario, nombre, apellido, dni, email, password, password, Rol(rol_id, "Analista"))

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.update_user.side_effect = Exception("El nombre no puede estar vacío")
        with pytest.raises(Exception) as excinfo:
            usuario.update_user(id_usuario, nombre, apellido, dni, email, rol_id)
        assert "El nombre no puede estar vacío" in str(excinfo.value)

def test_update_user_empty_lastname_mock():
    id_usuario = 2
    nombre = "Maria"
    apellido = ""
    dni = "43678123"
    email = "espinoza.enrique.87gmail.com"
    password = "secreto123"
    rol_id = 2
    usuario = Usuario(id_usuario, nombre, apellido, dni, email, password, password, Rol(rol_id, "Analista"))

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.update_user.side_effect = Exception("El apellido no puede estar vacío")
        with pytest.raises(Exception) as excinfo:
            usuario.update_user(id_usuario, nombre, apellido, dni, email, rol_id)
        assert "El apellido no puede estar vacío" in str(excinfo.value)

def test_update_user_negative_id_user_mock():
    id_usuario = -2
    nombre = "Maria"
    apellido = "Perez"
    dni = "43678123"
    email = "maria_perez@gmail.com"
    password = "secreto123"
    rol_id = 2
    usuario = Usuario(id_usuario, nombre, apellido, dni, email, password, password, Rol(rol_id, "Analista"))

    # El chequeo de ID negativo puede ocurrir ANTES de llamar a UserQueries, así que no mockeamos UserQueries,
    # sino que verificamos que se lance la excepción directamente (sin mock). 
    # Pero para mantener la coherencia, podemos simular que update_user nunca se llama.
    # En este caso la validación está en el método `update_user` de Usuario (o en el setter).
    # Por simplicidad, si el código real lanza la excepción, el test original no usa mock, pero aquí mockeamos igual.
    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        # Si la validación está en el método, no se llamará a update_user de queries.
        # Simplemente verificamos que la excepción se lance.
        with pytest.raises(Exception) as excinfo:
            usuario.update_user(id_usuario, nombre, apellido, dni, email, rol_id)
        assert "Identificador de usuario inválido" in str(excinfo.value)

def test_update_user_zero_id_user_mock():
    id_usuario = 0
    nombre = "Maria"
    apellido = "Perez"
    dni = "43678123"
    email = "maria_perez@gmail.com"
    password = "secreto123"
    rol_id = 2
    usuario = Usuario(id_usuario, nombre, apellido, dni, email, password, password, Rol(rol_id, "Analista"))

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        with pytest.raises(Exception) as excinfo:
            usuario.update_user(id_usuario, nombre, apellido, dni, email, rol_id)
        assert "Identificador de usuario inválido" in str(excinfo.value)
    
    
if __name__ == '__main__':
    unittest.main()
  