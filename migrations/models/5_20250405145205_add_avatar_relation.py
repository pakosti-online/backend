from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD COLUMN "avatar_id" INT;
        ALTER TABLE "users" ADD CONSTRAINT "fk_users_avatars_faee4bd7"
        FOREIGN KEY ("avatar_id") REFERENCES "avatars" ("id") ON DELETE SET NULL;
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP CONSTRAINT IF EXISTS "fk_users_avatars_faee4bd7";
        ALTER TABLE "users" DROP COLUMN "avatar_id";
    """
