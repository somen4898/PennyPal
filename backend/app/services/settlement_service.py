from typing import List, Dict
from decimal import Decimal
from sqlalchemy.orm import Session
from collections import defaultdict
from app.models.expense import ExpenseSplit
from app.models.group import GroupMember
from app.models.settlement import Settlement, SettlementStatus

def calculate_group_balances(group_id: int, db: Session) -> Dict[int, Decimal]:
    """Calculate net balances for all users in a group"""
    balances = defaultdict(Decimal)
    
    # Get all expense splits for the group
    splits = db.query(ExpenseSplit).join(
        ExpenseSplit.expense
    ).filter(
        ExpenseSplit.expense.has(group_id=group_id)
    ).all()
    
    # Calculate how much each user owes (negative) or is owed (positive)
    for split in splits:
        expense = split.expense
        created_by_id = expense.created_by_id
        user_id = split.user_id
        amount = split.amount
        
        if user_id == created_by_id:
            # User paid for their own split - they are owed the total minus their split
            balances[user_id] += expense.amount - amount
        else:
            # User owes their split amount
            balances[user_id] -= amount
            # Creator is owed this amount
            balances[created_by_id] += amount
    
    return dict(balances)

def generate_settlement_suggestions(group_id: int, db: Session) -> List[Dict]:
    """Generate optimal settlement suggestions to minimize transactions"""
    balances = calculate_group_balances(group_id, db)
    
    # Filter out zero balances
    balances = {user_id: balance for user_id, balance in balances.items() if balance != 0}
    
    settlements = []
    
    # Simple greedy algorithm to minimize transactions
    creditors = [(user_id, amount) for user_id, amount in balances.items() if amount > 0]
    debtors = [(user_id, -amount) for user_id, amount in balances.items() if amount < 0]
    
    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)
    
    i, j = 0, 0
    while i < len(creditors) and j < len(debtors):
        creditor_id, credit_amount = creditors[i]
        debtor_id, debt_amount = debtors[j]
        
        settlement_amount = min(credit_amount, debt_amount)
        
        settlements.append({
            'payer_id': debtor_id,
            'payee_id': creditor_id,
            'amount': settlement_amount,
            'group_id': group_id
        })
        
        creditors[i] = (creditor_id, credit_amount - settlement_amount)
        debtors[j] = (debtor_id, debt_amount - settlement_amount)
        
        if creditors[i][1] == 0:
            i += 1
        if debtors[j][1] == 0:
            j += 1
    
    return settlements

def get_user_balance_in_group(user_id: int, group_id: int, db: Session) -> Decimal:
    """Get a specific user's balance in a group"""
    balances = calculate_group_balances(group_id, db)
    return balances.get(user_id, Decimal('0'))