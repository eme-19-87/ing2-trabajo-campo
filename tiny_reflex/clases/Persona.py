#from tiny_reflex.queries.Personqueries import
from tiny_reflex.queries.Personqueries import Personaqueries
class Persona:
    """Clase encargada de validar DNI"""

    @staticmethod
    def control_dni(dni: str) -> bool:

        """Controla que el dni no exista en la base de datos
        
        parameters:
        
        dni: String. Indica el dni de la persona.

        Returns:
           bool: Retorna True si el dni ya existe en la tabla de persona
        """
        exist_dni=Personaqueries.exists_dni(dni)
        return  not exist_dni
