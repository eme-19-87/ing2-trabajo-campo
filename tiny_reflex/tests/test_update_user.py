import unittest
from unittest.mock import patch, MagicMock
from tiny_reflex.clases.Usuario import Usuario
from tiny_reflex.clases.Rol import Rol
import pytest
from sqlalchemy import text

class TestUpdateUser(unittest.TestCase):
    """Pruebas unitarias para la clase Usuario (método create_user)."""



def test_person_exist_email():
      # 1. Configurar los datos de prueba
      nombre = "Juan"
      apellido = "Perez"
      dni = "32837262"
      email = "espinoza.enrique.87@gmail.com"
      password = "secreto123"
      rol_id = 2  # Asegúrate de que este ID exista en tu BD de pruebas
      resultado=Usuario.control_email(email)
      assert isinstance(resultado, bool)
      assert resultado is False

def test_person_not_exist_email():
      # 1. Configurar los datos de prueba
      nombre = "Juan"
      apellido = "Perez"
      dni = "30876123"
      email = "prueba@email.com"
      password = "secreto123"
      rol_id = 2  # Asegúrate de que este ID exista en tu BD de pruebas
      resultado=Usuario.control_email(email)
      assert isinstance(resultado, bool)
      assert resultado is True



def test_update_user_duplicate_dni():
    """
    Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
    el dni y la excepción se levanta correctamente.
    """
    id_usuario=2
    nombre = "Juan"
    apellido = "Perez"
    dni = "32837262"
    email = "prueba@email.com"
    password = "secreto123"
    rol_id = 2  # Asegúrate de que este ID exista en tu BD de pruebas

    usuario=Usuario(id_usuario,nombre,apellido,dni,email,password,password,Rol(rol_id,"Analista"))
    with pytest.raises(Exception) as excinfo:
        usuario.update_user(id_usuario,nombre,apellido,dni,email,rol_id)

    # 3. Verificar el resultado esperado
    assert "El DNI ya existe en la base de datos" in str(excinfo.value)
    #assert dni in str(excinfo.value)
    
def test_update_user_duplicate_email():
    """
    Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
    el dni y la excepción se levanta correctamente.
    """
    id_usuario=2
    nombre = "Juan"
    apellido = "Perez"
    dni = "32845262"
    email = "espinoza.enrique.87@gmail.com"
    password = "secreto123"
    rol_id = 2  # Asegúrate de que este ID exista en tu BD de pruebas

    usuario=Usuario(id_usuario,nombre,apellido,dni,email,password,password,Rol(rol_id,"Analista"))
    with pytest.raises(Exception) as excinfo:
        usuario.update_user(id_usuario,nombre,apellido,dni,email,rol_id)

    # 3. Verificar el resultado esperado
    assert "El email ya existe en la base de datos" in str(excinfo.value)
    #assert dni in str(excinfo.value)

def test_update_user_empty_email():
    """
    Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
    el dni y la excepción se levanta correctamente.
    """
    id_usuario=2
    nombre = "Juan"
    apellido = "Perez"
    dni = "32845262"
    email = ""
    password = "secreto123"
    rol_id = 2  # Asegúrate de que este ID exista en tu BD de pruebas

    usuario=Usuario(id_usuario,nombre,apellido,dni,email,password,password,Rol(rol_id,"Analista"))
    with pytest.raises(Exception) as excinfo:
        usuario.update_user(id_usuario,nombre,apellido,dni,email,rol_id)

    # 3. Verificar el resultado esperado
    assert "El email no puede estar vacío" in str(excinfo.value)
    #assert dni in str(excinfo.value)
    
def test_update_user_bad_format_email():
    """
    Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
    el dni y la excepción se levanta correctamente.
    """
    id_usuario=2
    nombre = "Juan"
    apellido = "Perez"
    dni = "32845262"
    email = "espinoza.enrique.87gmail.com"
    password = "secreto123"
    rol_id = 2  # Asegúrate de que este ID exista en tu BD de pruebas

    usuario=Usuario(id_usuario,nombre,apellido,dni,email,password,password,Rol(rol_id,"Analista"))
    with pytest.raises(Exception) as excinfo:
        usuario.update_user(id_usuario,nombre,apellido,dni,email,rol_id)

    # 3. Verificar el resultado esperado
    assert "Formato de email inválido" in str(excinfo.value)
    #assert dni in str(excinfo.value)
    
if __name__ == '__main__':
    unittest.main()
  