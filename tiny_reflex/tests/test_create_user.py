import unittest
from unittest.mock import patch, MagicMock
from tiny_reflex.clases.Usuario import Usuario
import pytest
from sqlalchemy import text

class TestCreateUser(unittest.TestCase):
    """Pruebas unitarias para la clase Usuario (método create_user)."""


def test_create_user_duplicate_dni():
    """
    Prueba unitaria que simula un DNI duplicado usando mock.
    Verifica que Usuario.create_user propaga la excepción con el mensaje correcto.
    """
    # Datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "32837262"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 2

    # Configurar el mock de UserQueries.create_user
    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        # Crear el mock del método create_user
        mock_create_user = MockUserQueries.create_user
        # Simular que la base de datos lanza una excepción por DNI duplicado
        mock_create_user.side_effect = Exception("El DNI ya existe en la base de datos")

        # Llamar a Usuario.create_user y esperar la excepción
        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

        # Verificar el mensaje de la excepción
        assert "El DNI ya existe en la base de datos" in str(excinfo.value)
    
def test_create_user_empty_name():
    """
    Prueba unitaria que simula un nombre vacío usando mock.
    Verifica que Usuario.create_user propaga la excepción con el mensaje adecuado.
    """
    nombre = ""
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 2

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        mock_create_user = MockUserQueries.create_user
        # Simular que la base de datos lanza excepción por nombre vacío
        mock_create_user.side_effect = Exception("El nombre no puede estar vacío")

        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    


def test_create_user_empty_lastname():
    """
    Prueba unitaria con mock que simula un apellido vacío.
    Verifica que Usuario.create_user propaga la excepción correcta.
    """
    nombre = "Maria"
    apellido = ""
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 2

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        # Configuramos el método create_user para que lance la excepción
        MockUserQueries.create_user.side_effect = Exception("El apellido no puede estar vacío")

        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

        assert "El apellido no puede estar vacío" in str(excinfo.value)
    
def test_create_user_empty_password_mock():
    """
    Prueba unitaria con mock que simula una contraseña vacía.
    Verifica que Usuario.create_user propaga la excepción correcta.
    """
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = ""
    rol = 2

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.create_user.side_effect = Exception("La contraseña no puede estar vacía")

        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

        assert "La contraseña no puede estar vacía" in str(excinfo.value)
    
def test_create_user_few_char_password():
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12"
    rol = 2  

 
    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    # 3. Verificar el resultado esperado
    assert "La contraseña debe tener al menos 6 caracteres" in str(excinfo.value)
    #assert contrasenia in str(excinfo.value)
    
def test_create_user_not_exist_id_rol():
    """
    Prueba unitaria con mock que simula un rol inexistente.
    Verifica que Usuario.create_user propaga la excepción correcta.
    """
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 99

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.create_user.side_effect = Exception("El rol indicado no existe")

        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

        assert "El rol indicado no existe" in str(excinfo.value)
    
    


def test_create_user_empty_id_rol_mock():
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = None

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.create_user.side_effect = Exception("Debe indicar un id de rol válido")
        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
        assert "Debe indicar un id de rol válido" in str(excinfo.value)

def test_create_user_negative_id_rol():
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = -1

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.create_user.side_effect = Exception("Debe indicar un id de rol válido")
        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
        assert "Debe indicar un id de rol válido" in str(excinfo.value)

def test_create_user_zero_id_rol():
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 0

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.create_user.side_effect = Exception("Debe indicar un id de rol válido")
        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
        assert "Debe indicar un id de rol válido" in str(excinfo.value)

def test_create_user_empty_dni():
    nombre = "Maria"
    apellido = "Gonzales"
    dni = ""
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 2

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.create_user.side_effect = Exception("El DNI no puede estar vacío")
        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
        assert "El DNI no puede estar vacío" in str(excinfo.value)

def test_create_user_few_char_dni():
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "4567892"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 2

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.create_user.side_effect = Exception("El DNI debe tener entre 8 y 10 caracteres")
        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
        assert "El DNI debe tener entre 8 y 10 caracteres" in str(excinfo.value)

def test_create_user_more_char_dni():
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920101"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 2

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.create_user.side_effect = Exception("El DNI debe tener entre 8 y 10 caracteres")
        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
        assert "El DNI debe tener entre 8 y 10 caracteres" in str(excinfo.value)

def test_create_user_invalid_format_email():
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzalesgmail.com"
    contrasenia = "12345678"
    rol = 2

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.create_user.side_effect = Exception("Formato de email inválido")
        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
        assert "Formato de email inválido" in str(excinfo.value)

def test_create_user_empty_email():
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = ""
    contrasenia = "12345678"
    rol = 2

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.create_user.side_effect = Exception("El email no puede estar vacío")
        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
        assert "El email no puede estar vacío" in str(excinfo.value)

def test_create_user_repeated_email():
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "espinoza.enrique.87@gmail.com"
    contrasenia = "12345678"
    rol = 2

    with patch("tiny_reflex.clases.Usuario.UserQueries") as MockUserQueries:
        MockUserQueries.create_user.side_effect = Exception("El email ya existe en la base de datos")
        with pytest.raises(Exception) as excinfo:
            Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
        assert "El email ya existe en la base de datos" in str(excinfo.value)
    
if __name__ == '__main__':
    unittest.main()