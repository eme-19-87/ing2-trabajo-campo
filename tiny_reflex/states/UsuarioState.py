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
    

    
    # ===========================
    # FLAGS DE ESTADO
    # ===========================
    loading_usuarios: bool = False
    saving_usuario: bool = False
    deleting_usuario: bool = False
    
    

    
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
    def set_rol(self, value: str):
        """Actualiza el rol seleccionado."""
        self.rol = value
        
    

        
    def control_format(self):
        """Verifica si algún campo obligatorio está en blanco y muestra toast."""
        try:
            mjs=Usuario.control_format(self.email,self.dni,self.nombre,self.apellido,self.password,1,self.confirmar_password)
            if len(mjs)>0:
                return rx.toast.error(mjs, position="center")
        
        
        # Si todos los campos están completos
            return rx.toast.success("✅ Todos los campos están completos", position="top-right")
        except Exception as e:
            return rx.toast.error(f"Se ha producido un error: {e}", position="top-right")
    
 

    
    
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
        