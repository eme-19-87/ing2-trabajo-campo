import reflex as rx
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict
import functools
import json
from tiny_reflex.clases.DashboardController import DashboardController

class DashboardUI(rx.State):
    
   
    fecha_inicio: str = ""
    fecha_fin: str = ""
    categoria_seleccionada: str = ""
    estado_seleccionado: str = ""
    
    
    #variables para controlar los estados de la vista (proios de Reflex)
    #los datos que se mostrarán en el desplegable de categorías y estados
    categorias: list[str] = []
    estados: list[str] = []
    #controla lo que se mostrará o no mientras se están cargando los datos y el gráfico
    cargando_categorias: bool = False
    cargando_estados: bool = False
    cargando_grafico: bool = False
    #el conjunto de datos recuperados para mostrarlos en el gráfico
    datos: List[dict] = []  
    #el gráfico que se mostrará
    figura: go.Figure = px.line()

    @rx.event
    async def buscar_datos(self):
        self.cargando_grafico = True
        yield
        
        try:
            filtros = {
                "fecha_inicio": self.fecha_inicio,
                "fecha_fin": self.fecha_fin,
                "categoria": self.categoria_seleccionada,
                "estado": self.estado_seleccionado,
            }
            dashboard=DashboardController()
            dashboard.aplicar_filtros(json.dumps(filtros))
            self.datos=dashboard.obtener_datos_estado_categoria()
            print("En DasboardUI:")
            print(self.datos)
            self.dibujar_estado_categoria()
            
        except Exception as e:
            # Ya no asignamos self.figura, solo mostramos toast si quieres
            yield rx.toast.error(f"{e}", position="top-right")
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
             yield rx.toast.error(f"{e}", position="top-right")
        finally:
            self.cargando_categorias = False

    @rx.event
    async def cargar_estados(self):
        self.cargando_estados = True
        try:
            dashboard = DashboardController()
            func = functools.partial(dashboard.obtener_estados)
            estados = await rx.run_in_thread(func)
            self.estados = sorted(estados)
        except Exception as e:
             yield rx.toast.error(f"{e}", position="top-right")
        finally:
            self.cargando_estados = False

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
      
        self.estado_seleccionado = valor

   
    def dibujar_estado_categoria(self):
        
        try:
            df = pd.DataFrame(self.datos)   # <- ahora self.datos ya son dicts
            print("En la parte de la gráfica")
            print(df)
            # Ajusta los nombres de columna según lo que devuelve tu consulta
            if 'mes_nombre' in df and 'total_venta_neta' in df:
                self.figura = px.bar(
                df,
                x="mes_nombre",
                y="total_venta_neta",
                title=f"Ventas Por Meses Desde {self.fecha_inicio} Hasta {self.fecha_fin} para {self.categoria_seleccionada} ",
            )
        except Exception as e:
             yield rx.toast.error(f"{e}", position="top-right")
        if not self.datos:
            self.figura=px.bar()
        
        
        