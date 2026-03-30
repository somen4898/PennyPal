from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.adapters.outbound.persistence.models.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())

    group_memberships = relationship("GroupMemberModel", back_populates="user")
    expenses_created = relationship(
        "ExpenseModel", back_populates="created_by", foreign_keys="ExpenseModel.created_by_id"
    )
    expense_splits = relationship("ExpenseSplitModel", back_populates="user")
    settlements_paid = relationship(
        "SettlementModel", back_populates="payer", foreign_keys="SettlementModel.payer_id"
    )
    settlements_received = relationship(
        "SettlementModel", back_populates="payee", foreign_keys="SettlementModel.payee_id"
    )
