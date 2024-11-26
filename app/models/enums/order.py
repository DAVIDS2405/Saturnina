
from enum import Enum


class Estados_orden(str, Enum):
    P = "Pendiente"
    R = "Rechazado"
    En = "En entrega"
    F = "Finalizado"
