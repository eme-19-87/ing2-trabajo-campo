from datetime import date
from tiny_reflex.clases.VistaVentasKPI import VistaVentasKPI
from tiny_reflex.clases.DashboardController import DashboardController
import plotly.express as px
import plotly.graph_objects as go
import json
from typing import List,Dict, Any
class DashboardUI:
    def __init__(self, selected_region: str, selected_category: str, selected_initial_date: date,
                 selected_end_date:date):
        self._selected_region = selected_region
        self._selected_category = selected_category
        self._selected_initial_date = selected_initial_date
        self._selected_end_date = selected_end_date

    @property
    def selected_region(self) -> str:
        return self._selected_region

    @selected_region.setter
    def selected_region(self, value: str):
        self._selected_region = value

    @property
    def selected_category(self) -> str:
        return self._selected_category

    @selected_category.setter
    def selected_category(self, value: str):
        self._selected_category = value

    @property
    def selected_initial_date(self) -> date:
        return self._selected_initial_date

    @selected_initial_date.setter
    def selected_initial_date(self, value: date):
        self._selected_initial_date = value.isoformat().replace("-", "/")
        
    @property
    def selected_end_date(self) -> date:
        return self._selected_end_date

    @selected_end_date.setter
    def selected_end_date(self, value: date):
        self._selected_end_date = value.isoformat().replace("-", "/")
        
    
    def render():
        pass
    
    def dibujar_grafico_ventas(datos:List[VistaVentasKPI]):
        pass
        
    
    def dibujar_grafico_beneficio(datos:List[VistaVentasKPI]):
        
        pass
    

    
    def capturar_filtro(self) -> str:
        data = {
            "selected_region": self._selected_region,
            "selected_category": self._selected_category,
            "selected_initial_date": self._selected_initial_date.strftime("%Y/%m/%d") if self._selected_initial_date else None,
            "selected_end_date": self._selected_end_date.strftime("%Y/%m/%d") if self._selected_end_date else None
        }
        return json.dumps(data)