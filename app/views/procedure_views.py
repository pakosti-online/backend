from fastapi import APIRouter
from app.schemas.procedure import ProcedureCreate, ProcedureId, ProcedureOut
import app.controllers.procedure as procedure_controller

router = APIRouter(prefix="/procedures", tags=["Procedures"])


@router.post("", response_model=ProcedureOut)
async def create_procedure(procedure: ProcedureCreate):
    """Создание транзакции"""
    return await procedure_controller.create(procedure)


@router.get("", response_model=list[ProcedureOut])
async def list_procedures():
    """Получение всех транзакций"""
    return await procedure_controller.get()
