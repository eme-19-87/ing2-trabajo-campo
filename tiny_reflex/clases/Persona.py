#from tiny_reflex.queries.Personqueries import
class Persona:
    """Clase encargada de validar DNI"""

    @staticmethod
    def control_dni(dni: str) -> bool:
        return dni.isdigit() and (len(dni) >=8 and len(dni)<=10)
