from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.group import Group, GroupMember
from app.models.expense import Expense, ExpenseSplit, SplitType
from app.models.settlement import Settlement, SettlementStatus
from app.schemas.chatbot import ChatRequest, ChatResponse
from app.schemas.expense import ExpenseCreate, ExpenseSplitCreate
from app.schemas.settlement import SettlementCreate
from app.services.chatbot_service import ChatbotService
from app.services.expense_service import calculate_splits, validate_group_members
from decimal import Decimal

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_with_bot(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Main chat endpoint for natural language processing"""
    chatbot = ChatbotService(db, current_user)
    
    try:
        result = chatbot.process_message(chat_request.message, chat_request.group_id)
        
        return ChatResponse(
            response=result["response"],
            actions_taken=result.get("actions_taken", []),
            suggested_actions=result.get("suggested_actions", [])
        )
    
    except Exception as e:
        return ChatResponse(
            response="I'm sorry, I encountered an error processing your message. Please try again.",
            actions_taken=[],
            suggested_actions=[]
        )

@router.post("/execute-action")
def execute_suggested_action(
    action_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a suggested action from the chatbot"""
    action_type = action_data.get("action")
    
    try:
        if action_type == "confirm_expense":
            return _create_expense_from_action(action_data, current_user, db)
        
        elif action_type == "confirm_settlement":
            return _create_settlement_from_action(action_data, current_user, db)
        
        elif action_type == "show_balance":
            return _show_user_balance(current_user, db)
        
        elif action_type == "show_groups":
            return _show_user_groups(current_user, db)
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown action type: {action_type}"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to execute action: {str(e)}"
        )

def _create_expense_from_action(action_data: Dict, current_user: User, db: Session):
    """Create an expense from chatbot action data"""
    group_id = action_data.get("group_id")
    title = action_data.get("title", "Expense")
    amount = Decimal(str(action_data.get("amount", 0)))
    
    if not group_id or amount <= 0:
        raise ValueError("Invalid expense data")
    
    # Check if user is member of the group
    membership = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise ValueError("Not a member of this group")
    
    # Get all group members for equal split
    group_members = db.query(GroupMember).filter(
        GroupMember.group_id == group_id
    ).all()
    
    # Create expense splits for all members
    splits = []
    for member in group_members:
        splits.append(ExpenseSplitCreate(
            user_id=member.user_id,
            amount=None,  # Will be calculated for equal split
            percentage=None
        ))
    
    expense_create = ExpenseCreate(
        title=title,
        description=f"Added via chatbot",
        amount=amount,
        currency="USD",
        split_type=SplitType.EQUAL,
        group_id=group_id,
        splits=splits
    )
    
    # Validate and calculate splits
    if not validate_group_members(expense_create, db):
        raise ValueError("Invalid group members")
    
    calculated_splits = calculate_splits(expense_create, db)
    
    # Create expense
    db_expense = Expense(
        title=expense_create.title,
        description=expense_create.description,
        amount=expense_create.amount,
        currency=expense_create.currency,
        split_type=expense_create.split_type,
        group_id=expense_create.group_id,
        created_by_id=current_user.id
    )
    
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    # Create expense splits
    for split_data in calculated_splits:
        expense_split = ExpenseSplit(
            expense_id=db_expense.id,
            user_id=split_data["user_id"],
            amount=split_data["amount"],
            percentage=split_data["percentage"]
        )
        db.add(expense_split)
    
    db.commit()
    
    return {
        "message": f"Expense '{title}' for ${amount} added successfully!",
        "expense_id": db_expense.id
    }

def _create_settlement_from_action(action_data: Dict, current_user: User, db: Session):
    """Create a settlement from chatbot action data"""
    payee_id = action_data.get("payee_id")
    amount = Decimal(str(action_data.get("amount", 0)))
    group_id = action_data.get("group_id")
    
    if not payee_id or amount <= 0:
        raise ValueError("Invalid settlement data")
    
    # Verify payee exists
    payee = db.query(User).filter(User.id == payee_id).first()
    if not payee:
        raise ValueError("Payee not found")
    
    settlement_create = SettlementCreate(
        payee_id=payee_id,
        amount=amount,
        currency="USD",
        description="Created via chatbot",
        group_id=group_id
    )
    
    # If group_id is provided, verify both users are members
    if group_id:
        payer_membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == current_user.id
        ).first()
        
        payee_membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == payee_id
        ).first()
        
        if not payer_membership or not payee_membership:
            raise ValueError("Both users must be members of the group")
    
    db_settlement = Settlement(
        payer_id=current_user.id,
        payee_id=settlement_create.payee_id,
        amount=settlement_create.amount,
        currency=settlement_create.currency,
        description=settlement_create.description,
        group_id=settlement_create.group_id,
        status=SettlementStatus.PENDING
    )
    
    db.add(db_settlement)
    db.commit()
    db.refresh(db_settlement)
    
    return {
        "message": f"Settlement of ${amount} to {payee.full_name} created successfully!",
        "settlement_id": db_settlement.id
    }

def _show_user_balance(current_user: User, db: Session):
    """Show user's overall balance"""
    from app.services.settlement_service import calculate_group_balances
    
    groups = db.query(GroupMember).filter(GroupMember.user_id == current_user.id).all()
    
    total_balance = Decimal('0')
    group_balances = {}
    
    for membership in groups:
        group_id = membership.group_id
        balances = calculate_group_balances(group_id, db)
        user_balance = balances.get(current_user.id, Decimal('0'))
        
        if user_balance != 0:
            group = db.query(Group).filter(Group.id == group_id).first()
            group_name = group.name if group else f"Group {group_id}"
            group_balances[group_name] = float(user_balance)
            total_balance += user_balance
    
    return {
        "total_balance": float(total_balance),
        "group_balances": group_balances
    }

def _show_user_groups(current_user: User, db: Session):
    """Show user's groups with basic info"""
    groups = db.query(Group).join(GroupMember).filter(
        GroupMember.user_id == current_user.id
    ).all()
    
    group_info = []
    for group in groups:
        member_count = db.query(GroupMember).filter(
            GroupMember.group_id == group.id
        ).count()
        
        expense_count = db.query(Expense).filter(
            Expense.group_id == group.id
        ).count()
        
        group_info.append({
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "member_count": member_count,
            "expense_count": expense_count
        })
    
    return {
        "groups": group_info,
        "total_groups": len(group_info)
    }

@router.get("/quick-actions")
def get_quick_actions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get suggested quick actions for the user"""
    groups = db.query(Group).join(GroupMember).filter(
        GroupMember.user_id == current_user.id
    ).limit(3).all()
    
    quick_actions = [
        {
            "title": "Check my balance",
            "action": "show_balance",
            "description": "See how much you owe or are owed"
        },
        {
            "title": "View my groups",
            "action": "show_groups", 
            "description": "See all your expense groups"
        }
    ]
    
    # Add group-specific quick actions
    for group in groups:
        quick_actions.append({
            "title": f"Add expense to {group.name}",
            "action": "add_expense",
            "group_id": group.id,
            "group_name": group.name,
            "description": f"Quickly add an expense to {group.name}"
        })
    
    return {"quick_actions": quick_actions}