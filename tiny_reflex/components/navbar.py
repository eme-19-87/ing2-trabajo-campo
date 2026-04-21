import reflex as rx


def navbar() -> rx.Component:
    """Reusable navigation bar with Customers dropdown."""
    return rx.hstack(
        rx.heading("Brazil Ecommerce Explorer", size="5"),

        rx.spacer(),

        rx.link("Home", href="/"),

        # =========================
        # Customers (Dropdown)
        # =========================
        rx.menu.root(
            rx.menu.trigger(
                rx.text("Usuarios ▾", cursor="pointer")
            ),
            rx.menu.content(
                 rx.menu.item(
                    rx.link("Listar Usuarios", href="/customers")
                ),
                rx.menu.item(
                    rx.link("Alta Usuarios", href="/customers/sales_by_state")
                )
            ),
        ),

        padding="1em",
        width="100%",
        border_bottom="1px solid #333",
        align="center",
        spacing="4",
    )

