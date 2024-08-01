from fastapi import APIRouter, Depends

from api.user.endpoints import router as user_router
from api.pacientes.endpoints import router as pacientes_router
from api.planos.endpoints import router as planos_router
from api.consultas.endpoints import router as consultas_router
from api.medicos.endpoints import router as medicos_router
from api.especialidades.endpoints import router as especialidades_router
from api.procedimentos.endpoints import router as procedimentos_router

from .auth import auth_user

main_router = APIRouter(prefix="/medkit")
main_router.include_router(user_router)
main_router.include_router(pacientes_router, dependencies=[Depends(auth_user)])
main_router.include_router(planos_router, dependencies=[Depends(auth_user)])
main_router.include_router(consultas_router, dependencies=[Depends(auth_user)])
main_router.include_router(medicos_router, dependencies=[Depends(auth_user)])
main_router.include_router(especialidades_router, dependencies=[Depends(auth_user)])
main_router.include_router(procedimentos_router, dependencies=[Depends(auth_user)])
