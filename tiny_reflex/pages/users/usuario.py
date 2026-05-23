"""Customers page component."""

import reflex as rx
from tiny_reflex.components.navbar import navbar
from tiny_reflex.states.UsuarioState import UsuarioState





# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

import reflex as rx
from tiny_reflex.states.UsuarioState import UsuarioState

def tabla_usuarios_avanzada() -> rx.Component:
    """Tabla de usuarios con botón de Alta/Baja."""
    
    return rx.card(
        rx.vstack(
            # Barra de herramientas
            rx.hstack(
                rx.heading("Usuarios del Sistema", size="3"),
                rx.hstack(
                    rx.badge(
                        f"Total: {UsuarioState.total_usuarios}",
                        color_scheme="gray",
                    ),
                    rx.button(
                        "⟳ Recargar",
                        on_click=UsuarioState.cargar_usuarios,
                        color_scheme="blue",
                        size="2",
                        loading=UsuarioState.cargando_usuarios,
                    ),
                    spacing="3",
                ),
                justify="between",
                width="100%",
                margin_bottom="4",
            ),
            
            # Búsqueda
            rx.input(
                placeholder="🔍 Buscar usuario...",
                value=UsuarioState.busqueda,
                on_change=UsuarioState.set_busqueda,
                width="100%",
                margin_bottom="4",
            ),
            
            # Tabla
            rx.cond(
                UsuarioState.cargando_usuarios,
                rx.center(rx.spinner(size="3"), height="400px"),
                
                rx.cond(
                    UsuarioState.usuarios_filtrados,
                    rx.scroll_area(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID"),
                                    rx.table.column_header_cell("Nombre"),
                                    rx.table.column_header_cell("Apellido"),
                                    rx.table.column_header_cell("DNI"),
                                    rx.table.column_header_cell("Email"),
                                    rx.table.column_header_cell("Rol"),
                                    rx.table.column_header_cell("Estado"),
                                    rx.table.column_header_cell("Acción"),  # Nueva columna
                                ),
                            ),
                            rx.table.body(
                                rx.foreach(
                                    UsuarioState.usuarios_filtrados,
                                    lambda user: rx.table.row(
                                        rx.table.cell(user["id_usuario"]),
                                        rx.table.cell(rx.text(user["nombre"], weight="medium")),
                                        rx.table.cell(user["apellido"]),
                                        rx.table.cell(user["dni"]),
                                        rx.table.cell(user["email"]),
                                        # Celda de Rol
                                        rx.table.cell(
                                            rx.cond(
                                                user["nombre_rol"] == "Administrador",
                                                rx.badge(user["nombre_rol"], color_scheme="purple", radius="full"),
                                                rx.badge(user["nombre_rol"], color_scheme="cyan", radius="full"),
                                            )
                                        ),
                                        # Celda de Estado
                                        rx.table.cell(
                                            rx.cond(
                                                user["activo"],
                                                rx.badge("Activo", color_scheme="green", radius="full"),
                                                rx.badge("Inactivo", color_scheme="gray", radius="full"),
                                            )
                                        ),
                                        # Celda con botón Alta/Baja
                                        rx.table.cell(
                                            rx.cond(
                                                user["activo"],
                                                # Si está activo → Botón "Baja"
                                                rx.button(
                                                    "Dar de Baja",
                                                    color_scheme="red",
                                                    size="2",
                                                    variant="soft",
                                                    on_click=lambda id=user["id_usuario"], estado=user["activo"]: 
                                                        UsuarioState.cambiar_estado_usuario(id, estado),
                                                ),
                                                # Si está inactivo → Botón "Alta"
                                                rx.button(
                                                    "Dar de Alta",
                                                    color_scheme="green",
                                                    size="2",
                                                    variant="soft",
                                                    on_click=lambda id=user["id_usuario"], estado=user["activo"]: 
                                                        UsuarioState.cambiar_estado_usuario(id, estado),
                                                ),
                                            )
                                        ),
                                    ),
                                ),
                            ),
                            width="100%",
                        ),
                        type="auto",
                        height="500px",
                        width="100%",
                    ),
                    
                    # Mensaje cuando no hay datos
                    rx.center(
                        rx.vstack(
                            rx.icon("users", size=48, color="gray"),
                            rx.text("No se encontraron usuarios", size="3", color="gray"),
                            rx.text("Prueba a cambiar los criterios de búsqueda", size="1", color="gray"),
                            spacing="3",
                        ),
                        height="400px",
                    ),
                ),
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        padding="4",
    )

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
        box_shadow="3",
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

def listar_usuarios() -> rx.Component:
    """Página principal de gestión de usuarios."""
    return rx.container(
        navbar(),
        rx.vstack(
            
            tabla_usuarios_avanzada(),
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
