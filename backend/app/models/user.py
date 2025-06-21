from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    group_memberships = relationship("GroupMember", back_populates="user")
    expenses_created = relationship("Expense", back_populates="created_by", foreign_keys="Expense.created_by_id")
    expense_splits = relationship("ExpenseSplit", back_populates="user")
    settlements_paid = relationship("Settlement", back_populates="payer", foreign_keys="Settlement.payer_id")
    settlements_received = relationship("Settlement", back_populates="payee", foreign_keys="Settlement.payee_id")