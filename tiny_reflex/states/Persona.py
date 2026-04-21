import reflex as rx
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional
from tiny_reflex.types import (
    UserData
)




   
        
# ===========================
# STATE DE USUARIOS
# ===========================
# 
class Persona(rx.State):
    """State para gestión de usuarios (ABM)."""
    
    dni: str
    
    def control_dni(self)->bool:
        pass