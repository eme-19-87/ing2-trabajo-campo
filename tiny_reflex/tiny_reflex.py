"""Main application file for Reflex app."""

import reflex as rx
from tiny_reflex.pages.index import index
from tiny_reflex.pages.users.usuario import pagina_usuarios
from tiny_reflex.pages.users.usuario import listar_usuarios
from tiny_reflex.pages.graphics.graphics import dashboard_page

# Create and configure the app
app = rx.App()

# Register all pages
app.add_page(index, route="/",title="Home")
app.add_page(pagina_usuarios, route="/usuarios", title="Gestión de Usuarios")
app.add_page(listar_usuarios, route="/lista_usuarios", title="Lista Usuarios")
app.add_page(dashboard_page, route="/graficas", title="Gráficas")


