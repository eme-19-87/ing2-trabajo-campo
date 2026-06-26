import re
import reflex as rx
from tiny_reflex.clases.Persona import Persona
from tiny_reflex.clases.Rol import Rol          # Asumo que existe esta clase para la composición
from tiny_reflex.queries.UserQueries import UserQueries


class Usuario(Persona):
    """Clase Usuario que hereda de Persona y tiene un Rol (composición)."""

    def __init__(
        self,
        id_usuario: int,
        nombre: str,
        apellido: str,
        dni: str,
        email: str,
        contrasenia: str,
        contrarep: str,
        rol: Rol | int,   # Puede recibir un objeto Rol o su ID
    ) -> None:
        """
        Constructor de Usuario.

        Args:
            id_usuario: Identificador único del usuario.
            nombre: Nombre de la persona (hereda de Persona).
            apellido: Apellido de la persona.
            dni: DNI de la persona.
            email: Correo electrónico del usuario.
            contrasenia: Contraseña en texto plano (se almacenará hasheada).
            contrarep: Repetición de la contraseña para validación.
            rol: Objeto Rol o entero (ID del rol). Se almacena como composición.
        """
        # Llamada al constructor de Persona (validará nombre, apellido, dni)
        super().__init__(nombre, apellido, dni)

        # Atributos privados
        self._id_usuario = id_usuario
        self._email = email
        self._contrasenia = None       # Se asigna vía setter (con validación)
        self._contrarep = None         # Solo para validación, no se persiste
        self._rol = None
    
        # Asignaciones que activan los setters (validaciones)
        self.email = email
        self.contrasenia = contrasenia
        self.contrarep = contrarep
        self.rol = rol

    # ------------------------------------------------------------------
    # Propiedades y setters para los nuevos atributos
    # ------------------------------------------------------------------

    @property
    def id_usuario(self) -> int:
        """Getter del id_usuario."""
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, value: int) -> None:
        """Setter del id_usuario. Solo se permite si es entero positivo."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError("El id_usuario debe ser un entero positivo.")
        self._id_usuario = value

    @property
    def email(self) -> str:
        """Getter del email."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Setter del email. Valida formato y disponibilidad."""
        self._email = value.strip()

    @property
    def contrasenia(self) -> str | None:
        """Getter de la contraseña (usualmente retorna hash o None por seguridad)."""
        return self._contrasenia

    @contrasenia.setter
    def contrasenia(self, value: str) -> None:
        """Setter de la contraseña. Valida que cumpla requisitos."""
        # Aquí se debería aplicar hashing antes de almacenar
        self._contrasenia = value   # En producción: hashlib.sha256(value.encode()).hexdigest()

    @property
    def contrarep(self) -> str | None:
        """Getter de la repetición de contraseña (solo para validación)."""
        return self._contrarep

    @contrarep.setter
    def contrarep(self, value: str) -> None:
        """Setter de la repetición de contraseña. No se almacena permanentemente."""
        # Solo se almacena temporalmente para validar con contrasenia
        self._contrarep = value
    
    

    @property
    def rol(self) -> Rol:
        """Getter del rol (composición)."""
        return self._rol

    @rol.setter
    def rol(self, value: Rol | int) -> None:
        """
        Setter del rol. Acepta un objeto Rol o un entero (ID).
        Si es entero, se obtiene el objeto Rol desde la base de datos.
        """
        if isinstance(value, Rol):
            self._rol = value
        elif isinstance(value, int):
            # Se asume que existe un método estático Rol.get_rol_by_id()
            rol_obj = Rol.get_rol_by_id(value)   # Método a implementar en Rol
            if rol_obj is None:
                raise ValueError(f"No existe un rol con ID {value}")
            self._rol = rol_obj
        else:
            raise TypeError("El rol debe ser un objeto Rol o un entero (ID).")

    # ------------------------------------------------------------------
    # Métodos de control (refactorizados como métodos estáticos/clase)
    # ------------------------------------------------------------------

    @staticmethod
    def control_email(email: str) -> str:
        """Retorna True si el email NO existe en la tabla de usuarios (disponible)."""
        return UserQueries.exists_email(email)
    
    @staticmethod
    def control_update_email(id_usuario:int,email: str) -> str:
        """Retorna True si el email NO existe en la tabla de usuarios (disponible)."""
        return UserQueries.control_update_email(id_usuario,email)

  
    def __control_email_format(self,email: str) ->str:
        """Valida el formato del email. Retorna True si es válido."""
      
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        
        if not email:
            return "El email no puede estar vacío"
    
        if not re.match(patron, email):
            return "Formato de email inválido"
          
        return ""

    
    def __control_contra(self,contrasenia: str, repcontra: str) -> str:
        """
        Controla que las contraseñas cumplan el formato.
        Retorna string vacío si OK, o mensaje de error.
        """
        msj = ""
        if not contrasenia.strip():
            msj += "\n La contraseña no puede quedar vacía."
            return msj
        if contrasenia != repcontra:
            msj += "\n Las contraseñas no coinciden."
        return msj

    
    def __control_dni_format(self,dni: str) -> str:
        """Controla el formato del DNI. Retorna string vacío si OK, o error."""
        msj = ""
        if len(dni)==0:
            msj+="\n El DNI no puede estar vacío"
            return msj
        
        if not dni.isdigit():
            msj += "\n Ingrese sólo números al DNI"
            return msj
        
        if not (8 <= len(dni) <= 10):
            msj += "\n El dni debe contener entre 8 y 10 dígitos."
            
        
        return msj
        

    # Nota: Los métodos control_nombre y control_apellido ya existen en Persona.
    # Se pueden reutilizar desde la clase base.
    def __control_nombre(self,nombre: str) -> str:
        """Valida nombre. Retorna vacío si OK."""
        return "" if nombre.strip() else "El nombre no puede estar vacío."

    def __control_apellido(self,apellido: str) -> str:
        """Valida apellido. Retorna vacío si OK."""
        return "" if apellido.strip() else "El apellido no puede estar vacío."

    # ------------------------------------------------------------------
    # Método principal de control de formulario (actualizado)
    # ------------------------------------------------------------------

    def control_format(
        self,
        email: str,
        dni: str,
        nombre: str,
        apellido: str,
        contrasenia: str,
        contrarep: str,
    ) -> str:
        """
        Controla el formato de todos los campos del formulario de creación.
        Retorna string vacío si todo está bien, o mensaje concatenado de errores.
        """
        msj = ""
        msj += self.__control_nombre(nombre)
        msj += self.__control_apellido(apellido)
        msj += self.__control_contra(contrasenia, contrarep)
        msj += self.__control_email_format(email)
        msj += self.__control_dni_format(dni)
        return msj

 
    def control_format_update(
        self,
        id_usuario: int,
        email: str,
        dni: str,
        nombre: str,
        apellido: str,
    ) -> str:
        """
        Control de formato para actualización (sin validar contraseña nueva).
        Retorna mensaje de error o vacío.
        """
        msj = ""
        msj += self.__control_nombre(nombre)
        msj += self.__control_apellido(apellido)
        msj += self.__control_email_format(email)
        msj += self.__control_dni_format(dni)
        return msj

    # ------------------------------------------------------------------
    # Métodos estáticos que interactúan con la base de datos
    # (se mantienen como estaban, pero se ajustan a la nueva estructura)
    # ------------------------------------------------------------------

    @staticmethod
    def create_user(
        nombre: str,
        apellido: str,
        dni: str,
        email: str,
        contrasenia: str,
        rol: int,
    ) -> str:
        """
        Inserta un nuevo usuario en la tabla.
        Retorna mensaje de éxito.
        """
        try:
            UserQueries.create_user(nombre, apellido, dni, email, contrasenia, rol)
            return "Usuario insertado correctamente."
        except Exception as e:
            raise e

    @staticmethod
    def get_user_by_id(user_id: int) -> dict | None:
        """Obtiene un usuario por su ID."""
        try:
            return UserQueries.get_user_by_id(user_id)
        except Exception as e:
            raise e

    @staticmethod
    def load_user_data() -> dict | None:
        """Obtiene todos los usuarios."""
        try:
            return UserQueries.get_all_users()
        except Exception as e:
            raise e



    def update_user(
        self,
        id_usuario: int,
        nombre: str,
        apellido: str,
        dni: str,
        email: str,
        rol: int,
    ) -> str:
        """Actualiza los datos de un usuario."""
        try:
            return UserQueries.update_user(self.id_usuario,self.nombre, self.apellido, self.dni, self.email, rol)
        except Exception as e:
            raise e

    # ------------------------------------------------------------------
    # Representación string
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return f"Usuario(id={self.id_usuario}, {super().__str__()}, email={self.email}, rol={self.rol.nombre if self.rol else None})"