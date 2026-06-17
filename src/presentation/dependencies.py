from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.command_handlers.approve_refund_handler import (
    ApproveRefundCommandHandler,
)
from src.application.command_handlers.cancel_event_handler import (
    CancelEventCommandHandler,
)
from src.application.command_handlers.check_in_ticket_handler import (
    CheckInTicketCommandHandler,
)
from src.application.command_handlers.create_booking_handler import (
    CreateBookingCommandHandler,
)
from src.application.command_handlers.create_event_handler import (
    CreateEventCommandHandler,
)
from src.application.command_handlers.create_ticket_category_handler import (
    CreateTicketCategoryCommandHandler,
)
from src.application.command_handlers.disable_ticket_category_handler import (
    DisableTicketCategoryCommandHandler,
)
from src.application.command_handlers.expire_booking_handler import (
    ExpireBookingCommandHandler,
)
from src.application.command_handlers.mark_refund_paid_out_handler import (
    MarkRefundPaidOutCommandHandler,
)
from src.application.command_handlers.pay_booking_handler import (
    PayBookingCommandHandler,
)
from src.application.command_handlers.publish_event_handler import (
    PublishEventCommandHandler,
)
from src.application.command_handlers.reject_refund_handler import (
    RejectRefundCommandHandler,
)
from src.application.command_handlers.request_refund_handler import (
    RequestRefundCommandHandler,
)
from src.application.query_handlers.view_available_events_handler import (
    ViewAvailableEventsQueryHandler,
)
from src.application.query_handlers.view_event_details_handler import (
    ViewEventDetailsQueryHandler,
)
from src.application.query_handlers.view_event_participants_handler import (
    ViewEventParticipantsQueryHandler,
)
from src.application.query_handlers.view_event_sales_report_handler import (
    ViewEventSalesReportQueryHandler,
)
from src.application.query_handlers.view_purchased_tickets_handler import (
    ViewPurchasedTicketsQueryHandler,
)

from src.domain.services.event_cancellation_service import EventCancellationService

from src.infrastructure.database import get_db
from src.infrastructure.repositories import (
    SqlAlchemyBookingReadRepository,
    SqlAlchemyBookingRepository,
    SqlAlchemyEventReadRepository,
    SqlAlchemyEventRepository,
    SqlAlchemyRefundRepository,
    SqlAlchemyReportReadRepository,
)
from src.infrastructure.services import (
    FakeNotificationService,
    FakePaymentGateway,
    FakeRefundPaymentService,
    UUIDTicketCodeGenerator,
)
from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


def get_event_repository(
    db: Session = Depends(get_db),
) -> SqlAlchemyEventRepository:
    return SqlAlchemyEventRepository(db)


def get_booking_repository(
    db: Session = Depends(get_db),
) -> SqlAlchemyBookingRepository:
    return SqlAlchemyBookingRepository(db)


def get_refund_repository(
    db: Session = Depends(get_db),
) -> SqlAlchemyRefundRepository:
    return SqlAlchemyRefundRepository(db)


def get_event_read_repository(
    db: Session = Depends(get_db),
) -> SqlAlchemyEventReadRepository:
    return SqlAlchemyEventReadRepository(db)


def get_booking_read_repository(
    db: Session = Depends(get_db),
) -> SqlAlchemyBookingReadRepository:
    return SqlAlchemyBookingReadRepository(db)


def get_report_read_repository(
    db: Session = Depends(get_db),
) -> SqlAlchemyReportReadRepository:
    return SqlAlchemyReportReadRepository(db)


def get_unit_of_work(
    db: Session = Depends(get_db),
) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(db)


def get_payment_gateway() -> FakePaymentGateway:
    return FakePaymentGateway()


def get_refund_payment_service() -> FakeRefundPaymentService:
    return FakeRefundPaymentService()


def get_notification_service() -> FakeNotificationService:
    return FakeNotificationService()


def get_ticket_code_generator() -> UUIDTicketCodeGenerator:
    return UUIDTicketCodeGenerator()


def get_create_event_handler(
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> CreateEventCommandHandler:
    return CreateEventCommandHandler(
        event_repository=event_repository,
        unit_of_work=unit_of_work,
    )


def get_publish_event_handler(
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> PublishEventCommandHandler:
    return PublishEventCommandHandler(
        event_repository=event_repository,
        unit_of_work=unit_of_work,
    )


def get_cancel_event_handler(
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    booking_repository: SqlAlchemyBookingRepository = Depends(get_booking_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> CancelEventCommandHandler:
    return CancelEventCommandHandler(
        event_repository=event_repository,
        booking_repository=booking_repository,
        unit_of_work=unit_of_work,
        event_cancellation_service=EventCancellationService(),
    )


def get_create_ticket_category_handler(
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> CreateTicketCategoryCommandHandler:
    return CreateTicketCategoryCommandHandler(
        event_repository=event_repository,
        unit_of_work=unit_of_work,
    )


def get_disable_ticket_category_handler(
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> DisableTicketCategoryCommandHandler:
    return DisableTicketCategoryCommandHandler(
        event_repository=event_repository,
        unit_of_work=unit_of_work,
    )


def get_view_available_events_handler(
    event_read_repository: SqlAlchemyEventReadRepository = Depends(
        get_event_read_repository
    ),
) -> ViewAvailableEventsQueryHandler:
    return ViewAvailableEventsQueryHandler(
        event_read_repository=event_read_repository,
    )


def get_view_event_details_handler(
    event_read_repository: SqlAlchemyEventReadRepository = Depends(
        get_event_read_repository
    ),
) -> ViewEventDetailsQueryHandler:
    return ViewEventDetailsQueryHandler(
        event_read_repository=event_read_repository,
    )


def get_create_booking_handler(
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    booking_repository: SqlAlchemyBookingRepository = Depends(get_booking_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> CreateBookingCommandHandler:
    return CreateBookingCommandHandler(
        event_repository=event_repository,
        booking_repository=booking_repository,
        unit_of_work=unit_of_work,
    )


def get_pay_booking_handler(
    booking_repository: SqlAlchemyBookingRepository = Depends(get_booking_repository),
    payment_gateway: FakePaymentGateway = Depends(get_payment_gateway),
    ticket_code_generator: UUIDTicketCodeGenerator = Depends(
        get_ticket_code_generator
    ),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> PayBookingCommandHandler:
    return PayBookingCommandHandler(
        booking_repository=booking_repository,
        payment_gateway=payment_gateway,
        ticket_code_generator=ticket_code_generator,
        unit_of_work=unit_of_work,
    )


def get_expire_booking_handler(
    booking_repository: SqlAlchemyBookingRepository = Depends(get_booking_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> ExpireBookingCommandHandler:
    return ExpireBookingCommandHandler(
        booking_repository=booking_repository,
        unit_of_work=unit_of_work,
    )


def get_check_in_ticket_handler(
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    booking_repository: SqlAlchemyBookingRepository = Depends(get_booking_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> CheckInTicketCommandHandler:
    return CheckInTicketCommandHandler(
        event_repository=event_repository,
        booking_repository=booking_repository,
        unit_of_work=unit_of_work,
    )


def get_request_refund_handler(
    booking_repository: SqlAlchemyBookingRepository = Depends(get_booking_repository),
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    refund_repository: SqlAlchemyRefundRepository = Depends(get_refund_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> RequestRefundCommandHandler:
    return RequestRefundCommandHandler(
        booking_repository=booking_repository,
        event_repository=event_repository,
        refund_repository=refund_repository,
        unit_of_work=unit_of_work,
    )


def get_approve_refund_handler(
    refund_repository: SqlAlchemyRefundRepository = Depends(get_refund_repository),
    booking_repository: SqlAlchemyBookingRepository = Depends(get_booking_repository),
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> ApproveRefundCommandHandler:
    return ApproveRefundCommandHandler(
        refund_repository=refund_repository,
        booking_repository=booking_repository,
        event_repository=event_repository,
        unit_of_work=unit_of_work,
    )


def get_reject_refund_handler(
    refund_repository: SqlAlchemyRefundRepository = Depends(get_refund_repository),
    booking_repository: SqlAlchemyBookingRepository = Depends(get_booking_repository),
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> RejectRefundCommandHandler:
    return RejectRefundCommandHandler(
        refund_repository=refund_repository,
        booking_repository=booking_repository,
        event_repository=event_repository,
        unit_of_work=unit_of_work,
    )


def get_mark_refund_paid_out_handler(
    refund_repository: SqlAlchemyRefundRepository = Depends(get_refund_repository),
    refund_payment_service: FakeRefundPaymentService = Depends(
        get_refund_payment_service
    ),
    unit_of_work: SqlAlchemyUnitOfWork = Depends(get_unit_of_work),
) -> MarkRefundPaidOutCommandHandler:
    return MarkRefundPaidOutCommandHandler(
        refund_repository=refund_repository,
        refund_payment_service=refund_payment_service,
        unit_of_work=unit_of_work,
    )


def get_view_purchased_tickets_handler(
    booking_read_repository: SqlAlchemyBookingReadRepository = Depends(
        get_booking_read_repository
    ),
) -> ViewPurchasedTicketsQueryHandler:
    return ViewPurchasedTicketsQueryHandler(
        booking_read_repository=booking_read_repository,
    )


def get_view_event_sales_report_handler(
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    report_read_repository: SqlAlchemyReportReadRepository = Depends(
        get_report_read_repository
    ),
) -> ViewEventSalesReportQueryHandler:
    return ViewEventSalesReportQueryHandler(
        event_repository=event_repository,
        report_read_repository=report_read_repository,
    )


def get_view_event_participants_handler(
    event_repository: SqlAlchemyEventRepository = Depends(get_event_repository),
    report_read_repository: SqlAlchemyReportReadRepository = Depends(
        get_report_read_repository
    ),
) -> ViewEventParticipantsQueryHandler:
    return ViewEventParticipantsQueryHandler(
        event_repository=event_repository,
        report_read_repository=report_read_repository,
    )