from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "transaction_edits" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "product_name" VARCHAR(100) NOT NULL,
    "category_id" INT NOT NULL REFERENCES "transaction_types" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "transaction_edits";"""
