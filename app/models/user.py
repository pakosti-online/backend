from passlib.hash import bcrypt
from tortoise import fields
from tortoise.models import Model


class UserModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(null=False, max_length=40)
    surname = fields.CharField(null=False, max_length=40)
    patronymic = fields.CharField(null=False, max_length=40)
    login = fields.CharField(null=False, max_length=40, unique=True)
    password = fields.CharField(max_length=60)
    name = fields.CharField(null=False, max_length=40)
    role = fields.CharField(max_length=20, default="client")  # admin, client

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    class Meta:
        table: str = "users"
