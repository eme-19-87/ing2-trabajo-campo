import reflex as rx
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional
from tiny_reflex.clases.Persona import Persona
from tiny_reflex.clases.Usuario import Usuario
from tiny_reflex.queries.UserQueries import UserQueries
from tiny_reflex.types import (
    UserData
)




   
        
# ===========================
# STATE DE USUARIOS
# ===========================
class UsuarioState(rx.State):
    """State para gestión de usuarios (ABM)."""
    
    # ===========================
    # DATASETS PRINCIPALES
    # ===========================
    usuarios_data: list[UserData] = []
    
    # Campos del formulario
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    password: str = ""
    confirmar_password: str = ""
    rol: str = "Analista"
    dni: str
    
    #para cargar los roles
    roles_disponibles: list[dict] = []
    roles_loading: bool = False
    
    # Control de edición
    editando_id: Optional[int] = None
    
    # Mensajes y feedback
    mensaje: str = ""
    tipo_mensaje: str = "success"  # "success" o "error"
    
    # Opciones para selectores
    opciones_roles: list[dict] = [
        {"label": "Administrador", "value": 1},
        {"label": "Analista", "value": 2},
    ]
    
    # ===========================
    # FLAGS DE ESTADO
    # ===========================
    loading_usuarios: bool = False
    saving_usuario: bool = False
    deleting_usuario: bool = False
    
    # ===========================
    # ID SECUENCIAL SIMULADO (para demo sin BD)
    # ===========================
    next_id: int = 1
    

    
    # ===========================
    # PROPIEDADES DERIVADAS
    # ===========================
    @rx.var
    def has_usuarios(self) -> bool:
        return len(self.usuarios_data) > 0
    
    @rx.var
    def is_editando(self) -> bool:
        return self.editando_id is not None
    
    @rx.var
    def titulo_formulario(self) -> str:
        return "Editar Usuario" if self.is_editando else "Alta de Usuario"
    
    @rx.var
    def texto_boton(self) -> str:
        return "Actualizar Usuario" if self.is_editando else "Registrar Usuario"
    
   
    @rx.event
    def cancelar_edicion(self):
        """Cancela la edición y limpia el formulario."""
        self._limpiar_formulario()
        self.mensaje = ""
    
    @rx.event
    def limpiar_mensaje(self):
        """Limpia el mensaje mostrado."""
        self.mensaje = ""
    
    @rx.event
    def set_rol(self, value: str):
        """Actualiza el rol seleccionado."""
        self.rol = value
        
    
    
   
        
    def control_insert_user(self):
        """Verifica si algún campo obligatorio está en blanco y muestra toast."""
        try:
            mjs=Usuario.control_format(self.email,self.dni,self.nombre,self.apellido,self.password)
            if len(mjs)>0:
                return rx.toast.error(mjs, position="top-right")
        
        
        # Si todos los campos están completos
            return rx.toast.success("✅ Todos los campos están completos", position="top-right")
        except Exception as e:
            return rx.toast.success(f"Se ha producido un error: {e}", position="top-right")
    
    from tiny_reflex.queries.UserQueries import UserQueries


    
    
    @rx.event
    async def cargar_roles(self):
        """Carga los roles desde la base de datos."""
        self.roles_loading = True
        
        try:
            # Ejecutar la consulta en un hilo separado
            roles = await rx.run_in_thread(UserQueries.get_roles)
            
            self.roles_disponibles = roles
            rx.toast.error(f"roles: {roles}", position="top-right")
            # Si hay roles y el rol actual no está seleccionado, seleccionar el primero
            if roles and not self.rol:
                self.rol = roles[0]["nombre_rol"]
                
        except Exception as e:
            rx.toast.error(f"Error al cargar roles: {e}", position="top-right")
        
        self.roles_loading = False
    
    # Convertir roles al formato que espera el Select de Reflex
    @rx.var
    def opciones_roles_select(self) -> list:
        """Convierte los roles de BD al formato del select."""
        return [
            rol["nombre_rol"]
            for rol in self.roles_disponibles
        ]
        