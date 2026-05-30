import reflex as rx
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional
from tiny_reflex.clases.Persona import Persona
from tiny_reflex.clases.Usuario import Usuario
from tiny_reflex.clases.Rol import Rol
from tiny_reflex.queries.UserQueries import UserQueries
import functools
import asyncio





   
        
# ===========================
# STATE DE USUARIOS
# ===========================
class UsuarioState(rx.State):
    """State para gestión de usuarios (ABM)."""
    
    # ===========================
    # DATASETS PRINCIPALES
    # ===========================
    usuarios: list[dict] = []
    cargando_usuarios: bool = False
    
    # Campos del formulario
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    password: str = ""
    confirmar_password: str = ""
    rol: str = "Analista"
    dni: str
    
    cargando_usuarios: bool = False
    error_usuarios: str = ""
    
    # Variables para búsqueda/filtro
    busqueda: str = ""
    
    #para cargar los roles
    roles_disponibles: list[dict] = []
    roles_loading: bool = False
    id_rol_seleccionado: int = 0  # Guarda el ID del rol seleccionado
    nombre_rol_seleccionado: str = ""  # Guarda el nombre del rol seleccionado
    
    #variables para controlar la edición
    editando_id: Optional[int] = None  # None = modo creación, con ID = modo edición
    usuario_original_email: str = ""   # Para validar email único en edición
    usuario_original_dni: str = ""     # Para validar DNI único en edición
    usuario_editar_id: int=0
    
    # Para controlar el diálogo de confirmación en la cancelación del alta de usuario
    dialogo_cancelar_abierto: bool = False
    cancelando: bool = False
    

    
    # ===========================
    # FLAGS DE ESTADO
    # ===========================
    saving_usuario: bool = False
    
    

    
    # ===========================
    # PROPIEDADES DERIVADAS
    # ===========================
    @rx.var
    def has_usuarios(self) -> bool:
        return len(self.usuarios) > 0
    
    
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
    

    @rx.var
    def is_editando(self) -> bool:
        """Indica si el formulario está en modo edición."""
        return self.editando_id is not None
    
    @rx.var
    def titulo_formulario(self) -> str:
        """Título dinámico del formulario."""
        return "Editar Usuario" if self.is_editando else "Nuevo Usuario"
    
    @rx.var
    def texto_boton(self) -> str:
        """Texto dinámico del botón."""
        return "Actualizar Usuario" if self.is_editando else "Registrar Usuario"
    
    @rx.var
    def mostrar_campos_password(self) -> bool:
        """Indica si mostrar los campos de contraseña."""
        return not self.is_editando  # Solo mostrar en creación
    
    #--------------------------------------------------------------#
    #Métodos para controlar los datos del formulario traidos
    #o insertados en la base de datos
    #--------------------------------------------------------------#
        
    def control_format(self):
        """Método orquestador que controla el alta del nuevo usuario"""
        try:
            rol=Rol(self.id_rol_seleccionado,self.nombre_rol_seleccionado)
            usuario=Usuario(0,self.nombre,self.apellido,self.dni,self.email,self.password,self.confirmar_password,rol)
            msj=usuario.control_format(self.email,self.dni,self.nombre,self.apellido,self.password,self.confirmar_password)
            
            #si algún campo no cumple el formato, se informa, en caso contrario, el campo msj estará vacío
            if len(msj)>0:
                return rx.toast.error(msj, position="top-right", duration=None)
        
            
            msj= Persona.control_dni(usuario.dni)
            if len(msj)>0:
                return rx.toast.error(msj, position="top-right", duration=None)
            msj=Usuario.control_email(self.email)
            if len(msj)>0:
                return rx.toast.error(msj, position="top-right", duration=None)
            
            # Si todos los campos están completos
            self.saving_usuario=True
            msj=Usuario.create_user(self.nombre,self.apellido,self.dni,self.email,self.password,self.id_rol_seleccionado)
            self.cancelar_edicion()
            return rx.toast.success("Usuario creado correctamente", position="top-right", duration=None)
            
            
        except Exception as e:
            return rx.toast.error(e, position="top-right", duration=None)
        finally:
            self.saving_usuario=False
            
    @rx.event
    async def control_format_update(self):
        

        try:
            # Prepara los datos desde el estado
            id_usuario = self.editando_id
            nombre = self.nombre.strip()
            apellido = self.apellido.strip()
            dni = self.dni.strip()
            email = self.email.strip()
            rol = self.id_rol_seleccionado
            usuario=Usuario(id_usuario,nombre,apellido,dni,email,"","",Rol(rol,self.nombre_rol_seleccionado))
            msj=usuario.control_format_update(id_usuario,email,dni,nombre,apellido)
            if (len(msj)>0):
                yield rx.toast.error(msj,position="top-right")
                return
            msj=Persona.control_update_dni(id_usuario,dni)
            if (len(msj)>0):
                 yield rx.toast.error(msj,position="top-right")
                 return

            msj=Usuario.control_update_email(id_usuario,email)
            if (len(msj)>0):
                 yield rx.toast.error(msj,position="top-right")
                 return
            
            func = functools.partial(
                usuario.update_user,
                id_usuario,
                nombre,
                apellido,
                dni,
                email,
                rol,
            )
            
            mensaje = await rx.run_in_thread(func)

            # Si llegamos aquí, la actualización fue exitosa
            yield rx.toast.success(f"✅ Usuario actualizado correctamente", position="top-right")
            self.cancelar_edicion()   # limpia formulario y sale de edición
            

        except Exception as e:
            # Captura cualquier excepción (incluyendo las lanzadas por la función)
            yield rx.toast.error(f"{str(e)}", position="top-right")
        finally:
            self.saving_usuario = False       
        
    @rx.event
    async def cargar_roles(self):
        """Carga los roles desde la base de datos."""
        self.roles_loading = True
        
        try:
            
            self.roles_disponibles = await rx.run_in_thread(Rol.get_roles)
            
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
    
    @rx.event
    async def cargar_usuarios(self):
        """Carga todos los usuarios desde la base de datos."""
        self.cargando_usuarios = True
        try:
            usuarios = await rx.run_in_thread(Usuario.load_user_data)
            self.usuarios = usuarios
        except Exception as e:
            yield rx.toast.error(f"Error al cargar usuarios: {e}", position="top-right")
        finally:
            self.cargando_usuarios = False
    
    @rx.event
    async def cambiar_estado_usuario(self, id_usuario: int, estado_actual: bool):
        """Cambia el estado del usuario (activo/inactivo)."""
        
        # Mostrar toast de proceso
        yield rx.toast.info("⏳ Cambiando estado del usuario...", position="top-right")
        
        try:
            # Llamar al procedimiento almacenado para cambiar estado
            # Asumiendo que tienes un método como este en UserQueries
            exito = await rx.run_in_thread(
                UserQueries.cambiar_estado_usuario,
                id_usuario,
                not estado_actual  # Invertir el estado
            )
            
            if exito:
                nuevo_estado = "activado" if not estado_actual else "desactivado"
                yield rx.toast.success(f"✅ Usuario {nuevo_estado} correctamente", position="top-right")
                # Recargar la lista de usuarios
                await self.cargar_usuarios()
            else:
                yield rx.toast.error("❌ Error al cambiar el estado", position="top-right")
                
        except Exception as e:
            yield rx.toast.error(f"❌ Error: {e}", position="top-right")
            
    

    
     #--------------------------------------------------------------#
    #Métodos adicionales para el funcionamiento del formulario
    #
    #--------------------------------------------------------------#        
    @rx.event
    def set_busqueda(self, valor: str):
        """Actualiza el filtro de búsqueda."""
        self.busqueda = valor
    
    @rx.var
    def usuarios_filtrados(self) -> list[dict]:
        """Retorna usuarios filtrados por búsqueda."""
        if not self.busqueda.strip():
            return self.usuarios
        
        busqueda_lower = self.busqueda.lower().strip()
        
        return [
            u for u in self.usuarios
            if busqueda_lower in u.get("nombre", "").lower()
            or busqueda_lower in u.get("apellido", "").lower()
            or busqueda_lower in u.get("email", "").lower()
            or busqueda_lower in u.get("dni", "").lower()
            or busqueda_lower in u.get("nombre_rol", "").lower()
        ]
    
    @rx.var
    def total_usuarios(self) -> int:
        """Retorna el total de usuarios."""
        return len(self.usuarios)
    
    @rx.var
    def total_filtrados(self) -> int:
        """Retorna el total de usuarios filtrados."""
        return len(self.usuarios_filtrados)
    
    @rx.event
    def limpiar_si_editando(self):
        """Limpia el formulario si se está en modo edición al cargar la página."""
        if self.editando_id is not None:
            self._cancelar_edicion() 
    
    
    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.nombre = ""
        self.apellido = ""
        self.dni = ""
        self.email = ""
        self.password = ""
        self.confirmar_password = ""
        # No limpiar rol seleccionado
        
    
    def cancelar_edicion(self):
        """Cancela la edición y limpia todo."""
        self.editando_id = None
        self.usuario_original_email = ""
        self.usuario_original_dni = ""
        self._limpiar_formulario()
    
    
    @rx.event
    async def set_usuario_editar(self, id_usuario: int):
        """Guarda el ID del usuario a editar y redirige al formulario."""
        
        try:
            self.usuario_editar_id = id_usuario
            func = functools.partial(Usuario.get_user_by_id, id_usuario)
            usuario = await rx.run_in_thread(func)
            if usuario:
                self.editando_id = usuario["id_usuario"]
                self.nombre = usuario["nombre"]
                self.apellido = usuario["apellido"]
                self.dni = usuario["dni"]
                self.email = usuario["email"]
                self.nombre_rol_seleccionado = usuario["nombre_rol"]
                # Opcional: también guardar valores originales para validaciones
                self.usuario_original_email = usuario["email"]
                self.usuario_original_dni = usuario["dni"]
                # Buscar id_rol correspondiente (si tienes roles_disponibles cargados)
                for rol in self.roles_disponibles:
                    if rol["nombre_rol"] == usuario["nombre_rol"]:
                        self.id_rol_seleccionado = rol["id_rol"]
                        break
                yield rx.redirect("/usuarios") 
            else:
                yield rx.toast.error("Usuario no encontrado", position="top-right")
        except Exception as e:
            yield rx.toast.error(f"Error: {e}", position="top-right")
    
    @rx.event
    def abrir_dialogo_cancelar(self):
        """Abre el diálogo de confirmación para cancelar edición."""
        self.dialogo_cancelar_abierto = True

    @rx.event
    def cerrar_dialogo_cancelar(self):
        """Cierra el diálogo sin cancelar."""
        self.dialogo_cancelar_abierto = False

    @rx.event
    async def confirmar_cancelar_edicion(self):
        """Cancela la edición con confirmación."""
        self.dialogo_cancelar_abierto = False
        self.cancelando = True
        
        # Pausa opcional (para que se vea el toast)
        await asyncio.sleep(0.5)
        
        # Realizar la cancelación
        self.editando_id = None
        self.usuario_original_email = ""
        self.usuario_original_dni = ""
        self._limpiar_formulario()
        
        self.cancelando = False
        yield rx.toast.success("✅ Edición cancelada", position="top-right")
    
   