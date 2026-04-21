#from tiny_reflex.queries.Personqueries import
from tiny_reflex.queries.Personqueries import Personaqueries
class Persona:
    """Clase encargada de validar DNI"""

    @staticmethod
    def control_dni(dni: str) -> bool:
        exist_dni=Personaqueries.exists_dni(dni)
        return  not exist_dni
