from __future__ import annotations
from dataclasses import dataclass
from models.journey import Journey

TIPO_JORNADA      = "Jornada"
TIPO_REFEICAO     = "Refeição"
TIPO_EXTRA        = "Extra"
TIPO_DISPOSICAO   = "Disposição"
TIPO_INTERJORNADA = "Interjornada"

TODOS_TIPOS = [
    TIPO_JORNADA,
    TIPO_REFEICAO,
    TIPO_EXTRA,
    TIPO_DISPOSICAO,
    TIPO_INTERJORNADA,
]


@dataclass(frozen=True)
class Infraction:
    tipo:      str
    descricao: str

def _check_jornada(j: Journey) -> Infraction | None:
    if j.total > 12:
        return Infraction(
            tipo=TIPO_JORNADA,
            descricao=f"Jornada excede 12h ({j.total:.2f}h registradas)",
        )
    return None

def _check_refeicao(j: Journey) -> Infraction | None:
    if j.status != "Trabalhou":
        return None

    meal = j.stats.meal

    if meal > 2:
        return Infraction(
            tipo=TIPO_REFEICAO,
            descricao=f"Refeição excede 2h ({meal:.2f}h registradas)",
        )

    if j.total > 6 and meal < 1:
        motivo = "sem registro" if meal == 0 else f"{meal:.2f}h registrada"
        return Infraction(
            tipo=TIPO_REFEICAO,
            descricao=f"Refeição abaixo de 1h com jornada > 6h ({motivo})",
        )

    return None

def _check_extra(j: Journey) -> Infraction | None:
    extra_total = j.stats.extra + j.stats.extra50
    if extra_total > 4:
        return Infraction(
            tipo=TIPO_EXTRA,
            descricao=f"Extra excede 4h ({extra_total:.2f}h registradas)",
        )
    return None


def _check_disposicao(j: Journey) -> Infraction | None:
    if j.stats.available > 8:
        return Infraction(
            tipo=TIPO_DISPOSICAO,
            descricao=f"Disposição excede 8h ({j.stats.available:.2f}h registradas)",
        )
    return None

def _check_interjornada(j: Journey) -> Infraction | None:
    # Só aplica se jornada > 4h e trabalho efetivo > 2h
    if j.total <= 4 or j.stats.workTime <= 2:
        return None
    if j.inter > 0 and j.inter < 11:
        return Infraction(
            tipo=TIPO_INTERJORNADA,
            descricao=f"Interjornada abaixo de 11h ({j.inter:.2f}h registradas)",
        )
    return None

_CHECKS = [
    _check_jornada,
    _check_refeicao,
    _check_extra,
    _check_disposicao,
    _check_interjornada,
]


def calcular_infracoes(j: Journey) -> list[Infraction]:
    return [inf for check in _CHECKS if (inf := check(j)) is not None]
