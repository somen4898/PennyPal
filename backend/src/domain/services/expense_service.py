from decimal import Decimal
from typing import Any

from src.domain.entities.expense import SplitType
from src.domain.exceptions import ValidationError


def calculate_splits(
    total_amount: Decimal,
    split_type: SplitType,
    user_ids: list[int],
    split_amounts: list[Decimal] | None,
    split_percentages: list[Decimal] | None,
) -> list[dict[str, Any]]:
    """Calculate split amounts based on split type. Pure function — no DB access."""
    if not user_ids:
        raise ValidationError("At least one user is required for splitting")

    splits: list[dict[str, Any]] = []

    if split_type == SplitType.EQUAL:
        amount_per_person = total_amount / len(user_ids)
        for uid in user_ids:
            splits.append({"user_id": uid, "amount": amount_per_person, "percentage": None})

    elif split_type == SplitType.EXACT:
        if split_amounts is None or len(split_amounts) != len(user_ids):
            raise ValidationError("Amount must be specified for each user in exact splits")
        total_specified = sum(split_amounts)
        if total_specified != total_amount:
            raise ValidationError("Sum of split amounts must equal total expense amount")
        for uid, amount in zip(user_ids, split_amounts, strict=False):
            splits.append({"user_id": uid, "amount": amount, "percentage": None})

    elif split_type == SplitType.PERCENTAGE:
        if split_percentages is None or len(split_percentages) != len(user_ids):
            raise ValidationError("Percentage must be specified for each user in percentage splits")
        total_pct = sum(split_percentages)
        if abs(total_pct - Decimal("100")) > Decimal("0.01"):
            raise ValidationError("Percentages must sum to 100")
        for uid, pct in zip(user_ids, split_percentages, strict=False):
            amount = (total_amount * pct) / Decimal("100")
            splits.append({"user_id": uid, "amount": amount, "percentage": pct})

    return splits
