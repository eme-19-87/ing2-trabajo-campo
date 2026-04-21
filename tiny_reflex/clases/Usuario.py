import re
import reflex as rx
from tiny_reflex.clases.Persona import Persona
from tiny_reflex.queries.UserQueries import UserQueries
class Usuario:
    """Clase encargada de lógica de usuarios"""

    def control_email(email: str) -> str:
        return not UserQueries.exists_email(email)
    
    @staticmethod
    def control_format(
        email: str,
        dni: str,
        nombre: str,
        apellido: str,
        contrasenia: str,
        rol: int,
        contrarep: str
    ) -> str:
        try:
            msj=Usuario.control_form(email,dni,nombre,apellido,contrasenia,rol,contrarep)
            return msj
        except Exception as e:
            raise e
        
    
    def control_form(email: str,
        dni: str,
        nombre: str,
        apellido: str,
        contrasenia: str,
        rol: int,
        contrarep: str)->str:
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
    def create_user(
        nombre,
        apellido,
        dni,
        email,
        contrasenia,
        rol
    )->str:
        try:
            UserQueries.create_user(nombre,apellido,dni,email,contrasenia,rol)
            return "Usuario insertado correctamente."
        except Exception as e:
            raise e