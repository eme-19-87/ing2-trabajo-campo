import re
from tiny_reflex.clases.Persona import Persona
from tiny_reflex.queries.UserQueries import UserQueries
class Usuario:
    """Clase encargada de lógica de usuarios"""

    def control_email(email: str) -> str:
        return ""
    
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
            msj=""
            dni_exist=False
            if not nombre.strip():
                msj="El nombre no puede quedar vacío."

            if not apellido.strip():
                msj+="\nEl apellido no puede quedar vacío."

            if not contrasenia.strip():
                msj+="\n La contraseña no puede quedar vacía."

            patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(patron, email):
                msj+="\n Ingrese un email válido."
            
            if not dni.strip() or len(dni)<8:
                msj+="\n Ingrese un dni válido con 8 caracteres mínimo con sólo números."
                
            if contrasenia!=contrarep:
                msj+="\n Las contraseñas no coinciden."

            if len(msj)==0:
                dni_exist=Persona.control_dni(dni)
            
            if not dni_exist:
                msj=Usuario.control_email(email)
            else:
                msj="El dni que se quiere ingresar corresponde a otro usuario."
            
            if len(msj)==0:
                Usuario.create_user(nombre,apellido,dni,email,contrasenia,rol)
        except Exception as e:
            raise e
        
            

 
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