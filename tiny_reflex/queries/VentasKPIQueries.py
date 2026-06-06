
import pandas as pd
from typing import cast
from tiny_reflex.db_supabase_connection import get_engine,get_supabase
from tiny_reflex.clases.VistaVentasKPI import VistaVentasKPI
from typing import List
import json
def consultar_vista_ventas(filtros:json) -> list[VistaVentasKPI]:
    """Load customers data from database."""
    try:
        #engine = get_engine()
        #query = "SELECT * FROM gold_ventas_interactivasLIMIT 1"
        #df = pd.read_sql(query, engine)
        #records = df.to_dict("records")
        #return cast(list[VistaVentasKPI], records)
          # Consulta: SELECT * FROM gold_ventas_interactivas LIMIT 1
        supabase=get_supabase()
        response = supabase.table("gold_ventas_interactivas").select("*").limit(1).execute()
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

def load_sales(json: json) -> list[VistaVentasKPI]:
    """Load customers data from database."""
    try:
        #engine = get_engine()
        #query = "SELECT * FROM gold_ventas_interactivasLIMIT 1"
        #df = pd.read_sql(query, engine)
        #records = df.to_dict("records")
        #return cast(list[VistaVentasKPI], records)
          # Consulta: SELECT * FROM gold_ventas_interactivas LIMIT 1
        supabase=get_supabase()
        response = supabase.table("gold_ventas_interactivas").select("*").limit(1).execute()
        records = response.data
        
        instancias = [VistaVentasKPI(**record) for record in records]
        return instancias
    except Exception as e:
        print(f"Error loading customers: {e}")
        return []
    
def load_calendary() -> list[VistaVentasKPI]:
    """Load customers data from database."""
    try:
        #engine = get_engine()
        #query = "SELECT * FROM gold_ventas_interactivasLIMIT 1"
        #df = pd.read_sql(query, engine)
        #records = df.to_dict("records")
        #return cast(list[VistaVentasKPI], records)
          # Consulta: SELECT * FROM gold_ventas_interactivas LIMIT 1
        supabase=get_supabase()
        response = supabase.table("gold_calendario").select("*").limit(1).execute()
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
    
def obtener_estados()->List:
    try:
        supabase = get_supabase()
        response = supabase.table("gold_ventas_interactivas").select("estado_pedido").execute()
        estados_unicos = list(set(row["estado_pedido"] for row in response.data))
        return estados_unicos
    except Exception as e:
        raise e

def obtener_categorias()->List:
    try:
        supabase = get_supabase()
        response = supabase.table("gold_ventas_interactivas").select("categoria").execute()
        estados_unicos = list(set(row["categoria"] for row in response.data))
        return estados_unicos
    except Exception as e:
        raise e
    