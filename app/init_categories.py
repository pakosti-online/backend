from app.models.transaction import TransactionCategoryModel


CLASSES = [
    "Аксессуары",
    "Аренда",
    "Еда",
    "Зарплата",
    "Одежда и обувь",
    "Разное",
    "Транспорт",
]

IS_DEP = [
    False,
    False,
    False,
    True,
    False,
    False,
    False,
]


async def create_categories() -> None:
    for name, is_deposit in zip(CLASSES, IS_DEP):
        category, created = await TransactionCategoryModel.get_or_create(
            name=name,
            defaults={'is_deposit': is_deposit}
        )
    print("Все категории были успешно загружены")