from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..db import get_session
from ..tables_models import EspecialidadeModel

from .models import EspecialidadeModelIn, EspecialidadeModelOut


router = APIRouter(prefix="/especialidades", tags=["Especialidades"])


@router.post("/")
async def create_especialidade(
    data: EspecialidadeModelIn, session: AsyncSession = Depends(get_session)
) -> EspecialidadeModelOut:
    especialidade = EspecialidadeModel(espec_nome=data.espec_nome)
    session.add(especialidade)
    await session.commit()

    return especialidade


@router.get("/")
async def read_planos_saude(session: AsyncSession = Depends(get_session)) -> list[EspecialidadeModelOut]:
    especialidade_query = await session.execute(select(EspecialidadeModel))
    return especialidade_query.scalars().all()


@router.get("/{espec_codigo}")
async def read_especialidade(espec_codigo: int, session: AsyncSession = Depends(get_session)) -> EspecialidadeModelOut:
    especialidade_query = await session.execute(
        select(EspecialidadeModel).where(EspecialidadeModel.espec_codigo == espec_codigo)
    )
    especialidade = especialidade_query.scalars().first()

    if not especialidade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidade não encontrado")

    return especialidade


@router.patch("/{espec_codigo}")
async def update_especialidade(
    espec_codigo: int, data: EspecialidadeModelIn, session: AsyncSession = Depends(get_session)
) -> EspecialidadeModelOut:
    especialidade_query = await session.execute(
        select(EspecialidadeModel).where(EspecialidadeModel.espec_codigo == espec_codigo)
    )
    especialidade = especialidade_query.scalars().first()

    if not especialidade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidade não encontrado")

    especialidade.update(**data.dict(exclude_unset=True))

    session.add(especialidade)
    await session.commit()
    await session.refresh(especialidade)

    return especialidade


@router.delete("/{espec_codigo}")
async def delete_especialidade(espec_codigo: int, session: AsyncSession = Depends(get_session)):
    especialidade_query = await session.execute(
        select(EspecialidadeModel).where(EspecialidadeModel.espec_codigo == espec_codigo)
    )
    especialidade = especialidade_query.scalars().first()

    if not especialidade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidade não encontrado")

    await session.delete(especialidade)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
