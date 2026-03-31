from collections import defaultdict
from decimal import Decimal
from typing import Any


def calculate_balances_from_splits(
    splits: list[dict[str, Any]],
) -> dict[int, Decimal]:
    """Calculate net balances from expense split data. Pure function.

    Each split dict must have: expense_creator_id, user_id, amount, total_amount
    Positive balance = user is owed money. Negative = user owes money.
    """
    balances: dict[int, Decimal] = defaultdict(Decimal)

    for split in splits:
        creator_id = split["expense_creator_id"]
        user_id = split["user_id"]
        amount = split["amount"]

        if user_id != creator_id:
            balances[user_id] -= amount
            balances[creator_id] += amount

    return dict(balances)


def generate_settlement_suggestions(
    balances: dict[int, Decimal],
    group_id: int,
) -> list[dict[str, Any]]:
    """Greedy algorithm to minimize settlement transactions. Pure function."""
    # Filter out zero balances
    filtered = {uid: bal for uid, bal in balances.items() if bal != Decimal("0")}

    creditors = sorted(
        [(uid, amt) for uid, amt in filtered.items() if amt > 0],
        key=lambda x: x[1],
        reverse=True,
    )
    debtors = sorted(
        [(uid, -amt) for uid, amt in filtered.items() if amt < 0],
        key=lambda x: x[1],
        reverse=True,
    )

    settlements: list[dict[str, Any]] = []
    i, j = 0, 0

    while i < len(creditors) and j < len(debtors):
        creditor_id, credit_amount = creditors[i]
        debtor_id, debt_amount = debtors[j]
        settlement_amount = min(credit_amount, debt_amount)

        settlements.append(
            {
                "payer_id": debtor_id,
                "payee_id": creditor_id,
                "amount": settlement_amount,
                "group_id": group_id,
            }
        )

        creditors[i] = (creditor_id, credit_amount - settlement_amount)
        debtors[j] = (debtor_id, debt_amount - settlement_amount)

        if creditors[i][1] == Decimal("0"):
            i += 1
        if debtors[j][1] == Decimal("0"):
            j += 1

    return settlements
