from tiny_reflex.db_connection import get_engine
from sqlalchemy import text
class Personaqueries:
    @staticmethod
    def exists_dni(dni: str) -> bool:
        """
            Verifica la existencia del dni invocando una función en la base de datos
        Args:
            dni (str): El dni que quiere verificarse

        Raises:
            Exception: Eleva una excepción en caso de error. Por ejemplo, si el dni ya existe en la base de datos.

        Returns:
            bool: Retorna true en caso que el dni exista. Retorna false en caso contrario.
        """
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