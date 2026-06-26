from tiny_reflex.clases.SupabaseViewClient import SupabaseViewClient
from tiny_reflex.clases.Usuario import Usuario
import json
from typing import List,Dict

class DashboardController:
    def __init__(self):
        self.__filtros_activos=None
        self.__supabase_view_client=SupabaseViewClient()
      

    @property   
    def filtros_activos(self) -> json:
        return self.__filtros_activos

    @filtros_activos.setter
    def filtros_activos(self, value: json):
        self.__filtros_activos = value
        
    @property   
    def supabase_view_client(self) -> SupabaseViewClient:
        return self.__supabase_view_client

    @supabase_view_client.setter
    def supabase_view_client(self, value: SupabaseViewClient):
        self.__supabase_view_client = value
        

       
    def aplicar_filtros(self,filtros:json):
        self.filtros_activos= filtros

    def get_ventas_por_categoria_y_mes(self)->List[Dict]:
        try:
            
            resultado=self.supabase_view_client.get_ventas_por_categoria_y_mes(self.filtros_activos)
            if not resultado:  # Verifica si la lista está vacía
                raise Exception("No hay datos para los criterios de filtro establecidos")
            return resultado
        except Exception as e:
            if hasattr(e, 'message'):
                raise Exception(e.message) from e
            else:
                raise Exception(str(e)) from e
        finally:
            pass
    
    def get_kpi_por_categoria_y_mes(self)->List[Dict]:
        try:
            resultado=self.supabase_view_client.get_kpi_categoria_y_mes(self.filtros_activos)
            if not resultado:  # Verifica si la lista está vacía
                raise Exception("No hay datos para los criterios de filtro establecidos")
            return resultado
        except Exception as e:
            if hasattr(e, 'message'):
                raise Exception(e.message) from e
            else:
                raise Exception(str(e)) from e
        finally:
            pass
   
    
    def obtener_categorias(self)->List:
        try:
            return self.supabase_view_client.obtener_categorias()
        except Exception as e:
            raise e
        finally:
            pass