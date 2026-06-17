# Event Management System

Event Management System is a backend application for managing events, ticket categories, bookings, ticket payments, ticket check-in, refunds, sales reports, and participant lists.

This project is implemented using **Clean Architecture** and **Domain-Driven Design tactical patterns**. The system separates business logic from application use cases, infrastructure persistence, and REST API controllers.

## Main Features

- Event organizers can create, publish, and cancel events.
- Event organizers can create and disable ticket categories.
- Customers can browse published events and view event details.
- Customers can create bookings and pay for tickets.
- The system issues tickets with unique ticket codes after successful payment.
- Gate officers can validate and check in tickets.
- Customers can request refunds.
- Event organizers can approve or reject refund requests.
- System admins can mark approved refunds as paid out.
- Event organizers can view sales reports and participant lists.

## Architecture

This project follows four main layers:

```text
src/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

### Domain Layer

Contains core business rules and DDD tactical patterns:

- Aggregates
- Entities
- Value objects
- Domain services / policies
- Domain events
- Repository interfaces
- Domain exceptions

### Application Layer

Contains use case orchestration:

- Commands
- Command handlers
- Queries
- Query handlers
- DTOs
- Application service interfaces

### Infrastructure Layer

Contains technical implementations:

- PostgreSQL database connection
- SQLAlchemy models
- SQLAlchemy repository implementations
- Aggregate mappers
- Unit of Work implementation
- Simulated external service adapters
- SQL migration file

### Presentation Layer

Contains REST API implementation:

- FastAPI application
- API routers/controllers
- Request schemas
- Response schemas
- Dependency wiring

## Project Structure

```text
event-management-system/
├── docs/
│   ├── api_documentation.md
│   ├── aggregates_and_business_rules.md
│   ├── clean_architecture_diagram.svg
│   ├── domain_model_diagram.svg
│   └── ubiquitous_language_glossary.md
├── src/
│   ├── application/
│   │   ├── command_handlers/
│   │   ├── commands/
│   │   ├── dto/
│   │   ├── interfaces/
│   │   ├── queries/
│   │   └── query_handlers/
│   ├── domain/
│   │   ├── aggregates/
│   │   ├── entities/
│   │   ├── events/
│   │   ├── exceptions/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── value_objects/
│   ├── infrastructure/
│   │   ├── database/
│   │   │   ├── migrations/
│   │   │   └── models/
│   │   ├── mappers/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── unit_of_work/
│   └── presentation/
│       ├── api/
│       ├── schemas/
│       ├── dependencies.py
│       └── main.py
├── tests/
│   └── domain/
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- pytest
- uv

## PostgreSQL Configuration

Create a PostgreSQL database:

```sql
CREATE DATABASE event_ticketing;
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/event_ticketing
```

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/event_ticketing
```

Do not commit `.env`.

## Installation

From the project root:

```bash
uv sync
```

If dependencies are not installed yet:

```bash
uv add fastapi uvicorn sqlalchemy psycopg python-dotenv pydantic
uv add --dev pytest
```

## Database Migration

The SQL schema file is located at:

```text
src/infrastructure/database/migrations/001_create_event_ticketing_tables.sql
```

There are two ways to prepare the database.

### Option 1: Automatic table creation

The FastAPI application calls `create_tables()` during startup. Run the server:

```bash
uv run python -m uvicorn src.presentation.main:app --reload
```

### Option 2: Manual SQL migration

Open pgAdmin Query Tool and execute:

```text
src/infrastructure/database/migrations/001_create_event_ticketing_tables.sql
```

This creates the required PostgreSQL tables:

- `events`
- `ticket_categories`
- `bookings`
- `tickets`
- `refunds`

## Running the Project

Run the FastAPI server:

```bash
uv run python -m uvicorn src.presentation.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

Root endpoint:

```text
GET /
```

Expected response:

```json
{
  "message": "Event Ticketing System API",
  "status": "running"
}
```

## Running Tests

Run domain unit tests:

```bash
uv run python -m pytest tests/domain -q
```

Expected result:

```text
34 passed
```

The study case requires unit tests for the domain layer. The tests cover event rules, booking rules, ticket check-in rules, refund rules, and domain policies/services.

## Implemented User Stories

| ID | User Story | Status |
|---|---|---|
| US1 | Create Event | Implemented |
| US2 | Publish Event | Implemented |
| US3 | Cancel Event | Implemented |
| US4 | Create Ticket Category | Implemented |
| US5 | Disable Ticket Category | Implemented |
| US6 | View Available Events | Implemented |
| US7 | View Event Details | Implemented |
| US8 | Create Ticket Booking | Implemented |
| US9 | Calculate Booking Total Price | Implemented |
| US10 | Pay Booking | Implemented |
| US11 | Expire Booking | Implemented |
| US12 | View Purchased Tickets | Implemented |
| US13 | Check In Ticket | Implemented |
| US14 | Reject Invalid Ticket Check-in | Implemented |
| US15 | Request Refund | Implemented |
| US16 | Approve Refund | Implemented |
| US17 | Reject Refund | Implemented |
| US18 | Mark Refund as Paid Out | Implemented |
| US19 | View Event Sales Report | Implemented |
| US20 | View Event Participants | Implemented |

## REST API Summary

### Events

| Method | Endpoint | Description |
|---|---|---|
| POST | `/events` | Create event |
| GET | `/events/available` | View published available events |
| GET | `/events/{event_id}` | View event details |
| POST | `/events/{event_id}/publish` | Publish event |
| POST | `/events/{event_id}/cancel` | Cancel event |

### Ticket Categories

| Method | Endpoint | Description |
|---|---|---|
| POST | `/events/{event_id}/ticket-categories` | Create ticket category |
| PATCH | `/events/{event_id}/ticket-categories/{ticket_category_id}/disable` | Disable ticket category |

### Bookings and Payments

| Method | Endpoint | Description |
|---|---|---|
| POST | `/bookings` | Create booking |
| POST | `/bookings/{booking_id}/pay` | Pay booking |
| POST | `/bookings/{booking_id}/expire` | Expire unpaid booking |

### Tickets

| Method | Endpoint | Description |
|---|---|---|
| GET | `/customers/{customer_id}/tickets` | View purchased tickets |
| POST | `/tickets/check-in` | Check in ticket |

### Refunds

| Method | Endpoint | Description |
|---|---|---|
| POST | `/bookings/{booking_id}/refunds` | Request refund |
| POST | `/refunds/{refund_id}/approve` | Approve refund |
| POST | `/refunds/{refund_id}/reject` | Reject refund |
| POST | `/refunds/{refund_id}/paid-out` | Mark refund as paid out |

### Reports

| Method | Endpoint | Description |
|---|---|---|
| GET | `/events/{event_id}/sales-report` | View event sales report |
| GET | `/events/{event_id}/participants` | View event participants |

More detailed API examples are available in:

```text
docs/api_documentation.md
```

## Implemented Aggregates

### Event Aggregate

Responsible for event lifecycle and ticket category management.

Main rules:

- Event cannot be created with invalid date range.
- Event capacity must be greater than zero.
- New event starts as `Draft`.
- Event can only be published if it has at least one active ticket category.
- Total ticket category quota cannot exceed event capacity.
- Cancelled event cannot be published.
- Completed event cannot be cancelled.
- Cancelling an event disables ticket categories.

### Booking Aggregate

Responsible for ticket reservation, payment, expiry, ticket issuing, and ticket check-in.

Main rules:

- Booking quantity must be greater than zero.
- Booking can only be paid while `PendingPayment`.
- Booking cannot be paid after payment deadline.
- Payment amount must match total price.
- Paid booking issues unique tickets.
- Paid booking cannot expire.
- Checked-in ticket cannot be checked in again.

### Refund Aggregate

Responsible for refund request state transitions.

Main rules:

- Refund starts as `Requested`.
- Only requested refund can be approved.
- Only requested refund can be rejected.
- Rejection reason is required.
- Only approved refund can be marked as paid out.
- Payment reference is required when refund is paid out.

More details are available in:

```text
docs/aggregate_business_rules.md
```

## Implemented Domain Events

| Domain Event | Raised When |
|---|---|
| `EventCreated` | Event is created |
| `EventPublished` | Event is published |
| `EventCancelled` | Event is cancelled |
| `TicketCategoryCreated` | Ticket category is created |
| `TicketCategoryDisabled` | Ticket category is disabled |
| `TicketReserved` | Booking is created |
| `BookingPaid` | Booking is paid |
| `BookingExpired` | Booking expires |
| `TicketCheckedIn` | Ticket is checked in |
| `RefundRequested` | Refund is requested |
| `RefundApproved` | Refund is approved |
| `RefundRejected` | Refund is rejected |
| `RefundPaidOut` | Refund is marked as paid out |

## Application Service Interfaces

| Interface | Purpose | Infrastructure Implementation |
|---|---|---|
| `PaymentGateway` | Process booking payment | `FakePaymentGateway` |
| `RefundPaymentService` | Process refund payout | `FakeRefundPaymentService` |
| `NotificationService` | Send notification | `FakeNotificationService` |
| `TicketCodeGenerator` | Generate unique ticket codes | `UUIDTicketCodeGenerator` |
| `UnitOfWork` | Commit/rollback transaction | `SqlAlchemyUnitOfWork` |
| `EventReadRepository` | Read available events and event details | `SqlAlchemyEventReadRepository` |
| `BookingReadRepository` | Read purchased tickets | `SqlAlchemyBookingReadRepository` |
| `ReportReadRepository` | Read sales reports and participants | `SqlAlchemyReportReadRepository` |

## Notes

- This project uses simulated external service adapters instead of real payment, bank, or notification integrations. The interfaces are defined in the application layer, while the implementations are placed in the infrastructure layer.
- Additional documentation and diagrams may be found in the "docs" folder
