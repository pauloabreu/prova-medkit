from typing import Optional, List
from pydantic import BaseModel, Field


class MedicoModelIn(BaseModel):
    med_nome: str = Field(max_length=100)
    med_crm: str = Field(max_length=9)
    especialidade_codigo: int


class PatchMedicoModelIn(BaseModel):
    med_nome: Optional[str] = Field(max_length=100)
    med_crm: Optional[str] = Field(max_length=9)
    especialidade_codigo: Optional[int]


class MedicoModelOut(MedicoModelIn):
    med_codigo: int
    especialidade: Optional[dict]
    consultas: Optional[List[dict]]

    def dict(self, *args, **kwargs):
        kwargs.pop("exclude_none")
        return super().dict(*args, exclude_none=True, **kwargs)
