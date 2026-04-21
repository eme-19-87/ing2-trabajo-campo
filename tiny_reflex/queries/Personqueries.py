from tiny_reflex.db_connection import get_engine
from sqlalchemy import text
class Personaqueries:
    @staticmethod
    def exists_dni(dni: str) -> bool:
        """Verifica si un DNI ya existe usando la función exists_dni_func."""
        try:
            engine = get_engine()
            
            with engine.connect() as conn:
                result = conn.execute(
                    text("SELECT usuario.exists_dni(:p_dni)"),
                    {"p_dni": dni}
                )
                exists = result.scalar()
                return exists if exists is not None else False
                
        except Exception as e:
            raise Exception(f"Error al verificar DNI: {e}")