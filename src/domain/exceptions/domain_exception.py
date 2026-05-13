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