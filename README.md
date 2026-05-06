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
```

## 2. Business Rules

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