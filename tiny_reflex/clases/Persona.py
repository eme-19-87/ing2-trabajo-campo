class Persona:
    """Clase encargada de validar DNI"""

    @staticmethod
    def control_dni(dni: str) -> bool:
        return dni.isdigit() and len(dni) >= 7
