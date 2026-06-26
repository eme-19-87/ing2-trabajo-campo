from tiny_reflex.db_connection import get_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
class Personaqueries:
    @staticmethod
    def exists_dni(dni: str) -> str:
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
                return exists if len(exists)==0 else exists
                
        except DBAPIError as e:
            # Obtener solo el mensaje primario (sin CONTEXT, HINT, etc.)
            if e.orig and hasattr(e.orig, 'diag') and e.orig.diag is not None:
                error_msg = e.orig.diag.message_primary
            elif e.orig and len(e.orig.args) > 0:
                # Fallback: primer argumento (suele ser el mensaje completo)
                error_msg = str(e.orig.args[0]).split('\nCONTEXT:')[0]  # truncar manualmente
            else:
                error_msg = str(e)
            raise Exception(error_msg) from e
        
    @staticmethod
    def control_update_dni(id_usuario:int,dni: str) -> str:
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
                    text("SELECT usuario.control_update_dni(:p_id_usuario,:p_dni)"),
                    {"p_id_usuario":id_usuario, "p_dni": dni}
                )
                exists = result.scalar()
                return exists if len(exists)>0 else exists
                
        except DBAPIError as e:
            # Obtener solo el mensaje primario (sin CONTEXT, HINT, etc.)
            if e.orig and hasattr(e.orig, 'diag') and e.orig.diag is not None:
                error_msg = e.orig.diag.message_primary
            elif e.orig and len(e.orig.args) > 0:
                # Fallback: primer argumento (suele ser el mensaje completo)
                error_msg = str(e.orig.args[0]).split('\nCONTEXT:')[0]  # truncar manualmente
            else:
                error_msg = str(e)
            raise Exception(error_msg) from e