from tortoise.models import Model
from passlib.hash import bcrypt
from tortoise import fields


class UserModel(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(null=False, max_length=60, unique=True)
    password_hash = fields.CharField(max_length=128)

    first_name = fields.CharField(max_length=30)
    last_name = fields.CharField(max_length=30)
    patronymic = fields.CharField(max_length=30)

    balance = fields.IntField()

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    class Meta:
        table: str = "users"
