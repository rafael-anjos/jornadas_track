import pandas as pd
from dataclasses import dataclass

@dataclass
class EmployeeRepository:
    filepath: str

    def load(self) -> pd.DataFrame:
        df = pd.read_excel(self.filepath, dtype=str)
        df.fillna("", inplace=True)
        return df
