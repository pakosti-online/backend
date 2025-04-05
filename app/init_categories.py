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
    for i in range(len(CLASSES)):
        category = await TransactionCategoryModel.get_or_none(name=CLASSES[i])
        if not category:
            category = TransactionCategoryModel.create(
                name=CLASSES[i], is_deposit=IS_DEP[i]
            )
        else:
            continue
