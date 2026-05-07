## 1. Project Structure

```
event-ticketing-system
|
├───src
|   |
│   ├───application
│   │   ├───commandHandlers
│   │   ├───commands
│   │   ├───dto
│   │   ├───interfaces
│   │   ├───queries
│   │   └───queryHandlers
|   |
│   ├───domain
│   │   ├───aggregates
│   │   ├───entities
│   │   ├───events
│   │   ├───exceptions
│   │   ├───repositories
│   │   ├───services
│   │   └───valueObjects
|   |
│   ├───infrastructure
│   │   ├───database
│   │   │   ├───migrations
│   │   │   ├───models
│   │   │   └───repositories
│   │   └───externalServices
|   |
│   └───presentation
│       ├───api
│       └───schemas
└───test
    └───domain
```

## 2. Business Rules

### Event Rules

- Event endDate must be after startDate
- Event maxCapacity must be > 0
- Newly created event must have status Draft
- Event can only be published if it has ≥ 1 active ticket category
- Total ticket category quota must not exceed event maxCapacity
- Only Draft → Published transition is allowed (not from Cancelled)
- Only Published event can be cancelled
- Completed event cannot be cancelled
- Cancelling an event marks all paid bookings as requiring refund

### Ticket Category Rules

- Ticket price must be ≥ 0
- Ticket quota must be > 0
- Sales period must end before or at event startDate
- Sum of all category quotas must not exceed event maxCapacity
- Disabled category must be retained for historical purposes
- Customers cannot purchase from an inactive category

### Booking Rules

- Booking can only be created for a Published event
- Booking can only be created within the ticket sales period
- Quantity must be > 0 and ≤ remaining quota
- A customer can only have 1 active booking per event
- New booking status is PendingPayment
- Booking has a payment deadline (15 minutes after creation)
- Payment amount must equal total booking price
- Booking cannot be paid after payment deadline
- Paid booking cannot expire
- Expiring a booking releases the reserved ticket quota

### Ticket Rules

- Tickets are issued only after a booking is paid
- Each ticket must have a unique ticket code
- Ticket status: Active → CheckedIn or Cancelled
- Check-in only on event day or within allowed window
- An already checked-in ticket cannot be checked in again
- Check-in only allowed for the matching event

### Refund Rules

- Refund only for Paid bookings
- Refund cannot be requested if any ticket from booking is CheckedIn
- Refund must be requested before refund deadline
- Cancelled event → refund is automatically allowed
- Approving a refund changes booking → Refunded, tickets → Cancelled
- Rejecting a refund requires a rejection reason
- Rejected refund leaves booking as Paid, tickets as Active
- Payout requires payment reference; status → PaidOut
- PaidOut refund cannot be modified

## 3. Domain Model Draft



## 4. Ubiquitous Language Glossary

| Term | Meaning |
|--|--|
|**Event**| An activity organized by an Event Organizer and attended by customers.|
|**Event Organizer**| A user who creates and manages events.|
|**Customer**| A user who books and purchases tickets.|
|**Gate Officer**| A user who validates tickets during event check-in.|
|**Ticket Category**| A type of ticket, such as Regular, VIP, or Early Bird.|
|**Quota**| The maximum number of tickets available in a ticket category.|
|**Booking**| A temporary reservation before payment is completed.|
|**Pending Payment**|A booking status indicating that payment has not been completed.|
|**Paid**| A booking status indicating that payment has been completed.|
|**Expired**| A booking status indicating that the payment deadline has passed.|
|**Ticket**| Proof of attendance generated after a booking is paid.|
|**Ticket Code**| A unique code used to identify and validate a ticket.|
|**Check-in**| The process of validating a ticket when a participant enters the event venue.|
|**Refund**| The process of returning money to a customer.|
|**Money**| A value object representing an amount and currency.|
|**Sales Period**| The period during which a ticket category can be purchased.|
|**Payment Deadline**| The deadline for completing payment.| 
