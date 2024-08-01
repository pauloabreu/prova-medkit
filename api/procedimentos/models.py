from decimal import Decimal
from pydantic import BaseModel, Field


class ProcedimentoModelIn(BaseModel):
    proc_nome: str = Field(max_length=50)
    proc_valor: Decimal


class ProcedimentoModelOut(ProcedimentoModelIn):
    proc_codigo: int
