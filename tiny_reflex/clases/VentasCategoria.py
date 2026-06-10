from typing import TypedDict


class VentasCategoria(TypedDict):
   def __init(self,categoria:str,venta_bruta:float):
    
    self._categoria=categoria
    self._venta_bruta=venta_bruta

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def order_item_id(self, value: str):
        self._categoria = value
        
    @property
    def venta_bruta(self) -> float:
        return self._venta_bruta

    @venta_bruta.setter
    def order_item_id(self, value: float):
        self._venta_bruta = value