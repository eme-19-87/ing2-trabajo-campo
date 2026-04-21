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
            dni_exist=True
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

            if Persona.control_dni(dni):
                msj+=Usuario.control_email(email)
            else:
                msj+="El dni debe tener 8 dígitos como mínimo sin puntos. Si el error persiste, es posible que el dni ingresado ya figure para otro usuario"
            
            if len(msj)==0:
                msj+=Usuario.create_user(nombre,apellido,dni,email,contrasenia,rol)
            
            return msj
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