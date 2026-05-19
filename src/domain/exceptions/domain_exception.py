class DomainException(Exception):
    pass


class InvalidTicketQuantityError(DomainException):
    pass


class BookingCannotBePaidError(DomainException):
    pass


class BookingPaymentDeadlinePassedError(DomainException):
    pass


class IncorrectPaymentAmountError(DomainException):
    pass


class BookingCannotExpireError(DomainException):
    pass


class TicketCannotBeCheckedInError(DomainException):
    pass


class RefundNotAllowedError(DomainException):
    pass


class RefundStatusError(DomainException):
    pass


class RejectionReasonRequiredError(DomainException):
    pass


class PaymentReferenceRequiredError(DomainException):
    pass


class InvalidEventCapacityError(DomainException):
    pass


class EventCannotBePublishedError(DomainException):
    pass


class EventCannotBeCancelledError(DomainException):
    pass


class EventTicketCategoryQuotaExceededError(DomainException):
    pass


class EventTicketCategoryNotAllowedError(DomainException):
    pass


class InvalidTicketCategoryNameError(DomainException):
    pass


class InvalidTicketCategoryQuotaError(DomainException):
    pass


class BookingNotAllowedError(DomainException):
    pass