from tortoise.models import Model
from tortoise import fields


class TransactionCategoryModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    is_deposit = fields.BooleanField()

    class Meta:
        table = "transaction_types"


class TransactionModel(Model):
    id = fields.IntField(pk=True)
    product_name = fields.CharField(max_length=100)
    date_created = fields.DatetimeField(auto_now_add=True)
    balance = fields.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    delta = fields.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    user = fields.ForeignKeyField("models.UserModel", related_name="user")
    category = fields.ForeignKeyField(
        "models.TransactionCategoryModel", related_name="transactions"
    )

    class Meta:
        table: str = "transactions"
