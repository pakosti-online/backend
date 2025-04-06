from tortoise.models import Model
from tortoise import fields

class FinancesEducate(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    description = fields.TextField()
    
    class Meta:
        table = "finances_educate"