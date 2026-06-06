

class VistaKPIResumen:
    """Clase que representa un resumen de KPI (Indicadores Clave de Rendimiento)."""

    def __init__(self, ingreso_bruto_totales: float, total_dinero_descontado: float,
                 ingreso_netos_totales: float, cantidad_pedidos: int, tasa_descuento_promedio: float) -> None:
        """
        Constructor de VistaKPIResumen.

        Args:
            ingreso_bruto_totales: Ingresos sin descuentos.
            total_dinero_descontado: Total de dinero descontado.
            ingreso_netos_totales: Ingresos netos (brutos - descuentos).
            cantidad_pedidos: Número de pedidos realizados.
            tasa_descuento_promedio: Porcentaje promedio descontado (0-100).
        """
        self._ingreso_bruto_totales = ingreso_bruto_totales
        self._total_dinero_descontado = total_dinero_descontado
        self._ingreso_netos_totales = ingreso_netos_totales
        self._cantidad_pedidos = cantidad_pedidos
        self._tasa_descuento_promedio = tasa_descuento_promedio

    # ------------------------------------------------------------------
    # Getter y Setter para ingreso_bruto_totales
    # ------------------------------------------------------------------
    @property
    def ingreso_bruto_totales(self) -> float:
        """Retorna los ingresos brutos totales."""
        return self._ingreso_bruto_totales

    @ingreso_bruto_totales.setter
    def ingreso_bruto_totales(self, value: float) -> None:
        """Establece los ingresos brutos totales (debe ser >= 0)."""
        if not isinstance(value, (int, float)):
            raise TypeError("ingreso_bruto_totales debe ser un número.")
        if value < 0:
            raise ValueError("ingreso_bruto_totales no puede ser negativo.")
        self._ingreso_bruto_totales = float(value)

    # ------------------------------------------------------------------
    # Getter y Setter para total_dinero_descontado
    # ------------------------------------------------------------------
    @property
    def total_dinero_descontado(self) -> float:
        """Retorna el total de dinero descontado."""
        return self._total_dinero_descontado

    @total_dinero_descontado.setter
    def total_dinero_descontado(self, value: float) -> None:
        """Establece el total descontado (debe ser >= 0)."""
        if not isinstance(value, (int, float)):
            raise TypeError("total_dinero_descontado debe ser un número.")
        if value < 0:
            raise ValueError("total_dinero_descontado no puede ser negativo.")
        self._total_dinero_descontado = float(value)

    # ------------------------------------------------------------------
    # Getter y Setter para ingreso_netos_totales
    # ------------------------------------------------------------------
    @property
    def ingreso_netos_totales(self) -> float:
        """Retorna los ingresos netos totales."""
        return self._ingreso_netos_totales

    @ingreso_netos_totales.setter
    def ingreso_netos_totales(self, value: float) -> None:
        """Establece los ingresos netos (debe ser >= 0 y consistente con brutos y descuentos)."""
        if not isinstance(value, (int, float)):
            raise TypeError("ingreso_netos_totales debe ser un número.")
        if value < 0:
            raise ValueError("ingreso_netos_totales no puede ser negativo.")
        # Opcional: verificar coherencia con brutos y descuentos
        # if abs(value - (self._ingreso_bruto_totales - self._total_dinero_descontado)) > 0.01:
        #     raise ValueError("ingreso_netos_totales no coincide con la diferencia entre brutos y descuentos.")
        self._ingreso_netos_totales = float(value)

    # ------------------------------------------------------------------
    # Getter y Setter para cantidad_pedidos
    # ------------------------------------------------------------------
    @property
    def cantidad_pedidos(self) -> int:
        """Retorna la cantidad de pedidos."""
        return self._cantidad_pedidos

    @cantidad_pedidos.setter
    def cantidad_pedidos(self, value: int) -> None:
        """Establece la cantidad de pedidos (debe ser >= 0)."""
        if not isinstance(value, int):
            raise TypeError("cantidad_pedidos debe ser un entero.")
        if value < 0:
            raise ValueError("cantidad_pedidos no puede ser negativo.")
        self._cantidad_pedidos = value

    # ------------------------------------------------------------------
    # Getter y Setter para tasa_descuento_promedio
    # ------------------------------------------------------------------
    @property
    def tasa_descuento_promedio(self) -> float:
        """Retorna la tasa de descuento promedio (en porcentaje)."""
        return self._tasa_descuento_promedio

    @tasa_descuento_promedio.setter
    def tasa_descuento_promedio(self, value: float) -> None:
        """Establece la tasa de descuento promedio (entre 0 y 100 inclusive)."""
        if not isinstance(value, (int, float)):
            raise TypeError("tasa_descuento_promedio debe ser un número.")
        if value < 0 or value > 100:
            raise ValueError("tasa_descuento_promedio debe estar entre 0 y 100.")
        self._tasa_descuento_promedio = float(value)

    # ------------------------------------------------------------------
    # Representación en cadena (opcional)
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        return (f"VistaKPIResumen(ingreso_bruto_totales={self.ingreso_bruto_totales}, "
                f"total_dinero_descontado={self.total_dinero_descontado}, "
                f"ingreso_netos_totales={self.ingreso_netos_totales}, "
                f"cantidad_pedidos={self.cantidad_pedidos}, "
                f"tasa_descuento_promedio={self.tasa_descuento_promedio})")