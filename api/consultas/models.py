from datetime import date, datetime

from typing import Optional, List
from pydantic import BaseModel, validator


class ConsultaModelIn(BaseModel):
    data: date
    particular: bool
    paciente_codigo: int
    plano_codigo: Optional[int]
    medico_codigo: int

    @validator("data", pre=True)
    def parse_data(cls, value):
        return datetime.strptime(value, "%d/%m/%Y").date()


class PatchConsultaModelIn(ConsultaModelIn):
    data: Optional[date]
    particular: Optional[bool]
    paciente_codigo: Optional[int]
    plano_codigo: Optional[int]
    medico_codigo: Optional[int]


class ConsultaModelOut(ConsultaModelIn):
    cons_codigo: int
    data: str
    medico: Optional[dict]
    paciente: Optional[dict]
    procedimentos: Optional[List[dict]]
    plano: Optional[dict]

    @validator("data", pre=True)
    def parse_data(cls, value):
        return datetime.strftime(value, "%d/%m/%Y")

    def dict(self, *args, **kwargs):
        kwargs.pop("exclude_none")
        return super().dict(*args, exclude_none=True, **kwargs)
