from tortoise.models import Model
from tortoise import fields



class ProcedureModel(Model):
    id = fields.IntField(pk=True)
    name = fields.Charfield(max_length=100)
    date_created = fields.DatetimeField(auto_now_add=True)
    date_updated = fields.DatetimeField(auto_now=True)
    category = fields.CharField(max_length=60)


    class Meta:
        table: str = "procedures"