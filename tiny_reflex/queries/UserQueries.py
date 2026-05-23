from tiny_reflex.db_connection import get_engine
from sqlalchemy import text
import bcrypt

from typing import List, Dict



class UserQueries:
    
    @staticmethod
    def get_all_users() -> List[Dict]:
        """
        Permite recuperar todos los datos de los usuarios desde la base de datos. Recupera la información tanto del usuario como
        de la persona asociada a ese usuario.
    
        Return: Retorna una lista con los datos del usuario y los datos de la persona
        """
    
        try:
            engine = get_engine()
            
            with engine.connect() as conn:
                # Ejecutar la función que retorna TABLE
                result = conn.execute(
                    text("SELECT * FROM usuario.get_all_users()")
                )
                
                # Convertir resultados a lista de diccionarios
                users = []
                for row in result:
                    users.append({
                        "id_usuario": row[0],
                        "email": row[1],
                        "nombre": row[2],
                        "apellido": row[3],
                        "dni": row[4],
                        "activo": row[5],
                        "nombre_rol": row[6]
                    })
                
                return users
                
        except Exception as e:
            raise Exception(f"Error al obtener usuarios: {e}")
    
    @staticmethod
    def exists_email(email: str) -> bool:
        """
        Verifica si el email ya existe en la tabla de usuario

        Args:
            email (str): El email del usuario

        Raises:
            Exception: Eleva una excepción en caso

        Returns:
            bool: _description_
        """
        try:
            engine = get_engine()
            
            with engine.connect() as conn:
                result = conn.execute(
                    text("SELECT usuario.exists_email(:p_email)"),
                    {"p_email": email}
                )
                exists = result.scalar()
                return exists if exists is not None else False
                
        except Exception as e:
            raise Exception(f"Error al verificar DNI: {e}")
        
    def encrypt_password(password: str) -> str:
        """Encripta una contraseña usando bcrypt."""
        # Generar salt y encriptar la contraseña
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica si una contraseña en texto plano coincide con su versión encriptada."""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
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
                    encrypted_password = UserQueries.encrypt_password(password)
                    result = conn.execute(
                        text("CALL usuario.create_user(:p_nombre, :p_apellido, :p_dni, :p_email, :p_password, :p_id_rol)"),
                        {
                            "p_nombre": nombre,
                            "p_apellido": apellido,
                            "p_dni": dni,
                            "p_email": email,
                            "p_password": encrypted_password,
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