import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Obtener las credenciales del archivo .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Crear el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase() -> Client:
    """Retorna el cliente de Supabase para usar en toda la aplicación."""
    return supabase