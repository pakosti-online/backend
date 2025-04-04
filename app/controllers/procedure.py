from app.models.user import ProcedureModel
from app.schemas.user import Input_Procedure



async def create_procedure(data: Input_Procedure):
    user = await ProcedureModel.create