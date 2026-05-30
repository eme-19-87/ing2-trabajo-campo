import re
import reflex as rx
from tiny_reflex.queries.UserQueries import UserQueries


class Rol:
    """Clase encargada de la lógica de los roles de usuario."""

    def __init__(self, id_rol: int, nombre_rol: str) -> None:
        """
        Constructor de Rol.

        Args:
            id_rol: Identificador único del rol.
            nombre_rol: Nombre descriptivo del rol (ej. "admin", "usuario").
        """
        self.id_rol = id_rol      # Usa el setter para validar
        self.nombre_rol = nombre_rol

    # ------------------------------------------------------------------
    # Propiedades y setters
    # ------------------------------------------------------------------

    @property
    def id_rol(self) -> int:
        """Getter del id_rol."""
        return self._id_rol

    @id_rol.setter
    def id_rol(self, value: int) -> None:
        self._id_rol = value

    @property
    def nombre_rol(self) -> str:
        """Getter del nombre_rol."""
        return self._nombre_rol

    @nombre_rol.setter
    def nombre_rol(self, value: str) -> None:
        self._nombre_rol = value.strip()

    # ------------------------------------------------------------------
    # Métodos estáticos originales
    # ------------------------------------------------------------------

    @staticmethod
    def get_roles() -> list[dict]:
        """
        Permite obtener los roles de los usuarios.

        Raises:
            e: Mensaje de error en caso de que ocurra alguna excepción,
               por ejemplo, que no se pueda recuperar la información de los roles.

        Returns:
            list[dict]: Retorna una lista de diccionarios con los datos de los roles.
        """
        try:
            roles = UserQueries.get_roles()
            return roles
        except Exception as e:
            raise e

    # ------------------------------------------------------------------
    # Representación string
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return f"Rol(id={self.id_rol}, nombre={self.nombre_rol})"
        
    
    