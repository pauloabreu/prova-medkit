from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from ..db import get_session
from ..tables_models import ConsultaModel, MedicoModel, PlanoSaudeModel

from .models import ConsultaModelIn, PatchConsultaModelIn, ConsultaModelOut


router = APIRouter(prefix="/consultas", tags=["Consultas"])


@router.post("/")
async def create_consulta(data: ConsultaModelIn, session: AsyncSession = Depends(get_session)) -> ConsultaModelOut:
    medico_query = await session.execute(select(MedicoModel).where(MedicoModel.med_codigo == data.medico_codigo))
    medico = medico_query.scalars().first()

    if not medico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")

    consulta = ConsultaModel(
        data=data.data,
        particular=data.particular,
        paciente_codigo=data.paciente_codigo,
        medico_codigo=data.medico_codigo,
    )

    if plano_codigo := data.plano_codigo:
        plano_query = await session.execute(select(PlanoSaudeModel).where(PlanoSaudeModel.plan_codigo == plano_codigo))
        plano = plano_query.scalars().first()

        if not plano:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plano não encontrado")

        consulta.plano_codigo = plano_codigo

    session.add(consulta)
    await session.commit()

    return consulta


@router.get("/")
async def read_planos_saude(session: AsyncSession = Depends(get_session)) -> list[ConsultaModelOut]:
    consulta_query = await session.execute(
        select(ConsultaModel).options(
            joinedload(ConsultaModel.medico),
            joinedload(ConsultaModel.paciente),
            joinedload(ConsultaModel.procedimentos),
            joinedload(ConsultaModel.plano),
        )
    )
    return consulta_query.unique().scalars().all()


@router.get("/{cons_codigo}")
async def read_consulta(cons_codigo: int, session: AsyncSession = Depends(get_session)) -> ConsultaModelOut:
    consulta_query = await session.execute(
        select(ConsultaModel)
        .options(
            joinedload(ConsultaModel.medico),
            joinedload(ConsultaModel.paciente),
            joinedload(ConsultaModel.procedimentos),
            joinedload(ConsultaModel.plano),
        )
        .where(ConsultaModel.cons_codigo == cons_codigo)
    )
    consulta = consulta_query.scalars().first()

    if not consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")

    return consulta


@router.patch("/{cons_codigo}")
async def update_consulta(
    cons_codigo: int, data: PatchConsultaModelIn, session: AsyncSession = Depends(get_session)
) -> ConsultaModelOut:
    consulta_query = await session.execute(select(ConsultaModel).where(ConsultaModel.cons_codigo == cons_codigo))
    consulta = consulta_query.scalars().first()

    if not consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")

    consulta.update(**data.dict(exclude_unset=True))

    session.add(consulta)
    await session.commit()
    await session.refresh(consulta)

    return consulta


@router.delete("/{cons_codigo}")
async def delete_consulta(cons_codigo: int, session: AsyncSession = Depends(get_session)):
    consulta_query = await session.execute(select(ConsultaModel).where(ConsultaModel.cons_codigo == cons_codigo))
    consulta = consulta_query.scalars().first()

    if not consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")

    await session.delete(consulta)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
