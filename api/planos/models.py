from typing import Optional, List
from pydantic import BaseModel, Field


class PlanoSaudeModelIn(BaseModel):
    plano_descricao: str = Field(max_length=50)
    plano_telefone: str = Field(max_length=11)


class PlanoSaudeModelOut(PlanoSaudeModelIn):
    plan_codigo: int
    pacientes: Optional[List[dict]]

    def dict(self, *args, **kwargs):
        kwargs.pop("exclude_none")
        return super().dict(*args, exclude_none=True, **kwargs)
