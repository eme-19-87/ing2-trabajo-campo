import os
from supabase import create_client, Client
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Cliente REST (para operaciones que no requieren SQL directo)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase() -> Client:
    return supabase

# Engine SQLAlchemy (para pandas.read_sql)
def get_engine():
    database_url = os.getenv("SUPABASE_DATABASE_URL")
    if not database_url:
        raise ValueError("SUPABASE_DATABASE_URL no está configurada en el archivo .env")
    return create_engine(database_url)