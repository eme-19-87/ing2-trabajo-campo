import reflex as rx
from tiny_reflex.components.navbar import navbar
from tiny_reflex.states.DashboardUI import DashboardUI

def filtros() -> rx.Component:
    """Componente con los controles de filtro."""
    return rx.card(
        rx.vstack(
            rx.heading("Filtros", size="2"),
            rx.hstack(
                rx.vstack(
                    rx.text("Fecha Inicio:", font_weight="bold"),
                    rx.input(
                        type="date",
                        value=DashboardUI.fecha_inicio,
                        on_change=DashboardUI.set_fecha_inicio,
                        width="200px",
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Fecha Fin:", font_weight="bold"),
                    rx.input(
                        type="date",
                        value=DashboardUI.fecha_fin,
                        on_change=DashboardUI.set_fecha_fin,
                        width="200px",
                    ),
                    spacing="1",
                ),
                spacing="4",
            ),
            rx.hstack(
                rx.vstack(
                    rx.text("Categoría:", font_weight="bold"),
                    rx.cond(
                        DashboardUI.cargando_categorias,
                        rx.spinner(),
                        rx.select(
                            DashboardUI.categorias,
                            placeholder="Todas",
                            on_change=DashboardUI.set_categoria_seleccionada,   # <-- nuevo
                            width="200px",
                        ),
                    ),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Estado:", font_weight="bold"),
                    rx.cond(
                        DashboardUI.cargando_estados,
                        rx.spinner(),
                        rx.select(
                            DashboardUI.estados,
                            placeholder="Todos",
                            on_change=DashboardUI.set_estado_seleccionado,      # <-- nuevo
                            width="200px",
                        ),
                    ),
                    spacing="1",
                ),
                rx.button(
                    "Graficar",
                    on_click=DashboardUI.buscar_datos,   # <-- aquí el método
                    color_scheme="blue",
                    margin_top="auto",
                ),
                spacing="4",
                align="end",
            ),
            spacing="4",
            width="100%",
        ),
        padding="4",
        margin_bottom="4",
    )


def grafico_ventas() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Ventas por Categoría", size="2"),
            rx.cond(
                DashboardUI.cargando_grafico,
                rx.center(rx.spinner(size="3"), height="400px"),
                rx.plotly(
                            data=DashboardUI.figura
                            
                        )
            ),
            spacing="4",
            width="100%",
        ),
        padding="4",
    )


def dashboard_page() -> rx.Component:
    """Página principal del dashboard."""
    return rx.container(
        navbar(),
        rx.vstack(
            filtros(),
            grafico_ventas(),                     # <-- descomentado
            spacing="4",
            width="100%",
        ),
        max_width="1200px",
        padding="4",
        on_mount=[
            DashboardUI.cargar_categorias,
            DashboardUI.cargar_estados
         # carga inicial con filtros vacíos
        ],
    )