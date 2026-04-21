"""Application state management."""


import reflex as rx
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional
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
        
        
    def verificar_campos_en_blanco(self):
        """Verifica si algún campo obligatorio está en blanco y muestra toast."""
        
        if not self.nombre or not self.nombre.strip():
            return rx.toast.error("❌ El campo Nombre está vacío", position="top-right")
        
        if not self.apellido or not self.apellido.strip():
            return rx.toast.error("❌ El campo Apellido está vacío", position="top-right")
        
        if not self.dni or not self.dni.strip():
            return rx.toast.error("❌ El campo DNI está vacío", position="top-right")
        
        if not self.email or not self.email.strip():
            return rx.toast.error("❌ El campo Email está vacío", position="top-right")
        
        if not self.password or not self.password.strip():
            return rx.toast.error("❌ El campo Contraseña está vacío", position="top-right")
        
        if not self.confirmar_password or not self.confirmar_password.strip():
            return rx.toast.error("❌ El campo Repetir Contraseña está vacío", position="top-right")
        
        # Si todos los campos están completos
        return rx.toast.success("✅ Todos los campos están completos", position="top-right")