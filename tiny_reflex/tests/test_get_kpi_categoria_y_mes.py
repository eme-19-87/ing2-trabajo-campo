import unittest
from unittest.mock import patch, MagicMock
from tiny_reflex.clases.SupabaseViewClient import SupabaseViewClient
import pytest
from sqlalchemy import text

class TestKpiCategoryMonth(unittest.TestCase):

    def test_get_data_ok(self):
        """
        Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
        el dni y la excepción se levanta correctamente.
        """

        filtros={
            "categoria":"Accessories",
            "fecha_inicio":"1/1/2015",
            "fecha_fin":"10/6/2026"
        }
        supa=SupabaseViewClient()
        resultado=[]
        resultado=supa.get_kpi_categoria_y_mes(filtros)

        # 3. Verificar el resultado esperado
        assert len(resultado)>0
        #assert dni in str(excinfo.value)
        
    def test_empty_category(self):
        """
        Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
        el dni y la excepción se levanta correctamente.
        """

        filtros={
            "categoria":"",
            "fecha_inicio":"1/1/2015",
            "fecha_fin":"10/6/2026"
        }
        supa=SupabaseViewClient()
        resultado=[]
        with pytest.raises(Exception) as excinfo:
            resultado=supa.get_kpi_categoria_y_mes(filtros)

        # 3. Verificar el resultado esperado
        assert "El nombre de categoría no puede estar vacío" in str(excinfo.value)
        #assert dni in str(excinfo.value)
    
    def test_empty_initial_date(self):
        """
        Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
        el dni y la excepción se levanta correctamente.
        """

        filtros={
            "categoria":"Accessories",
            "fecha_inicio":None,
            "fecha_fin":"10/6/2026"
        }
        supa=SupabaseViewClient()
        resultado=[]
        with pytest.raises(Exception) as excinfo:
            resultado=supa.get_kpi_categoria_y_mes(filtros)

        # 3. Verificar el resultado esperado
        assert "La fecha de inicio no puede estar vacía" in str(excinfo.value)
        #assert dni in str(excinfo.value)
    
    def test_empty_final_date(self):
        """
        Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
        el dni y la excepción se levanta correctamente.
        """

        filtros={
            "categoria":"Accessories",
            "fecha_inicio":"1/1/2015",
            "fecha_fin":None
        }
        supa=SupabaseViewClient()
        resultado=[]
        with pytest.raises(Exception) as excinfo:
            resultado=supa.get_kpi_categoria_y_mes(filtros)

        # 3. Verificar el resultado esperado
        assert "La fecha de fin no puede estar vacía" in str(excinfo.value)
        #assert dni in str(excinfo.value)
        
    def test_final_date_lt_initial_date(self):
        """
        Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
        el dni y la excepción se levanta correctamente.
        """

        filtros={
            "categoria":"Accessories",
            "fecha_inicio":"6/21/2026",
            "fecha_fin":"6/20/2026"
        }
        supa=SupabaseViewClient()
        resultado=[]
        with pytest.raises(Exception) as excinfo:
            resultado=supa.get_kpi_categoria_y_mes(filtros)

        # 3. Verificar el resultado esperado
        assert "La fecha de inicio no puede ser mayor que la fecha de fin" in str(excinfo.value)
        #assert dni in str(excinfo.value)
    
    def test_no_data_in_range_date(self):
        """
        Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
        el dni y la excepción se levanta correctamente.
        """

        filtros={
            "categoria":"Accessories",
            "fecha_inicio":"6/20/2026",
            "fecha_fin":"6/21/2026"
        }
        supa=SupabaseViewClient()
        resultado=[]
    
        # 3. Verificar el resultado esperado
        assert len(resultado)==0
        #assert dni in str(excinfo.value)
    
    def test_invalid_category(self):
        """
        Prueba que permite verificar si hay un dni duplicado. Si la prueba es exitosa, significa que sí está duplicado
        el dni y la excepción se levanta correctamente.
        """

        filtros={
            "categoria":"UNNE",
            "fecha_inicio":"1/1/2015",
            "fecha_fin":"10/6/2026"
        }
        supa=SupabaseViewClient()
        resultado=[]
        with pytest.raises(Exception) as excinfo:
            resultado=supa.get_kpi_categoria_y_mes(filtros)

        # 3. Verificar el resultado esperado
        assert "No existe la categoría" in str(excinfo.value)
        #assert dni in str(excinfo.value)