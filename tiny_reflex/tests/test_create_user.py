import unittest
from unittest.mock import patch, MagicMock
from tiny_reflex.clases.Usuario import Usuario
import pytest
from sqlalchemy import text

class TestCreateUser(unittest.TestCase):
    """Pruebas unitarias para la clase Usuario (método create_user)."""



def test_create_user_duplicate_dni():
    """
    Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
    el dni y la excepción se levanta correctamente.
    """

    nombre = "Maria"
    apellido = "Gonzales"
    dni = "32837262"
    email="maria_gonzales@gmail.com"
    contrasenia="12345678"
    rol = 2  # Asegúrate de que este ID exista en tu BD de pruebas

    # Nota: Necesitarás adaptar `create_user` para recibir una sesión de SQLAlchemy.
    # Esto se denomina "inyección de dependencias" y es una buena práctica para pruebas.
    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    # 3. Verificar el resultado esperado
    assert "El DNI ya existe en la base de datos" in str(excinfo.value)
    #assert dni in str(excinfo.value)
    
def test_create_user_empty_name():
    """
    Prueba que permite verificar que se levanta excepción cuando se quiere insertar un usuario con nombre vacío. 
    Si la prueba es exitosa, significa que no se creo el usuario con nombre vacío y la excepción se levanta correctamente
    """
    nombre = ""
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 2  
    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    # 3. Verificar el resultado esperado
    assert "El nombre no puede estar vacío" in str(excinfo.value)
    assert nombre in str(excinfo.value)
    
def test_create_user_empty_lastname():
    """
    Prueba que permite verificar que se levanta excepción cuando se quiere insertar un usuario con apellido vacío. 
    Si la prueba es exitosa, significa que no se creo el usuario con apellido vacío y la excepción se levanta correctamente
    """
    nombre = "Maria"
    apellido = ""
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 2  

 
    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    # 3. Verificar el resultado esperado
    assert "El apellido no puede estar vacío" in str(excinfo.value)
    #assert apellido in str(excinfo.value)
    
def test_create_user_empty_password():
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = ""
    rol = 2  

 
    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    # 3. Verificar el resultado esperado
    assert "La contraseña no puede estar vacía" in str(excinfo.value)
    assert contrasenia in str(excinfo.value)
    
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
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 99

 
    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
    
    # 3. Verificar el resultado esperado
    assert "El rol indicado no existe" in str(excinfo.value)
    #assert str(rol) in str(excinfo.value)
    
def test_create_user_empty_id_rol():
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = None

 
    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
    
    # 3. Verificar el resultado esperado
    assert "Debe indicar un id de rol válido" in str(excinfo.value)
    #assert str(rol) in str(excinfo.value)
    
def test_create_user_negative_id_rol():
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = -1

 
    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
    
    # 3. Verificar el resultado esperado
    assert "Debe indicar un id de rol válido" in str(excinfo.value)
    #assert str(rol) in str(excinfo.value)
    
def test_create_user_zero_id_rol():
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 0

 
    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)
    
    # 3. Verificar el resultado esperado
    assert "Debe indicar un id de rol válido" in str(excinfo.value)
    #assert str(rol) in str(excinfo.value)

def test_create_user_empty_dni():
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = ""
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 2  

    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    # 3. Verificar el resultado esperado
    assert "El DNI no puede estar vacío" in str(excinfo.value)
    #assert nombre in str(excinfo.value)
    
def test_create_user_few_char_dni():
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "4567892"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 2  

    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    # 3. Verificar el resultado esperado
    assert "El DNI debe tener entre 8 y 10 caracteres" in str(excinfo.value)
    #assert nombre in str(excinfo.value)
    
def test_create_user_more_char_dni():
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920101"
    email = "maria_gonzales@gmail.com"
    contrasenia = "12345678"
    rol = 2  

    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    # 3. Verificar el resultado esperado
    assert "El DNI debe tener entre 8 y 10 caracteres" in str(excinfo.value)
    #assert nombre in str(excinfo.value)

def test_create_user_invalid_format_email():
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "maria_gonzalesgmail.com"
    contrasenia = "12345678"
    rol = 2  

    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    # 3. Verificar el resultado esperado
    assert "Formato de email inválido" in str(excinfo.value)
    #assert nombre in str(excinfo.value)

def test_create_user_empty_email():
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = ""
    contrasenia = "12345678"
    rol = 2  

    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    # 3. Verificar el resultado esperado
    assert "El email no puede estar vacío" in str(excinfo.value)
    #assert nombre in str(excinfo.value)

def test_create_user_repeated_email():
    # 1. Configurar los datos de prueba
    nombre = "Maria"
    apellido = "Gonzales"
    dni = "45678920"
    email = "espinoza.enrique.87@gmail.com"
    contrasenia = "12345678"
    rol = 2  

    with pytest.raises(Exception) as excinfo:
        Usuario.create_user(nombre, apellido, dni, email, contrasenia, rol)

    # 3. Verificar el resultado esperado
    assert "El email ya existe en la base de datos" in str(excinfo.value)
    #assert nombre in str(excinfo.value)
    
if __name__ == '__main__':
    unittest.main()