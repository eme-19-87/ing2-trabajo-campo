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
    id_rol_seleccionado: int = 0  # Guarda el ID del rol seleccionado
    nombre_rol_seleccionado: str = ""  # Guarda el nombre del rol seleccionado
    

    
    # ===========================
    # FLAGS DE ESTADO
    # ===========================
    saving_usuario: bool = False
    
    

    
    # ===========================
    # PROPIEDADES DERIVADAS
    # ===========================
    @rx.var
    def has_usuarios(self) -> bool:
        return len(self.usuarios_data) > 0
    
    
    @rx.var
    def is_user_insert(self)->bool:
        return self.saving_usuario
       
    @rx.event
    def set_rol(self, value: str):
        """Actualiza el rol seleccionado."""
        self.rol = value
    
    @rx.event
    def set_rol_por_id(self, value: str):
        """Actualiza el rol seleccionado cuando cambia el select."""
        # value es el nombre del rol seleccionado
        self.nombre_rol_seleccionado = value
        
        # Buscar el id_rol correspondiente
        for rol in self.roles_disponibles:
            if rol["nombre_rol"] == value:
                self.id_rol_seleccionado = rol["id_rol"]
                break
    

        
    def control_format(self):
        """Verifica si algún campo obligatorio está en blanco y muestra toast."""
        try:
           
            mjs=Usuario.control_format(self.email,self.dni,self.nombre,self.apellido,self.password,self.id_rol_seleccionado,self.confirmar_password)
            if len(mjs)>0:
                return self.view_toast(mjs,2)
        
            
        # Si todos los campos están completos
            self.saving_usuario=True
            yield rx.toast.info("⏳ Por favor, verifique el mensaje...", position="top-right", duration=None)
            if not Persona.control_dni(self.dni):
                mjs+="El dni del usuario ya figura en el sistema"
                return rx.toast.info(mjs, position="top-right", duration=None)
            
            if not Usuario.control_email(self.email):
                mjs+="El email del usuario ya figura en el sistema"
                return rx.toast.info(mjs, position="top-right", duration=None)
            
            if Usuario.create_user(self.nombre,self.apellido,self.dni,self.email,self.password,self.id_rol_seleccionado):
                self.saving_usuario=False
                return rx.toast.success("Usuario creada correctamente", position="top-right", duration=None)
            
            return self.view_toast("Error al insertar el usuario",2)
        except Exception as e:
            return self.view_toast(f"Error al insertar usuario: {e}",2)
        finally:
            self.saving_usuario=False
    
 
    def view_toast(self,msj:str, msj_type: int):
        if msj_type==1:
            return rx.toast.success(msj, position="top-right")
        else:
            return rx.toast.error(msj, position="top-right")
        
    @rx.event
    async def cargar_roles(self):
        """Carga los roles desde la base de datos."""
        self.roles_loading = True
        
        try:
            
            self.roles_disponibles = await rx.run_in_thread(UserQueries.get_roles)
            
            # Seleccionar el primer rol por defecto si hay roles disponibles
            if self.roles_disponibles and self.id_rol_seleccionado == 0:
                self.id_rol_seleccionado = self.roles_disponibles[0]["id_rol"]
                self.nombre_rol_seleccionado = self.roles_disponibles[0]["nombre_rol"]
                
        except Exception as e:
            yield rx.toast.error(f"Error al cargar roles: {e}", position="top-right")
        
        self.roles_loading = False
    
    # Convertir roles al formato que espera el Select de Reflex
    @rx.var
    def opciones_roles_select(self) -> list:
        """Convierte los roles de BD al formato del select."""
        return [
            rol["nombre_rol"]
            for rol in self.roles_disponibles
        ]
        