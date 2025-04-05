from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_transaction_name_6e011b";
        ALTER TABLE "transaction_types" ADD "is_deposit" BOOL NOT NULL;
        ALTER TABLE "transaction_types" ALTER COLUMN "name" TYPE VARCHAR(100) USING "name"::VARCHAR(100);
        COMMENT ON COLUMN "transaction_types"."name" IS NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "transaction_types" DROP COLUMN "is_deposit";
        ALTER TABLE "transaction_types" ALTER COLUMN "name" TYPE VARCHAR(20) USING "name"::VARCHAR(20);
        COMMENT ON COLUMN "transaction_types"."name" IS 'ACCESSORIES: Аксессуары
RENT: Аренда
FOOD: Еда
SALARY: Зарплата
CLOTHES: Одежда и обувь
TRANSPORT: Транспорт
OTHER: Разное';
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_transaction_name_6e011b" ON "transaction_types" ("name");"""
