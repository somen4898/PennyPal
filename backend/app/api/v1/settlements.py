from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
from decimal import Decimal

from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.group import GroupMember
from app.models.settlement import Settlement, SettlementStatus
from app.schemas.settlement import SettlementCreate, SettlementResponse, SettlementUpdate
from app.services.settlement_service import (
    calculate_group_balances, 
    generate_settlement_suggestions,
    get_user_balance_in_group
)

router = APIRouter()

@router.post("/", response_model=SettlementResponse)
def create_settlement(
    settlement: SettlementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify payee exists
    payee = db.query(User).filter(User.id == settlement.payee_id).first()
    if not payee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payee not found"
        )
    
    # If group_id is provided, verify both users are members
    if settlement.group_id:
        payer_membership = db.query(GroupMember).filter(
            GroupMember.group_id == settlement.group_id,
            GroupMember.user_id == current_user.id
        ).first()
        
        payee_membership = db.query(GroupMember).filter(
            GroupMember.group_id == settlement.group_id,
            GroupMember.user_id == settlement.payee_id
        ).first()
        
        if not payer_membership or not payee_membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Both users must be members of the group"
            )
    
    db_settlement = Settlement(
        payer_id=current_user.id,
        payee_id=settlement.payee_id,
        amount=settlement.amount,
        currency=settlement.currency,
        description=settlement.description,
        group_id=settlement.group_id,
        status=SettlementStatus.PENDING
    )
    
    db.add(db_settlement)
    db.commit()
    db.refresh(db_settlement)
    
    return db_settlement

@router.get("/", response_model=List[SettlementResponse])
def get_user_settlements(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    settlements = db.query(Settlement).filter(
        (Settlement.payer_id == current_user.id) | 
        (Settlement.payee_id == current_user.id)
    ).offset(skip).limit(limit).all()
    
    return settlements

@router.get("/group/{group_id}", response_model=List[SettlementResponse])
def get_group_settlements(
    group_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user is member of the group
    membership = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this group"
        )
    
    settlements = db.query(Settlement).filter(
        Settlement.group_id == group_id
    ).offset(skip).limit(limit).all()
    
    return settlements

@router.get("/group/{group_id}/balances")
def get_group_balances(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Decimal]:
    # Check if user is member of the group
    membership = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this group"
        )
    
    balances = calculate_group_balances(group_id, db)
    
    # Convert user_ids to usernames for better readability
    result = {}
    for user_id, balance in balances.items():
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            result[user.username] = balance
    
    return result

@router.get("/group/{group_id}/suggestions")
def get_settlement_suggestions(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user is member of the group
    membership = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this group"
        )
    
    suggestions = generate_settlement_suggestions(group_id, db)
    
    # Add user details to suggestions
    result = []
    for suggestion in suggestions:
        payer = db.query(User).filter(User.id == suggestion['payer_id']).first()
        payee = db.query(User).filter(User.id == suggestion['payee_id']).first()
        
        result.append({
            'payer': {
                'id': payer.id,
                'username': payer.username,
                'full_name': payer.full_name
            },
            'payee': {
                'id': payee.id,
                'username': payee.username,
                'full_name': payee.full_name
            },
            'amount': suggestion['amount'],
            'group_id': suggestion['group_id']
        })
    
    return result

@router.put("/{settlement_id}", response_model=SettlementResponse)
def update_settlement(
    settlement_id: int,
    settlement_update: SettlementUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    settlement = db.query(Settlement).filter(Settlement.id == settlement_id).first()
    if not settlement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Settlement not found"
        )
    
    # Only payer or payee can update the settlement
    if settlement.payer_id != current_user.id and settlement.payee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only payer or payee can update this settlement"
        )
    
    update_data = settlement_update.dict(exclude_unset=True)
    
    # If marking as completed, set settled_at timestamp
    if update_data.get("status") == SettlementStatus.COMPLETED:
        update_data["settled_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(settlement, field, value)
    
    db.commit()
    db.refresh(settlement)
    
    return settlement

@router.delete("/{settlement_id}")
def delete_settlement(
    settlement_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    settlement = db.query(Settlement).filter(Settlement.id == settlement_id).first()
    if not settlement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Settlement not found"
        )
    
    # Only payer can delete pending settlements
    if settlement.payer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the payer can delete this settlement"
        )
    
    if settlement.status != SettlementStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending settlements can be deleted"
        )
    
    db.delete(settlement)
    db.commit()
    
    return {"message": "Settlement deleted successfully"}

@router.get("/balance/me")
def get_my_total_balance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get user's balance across all groups
    groups = db.query(GroupMember).filter(GroupMember.user_id == current_user.id).all()
    
    total_balance = Decimal('0')
    group_balances = {}
    
    for membership in groups:
        group_id = membership.group_id
        balance = get_user_balance_in_group(current_user.id, group_id, db)
        total_balance += balance
        
        if balance != 0:
            group_balances[f"group_{group_id}"] = balance
    
    return {
        "total_balance": total_balance,
        "group_balances": group_balances
    }