from tortoise.models import Model
from tortoise import fields


class TransactionModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    date_created = fields.DatetimeField(auto_now_add=True)
    date_updated = fields.DatetimeField(auto_now=True)
    category = fields.CharField(max_length=60)
    balance = fields.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    delta = fields.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    user = fields.ForeignKeyField("models.UserModel", related_name="user")

    class Meta:
        table: str = "transactions"
