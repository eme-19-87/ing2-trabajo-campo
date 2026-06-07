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
    cargando_kpi:bool=False
    #el conjunto de datos recuperados para mostrarlos en el gráfico
    datos: List[dict] = []  
    #datos kpi
    datos_kpi: List[dict] = []  
    #el gráfico que se mostrará
    figura: go.Figure = px.line()
    figura_kpi:go.Figure=px.line()

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
            self.datos=dashboard.get_ventas_por_categoria_y_mes()
            self.dibujar_grafico_ventas_por_categoria_y_mes()
            self.datos_kpi=dashboard.get_kpi_por_categoria_y_mes()
            self.dibujar_kpi_categoria_mes()
            yield
            
        except Exception as e:
            # Ya no asignamos self.figura, solo mostramos toast si quieres
            yield rx.toast.error(f"{e}", position="top-right")
        finally:
            self.cargando_grafico = False
            self.cargando_kpi = False

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

   
    def dibujar_grafico_ventas_por_categoria_y_mes(self):
        try:
            if not self.datos:
                self.figura = px.bar()  # gráfico vacío
                return
            df = pd.DataFrame(self.datos)
            if 'mes_nombre' in df and 'total_venta_neta' in df:
                self.figura = px.bar(
                    df,
                    x="mes_nombre",
                    y="total_venta_neta",
                    title=f"Ventas Por Meses Desde {self.fecha_inicio} Hasta {self.fecha_fin} para {self.categoria_seleccionada}",
                )
            else:
                self.figura = px.bar()
        except Exception as e:
            # NO uses yield aquí; solo imprime o muestra toast con un evento (pero no es evento)
            print(f"Error en dibujar_grafico: {e}")
            self.figura = px.bar()
            
        
    def dibujar_kpi_categoria_mes(self):
        try:
            if not self.datos_kpi:
                self.figura_kpi = go.Figure()   # vacío
                return
            # Asumimos que self.datos_kpi es un dict con las claves: 
            # 'promedio', 'maximo', 'minimo', 'mediana', 'desviacion_estandar'
            # Si es una lista de un solo elemento, lo extraemos:
            if isinstance(self.datos_kpi, list) and len(self.datos_kpi) == 1:
                kpi = self.datos_kpi[0]
            else:
                kpi = self.datos_kpi
            
            # Construir tabla con los valores
            self.figura_kpi = go.Figure(data=[go.Table(
                header=dict(
                    values=["Métrica", "Valor"],
                    fill_color='paleturquoise',
                    align='left',
                    font=dict(size=12)
                ),
                cells=dict(
                    values=[
                        ["Promedio", "Máximo", "Mínimo", "Mediana", "Desviación Estándar"],
                        [
                            f"{kpi.get('promedio', 0):,.2f}",
                            f"{kpi.get('maximo', 0):,.2f}",
                            f"{kpi.get('minimo', 0):,.2f}",
                            f"{kpi.get('mediana', 0):,.2f}",
                            f"{kpi.get('desviacion_estandar', 0):,.2f}"
                        ]
                    ],
                    fill_color='lavender',
                    align='left'
                )
            )])
            self.figura_kpi.update_layout(title="Estadísticos de venta neta por mes")
        except Exception as e:
            print(f"Error en dibujar_kpi_categoria_mes: {e}")
            self.figura_kpi = go.Figure()