from tiny_reflex.queries.VentasKPIQueries import load_sales,load_calendary

def test_supabase_connection():
    try:
        # Para ejecutarlo en terminal: python -m pytest tiny_reflex/tests/test_supabase_connection.py
        
        
        print("✅ Conexión exitosa. Datos obtenidos:", load_sales())
        return True
    except Exception as e:
        print("❌ Error de conexión:", e)
        return False

if __name__ == "__main__":
    test_supabase_connection()
