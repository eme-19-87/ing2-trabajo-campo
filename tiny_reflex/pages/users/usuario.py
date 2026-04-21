"""Customers page component."""

import reflex as rx
from tiny_reflex.components.navbar import navbar
from tiny_reflex.states.UsuarioState import UsuarioState





# ============================================================
# PÁGINA PRINCIPAL
# ============================================================


def formulario_usuario() -> rx.Component:
    """Formulario para alta y edición de usuarios."""
    return rx.card(
        rx.vstack(
            rx.heading("Alta De Usuarios", font_size="2em",align="center"),
            # Campo: Nombre
            rx.text("Nombre:", font_weight="bold"),
            rx.input(
                placeholder="Ingrese el nombre",
                value=UsuarioState.nombre,
                on_change=UsuarioState.set_nombre,
                width="100%",
                required=True,
            ),
            
            # Campo: Apellido
            rx.text("Apellido:", font_weight="bold"),
            rx.input(
                placeholder="Ingrese el apellido",
                value=UsuarioState.apellido,
                on_change=UsuarioState.set_apellido,
                width="100%",
                required=True,
            ),
            
            #Campo: DNI
            rx.text("DNI:", font_weight="bold"),
            rx.input(
                placeholder="DNI de al menos 8 números sin puntos",
                value=UsuarioState.dni,
                on_change=UsuarioState.set_dni,
                width="100%",
                required=True,
            ),
            
            # Campo: Email
            rx.text("Email:", font_weight="bold"),
            rx.input(
                placeholder="UsuarioState@ejemplo.com",
                type="email",
                value=UsuarioState.email,
                on_change=UsuarioState.set_email,
                width="100%",
                required=True,
            ),
            
            # Campo: Contraseña
            rx.text("Contraseña:", font_weight="bold"),
            rx.input(
                placeholder="Ingrese contraseña",
                type="password",
                value=UsuarioState.password,
                on_change=UsuarioState.set_password,
                width="100%",
               
            ),
           
            
            # Campo: Repetir Contraseña
            rx.text("Repetir Contraseña:", font_weight="bold"),
            rx.input(
                placeholder="Repita la contraseña",
                type="password",
                value=UsuarioState.confirmar_password,
                on_change=UsuarioState.set_confirmar_password,
                width="100%"
            ),
            
            # Campo: Rol (Select desde BD)
            rx.text("Rol:", font_weight="bold"),
            rx.cond(
                UsuarioState.roles_loading,
                rx.spinner(),  # Mostrar spinner mientras carga
                rx.select(
                    UsuarioState.opciones_roles_select,
                    value=UsuarioState.nombre_rol_seleccionado,
                    on_change=UsuarioState.set_rol_por_id,
                    width="100%",
                    placeholder="Seleccione un rol",
                    on_mount=UsuarioState.cargar_roles
                ),
            ),
            
            
            # Botones
            rx.hstack(
                rx.button(
                    "Ingresar",
                    on_click=UsuarioState.control_format,
                    color_scheme="blue",
                    width="100%",
                    loading=UsuarioState.saving_usuario
            ),
            
            spacing="4",
            width="100%",
        ),
        width="500px",
        padding="6",
        box_shadow="lg",
    )
    )


def pagina_usuarios() -> rx.Component:
    """Página principal de gestión de usuarios."""
    return rx.container(
        navbar(),
        rx.vstack(
            
            formulario_usuario(),
            spacing="2",
            width="100%",
            align="center",
            margin="10px"
        ),
        width="100%",
        padding="4",
        align="center",
    )


# Para agregar la página a la aplicación (en tu archivo principal)
# app.add_page(pagina_usuarios, route="/usuarios", title="Gestión de Usuarios")
