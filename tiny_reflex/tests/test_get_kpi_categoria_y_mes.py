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
        """Simula categoría vacía -> la función SQL lanza excepción."""
        filtros = {
            "categoria": "",
            "fecha_inicio": "1/1/2015",
            "fecha_fin": "10/6/2026"
        }
        supa = SupabaseViewClient()
        # Mock del método rpc.execute() para que lance una excepción con el mensaje esperado
        with patch.object(supa.client_connection, "rpc") as mock_rpc:
            mock_execute = MagicMock()
            mock_execute.execute.side_effect = Exception("El nombre de categoría no puede estar vacío")
            mock_rpc.return_value = mock_execute

            with pytest.raises(Exception) as excinfo:
                supa.get_kpi_categoria_y_mes(filtros)
            assert "El nombre de categoría no puede estar vacío" in str(excinfo.value)

    def test_empty_initial_date(self):
        filtros = {
            "categoria": "Accessories",
            "fecha_inicio": None,
            "fecha_fin": "10/6/2026"
        }
        supa = SupabaseViewClient()
        with patch.object(supa.client_connection, "rpc") as mock_rpc:
            mock_rpc.return_value.execute.side_effect = Exception("La fecha de inicio no puede estar vacía")
            with pytest.raises(Exception) as excinfo:
                supa.get_kpi_categoria_y_mes(filtros)
            assert "La fecha de inicio no puede estar vacía" in str(excinfo.value)

    def test_empty_final_date(self):
        filtros = {
            "categoria": "Accessories",
            "fecha_inicio": "1/1/2015",
            "fecha_fin": None
        }
        supa = SupabaseViewClient()
        with patch.object(supa.client_connection, "rpc") as mock_rpc:
            mock_rpc.return_value.execute.side_effect = Exception("La fecha de fin no puede estar vacía")
            with pytest.raises(Exception) as excinfo:
                supa.get_kpi_categoria_y_mes(filtros)
            assert "La fecha de fin no puede estar vacía" in str(excinfo.value)

    def test_final_date_lt_initial_date(self):
        filtros = {
            "categoria": "Accessories",
            "fecha_inicio": "6/21/2026",
            "fecha_fin": "6/20/2026"
        }
        supa = SupabaseViewClient()
        with patch.object(supa.client_connection, "rpc") as mock_rpc:
            mock_rpc.return_value.execute.side_effect = Exception("La fecha de inicio no puede ser mayor que la fecha de fin")
            with pytest.raises(Exception) as excinfo:
                supa.get_kpi_categoria_y_mes(filtros)
            assert "La fecha de inicio no puede ser mayor que la fecha de fin" in str(excinfo.value)

    def test_no_data_in_range_date(self):
        """Simula consulta sin datos -> la función SQL retorna lista vacía."""
        filtros = {
            "categoria": "Accessories",
            "fecha_inicio": "6/20/2026",
            "fecha_fin": "6/21/2026"
        }
        supa = SupabaseViewClient()
        with patch.object(supa.client_connection, "rpc") as mock_rpc:
            mock_rpc.return_value.execute.return_value = MagicMock(data=[])
            resultado = supa.get_kpi_categoria_y_mes(filtros)
            assert len(resultado) == 0

    def test_invalid_category(self):
        filtros = {
            "categoria": "UNNE",
            "fecha_inicio": "1/1/2015",
            "fecha_fin": "10/6/2026"
        }
        supa = SupabaseViewClient()
        with patch.object(supa.client_connection, "rpc") as mock_rpc:
            mock_rpc.return_value.execute.side_effect = Exception("No existe la categoría")
            with pytest.raises(Exception) as excinfo:
                supa.get_kpi_categoria_y_mes(filtros)
            assert "No existe la categoría" in str(excinfo.value)