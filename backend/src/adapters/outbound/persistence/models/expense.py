import enum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.adapters.outbound.persistence.models.base import Base


class SplitTypeEnum(enum.Enum):
    EQUAL = "equal"
    EXACT = "exact"
    PERCENTAGE = "percentage"


class ExpenseModel(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description = mapped_column(Text, nullable=True)
    amount = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    split_type = mapped_column(Enum(SplitTypeEnum), default=SplitTypeEnum.EQUAL)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"), nullable=False)
    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())

    group = relationship("GroupModel", back_populates="expenses")
    created_by = relationship("UserModel", back_populates="expenses_created")
    splits = relationship("ExpenseSplitModel", back_populates="expense", cascade="all, delete-orphan")


class ExpenseSplitModel(Base):
    __tablename__ = "expense_splits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    expense_id: Mapped[int] = mapped_column(Integer, ForeignKey("expenses.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount = mapped_column(Numeric(10, 2), nullable=False)
    percentage = mapped_column(Numeric(5, 2), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    expense = relationship("ExpenseModel", back_populates="splits")
    user = relationship("UserModel", back_populates="expense_splits")
