from datetime import date

class VistaCalendario:
    """Clase que representa un resumen de calendario con datos de fecha, mes, año, trimestre, etc."""

    def __init__(self, fecha: date, anio: int, mes_nro: int, mes_nombre: str, trimestre: str,
                 dia_nombre: str, mes_dia: str, mes_anio: str, tipo_dia: str) -> None:
        """
        Constructor de VistaCalendario.

        Args:
            fecha: La fecha (objeto datetime.date).
            anio: El año numérico.
            mes_nro: El número del mes (1-12).
            mes_nombre: El nombre del mes (ej. "Enero").
            trimestre: El trimestre ("Primer", "Segundo", "Tercer", "Cuarto").
            dia_nombre: El nombre del día (ej. "Lunes").
            mes_dia: Combinación mes+día como cadena de 4 dígitos ("MMDD").
            mes_anio: Combinación año+mes como cadena de 6 dígitos ("YYYYMM").
            tipo_dia: Tipo de día ("Feriado" o "Laborable").
        """
        self._fecha = None
        self._anio = None
        self._mes_nro = None
        self._mes_nombre = None
        self._trimestre = None
        self._dia_nombre = None
        self._mes_dia = None
        self._mes_anio = None
        self._tipo_dia = None

        # Uso de setters para validar
        self.fecha = fecha
        self.anio = anio
        self.mes_nro = mes_nro
        self.mes_nombre = mes_nombre
        self.trimestre = trimestre
        self.dia_nombre = dia_nombre
        self.mes_dia = mes_dia
        self.mes_anio = mes_anio
        self.tipo_dia = tipo_dia

    # ------------------------------------------------------------------
    # Getter y Setter para fecha (datetime.date)
    # ------------------------------------------------------------------
    @property
    def fecha(self) -> date:
        """Retorna la fecha como objeto date."""
        return self._fecha

    @fecha.setter
    def fecha(self, value: date) -> None:
        if not isinstance(value, date):
            raise TypeError("fecha debe ser un objeto datetime.date")
        self._fecha = value

    # ------------------------------------------------------------------
    # Getter y Setter para anio (int)
    # ------------------------------------------------------------------
    @property
    def anio(self) -> int:
        return self._anio

    @anio.setter
    def anio(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("anio debe ser un entero")
        if value < 1900 or value > 2100:  # rango razonable
            raise ValueError("anio debe estar entre 1900 y 2100")
        self._anio = value

    # ------------------------------------------------------------------
    # Getter y Setter para mes_nro (int 1-12)
    # ------------------------------------------------------------------
    @property
    def mes_nro(self) -> int:
        return self._mes_nro

    @mes_nro.setter
    def mes_nro(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("mes_nro debe ser un entero")
        if value < 1 or value > 12:
            raise ValueError("mes_nro debe estar entre 1 y 12")
        self._mes_nro = value

    # ------------------------------------------------------------------
    # Getter y Setter para mes_nombre (str)
    # ------------------------------------------------------------------
    @property
    def mes_nombre(self) -> str:
        return self._mes_nombre

    @mes_nombre.setter
    def mes_nombre(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("mes_nombre debe ser una cadena")
        if not value.strip():
            raise ValueError("mes_nombre no puede estar vacío")
        self._mes_nombre = value.strip()

    # ------------------------------------------------------------------
    # Getter y Setter para trimestre (str)
    # ------------------------------------------------------------------
    @property
    def trimestre(self) -> str:
        return self._trimestre

    @trimestre.setter
    def trimestre(self, value: str) -> None:
        validos = ["Primer", "Segundo", "Tercer", "Cuarto"]
        if not isinstance(value, str):
            raise TypeError("trimestre debe ser una cadena")
        valor_limpio = value.strip()
        if not valor_limpio:
            raise ValueError("trimestre no puede estar vacío")
        if valor_limpio not in validos:
            raise ValueError(f"trimestre debe ser uno de {validos}")
        self._trimestre = valor_limpio

    # ------------------------------------------------------------------
    # Getter y Setter para dia_nombre (str)
    # ------------------------------------------------------------------
    @property
    def dia_nombre(self) -> str:
        return self._dia_nombre

    @dia_nombre.setter
    def dia_nombre(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("dia_nombre debe ser una cadena")
        if not value.strip():
            raise ValueError("dia_nombre no puede estar vacío")
        self._dia_nombre = value.strip()

    # ------------------------------------------------------------------
    # Getter y Setter para mes_dia (str con formato MMDD)
    # ------------------------------------------------------------------
    @property
    def mes_dia(self) -> str:
        return self._mes_dia

    @mes_dia.setter
    def mes_dia(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("mes_dia debe ser una cadena")
        if len(value) != 4 or not value.isdigit():
            raise ValueError("mes_dia debe ser una cadena de 4 dígitos (MMDD)")
        # Validación adicional: mes 01-12, día 01-31 (simplificada)
        mes = int(value[:2])
        dia = int(value[2:])
        if mes < 1 or mes > 12:
            raise ValueError("mes_dia: los dos primeros dígitos deben representar un mes válido (01-12)")
        if dia < 1 or dia > 31:
            raise ValueError("mes_dia: los dos últimos dígitos deben representar un día válido (01-31)")
        self._mes_dia = value

    # ------------------------------------------------------------------
    # Getter y Setter para mes_anio (str con formato YYYYMM)
    # ------------------------------------------------------------------
    @property
    def mes_anio(self) -> str:
        return self._mes_anio

    @mes_anio.setter
    def mes_anio(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("mes_anio debe ser una cadena")
        if len(value) != 6 or not value.isdigit():
            raise ValueError("mes_anio debe ser una cadena de 6 dígitos (YYYYMM)")
        anio = int(value[:4])
        mes = int(value[4:])
        if anio < 1900 or anio > 2100:
            raise ValueError("mes_anio: año fuera de rango (1900-2100)")
        if mes < 1 or mes > 12:
            raise ValueError("mes_anio: mes debe estar entre 01 y 12")
        self._mes_anio = value

    # ------------------------------------------------------------------
    # Getter y Setter para tipo_dia (str)
    # ------------------------------------------------------------------
    @property
    def tipo_dia(self) -> str:
        return self._tipo_dia

    @tipo_dia.setter
    def tipo_dia(self, value: str) -> None:
        valores_permitidos = ["Feriado", "Laborable"]
        if not isinstance(value, str):
            raise TypeError("tipo_dia debe ser una cadena")
        valor_limpio = value.strip().capitalize()
        if valor_limpio not in valores_permitidos:
            raise ValueError(f"tipo_dia debe ser uno de {valores_permitidos}")
        self._tipo_dia = valor_limpio

    # ------------------------------------------------------------------
    # Representación en cadena (opcional)
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        return (f"VistaCalendario(fecha={self.fecha.isoformat()}, anio={self.anio}, "
                f"mes_nro={self.mes_nro}, mes_nombre={self.mes_nombre}, trimestre={self.trimestre}, "
                f"dia_nombre={self.dia_nombre}, mes_dia={self.mes_dia}, mes_anio={self.mes_anio}, "
                f"tipo_dia={self.tipo_dia})")
