from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..db import get_session
from ..tables_models import ProcedimentoModel

from .models import ProcedimentoModelIn, ProcedimentoModelOut


router = APIRouter(prefix="/procedimentos", tags=["Procedimentos"])


@router.post("/")
async def create_procedimento(
    data: ProcedimentoModelIn, session: AsyncSession = Depends(get_session)
) -> ProcedimentoModelOut:
    procedimento = ProcedimentoModel(
        proc_nome=data.proc_nome,
        proc_valor=data.proc_valor,
    )
    session.add(procedimento)
    await session.commit()

    return procedimento


@router.get("/")
async def read_procedimentos(session: AsyncSession = Depends(get_session)) -> list[ProcedimentoModelOut]:
    procedimento_query = await session.execute(select(ProcedimentoModel))
    return procedimento_query.scalars().all()


@router.get("/{proc_codigo}")
async def read_procedimento(proc_codigo: int, session: AsyncSession = Depends(get_session)) -> ProcedimentoModelOut:
    procedimento_query = await session.execute(
        select(ProcedimentoModel).where(ProcedimentoModel.proc_codigo == proc_codigo)
    )
    procedimento = procedimento_query.scalars().first()

    if not procedimento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidade não encontrado")

    return procedimento


@router.patch("/{proc_codigo}")
async def update_procedimento(
    proc_codigo: int, data: ProcedimentoModelIn, session: AsyncSession = Depends(get_session)
) -> ProcedimentoModelOut:
    procedimento_query = await session.execute(
        select(ProcedimentoModel).where(ProcedimentoModel.proc_codigo == proc_codigo)
    )
    procedimento = procedimento_query.scalars().first()

    if not procedimento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidade não encontrado")

    procedimento.update(**data.dict(exclude_unset=True))

    session.add(procedimento)
    await session.commit()
    await session.refresh(procedimento)

    return procedimento


@router.delete("/{proc_codigo}")
async def delete_procedimento(proc_codigo: int, session: AsyncSession = Depends(get_session)):
    procedimento_query = await session.execute(
        select(ProcedimentoModel).where(ProcedimentoModel.proc_codigo == proc_codigo)
    )
    procedimento = procedimento_query.scalars().first()

    if not procedimento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidade não encontrado")

    await session.delete(procedimento)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
