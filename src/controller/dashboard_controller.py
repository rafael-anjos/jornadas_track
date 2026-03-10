from __future__ import annotations

import pandas as pd
from typing import TYPE_CHECKING

from service.employee_service import EmployeeService
from service.infraction_service import calcular_infracoes, Infraction
from models.employee import Employee

if TYPE_CHECKING:
    from view.dashboard_view import DashboardView
    from view.jornadas_view import JornadasView
    from view.infracoes_view import InfracoesView

def _fmt_data(ts) -> str:
    try:
        if ts is None or pd.isnull(ts):
            return "--"
        return ts.strftime("%d/%m/%Y")
    except Exception:
        return "--"


def _fmt_hora(dt) -> str:
    return dt.strftime("%H:%M") if dt else "--"


def _fmt_f(valor: float, decimais: int = 2) -> str:
    return f"{valor:.{decimais}f}"

InfracoesMap = dict[str, list[list[Infraction]]]

class DashboardController:
    def __init__(
        self,
        service:        "EmployeeService | None",
        dashboard_view: "DashboardView",
        jornadas_view:  "JornadasView",
        infracoes_view: "InfracoesView",
    ):
        self.service        = service
        self.dashboard_view = dashboard_view
        self.jornadas_view  = jornadas_view
        self.infracoes_view = infracoes_view

    def carregar(self, filepath: str) -> None:
        from repository.employee_repository import EmployeeRepository
        self.service = EmployeeService(EmployeeRepository(filepath))
        self.iniciar()

    def iniciar(self) -> None:
        if self.service is None:
            return
        employees = self.service.load()

        infracoes_map: InfracoesMap = {
            cpf: [calcular_infracoes(j) for j in emp.journeys]
            for cpf, emp in employees.items()
        }

        employees_sorted = sorted(employees.items(), key=lambda kv: kv[1].name)

        self._popular_dashboard(employees, employees_sorted, infracoes_map)
        self._popular_jornadas(employees_sorted, infracoes_map)
        self._popular_infracoes(employees_sorted, infracoes_map)

    def _popular_dashboard(
        self,
        employees:        dict[str, Employee],
        employees_sorted: list[tuple[str, Employee]],
        infracoes_map:    InfracoesMap,
    ) -> None:
        total_jornadas  = sum(len(e.journeys) for e in employees.values())
        total_folgas    = sum(
            1 for e in employees.values()
            for j in e.journeys if j.status == "Folga"
        )
        total_infracoes = sum(
            len(infs)
            for infs_emp in infracoes_map.values()
            for infs in infs_emp
        )

        self.dashboard_view.atualizar_cards({
            "funcionarios": len(employees),
            "jornadas":     total_jornadas,
            "folgas":       total_folgas,
            "infracoes":    total_infracoes,
        })

        rows = [
            {
                "nome":      emp.name,
                "cpf":       emp.cpf,
                "tipo":      "Plantonista" if emp.nightWorker else "Diarista",
                "jornadas":  len(emp.journeys),
                "folgas":    sum(1 for j in emp.journeys if j.status == "Folga"),
                "ferias":    sum(1 for j in emp.journeys if j.status == "Férias"),
                "extras":    round(
                    sum(j.stats.extra + j.stats.extra50 for j in emp.journeys), 2
                ),
                "faltas":    sum(1 for j in emp.journeys if j.status == "Falta"),
                "atestados": sum(1 for j in emp.journeys if j.status == "Atestado"),
                "diarias":   sum(1 for j in emp.journeys if j.daily),
                "infracoes": sum(len(infs) for infs in infracoes_map[cpf]),
            }
            for cpf, emp in employees_sorted
        ]

        nomes = [r["nome"] for r in rows]
        self.dashboard_view.popular_funcionarios(nomes)
        self.dashboard_view.atualizar_tabela(rows)

    def _popular_jornadas(
        self,
        employees_sorted: list[tuple[str, Employee]],
        infracoes_map:    InfracoesMap,
    ) -> None:
        nomes = [emp.name for _, emp in employees_sorted]
        self.jornadas_view.popular_funcionarios(nomes)

        rows = [
            (
                emp.name,
                _fmt_data(j.date),
                j.status,
                _fmt_hora(j.start),
                _fmt_hora(j.end),
                _fmt_f(j.total),
                _fmt_f(j.stats.drive),
                _fmt_f(j.stats.available),
                _fmt_f(j.stats.workTime),
                _fmt_f(j.inter),
                _fmt_f(j.stats.extra + j.stats.extra50),
                _fmt_f(j.stats.night),
                "Sim" if j.daily else "Não",
                _fmt_f(j.stats.travel, 0),
                _fmt_f(j.stats.speed, 1),
                len(infracoes_map[cpf][idx]),
            )
            for cpf, emp in employees_sorted
            for idx, j in enumerate(emp.journeys)
        ]

        self.jornadas_view.atualizar_tabela(rows)

    def _popular_infracoes(
        self,
        employees_sorted: list[tuple[str, Employee]],
        infracoes_map:    InfracoesMap,
    ) -> None:
        rows = [
            (
                emp.name,
                _fmt_data(j.date),
                inf.tipo,
                inf.descricao,
            )
            for cpf, emp in employees_sorted
            for idx, j in enumerate(emp.journeys)
            for inf in infracoes_map[cpf][idx]
        ]

        self.infracoes_view.atualizar_tabela(rows)
