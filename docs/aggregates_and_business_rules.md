# Implemented Aggregates and Business Rules

## 1. Event Aggregate

The `Event` aggregate is responsible for event lifecycle and ticket category management.

### Main State

- `id`
- `organizer_id`
- `name`
- `description`
- `date_range`
- `location`
- `capacity`
- `status`
- `ticket_categories`

### Business Rules

- Event end date cannot be earlier than start date.
- Event capacity must be greater than zero.
- A newly created event has status `Draft`.
- Event can only be published from `Draft`.
- Event cannot be published if it is `Cancelled`.
- Event can only be published when it has at least one active ticket category.
- Event can only be published when total ticket category quota does not exceed event capacity.
- Published event can be cancelled.
- Completed event cannot be cancelled.
- Cancelling an event disables all ticket categories.

### Related Domain Events

- `EventCreated`
- `EventPublished`
- `EventCancelled`
- `TicketCategoryCreated`
- `TicketCategoryDisabled`

## 2. Ticket Category Entity

`TicketCategory` is an entity inside the `Event` aggregate.

### Main State

- `id`
- `name`
- `price`
- `quota`
- `sales_date_range`
- `is_active`

### Business Rules

- Ticket price cannot be negative.
- Ticket quota must be greater than zero.
- Ticket sales period must be valid.
- Ticket sales period must end before or at the event start date.
- Disabled ticket categories are retained for historical data.

## 3. Booking Aggregate

The `Booking` aggregate is responsible for ticket reservation, payment, ticket issuing, expiry, refund marking, and ticket check-in.

### Main State

- `id`
- `customer_id`
- `customer_name`
- `event_id`
- `ticket_category_id`
- `quantity`
- `unit_price`
- `service_fee`
- `total_price`
- `payment_deadline`
- `status`
- `refund_required`
- `tickets`

### Business Rules

- Booking quantity must be greater than zero.
- Booking can only be created for a published event.
- Booking can only be created for an active ticket category.
- Booking can only be created inside the ticket category sales period.
- Booking quantity must not exceed remaining ticket quota.
- Customer cannot have more than one active booking for the same event.
- New booking has status `PendingPayment`.
- Total price is calculated from unit price multiplied by quantity plus service fee.
- Total price cannot be negative.
- Booking can only be paid while `PendingPayment`.
- Booking cannot be paid after payment deadline.
- Payment amount must match total price.
- Successful payment changes booking status to `Paid`.
- Successful payment issues unique tickets.
- Pending booking can expire after payment deadline.
- Paid booking cannot expire.
- Expired booking releases reserved quota because it is excluded from active reservation count.

### Related Domain Events

- `TicketReserved`
- `BookingPaid`
- `BookingExpired`
- `TicketCheckedIn`

## 4. Ticket Entity

`Ticket` is an entity inside the `Booking` aggregate.

### Main State

- `id`
- `booking_id`
- `event_id`
- `ticket_category_id`
- `ticket_code`
- `status`
- `checked_in_at`

### Business Rules

- Ticket code must be unique.
- Ticket can only be checked in when status is `Active`.
- Checked-in ticket cannot be checked in again.
- Ticket from a refunded booking becomes `Cancelled`.
- Ticket from a cancelled event can become `RefundRequired`.

## 5. Refund Aggregate

The `Refund` aggregate is responsible for refund request state transitions.

### Main State

- `id`
- `booking_id`
- `customer_id`
- `amount`
- `reason`
- `status`
- `rejection_reason`
- `payment_reference`

### Business Rules

- Refund can only be requested for paid bookings.
- Refund cannot be requested when any ticket from the booking has already been checked in.
- Refund can only be requested before refund deadline.
- If an event is cancelled, refund is automatically allowed.
- New refund request has status `Requested`.
- Only requested refund can be approved.
- Approval changes refund status to `Approved`.
- Approval changes related booking to `Refunded`.
- Approval cancels related tickets.
- Only requested refund can be rejected.
- Rejection reason is required.
- Rejected refund leaves related booking as `Paid`.
- Only approved refund can be marked as paid out.
- Payment reference is required when marking refund as paid out.
- Paid-out refund cannot be approved or rejected again.

### Related Domain Events

- `RefundRequested`
- `RefundApproved`
- `RefundRejected`
- `RefundPaidOut`

## 6. Domain Services and Policies

### BookingPolicy

Validates booking creation rules:

- Event must be published.
- Ticket category must be active.
- Requested date must be inside sales period.
- Quantity must be greater than zero.
- Quantity must not exceed remaining quota.
- Customer must not already have an active booking for the same event.

### RefundPolicy

Validates refund request rules:

- Booking must be paid.
- Booking must not have checked-in tickets.
- Refund request must be before deadline unless event is cancelled.

### CheckInPolicy

Validates ticket check-in rules:

- Event must not be cancelled.
- Ticket code must exist.
- Ticket must belong to the selected event.
- Check-in must be within event date.
- Ticket must be active.
- Ticket must not have been checked in before.

### EventCancellationService

Coordinates event cancellation with booking refund marking:

- Cancels event.
- Disables ticket categories.
- Marks paid bookings as requiring refund.
