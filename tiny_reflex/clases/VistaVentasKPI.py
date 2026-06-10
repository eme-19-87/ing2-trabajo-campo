
from datetime import date, datetime, timedelta

class VistaVentasKPI:
    def __init__(
        self,
        order_item_id: int,
        producto: str,
        categoria: str,
        ciudad: str,
        estado_pedido: str,
        segmento: str,
        venta_bruta: float,
        venta_neta: float,
        descuento_porcentaje: float,
        descuento_valor: float,
        fecha:date,
        nombre_cliente:str,
        pais:str,
        cantidad:int
        
    ):
        self._order_item_id = order_item_id
        self._producto = producto
        self._categoría = categoria
        self._ciudad = ciudad
        self._estado_pedido = estado_pedido
        self._segmento = segmento
        self._venta_bruta = venta_bruta
        self._venta_neta = venta_neta
        self._descuento_porcentaje = descuento_porcentaje
        self._descuento_valor = descuento_valor
        self._fecha= fecha
        self._nombre_cliente= nombre_cliente
        self._pais= pais
        self._cantidad= cantidad

    @property
    def order_item_id(self) -> int:
        return self._order_item_id

    @order_item_id.setter
    def order_item_id(self, value: int):
        self._order_item_id = value

    @property
    def producto(self) -> str:
        return self._producto

    @producto.setter
    def producto(self, value: str):
        self._producto = value

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, value: str):
        self._categoria = value

    @property
    def ciudad(self) -> str:
        return self._ciudad

    @ciudad.setter
    def ciudad(self, value: str):
        self._ciudad = value

    @property
    def estado_pedido(self) -> str:
        return self._estado

    @estado_pedido.setter
    def estado_pedido(self, value: str):
        self._estado_pedido = value

    @property
    def segmento(self) -> str:
        return self._segmento

    @segmento.setter
    def segmento(self, value: str):
        self._segmento = value

    @property
    def venta_bruta(self) -> float:
        return self._venta_bruta

    @venta_bruta.setter
    def venta_bruta(self, value: float):
        self._venta_bruta = value

    @property
    def venta_neta(self) -> float:
        return self._venta_neta

    @venta_neta.setter
    def venta_neta(self, value: float):
        self._venta_neta = value

    @property
    def descuento_porcentaje(self) -> float:
        return self._descuento_porcentaje

    @descuento_porcentaje.setter
    def descuento_porcentaje(self, value: float):
        self._descuento_porcentaje = value

    @property
    def descuento_valor(self) -> float:
        return self._descuento_valor

    @descuento_valor.setter
    def descuento_valor(self, value: float):
        self._descuento_valor = value
    
    @property
    def fecha(self) -> date:
        return self._fecha

    @fecha.setter
    def fecha(self, value: float):
        self._fecha = value
        
    @property
    def nombre_cliente(self) -> date:
        return self._nombre_cliente

    @nombre_cliente.setter
    def nombre_cliente(self, value: float):
        self._nombre_cliente = value
        
    @property
    def pais(self) -> date:
        return self._pais

    @pais.setter
    def pais(self, value: float):
        self._pais = value
        
    @property
    def cantidad(self) -> date:
        return self._cantidad

    @pais.setter
    def cantidad(self, value: float):
        self._cantidad = value