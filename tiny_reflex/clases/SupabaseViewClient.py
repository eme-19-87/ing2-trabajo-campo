from tiny_reflex.clases.VistaVentasKPI import VistaVentasKPI
import json
from typing import List,Dict, Any
from sqlalchemy.engine import Engine
import os
from supabase import create_client, Client
from sqlalchemy import create_engine
from dotenv import load_dotenv

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
        
    def consultar_vista_ventas(self,filtros:json) -> list[VistaVentasKPI]:
    
        try:
            #engine = get_engine()
            #query = "SELECT * FROM gold_ventas_interactivasLIMIT 1"
            #df = pd.read_sql(query, engine)
            #records = df.to_dict("records")
            #return cast(list[VistaVentasKPI], records)
            # Consulta: SELECT * FROM gold_ventas_interactivas LIMIT 1
            
            supabase = self.__client_connection
            query = supabase.table("gold_ventas_interactivas").select(
                "order_item_id", "producto", "categoria", "ciudad", "estado_pedido",
                "segmento", "venta_bruta", "venta_neta", "descuento_porcentaje",
                "descuento_valor", "fecha", "nombre_cliente", "pais", "cantidad"
            )

            if filtros.get("fecha_inicio"):
                query = query.gte("fecha", filtros["fecha_inicio"])
            if filtros.get("fecha_fin"):
                query = query.lte("fecha", filtros["fecha_fin"])
            if filtros.get("categoria") and filtros["categoria"].strip():
                query = query.eq("categoria", filtros["categoria"])
            if filtros.get("estado") and filtros["estado"].strip():
                query = query.eq("estado_pedido", filtros["estado"])
            records = query.data
            
            # Convierte cada diccionario en una instancia de VistaVentasKPI
            # Asumiendo que tu clase acepta los mismos nombres de campos en __init__
            #instancias = [VistaVentasKPI(**record) for record in records]
            
            # Si necesitas el cast (aunque ya es list[VistaVentasKPI] gracias a la comprensión)
            #return cast(List[VistaVentasKPI], instancias)
            return records
        except Exception as e:
            print(f"Error loading customers: {e}")
            return []

    def load_sales(self,json: json) -> list[VistaVentasKPI]:
        """Load customers data from database."""
        try:
            #engine = get_engine()
            #query = "SELECT * FROM gold_ventas_interactivasLIMIT 1"
            #df = pd.read_sql(query, engine)
            #records = df.to_dict("records")
            #return cast(list[VistaVentasKPI], records)
            # Consulta: SELECT * FROM gold_ventas_interactivas LIMIT 1
            
            response = self.client_connection.table("gold_ventas_interactivas").select("*").limit(1).execute()
            records = response.data
            
            instancias = [VistaVentasKPI(**record) for record in records]
            return instancias
        except Exception as e:
            print(f"Error loading customers: {e}")
            return []
    
    def load_calendary(self) -> list[VistaVentasKPI]:
        """Load customers data from database."""
        try:
            #engine = get_engine()
            #query = "SELECT * FROM gold_ventas_interactivasLIMIT 1"
            #df = pd.read_sql(query, engine)
            #records = df.to_dict("records")
            #return cast(list[VistaVentasKPI], records)
            # Consulta: SELECT * FROM gold_ventas_interactivas LIMIT 1
            
            response = self.client_connection.table("gold_calendario").select("*").limit(1).execute()
            records = response.data
            
            # Convierte cada diccionario en una instancia de VistaVentasKPI
            # Asumiendo que tu clase acepta los mismos nombres de campos en __init__
            #instancias = [VistaVentasKPI(**record) for record in records]
            
            # Si necesitas el cast (aunque ya es list[VistaVentasKPI] gracias a la comprensión)
            #return cast(List[VistaVentasKPI], instancias)
            return records
        except Exception as e:
            print(f"Error loading customers: {e}")
            return []
        
    def obtener_estados(self)->List:
        try:
          
            response = self.client_connection.table("gold_ventas_interactivas").select("estado_pedido").execute()
            estados_unicos = list(set(row["estado_pedido"] for row in response.data))
            return estados_unicos
        except Exception as e:
            raise e

    def obtener_categorias(self)->List:
        try:
           
            response = self.client_connection.table("gold_ventas_interactivas").select("categoria").execute()
            estados_unicos = list(set(row["categoria"] for row in response.data))
            return estados_unicos
        except Exception as e:
            raise e
        



    # Engine SQLAlchemy (para pandas.read_sql)
    def get_engine():
        database_url = os.getenv("SUPABASE_DATABASE_URL")
        if not database_url:
            raise ValueError("SUPABASE_DATABASE_URL no está configurada en el archivo .env")
        return create_engine(database_url)