from decimal import Decimal

from src.adapters.outbound.persistence.models.expense import ExpenseModel, ExpenseSplitModel, SplitTypeEnum
from src.domain.entities.expense import Expense, ExpenseSplit, SplitType


_SPLIT_TYPE_MAP = {
    SplitTypeEnum.EQUAL: SplitType.EQUAL,
    SplitTypeEnum.EXACT: SplitType.EXACT,
    SplitTypeEnum.PERCENTAGE: SplitType.PERCENTAGE,
}
_SPLIT_TYPE_REVERSE = {v: k for k, v in _SPLIT_TYPE_MAP.items()}


class ExpenseSplitMapper:
    @staticmethod
    def to_domain(model: ExpenseSplitModel) -> ExpenseSplit:
        return ExpenseSplit(
            id=model.id,
            expense_id=model.expense_id,
            user_id=model.user_id,
            amount=Decimal(str(model.amount)),
            percentage=Decimal(str(model.percentage)) if model.percentage else None,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: ExpenseSplit) -> ExpenseSplitModel:
        return ExpenseSplitModel(
            id=entity.id if entity.id else None,
            expense_id=entity.expense_id,
            user_id=entity.user_id,
            amount=entity.amount,
            percentage=entity.percentage,
        )


class ExpenseMapper:
    @staticmethod
    def to_domain(model: ExpenseModel) -> Expense:
        splits = [ExpenseSplitMapper.to_domain(s) for s in model.splits] if model.splits else []
        return Expense(
            id=model.id,
            title=model.title,
            amount=Decimal(str(model.amount)),
            group_id=model.group_id,
            created_by_id=model.created_by_id,
            split_type=_SPLIT_TYPE_MAP[model.split_type],
            description=model.description,
            currency=model.currency,
            created_at=model.created_at,
            updated_at=model.updated_at,
            splits=splits,
        )

    @staticmethod
    def to_model(entity: Expense) -> ExpenseModel:
        return ExpenseModel(
            id=entity.id if entity.id else None,
            title=entity.title,
            description=entity.description,
            amount=entity.amount,
            currency=entity.currency,
            split_type=_SPLIT_TYPE_REVERSE[entity.split_type],
            group_id=entity.group_id,
            created_by_id=entity.created_by_id,
        )
