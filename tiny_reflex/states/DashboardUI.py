import reflex as rx
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict
import functools
import json
from tiny_reflex.clases.DashboardController import DashboardController

class DashboardUI(rx.State):
    
    datos: List[dict] = []   # <- ahora lista de diccionarios (serializable)
    fecha_inicio: str = ""
    fecha_fin: str = ""
    
    categorias: list[str] = []
    regiones: list[str] = []
    
    categoria_seleccionada: str = ""
    region_seleccionada: str = ""
    
    cargando_categorias: bool = False
    cargando_regiones: bool = False
    cargando_grafico: bool = False
    
    figura: go.Figure = px.line()

    @rx.event
    async def cargar_y_graficar(self):
        self.cargando_grafico = True
        yield
        
        try:
            filtros = {
                "fecha_inicio": self.fecha_inicio,
                "fecha_fin": self.fecha_fin,
                "categoria": self.categoria_seleccionada,
                "region": self.region_seleccionada,
            }
            dashboard = DashboardController()
            dashboard.aplicar_filtros(json.dumps(filtros))
            func = functools.partial(dashboard.obtener_datos_metricas)
            datos_dict = await rx.run_in_thread(func)
            
            # Guardar directamente los diccionarios (ya serializables)
            self.datos = datos_dict if datos_dict else []
            
        except Exception as e:
            print(f"{e}")
            # Ya no asignamos self.figura, solo mostramos toast si quieres
            yield rx.toast.error(f"Error: {e}", position="top-right")
        finally:
            self.cargando_grafico = False

    @rx.event
    async def cargar_categorias(self):
        self.cargando_categorias = True
        try:
            dashboard = DashboardController()
            func = functools.partial(dashboard.obtener_categorias)
            categorias = await rx.run_in_thread(func)
            self.categorias = sorted(categorias)
        except Exception as e:
            print(f"Error cargando categorías: {e}")
        finally:
            self.cargando_categorias = False

    @rx.event
    async def cargar_regiones(self):
        self.cargando_regiones = True
        try:
            dashboard = DashboardController()
            func = functools.partial(dashboard.obtener_estados)
            regiones = await rx.run_in_thread(func)
            self.regiones = sorted(regiones)
        except Exception as e:
            print(f"{e}")
        finally:
            self.cargando_regiones = False

    @rx.event
    def set_fecha_inicio(self, valor: str):
        self.fecha_inicio = valor

    @rx.event
    def set_fecha_fin(self, valor: str):
        self.fecha_fin = valor

    @rx.event
    def set_categoria_seleccionada(self, valor: str):
        self.categoria_seleccionada = valor

    @rx.event
    def set_region_seleccionada(self, valor: str):
        self.region_seleccionada = valor

    @rx.event
    def dibujar_grafico_ventas(self):
        dashboard = DashboardController()
        self.datos=dashboard.obtener_datos_metricas()
        if not self.datos:
            self.figura=px.bar()
        
        df = pd.DataFrame(self.datos)   # <- ahora self.datos ya son dicts
        
        # Ajusta los nombres de columna según lo que devuelve tu consulta
        if 'categoria' in df and 'venta_bruta' in df:
            self.figura = px.bar(
            df,
            x="categoria",
            y="venta_bruta",
            title="Ventas Bruta Por Categoría",
        )
        