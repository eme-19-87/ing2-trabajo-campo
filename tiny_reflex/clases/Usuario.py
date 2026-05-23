import re
import reflex as rx
from tiny_reflex.clases.Persona import Persona
from tiny_reflex.queries.UserQueries import UserQueries
class Usuario:
    """Clase encargada de lógica de usuarios"""

    def control_email(email: str) -> bool:
        """Controla que si el email existe en la tabla de usuarios

        Args:
            email (str): El email del usuario

        Returns:
            bool: Retorna true si el email existe
        """
        return not UserQueries.exists_email(email)
    
    @staticmethod
    def control_format(email: str,dni: str,nombre: str,apellido: str,contrasenia: str,rol: int,contrarep: str) -> str:
        """Permite el control de los datos para insertar correctamente al nuevo usuario

        Args:
            email (str): El email del usuario
            dni (str): El dni de la persona
            nombre (str): El nombre de la persona
            apellido (str): El apellido de la persona
            contrasenia (str): La contraseña de la persona que se encriptará antes del ingreso
            rol (int): Determina el rol del usuario
            contrarep (str): Repetición de la contraseña para verificar que esta esté correcta

        Raises:
            e: Mensaje de error en caso de que ocurra alguna excepción. Por ejemplo, que el email ya exista en la base de datos.

        Returns:
            str: Retorna vacío si no hay error o el mensaje de error en caso contrario.
        """
        try:

            msj=Usuario.control_form(email,dni,nombre,apellido,contrasenia,rol,contrarep)
            return msj
        except Exception as e:
            raise e
        
    
    def control_form(email: str,dni: str,nombre: str,apellido: str,contrasenia: str,rol: int,contrarep: str)->str:
            """Controla el formato de los campos provenientes del formulario

            Args:
                Args:
                email (str): El email del usuario
                dni (str): El dni de la persona
                nombre (str): El nombre de la persona
                apellido (str): El apellido de la persona
                contrasenia (str): La contraseña de la persona que se encriptará antes del ingreso
                rol (int): Determina el rol del usuario
                contrarep (str): Repetición de la contraseña para verificar que esta esté correcta

            Raises:
                e: Mensaje de error en caso de que ocurra alguna excepción. Por ejemplo, que el email ya exista en la base de datos.

            Returns:
                str: Retorna vacío si no hay error o el mensaje de error en caso contrario.
            """
            msj=""
            if not nombre.strip():
                msj+="El nombre no puede quedar vacío."

            if not apellido.strip():
                msj+="\nEl apellido no puede quedar vacío."

            if not contrasenia.strip():
                msj+="\n La contraseña no puede quedar vacía."

            patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(patron, email):
                msj+="\n Ingrese un email válido."
            
                
            if contrasenia!=contrarep:
                msj+="\n Las contraseñas no coinciden."
            
            if not dni.isdigit():
                msj+="\n Ingrese sólo números al dni"
                
            if not (len(dni) >=8 and len(dni)<=10):
                msj+="\n El dni debe contener entre 8 y 10 dígitos."
                
            return msj

    @staticmethod
    def create_user(nombre,apellido,dni,email,contrasenia,rol)->str:
        """
        Permite insertar el usuario en la tabla de usuarios

         Args:
                Args:
                email (str): El email del usuario
                dni (str): El dni de la persona
                nombre (str): El nombre de la persona
                apellido (str): El apellido de la persona
                contrasenia (str): La contraseña de la persona que se encriptará antes del ingreso
                rol (int): Determina el rol del usuario

            Raises:
                e: Mensaje de error en caso de que ocurra alguna excepción. Por ejemplo, que el email ya exista en la base de datos.

            Returns:
                str: Retorna un mensaje de éxito para indicar que se insertó correctamente.
        """
        try:
            UserQueries.create_user(nombre,apellido,dni,email,contrasenia,rol)
            return "Usuario insertado correctamente."
        except Exception as e:
            raise e