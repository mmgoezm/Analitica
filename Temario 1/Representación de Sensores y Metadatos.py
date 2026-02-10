from datetime import datetime


class SensorIndustrial:
    def __init__(self, tag: str, unidad: str, rango: tuple):
        # Los metadatos permiten interpretar correctamente un valor
        self.metadatos = {
            "tag": tag,  # Tipo: String
            "unidad": unidad,  # Tipo: String
            "rango_max_min": rango,  # Tipo: Tuple (Estructura de almacenamiento)
            "instalacion": "Planta ITM"
        }

    def procesar_lectura(self, valor: int | float) -> dict:
        """
        Valida la taxonomía del dato y su rango de ingeniería.
        """
        # Validación de tipos: Asegura integridad en la analítica de datos
        if not isinstance(valor, (int, float)):
            raise ValueError(f"Error: Se esperaba número, se recibió {type(valor)}")

        # Lógica de proceso: Determinamos si hay alarma (Boolean)
        rango = self.metadatos["rango_max_min"]
        estado_alerta = not (rango[0] <= valor <= rango[1])

        return {
            "timestamp": datetime.now().isoformat(),  # Tipo: Timestamp
            "valor": float(valor),  # Tipo: Float
            "alerta": estado_alerta,  # Tipo: Boolean
            "contexto": self.metadatos  # Metadatos (Datos sobre los datos)
        }


# --- Ejemplo 1 de Aplicación: Optimización de Bombeo ---
sensor_presion = SensorIndustrial("BOMBA_02", "PSI", (20.0, 80.0))

try:
    # Captura de un dato cuantitativo continuo
    resultado = sensor_presion.procesar_lectura(98)

    print(f"Lectura capturada: {resultado['valor']} {resultado['contexto']['unidad']}")
    print(f"Estado de alerta: {resultado['alerta']}")  # Muestra True si está fuera de rango
except Exception as e:
    print(f"Error en el flujo de datos: {e}")