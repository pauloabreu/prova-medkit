from datetime import datetime, date

from typing import List, Optional
from decimal import Decimal
from sqlmodel import SQLModel, Column, DECIMAL, DATE, Field, Relationship


class BaseModel(SQLModel):
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class PacientePlanosModel(SQLModel, table=True):
    __tablename__ = "paciente_plano"
    paciente_codigo: int = Field(primary_key=True, foreign_key="paciente.pac_codigo")
    plano_codigo: int = Field(foreign_key="plano_saucde.plan_codigo")
    nr_contrato: Optional[int] = Field(nullable=True)


class PacienteModel(BaseModel, table=True):
    __tablename__ = "paciente"
    pac_codigo: int = Field(primary_key=True)
    pac_data_nascimento: date = Field(sa_column=DATE)
    pac_nome: str = Field(max_length=100, nullable=False)
    planos: List["PlanoSaudeModel"] = Relationship(back_populates="pacientes", link_model=PacientePlanosModel)
    telefones: List["TelefoneModel"] = Relationship(back_populates="paciente", cascade_delete=True)
    consultas: List["ConsultaModel"] = Relationship(back_populates="paciente", cascade_delete=True)


class TelefoneModel(SQLModel, table=True):
    __tablename__ = "paciente_telefone"
    id: int = Field(primary_key=True)
    telefone: str = Field(max_length=11, nullable=False)
    paciente_codigo: int = Field(foreign_key="paciente.pac_codigo")
    paciente: Optional[PacienteModel] = Relationship(back_populates="telefones")


class ConsultaProcedimentoModel(SQLModel, table=True):
    __tablename__ = "consulta_procedimento"
    id_consulta: int = Field(foreign_key="consulta.cons_codigo", primary_key=True)
    id_procedimento: int = Field(foreign_key="procedimento.proc_codigo", primary_key=True)


class ConsultaModel(BaseModel, table=True):
    __tablename__ = "consulta"
    cons_codigo: int = Field(primary_key=True)
    data: datetime = Field(default=datetime.now(), nullable=False)
    particular: bool = Field(default=False, nullable=False)
    paciente_codigo: int = Field(foreign_key="paciente.pac_codigo")
    plano_codigo: Optional[int] = Field(foreign_key="plano_saucde.plan_codigo", nullable=True, ondelete="SET NULL")
    medico_codigo: int = Field(foreign_key="medico.med_codigo")
    medico: "MedicoModel" = Relationship(back_populates="consultas")
    paciente: "PacienteModel" = Relationship(back_populates="consultas")
    procedimentos: List["ProcedimentoModel"] = Relationship(
        back_populates="consultas", link_model=ConsultaProcedimentoModel
    )
    plano: Optional["PlanoSaudeModel"] = Relationship(back_populates="consultas")


class MedicoModel(BaseModel, table=True):
    __tablename__ = "medico"
    med_codigo: int = Field(primary_key=True)
    med_nome: str = Field(max_length=100, nullable=False)
    med_crm: str = Field(title="med_CRM", max_length=9, nullable=False)
    consultas: List[ConsultaModel] = Relationship(back_populates="medico", cascade_delete=True)
    especialidade: Optional["EspecialidadeModel"] = Relationship(back_populates="medicos")
    especialidade_codigo: int = Field(foreign_key="especialidade.espec_codigo")


class PlanoSaudeModel(BaseModel, table=True):
    __tablename__ = "plano_saucde"
    plan_codigo: int = Field(primary_key=True)
    plano_descricao: str = Field(max_length=50)
    plano_telefone: str = Field(max_length=11)
    pacientes: List[PacienteModel] = Relationship(back_populates="planos", link_model=PacientePlanosModel)
    consultas: List[ConsultaModel] = Relationship(back_populates="plano", cascade_delete=True)


class ProcedimentoModel(BaseModel, table=True):
    __tablename__ = "procedimento"
    proc_codigo: int = Field(primary_key=True)
    proc_nome: str = Field(max_length=50)
    proc_valor: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    consultas: List[ConsultaModel] = Relationship(back_populates="procedimentos", link_model=ConsultaProcedimentoModel)


class EspecialidadeModel(BaseModel, table=True):
    __tablename__ = "especialidade"
    espec_codigo: int = Field(primary_key=True)
    espec_nome: str = Field(max_length=50)
    medicos: List["MedicoModel"] = Relationship(back_populates="especialidade", cascade_delete=True)
