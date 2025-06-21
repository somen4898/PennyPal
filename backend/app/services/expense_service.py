from typing import List
from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.expense import Expense, ExpenseSplit, SplitType
from app.models.group import GroupMember
from app.schemas.expense import ExpenseCreate

def calculate_splits(expense: ExpenseCreate, db: Session) -> List[dict]:
    """Calculate split amounts based on split type"""
    splits = []
    
    if expense.split_type == SplitType.EQUAL:
        # Equal split among all users
        amount_per_person = expense.amount / len(expense.splits)
        for split in expense.splits:
            splits.append({
                "user_id": split.user_id,
                "amount": amount_per_person,
                "percentage": None
            })
    
    elif expense.split_type == SplitType.EXACT:
        # Exact amounts specified
        total_specified = sum(split.amount for split in expense.splits if split.amount)
        if total_specified != expense.amount:
            raise ValueError("Sum of split amounts must equal total expense amount")
        
        for split in expense.splits:
            if split.amount is None:
                raise ValueError("Amount must be specified for exact splits")
            splits.append({
                "user_id": split.user_id,
                "amount": split.amount,
                "percentage": None
            })
    
    elif expense.split_type == SplitType.PERCENTAGE:
        # Percentage-based splits
        total_percentage = sum(split.percentage for split in expense.splits if split.percentage)
        if abs(total_percentage - 100) > 0.01:  # Allow for small floating point errors
            raise ValueError("Percentages must sum to 100")
        
        for split in expense.splits:
            if split.percentage is None:
                raise ValueError("Percentage must be specified for percentage splits")
            amount = (expense.amount * split.percentage) / 100
            splits.append({
                "user_id": split.user_id,
                "amount": amount,
                "percentage": split.percentage
            })
    
    return splits

def validate_group_members(expense: ExpenseCreate, db: Session) -> bool:
    """Validate that all users in splits are members of the group"""
    user_ids = [split.user_id for split in expense.splits]
    
    # Check if all users are members of the group
    member_count = db.query(GroupMember).filter(
        GroupMember.group_id == expense.group_id,
        GroupMember.user_id.in_(user_ids)
    ).count()
    
    return member_count == len(user_ids)