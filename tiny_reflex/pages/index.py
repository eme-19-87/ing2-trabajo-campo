"""Home page component."""

import reflex as rx
from tiny_reflex.components.navbar import navbar
from tiny_reflex.components.info_card import info_card

def index() -> rx.Component:
    """Main index page with navigation."""
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.heading("Proyecto: Sistema de Inteligencia de Datos (BI Pipeline)", font_size="2em"),
            rx.box("Análisis Base De Datos Dataco Supply Chain", font_size="1.2em"),
            rx.vstack(
                rx.box("Presentación"),
                spacing="2",
            ),
            rx.vstack(
                info_card(
                image_src="/favicon.ico",
                title="Espinoza Enrique Manuel",
                description=(
                    "Estudiante de Licenciatura En Sistemas De Información 4º Año. "
                    "DNI:32837262."
                ),
                footer_text="Linkedin:",
                footer_link="https://www.linkedin.com/in/enrique-espinoza-948157224",
                
            ),
                info_card(
                image_src="/favicon.ico",
                title="Canteros Murcia, Juan Ignacio Benjamin",
                description=(
                    "Estudiante de Licenciatura En Sistemas De Información 4º Año. "
                    "DNI:42059611"
                ),
                footer_text="Linkedin:",
                footer_link="https://www.linkedin.com/in/enrique-espinoza-948157224",
                
            ),
                spacing="2",
            ),
            spacing="2",
            padding_top="10%",
            align="center",
        ),
        width="100%",
        align="center"
    )
