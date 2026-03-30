import enum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.adapters.outbound.persistence.models.base import Base


class SettlementStatusEnum(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SettlementModel(Base):
    __tablename__ = "settlements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    payer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    payee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    description = mapped_column(Text, nullable=True)
    status = mapped_column(Enum(SettlementStatusEnum), default=SettlementStatusEnum.PENDING)
    group_id = mapped_column(Integer, ForeignKey("groups.id"), nullable=True)
    settled_at = mapped_column(DateTime(timezone=True), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())

    payer = relationship("UserModel", back_populates="settlements_paid", foreign_keys=[payer_id])
    payee = relationship("UserModel", back_populates="settlements_received", foreign_keys=[payee_id])
    group = relationship("GroupModel")
