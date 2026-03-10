import pandas as pd
from dataclasses import dataclass
from datetime import datetime
from repository.employee_repository import EmployeeRepository
from models.employee import Employee
from models.journey import Journey
from models.stats import Stats

STATUS_MAP: dict[str, str] = {
    "FOLGA":              "Folga",
    "FERIAS":             "Férias",
    "FÉRIAS":             "Férias",
    "ATESTADO MÉDICO":    "Atestado",
    "ATESTADO MEDICO":    "Atestado",
    "ATESTADO":           "Atestado",
    "FALTA":              "Falta",
    "AFASTADO PELO INSS": "Afastado",
    "AFASTADO":           "Afastado",
    "":                   "Trabalhou",
}

@dataclass
class EmployeeService:
    repository: EmployeeRepository

    @staticmethod
    def _para_float(valor: str) -> float:
        if not valor or valor in ("--", "None"):
            return 0.0
        try:
            return float(valor)
        except ValueError:
            return 0.0

    @staticmethod
    def _para_hora(valor: str) -> datetime | None:
        if not valor or valor in ("--", "None"):
            return None
        try:
            return pd.to_datetime(valor, format="%H:%M").to_pydatetime()
        except Exception:
            return None

    @staticmethod
    def _para_bool(valor: str) -> bool:
        return str(valor).strip().lower() in ("t", "true", "sim", "1")

    @staticmethod
    def _mapear_status(valor: str) -> str:
        return STATUS_MAP.get(valor.strip().upper(), "Trabalhou")

    def load(self) -> dict[str, Employee]:
        df = self.repository.load()
        employees: dict[str, Employee] = {}

        for row in df.itertuples(index=False):
            cpf = row.CpfMotorista

            if cpf not in employees:
                employees[cpf] = Employee(
                    cpf=cpf,
                    name=row.Funcionario,
                    nightWorker=self._para_bool(row.Plantonista),
                )

            status_raw = row.StatusFuncionario
            status     = self._mapear_status(status_raw)
            data       = pd.to_datetime(row.DataApuracao, dayfirst=True, errors="coerce")

            stats = Stats(
                drive     = self._para_float(row.TotalDirecao),
                available = self._para_float(row.TotalDisposicao),
                workTime  = self._para_float(row.TotalTrabalhoEfetivo),
                extra     = self._para_float(row.TotalExtra100),
                extra50   = self._para_float(row.TotalExtra50),
                night     = self._para_float(row.TotalAdcNoturno),
                travel    = self._para_float(row.DeslocamentoKmDia),
                speed     = self._para_float(row.VelocidadeMedia),
                rest      = self._para_float(row.TotalDescanso),
                meal      = self._para_float(row.TotalRefeicao),
            )

            journey = Journey(
                date       = data,
                status     = status,
                status_raw = status_raw,
                start      = self._para_hora(row.PrimeiraLigada),
                end        = self._para_hora(row.UltimaDesligada),
                total      = self._para_float(row.TotalJornada),
                daily      = self._para_bool(row.TeveDiaria),
                inter      = self._para_float(row.TotalInterjornada),
                plate      = row.PlacaVeiculo,
                tracker    = row.Rastreador,
                group      = row.GrupoVeiculo,
                vehicle    = row.ClasseVeiculo,
                manobrista = self._para_bool(row.Manobrista),
                stats      = stats,
            )

            employees[cpf].journeys.append(journey)

        return employees
