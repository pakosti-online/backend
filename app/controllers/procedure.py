from app.models.procedure import ProcedureModel
from app.schemas.procedure import ProcedureCreate, ProcedureId



async def create_procedure(data: ProcedureCreate) -> ProcedureModel:
    procedure = await ProcedureModel.create(**data.model_dump())
    return procedure


async def change_procedure_by_id(data: ProcedureId) -> ProcedureModel:
    procedure_old = await ProcedureModel.get_or_none(id=data.id)
    procedure_new = create_procedure()
    
    return 