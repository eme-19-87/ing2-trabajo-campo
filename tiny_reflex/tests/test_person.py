import unittest
from unittest.mock import patch, MagicMock
from tiny_reflex.clases.Persona import Persona
import pytest
from sqlalchemy import text

class TestCreateUser(unittest.TestCase):
    """Pruebas unitarias para la clase Usuario (método create_user)."""



def test_person_exist_dni():
      # 1. Configurar los datos de prueba
      id_usuario=35
      dni="32837262"
      with pytest.raises(Exception) as excinfo:
            Persona.control_update_dni(id_usuario,dni)

     # 3. Verificar el resultado esperado
      assert "El DNI ya existe en la base de datos" in str(excinfo.value)

def test_person_not_exist_dni():
     
      id_usuario=34
      dni="32837262"
      with pytest.raises(Exception) as excinfo:
            Persona.control_update_dni(id_usuario,dni)
      assert "" in str(excinfo.value)
      
def test_person_empty_dni():
     
      id_usuario=34
      dni=""
      with pytest.raises(Exception) as excinfo:
            Persona.control_update_dni(id_usuario,dni)
      assert "" in str(excinfo.value)
      
if __name__ == '__main__':
    unittest.main()
  
   