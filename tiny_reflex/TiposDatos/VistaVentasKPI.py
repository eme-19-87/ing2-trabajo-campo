from typing import TypedDict


class VistaVentasKPI(TypedDict):
    """Definición de tipo para las ventas"""

    order_id: int
    order_item_id: int
    product_name: str | None
    category_name: str | None
    department_name: str | None
    city_name: str | None
    state_name: str | None
    market_name: str | None
    sales:float
    benefit_per_order: float
    profit_ratio_calc: float