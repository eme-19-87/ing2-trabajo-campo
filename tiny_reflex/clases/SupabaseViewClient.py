import json
from typing import List,Dict
import os
from supabase import create_client, Client
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.exc import DBAPIError

load_dotenv()


class SupabaseViewClient:
    def __init__(self):
        self.__supabase_key= os.getenv("SUPABASE_KEY")
        self.__supabase_url=os.getenv("SUPABASE_URL")
        self.__client_connection:Client = create_client(self.__supabase_url, self.__supabase_key)
        

    @property
    def supabase_url(self) -> str:
        return self.__supabase_url

    @supabase_url.setter
    def supabase_url(self, value: str):
        self.__supabase_url = value

    @property
    def supabase_key(self) -> str:
        return self.__supabase_key

    @supabase_key.setter
    def supabase_key(self, value: str):
        self.__supabase_key = value

    @property
    def client_connection(self) -> object:
        return self.__client_connection

    @client_connection.setter
    def client_connection(self, value: object):
        self.__client_connection = value
        
    def get_ventas_por_categoria_y_mes(self, filtros: json) -> List[Dict]:
        """
        Llama a la función SQL get_ventas_por_categoria_y_mes.
        filtros: dict con claves 'fecha_inicio', 'fecha_fin', 'categoria'
        """
        try:
            try:
                filtros_dict = json.loads(filtros)
            except json.JSONDecodeError as e:
                raise Exception(f"El filtro no es un JSON válido: {e}") from e
                # 1. Extraer parámetros
            fecha_inicio = filtros_dict.get("fecha_inicio")
            fecha_fin = filtros_dict.get("fecha_fin")
            categoria= filtros_dict.get("categoria", "")

        

            # 3. Llamar a la función RPC
            params = {
                "p_fecha_inicio": fecha_inicio,
                "p_fecha_fin": fecha_fin,
                "p_categoria": categoria
            }
            print(params)
            result = self.client_connection.rpc("get_ventas_por_categoria_y_mes", params).execute()
            #print(result.data)
            # 4. Retornar la lista de diccionarios
            return result.data  # [{"mes_nombre": "Enero", "total_venta_neta": 1234.56}, ...]
        
        
        except DBAPIError as e:
            # Para errores de base de datos (incluye RAISE EXCEPTION)
            # El mensaje original suele estar en e.orig.args[0]
            
            if e.orig and len(e.orig.args) > 0:
               
                raw = str(e.orig.args[0])
                msj_limpio = raw.split('\n')[0]
                
            else:
               
                msj_limpio = str(e.message)
            raise Exception(msj_limpio) from e
    
        finally:
            pass
    
    def get_kpi_categoria_y_mes(self, filtros: str) -> List[Dict]:
        """
        Llama a la función SQL get_ventas_por_categoria_y_mes.
        filtros: string JSON con claves 'fecha_inicio', 'fecha_fin', 'categoria'
        """
        try:
            filtros_dict = json.loads(filtros)
        except json.JSONDecodeError as e:
            raise Exception(f"El filtro no es un JSON válido: {e}") from e

        try:
            fecha_inicio = filtros_dict.get("fecha_inicio")
            fecha_fin = filtros_dict.get("fecha_fin")
            categoria = filtros_dict.get("categoria", "")

            params = {
                "p_fecha_inicio": fecha_inicio,
                "p_fecha_fin": fecha_fin,
                "p_categoria": categoria
            }
            result = self.client_connection.rpc("get_kpi_categoria_y_mes", params).execute()
            return result.data

        except DBAPIError as e:
            if e.orig and len(e.orig.args) > 0:
                error_msg = str(e.orig.args[0])
            else:
                error_msg = str(e)
            raise Exception(error_msg) from e
        
    

    def obtener_categorias(self)->List:
        try:
           
            response = self.client_connection.table("gold_ventas_interactivas").select("categoria").execute()
            categorias_unicas = list(set(row["categoria"] for row in response.data))
            categorias_unicas.insert(0, "Ninguna")
            return categorias_unicas
        except Exception as e:
            raise e
        



    # Engine SQLAlchemy (para pandas.read_sql)
    def get_engine():
        database_url = os.getenv("SUPABASE_DATABASE_URL")
        if not database_url:
            raise ValueError("SUPABASE_DATABASE_URL no está configurada en el archivo .env")
        return create_engine(database_url)