#from tiny_reflex.queries.Personqueries import
from tiny_reflex.queries.Personqueries import Personaqueries
class Persona:
    """Clase que representa una persona con validación de DNI."""

    def __init__(self, nombre: str, apellido: str, dni: str) -> None:
        """
        Constructor de Persona.

        Args:
            nombre: Nombre de la persona.
            apellido: Apellido de la persona.
            dni: Documento nacional de identidad.
        """
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni   # Usa el setter para validar

    @property
    def nombre(self) -> str:
        """Getter del nombre."""
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        self._nombre = value.strip()

    @property
    def apellido(self) -> str:
        """Getter del apellido."""
        return self._apellido

    @apellido.setter
    def apellido(self, value: str) -> None:
        self._apellido = value.strip()

    @property
    def dni(self) -> str:
        """Getter del DNI."""
        return self._dni

    @dni.setter
    def dni(self, value: str) -> None:
        self._dni = value.strip()

    @staticmethod
    def control_dni(dni: str) -> str:
        """
        Controla que el DNI no exista en la base de datos.

        Parameters:
            dni: String. Indica el DNI de la persona.

        Returns:
            bool: Retorna True si el DNI **no existe** en la tabla de persona
                  (es decir, está disponible). Retorna False si ya existe.
        """
        exist_dni = Personaqueries.exists_dni(dni)
        return exist_dni   # True = disponible, False = ya existe
    
    @staticmethod
    def control_update_dni(id_usuario:int,dni: str) -> str:
        """
        Controla que el DNI no exista en la base de datos.

        Parameters:
            dni: String. Indica el DNI de la persona.

        Returns:
            bool: Retorna True si el DNI **no existe** en la tabla de persona
                  (es decir, está disponible). Retorna False si ya existe.
        """
        dni_available= Personaqueries.control_update_dni(id_usuario,dni)
        return  dni_available  # True = disponible, False = ya existe
    

    def __str__(self) -> str:
        """Representación legible de la persona."""
        return f"{self.nombre} {self.apellido} (DNI: {self.dni})"