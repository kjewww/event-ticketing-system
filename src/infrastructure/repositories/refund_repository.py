from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.aggregates.refund import Refund
from src.domain.repositories.refund_repository import RefundRepository

from src.infrastructure.database.models.refund_model import RefundModel
from src.infrastructure.mappers.refund_mapper import RefundMapper


class SqlAlchemyRefundRepository(RefundRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, refund_id: UUID) -> Refund | None:
        model = (
            self.session.query(RefundModel)
            .filter(RefundModel.id == refund_id)
            .first()
        )

        if model is None:
            return None

        return RefundMapper.to_domain(model)

    def get_by_booking_id(self, booking_id: UUID) -> Refund | None:
        model = (
            self.session.query(RefundModel)
            .filter(RefundModel.booking_id == booking_id)
            .first()
        )

        if model is None:
            return None

        return RefundMapper.to_domain(model)

    def save(self, refund: Refund) -> None:
        model = RefundMapper.to_model(refund)
        self.session.merge(model)