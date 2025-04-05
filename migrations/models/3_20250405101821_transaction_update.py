from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "transaction_types" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(20) NOT NULL UNIQUE
);
COMMENT ON COLUMN "transaction_types"."name" IS 'ACCESSORIES: Аксессуары\nRENT: Аренда\nFOOD: Еда\nSALARY: Зарплата\nCLOTHES: Одежда и обувь\nTRANSPORT: Транспорт\nOTHER: Разное';
        ALTER TABLE "transactions" ADD "category_id" INT NOT NULL;
        ALTER TABLE "transactions" RENAME COLUMN "name" TO "product_name";
        ALTER TABLE "transactions" DROP COLUMN "date_updated";
        ALTER TABLE "transactions" DROP COLUMN "category";
        ALTER TABLE "transactions" ADD CONSTRAINT "fk_transact_transact_86617030" FOREIGN KEY ("category_id") REFERENCES "transaction_types" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "transactions" DROP CONSTRAINT IF EXISTS "fk_transact_transact_86617030";
        ALTER TABLE "transactions" ADD "date_updated" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "transactions" ADD "category" VARCHAR(60) NOT NULL;
        ALTER TABLE "transactions" RENAME COLUMN "product_name" TO "name";
        ALTER TABLE "transactions" DROP COLUMN "category_id";
        DROP TABLE IF EXISTS "transaction_types";"""
