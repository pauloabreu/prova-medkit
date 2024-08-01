from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from ..db import get_session
from ..tables_models import MedicoModel, EspecialidadeModel

from .models import MedicoModelIn, PatchMedicoModelIn, MedicoModelOut


router = APIRouter(prefix="/medicos", tags=["Médicos"])


@router.post("/")
async def create_medico(data: MedicoModelIn, session: AsyncSession = Depends(get_session)) -> MedicoModelOut:
    especialidade_query = await session.execute(
        select(EspecialidadeModel).where(EspecialidadeModel.espec_codigo == data.especialidade_codigo)
    )
    especialidade = especialidade_query.scalars().first()

    if not especialidade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidade não encontrado")

    medico = MedicoModel(
        med_nome=data.med_nome,
        med_crm=data.med_crm,
        especialidade_codigo=data.especialidade_codigo,
    )

    session.add(medico)
    await session.commit()

    return medico


@router.get("/")
async def read_medicos(session: AsyncSession = Depends(get_session)) -> list[MedicoModelOut]:
    medico_query = await session.execute(
        select(MedicoModel).options(
            joinedload(MedicoModel.especialidade),
            joinedload(MedicoModel.consultas),
        )
    )
    return medico_query.unique().scalars().all()


@router.get("/{med_codigo}")
async def read_medico(med_codigo: int, session: AsyncSession = Depends(get_session)) -> MedicoModelOut:
    medico_query = await session.execute(
        select(MedicoModel)
        .options(
            joinedload(MedicoModel.especialidade),
            joinedload(MedicoModel.consultas),
        )
        .where(MedicoModel.med_codigo == med_codigo)
    )
    medico = medico_query.scalars().first()

    if not medico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")

    return medico


@router.patch("/{med_codigo}")
async def update_medico(
    med_codigo: int, data: PatchMedicoModelIn, session: AsyncSession = Depends(get_session)
) -> MedicoModelOut:
    medico_query = await session.execute(select(MedicoModel).where(MedicoModel.med_codigo == med_codigo))
    medico = medico_query.scalars().first()

    if not medico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")

    medico.update(**data.dict(exclude_unset=True))

    session.add(medico)
    await session.commit()
    await session.refresh(medico)

    return medico


@router.delete("/{med_codigo}")
async def delete_medico(med_codigo: int, session: AsyncSession = Depends(get_session)):
    medico_query = await session.execute(select(MedicoModel).where(MedicoModel.med_codigo == med_codigo))
    medico = medico_query.scalars().first()

    if not medico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Médico não encontrado")

    await session.delete(medico)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
