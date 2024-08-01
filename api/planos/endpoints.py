from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from ..db import get_session
from ..tables_models import PlanoSaudeModel

from .models import PlanoSaudeModelIn, PlanoSaudeModelOut


router = APIRouter(prefix="/planos", tags=["Planos de Saúde"])


@router.post("/")
async def create_plano_saude(
    data: PlanoSaudeModelIn, session: AsyncSession = Depends(get_session)
) -> PlanoSaudeModelOut:
    plano_saude = PlanoSaudeModel(
        plano_descricao=data.plano_descricao,
        plano_telefone=data.plano_telefone,
    )

    session.add(plano_saude)
    await session.commit()

    return plano_saude


@router.get("/")
async def read_planos_saude(session: AsyncSession = Depends(get_session)) -> list[PlanoSaudeModelOut]:
    plano_saude_query = await session.execute(select(PlanoSaudeModel).options(joinedload(PlanoSaudeModel.pacientes)))
    return plano_saude_query.unique().scalars().all()


@router.get("/{plan_codigo}")
async def read_plano_saude(plan_codigo: int, session: AsyncSession = Depends(get_session)) -> PlanoSaudeModelOut:
    plano_saude_query = await session.execute(
        select(PlanoSaudeModel)
        .where(PlanoSaudeModel.plan_codigo == plan_codigo)
        .options(joinedload(PlanoSaudeModel.pacientes))
    )
    plano_saude = plano_saude_query.scalars().first()

    if not plano_saude:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plano de Saúde não encontrado")

    return plano_saude


@router.patch("/{plan_codigo}")
async def update_plano_saude(
    plan_codigo: int, data: PlanoSaudeModelIn, session: AsyncSession = Depends(get_session)
) -> PlanoSaudeModelOut:
    plano_saude_query = await session.execute(
        select(PlanoSaudeModel).where(PlanoSaudeModel.plan_codigo == plan_codigo)
    )
    plano_saude = plano_saude_query.scalars().first()

    if not plano_saude:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plano de Saúde não encontrado")

    plano_saude.update(**data.dict(exclude_unset=True))

    session.add(plano_saude)
    await session.commit()
    await session.refresh(plano_saude)

    return plano_saude


@router.delete("/{plan_codigo}")
async def delete_plano_saude(plan_codigo: int, session: AsyncSession = Depends(get_session)):
    plano_saude_query = await session.execute(
        select(PlanoSaudeModel).where(PlanoSaudeModel.plan_codigo == plan_codigo)
    )
    plano_saude = plano_saude_query.scalars().first()

    if not plano_saude:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plano de Saúde não encontrado")

    await session.delete(plano_saude)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
