from tiny_reflex.db_connection import get_engine
from sqlalchemy import text

class UserQueries:
    @staticmethod
    def create_user(
        nombre: str,
        apellido: str,
        dni: str,
        email: str,
        password: str,
        rol: int  # "Administrador" o "Analista"
    ) -> bool:
        """Llama al procedimiento almacenado create_user."""
        
        
        try:
            engine = get_engine()
            
            with engine.connect() as conn:
                with conn.begin() as trans:  # Context manager automático
                    result = conn.execute(
                        text("CALL usuario.create_user(:p_nombre, :p_apellido, :p_dni, :p_email, :p_password, :p_id_rol)"),
                        {
                            "p_nombre": nombre,
                            "p_apellido": apellido,
                            "p_dni": dni,
                            "p_email": email,
                            "p_password": password,
                            "p_id_rol": rol
                        }
                    )
                    
                    return True
                    
        except Exception as e:
            print(f"{e}")
            raise Exception(f"Error al ingresar el nuevo usuario: {e}")
        

    @staticmethod
    def get_roles() -> list[dict]:
        """Obtiene los roles desde la base de datos usando la función get_roles()"""
        try:
            engine = get_engine()
            
            with engine.connect() as conn:
                # Ejecutar la función y obtener resultados
                result = conn.execute(
                    text("SELECT * FROM usuario.get_roles()")
                )
              
                
                # Convertir resultados a lista de diccionarios
                roles = []
                for row in result:
                    roles.append({
                        "id_rol": row[0],  # id_rol
                        "nombre_rol": row[1]  # nombre_rol
                    })
                
                return roles
                
        except Exception as e:
            raise Exception(f"Error al obtener los roles: {e}")