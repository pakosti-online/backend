from tortoise.models import Model
from passlib.hash import bcrypt
from tortoise import fields


class AvatarModel(Model):
    id = fields.IntField(pk=True)
    file_path = fields.CharField(
        max_length=255, null=True, default=None
    )  # Путь к файлу или URL

    class Meta:
        table: str = "avatars"


class UserModel(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(null=False, max_length=60, unique=True)
    password_hash = fields.CharField(max_length=128)

    first_name = fields.CharField(max_length=30)
    last_name = fields.CharField(max_length=30)
    patronymic = fields.CharField(max_length=30)

    balance = fields.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    avatar = fields.ForeignKeyField(
        "models.AvatarModel",
        related_name="users",
        null=True,
        on_delete=fields.SET_NULL,
    )

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    class Meta:
        table: str = "users"
