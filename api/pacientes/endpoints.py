from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from ..db import get_session
from ..tables_models import PacienteModel, PlanoSaudeModel, PacientePlanosModel

from .models import PacienteModelIn, PacienteModelOut, SubscribePacientePlanoSaudeModelIn


router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("/")
async def create_paciente(data: PacienteModelIn, session: AsyncSession = Depends(get_session)) -> PacienteModelOut:
    paciente = PacienteModel(
        pac_nome=data.pac_nome,
        pac_data_nascimento=data.pac_data_nascimento,
    )

    session.add(paciente)
    await session.commit()

    return paciente


@router.get("/")
async def read_pacientes(session: AsyncSession = Depends(get_session)) -> list[PacienteModelOut]:
    paciente_query = await session.execute(
        select(PacienteModel).options(
            joinedload(PacienteModel.planos),
            joinedload(PacienteModel.telefones),
            joinedload(PacienteModel.consultas),
        )
    )
    return paciente_query.unique().scalars().all()


@router.get("/{pac_codigo}")
async def read_paciente(pac_codigo: int, session: AsyncSession = Depends(get_session)) -> PacienteModelOut:
    paciente_query = await session.execute(
        select(PacienteModel)
        .options(
            joinedload(PacienteModel.planos),
            joinedload(PacienteModel.telefones),
            joinedload(PacienteModel.consultas),
        )
        .where(PacienteModel.pac_codigo == pac_codigo)
    )
    paciente = paciente_query.scalars().first()

    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    return paciente


@router.patch("/{pac_codigo}")
async def update_paciente(
    pac_codigo: int, data: PacienteModelIn, session: AsyncSession = Depends(get_session)
) -> PacienteModelOut:
    paciente_query = await session.execute(select(PacienteModel).where(PacienteModel.pac_codigo == pac_codigo))
    paciente = paciente_query.scalars().first()

    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    paciente.update(**data.dict(exclude_unset=True))

    session.add(paciente)
    await session.commit()
    await session.refresh(paciente)

    return paciente


@router.delete("/{pac_codigo}")
async def delete_paciente(pac_codigo: int, session: AsyncSession = Depends(get_session)):
    paciente_query = await session.execute(select(PacienteModel).where(PacienteModel.pac_codigo == pac_codigo))
    paciente = paciente_query.scalars().first()

    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    await session.delete(paciente)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/subscribe-plano")
async def sub_paciente_plano_saude(
    data: SubscribePacientePlanoSaudeModelIn, session: AsyncSession = Depends(get_session)
):
    paciente_query = await session.execute(select(PacienteModel).where(PacienteModel.pac_codigo == data.pac_codigo))
    paciente = paciente_query.scalars().first()

    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    plano_saude_query = await session.execute(
        select(PlanoSaudeModel).where(PlanoSaudeModel.plan_codigo == data.plan_codigo)
    )
    plano_saude = plano_saude_query.scalars().first()

    if not plano_saude:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plano de Saúde não encontrado")

    paciente_plano = PacientePlanosModel(
        paciente_codigo=paciente.pac_codigo,
        plano_codigo=plano_saude.plan_codigo,
        nr_contrato=data.nr_contrato,
    )

    session.add(paciente_plano)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/unsubscribe-plano")
async def unsub_paciente_plano_saude(
    data: SubscribePacientePlanoSaudeModelIn, session: AsyncSession = Depends(get_session)
):
    paciente_plano_query = await session.execute(
        select(PacientePlanosModel).where(
            PacientePlanosModel.paciente_codigo == data.pac_codigo,
            PacientePlanosModel.plano_codigo == data.plan_codigo,
        )
    )
    paciente_plano_saude = paciente_plano_query.scalars().first()

    if not paciente_plano_saude:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Paciente com esse Plano de Saúde não encontrado"
        )

    await session.delete(paciente_plano_saude)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
