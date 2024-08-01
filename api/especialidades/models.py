from pydantic import BaseModel, Field


class EspecialidadeModelIn(BaseModel):
    espec_nome: str = Field(max_length=50)


class EspecialidadeModelOut(EspecialidadeModelIn):
    espec_codigo: int
