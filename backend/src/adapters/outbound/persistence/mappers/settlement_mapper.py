from decimal import Decimal

from src.adapters.outbound.persistence.models.settlement import (
    SettlementModel,
    SettlementStatusEnum,
)
from src.domain.entities.settlement import Settlement, SettlementStatus


class SettlementMapper:
    @staticmethod
    def to_domain(model: SettlementModel) -> Settlement:
        return Settlement(
            id=model.id,
            payer_id=model.payer_id,
            payee_id=model.payee_id,
            amount=Decimal(str(model.amount)),
            status=SettlementStatus(model.status.value),
            currency=model.currency,
            description=model.description,
            group_id=model.group_id,
            settled_at=model.settled_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Settlement) -> SettlementModel:
        return SettlementModel(
            id=entity.id if entity.id else None,
            payer_id=entity.payer_id,
            payee_id=entity.payee_id,
            amount=entity.amount,
            currency=entity.currency,
            description=entity.description,
            status=SettlementStatusEnum(entity.status.value),
            group_id=entity.group_id,
            settled_at=entity.settled_at,
        )
