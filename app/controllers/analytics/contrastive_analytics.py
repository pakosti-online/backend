from app.models.transaction import TransactionModel
from app.models.user import UserModel
from app.schemas.analytics import BalanceStructureAnalytics
from typing import List
from decimal import Decimal


MANDATORY_INCOMES = {"заработная плата", "пенсия"}
MANDATORY_EXPENSES = {"аренда", "коммунальные услуги", "проездной"}

    
def _is_mandatory(product_name: str, is_deposit: bool) -> bool:
    name = product_name.lower().strip()
    if is_deposit:
        return name in MANDATORY_INCOMES
    else:
        return name in MANDATORY_EXPENSES


async def get_balance_structure_analytics(user: UserModel) -> BalanceStructureAnalytics:
    transactions = await TransactionModel.filter(user=user).prefetch_related("category")

    mandatory_income = Decimal("0.00")
    non_mandatory_income = Decimal("0.00")
    mandatory_expense = Decimal("0.00")
    non_mandatory_expense = Decimal("0.00")

    for tx in transactions:
        is_deposit = tx.category.is_deposit
        is_mandatory = _is_mandatory(tx.product_name, is_deposit)

        if is_deposit and is_mandatory:
            mandatory_income += tx.delta
        elif is_deposit and not is_mandatory:
            non_mandatory_income += tx.delta
        elif not is_deposit and is_mandatory:
            mandatory_expense += tx.delta
        else:
            non_mandatory_expense += tx.delta

    balance = user.balance or Decimal("0.00")
    def safe_percent(value: Decimal) -> float:
        return float((value / balance) * 100) if balance > 0 else 0.0

    return BalanceStructureAnalytics(
        balance=balance,
        mandatory_income=mandatory_income,
        non_mandatory_income=non_mandatory_income,
        mandatory_expense=mandatory_expense,
        non_mandatory_expense=non_mandatory_expense,
        mandatory_income_percent=round(safe_percent(mandatory_income), 2),
        non_mandatory_income_percent=round(safe_percent(non_mandatory_income), 2),
        mandatory_expense_percent=round(safe_percent(mandatory_expense), 2),
        non_mandatory_expense_percent=round(safe_percent(non_mandatory_expense), 2),
    )
