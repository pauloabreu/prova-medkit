from datetime import datetime, date

from typing import Optional
from pydantic import BaseModel, Field, validator

from ..planos.models import PlanoSaudeModelOut
from ..consultas.models import ConsultaModelOut


class PacienteModelIn(BaseModel):
    pac_nome: str = Field(max_length=100)
    pac_data_nascimento: date

    @validator("pac_data_nascimento", pre=True)
    def parse_data_nascimento(cls, value):
        return datetime.strptime(value, "%d/%m/%Y").date()


class PacienteModelOut(PacienteModelIn):
    pac_codigo: int
    pac_data_nascimento: str
    planos: Optional[list[PlanoSaudeModelOut]]
    telefones: Optional[list[dict]]
    consultas: Optional[list[ConsultaModelOut]]

    @validator("pac_data_nascimento", pre=True)
    def parse_data_nascimento(cls, value):
        return datetime.strftime(value, "%d/%m/%Y")

    def dict(self, *args, **kwargs):
        kwargs.pop("exclude_none")
        return super().dict(*args, exclude_none=True, **kwargs)


class SubscribePacientePlanoSaudeModelIn(BaseModel):
    plan_codigo: int
    pac_codigo: int
    nr_contrato: Optional[str] = Field(max_length=11)
